# Reproducibility Checklist — Foundation Models for Clean Energy Systems

## Code
- [ ] All dependencies listed in `codes/requirements.txt`
- [ ] Setup instructions in `codes/README.md`
- [ ] Code runs on a clean environment without modification
- [ ] Literature search queries documented and reproducible

## Data
- [ ] Literature database (search results, screening records) available
- [ ] PRISMA flow data documented
- [ ] Coding scheme and inter-rater reliability data available

## Results
- [ ] `results/reproduce.sh` exists and regenerates all figures/tables
- [ ] Script exits with code 0 on success
- [ ] Generated outputs match paper's figures and tables

## Process Log
- [ ] `process-log/README.md` describes research workflow
- [ ] AI session logs included in `process-log/ai-sessions/`
- [ ] Human decisions documented in `process-log/human-decisions/`
- [ ] All AI tools and versions disclosed

## Licensing
- [ ] Paper: CC-BY 4.0
- [ ] Code: MIT License
- [ ] Data: CC-BY 4.0
