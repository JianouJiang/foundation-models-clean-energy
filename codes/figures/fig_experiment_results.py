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
                fontsize=12, y=1.02)
    fig.tight_layout()
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

    # (a) Model comparison bar chart
    ax = axes[0]
    models = []
    accs = []
    f1s = []
    for name, metrics in data.items():
        if isinstance(metrics, dict) and "accuracy" in metrics:
            models.append(name)
            accs.append(metrics["accuracy"])
            f1s.append(metrics["f1"])

    x = np.arange(len(models))
    width = 0.35

    bars1 = ax.bar(x - width / 2, accs, width, label="Accuracy",
                   color=colors[0], alpha=0.85, edgecolor="white")
    bars2 = ax.bar(x + width / 2, f1s, width, label="F1 Score",
                   color=colors[1], alpha=0.85, edgecolor="white")

    ax.set_xticks(x)
    ax.set_xticklabels(models, rotation=35, ha="right", fontsize=7)
    ax.set_ylabel("Score")
    ax.set_ylim(0, 1.1)
    ax.set_title("(a) Model Comparison")
    ax.legend(fontsize=8)

    # Annotate bars
    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
               f"{bar.get_height():.2f}", ha="center", fontsize=7)
    for bar in bars2:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
               f"{bar.get_height():.2f}", ha="center", fontsize=7)

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
                fontsize=12, y=1.02)
    fig.tight_layout()
    pu.save_figure(fig, "fig_vlm_inspection")
    print("Done: fig_vlm_inspection")


def plot_llm_qa():
    """Plot LLM Q&A results. Uses dedicated file or falls back to RAG baseline."""
    # Try dedicated Q&A file first, fall back to RAG direct baseline
    fpath = os.path.join(RESULTS_DIR, "llm_energy_qa.json")
    rag_path = os.path.join(RESULTS_DIR, "rag_pipeline.json")

    domain_scores = {}
    n_q = 0

    if os.path.exists(fpath):
        with open(fpath) as f:
            data = json.load(f)
        domain_scores = data.get("domain_scores", {})
        n_q = data.get("n_questions", 0)
        source = "dedicated"
    elif os.path.exists(rag_path):
        with open(rag_path) as f:
            data = json.load(f)
        by_domain = data.get("summary", {}).get("by_domain", {})
        domain_scores = {d: v["direct_mean"] for d, v in by_domain.items()}
        n_q = data.get("summary", {}).get("n_questions", 15)
        source = "RAG baseline"
    else:
        print("Skipping LLM Q&A (no results)")
        return

    colors = pu.COLORS
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # (a) Direct LLM score by domain
    ax = axes[0]
    if domain_scores:
        domains = list(domain_scores.keys())
        scores = [domain_scores[d] for d in domains]
        bar_colors = [colors[i % len(colors)] for i in range(len(domains))]

        bars = ax.barh(domains, scores, color=bar_colors, alpha=0.85, edgecolor="white")
        for bar, sc in zip(bars, scores):
            ax.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height() / 2,
                   f"{sc:.3f}", va="center", fontsize=9)

        ax.set_xlabel("Mean Keyword Match Score")
        ax.set_xlim(0, 1.15)
        ax.set_title("(a) Direct LLM Score by Domain")
        ax.invert_yaxis()

    # (b) Direct vs RAG comparison (if RAG data available)
    ax = axes[1]
    if os.path.exists(rag_path):
        with open(rag_path) as f:
            rag_data = json.load(f)
        by_domain = rag_data.get("summary", {}).get("by_domain", {})
        if by_domain:
            domains = list(by_domain.keys())
            direct_scores = [by_domain[d]["direct_mean"] for d in domains]
            rag_scores = [by_domain[d]["rag_mean"] for d in domains]

            x = np.arange(len(domains))
            w = 0.35
            bars1 = ax.bar(x - w/2, direct_scores, w, label="Direct LLM",
                           color=colors[4], alpha=0.85, edgecolor="white")
            bars2 = ax.bar(x + w/2, rag_scores, w, label="RAG-augmented",
                           color=colors[0], alpha=0.85, edgecolor="white")

            for bar, val in zip(bars1, direct_scores):
                if val > 0:
                    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                           f"{val:.2f}", ha="center", fontsize=8)
            for bar, val in zip(bars2, rag_scores):
                if val > 0:
                    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                           f"{val:.2f}", ha="center", fontsize=8)

            ax.set_xticks(x)
            ax.set_xticklabels(domains, rotation=30, ha="right", fontsize=9)
            ax.set_ylabel("Mean Score")
            ax.set_ylim(0, 1.2)
            ax.legend(loc="upper right", fontsize=9)
            ax.set_title("(b) Direct LLM vs RAG by Domain")

    fig.suptitle(f"LLM Energy Domain Q&A (Qwen2.5-7B, n={n_q}, {source})",
                fontsize=12, y=1.02)
    fig.tight_layout()
    pu.save_figure(fig, "fig_llm_qa")
    print(f"Done: fig_llm_qa (source: {source})")


def plot_rag_comparison():
    """Plot RAG vs direct LLM comparison."""
    fpath = os.path.join(RESULTS_DIR, "rag_pipeline.json")
    if not os.path.exists(fpath):
        print("Skipping RAG pipeline (no results)")
        return

    with open(fpath) as f:
        data = json.load(f)

    colors = pu.COLORS
    summary = data.get("summary", {})

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # (a) Direct vs RAG by domain
    ax = axes[0]
    by_domain = summary.get("by_domain", {})
    if by_domain:
        domains = list(by_domain.keys())
        direct = [by_domain[d]["direct_mean"] for d in domains]
        rag = [by_domain[d]["rag_mean"] for d in domains]

        x = np.arange(len(domains))
        width = 0.35

        bars1 = ax.bar(x - width / 2, direct, width, label="Direct LLM",
                       color=colors[3], alpha=0.85, edgecolor="white")
        bars2 = ax.bar(x + width / 2, rag, width, label="RAG-augmented",
                       color=colors[0], alpha=0.85, edgecolor="white")

        ax.set_xticks(x)
        ax.set_xticklabels(domains, rotation=30, ha="right", fontsize=8)
        ax.set_ylabel("Score")
        ax.set_ylim(0, 1.1)
        ax.set_title("(a) Score by Domain")
        ax.legend(fontsize=9)

    # (b) Overall comparison with error bars
    ax = axes[1]
    methods = ["Direct LLM", "RAG-augmented"]
    means = [summary.get("direct_llm", {}).get("mean_score", 0),
             summary.get("rag_augmented", {}).get("mean_score", 0)]
    stds = [summary.get("direct_llm", {}).get("std_score", 0),
            summary.get("rag_augmented", {}).get("std_score", 0)]

    bars = ax.bar(methods, means, yerr=stds, capsize=8,
                 color=[colors[3], colors[0]], alpha=0.85, edgecolor="white")
    for bar, mean in zip(bars, means):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
               f"{mean:.3f}", ha="center", fontsize=11, fontweight="bold")

    improvement = summary.get("improvement_pct", 0)
    ax.set_ylabel("Score")
    ax.set_ylim(0, 1.2)
    ax.set_title(f"(b) Overall: RAG improvement = {improvement:+.1f}%")

    fig.suptitle(f"RAG Pipeline: Direct LLM vs RAG-Augmented (n={summary.get('n_questions', '?')})",
                fontsize=12, y=1.02)
    fig.tight_layout()
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
