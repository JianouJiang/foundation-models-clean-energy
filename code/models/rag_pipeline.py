#!/usr/bin/env python3
"""Experiment 4: RAG Pipeline for Energy Technical Documents.

Builds a simple RAG pipeline using sentence-transformers + FAISS for retrieval,
and Ollama Qwen2.5 for generation. Compares RAG-augmented vs direct LLM answers.
"""
import os, sys, time, json
import numpy as np
import warnings
warnings.filterwarnings("ignore")

np.random.seed(42)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "code", "results")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

OLLAMA_URL = "http://localhost:11434/api/generate"

# ============================================================
# Energy knowledge base - curated technical passages
# ============================================================
ENERGY_KNOWLEDGE_BASE = [
    # Hydropower
    {
        "id": "hydro_001",
        "domain": "hydropower",
        "text": "The Francis turbine is the most commonly used water turbine in hydropower plants. It operates efficiently at heads from 40 to 600 meters and can achieve efficiencies above 95%. The runner consists of curved vanes that redirect water flow from radial to axial direction. Francis turbines are reaction turbines where both the pressure and velocity of water decrease as it passes through the runner."
    },
    {
        "id": "hydro_002",
        "domain": "hydropower",
        "text": "Cavitation in hydraulic turbines occurs when local pressure drops below the vapor pressure of water, forming vapor bubbles that collapse violently. This causes pitting, erosion, vibration, and noise. The Thoma cavitation coefficient (sigma) is used to predict cavitation risk. Typical mitigation strategies include optimizing turbine draft tube design, controlling operating conditions, and applying cavitation-resistant coatings."
    },
    {
        "id": "hydro_003",
        "domain": "hydropower",
        "text": "Pumped-storage hydroelectricity (PSH) accounts for over 94% of installed global energy storage capacity. During low-demand periods, water is pumped from a lower reservoir to an upper reservoir. During peak demand, water flows back through turbines to generate electricity. Round-trip efficiency typically ranges from 70-85%. PSH provides grid-scale energy storage, frequency regulation, and spinning reserve services."
    },
    {
        "id": "hydro_004",
        "domain": "hydropower",
        "text": "Sediment transport modeling is critical for hydropower reservoir management. The Brune curve estimates trap efficiency as a function of the capacity-inflow ratio. Reservoir sedimentation reduces storage volume over time, affecting power generation capacity. Sediment flushing, sluicing, and dredging are common management strategies. Annual sediment yield varies from 50 to over 5000 t/km2 depending on climate and geology."
    },
    # Wind Energy
    {
        "id": "wind_001",
        "domain": "wind",
        "text": "Modern horizontal-axis wind turbines (HAWTs) follow the Betz limit, which states that no turbine can capture more than 59.3% of the kinetic energy in wind. The power output is proportional to the cube of wind speed: P = 0.5 * rho * A * Cp * v^3, where rho is air density, A is rotor swept area, Cp is the power coefficient, and v is wind speed. Modern turbines achieve Cp values of 0.35-0.45."
    },
    {
        "id": "wind_002",
        "domain": "wind",
        "text": "Wind turbine blade inspection traditionally requires manual visual inspection using rope access technicians or cranes, costing $10,000-30,000 per inspection. Common defects include leading edge erosion, lightning damage, trailing edge splits, and delamination. Drone-based inspection combined with AI image analysis has reduced inspection time from days to hours while improving defect detection rates."
    },
    {
        "id": "wind_003",
        "domain": "wind",
        "text": "Wake effects in wind farms cause downstream turbines to experience reduced wind speed and increased turbulence. The Jensen/PARK model estimates wake velocity deficit as a function of downstream distance and wake expansion coefficient. Wake losses typically reduce farm output by 10-20%. Active wake steering using yaw misalignment can recover 1-5% of annual energy production."
    },
    {
        "id": "wind_004",
        "domain": "wind",
        "text": "Offshore wind energy has grown rapidly, with global capacity exceeding 60 GW in 2023. Fixed-bottom foundations (monopile, jacket, gravity-based) are used in water depths up to 60 meters. Floating offshore wind platforms (spar-buoy, semi-submersible, tension-leg) enable deployment in deeper waters. The levelized cost of offshore wind has decreased from $0.16/kWh in 2010 to $0.08/kWh in 2022."
    },
    # Solar Energy
    {
        "id": "solar_001",
        "domain": "solar",
        "text": "Crystalline silicon (c-Si) solar cells dominate the photovoltaic market with over 95% market share. Monocrystalline cells achieve lab efficiencies of 26.7% (heterojunction with interdigitated back contacts) while commercial modules reach 20-22%. Common degradation modes include potential-induced degradation (PID), light-induced degradation (LID), and hotspot formation due to cell mismatch or partial shading."
    },
    {
        "id": "solar_002",
        "domain": "solar",
        "text": "Electroluminescence (EL) imaging is a non-destructive testing method for solar cells and modules. By applying forward bias current, solar cells emit near-infrared light proportional to local recombination activity. Dark areas in EL images indicate defects such as micro-cracks, broken interconnects, or shunts. Automated EL image analysis using deep learning has achieved defect detection accuracy above 95%."
    },
    {
        "id": "solar_003",
        "domain": "solar",
        "text": "Perovskite solar cells have shown rapid efficiency improvement from 3.8% in 2009 to 26.1% in 2023 (single junction). Perovskite-silicon tandem cells have reached 33.7% efficiency. Key challenges include long-term stability under heat, moisture, and UV exposure. Encapsulation strategies and compositional engineering (mixed halide, 2D/3D heterostructures) aim to achieve 25+ year operational lifetimes."
    },
    {
        "id": "solar_004",
        "domain": "solar",
        "text": "Solar irradiance forecasting is essential for grid integration of photovoltaic systems. Numerical weather prediction (NWP) models provide day-ahead forecasts with 15-25% normalized RMSE. Satellite-based nowcasting achieves 10-20% nRMSE for 1-4 hour horizons. Hybrid approaches combining NWP, satellite imagery, and machine learning have reduced forecast errors by 20-40% compared to persistence models."
    },
    # Grid and Storage
    {
        "id": "grid_001",
        "domain": "grid",
        "text": "Lithium-ion batteries dominate grid-scale energy storage with costs dropping from $1,100/kWh in 2010 to $139/kWh in 2023 (pack level). Lithium iron phosphate (LFP) chemistry has gained market share due to lower cost, longer cycle life (6000+ cycles), and improved safety compared to NMC. Grid-scale battery storage provides services including peak shaving, frequency regulation, and renewable integration."
    },
    {
        "id": "grid_002",
        "domain": "grid",
        "text": "Power system stability requires maintaining frequency within tight bounds (e.g., 50 Hz +/- 0.5 Hz in Europe). Increasing renewable penetration reduces system inertia since inverter-based resources do not inherently provide synchronous inertia. Grid-forming inverters can emulate inertial response through virtual synchronous machine (VSM) control. Synthetic inertia requirements are being introduced in grid codes worldwide."
    },
    {
        "id": "grid_003",
        "domain": "grid",
        "text": "Demand response programs enable electricity consumers to adjust their consumption in response to price signals or grid operator requests. Industrial demand response can provide 10-20% peak load reduction. Smart meters and IoT devices enable automated demand response at residential scale. Virtual power plants (VPPs) aggregate distributed energy resources including rooftop solar, batteries, and flexible loads to participate in wholesale markets."
    },
    {
        "id": "grid_004",
        "domain": "grid",
        "text": "Electric vehicle (EV) smart charging and vehicle-to-grid (V2G) technology can provide significant flexibility to power systems. A fleet of 1 million EVs with 50 kWh batteries represents 50 GWh of distributed storage capacity. Uncontrolled EV charging could increase peak demand by 30%, while smart charging algorithms can shift load to low-demand periods and provide ancillary services."
    },
    # Ecological / Environmental
    {
        "id": "eco_001",
        "domain": "ecological",
        "text": "Fish passage at hydropower dams is a critical ecological concern. Upstream passage facilities include fish ladders, fish lifts, and nature-like fishways. Downstream passage hazards include turbine strike, barotrauma, and disorientation. Turbine strike mortality rates range from 5-30% depending on turbine type and fish species. Advanced turbine designs (Alden turbine, minimum gap runner) aim to reduce fish mortality below 2%."
    },
    {
        "id": "eco_002",
        "domain": "ecological",
        "text": "Bird and bat collision mortality at wind farms is a significant environmental concern. Estimated annual bird mortality in the US from wind turbines is 140,000-500,000 birds. Radar-based detection systems can detect approaching birds and trigger turbine curtailment. Painting one blade black has been shown to reduce bird mortality by 70% in a Norwegian study. Ultrasonic deterrents show promise for reducing bat fatalities."
    },
    {
        "id": "eco_003",
        "domain": "ecological",
        "text": "Environmental DNA (eDNA) monitoring uses genetic material shed by organisms into water to detect species presence without physical capture. For hydropower impact assessment, eDNA can monitor fish community composition upstream and downstream of dams. Metabarcoding of eDNA samples can identify dozens of species simultaneously. Detection sensitivity depends on water flow, temperature, UV exposure, and sampling methodology."
    },
    {
        "id": "eco_004",
        "domain": "ecological",
        "text": "Life cycle assessment (LCA) of renewable energy technologies compares environmental impacts across the full lifecycle. Solar PV has a carbon footprint of 20-50 gCO2eq/kWh, wind power 7-15 gCO2eq/kWh, and hydropower 4-30 gCO2eq/kWh, compared to coal at 820 gCO2eq/kWh and natural gas at 490 gCO2eq/kWh. Energy payback time for solar PV is 1-3 years depending on technology and location."
    },
    # AI/ML in Energy
    {
        "id": "ai_001",
        "domain": "AI_energy",
        "text": "Transfer learning enables foundation models pretrained on large general datasets to be adapted for energy-specific tasks with limited labeled data. Fine-tuning the last few layers of a pretrained vision model (e.g., ResNet, ViT) on 100-500 labeled energy images often outperforms training from scratch on the same data. This is particularly valuable for rare fault detection where labeled examples are scarce."
    },
    {
        "id": "ai_002",
        "domain": "AI_energy",
        "text": "Time-series foundation models like Chronos (Amazon), TimesFM (Google), and MOMENT are pretrained on large corpora of time-series data from diverse domains. These models can perform zero-shot forecasting without task-specific training. On energy load forecasting benchmarks, Chronos achieves comparable or better performance than tuned statistical baselines (ARIMA, ETS) while requiring no domain-specific configuration."
    },
    {
        "id": "ai_003",
        "domain": "AI_energy",
        "text": "Retrieval-Augmented Generation (RAG) enhances LLM responses by grounding them in retrieved domain-specific documents. For energy applications, RAG pipelines can access technical standards (IEEE, IEC), equipment manuals, and regulatory documents. This reduces hallucination and provides traceable answers. Typical RAG architecture includes: document chunking, embedding with sentence transformers, vector store retrieval (FAISS, Chroma), and LLM-based answer synthesis."
    },
    {
        "id": "ai_004",
        "domain": "AI_energy",
        "text": "Federated learning enables collaborative model training across multiple energy utilities without sharing sensitive operational data. This addresses data privacy concerns while leveraging diverse datasets. Applications include collaborative load forecasting across utilities, distributed fault detection in smart grids, and privacy-preserving demand response optimization. Communication efficiency is improved through gradient compression and asynchronous aggregation."
    },
]

