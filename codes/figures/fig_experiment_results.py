#!/usr/bin/env python3
"""Fig: Combined experiment results figures.

Generates figures from benchmark experiment results:
- Time-series forecasting comparison
- VLM inspection confusion matrix and comparison
- LLM Q&A domain breakdown
- RAG pipeline comparison
"""
import os, sys, json
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "utils"))
import plotting_utils as pu

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "codes", "results")
FIG_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "manuscript", "figures")
os.makedirs(FIG_DIR, exist_ok=True)


def plot_timeseries_benchmark():
    """Plot time-series benchmark results."""
    fpath = os.path.join(RESULTS_DIR, "timeseries_benchmark.json")
    if not os.path.exists(fpath):
        print("Skipping timeseries benchmark (no results)")
        return

    with open(fpath) as f:
        data = json.load(f)

    colors = pu.COLORS
    models = list(data.keys())
    metrics_names = ["MAE", "RMSE", "MAPE"]

    fig, axes = plt.subplots(1, 3, figsize=(14, 5))

    for ax, metric in zip(axes, metrics_names):
        values = [data[m][metric] for m in models]
        bar_colors = [colors[i % len(colors)] for i in range(len(models))]

        bars = ax.bar(range(len(models)), values, color=bar_colors,
                     edgecolor="white", alpha=0.85)

        for bar, val in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01 * max(values),
                   f"{val:.3f}", ha="center", fontsize=8, fontweight="bold")

        ax.set_xticks(range(len(models)))
        ax.set_xticklabels(models, rotation=30, ha="right", fontsize=8)
        ax.set_ylabel(metric)
        ax.set_title(f"({chr(97 + metrics_names.index(metric))}) {metric}")

    fig.suptitle("Time-Series Foundation Model Benchmark: 24h Ahead Load Forecasting",
                fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    pu.save_figure(fig, "fig_timeseries_benchmark")
    print("Done: fig_timeseries_benchmark")

    # Also plot predictions if available
    pred_path = os.path.join(RESULTS_DIR, "timeseries_predictions.json")
    if os.path.exists(pred_path):
        with open(pred_path) as f:
            preds = json.load(f)

        fig2, ax2 = plt.subplots(figsize=(12, 5))
        test = np.array(preds["test"])
        hours = range(min(168, len(test)))  # First 7 days

        ax2.plot(hours, test[:len(hours)], "k-", linewidth=1.5, label="Actual", alpha=0.9)

        for i, (name, key) in enumerate([("ARIMA", "ARIMA"), ("XGBoost", "XGBoost"),
                                          ("LSTM", "LSTM"), ("Chronos", "Chronos")]):
            if key in preds:
                pred = np.array(preds[key])
                ax2.plot(hours, pred[:len(hours)], color=colors[i],
                        linewidth=1, alpha=0.7, label=name)

        ax2.set_xlabel("Hour")
        ax2.set_ylabel("Power (kW)")
        ax2.set_title("First 7 Days: Actual vs Predicted Load")
        ax2.legend(fontsize=9)
        ax2.grid(True, alpha=0.3)

        fig2.tight_layout()
        pu.save_figure(fig2, "fig_timeseries_predictions")
        print("Done: fig_timeseries_predictions")


def plot_vlm_results():
    """Plot VLM inspection results."""
    fpath = os.path.join(RESULTS_DIR, "vlm_inspection.json")
    if not os.path.exists(fpath):
        print("Skipping VLM inspection (no results)")
        return

    with open(fpath) as f:
        data = json.load(f)

    colors = pu.COLORS
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # (a) Precision–Recall scatter (Tufte: higher density than bars)
    ax = axes[0]
    models = []
    precs = []
    recs = []
    f1s = []
    for name, metrics in data.items():
        if isinstance(metrics, dict) and "precision" in metrics:
            models.append(name)
            precs.append(metrics["precision"])
            recs.append(metrics["recall"])
            f1s.append(metrics["f1"])

    # F1 iso-curves (background reference)
    for f1_val in [0.4, 0.6, 0.8]:
        r_range = np.linspace(0.01, 1.0, 200)
        p_iso = f1_val * r_range / (2 * r_range - f1_val)
        mask = (p_iso > 0) & (p_iso <= 1)
        ax.plot(r_range[mask], p_iso[mask], color="0.85", lw=0.8, zorder=1)
        # Label the iso-curve
        idx = np.argmin(np.abs(r_range[mask] - 0.95))
        ax.text(r_range[mask][idx], p_iso[mask][idx] + 0.02,
                f"F1={f1_val}", fontsize=6, color="0.6", ha="right")

    model_colors = [colors[i % len(colors)] for i in range(len(models))]
    for i, (m, p, r, f) in enumerate(zip(models, precs, recs, f1s)):
        ax.scatter(r, p, s=80, color=model_colors[i], edgecolors="white",
                   linewidths=0.5, zorder=5)
        # Direct label (Tufte: avoid legend when possible)
        short = m.replace("CLIP zero-shot ", "").replace("Supervised ", "Sup. ")
        # Custom offsets to avoid overlap between nearby points
        offsets = [(-60, -20), (12, 10), (12, 14), (-70, 10), (12, -14)]
        idx = i % len(offsets)
        offset = offsets[idx]
        ha_ann = "left" if offset[0] > 0 else "right"
        va_ann = "bottom" if offset[1] > 0 else "top"
        ax.annotate(f"{short}\nF1={f:.2f}", (r, p),
                    fontsize=7, xytext=offset, textcoords="offset points",
                    ha=ha_ann, va=va_ann,
                    arrowprops=dict(arrowstyle="-", color="0.5", lw=0.4))

    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_xlim(0, 1.08)
    ax.set_ylim(0.3, 1.0)
    ax.set_title("(a) Precision–Recall space")
    ax.grid(visible=False)

    # (b) Confusion matrix
    ax = axes[1]
    cm = data.get("confusion_matrix_ensemble")
    if cm:
        cm = np.array(cm)
        im = ax.imshow(cm, cmap="Blues")
        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        ax.set_xticklabels(["Functional", "Defective"])
        ax.set_yticklabels(["Functional", "Defective"])
        ax.set_xlabel("Predicted")
        ax.set_ylabel("Actual")
        ax.set_title("(b) Confusion Matrix (CLIP Ensemble)")

        for i in range(2):
            for j in range(2):
                ax.text(j, i, f"{cm[i, j]}", ha="center", va="center",
                       fontsize=14, fontweight="bold",
                       color="white" if cm[i, j] > cm.max() / 2 else "black")
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    else:
        ax.text(0.5, 0.5, "No confusion matrix data", transform=ax.transAxes,
               ha="center")
        ax.set_title("(b) Confusion Matrix")

    fig.suptitle("VLM Zero-Shot Solar Panel Defect Detection (ELPV Dataset)",
                fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    pu.save_figure(fig, "fig_vlm_inspection")
    print("Done: fig_vlm_inspection")


def plot_llm_qa():
    """Plot LLM Q&A results: (a) Cleveland dot plot with 7B+3B, (b) slopegraph Direct vs RAG."""
    fpath = os.path.join(RESULTS_DIR, "llm_energy_qa.json")
    fpath_3b = os.path.join(RESULTS_DIR, "llm_energy_qa_3b.json")
    rag_path = os.path.join(RESULTS_DIR, "rag_pipeline.json")

    domain_scores_7b = {}
    domain_scores_3b = {}
    n_q = 0

    if os.path.exists(fpath):
        with open(fpath) as f:
            data = json.load(f)
        domain_scores_7b = data.get("domain_scores", {})
        n_q = data.get("n_questions", 0)
        source = "dedicated"
    elif os.path.exists(rag_path):
        with open(rag_path) as f:
            data = json.load(f)
        by_domain = data.get("summary", {}).get("by_domain", {})
        domain_scores_7b = {d: v["direct_mean"] for d, v in by_domain.items()}
        n_q = data.get("summary", {}).get("n_questions", 15)
        source = "RAG baseline"
    else:
        print("Skipping LLM Q&A (no results)")
        return

    if os.path.exists(fpath_3b):
        with open(fpath_3b) as f:
            data_3b = json.load(f)
        domain_scores_3b = data_3b.get("domain_scores", {})

    colors = pu.COLORS
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # (a) Direct LLM score by domain: Cleveland dot plot (7B + 3B)
    ax = axes[0]
    if domain_scores_7b:
        domains = sorted(domain_scores_7b.keys(), key=lambda d: domain_scores_7b[d])
        scores_7b = [domain_scores_7b[d] for d in domains]
        y = np.arange(len(domains))

        ax.hlines(y, 0, [max(s7, domain_scores_3b.get(d, 0))
                         for s7, d in zip(scores_7b, domains)],
                  color="0.85", lw=1)
        ax.plot(scores_7b, y, "o", color=colors["primary"], markersize=8,
                zorder=5, label="Qwen2.5-7B")

        if domain_scores_3b:
            scores_3b = [domain_scores_3b.get(d, 0) for d in domains]
            ax.plot(scores_3b, y, "s", color=colors["secondary"], markersize=7,
                    zorder=5, label="Qwen2.5-3B")
            for yy, s7, s3 in zip(y, scores_7b, scores_3b):
                ax.text(max(s7, s3) + 0.03, yy,
                        f"{s7:.3f} / {s3:.3f}", va="center", fontsize=8)
        else:
            for yy, sc in zip(y, scores_7b):
                ax.text(sc + 0.03, yy, f"{sc:.3f}", va="center", fontsize=9)

        ax.set_yticks(y)
        ax.set_yticklabels(domains)
        ax.set_xlabel("Mean keyword match score")
        ax.set_xlim(0, 1.0)
        ax.set_title("(a) Direct LLM score by domain")
        ax.legend(fontsize=8, frameon=False, loc="lower right")
        ax.grid(axis="y", visible=False)

    # (b) Direct vs RAG: slopegraph (paired comparison)
    ax = axes[1]
    if os.path.exists(rag_path):
        with open(rag_path) as f:
            rag_data = json.load(f)
        by_domain = rag_data.get("summary", {}).get("by_domain", {})
        if by_domain:
            domains = sorted(by_domain.keys())
            direct = [by_domain[d]["direct_mean"] for d in domains]
            rag = [by_domain[d]["rag_mean"] for d in domains]
            domain_colors = [colors[i % len(colors)] for i in range(len(domains))]

            # Sort right-side labels and add offsets to prevent overlap
            right_labels = sorted(enumerate(zip(domains, rag)), key=lambda x: x[1][1])
            right_offsets = {}
            min_gap = 0.06
            prev_y = -999
            for idx, (d, rs) in right_labels:
                y_pos = rs
                if y_pos - prev_y < min_gap:
                    y_pos = prev_y + min_gap
                right_offsets[idx] = y_pos
                prev_y = y_pos

            for i, (d, ds, rs, c) in enumerate(zip(domains, direct, rag, domain_colors)):
                ax.plot([0, 1], [ds, rs], 'o-', color=c, linewidth=1.5,
                        markersize=7, zorder=3)
                ax.text(-0.08, ds, f"{ds:.2f}", ha="right", va="center",
                        fontsize=8, color=c)
                ax.text(1.08, right_offsets[i], f"{rs:.2f} {d}", ha="left", va="center",
                        fontsize=8, color=c)

            ax.set_xticks([0, 1])
            ax.set_xticklabels(["Direct LLM", "RAG-augmented"], fontsize=10)
            ax.set_ylabel("Mean score")
            ax.set_ylim(-0.05, 1.15)
            ax.set_xlim(-0.3, 1.4)
            ax.set_title("(b) Direct LLM vs RAG by domain")
            ax.grid(axis="x", visible=False)

    fig.suptitle(f"LLM energy domain Q&A (n = {n_q})",
                fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    pu.save_figure(fig, "fig_llm_qa")
    print(f"Done: fig_llm_qa (source: {source})")


def plot_rag_comparison():
    """Plot RAG vs direct LLM: (a) domain slopegraph, (b) improvement waterfall."""
    fpath = os.path.join(RESULTS_DIR, "rag_pipeline.json")
    if not os.path.exists(fpath):
        print("Skipping RAG pipeline (no results)")
        return

    with open(fpath) as f:
        data = json.load(f)

    colors = pu.COLORS
    summary = data.get("summary", {})

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # (a) Domain improvement: horizontal dumbbell chart
    ax = axes[0]
    by_domain = summary.get("by_domain", {})
    if by_domain:
        domains = sorted(by_domain.keys(), key=lambda d: by_domain[d].get("improvement", 0))
        direct = [by_domain[d]["direct_mean"] for d in domains]
        rag = [by_domain[d]["rag_mean"] for d in domains]
        y = np.arange(len(domains))

        # Connecting lines
        for yy, ds, rs in zip(y, direct, rag):
            c = colors["primary"] if rs > ds else colors["secondary"]
            ax.plot([ds, rs], [yy, yy], '-', color=c, lw=2, alpha=0.6)
        # Direct dots
        ax.scatter(direct, y, s=50, color=colors["octonary"], zorder=5,
                   label="Direct LLM", edgecolors="white", linewidths=0.5)
        # RAG dots
        ax.scatter(rag, y, s=50, color=colors["primary"], zorder=5,
                   label="RAG-augmented", edgecolors="white", linewidths=0.5)

        ax.set_yticks(y)
        ax.set_yticklabels(domains)
        ax.set_xlabel("Mean score")
        ax.set_xlim(-0.05, 1.15)
        ax.set_title("(a) Direct vs RAG by domain")
        ax.legend(fontsize=8, frameon=False, loc="lower right")
        ax.grid(axis="y", visible=False)

    # (b) Improvement waterfall
    ax = axes[1]
    if by_domain:
        domains_sorted = sorted(by_domain.keys(),
                                key=lambda d: by_domain[d].get("improvement", 0),
                                reverse=True)
        improvements = [by_domain[d].get("improvement", 0) for d in domains_sorted]
        y2 = np.arange(len(domains_sorted))
        bar_colors = [colors["primary"] if imp > 0 else colors["secondary"]
                      for imp in improvements]

        ax.barh(y2, improvements, color=bar_colors, alpha=0.85, edgecolor="white",
                height=0.6)
        ax.axvline(0, color="0.3", lw=0.8)
        for yy, imp in zip(y2, improvements):
            ax.text(imp + 0.02 if imp >= 0 else imp - 0.02, yy,
                    f"{imp:+.3f}", va="center", fontsize=9,
                    ha="left" if imp >= 0 else "right")
        ax.set_yticks(y2)
        ax.set_yticklabels(domains_sorted)
        ax.set_xlabel("Score improvement (RAG - Direct)")
        overall_imp = summary.get("improvement_pct", 0)
        ax.set_title(f"(b) RAG improvement (+{overall_imp:.1f}% overall)")
        ax.grid(axis="y", visible=False)

    fig.suptitle(f"RAG pipeline evaluation (n = {summary.get('n_questions', '?')})",
                fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    pu.save_figure(fig, "fig_rag_comparison")
    print("Done: fig_rag_comparison")


def main():
    print("=" * 60)
    print("Generating experiment result figures")
    print("=" * 60)

    plot_timeseries_benchmark()
    plot_vlm_results()
    plot_llm_qa()
    plot_rag_comparison()

    print("\nAll available figures generated.")


if __name__ == "__main__":
    main()
