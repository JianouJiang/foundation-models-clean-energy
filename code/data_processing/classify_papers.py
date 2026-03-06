#!/usr/bin/env python3
"""Classify collected papers by energy domain, FM type, task, and deployment strategy.

Uses keyword matching + concept scoring for robust multi-label classification.
"""
import json
import os
import re
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
INPUT_FILE = os.path.join(DATA_DIR, "openalex_papers.json")
OUTPUT_FILE = os.path.join(DATA_DIR, "classified_papers.csv")

# ============================================================
# Classification rules (keyword patterns in title + abstract)
# ============================================================

ENERGY_DOMAIN_RULES = {
    "hydropower": r"\b(hydro.?power|hydroelectric|reservoir|dam\b|streamflow|"
                  r"river flow|water resource|turbine.*water|fish passage|"
                  r"flood control|hydrology|inflow forecast)",
    "wind": r"\b(wind (power|energy|turbine|farm|speed|forecast)|"
            r"offshore wind|blade (defect|damage|inspect)|nacelle|SCADA.*wind|"
            r"wind generation|yaw)",
    "solar": r"\b(solar (energy|power|panel|cell|irradiance|forecast)|"
             r"photovoltaic|PV (module|panel|defect|system)|"
             r"electroluminescence|solar farm|inverter.*solar)",
    "grid": r"\b(power (grid|system|flow|quality)|smart grid|"
            r"electricity (market|price|load|demand)|microgrid|"
            r"grid stability|frequency (regul|control)|voltage|"
            r"energy storage|battery|demand response)",
    "ecological": r"\b(ecolog|wildlife|bird|fish|bat |species|"
                  r"biodiversity|habitat|environmental monitor|"
                  r"collision risk|avian|marine life|coral)",
}

FM_TYPE_RULES = {
    "LLM": r"\b(large language model|LLM|GPT-[234]|GPT.?4|ChatGPT|"
           r"BERT|LLaMA|Llama[- ]|Qwen|Mistral|ChatGLM|Baichuan|"
           r"instruction tun|prompt engineer|chain.of.thought|"
           r"language model.*pre.train|retrieval.augmented|RAG\b)",
    "VLM": r"\b(vision.language|VLM|CLIP|BLIP|LLaVA|GPT.?4V|"
           r"visual question|image.text|segment anything|SAM\b|"
           r"zero.shot.*classif.*image|DINOv2|visual foundation)",
    "TSFM": r"\b(time.series foundation|TimeGPT|Chronos|Moirai|"
            r"Lag.Llama|MOMENT|PatchTST|TimesFM|Timer\b|Time.LLM|"
            r"time.series.*pre.train|iTransformer|one fits all|"
            r"foundation.*forecast|pre.train.*time.series)",
    "diffusion": r"\b(diffusion model|DDPM|stable diffusion|"
                 r"denoising diffusion|score.based|DALL.E|"
                 r"generative.*synthetic|latent diffusion|"
                 r"conditional.*diffusion|data augment.*generat)",
    "multimodal": r"\b(multimodal|multi.modal|ImageBind|"
                  r"cross.modal|agent.based.*LLM|LLM.*agent|"
                  r"tool.*language model|ReAct|autonomous agent|"
                  r"multi.*modality.*fusion)",
    "standard_transformer": r"\b(transformer|attention mechanism|"
                            r"self.attention|informer|autoformer|"
                            r"FEDformer|temporal fusion|"
                            r"encoder.decoder.*forecast)",
}

TASK_RULES = {
    "forecasting": r"\b(forecast|predict|prediction|time.series|"
                   r"regression|load forecast|generation forecast|"
                   r"nowcast|day.ahead|short.term|long.term.*predict|"
                   r"wind speed predict|power predict|irradiance predict)",
    "fault_detection": r"\b(fault (detect|diagnos|classif)|"
                       r"defect (detect|classif|segment)|"
                       r"anomaly detect|damage detect|"
                       r"predictive maintenance|condition monitor|"
                       r"health monitor|crack detect|hot.?spot)",
    "anomaly_narration": r"\b(anomaly.*narrat|anomaly.*explain|"
                         r"natural language.*anomal|explainab|"
                         r"interpretab.*anomal|narrat.*fault)",
    "nlp_qa": r"\b(question answer|Q\&?A|knowledge (base|graph|manag)|"
              r"information extract|text min|named entity|"
              r"document.*query|chatbot|conversational|dialogue|"
              r"report generat|text classif.*energy)",
    "image_inspection": r"\b(image.*inspect|visual inspect|"
                        r"drone.*inspect|aerial.*inspect|"
                        r"infrared.*inspect|thermal.*inspect|"
                        r"image.*segment|object detect.*energy|"
                        r"remote sens.*monitor)",
    "data_augmentation": r"\b(data augment|synthetic data|"
                         r"image generat|scenario generat|"
                         r"oversampl|class imbalanc|"
                         r"generat.*train|artificial.*sample)",
    "optimization": r"\b(optim|scheduling|dispatch|planning|"
                    r"energy manage|demand side|unit commitment|"
                    r"economic dispatch|reinforcement learn.*energy|"
                    r"multi.objective.*energy)",
}

