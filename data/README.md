# Data — Foundation Models for Clean Energy Systems

This directory contains the datasets required to reproduce the figures and analyses in the paper.

## Contents

- `openalex_papers.json`
  - Raw literature search results from OpenAlex used for the PRISMA-based screening pipeline.
  - Source script: `code/data_processing/collect_papers.py`
  - TODO: document query parameters, collection date, and OpenAlex license/terms.

- `classified_papers.csv`
  - Classified subset of OpenAlex papers produced by `code/data_processing/classify_papers.py`.

- `household_power.csv`
  - Time-series dataset used for baseline forecasting experiments.
  - TODO: document original source and license.

- `elpv_repo/`
  - Snapshot of the ELPV dataset repository used for PV defect inspection experiments.
  - TODO: document upstream source URL, commit/hash, and license.

## Size / Hosting

If this dataset exceeds GitHub file size limits for submission, host it on Zenodo or HuggingFace Datasets and include the DOI here.
