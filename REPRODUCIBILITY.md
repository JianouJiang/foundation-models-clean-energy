# Reproducibility Checklist — Foundation Models for Clean Energy Systems

## Code
- [x] All dependencies listed in `code/requirements.txt`
- [x] Setup instructions in `code/README.md`
- [ ] Code runs on a clean environment without modification
- [ ] Literature search queries documented and reproducible

## Data
- [x] Literature database (search results, screening records) available
- [ ] PRISMA flow data documented
- [ ] Coding scheme and inter-rater reliability data available

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
