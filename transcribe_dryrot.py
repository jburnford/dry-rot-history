#!/usr/bin/env python3
"""
Batch transcription of James Sowerby dry rot papers using Gemini API.

Documents from the Natural History Museum relating to Sowerby's investigation
of dry rot aboard HMS Queen Charlotte (1810), 1812-1815.

Output: JSON files with per-page structured transcriptions in markdown.

Usage:
    # Process all PDFs
    python transcribe_dryrot.py --all

    # Process specific file
    python transcribe_dryrot.py --file "B96 - Notebook of observations....pdf"

    # List pending files
    python transcribe_dryrot.py --list

    # Adjust pages per chunk (default: 3)
    python transcribe_dryrot.py --all --pages-per-chunk 5
"""

import os
import sys
import json
import time
import re
import argparse
import tempfile
from pathlib import Path
from datetime import datetime

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

try:
    import google.generativeai as genai
    from google.generativeai.types import HarmCategory, HarmBlockThreshold
except ImportError:
    print("Please install the Google AI SDK:")
    print("  pip install google-generativeai python-dotenv")
    sys.exit(1)

SAFETY_SETTINGS = {
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Please install PyMuPDF for PDF chunking:")
    print("  pip install pymupdf")
    sys.exit(1)


TRANSCRIPTION_PROMPT = """You are an expert paleographer specializing in early 19th-century British handwriting.

These are pages {start_page}-{end_page} of a document from the Natural History Museum archive relating to James Sowerby's (1757-1822, F.L.S.) investigation of dry rot aboard HMS Queen Charlotte, 1812-1815, commissioned by the Navy Board.

Key names: James Sowerby, Lionel Lukin, J. Knowles, F.T. Hartwell, H. Legge, T.B. Thompson, George Brettingham Sowerby, Commissioner Cunningham.

Provide a faithful transcription of each page. Use these conventions:
- Preserve original spelling, capitalization, and punctuation
- Use ^ for superscript (e.g., "17^th July")
- Use [text crossed out: words] for deleted text still legible
- Use [inserted above: words] for interlineations/additions above the line
- Use [unclear: best guess?] for difficult passages
- Use [...] for completely illegible sections
- Use [sketch: description] for any drawings or diagrams
- Note any visible archival markings, page numbers, or reference codes
- If a page is blank or contains only a cover/envelope, note that briefly

Focus on accuracy - mark uncertain readings rather than guessing.

Return your response as a JSON array with one object per page. Each object must have:
- "page": the page number (integer)
- "transcription": the transcription text in markdown format

Example:
```json
[
  {{"page": 1, "transcription": "Navy Office 15^th July 1812\\n\\nSir,\\n\\nI have the commands..."}},
  {{"page": 2, "transcription": "[blank page]"}}
]
```

Return ONLY the JSON array, no other text."""


def load_api_key(base_dir: Path) -> str:
    """Load API key from .env file or environment."""
    # Try .env file first
    env_path = base_dir / ".env"
    if env_path.exists():
        if load_dotenv:
            load_dotenv(env_path)
        else:
            # Manual .env parsing as fallback
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, val = line.split("=", 1)
                        os.environ[key.strip()] = val.strip()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found")
        print(f"  Set it in {env_path} or as an environment variable")
        sys.exit(1)
    return api_key


def find_all_pdfs(base_dir: Path) -> list:
    """Recursively find all PDFs in the directory tree."""
    return sorted(base_dir.rglob("*.pdf"))


def get_output_path(pdf_path: Path) -> Path:
    """Get the transcription output path for a PDF (same dir, .json extension)."""
    return pdf_path.with_suffix(".json")


def get_processed_pdfs(base_dir: Path) -> set:
    """Find PDFs that have completed transcription JSON files.

    Only counts files with status 'complete'. Partial results are
    treated as pending so they get resumed.
    """
    processed = set()
    for pdf in find_all_pdfs(base_dir):
        out = get_output_path(pdf)
        if out.exists() and out.stat().st_size > 0:
            try:
                with open(out) as f:
                    data = json.load(f)
                # Legacy files without status field are assumed complete
                if data.get("status", "complete") == "complete":
                    processed.add(pdf)
            except (json.JSONDecodeError, KeyError):
                pass
    return processed


def get_pending_pdfs(base_dir: Path) -> list:
    """Get list of PDFs that haven't been transcribed yet."""
    processed = get_processed_pdfs(base_dir)
    all_pdfs = find_all_pdfs(base_dir)
    return [p for p in all_pdfs if p not in processed]


def get_page_count(pdf_path: Path) -> int:
    """Get the number of pages in a PDF."""
    doc = fitz.open(pdf_path)
    count = len(doc)
    doc.close()
    return count


def extract_pages(pdf_path: Path, start_page: int, end_page: int, output_path: Path):
    """Extract a range of pages from a PDF to a new file."""
    doc = fitz.open(pdf_path)
    new_doc = fitz.open()
    for page_num in range(start_page - 1, min(end_page, len(doc))):
        new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
    new_doc.save(output_path)
    new_doc.close()
    doc.close()


def parse_json_response(text: str, start_page: int, end_page: int) -> list:
    """Parse the JSON array from Gemini's response, with fallback."""
    # Try to extract JSON from markdown code blocks first
    match = re.search(r'```(?:json)?\s*\n(.*?)\n```', text, re.DOTALL)
    if match:
        text_to_parse = match.group(1)
    else:
        text_to_parse = text.strip()

    try:
        pages = json.loads(text_to_parse)
        if isinstance(pages, list):
            return pages
    except json.JSONDecodeError:
        pass

    # Fallback: wrap raw text as a single chunk
    return [{"page": p, "transcription": text if p == start_page else "[see previous page]"}
            for p in range(start_page, end_page + 1)]


def transcribe_chunk(chunk_path: Path, model, start_page: int, end_page: int, max_retries: int = 3) -> list:
    """Transcribe a PDF chunk using Gemini. Returns list of page dicts."""
    uploaded_file = None
    prompt = TRANSCRIPTION_PROMPT.format(start_page=start_page, end_page=end_page)

    for attempt in range(max_retries):
        try:
            if uploaded_file is None:
                uploaded_file = genai.upload_file(chunk_path)
                while uploaded_file.state.name == "PROCESSING":
                    time.sleep(2)
                    uploaded_file = genai.get_file(uploaded_file.name)
                if uploaded_file.state.name == "FAILED":
                    raise Exception("File processing failed")

            response = model.generate_content(
                [prompt, uploaded_file],
                safety_settings=SAFETY_SETTINGS
            )

            try:
                genai.delete_file(uploaded_file.name)
            except:
                pass

            return parse_json_response(response.text, start_page, end_page)

        except Exception as e:
            error_str = str(e)
            if attempt < max_retries - 1 and any(x in error_str for x in ['504', '503', '500', 'timeout', 'Cancelled']):
                wait_time = (attempt + 1) * 10
                print(f"    Retry {attempt + 1}/{max_retries} in {wait_time}s...")
                time.sleep(wait_time)
            else:
                if uploaded_file:
                    try:
                        genai.delete_file(uploaded_file.name)
                    except:
                        pass
                raise


def save_partial_result(output_path: Path, result: dict):
    """Save current transcription state to disk (incremental save)."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)


def load_partial_result(output_path: Path) -> dict | None:
    """Load a partial transcription result if one exists."""
    if not output_path.exists() or output_path.stat().st_size == 0:
        return None
    try:
        with open(output_path) as f:
            data = json.load(f)
        if data.get("status") == "partial":
            return data
    except (json.JSONDecodeError, KeyError):
        pass
    return None


def transcribe_pdf(pdf_path: Path, base_dir: Path, model, pages_per_chunk: int = 3, max_retries: int = 3) -> dict:
    """Transcribe a PDF into structured JSON with per-page chunks.

    Saves progress after each chunk so work survives crashes.
    Resumes from last completed chunk if a partial result exists.
    """
    page_count = get_page_count(pdf_path)
    folder_name = pdf_path.parent.name
    rel_path = str(pdf_path.relative_to(base_dir))
    output_path = get_output_path(pdf_path)

    print(f"  {page_count} pages, chunking by {pages_per_chunk}")

    # Check for partial results from a previous interrupted run
    partial = load_partial_result(output_path)
    if partial:
        all_pages = partial["pages"]
        completed_pages = {p["page"] for p in all_pages}
        print(f"  Resuming from partial result ({len(completed_pages)} pages already done)")
    else:
        all_pages = []
        completed_pages = set()

    result = {
        "source_file": pdf_path.name,
        "source_path": rel_path,
        "archive_folder": folder_name,
        "total_pages": page_count,
        "transcription_date": datetime.now().isoformat(),
        "status": "partial",
        "pages": all_pages
    }

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir = Path(temp_dir)
        chunk_num = 0

        for start_page in range(1, page_count + 1, pages_per_chunk):
            chunk_num += 1
            end_page = min(start_page + pages_per_chunk - 1, page_count)

            # Skip chunks already completed in a previous run
            chunk_pages = set(range(start_page, end_page + 1))
            if chunk_pages.issubset(completed_pages):
                print(f"    Chunk {chunk_num}: pages {start_page}-{end_page}... Skipped (already done)")
                continue

            print(f"    Chunk {chunk_num}: pages {start_page}-{end_page}...", end=" ", flush=True)

            chunk_path = temp_dir / f"chunk_{chunk_num}.pdf"
            extract_pages(pdf_path, start_page, end_page, chunk_path)

            try:
                page_results = transcribe_chunk(chunk_path, model, start_page, end_page, max_retries)
                all_pages.extend(page_results)
                print("Done")
            except Exception as e:
                print(f"ERROR: {e}")
                for p in range(start_page, end_page + 1):
                    all_pages.append({
                        "page": p,
                        "transcription": f"[TRANSCRIPTION FAILED: {e}]"
                    })

            # Save after every chunk so progress survives crashes
            result["transcription_date"] = datetime.now().isoformat()
            save_partial_result(output_path, result)

            time.sleep(2)

    # Mark as complete
    result["status"] = "complete"
    result["transcription_date"] = datetime.now().isoformat()
    save_partial_result(output_path, result)

    return result


def save_progress(base_dir: Path, processed_this_run: list, failed: list):
    """Save progress log."""
    log_file = base_dir / "transcription_log.json"

    log_data = {
        "last_run": datetime.now().isoformat(),
        "processed_this_run": processed_this_run,
        "failed": failed
    }

    if log_file.exists():
        try:
            with open(log_file) as f:
                existing = json.load(f)
            if "runs" not in existing:
                existing = {"runs": [existing]}
            existing["runs"].append(log_data)
            log_data = existing
        except:
            log_data = {"runs": [log_data]}
    else:
        log_data = {"runs": [log_data]}

    with open(log_file, "w") as f:
        json.dump(log_data, f, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="Transcribe Sowerby dry rot papers using Gemini"
    )
    parser.add_argument("--batch-size", "-n", type=int, default=10,
                        help="Number of PDFs to process (default: 10)")
    parser.add_argument("--all", action="store_true",
                        help="Process all remaining PDFs")
    parser.add_argument("--file", "-f", type=str,
                        help="Process a specific PDF file")
    parser.add_argument("--list", "-l", action="store_true",
                        help="List pending files and exit")
    parser.add_argument("--model", "-m", type=str, default="models/gemini-3.1-pro-preview",
                        help="Gemini model to use")
    parser.add_argument("--temperature", "-t", type=float, default=0.2,
                        help="Temperature (0.0-1.0, default: 0.2)")
    parser.add_argument("--pages-per-chunk", "-p", type=int, default=3,
                        help="Max pages per API call (default: 3)")
    args = parser.parse_args()

    base_dir = Path(__file__).parent
    api_key = load_api_key(base_dir)
    genai.configure(api_key=api_key)

    # List mode
    if args.list:
        pending = get_pending_pdfs(base_dir)
        processed = get_processed_pdfs(base_dir)
        total_pages = 0
        print(f"Processed: {len(processed)} files")
        print(f"Pending: {len(pending)} files")
        if pending:
            print("\nPending files:")
            for p in pending:
                pc = get_page_count(p)
                total_pages += pc
                rel = p.relative_to(base_dir)
                print(f"  {rel} ({pc} pages)")
            print(f"\nTotal pending pages: {total_pages}")
        return

    # Determine files to process
    if args.file:
        pdf_path = base_dir / args.file
        if not pdf_path.exists():
            matches = list(base_dir.rglob(args.file))
            if matches:
                pdf_path = matches[0]
            else:
                print(f"Error: File not found: {args.file}")
                sys.exit(1)
        to_process = [pdf_path]
    else:
        pending = get_pending_pdfs(base_dir)
        if not pending:
            print("All PDFs have been transcribed!")
            return

        if args.all:
            to_process = pending
        else:
            to_process = pending[:args.batch_size]

    total_pages = sum(get_page_count(p) for p in to_process)
    print(f"Will process {len(to_process)} PDF(s) ({total_pages} pages)")
    print(f"Model: {args.model}")
    print(f"Temperature: {args.temperature}")
    print(f"Pages per chunk: {args.pages_per_chunk}")
    print(f"Output format: JSON (per-page structured)")
    print()

    generation_config = genai.GenerationConfig(
        temperature=args.temperature,
        top_p=0.95,
        top_k=40,
    )
    model = genai.GenerativeModel(args.model, generation_config=generation_config)

    processed_this_run = []
    failed = []

    for i, pdf_path in enumerate(to_process, 1):
        rel = pdf_path.relative_to(base_dir)
        print(f"[{i}/{len(to_process)}] {rel}")

        try:
            result = transcribe_pdf(pdf_path, base_dir, model, args.pages_per_chunk)

            print(f"  Saved to {get_output_path(pdf_path).name} ({len(result['pages'])} pages)")
            processed_this_run.append(str(rel))

            if i < len(to_process):
                time.sleep(2)

        except Exception as e:
            print(f"  ERROR: {e}")
            failed.append({"file": str(rel), "error": str(e)})

    save_progress(base_dir, processed_this_run, failed)

    print()
    print(f"Completed: {len(processed_this_run)}")
    if failed:
        print(f"Failed: {len(failed)}")
        for f in failed:
            print(f"  {f['file']}: {f['error']}")

    remaining = len(get_pending_pdfs(base_dir))
    if remaining > 0:
        print(f"\nRemaining: {remaining} files")


if __name__ == "__main__":
    main()
