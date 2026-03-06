#!/usr/bin/env python3
"""Fig: Domain × FM type heatmap with paper counts."""
import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "utils"))
import plotting_utils as pu

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
FIG_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "manuscript", "figures")
os.makedirs(FIG_DIR, exist_ok=True)

def main():
    df = pd.read_csv(os.path.join(DATA_DIR, "classified_papers.csv"))

    domains = ["wind", "solar", "hydropower", "grid", "ecological"]
    domain_labels = ["Wind", "Solar", "Hydropower", "Grid/Storage", "Ecological"]
    fm_types = ["LLM", "TSFM", "VLM", "diffusion", "multimodal"]

    # Build count matrix using multi-label fields
    matrix = np.zeros((len(domains), len(fm_types)), dtype=int)
    for i, domain in enumerate(domains):
        for j, fm in enumerate(fm_types):
            mask_d = df["energy_domains"].str.contains(domain, na=False)
            mask_f = df["fm_types"].str.contains(fm, na=False)
            matrix[i, j] = (mask_d & mask_f).sum()

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(matrix, annot=True, fmt="d", cmap="Blues",
                xticklabels=fm_types, yticklabels=domain_labels,
                ax=ax, linewidths=0.5, linecolor="white",
                cbar_kws={"label": "Number of papers"})
    ax.set_xlabel("Foundation Model Type")
    ax.set_ylabel("Energy Domain")
    ax.set_title("Energy Domain × FM Type (paper counts from OpenAlex, n=3,645)")

    # Highlight gaps
    for i in range(len(domains)):
        for j in range(len(fm_types)):
            if matrix[i, j] <= 3:
                ax.add_patch(plt.Rectangle((j, i), 1, 1,
                             fill=False, edgecolor="red",
                             linewidth=1.5, linestyle="--"))

    fig.tight_layout()
    pu.save_figure(fig, "fig_domain_heatmap")
    print("Done: fig_domain_heatmap")

if __name__ == "__main__":
    main()