# ============================================================
# Evaluation questions with ground-truth answers
# ============================================================
RAG_QUESTIONS = [
    {
        "id": "q1",
        "question": "What is the maximum theoretical efficiency limit for wind turbines and what is it called?",
        "domain": "wind",
        "relevant_docs": ["wind_001"],
        "reference_answer": "The Betz limit states that no turbine can capture more than 59.3% of the kinetic energy in wind.",
        "keywords": ["betz", "59.3", "59%"],
    },
    {
        "id": "q2",
        "question": "What is cavitation in hydraulic turbines and how is it measured?",
        "domain": "hydropower",
        "relevant_docs": ["hydro_002"],
        "reference_answer": "Cavitation occurs when local pressure drops below vapor pressure, forming vapor bubbles. The Thoma cavitation coefficient (sigma) is used to predict cavitation risk.",
        "keywords": ["pressure", "vapor", "thoma", "sigma", "bubbles"],
    },
    {
        "id": "q3",
        "question": "What is the typical round-trip efficiency of pumped-storage hydroelectricity?",
        "domain": "hydropower",
        "relevant_docs": ["hydro_003"],
        "reference_answer": "Round-trip efficiency of pumped-storage hydroelectricity typically ranges from 70-85%.",
        "keywords": ["70", "85", "round-trip", "efficiency"],
    },
    {
        "id": "q4",
        "question": "What defects can electroluminescence imaging detect in solar cells?",
        "domain": "solar",
        "relevant_docs": ["solar_002"],
        "reference_answer": "EL imaging can detect micro-cracks, broken interconnects, shunts, and other defects shown as dark areas in images.",
        "keywords": ["micro-cracks", "cracks", "interconnect", "shunt", "dark"],
    },
    {
        "id": "q5",
        "question": "What is the current cost of lithium-ion battery packs for grid storage?",
        "domain": "grid",
        "relevant_docs": ["grid_001"],
        "reference_answer": "Lithium-ion battery pack costs dropped to $139/kWh in 2023, down from $1,100/kWh in 2010.",
        "keywords": ["139", "kwh", "2023"],
    },
    {
        "id": "q6",
        "question": "How much can wake effects reduce wind farm output?",
        "domain": "wind",
        "relevant_docs": ["wind_003"],
        "reference_answer": "Wake losses typically reduce wind farm output by 10-20%. Active wake steering can recover 1-5% of annual energy production.",
        "keywords": ["10", "20", "wake", "steering", "yaw"],
    },
    {
        "id": "q7",
        "question": "What is the estimated annual bird mortality from wind turbines in the US?",
        "domain": "ecological",
        "relevant_docs": ["eco_002"],
        "reference_answer": "Estimated annual bird mortality in the US from wind turbines is 140,000-500,000 birds.",
        "keywords": ["140", "500", "bird", "mortality"],
    },
    {
        "id": "q8",
        "question": "What is the carbon footprint of solar PV compared to coal?",
        "domain": "ecological",
        "relevant_docs": ["eco_004"],
        "reference_answer": "Solar PV has 20-50 gCO2eq/kWh vs coal at 820 gCO2eq/kWh.",
        "keywords": ["20", "50", "820", "gco2", "co2"],
    },
    {
        "id": "q9",
        "question": "What are the key challenges for perovskite solar cell commercialization?",
        "domain": "solar",
        "relevant_docs": ["solar_003"],
        "reference_answer": "Key challenges include long-term stability under heat, moisture, and UV exposure. Encapsulation and compositional engineering aim to achieve 25+ year lifetimes.",
        "keywords": ["stability", "heat", "moisture", "uv", "encapsulation", "lifetime"],
    },
    {
        "id": "q10",
        "question": "How do time-series foundation models like Chronos perform on energy forecasting?",
        "domain": "AI_energy",
        "relevant_docs": ["ai_002"],
        "reference_answer": "Chronos achieves comparable or better performance than tuned ARIMA/ETS baselines while requiring no domain-specific configuration.",
        "keywords": ["chronos", "zero-shot", "arima", "comparable", "baseline"],
    },
    {
        "id": "q11",
        "question": "What is the fish turbine strike mortality rate at hydropower dams?",
        "domain": "ecological",
        "relevant_docs": ["eco_001"],
        "reference_answer": "Turbine strike mortality rates range from 5-30% depending on turbine type and fish species.",
        "keywords": ["5", "30", "strike", "mortality", "fish"],
    },
    {
        "id": "q12",
        "question": "How does RAG improve LLM performance for energy applications?",
        "domain": "AI_energy",
        "relevant_docs": ["ai_003"],
        "reference_answer": "RAG reduces hallucination and provides traceable answers by grounding LLM responses in retrieved domain-specific documents like technical standards and manuals.",
        "keywords": ["hallucination", "retrieval", "document", "grounding", "traceable"],
    },
    {
        "id": "q13",
        "question": "What grid services can battery energy storage systems provide?",
        "domain": "grid",
        "relevant_docs": ["grid_001"],
        "reference_answer": "Grid-scale battery storage provides peak shaving, frequency regulation, and renewable integration services.",
        "keywords": ["peak", "frequency", "regulation", "renewable", "integration"],
    },
    {
        "id": "q14",
        "question": "What is the efficiency record for perovskite-silicon tandem solar cells?",
        "domain": "solar",
        "relevant_docs": ["solar_003"],
        "reference_answer": "Perovskite-silicon tandem cells have reached 33.7% efficiency.",
        "keywords": ["33", "tandem", "perovskite", "silicon"],
    },
    {
        "id": "q15",
        "question": "How much peak load can industrial demand response reduce?",
        "domain": "grid",
        "relevant_docs": ["grid_003"],
        "reference_answer": "Industrial demand response can provide 10-20% peak load reduction.",
        "keywords": ["10", "20", "peak", "demand", "response", "industrial"],
    },
]


