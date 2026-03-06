# Code — Foundation Models for Clean Energy Systems

This directory contains all source code required to reproduce the results and figures in the paper.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Reproduce Results

From the repository root:

```bash
bash results/reproduce.sh
```

Outputs:
- Figures are saved to `paper/figures/`
- Intermediate and final result JSONs are saved to `code/results/`

## Notes
- The reproduction script uses the data already present in `data/`.
- If you need to refresh the OpenAlex dataset, run `code/data_processing/collect_papers.py` (network required).
