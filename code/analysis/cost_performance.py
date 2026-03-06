#!/usr/bin/env python3
"""Part C: Deployment Cost-Performance Analysis with Pareto Frontier.

Analyzes the cost-performance tradeoffs of different FM deployment strategies
for energy applications, using data from our benchmark experiments.
"""
import os, sys, json
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "utils"))
import plotting_utils as pu
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "code", "results")
FIG_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "paper", "figures")
os.makedirs(FIG_DIR, exist_ok=True)


def load_experiment_results():
    """Load results from all experiments."""
    results = {}

    for fname in ["timeseries_benchmark.json", "vlm_inspection.json",
                   "llm_energy_qa.json", "llm_energy_qa_3b.json",
                   "rag_pipeline.json", "reproducibility_audit.json"]:
        fpath = os.path.join(RESULTS_DIR, fname)
        if os.path.exists(fpath):
            with open(fpath) as f:
                results[fname.replace(".json", "")] = json.load(f)
            print(f"  Loaded {fname}")
        else:
            print(f"  Missing {fname}")

    return results


def build_deployment_matrix():
    """Build the deployment strategy cost-performance matrix.

    Combines experimental results with literature estimates for a comprehensive
    comparison of FM deployment strategies across energy tasks.
    """
    # Each entry: (strategy, task, performance_metric, performance_value,
    #              compute_cost_relative, setup_effort, data_requirement)
    #
    # Performance: normalized 0-1 (higher=better)
    # Cost: relative compute cost (1=cheapest)
    # Setup: qualitative 1-5 (1=easiest)
    # Data: labeled samples needed (0=none)

    strategies = []

    # --- Time-series forecasting strategies ---
    strategies.extend([
        {
            "strategy": "Zero-shot FM",
            "task": "Load forecasting",
            "model": "Chronos-T5-Small",
            "performance": 0.0,  # Will be filled from results
            "perf_metric": "1 - nMAE",
            "compute_tflops": 0.02,
            "setup_hours": 1,
            "labeled_data": 0,
            "category": "time-series",
        },
        {
            "strategy": "Fine-tuned DL",
            "task": "Load forecasting",
            "model": "LSTM",
            "performance": 0.0,
            "perf_metric": "1 - nMAE",
            "compute_tflops": 0.5,
            "setup_hours": 20,
            "labeled_data": 5000,
            "category": "time-series",
        },
        {
            "strategy": "Classical ML",
            "task": "Load forecasting",
            "model": "XGBoost",
            "performance": 0.0,
            "perf_metric": "1 - nMAE",
            "compute_tflops": 0.001,
            "setup_hours": 10,
            "labeled_data": 5000,
            "category": "time-series",
        },
        {
            "strategy": "Statistical",
            "task": "Load forecasting",
            "model": "ARIMA",
            "performance": 0.0,
            "perf_metric": "1 - nMAE",
            "compute_tflops": 0.0001,
            "setup_hours": 5,
            "labeled_data": 1000,
            "category": "time-series",
        },
    ])

    # --- VLM inspection strategies ---
    strategies.extend([
        {
            "strategy": "Zero-shot FM",
            "task": "Defect detection",
            "model": "CLIP ViT-B-32",
            "performance": 0.0,
            "perf_metric": "F1",
            "compute_tflops": 0.01,
            "setup_hours": 2,
            "labeled_data": 0,
            "category": "vision",
        },
        {
            "strategy": "Few-shot FM",
            "task": "Defect detection",
            "model": "CLIP + LogReg",
            "performance": 0.0,
            "perf_metric": "F1",
            "compute_tflops": 0.02,
            "setup_hours": 5,
            "labeled_data": 50,
            "category": "vision",
        },
    ])

    # --- LLM Q&A strategies ---
    strategies.extend([
        {
            "strategy": "Zero-shot FM",
            "task": "Domain Q&A",
            "model": "Qwen2.5-7B",
            "performance": 0.0,
            "perf_metric": "Keyword score",
            "compute_tflops": 0.1,
            "setup_hours": 1,
            "labeled_data": 0,
            "category": "nlp",
        },
        {
            "strategy": "Zero-shot FM (small)",
            "task": "Domain Q&A",
            "model": "Qwen2.5-3B",
            "performance": 0.0,
            "perf_metric": "Keyword score",
            "compute_tflops": 0.04,
            "setup_hours": 1,
            "labeled_data": 0,
            "category": "nlp",
        },
        {
            "strategy": "RAG",
            "task": "Domain Q&A",
            "model": "Qwen2.5-7B + RAG",
            "performance": 0.0,
            "perf_metric": "Keyword score",
            "compute_tflops": 0.15,
            "setup_hours": 10,
            "labeled_data": 0,
            "category": "nlp",
        },
    ])

    return strategies


