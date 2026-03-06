#!/bin/bash
# reproduce.sh — Regenerate all figures and analysis for Foundation Models review paper
# Expected runtime: ~30–60 minutes (analysis + figure generation)
# Usage: bash results/reproduce.sh
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
CODE_DIR="$ROOT_DIR/code"
DATA_DIR="$ROOT_DIR/data"
FIG_DIR="$ROOT_DIR/paper/figures"

echo "=== Foundation Models for Clean Energy — Full Reproduction Script ==="
echo "Started at: $(date)"

echo "ROOT: $ROOT_DIR"

# Install dependencies
if [ -f "$CODE_DIR/requirements.txt" ]; then
    pip install -r "$CODE_DIR/requirements.txt" -q
fi

# Ensure required data exists
if [ ! -f "$DATA_DIR/openalex_papers.json" ]; then
    echo "Missing $DATA_DIR/openalex_papers.json"
    echo "Run: python3 code/data_processing/collect_papers.py (network required)"
    exit 1
fi

if [ ! -f "$DATA_DIR/classified_papers.csv" ]; then
    echo "Classified papers not found — generating..."
    python3 "$CODE_DIR/data_processing/classify_papers.py"
fi

mkdir -p "$FIG_DIR"

# Step 1: Analysis
echo "[1/3] Running analysis scripts..."
python3 "$CODE_DIR/analysis/summary_statistics.py"
python3 "$CODE_DIR/analysis/scientometrics.py"
python3 "$CODE_DIR/analysis/cost_performance.py"

if [ "${SKIP_NETWORK:-}" != "1" ]; then
    python3 "$CODE_DIR/analysis/reproducibility_audit.py"
else
    echo "Skipping reproducibility_audit.py (SKIP_NETWORK=1)"
fi

# Step 2: Generate figures
echo "[2/3] Generating figures..."
for fig_script in "$CODE_DIR"/figures/fig_*.py; do
    if [ -f "$fig_script" ]; then
        echo "  Running $fig_script..."
        python3 "$fig_script"
    fi
done

# Step 3: Sanity check outputs
echo "[3/3] Verifying figure outputs..."
FIG_COUNT=$(ls -1 "$FIG_DIR" 2>/dev/null | wc -l | tr -d ' ')
if [ "$FIG_COUNT" -eq 0 ]; then
    echo "No figures found in $FIG_DIR"
    exit 1
fi

echo "Figures generated: $FIG_COUNT"

echo "=== Reproduction complete at $(date) ==="
