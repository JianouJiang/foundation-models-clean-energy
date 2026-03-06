#!/usr/bin/env python3
"""Scientometric analysis of the FM+energy literature.

Generates statistics, fits growth models, and produces analysis data
for figure generation scripts.
"""
import json
import os
import sys
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.stats import pearsonr, spearmanr
from collections import Counter

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "utils"))

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "code", "results")
os.makedirs(RESULTS_DIR, exist_ok=True)


def load_data():
    df = pd.read_csv(os.path.join(DATA_DIR, "classified_papers.csv"))
    # Filter out 2026 partial year for trend analysis
    return df


def exponential_model(x, a, b):
    return a * np.exp(b * x)


def logistic_model(x, L, k, x0):
    return L / (1 + np.exp(-k * (x - x0)))


def publication_growth_analysis(df):
    """Analyze publication growth trends with exponential fit."""
    print("\n" + "="*60)
    print("PUBLICATION GROWTH ANALYSIS")
    print("="*60)

    # Exclude 2026 (partial year)
    df_trend = df[df["year"] <= 2025].copy()
    yearly = df_trend.groupby("year").size().reset_index(name="count")

    # Exponential fit on years 2019-2025 (post-BERT era)
    mask = yearly["year"] >= 2019
    x = yearly.loc[mask, "year"].values - 2019
    y = yearly.loc[mask, "count"].values

    try:
        popt, pcov = curve_fit(exponential_model, x, y, p0=[50, 0.5], maxfev=5000)
        y_pred = exponential_model(x, *popt)
        ss_res = np.sum((y - y_pred)**2)
        ss_tot = np.sum((y - np.mean(y))**2)
        r_squared = 1 - ss_res / ss_tot
        doubling_time = np.log(2) / popt[1] if popt[1] > 0 else float('inf')

        print(f"Exponential fit: y = {popt[0]:.1f} * exp({popt[1]:.3f} * t)")
        print(f"R² = {r_squared:.4f}")
        print(f"Doubling time: {doubling_time:.1f} years")
        print(f"Annual growth rate: {(np.exp(popt[1])-1)*100:.0f}%")
    except Exception as e:
        print(f"Exponential fit failed: {e}")
        popt = None
        r_squared = None
        doubling_time = None

    # Growth by FM type
    print("\nGrowth by FM Type (2019–2025):")
    fm_yearly = df_trend[df_trend["year"] >= 2019].groupby(
        ["year", "primary_fm_type"]).size().unstack(fill_value=0)
    print(fm_yearly.to_string())

    # Save results
    results = {
        "yearly_counts": yearly.to_dict(orient="records"),
        "exp_fit_params": popt.tolist() if popt is not None else None,
        "r_squared": float(r_squared) if r_squared else None,
        "doubling_time_years": float(doubling_time) if doubling_time else None,
        "fm_type_yearly": fm_yearly.reset_index().to_dict(orient="records"),
    }

    return results


def domain_analysis(df):
    """Analyze distribution across energy domains."""
    print("\n" + "="*60)
    print("ENERGY DOMAIN ANALYSIS")
    print("="*60)

    # Explode multi-label domains
    domain_counts = Counter()
    for domains in df["energy_domains"]:
        for d in str(domains).split("|"):
            domain_counts[d] += 1

    print("\nDomain distribution (multi-label):")
    for domain, count in domain_counts.most_common():
        print(f"  {domain:25s} {count:5d}")

    # Domain × FM type cross-tabulation
    print("\nDomain × FM Type cross-tab (primary labels):")
    cross = pd.crosstab(df["primary_domain"], df["primary_fm_type"], margins=True)
    print(cross.to_string())

    # Domain × Task cross-tabulation
    print("\nDomain × Task cross-tab (primary labels):")
    cross2 = pd.crosstab(df["primary_domain"], df["primary_task"], margins=True)
    print(cross2.to_string())

    return {
        "domain_counts": dict(domain_counts),
        "domain_fm_cross": cross.to_dict(),
        "domain_task_cross": cross2.to_dict(),
    }


def citation_analysis(df):
    """Analyze citation patterns."""
    print("\n" + "="*60)
    print("CITATION ANALYSIS")
    print("="*60)

    # Top cited papers
    top = df.nlargest(20, "cited_by_count")[["title", "year", "cited_by_count",
                                              "primary_fm_type", "primary_domain"]]
    print("\nTop 20 most-cited papers:")
    for _, row in top.iterrows():
        print(f"  [{row['year']}] {row['cited_by_count']:5d} cites | "
              f"{row['primary_fm_type']:10s} | {row['title'][:60]}")

    # Citation stats by FM type
    print("\nCitation statistics by FM type:")
    for fmtype in df["primary_fm_type"].unique():
        subset = df[df["primary_fm_type"] == fmtype]
        cites = subset["cited_by_count"]
        print(f"  {fmtype:25s}: n={len(subset):4d}, "
              f"median={cites.median():.0f}, mean={cites.mean():.0f}, "
              f"max={cites.max()}")

    return {
        "top_papers": top.to_dict(orient="records"),
        "citation_by_fm_type": df.groupby("primary_fm_type")["cited_by_count"].describe().to_dict(),
    }