def build_faiss_index(documents):
    """Build FAISS index from document texts."""
    from sentence_transformers import SentenceTransformer
    import faiss

    print("Building FAISS index from knowledge base...")
    t0 = time.time()

    model = SentenceTransformer("all-MiniLM-L6-v2")
    texts = [doc["text"] for doc in documents]
    embeddings = model.encode(texts, show_progress_bar=False)
    embeddings = np.array(embeddings, dtype=np.float32)

    # Normalize for cosine similarity
    faiss.normalize_L2(embeddings)

    # Build index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)  # Inner product = cosine similarity after normalization
    index.add(embeddings)

    elapsed = time.time() - t0
    print(f"  Indexed {len(documents)} passages in {elapsed:.1f}s (dim={dim})")
    return index, model, embeddings


def retrieve(query, index, embed_model, documents, top_k=3):
    """Retrieve top-k relevant documents for a query."""
    import faiss

    query_emb = embed_model.encode([query])
    query_emb = np.array(query_emb, dtype=np.float32)
    faiss.normalize_L2(query_emb)

    scores, indices = index.search(query_emb, top_k)
    results = []
    for score, idx in zip(scores[0], indices[0]):
        results.append({
            "doc": documents[idx],
            "score": float(score),
        })
    return results


def query_ollama(prompt, model="qwen2.5:7b", timeout=300):
    """Query Ollama local LLM."""
    import requests

    try:
        resp = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.1, "num_predict": 100},
            },
            timeout=timeout,
        )
        if resp.status_code == 200:
            return resp.json().get("response", "")
        return f"[Error: HTTP {resp.status_code}]"
    except Exception as e:
        return f"[Error: {str(e)}]"