def fill_from_experiments(strategies, exp_results):
    """Fill strategy performance values from experimental results."""

    # Time-series results
    ts = exp_results.get("timeseries_benchmark", {})
    if ts:
        # Normalize MAE: performance = 1 - (MAE / max_MAE)
        maes = {}
        for model, metrics in ts.items():
            if isinstance(metrics, dict) and "MAE" in metrics:
                maes[model] = metrics["MAE"]

        if maes:
            max_mae = max(maes.values()) * 1.1  # slight padding
            for s in strategies:
                if s["category"] == "time-series":
                    if s["model"] == "Chronos-T5-Small" and "Chronos (zero-shot)" in maes:
                        s["performance"] = round(1 - maes["Chronos (zero-shot)"] / max_mae, 3)
                    elif s["model"] == "LSTM" and "LSTM" in maes:
                        s["performance"] = round(1 - maes["LSTM"] / max_mae, 3)
                    elif s["model"] == "XGBoost" and "XGBoost" in maes:
                        s["performance"] = round(1 - maes["XGBoost"] / max_mae, 3)
                    elif s["model"] == "ARIMA" and "ARIMA" in maes:
                        s["performance"] = round(1 - maes["ARIMA"] / max_mae, 3)

    # VLM results
    vlm = exp_results.get("vlm_inspection", {})
    if vlm:
        for s in strategies:
            if s["category"] == "vision":
                if s["model"] == "CLIP ViT-B-32":
                    clip_res = vlm.get("CLIP zero-shot (ensemble)", {})
                    s["performance"] = clip_res.get("f1", 0)
                elif s["model"] == "CLIP + LogReg":
                    sup_res = vlm.get("Supervised (CLIP+LogReg)", {})
                    s["performance"] = sup_res.get("f1", 0)

    # LLM Q&A results (top-level keys: mean_keyword_score, accuracy_at_04)
    qa = exp_results.get("llm_energy_qa", {})
    if qa:
        for s in strategies:
            if s["category"] == "nlp":
                if s["strategy"] == "Zero-shot FM" and s["model"] == "Qwen2.5-7B":
                    s["performance"] = qa.get("mean_keyword_score", 0)

    # LLM Q&A 3B results
    qa_3b = exp_results.get("llm_energy_qa_3b", {})
    if qa_3b:
        for s in strategies:
            if s["category"] == "nlp" and s["model"] == "Qwen2.5-3B":
                s["performance"] = qa_3b.get("mean_keyword_score", 0)

    # RAG results
    rag = exp_results.get("rag_pipeline", {})
    if rag:
        summary = rag.get("summary", {})
        for s in strategies:
            if s["strategy"] == "RAG" and s["category"] == "nlp":
                rag_mean = summary.get("rag_augmented", {}).get("mean_score", 0)
                s["performance"] = round(rag_mean, 3)

    return strategies


def compute_pareto_frontier(strategies):
    """Identify Pareto-optimal strategies (maximize performance, minimize cost)."""
    points = [(s["performance"], s["compute_tflops"]) for s in strategies]

    pareto = []
    for i, (perf_i, cost_i) in enumerate(points):
        dominated = False
        for j, (perf_j, cost_j) in enumerate(points):
            if i != j and perf_j >= perf_i and cost_j <= cost_i:
                if perf_j > perf_i or cost_j < cost_i:
                    dominated = True
                    break
        if not dominated:
            pareto.append(i)

    for i, s in enumerate(strategies):
        s["pareto_optimal"] = i in pareto

    return strategies, pareto


