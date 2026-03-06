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

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "codes", "results")
FIG_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "manuscript", "figures")
os.makedirs(FIG_DIR, exist_ok=True)


def load_experiment_results():
    """Load results from all experiments."""
    results = {}

    for fname in ["timeseries_benchmark.json", "vlm_inspection.json",
                   "llm_energy_qa.json", "rag_pipeline.json",
                   "reproducibility_audit.json"]:
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
            "perf_metric": "Accuracy",
            "compute_tflops": 0.1,
            "setup_hours": 1,
            "labeled_data": 0,
            "category": "nlp",
        },
        {
            "strategy": "RAG",
            "task": "Domain Q&A",
            "model": "Qwen2.5-7B + RAG",
            "performance": 0.0,
            "perf_metric": "Accuracy",
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

    # LLM Q&A results
    qa = exp_results.get("llm_energy_qa", {})
    if qa:
        summary = qa.get("summary", {})
        for s in strategies:
            if s["category"] == "nlp":
                if s["strategy"] == "Zero-shot FM":
                    s["performance"] = summary.get("overall_accuracy", 0)

    # RAG results
    rag = exp_results.get("rag_pipeline", {})
    if rag:
        summary = rag.get("summary", {})
        for s in strategies:
            if s["strategy"] == "RAG" and s["category"] == "nlp":
                rag_mean = summary.get("rag_augmented", {}).get("mean_score", 0)
                s["performance"] = round(rag_mean, 3)
                # Also update direct LLM from RAG experiment
                direct_mean = summary.get("direct_llm", {}).get("mean_score", 0)
                for s2 in strategies:
                    if s2["strategy"] == "Zero-shot FM" and s2["category"] == "nlp":
                        if s2["performance"] == 0:
                            s2["performance"] = round(direct_mean, 3)

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
    """Plot performance vs compute cost with Pareto frontier."""
    fig, ax = plt.subplots(figsize=(10, 7))

    colors = pu.COLORS
    category_colors = {
        "time-series": colors[0],
        "vision": colors[1],
        "nlp": colors[2],
    }
    category_labels = {
        "time-series": "Time-Series Forecasting",
        "vision": "Visual Inspection",
        "nlp": "Domain Q&A",
    }

    markers = {
        "Statistical": "s",
        "Classical ML": "D",
        "Fine-tuned DL": "^",
        "Zero-shot FM": "o",
        "Few-shot FM": "p",
        "RAG": "*",
    }

    # Plot each strategy
    plotted_cats = set()
    plotted_strats = set()

    for s in strategies:
        if s["performance"] == 0:
            continue

        cat = s["category"]
        strat = s["strategy"]
        color = category_colors[cat]
        marker = markers.get(strat, "o")
        size = 150 if s.get("pareto_optimal") else 80

        # Legend labels
        cat_label = category_labels[cat] if cat not in plotted_cats else None
        plotted_cats.add(cat)

        ax.scatter(s["compute_tflops"], s["performance"],
                  c=color, marker=marker, s=size,
                  edgecolors="black" if s.get("pareto_optimal") else "gray",
                  linewidths=2 if s.get("pareto_optimal") else 0.5,
                  zorder=5)

        # Label
        offset = (8, 8)
        if s["strategy"] == "Statistical":
            offset = (8, -12)
        elif s["strategy"] == "RAG":
            offset = (-60, 8)

        ax.annotate(f"{s['model']}\n({s['strategy']})",
                   (s["compute_tflops"], s["performance"]),
                   fontsize=7, ha="left",
                   xytext=offset, textcoords="offset points",
                   arrowprops=dict(arrowstyle="-", color="gray", lw=0.5))

    # Draw Pareto frontier
    pareto_points = [(s["compute_tflops"], s["performance"])
                     for s in strategies if s.get("pareto_optimal") and s["performance"] > 0]
    if len(pareto_points) >= 2:
        pareto_points.sort(key=lambda p: p[0])
        xs, ys = zip(*pareto_points)
        ax.plot(xs, ys, "k--", alpha=0.5, linewidth=1.5, label="Pareto frontier")

    ax.set_xscale("log")
    ax.set_xlabel("Compute Cost (relative TFLOPS)")
    ax.set_ylabel("Performance (normalized, higher = better)")
    ax.set_title("FM Deployment Strategy: Performance vs Compute Cost")

    # Custom legend
    from matplotlib.lines import Line2D
    legend_elements = []
    for cat, label in category_labels.items():
        legend_elements.append(Line2D([0], [0], marker="o", color="w",
                              markerfacecolor=category_colors[cat],
                              markersize=10, label=label))
    for strat, marker in markers.items():
        legend_elements.append(Line2D([0], [0], marker=marker, color="w",
                              markerfacecolor="gray",
                              markersize=8, label=strat))
    legend_elements.append(Line2D([0], [0], linestyle="--", color="black",
                          label="Pareto frontier"))

    ax.legend(handles=legend_elements, loc="lower right", fontsize=8,
             ncol=2, framealpha=0.9)
    ax.set_ylim(0, 1.05)
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    pu.save_figure(fig, "fig_pareto_frontier")
    print("Saved: fig_pareto_frontier")
    return fig


def plot_deployment_comparison(strategies):
    """Bar chart comparing deployment strategies across tasks."""
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))

    categories = ["time-series", "vision", "nlp"]
    titles = ["(a) Load Forecasting", "(b) Visual Inspection", "(c) Domain Q&A"]
    colors = pu.COLORS

    for ax, cat, title in zip(axes, categories, titles):
        cat_strategies = [s for s in strategies
                         if s["category"] == cat and s["performance"] > 0]
        if not cat_strategies:
            ax.text(0.5, 0.5, "No data", transform=ax.transAxes, ha="center")
            ax.set_title(title)
            continue

        names = [f"{s['model']}\n({s['strategy']})" for s in cat_strategies]
        perfs = [s["performance"] for s in cat_strategies]
        bar_colors = [colors[i % len(colors)] for i in range(len(cat_strategies))]

        bars = ax.barh(range(len(names)), perfs, color=bar_colors, edgecolor="white")

        # Annotate bars
        for bar, perf in zip(bars, perfs):
            ax.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height() / 2,
                   f"{perf:.3f}", va="center", fontsize=8)

        ax.set_yticks(range(len(names)))
        ax.set_yticklabels(names, fontsize=8)
        ax.set_xlim(0, 1.15)
        ax.set_xlabel("Performance")
        ax.set_title(title, fontweight="bold")
        ax.invert_yaxis()

    fig.suptitle("FM Deployment Strategy Comparison Across Energy Tasks", fontsize=12, y=1.02)
    fig.tight_layout()
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
