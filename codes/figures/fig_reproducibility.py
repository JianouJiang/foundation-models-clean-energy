#!/usr/bin/env python3
"""Fig: Reproducibility audit dashboard (Tufte-style redesign).
(a) OA rate over time as line + Wilson CI band
(b) OA by FM type as Cleveland dot plot
(c) Reproducibility scorecard as bullet charts with benchmark targets
"""
import os, sys, json
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "utils"))
import plotting_utils as pu

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "codes", "results")
FIG_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "manuscript", "figures")
os.makedirs(FIG_DIR, exist_ok=True)


def wilson_ci(p, n, z=1.96):
    """Wilson score confidence interval for a proportion."""
    n = np.maximum(n, 1)
    den = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / den
    half = (z * np.sqrt((p * (1 - p) + z**2 / (4 * n)) / n)) / den
    return np.clip(center - half, 0, 1), np.clip(center + half, 0, 1)


def main():
    with open(os.path.join(RESULTS_DIR, "reproducibility_audit.json")) as f:
        data = json.load(f)

    fig, axes = plt.subplots(1, 3, figsize=(14, 5),
                             gridspec_kw={"width_ratios": [1.2, 1.0, 1.4]})
    colors = pu.COLORS

    # --- (a) OA by year: line + Wilson CI band ---
    ax = axes[0]
    oa = data["open_access"]["by_year"]
    years = sorted(oa["pct"].keys())
    pcts = np.array([oa["pct"][y] for y in years]) / 100.0
    counts = np.array([oa["count"][y] for y in years])

    lo, hi = wilson_ci(pcts, counts)
    ax.fill_between(years, 100 * lo, 100 * hi, color=colors["primary"],
                    alpha=0.15, linewidth=0)
    ax.plot(years, 100 * pcts, 'o-', color=colors["primary"],
            markersize=5, linewidth=1.5)
    overall = data["open_access"]["open_access_pct"]
    ax.axhline(overall, color=colors["secondary"], ls="--", lw=1, alpha=0.7)
    ax.text(years[-1], overall + 2, f"Overall: {overall:.0f}%",
            color=colors["secondary"], fontsize=8, ha="right")
    ax.set_xlabel("Year")
    ax.set_ylabel("Open access (%)")
    ax.set_title("(a) Open-access rate over time")
    ax.set_ylim(0, 100)
    ax.grid(axis="x", visible=False)
    ax.tick_params(axis="x", rotation=45)

    # --- (b) OA by FM type: Cleveland dot plot ---
    ax = axes[1]
    fm_oa = data["open_access"]["by_fm_type"]
    fm_types = sorted(fm_oa["pct"].keys())
    fm_pcts = np.array([fm_oa["pct"][ft] for ft in fm_types])
    y = np.arange(len(fm_types))

    ax.hlines(y, 0, fm_pcts, color="0.80", lw=1)
    ax.plot(fm_pcts, y, "o", color=colors["tertiary"], markersize=7, zorder=5)
    for yy, vv, ft in zip(y, fm_pcts, fm_types):
        n = fm_oa["count"][ft]
        ax.text(vv + 2, yy, f"{vv:.0f}% (n={n})", va="center", fontsize=8)
    ax.set_yticks(y)
    ax.set_yticklabels(fm_types)
    ax.set_xlim(0, 100)
    ax.set_xlabel("Open access (%)")
    ax.set_title("(b) Open access by FM type")
    ax.grid(axis="y", visible=False)

    # --- (c) Bullet charts for reproducibility components ---
    ax = axes[2]
    metrics = [
        ("Has DOI", data["doi"]["doi_pct"], 95),
        ("Open Access", data["open_access"]["open_access_pct"], 80),
        ("ML Venue", data["code_estimate"]["ml_venue_pct"], 40),
        ("Code Mentioned", data["code_estimate"]["code_mention_pct"], 50),
        ("Papers w/ Code", data["pwc_check"]["found_pct"], 50),
    ]

    y2 = np.arange(len(metrics))[::-1]
    bar_h = 0.5
    for (label, val, target), yy in zip(metrics, y2):
        # Background bar (100% reference)
        ax.barh(yy, 100, height=bar_h, color="0.92", edgecolor="none")
        # Actual value bar
        color = colors["primary"] if val >= target else colors["quaternary"]
        ax.barh(yy, val, height=bar_h, color=color, alpha=0.85, edgecolor="none")
        # Target marker
        ax.plot([target, target], [yy - bar_h / 2 + 0.05, yy + bar_h / 2 - 0.05],
                color="0.2", lw=2)
        # Value label
        ax.text(max(val, 3) + 1.5, yy, f"{val:.1f}%", va="center", fontsize=8)

    ax.set_yticks(y2)
    ax.set_yticklabels([m[0] for m in metrics])
    ax.set_xlim(0, 110)
    ax.set_xlabel("Percentage (%)")
    ax.set_title(f"(c) Reproducibility scorecard (index: {data['reproducibility_index']:.2f})")
    ax.grid(visible=False)

    fig.suptitle(f"Reproducibility audit (n = {data['open_access']['total_papers']:,})",
                 fontsize=12, y=1.02)
    fig.tight_layout()
    pu.save_figure(fig, "fig_reproducibility")
    print("Done: fig_reproducibility")


if __name__ == "__main__":
    main()
