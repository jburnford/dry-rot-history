#!/bin/bash
#SBATCH --account=hpc_p_clifford
#SBATCH --gpus-per-node=a100:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --job-name=dryrot_ner
#SBATCH --output=dryrot_ner_%j.out

echo "=== EarlyModernNER - Sowerby Dry Rot Papers (442 pages) ==="
echo "Job ID: $SLURM_JOB_ID, Host: $(hostname), Date: $(date)"

module load gcc/12.3 cuda/12.6

OLMOCR_BASE="$HOME/olmocr_plato"
source "$OLMOCR_BASE/venv/bin/activate"

# Install earlymodernner + missing dep if needed
pip show earlymodernner >/dev/null 2>&1 || pip install earlymodernner 2>&1 | tail -3
pip show python-dateutil >/dev/null 2>&1 || pip install python-dateutil 2>&1 | tail -3

JOB_DIR="$HOME/projects/def-jic823/dryrot_ner"
INPUT="$JOB_DIR/dryrot_for_ner.jsonl"
OUTPUT_JSONL="$JOB_DIR/ner_results.jsonl"
OUTPUT_CSV="$JOB_DIR/ner_results.csv"

echo "Input: $(wc -l < "$INPUT") pages"
echo ""

echo "--- Running NER (JSONL) ---"
time python -m earlymodernner \
    --input "$INPUT" \
    --output "$OUTPUT_JSONL" \
    --verbose
echo ""

echo "--- Running NER (CSV) ---"
time python -m earlymodernner \
    --input "$INPUT" \
    --output "$OUTPUT_CSV" \
    --csv
echo ""

echo "--- Summary ---"
if [ -f "$OUTPUT_JSONL" ]; then
    echo "JSONL: $(wc -l < "$OUTPUT_JSONL") documents"
    echo "CSV: $(wc -l < "$OUTPUT_CSV") rows"
    python3 -c "
import json
from collections import Counter
counts = Counter()
with open('$OUTPUT_JSONL') as f:
    for line in f:
        obj = json.loads(line)
        for etype, n in obj.get('entity_counts', {}).items():
            counts[etype] += n if isinstance(n, int) else len(n)
print('Entity counts:')
for t, c in counts.most_common():
    print(f'  {t}: {c}')
print(f'  TOTAL: {sum(counts.values())}')
"
else
    echo "ERROR: No output produced"
fi

echo "=== Done: $(date) ==="
