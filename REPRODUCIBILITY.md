# Reproducibility Checklist — Foundation Models for Clean Energy Systems

## Code
- [x] All dependencies listed in `code/requirements.txt`
- [x] Setup instructions in `code/README.md`
- [x] Code runs on a clean environment without modification
- [x] Literature search queries documented and reproducible

## Data
- [x] Literature database (search results, screening records) available
- [x] PRISMA flow data documented
- [x] Coding scheme and inter-rater reliability data available
- [x] Data sources, collection dates, and licenses documented in `data/README.md`

## Results
- [x] `results/reproduce.sh` exists and regenerates all figures/tables
- [x] Script exits with code 0 on success
- [x] Generated outputs match paper's figures and tables

## Process Log
- [x] `process-log/README.md` describes research workflow
- [x] AI session logs included in `process-log/ai-sessions/`
- [x] Human decisions documented in `process-log/human-decisions/`
- [x] All AI tools and versions disclosed

## Licensing
- [x] Paper: CC-BY 4.0
- [x] Code: MIT License
- [x] Data: CC-BY 4.0

## Notes
- Benchmark experiments (Chronos, CLIP, RAG) require additional packages beyond `code/requirements.txt` (torch, chronos, open_clip, sentence-transformers, faiss-cpu). These are documented in `code/README.md` but are not installed by `reproduce.sh` as the experiments depend on GPU/Ollama infrastructure. The reproducible outputs are the analysis figures and tables generated from pre-computed results.
