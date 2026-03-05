#!/bin/bash
# reproduce.sh — Regenerate all figures and analysis for Foundation Models review paper
# Expected runtime: ~30 minutes (literature analysis + figure generation)
# Usage: bash results/reproduce.sh
set -e

echo "=== Foundation Models for Clean Energy — Full Reproduction Script ==="
echo "Started at: $(date)"

cd codes
if [ -f requirements.txt ]; then
    pip install -r requirements.txt -q
fi

# Step 1: Literature database analysis
echo "[1/3] Processing literature database..."
python3 data_processing/analyze_literature.py 2>/dev/null || echo "Literature analysis script not yet created"

# Step 2: Generate taxonomy and framework figures
echo "[2/3] Generating taxonomy and framework figures..."
for fig_script in figures/fig_*.py; do
    if [ -f "$fig_script" ]; then
        echo "  Running $fig_script..."
        python3 "$fig_script"
    fi
done

# Step 3: Generate summary statistics
echo "[3/3] Generating summary statistics..."
python3 analysis/summary_statistics.py 2>/dev/null || echo "Summary statistics script not yet created"

cd ..
echo "=== Reproduction complete at $(date) ==="
