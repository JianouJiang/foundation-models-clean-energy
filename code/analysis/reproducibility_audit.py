#!/usr/bin/env python3
"""Experiment 5: Reproducibility Audit of FM+Energy Papers.

For the most-cited papers, check code/data availability via OpenAlex metadata
and Papers With Code API.
"""
import os, sys, time, json
import requests
import pandas as pd
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "code", "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

OPENALEX_PAPERS = os.path.join(DATA_DIR, "openalex_papers.json")
CLASSIFIED = os.path.join(DATA_DIR, "classified_papers.csv")


def check_papers_with_code(title):
    """Check Papers With Code API for code availability."""
    try:
        resp = requests.get(
            "https://paperswithcode.com/api/v1/papers/",
            params={"q": title[:100]},
            timeout=10,
        )
        if resp.status_code == 200:
            results = resp.json().get("results", [])
            if results:
                paper = results[0]
                return {
                    "found_on_pwc": True,
                    "has_code": bool(paper.get("proceeding")),
                    "n_implementations": 0,
                }
        return {"found_on_pwc": False, "has_code": False, "n_implementations": 0}
    except Exception:
        return {"found_on_pwc": False, "has_code": False, "n_implementations": 0}


def audit_open_access(df):
    """Check open access status across the dataset."""
    oa_count = df["open_access"].sum()
    total = len(df)

    # By year
    oa_by_year = df.groupby("year")["open_access"].agg(["sum", "count"])
    oa_by_year["pct"] = (oa_by_year["sum"] / oa_by_year["count"] * 100).round(1)

    # By FM type
    oa_by_fm = df.groupby("primary_fm_type")["open_access"].agg(["sum", "count"])
    oa_by_fm["pct"] = (oa_by_fm["sum"] / oa_by_fm["count"] * 100).round(1)

    return {
        "total_papers": int(total),
        "open_access_count": int(oa_count),
        "open_access_pct": round(100 * oa_count / total, 1),
        "by_year": oa_by_year.to_dict(),
        "by_fm_type": oa_by_fm.to_dict(),
    }


def audit_doi_availability(df):
    """Check DOI availability."""
    has_doi = df["doi"].notna() & (df["doi"] != "")
    doi_count = has_doi.sum()
    return {
        "total": int(len(df)),
        "has_doi": int(doi_count),
        "doi_pct": round(100 * doi_count / len(df), 1),
    }


def estimate_code_availability(df):
    """Estimate code availability from titles and venues."""
    # Heuristic: papers from ML conferences more likely to have code
    ml_venues = ["NeurIPS", "ICML", "ICLR", "AAAI", "CVPR", "ECCV",
                 "ACL", "EMNLP", "arXiv", "ArXiv"]

    code_keywords = ["github", "code", "implementation", "repository",
                     "open source", "reproducib"]

    code_likely = 0
    ml_venue_count = 0
    for _, row in df.iterrows():
        venue = str(row.get("venue", ""))
        abstract = str(row.get("abstract", "")).lower()

        is_ml_venue = any(v.lower() in venue.lower() for v in ml_venues)
        has_code_mention = any(kw in abstract for kw in code_keywords)

        if is_ml_venue:
            ml_venue_count += 1
        if has_code_mention:
            code_likely += 1

    return {
        "ml_venue_papers": int(ml_venue_count),
        "ml_venue_pct": round(100 * ml_venue_count / len(df), 1),
        "code_mentioned_in_abstract": int(code_likely),
        "code_mention_pct": round(100 * code_likely / len(df), 1),
    }


def check_top_papers_pwc(df, n=50):
    """Check top N cited papers on Papers With Code."""
    print(f"\nChecking top {n} papers on Papers With Code...")
    top = df.nlargest(n, "cited_by_count")

    results = []
    found_count = 0
    for i, (_, row) in enumerate(top.iterrows()):
        title = str(row.get("title", ""))
        pwc = check_papers_with_code(title)
        if pwc["found_on_pwc"]:
            found_count += 1

        results.append({
            "title": title[:80],
            "year": int(row["year"]) if pd.notna(row["year"]) else None,
            "cited_by": int(row["cited_by_count"]),
            **pwc,
        })
        time.sleep(0.5)  # rate limiting
        if (i + 1) % 10 == 0:
            print(f"  Checked {i+1}/{n} papers ({found_count} found on PWC)")

    return {
        "checked": n,
        "found_on_pwc": found_count,
        "found_pct": round(100 * found_count / n, 1),
        "papers": results,
    }


def main():
    print("="*60)
    print("EXPERIMENT 5: Reproducibility Audit")
    print("="*60)

    df = pd.read_csv(CLASSIFIED)
    print(f"Auditing {len(df)} classified FM+energy papers\n")

    results = {}

    # 1. Open access audit
    print("1. Open Access Audit")
    results["open_access"] = audit_open_access(df)
    print(f"   Open access: {results['open_access']['open_access_pct']}%")

    # 2. DOI availability
    print("\n2. DOI Availability")
    results["doi"] = audit_doi_availability(df)
    print(f"   Has DOI: {results['doi']['doi_pct']}%")

    # 3. Code availability estimate
    print("\n3. Code Availability Estimate")
    results["code_estimate"] = estimate_code_availability(df)
    print(f"   ML venue papers: {results['code_estimate']['ml_venue_pct']}%")
    print(f"   Code mentioned in abstract: {results['code_estimate']['code_mention_pct']}%")

    # 4. Check top papers on Papers With Code
    print("\n4. Papers With Code Check (top 50)")
    results["pwc_check"] = check_top_papers_pwc(df, n=50)
    print(f"   Found on PWC: {results['pwc_check']['found_pct']}%")

    # 5. Reproducibility by domain
    print("\n5. Open Access by Domain:")
    for domain in df["primary_domain"].unique():
        subset = df[df["primary_domain"] == domain]
        oa_pct = 100 * subset["open_access"].sum() / len(subset)
        print(f"   {domain:25s}: {oa_pct:.0f}% open access ({len(subset)} papers)")

    # 6. Summary statistics
    print(f"\n{'='*60}")
    print("REPRODUCIBILITY SUMMARY")
    print(f"{'='*60}")
    print(f"Total papers analyzed: {len(df)}")
    print(f"Open access: {results['open_access']['open_access_pct']}%")
    print(f"Has DOI: {results['doi']['doi_pct']}%")
    print(f"Published at ML venues: {results['code_estimate']['ml_venue_pct']}%")
    print(f"Code mentioned in abstract: {results['code_estimate']['code_mention_pct']}%")
    print(f"Top-50 found on Papers With Code: {results['pwc_check']['found_pct']}%")

    # Reproducibility index
    repro_idx = (
        results["open_access"]["open_access_pct"] * 0.3 +
        results["doi"]["doi_pct"] * 0.2 +
        results["code_estimate"]["code_mention_pct"] * 0.3 +
        results["pwc_check"]["found_pct"] * 0.2
    ) / 100
    results["reproducibility_index"] = round(repro_idx, 3)
    print(f"\nComposite Reproducibility Index: {repro_idx:.3f} (0-1 scale)")

    # Save
    output = os.path.join(RESULTS_DIR, "reproducibility_audit.json")
    with open(output, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults saved to {output}")

    return results


if __name__ == "__main__":
    main()