def score_answer(answer, question_data):
    """Score an answer based on keyword matching and relevance."""
    answer_lower = answer.lower()
    keywords = question_data["keywords"]

    # Keyword match score
    matched = sum(1 for kw in keywords if kw.lower() in answer_lower)
    keyword_score = matched / len(keywords) if keywords else 0

    # Length penalty (too short = likely bad, too long = likely rambling)
    word_count = len(answer.split())
    length_score = 1.0
    if word_count < 10:
        length_score = 0.5
    elif word_count > 500:
        length_score = 0.7

    # Hallucination heuristic: check for fabricated numbers
    hallucination_penalty = 0
    import re
    numbers_in_answer = set(re.findall(r'\d+\.?\d*', answer))
    ref_numbers = set(re.findall(r'\d+\.?\d*', question_data["reference_answer"]))
    if numbers_in_answer and not numbers_in_answer.intersection(ref_numbers):
        # Answer has numbers but none match reference — possible hallucination
        hallucination_penalty = 0.2

    final_score = keyword_score * length_score - hallucination_penalty
    return max(0, min(1, final_score)), {
        "keyword_score": round(keyword_score, 3),
        "keywords_matched": matched,
        "keywords_total": len(keywords),
        "length_score": round(length_score, 3),
        "hallucination_penalty": round(hallucination_penalty, 3),
    }