def plot_pareto(strategies):
    """Plot performance vs compute cost with Pareto frontier.
    Color encodes setup effort, shape encodes task category.
    Only Pareto-optimal points are labeled (Tufte: reduce clutter).
    """
    import matplotlib.cm as cm
    from matplotlib.colors import Normalize
    from matplotlib.lines import Line2D

    fig, ax = plt.subplots(figsize=(10, 7))

    category_markers = {
        "time-series": "o",
        "vision": "s",
        "nlp": "D",
    }
    category_labels = {
        "time-series": "Time-series forecasting",
        "vision": "Visual inspection",
        "nlp": "Domain Q&A",
    }

    # Collect valid strategies
    valid = [s for s in strategies if s["performance"] > 0]
    setup_vals = np.array([s["setup_hours"] for s in valid])
    norm = Normalize(vmin=max(setup_vals.min(), 0.01), vmax=setup_vals.max())
    cmap = cm.get_cmap("plasma")

    for s in valid:
        marker = category_markers.get(s["category"], "o")
        size = 120 if s.get("pareto_optimal") else 60
        edgewidth = 2 if s.get("pareto_optimal") else 0.3
        edgecolor = "black" if s.get("pareto_optimal") else "0.6"

        ax.scatter(s["compute_tflops"], s["performance"],
                   c=[cmap(norm(s["setup_hours"]))], marker=marker, s=size,
                   edgecolors=edgecolor, linewidths=edgewidth, zorder=5)

    # Draw Pareto frontier
    pareto_pts = sorted(
        [(s["compute_tflops"], s["performance"], f"{s['model']}\n({s['strategy']})")
         for s in valid if s.get("pareto_optimal")],
        key=lambda p: p[0])
    if len(pareto_pts) >= 2:
        px, py, _ = zip(*pareto_pts)
        ax.plot(px, py, "k--", alpha=0.5, linewidth=1.5)

    # Label ONLY Pareto points — custom offsets to avoid overlap
    custom_offsets = [(10, -22), (10, 14), (-80, -20), (14, 14)]
    for i, (x, y, lab) in enumerate(pareto_pts):
        ox, oy = custom_offsets[i % len(custom_offsets)]
        ha_ann = "left" if ox > 0 else "right"
        va_ann = "bottom" if oy > 0 else "top"
        ax.annotate(lab, (x, y), fontsize=9, ha=ha_ann,
                    xytext=(ox, oy), textcoords="offset points",
                    arrowprops=dict(arrowstyle="-", color="0.4", lw=0.5))

    ax.set_xscale("log")
    ax.set_xlabel("Compute cost (relative TFLOPS, log scale)")
    ax.set_ylabel("Performance (normalized)")
    ax.set_title("Deployment strategies: Pareto frontier")
    ax.set_ylim(0, 1.05)

    # Colorbar for setup effort
    sm = cm.ScalarMappable(norm=norm, cmap=cmap)
    cb = fig.colorbar(sm, ax=ax, fraction=0.03, pad=0.02)
    cb.set_label("Setup effort (hours)")

    # Category legend
    legend_elements = [
        Line2D([0], [0], marker=m, color="w", markerfacecolor="0.5",
               markersize=8, label=label)
        for cat, (m, label) in zip(
            category_markers.keys(),
            zip(category_markers.values(), category_labels.values()))
    ]
    legend_elements.append(Line2D([0], [0], ls="--", color="black",
                                  label="Pareto frontier"))
    ax.legend(handles=legend_elements, loc="lower right", fontsize=8,
              framealpha=0.9)

    fig.tight_layout()
    pu.save_figure(fig, "fig_pareto_frontier")
    print("Saved: fig_pareto_frontier")
    return fig


