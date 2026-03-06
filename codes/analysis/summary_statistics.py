#!/usr/bin/env python3
"""Summary statistics and statistical tests on trends in the FM+energy literature."""
import os, sys, json
import numpy as np
import pandas as pd
from scipy import stats

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "codes", "results")
os.makedirs(RESULTS_DIR, exist_ok=True)


def main():
    print("=" * 60)
    print("Summary Statistics & Trend Tests")
    print("=" * 60)

    df = pd.read_csv(os.path.join(DATA_DIR, "classified_papers.csv"))
    print(f"Total papers: {len(df)}")

    results = {}

    # 1. Basic counts
    results["total_papers"] = len(df)
    results["year_range"] = f"{int(df['year'].min())}-{int(df['year'].max())}"

    # 2. FM type distribution
    fm_counts = df["primary_fm_type"].value_counts().to_dict()
    results["fm_type_distribution"] = {k: int(v) for k, v in fm_counts.items()}

    # 3. Domain distribution
    domain_counts = df["primary_domain"].value_counts().to_dict()
    results["domain_distribution"] = {k: int(v) for k, v in domain_counts.items()}

    # 4. Year-over-year growth
    yearly = df.groupby("year").size()
    years = yearly.index.values
    counts = yearly.values

    # Growth rates
    growth_rates = []
    for i in range(1, len(counts)):
        if counts[i - 1] > 0:
            gr = (counts[i] - counts[i - 1]) / counts[i - 1] * 100
            growth_rates.append({"year": int(years[i]), "growth_pct": round(gr, 1)})

    results["yearly_counts"] = {int(y): int(c) for y, c in zip(years, counts)}
    results["growth_rates"] = growth_rates

    # 5. Exponential growth test
    # Fit: log(count) = a + b*year
    mask = counts > 0
    log_counts = np.log(counts[mask])
    years_fit = years[mask]
    slope, intercept, r_value, p_value, std_err = stats.linregress(years_fit, log_counts)
    results["exponential_fit"] = {
        "slope": round(slope, 4),
        "intercept": round(intercept, 4),
        "r_squared": round(r_value ** 2, 4),
        "p_value": float(f"{p_value:.2e}"),
        "doubling_time_years": round(np.log(2) / slope, 2) if slope > 0 else None,
        "annual_growth_rate_pct": round((np.exp(slope) - 1) * 100, 1),
    }

    # 6. Chi-squared test: FM type vs domain independence
    ct = pd.crosstab(df["primary_fm_type"], df["primary_domain"])
    chi2, p_chi2, dof, expected = stats.chi2_contingency(ct)
    results["chi2_fm_vs_domain"] = {
        "chi2": round(chi2, 2),
        "p_value": float(f"{p_chi2:.2e}"),
        "dof": int(dof),
        "significant": p_chi2 < 0.05,
        "interpretation": "FM type and energy domain are NOT independent" if p_chi2 < 0.05
                         else "No significant association between FM type and domain",
    }

    # 7. Citation statistics
    cite_stats = df["cited_by_count"].describe()
    results["citation_stats"] = {
        "mean": round(cite_stats["mean"], 1),
        "median": round(cite_stats["50%"], 1),
        "std": round(cite_stats["std"], 1),
        "max": int(cite_stats["max"]),
        "q25": round(cite_stats["25%"], 1),
        "q75": round(cite_stats["75%"], 1),
    }

    # Kruskal-Wallis test: do citation counts differ by FM type?
    groups = [g["cited_by_count"].values for _, g in df.groupby("primary_fm_type")]
    groups = [g for g in groups if len(g) > 5]
    if len(groups) >= 2:
        h_stat, p_kw = stats.kruskal(*groups)
        results["kruskal_citations_by_fm"] = {
            "H_statistic": round(h_stat, 2),
            "p_value": float(f"{p_kw:.2e}"),
            "significant": p_kw < 0.05,
        }

    # 8. Open access rate and trend
    if "open_access" in df.columns:
        oa_by_year = df.groupby("year")["open_access"].agg(["sum", "count"])
        oa_by_year["pct"] = oa_by_year["sum"] / oa_by_year["count"] * 100
        results["open_access_trend"] = {
            int(y): round(r["pct"], 1) for y, r in oa_by_year.iterrows()
        }
        # Mann-Kendall trend test (simple version)
        oa_pcts = oa_by_year["pct"].values
        n_oa = len(oa_pcts)
        s = 0
        for i in range(n_oa):
            for j in range(i + 1, n_oa):
                s += np.sign(oa_pcts[j] - oa_pcts[i])
        results["oa_trend_kendall_S"] = int(s)
        results["oa_trend_direction"] = "increasing" if s > 0 else "decreasing" if s < 0 else "no trend"

    # 9. Top venues
    top_venues = df["venue"].value_counts().head(15)
    results["top_venues"] = {k: int(v) for k, v in top_venues.items() if k and k != "nan"}

    # 10. Concentration metrics
    # Gini coefficient for country distribution
    if "countries" in df.columns:
        country_series = df["countries"].dropna().str.split(";").explode().str.strip()
        country_counts = country_series.value_counts()
        sorted_counts = np.sort(country_counts.values)
        n = len(sorted_counts)
        cum = np.cumsum(sorted_counts)
        gini = 1 - 2 * cum.sum() / (n * sorted_counts.sum()) + 1 / n
        results["geographic_concentration"] = {
            "n_countries": int(n),
            "gini_coefficient": round(gini, 3),
            "top3_share_pct": round(100 * sorted_counts[-3:].sum() / sorted_counts.sum(), 1),
        }

    # Print summary
    print(f"\nExponential growth: R²={results['exponential_fit']['r_squared']}, "
          f"doubling time={results['exponential_fit']['doubling_time_years']} years")
    print(f"Chi² FM×Domain: χ²={results['chi2_fm_vs_domain']['chi2']}, "
          f"p={results['chi2_fm_vs_domain']['p_value']}")
    print(f"Citation stats: median={results['citation_stats']['median']}, "
          f"mean={results['citation_stats']['mean']}")

    # Save
    output = os.path.join(RESULTS_DIR, "summary_statistics.json")
    with open(output, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults saved to {output}")

    return results


if __name__ == "__main__":
    main()