DEPLOYMENT_RULES = {
    "zero_shot": r"\b(zero.shot|zero shot|without.*train|"
                 r"no.*fine.?tun|out.of.the.box)",
    "few_shot": r"\b(few.shot|few shot|in.context learn|"
                r"k.shot|one.shot|prompt.*example)",
    "fine_tuned": r"\b(fine.tun|transfer learn|domain adapt|"
                  r"LoRA|adapter|prefix tun|parameter.efficient|"
                  r"PEFT|instruction.*tun)",
    "rag": r"\b(retrieval.augmented|RAG\b|retriev.*generat|"
           r"knowledge.*retriev|vector.*database|embedding.*search)",
    "agent": r"\b(agent|agentic|tool.?use|ReAct|"
             r"autonomous.*reason|multi.step.*reason)",
}


def classify_text(text, rules):
    """Return all matching categories for a given text."""
    text = text.lower()
    matches = []
    for category, pattern in rules.items():
        if re.search(pattern, text, re.IGNORECASE):
            matches.append(category)
    return matches


def is_fm_paper(paper):
    """Filter: does this paper actually involve foundation models (not just standard DL)?"""
    text = f"{paper.get('title', '')} {paper.get('abstract', '')}".lower()
    # Must mention at least one FM-class concept
    fm_indicators = [
        r"foundation model", r"large language model", r"\bLLM\b",
        r"\bGPT\b", r"pre.train.*large", r"CLIP\b", r"segment anything",
        r"\bSAM\b", r"vision.language", r"time.series foundation",
        r"Chronos", r"Moirai", r"Lag.Llama", r"MOMENT\b", r"PatchTST",
        r"TimesFM", r"TimeGPT", r"diffusion model",
        r"ChatGPT", r"LLaMA", r"Qwen", r"ChatGLM", r"BERT",
        r"generative AI", r"zero.shot", r"few.shot", r"prompt",
        r"retrieval.augmented", r"\bRAG\b", r"fine.tun.*pretrain",
        r"transfer learn.*pretrain",
    ]
    return any(re.search(p, text, re.IGNORECASE) for p in fm_indicators)


def classify_all():
    """Classify all collected papers and save as CSV."""
    print("Loading papers...")
    with open(INPUT_FILE) as f:
        papers = json.load(f)
    print(f"  Loaded {len(papers)} papers")

    # Filter to FM-related papers
    fm_papers = [p for p in papers if is_fm_paper(p)]
    print(f"  FM-related: {len(fm_papers)} papers")

    rows = []
    for p in fm_papers:
        text = f"{p.get('title', '')} {p.get('abstract', '')}"

        domains = classify_text(text, ENERGY_DOMAIN_RULES)
        fm_types = classify_text(text, FM_TYPE_RULES)
        tasks = classify_text(text, TASK_RULES)
        deployments = classify_text(text, DEPLOYMENT_RULES)

        # Only keep papers with at least one energy domain match
        if not domains:
            # Check if it's a general energy/AI paper
            if re.search(r"\b(energy|power|electric|renewable)\b", text, re.IGNORECASE):
                domains = ["general_energy"]
            else:
                continue

        rows.append({
            "openalex_id": p["openalex_id"],
            "doi": p.get("doi", ""),
            "title": p.get("title", ""),
            "year": p.get("year"),
            "cited_by_count": p.get("cited_by_count", 0),
            "venue": p.get("venue", ""),
            "authors": "; ".join(p.get("authors", [])[:5]),
            "institutions": "; ".join(p.get("institutions", [])[:3]),
            "countries": "; ".join(p.get("countries", [])),
            "open_access": p.get("open_access", False),
            "n_references": p.get("n_references", 0),
            "abstract": p.get("abstract", "")[:500],
            # Classification results
            "energy_domains": "|".join(domains) if domains else "unclassified",
            "fm_types": "|".join(fm_types) if fm_types else "unclassified",
            "tasks": "|".join(tasks) if tasks else "unclassified",
            "deployment": "|".join(deployments) if deployments else "not_specified",
            # Primary labels (first match)
            "primary_domain": domains[0] if domains else "unclassified",
            "primary_fm_type": fm_types[0] if fm_types else "unclassified",
            "primary_task": tasks[0] if tasks else "unclassified",
        })

    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nClassified {len(df)} FM+energy papers → {OUTPUT_FILE}")

    # Summary statistics
    print(f"\n{'='*60}")
    print("CLASSIFICATION SUMMARY")
    print(f"{'='*60}")

    print(f"\nBy Energy Domain (primary):")
    for domain, count in df["primary_domain"].value_counts().items():
        print(f"  {domain:25s} {count:5d}")

    print(f"\nBy FM Type (primary):")
    for fmtype, count in df["primary_fm_type"].value_counts().items():
        print(f"  {fmtype:25s} {count:5d}")

    print(f"\nBy Task (primary):")
    for task, count in df["primary_task"].value_counts().items():
        print(f"  {task:25s} {count:5d}")

    print(f"\nBy Year:")
    for year, count in df["year"].value_counts().sort_index().items():
        print(f"  {year}: {count}")

    return df


if __name__ == "__main__":
    classify_all()
