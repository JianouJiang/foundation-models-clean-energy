#!/usr/bin/env python3
"""Fig: Reproducibility audit dashboard."""
import os, sys, json
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "utils"))
import plotting_utils as pu

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "codes", "results")
FIG_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "manuscript", "figures")
os.makedirs(FIG_DIR, exist_ok=True)


def main():
    with open(os.path.join(RESULTS_DIR, "reproducibility_audit.json")) as f:
        data = json.load(f)

    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    colors = pu.COLORS

    # (a) Open access by year
    ax = axes[0]
    oa = data["open_access"]["by_year"]
    years = sorted(oa["pct"].keys())
    pcts = [oa["pct"][y] for y in years]
    counts = [oa["count"][y] for y in years]

    ax.bar(years, pcts, color=colors[0], alpha=0.8, edgecolor="white")
    ax.set_xlabel("Year")
    ax.set_ylabel("Open Access (%)")
    ax.set_title("(a) Open Access Rate by Year")
    ax.set_ylim(0, 100)
    ax.axhline(y=data["open_access"]["open_access_pct"], color="red",
               linestyle="--", alpha=0.7, label=f"Overall: {data['open_access']['open_access_pct']}%")
    ax.legend(fontsize=8)
    ax.tick_params(axis='x', rotation=45)

    # (b) Open access by FM type
    ax = axes[1]
    fm_oa = data["open_access"]["by_fm_type"]
    fm_types = sorted(fm_oa["pct"].keys())
    fm_pcts = [fm_oa["pct"][ft] for ft in fm_types]
    fm_counts = [fm_oa["count"][ft] for ft in fm_types]

    bar_colors = [colors[i % len(colors)] for i in range(len(fm_types))]
    bars = ax.barh(fm_types, fm_pcts, color=bar_colors, alpha=0.8, edgecolor="white")

    for bar, pct, count in zip(bars, fm_pcts, fm_counts):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
               f"{pct:.0f}% (n={count})", va="center", fontsize=8)

    ax.set_xlabel("Open Access (%)")
    ax.set_title("(b) Open Access by FM Type")
    ax.set_xlim(0, 110)

    # (c) Reproducibility scorecard
    ax = axes[2]
    metrics = {
        "Open Access": data["open_access"]["open_access_pct"],
        "Has DOI": data["doi"]["doi_pct"],
        "ML Venue": data["code_estimate"]["ml_venue_pct"],
        "Code in Abstract": data["code_estimate"]["code_mention_pct"],
        "On Papers w/ Code": data["pwc_check"]["found_pct"],
    }

    labels = list(metrics.keys())
    values = list(metrics.values())
    bar_colors = [colors[2] if v > 50 else colors[3] if v > 10 else colors[4]
                  for v in values]

    bars = ax.barh(labels, values, color=bar_colors, alpha=0.8, edgecolor="white")
    for bar, val in zip(bars, values):
        ax.text(bar.get_width() + 1.5, bar.get_y() + bar.get_height() / 2,
               f"{val:.1f}%", va="center", fontsize=9, fontweight="bold")

    ax.set_xlabel("Percentage (%)")
    ax.set_title(f"(c) Reproducibility Scorecard\n(Index: {data['reproducibility_index']:.3f})")
    ax.set_xlim(0, 110)
    ax.invert_yaxis()

    fig.suptitle(f"Reproducibility Audit of FM+Energy Literature (n={data['open_access']['total_papers']:,})",
                fontsize=12, y=1.02)
    fig.tight_layout()
    pu.save_figure(fig, "fig_reproducibility")
    print("Done: fig_reproducibility")


if __name__ == "__main__":
    main()
