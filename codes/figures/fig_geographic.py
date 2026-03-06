#!/usr/bin/env python3
"""Fig: Geographic distribution of FM+energy research.
(a) Cleveland dot plot of top-15 countries
(b) 100% stacked horizontal bars for FM-type composition of top-5 countries
"""
import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "utils"))
import plotting_utils as pu

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
FIG_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "manuscript", "figures")
os.makedirs(FIG_DIR, exist_ok=True)

COUNTRY_NAMES = {
    "CN": "China", "US": "USA", "GB": "UK", "DE": "Germany",
    "IN": "India", "CA": "Canada", "KR": "South Korea", "AU": "Australia",
    "IT": "Italy", "SG": "Singapore", "HK": "Hong Kong", "JP": "Japan",
    "ES": "Spain", "FR": "France", "CH": "Switzerland", "NL": "Netherlands",
    "SE": "Sweden", "SA": "Saudi Arabia", "BR": "Brazil", "TR": "Turkey",
}

def main():
    df = pd.read_csv(os.path.join(DATA_DIR, "classified_papers.csv"))

    # Count countries
    country_counts = Counter()
    for countries in df["countries"]:
        for c in str(countries).split("; "):
            c = c.strip()
            if c and c != "nan":
                country_counts[c] += 1

    top15 = country_counts.most_common(15)
    names = [COUNTRY_NAMES.get(c, c) for c, _ in top15]
    vals = [v for _, v in top15]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5),
                                    gridspec_kw={"width_ratios": [1.2, 1.0]})

    # (a) Cleveland dot plot (Tufte: less ink than bars)
    y = np.arange(len(names))
    ax1.hlines(y, 0, vals, color="0.80", lw=1)
    ax1.plot(vals, y, "o", color=pu.COLORS["primary"], markersize=7, zorder=5)
    for yy, val in zip(y, vals):
        ax1.text(val + max(vals) * 0.02, yy, str(val), va="center", fontsize=8)
    ax1.set_yticks(y)
    ax1.set_yticklabels(names)
    ax1.invert_yaxis()
    ax1.set_xlabel("Papers (author affiliations)")
    ax1.set_title("(a) Geographic distribution")
    ax1.grid(axis="y", visible=False)

    # (b) 100% stacked horizontal bars for FM composition (top-5)
    top5_codes = [c for c, _ in country_counts.most_common(5)]
    top5_names = [COUNTRY_NAMES.get(c, c) for c in top5_codes]
    fm_types = ["LLM", "TSFM", "VLM", "diffusion", "multimodal"]
    fm_colors = [pu.COLORS["primary"], pu.COLORS["secondary"],
                 pu.COLORS["tertiary"], pu.COLORS["quaternary"],
                 pu.COLORS["quinary"]]

    # Build composition matrix
    comp = np.zeros((len(top5_codes), len(fm_types)))
    for j, fm in enumerate(fm_types):
        for i, cc in enumerate(top5_codes):
            mask_cc = df["countries"].str.contains(cc, na=False)
            mask_fm = df["fm_types"].str.contains(fm, na=False)
            comp[i, j] = (mask_cc & mask_fm).sum()
    row_totals = comp.sum(axis=1, keepdims=True)
    row_totals[row_totals == 0] = 1
    pct = comp / row_totals

    y2 = np.arange(len(top5_codes))
    left = np.zeros(len(top5_codes))
    for j, (fm, color) in enumerate(zip(fm_types, fm_colors)):
        ax2.barh(y2, pct[:, j], left=left, color=color, height=0.6,
                 edgecolor="white", linewidth=0.3, label=fm)
        left += pct[:, j]

    ax2.set_yticks(y2)
    ax2.set_yticklabels(top5_names)
    ax2.invert_yaxis()
    ax2.set_xlim(0, 1)
    ax2.set_xlabel("Share of publications")
    ax2.set_title("(b) FM-type portfolio (top-5)")
    ax2.legend(fontsize=8, frameon=False, loc="lower right")
    ax2.grid(visible=False)

    fig.tight_layout()
    pu.save_figure(fig, "fig_geographic")
    print("Done: fig_geographic")

if __name__ == "__main__":
    main()