def plot_deployment_comparison(strategies):
    """Dot plot comparing deployment strategies across tasks (Tufte: less ink than bars)."""
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))

    categories = ["time-series", "vision", "nlp"]
    titles = ["(a) Load forecasting", "(b) Visual inspection", "(c) Domain Q&A"]
    colors = pu.COLORS

    for ax, cat, title in zip(axes, categories, titles):
        cat_strategies = sorted(
            [s for s in strategies if s["category"] == cat and s["performance"] > 0],
            key=lambda s: s["performance"])
        if not cat_strategies:
            ax.text(0.5, 0.5, "No data", transform=ax.transAxes, ha="center")
            ax.set_title(title)
            continue

        names = [f"{s['model']} ({s['strategy']})" for s in cat_strategies]
        perfs = [s["performance"] for s in cat_strategies]
        y = np.arange(len(names))

        ax.hlines(y, 0, perfs, color="0.80", lw=1)
        ax.plot(perfs, y, "o", color=colors[0], markersize=7, zorder=5)
        for yy, perf in zip(y, perfs):
            ax.text(perf + 0.02, yy, f"{perf:.3f}", va="center", fontsize=8)

        ax.set_yticks(y)
        ax.set_yticklabels(names, fontsize=8)
        ax.set_xlim(0, 1.1)
        ax.set_xlabel("Performance")
        ax.set_title(title)
        ax.grid(axis="y", visible=False)

    fig.suptitle("FM deployment strategy comparison", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    pu.save_figure(fig, "fig_deployment_comparison")
    print("Saved: fig_deployment_comparison")
    return fig


def plot_setup_effort(strategies):
    """Bubble chart: performance vs setup effort, bubble size = data requirement."""
    fig, ax = plt.subplots(figsize=(9, 6))

    colors = pu.COLORS
    category_colors = {
        "time-series": colors[0],
        "vision": colors[1],
        "nlp": colors[2],
    }

    for s in strategies:
        if s["performance"] == 0:
            continue

        size = max(30, (s["labeled_data"] / 50) + 30)
        size = min(size, 300)

        ax.scatter(s["setup_hours"], s["performance"],
                  s=size, c=category_colors[s["category"]],
                  alpha=0.7, edgecolors="black", linewidths=0.5)

        ax.annotate(s["model"], (s["setup_hours"], s["performance"]),
                   fontsize=7, xytext=(5, 5), textcoords="offset points")

    ax.set_xlabel("Setup Effort (hours)")
    ax.set_ylabel("Performance (normalized)")
    ax.set_title("Performance vs Setup Effort\n(bubble size = labeled data requirement)")
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    pu.save_figure(fig, "fig_setup_effort")
    print("Saved: fig_setup_effort")
    return fig


def main():
    print("=" * 60)
    print("PART C: Cost-Performance Analysis")
    print("=" * 60)

    # Load experiment results
    print("\nLoading experiment results...")
    exp_results = load_experiment_results()

    # Build strategy matrix
    strategies = build_deployment_matrix()

    # Fill from experiments
    strategies = fill_from_experiments(strategies, exp_results)

    # Compute Pareto frontier
    strategies, pareto_idx = compute_pareto_frontier(strategies)

    # Print summary table
    print(f"\n{'Strategy':15s} {'Task':18s} {'Model':20s} {'Perf':>6s} {'Cost':>8s} {'Pareto':>7s}")
    print("-" * 80)
    for s in strategies:
        pareto_str = "YES" if s.get("pareto_optimal") else ""
        print(f"{s['strategy']:15s} {s['task']:18s} {s['model']:20s} "
              f"{s['performance']:6.3f} {s['compute_tflops']:8.4f} {pareto_str:>7s}")

    # Generate figures
    print("\nGenerating figures...")
    plot_pareto(strategies)
    plot_deployment_comparison(strategies)
    plot_setup_effort(strategies)

    # Save results
    output = os.path.join(RESULTS_DIR, "cost_performance.json")
    with open(output, "w") as f:
        json.dump(strategies, f, indent=2, default=str)
    print(f"\nResults saved to {output}")

    return strategies


if __name__ == "__main__":
    main()
