#!/usr/bin/env python3
"""Fig: Taxonomy heatmap — FM type × energy task, cell intensity = paper count."""
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

    fm_types = ["LLM", "TSFM", "VLM", "diffusion", "multimodal"]
    tasks = ["forecasting", "fault_detection", "nlp_qa", "image_inspection",
             "data_augmentation", "optimization", "anomaly_narration"]
    task_labels = ["Forecasting", "Fault detection", "NLP / Q&A",
                   "Image inspection", "Data augmentation",
                   "Optimization", "Anomaly narration"]

    # Build count matrix using multi-label fields
    matrix = np.zeros((len(tasks), len(fm_types)), dtype=int)
    for i, task in enumerate(tasks):
        for j, fm in enumerate(fm_types):
            mask_task = df["tasks"].str.contains(task, na=False)
            mask_fm = df["fm_types"].str.contains(fm, na=False)
            matrix[i, j] = (mask_task & mask_fm).sum()

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(matrix, annot=True, fmt="d", cmap="YlOrRd",
                xticklabels=fm_types, yticklabels=task_labels,
                ax=ax, linewidths=0.5, linecolor="white",
                cbar_kws={"label": "Number of papers"})
    ax.set_xlabel("Foundation Model Type")
    ax.set_ylabel("Energy Task Category")
    ax.set_title("FM Type × Task Taxonomy Heatmap (paper counts)")

    # Highlight gaps (cells with 0 papers)
    for i in range(len(tasks)):
        for j in range(len(fm_types)):
            if matrix[i, j] == 0:
                ax.add_patch(plt.Rectangle((j, i), 1, 1,
                             fill=False, edgecolor="red",
                             linewidth=2, linestyle="--"))

    fig.tight_layout()
    pu.save_figure(fig, "fig_taxonomy_heatmap")
    print("Done: fig_taxonomy_heatmap")

if __name__ == "__main__":
    main()
