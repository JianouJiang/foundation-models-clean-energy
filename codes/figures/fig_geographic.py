#!/usr/bin/env python3
"""Fig: Geographic distribution of FM+energy research."""
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

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Panel A: Bar chart by country
    colors = [pu.COLORS["quaternary"] if n == "China" else
              pu.COLORS["primary"] if n == "USA" else
              pu.COLORS["tertiary"] if n == "UK" else
              pu.COLORS["octonary"]
              for n in names]
    bars = ax1.barh(range(len(names)), vals, color=colors, alpha=0.8)
    ax1.set_yticks(range(len(names)))
    ax1.set_yticklabels(names)
    ax1.invert_yaxis()
    ax1.set_xlabel("Number of papers (author affiliations)")
    ax1.set_title("(a) Geographic distribution")
    for bar, val in zip(bars, vals):
        ax1.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
                 str(val), va="center", fontsize=8)

    # Panel B: Country × FM type breakdown for top 5 countries
    top5_codes = [c for c, _ in country_counts.most_common(5)]
    fm_types = ["LLM", "TSFM", "VLM", "diffusion", "multimodal"]
    fm_colors = [pu.COLORS["primary"], pu.COLORS["secondary"],
                 pu.COLORS["tertiary"], pu.COLORS["quaternary"],
                 pu.COLORS["quinary"]]

    x = np.arange(len(top5_codes))
    width = 0.15
    for i, (fm, color) in enumerate(zip(fm_types, fm_colors)):
        counts = []
        for cc in top5_codes:
            mask_cc = df["countries"].str.contains(cc, na=False)
            mask_fm = df["fm_types"].str.contains(fm, na=False)
            counts.append((mask_cc & mask_fm).sum())
        ax2.bar(x + i*width - 2*width, counts, width, label=fm,
                color=color, alpha=0.8)

    ax2.set_xticks(x)
    ax2.set_xticklabels([COUNTRY_NAMES.get(c, c) for c in top5_codes])
    ax2.set_ylabel("Number of papers")
    ax2.set_title("(b) FM type by top-5 countries")
    ax2.legend(fontsize=8)

    fig.tight_layout()
    pu.save_figure(fig, "fig_geographic")
    print("Done: fig_geographic")

if __name__ == "__main__":
    main()