def run_rag_experiment():
    """Run the full RAG vs direct LLM comparison."""
    print("=" * 60)
    print("EXPERIMENT 4: RAG Pipeline for Energy Documents")
    print("=" * 60)

    # Check Ollama availability
    import requests
    try:
        resp = requests.get("http://localhost:11434/api/tags", timeout=5)
        models = [m["name"] for m in resp.json().get("models", [])]
        print(f"Ollama available. Models: {models}")
        if not any("qwen" in m.lower() for m in models):
            print("WARNING: qwen2.5 not found. Will try anyway.")
    except Exception as e:
        print(f"WARNING: Ollama not available ({e}). Will record errors.")

    # Build knowledge base and index
    index, embed_model, embeddings = build_faiss_index(ENERGY_KNOWLEDGE_BASE)

    results = {
        "direct_llm": [],
        "rag_augmented": [],
        "retrieval_quality": [],
    }

    print(f"\nEvaluating {len(RAG_QUESTIONS)} questions...")
    print("-" * 60)

    for i, q in enumerate(RAG_QUESTIONS):
        print(f"\n[{i+1}/{len(RAG_QUESTIONS)}] {q['question'][:60]}...")

        # 1. Direct LLM (no retrieval)
        direct_prompt = (
            f"Answer the following energy engineering question concisely and accurately.\n\n"
            f"Question: {q['question']}\n\n"
            f"Answer:"
        )
        t0 = time.time()
        direct_answer = query_ollama(direct_prompt)
        direct_time = time.time() - t0

        direct_score, direct_details = score_answer(direct_answer, q)
        results["direct_llm"].append({
            "question_id": q["id"],
            "domain": q["domain"],
            "answer": direct_answer[:500],
            "score": round(direct_score, 3),
            "details": direct_details,
            "time_sec": round(direct_time, 2),
        })
        print(f"  Direct LLM:  score={direct_score:.3f} ({direct_details['keywords_matched']}/{direct_details['keywords_total']} keywords)")

        # 2. RAG-augmented
        retrieved = retrieve(q["question"], index, embed_model,
                           ENERGY_KNOWLEDGE_BASE, top_k=3)

        context = "\n\n".join([
            f"[Source {j+1}]: {r['doc']['text']}"
            for j, r in enumerate(retrieved)
        ])

        rag_prompt = (
            f"Use the following technical reference material to answer the question. "
            f"Base your answer on the provided sources. Be concise and accurate.\n\n"
            f"Reference Material:\n{context}\n\n"
            f"Question: {q['question']}\n\n"
            f"Answer:"
        )
        t0 = time.time()
        rag_answer = query_ollama(rag_prompt)
        rag_time = time.time() - t0

        rag_score, rag_details = score_answer(rag_answer, q)
        results["rag_augmented"].append({
            "question_id": q["id"],
            "domain": q["domain"],
            "answer": rag_answer[:500],
            "score": round(rag_score, 3),
            "details": rag_details,
            "time_sec": round(rag_time, 2),
        })
        print(f"  RAG:         score={rag_score:.3f} ({rag_details['keywords_matched']}/{rag_details['keywords_total']} keywords)")

        # 3. Retrieval quality — did we retrieve the right docs?
        retrieved_ids = [r["doc"]["id"] for r in retrieved]
        relevant_ids = q["relevant_docs"]
        recall = sum(1 for rid in relevant_ids if rid in retrieved_ids) / len(relevant_ids)
        results["retrieval_quality"].append({
            "question_id": q["id"],
            "retrieved": retrieved_ids,
            "relevant": relevant_ids,
            "recall_at_3": round(recall, 3),
            "top_score": round(retrieved[0]["score"], 4) if retrieved else 0,
        })

        time.sleep(0.5)  # Rate limiting for Ollama

    # Compute summary statistics
    direct_scores = [r["score"] for r in results["direct_llm"]]
    rag_scores = [r["score"] for r in results["rag_augmented"]]
    retrieval_recalls = [r["recall_at_3"] for r in results["retrieval_quality"]]

    # Per-domain breakdown
    domains = sorted(set(q["domain"] for q in RAG_QUESTIONS))
    domain_results = {}
    for domain in domains:
        d_direct = [r["score"] for r, q in zip(results["direct_llm"], RAG_QUESTIONS)
                    if q["domain"] == domain]
        d_rag = [r["score"] for r, q in zip(results["rag_augmented"], RAG_QUESTIONS)
                 if q["domain"] == domain]
        domain_results[domain] = {
            "n_questions": len(d_direct),
            "direct_mean": round(np.mean(d_direct), 3) if d_direct else 0,
            "rag_mean": round(np.mean(d_rag), 3) if d_rag else 0,
            "improvement": round(np.mean(d_rag) - np.mean(d_direct), 3) if d_direct else 0,
        }

    summary = {
        "n_questions": len(RAG_QUESTIONS),
        "n_knowledge_passages": len(ENERGY_KNOWLEDGE_BASE),
        "embedding_model": "all-MiniLM-L6-v2",
        "llm_model": "qwen2.5:7b",
        "direct_llm": {
            "mean_score": round(np.mean(direct_scores), 3),
            "std_score": round(np.std(direct_scores), 3),
            "median_score": round(np.median(direct_scores), 3),
        },
        "rag_augmented": {
            "mean_score": round(np.mean(rag_scores), 3),
            "std_score": round(np.std(rag_scores), 3),
            "median_score": round(np.median(rag_scores), 3),
        },
        "retrieval": {
            "mean_recall_at_3": round(np.mean(retrieval_recalls), 3),
        },
        "improvement": round(np.mean(rag_scores) - np.mean(direct_scores), 3),
        "improvement_pct": round(
            100 * (np.mean(rag_scores) - np.mean(direct_scores)) /
            max(np.mean(direct_scores), 0.01), 1
        ),
        "by_domain": domain_results,
    }

    results["summary"] = summary

    # Print summary
    print(f"\n{'=' * 60}")
    print("RAG EXPERIMENT RESULTS")
    print(f"{'=' * 60}")
    print(f"Questions: {summary['n_questions']}")
    print(f"Knowledge passages: {summary['n_knowledge_passages']}")
    print(f"Embedding model: {summary['embedding_model']}")
    print(f"LLM: {summary['llm_model']}")
    print(f"\n{'Method':25s} {'Mean':>8s} {'Std':>8s} {'Median':>8s}")
    print("-" * 50)
    print(f"{'Direct LLM':25s} {summary['direct_llm']['mean_score']:8.3f} "
          f"{summary['direct_llm']['std_score']:8.3f} "
          f"{summary['direct_llm']['median_score']:8.3f}")
    print(f"{'RAG-augmented':25s} {summary['rag_augmented']['mean_score']:8.3f} "
          f"{summary['rag_augmented']['std_score']:8.3f} "
          f"{summary['rag_augmented']['median_score']:8.3f}")
    print(f"\nImprovement: {summary['improvement']:+.3f} ({summary['improvement_pct']:+.1f}%)")
    print(f"Retrieval recall@3: {summary['retrieval']['mean_recall_at_3']:.3f}")

    print(f"\nBy domain:")
    for domain, dr in domain_results.items():
        print(f"  {domain:15s}: Direct={dr['direct_mean']:.3f}, "
              f"RAG={dr['rag_mean']:.3f}, "
              f"Delta={dr['improvement']:+.3f} (n={dr['n_questions']})")

    # Save results
    output = os.path.join(RESULTS_DIR, "rag_pipeline.json")
    with open(output, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults saved to {output}")

    return results


if __name__ == "__main__":
    run_rag_experiment()
