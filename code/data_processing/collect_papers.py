#!/usr/bin/env python3
"""Collect foundation-model + energy papers from OpenAlex API.

OpenAlex is free, no API key needed. Rate limit: ~10 req/s for polite pool.
We use the 'mailto' parameter to get into the polite pool (faster).
"""
import json
import os
import sys
import time
import requests

BASE_URL = "https://api.openalex.org/works"
MAILTO = "jianou.jiang@eng.ox.ac.uk"
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "openalex_papers.json")

# Search queries — broad enough to capture FM+energy papers
QUERIES = [
    '("foundation model" OR "large language model" OR "LLM") AND ("energy" OR "solar" OR "wind" OR "hydropower" OR "power system")',
    '("GPT" OR "BERT" OR "transformer") AND ("renewable energy" OR "wind power" OR "solar power" OR "photovoltaic")',
    '("vision language model" OR "multimodal" OR "CLIP" OR "segment anything") AND ("energy" OR "turbine" OR "solar panel" OR "inspection")',
    '("time series foundation" OR "TimeGPT" OR "Chronos" OR "Moirai" OR "Lag-Llama") AND ("energy" OR "forecasting" OR "power")',
    '("diffusion model" OR "generative AI") AND ("energy" OR "wind" OR "solar" OR "power" OR "renewable")',
    '("pretrained transformer" OR "foundation model") AND ("grid" OR "electricity" OR "hydropower" OR "dam" OR "turbine")',
    '("large language model" OR "LLM" OR "GPT-4") AND ("fault detection" OR "anomaly" OR "maintenance" OR "SCADA")',
    '("retrieval augmented generation" OR "RAG") AND ("energy" OR "power" OR "wind" OR "solar")',
]

def fetch_page(query, cursor="*", per_page=100):
    """Fetch one page of results from OpenAlex."""
    params = {
        "search": query,
        "filter": "from_publication_date:2017-01-01,to_publication_date:2026-12-31",
        "per_page": per_page,
        "cursor": cursor,
        "mailto": MAILTO,
        "select": "id,doi,title,publication_year,type,cited_by_count,"
                  "authorships,primary_location,concepts,keywords,"
                  "open_access,referenced_works,abstract_inverted_index,"
                  "topics",
    }
    resp = requests.get(BASE_URL, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def reconstruct_abstract(inverted_index):
    """Reconstruct abstract text from OpenAlex inverted index."""
    if not inverted_index:
        return ""
    word_positions = []
    for word, positions in inverted_index.items():
        for pos in positions:
            word_positions.append((pos, word))
    word_positions.sort()
    return " ".join(w for _, w in word_positions)


def extract_paper_data(work):
    """Extract relevant fields from an OpenAlex work object."""
    # Authors and affiliations
    authors = []
    institutions = []
    countries = []
    for authorship in (work.get("authorships") or []):
        author = authorship.get("author", {})
        authors.append(author.get("display_name", ""))
        for inst in (authorship.get("institutions") or []):
            inst_name = inst.get("display_name", "")
            if inst_name and inst_name not in institutions:
                institutions.append(inst_name)
            cc = inst.get("country_code", "")
            if cc and cc not in countries:
                countries.append(cc)

    # Venue
    loc = work.get("primary_location") or {}
    source = loc.get("source") or {}
    venue = source.get("display_name", "")

    # Keywords and concepts
    keywords = [kw.get("keyword", "") for kw in (work.get("keywords") or [])]
    concepts = [(c.get("display_name", ""), c.get("score", 0))
                for c in (work.get("concepts") or [])]

    # Topics
    topics = [(t.get("display_name", ""), t.get("score", 0))
              for t in (work.get("topics") or [])]

    return {
        "openalex_id": work.get("id", ""),
        "doi": work.get("doi", ""),
        "title": work.get("title", ""),
        "year": work.get("publication_year"),
        "type": work.get("type", ""),
        "cited_by_count": work.get("cited_by_count", 0),
        "authors": authors,
        "institutions": institutions,
        "countries": countries,
        "venue": venue,
        "keywords": keywords,
        "concepts": concepts,
        "topics": topics,
        "open_access": (work.get("open_access") or {}).get("is_oa", False),
        "abstract": reconstruct_abstract(work.get("abstract_inverted_index")),
        "n_references": len(work.get("referenced_works") or []),
    }


def collect_all():
    """Run all queries and deduplicate results."""
    os.makedirs(DATA_DIR, exist_ok=True)

    all_papers = {}  # keyed by openalex_id for dedup
    total_fetched = 0

    for qi, query in enumerate(QUERIES):
        print(f"\n[Query {qi+1}/{len(QUERIES)}] {query[:80]}...")
        cursor = "*"
        query_count = 0
        pages = 0

        while cursor and pages < 20:  # Cap at 20 pages (2000 results) per query
            try:
                data = fetch_page(query, cursor=cursor)
            except Exception as e:
                print(f"  Error fetching page: {e}")
                break

            results = data.get("results", [])
            if not results:
                break

            for work in results:
                paper = extract_paper_data(work)
                oid = paper["openalex_id"]
                if oid not in all_papers:
                    all_papers[oid] = paper
                    query_count += 1

            cursor = data.get("meta", {}).get("next_cursor")
            pages += 1
            total_fetched += len(results)
            time.sleep(0.1)  # polite rate limiting

        print(f"  → {query_count} new papers (total unique: {len(all_papers)})")

    papers_list = list(all_papers.values())

    # Save raw data
    with open(OUTPUT_FILE, "w") as f:
        json.dump(papers_list, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print(f"Total unique papers collected: {len(papers_list)}")
    print(f"Saved to: {OUTPUT_FILE}")

    # Quick stats
    years = [p["year"] for p in papers_list if p["year"]]
    if years:
        print(f"Year range: {min(years)}–{max(years)}")
    cited = [p["cited_by_count"] for p in papers_list]
    print(f"Citations: median={sorted(cited)[len(cited)//2]}, "
          f"max={max(cited)}, total={sum(cited)}")
    oa_count = sum(1 for p in papers_list if p["open_access"])
    print(f"Open access: {oa_count}/{len(papers_list)} ({100*oa_count/len(papers_list):.0f}%)")

    return papers_list


if __name__ == "__main__":
    collect_all()