def geographic_analysis(df):
    """Analyze geographic distribution."""
    print("\n" + "="*60)
    print("GEOGRAPHIC ANALYSIS")
    print("="*60)

    country_counts = Counter()
    for countries in df["countries"]:
        for c in str(countries).split("; "):
            c = c.strip()
            if c and c != "nan":
                country_counts[c] += 1

    print("\nTop 15 countries:")
    for country, count in country_counts.most_common(15):
        print(f"  {country:5s} {count:5d}")

    # Institution counts
    inst_counts = Counter()
    for institutions in df["institutions"]:
        for inst in str(institutions).split("; "):
            inst = inst.strip()
            if inst and inst != "nan":
                inst_counts[inst] += 1

    print("\nTop 15 institutions:")
    for inst, count in inst_counts.most_common(15):
        print(f"  {inst[:50]:50s} {count:4d}")

    return {
        "country_counts": dict(country_counts.most_common(30)),
        "institution_counts": dict(inst_counts.most_common(30)),
    }


def keyword_analysis(df):
    """Analyze keyword co-occurrence and temporal evolution."""
    print("\n" + "="*60)
    print("KEYWORD ANALYSIS")
    print("="*60)

    # Build keyword co-occurrence from titles/abstracts
    # Use common energy + AI terms
    important_terms = [
        "transformer", "BERT", "GPT", "LLM", "foundation model",
        "deep learning", "neural network", "machine learning",
        "LSTM", "CNN", "attention", "pre-train", "fine-tun",
        "transfer learn", "zero-shot", "few-shot", "prompt",
        "forecasting", "prediction", "fault detection", "anomaly",
        "defect", "inspection", "classification", "segmentation",
        "solar", "wind", "hydropower", "grid", "battery",
        "renewable", "energy", "power system", "SCADA",
        "diffusion", "generative", "augmentation", "synthetic",
        "retrieval", "RAG", "knowledge", "question answer",
        "CLIP", "SAM", "vision", "image", "multimodal",
        "time series", "Chronos", "Moirai", "PatchTST",
    ]

    # Temporal keyword evolution
    print("\nKeyword temporal evolution (selected terms):")
    for term in ["foundation model", "LLM", "GPT", "deep learning",
                 "transformer", "diffusion", "zero-shot", "RAG",
                 "CLIP", "time series foundation"]:
        yearly = []
        for year in range(2019, 2026):
            year_df = df[df["year"] == year]
            count = 0
            for _, row in year_df.iterrows():
                text = f"{row.get('title', '')} {row.get('abstract', '')}".lower()
                if term.lower() in text:
                    count += 1
            yearly.append(count)
        print(f"  {term:25s}: {yearly}")

    return {"keyword_temporal": "see console output"}


def venue_analysis(df):
    """Analyze publication venues."""
    print("\n" + "="*60)
    print("VENUE ANALYSIS")
    print("="*60)

    venue_counts = df["venue"].value_counts().head(20)
    print("\nTop 20 venues:")
    for venue, count in venue_counts.items():
        print(f"  {venue[:60]:60s} {count:4d}")

    return {"top_venues": venue_counts.to_dict()}


def maturity_index(df):
    """Compute research maturity index for each FM type × energy domain cell."""
    print("\n" + "="*60)
    print("RESEARCH MATURITY INDEX")
    print("="*60)

    domains = ["wind", "solar", "hydropower", "grid", "ecological"]
    fm_types = ["LLM", "VLM", "TSFM", "diffusion", "multimodal"]

    maturity = {}
    for domain in domains:
        for fm in fm_types:
            # Count papers in this cell
            mask_domain = df["energy_domains"].str.contains(domain, na=False)
            mask_fm = df["fm_types"].str.contains(fm, na=False)
            cell_df = df[mask_domain & mask_fm]

            n_papers = len(cell_df)
            avg_cites = cell_df["cited_by_count"].mean() if n_papers > 0 else 0
            recent = len(cell_df[cell_df["year"] >= 2024])

            # Maturity index: weighted combination
            # Higher = more mature research area
            idx = (n_papers * 0.5 + avg_cites * 0.01 + recent * 0.3)
            maturity[f"{domain}_{fm}"] = {
                "n_papers": n_papers,
                "avg_citations": round(avg_cites, 1),
                "recent_2024_plus": recent,
                "maturity_index": round(idx, 2),
            }

    print(f"\n{'Domain':12s} {'FM':12s} {'Papers':>7s} {'AvgCite':>8s} "
          f"{'Recent':>7s} {'Maturity':>9s}")
    print("-" * 60)
    for key, vals in sorted(maturity.items(),
                            key=lambda x: -x[1]["maturity_index"]):
        parts = key.split("_", 1)
        print(f"{parts[0]:12s} {parts[1]:12s} {vals['n_papers']:7d} "
              f"{vals['avg_citations']:8.1f} {vals['recent_2024_plus']:7d} "
              f"{vals['maturity_index']:9.2f}")

    return maturity


def run_all():
    """Run all analyses and save results."""
    df = load_data()
    print(f"Loaded {len(df)} classified papers")

    results = {}
    results["growth"] = publication_growth_analysis(df)
    results["domains"] = domain_analysis(df)
    results["citations"] = citation_analysis(df)
    results["geographic"] = geographic_analysis(df)
    results["keywords"] = keyword_analysis(df)
    results["venues"] = venue_analysis(df)
    results["maturity"] = maturity_index(df)

    # Open access stats
    oa = df["open_access"].sum()
    print(f"\nOpen access: {oa}/{len(df)} ({100*oa/len(df):.0f}%)")

    # Save results
    output = os.path.join(RESULTS_DIR, "scientometrics_results.json")
    # Convert numpy types for JSON serialization
    def convert(obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        elif isinstance(obj, (np.floating,)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, pd.DataFrame):
            return obj.to_dict()
        return obj

    with open(output, "w") as f:
        json.dump(results, f, indent=2, default=convert)
    print(f"\nResults saved to {output}")

    return results


if __name__ == "__main__":
    run_all()
