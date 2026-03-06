#!/usr/bin/env python3
"""Fig: Publication trend with exponential fit, split by FM type."""
import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "utils"))
import plotting_utils as pu

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
FIG_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "manuscript", "figures")
os.makedirs(FIG_DIR, exist_ok=True)

def exponential_model(x, a, b):
    return a * np.exp(b * x)

def main():
    df = pd.read_csv(os.path.join(DATA_DIR, "classified_papers.csv"))
    df = df[df["year"] <= 2025]

    # Overall trend
    yearly = df.groupby("year").size()
    years = yearly.index.values
    counts = yearly.values

    # Exponential fit (2019-2025)
    mask = years >= 2019
    x_fit = years[mask] - 2019
    y_fit = counts[mask]
    popt, _ = curve_fit(exponential_model, x_fit, y_fit, p0=[50, 0.5], maxfev=5000)
    x_smooth = np.linspace(0, 7, 100)
    y_smooth = exponential_model(x_smooth, *popt)

    # R² calculation
    y_pred = exponential_model(x_fit, *popt)
    r2 = 1 - np.sum((y_fit - y_pred)**2) / np.sum((y_fit - np.mean(y_fit))**2)

    # By FM type (stacked area)
    fm_types = ["LLM", "TSFM", "VLM", "diffusion", "multimodal"]
    fm_colors = [pu.COLORS["primary"], pu.COLORS["secondary"],
                 pu.COLORS["tertiary"], pu.COLORS["quaternary"],
                 pu.COLORS["quinary"]]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Panel A: Line+markers with exponential fit (Tufte: less ink than bars)
    doubling = np.log(2) / popt[1]
    ax1.plot(years, counts, 'o-', color=pu.COLORS["primary"],
             markersize=6, linewidth=1.5, zorder=4, label="Observed")
    ax1.plot(x_smooth + 2019, y_smooth, '--', color=pu.COLORS["secondary"],
             linewidth=1.5, zorder=3, label=f"Exp. fit ($R^2$={r2:.3f})")
    # Annotate doubling time directly on curve
    mid_idx = len(x_smooth) // 2
    ax1.annotate(f"Doubling time: {doubling:.1f} yr",
                 xy=(x_smooth[mid_idx] + 2019, y_smooth[mid_idx]),
                 xytext=(15, 15), textcoords="offset points",
                 fontsize=9, ha="left",
                 arrowprops=dict(arrowstyle="->", color="0.4", lw=0.8))
    ax1.set_xlabel("Year")
    ax1.set_ylabel("Number of publications")
    ax1.set_title("(a) FM+Energy publication growth")
    ax1.legend(fontsize=8, frameon=False)
    ax1.set_xlim(2016.5, 2025.5)

    # Panel B: Stacked area by FM type
    fm_yearly = df.groupby(["year", "primary_fm_type"]).size().unstack(fill_value=0)
    y_data = []
    labels = []
    colors = []
    for fm, color in zip(fm_types, fm_colors):
        if fm in fm_yearly.columns:
            y_data.append(fm_yearly[fm].values)
            labels.append(fm)
            colors.append(color)
    # Add "other"
    other = counts.copy()
    for yd in y_data:
        # Align lengths
        min_len = min(len(other), len(yd))
        other[:min_len] -= yd[:min_len]
    y_data.append(np.maximum(other, 0))
    labels.append("Other")
    colors.append(pu.COLORS["octonary"])

    ax2.stackplot(years, *y_data, labels=labels, colors=colors, alpha=0.8)
    ax2.set_xlabel("Year")
    ax2.set_ylabel("Number of publications")
    ax2.set_title("(b) By foundation model type")
    ax2.legend(loc="upper left", fontsize=8)
    ax2.set_xlim(2017, 2025)

    fig.tight_layout()
    pu.save_figure(fig, "fig_publication_trend")
    print("Done: fig_publication_trend")

if __name__ == "__main__":
    main()
