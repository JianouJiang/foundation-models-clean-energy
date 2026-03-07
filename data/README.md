# Data — Foundation Models for Clean Energy Systems

This directory contains the datasets required to reproduce the figures and analyses in the paper.

## Contents

- `openalex_papers.json`
  - Raw literature search results from OpenAlex used for the PRISMA-based screening pipeline.
  - Source script: `code/data_processing/collect_papers.py`
  - **Query**: Foundation model + clean energy keyword combinations (see Section 2 of the paper for the full search string)
  - **Collection date**: December 2025 — February 2026
  - **License**: OpenAlex data is available under CC0 (public domain). See [OpenAlex documentation](https://docs.openalex.org/).

- `classified_papers.csv`
  - Classified subset of OpenAlex papers produced by `code/data_processing/classify_papers.py`.
  - Contains 3,645 papers classified by FM type and energy domain using regex keyword matching (12% estimated misclassification rate; see paper Section 3).

- `household_power.csv`
  - Time-series dataset used for baseline forecasting experiments (Experiment 1).
  - **Source**: UCI Machine Learning Repository — [Individual Household Electric Power Consumption](https://archive.ics.uci.edu/dataset/235/individual+household+electric+power+consumption)
  - **Original authors**: Hebrail, G. and Berard, A. (2012)
  - **License**: CC BY 4.0
  - **Processing**: Resampled to hourly frequency, missing values forward-filled.

- `elpv_repo/`
  - Snapshot of the ELPV dataset repository used for PV defect inspection experiments (Experiment 3).
  - **Source**: [https://github.com/zae-bayern/elpv-dataset](https://github.com/zae-bayern/elpv-dataset)
  - **Reference**: Deitsch, S. et al. (2019). "Automatic classification of defective photovoltaic module cells in electroluminescence images." Solar Energy, 185, 455–468.
  - **License**: CC BY-NC-SA 4.0
  - **Snapshot date**: January 2026

## Size / Hosting

All datasets are small enough to be hosted directly on GitHub. If future versions exceed GitHub file size limits, they will be hosted on Zenodo with a DOI linked here.
