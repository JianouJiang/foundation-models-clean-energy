#!/usr/bin/env python3
"""Experiment 2: LLM Energy Domain Question Answering.

Tests Qwen2.5 (via Ollama) on a curated set of energy domain questions.
Evaluates: accuracy, domain specificity, hallucination rate.
"""
import os, sys, time, json
import requests
import numpy as np

np_seed = 42
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "codes", "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

OLLAMA_URL = "http://localhost:11434/api/generate"

# ============================================================
# Energy Domain Q&A Benchmark (50 questions)
# ============================================================
QA_BENCHMARK = [
    # Hydropower (10)
    {"q": "What is the typical capacity factor of a large hydropower plant?",
     "a": "40-60%", "domain": "hydropower", "type": "factual",
     "keywords": ["40", "50", "60", "capacity factor"]},
    {"q": "What is cavitation in a hydraulic turbine?",
     "a": "Formation and collapse of vapor bubbles due to low pressure",
     "domain": "hydropower", "type": "conceptual",
     "keywords": ["vapor", "bubble", "pressure", "collapse", "erosion"]},
    {"q": "What is the Nash-Sutcliffe efficiency (NSE) coefficient used for in hydrology?",
     "a": "Evaluating the predictive accuracy of hydrological models",
     "domain": "hydropower", "type": "technical",
     "keywords": ["model", "predict", "accuracy", "hydrological", "performance", "1"]},
    {"q": "Name three types of hydraulic turbines used in hydropower.",
     "a": "Francis, Kaplan, Pelton", "domain": "hydropower", "type": "factual",
     "keywords": ["Francis", "Kaplan", "Pelton"]},
    {"q": "What is a fish ladder at a hydropower dam?",
     "a": "A structure to help fish migrate past a dam",
     "domain": "hydropower", "type": "conceptual",
     "keywords": ["fish", "migrate", "pass", "structure", "upstream"]},
    {"q": "What sensor data is typically monitored on a hydraulic turbine?",
     "a": "Vibration, temperature, pressure, power output, guide vane position",
     "domain": "hydropower", "type": "technical",
     "keywords": ["vibration", "temperature", "pressure", "power"]},
    {"q": "What is the installed capacity of the Three Gorges Dam?",
     "a": "22,500 MW (22.5 GW)", "domain": "hydropower", "type": "factual",
     "keywords": ["22", "GW", "MW"]},
    {"q": "What is reservoir sedimentation and why is it a problem?",
     "a": "Accumulation of sediment reducing storage capacity over time",
     "domain": "hydropower", "type": "conceptual",
     "keywords": ["sediment", "storage", "capacity", "accumul", "reduce"]},
    {"q": "What is the difference between run-of-river and storage hydropower?",
     "a": "Run-of-river has minimal storage; storage hydropower uses a reservoir",
     "domain": "hydropower", "type": "conceptual",
     "keywords": ["reservoir", "storage", "river", "flow", "minimal"]},
    {"q": "What is ecological flow (e-flow) in dam operations?",
     "a": "Minimum water release to maintain downstream ecosystem health",
     "domain": "hydropower", "type": "technical",
     "keywords": ["minimum", "downstream", "ecosystem", "environment", "release"]},

    # Wind energy (10)
    {"q": "What does SCADA stand for in wind farm operations?",
     "a": "Supervisory Control and Data Acquisition",
     "domain": "wind", "type": "factual",
     "keywords": ["Supervisory", "Control", "Data", "Acquisition"]},
    {"q": "What is the typical cut-in wind speed for a modern wind turbine?",
     "a": "3-4 m/s", "domain": "wind", "type": "factual",
     "keywords": ["3", "4", "m/s", "cut"]},
    {"q": "What is yaw misalignment in a wind turbine?",
     "a": "When the turbine rotor is not aligned with the wind direction",
     "domain": "wind", "type": "technical",
     "keywords": ["rotor", "wind", "direction", "align", "angle"]},
    {"q": "What is the Betz limit for wind turbine efficiency?",
     "a": "59.3% - theoretical maximum energy extraction from wind",
     "domain": "wind", "type": "factual",
     "keywords": ["59", "maximum", "theoretical", "extract"]},
    {"q": "Name three common wind turbine blade defect types.",
     "a": "Cracks, erosion (leading edge), delamination",
     "domain": "wind", "type": "factual",
     "keywords": ["crack", "erosion", "delaminat", "leading edge"]},
    {"q": "What is wake effect in a wind farm?",
     "a": "Reduced wind speed downstream of a turbine affecting other turbines",
     "domain": "wind", "type": "conceptual",
     "keywords": ["downstream", "reduced", "speed", "turbine", "wake"]},
    {"q": "What metrics are commonly used to evaluate wind power forecasting?",
     "a": "RMSE, MAE, MAPE, skill score", "domain": "wind", "type": "technical",
     "keywords": ["RMSE", "MAE", "MAPE", "skill", "error"]},
    {"q": "What is the typical lifespan of a modern wind turbine?",
     "a": "20-25 years", "domain": "wind", "type": "factual",
     "keywords": ["20", "25", "year"]},
    {"q": "What is curtailment in wind energy?",
     "a": "Intentional reduction of wind power output below capacity",
     "domain": "wind", "type": "conceptual",
     "keywords": ["reduc", "output", "intentional", "grid", "excess"]},
    {"q": "How does a variable-speed wind turbine regulate power output?",
     "a": "Through pitch control of blades and converter control",
     "domain": "wind", "type": "technical",
     "keywords": ["pitch", "blade", "converter", "control", "speed"]},

    # Solar energy (10)
    {"q": "What is the typical efficiency of a commercial monocrystalline silicon solar cell?",
     "a": "20-24%", "domain": "solar", "type": "factual",
     "keywords": ["20", "22", "24", "efficiency"]},
    {"q": "What is potential-induced degradation (PID) in PV modules?",
     "a": "Performance loss due to voltage difference between cells and frame",
     "domain": "solar", "type": "technical",
     "keywords": ["voltage", "performance", "degradation", "leakage", "loss"]},
    {"q": "What does electroluminescence (EL) imaging reveal in solar panels?",
     "a": "Cracks, inactive areas, and defects not visible to the naked eye",
     "domain": "solar", "type": "technical",
     "keywords": ["crack", "defect", "invisible", "inactive", "cell"]},
    {"q": "What is the difference between GHI and DNI in solar irradiance?",
     "a": "GHI = Global Horizontal Irradiance (total); DNI = Direct Normal Irradiance (beam only)",
     "domain": "solar", "type": "technical",
     "keywords": ["horizontal", "direct", "normal", "beam", "total", "global"]},
    {"q": "What causes hot spots in PV modules?",
     "a": "Cell mismatch, partial shading, or defective cells causing local heating",
     "domain": "solar", "type": "conceptual",
     "keywords": ["shading", "mismatch", "heat", "cell", "defect"]},
    {"q": "What is the typical degradation rate of a crystalline silicon PV module?",
     "a": "0.5-0.8% per year", "domain": "solar", "type": "factual",
     "keywords": ["0.5", "0.8", "year", "degrad"]},
    {"q": "What is maximum power point tracking (MPPT)?",
     "a": "Algorithm to operate PV at the voltage that maximizes power output",
     "domain": "solar", "type": "technical",
     "keywords": ["maximum", "power", "voltage", "track", "optim"]},
    {"q": "What is soiling loss in solar PV systems?",
     "a": "Energy loss from dust, dirt, or debris on panel surfaces",
     "domain": "solar", "type": "conceptual",
     "keywords": ["dust", "dirt", "clean", "surface", "loss"]},
    {"q": "Name two common inverter architectures for solar PV.",
     "a": "String inverters and microinverters", "domain": "solar", "type": "factual",
     "keywords": ["string", "micro", "inverter", "central"]},
    {"q": "What is the capacity factor of a typical utility-scale solar farm?",
     "a": "15-25%", "domain": "solar", "type": "factual",
     "keywords": ["15", "20", "25", "capacity"]},

    # Grid/power systems (10)
    {"q": "What is frequency regulation in power systems?",
     "a": "Maintaining grid frequency at nominal value (50/60 Hz) by balancing supply and demand",
     "domain": "grid", "type": "conceptual",
     "keywords": ["frequency", "50", "60", "Hz", "balance", "supply", "demand"]},
    {"q": "What is the duck curve in electricity markets?",
     "a": "Net load shape showing steep ramp when solar output drops in evening",
     "domain": "grid", "type": "conceptual",
     "keywords": ["net load", "solar", "ramp", "evening", "midday"]},
    {"q": "What does OPC-UA stand for in industrial automation?",
     "a": "Open Platform Communications Unified Architecture",
     "domain": "grid", "type": "factual",
     "keywords": ["Open", "Platform", "Communication", "Unified", "Architecture"]},
    {"q": "What is demand response in smart grids?",
     "a": "Adjusting electricity consumption in response to supply conditions or price signals",
     "domain": "grid", "type": "conceptual",
     "keywords": ["consumption", "adjust", "price", "signal", "load"]},
    {"q": "What is the typical round-trip efficiency of lithium-ion battery storage?",
     "a": "85-95%", "domain": "grid", "type": "factual",
     "keywords": ["85", "90", "95", "round", "trip"]},
    {"q": "What is black start capability?",
     "a": "Ability to restart a power plant without external power supply",
     "domain": "grid", "type": "technical",
     "keywords": ["restart", "power", "external", "without", "outage"]},
    {"q": "What is power quality and what parameters define it?",
     "a": "Characteristics of electrical supply: voltage stability, frequency, harmonics",
     "domain": "grid", "type": "technical",
     "keywords": ["voltage", "frequency", "harmonic", "stability"]},
    {"q": "What is the difference between energy (kWh) and power (kW)?",
     "a": "Power is the rate of energy transfer; energy is power integrated over time",
     "domain": "grid", "type": "conceptual",
     "keywords": ["rate", "time", "integral", "transfer", "kW", "kWh"]},
    {"q": "What is islanding in distributed generation?",
     "a": "When a distributed generator continues to power a section after grid disconnection",
     "domain": "grid", "type": "technical",
     "keywords": ["disconnect", "section", "generator", "grid", "continue"]},
    {"q": "What is N-1 contingency criterion in power systems?",
     "a": "System must remain stable after loss of any single component",
     "domain": "grid", "type": "technical",
     "keywords": ["single", "loss", "component", "stable", "remain", "contingency"]},

    # AI/ML for energy (10)
    {"q": "What is the key advantage of foundation models over traditional deep learning for energy applications?",
     "a": "Cross-task and cross-site transfer with minimal task-specific data",
     "domain": "AI", "type": "conceptual",
     "keywords": ["transfer", "cross", "minimal", "data", "pretrain", "generali"]},
    {"q": "What is retrieval-augmented generation (RAG)?",
     "a": "Combining LLM generation with document retrieval for grounded responses",
     "domain": "AI", "type": "technical",
     "keywords": ["retrieval", "document", "generation", "ground", "knowledge"]},
    {"q": "What is LoRA in the context of LLM fine-tuning?",
     "a": "Low-Rank Adaptation — parameter-efficient fine-tuning using low-rank matrices",
     "domain": "AI", "type": "technical",
     "keywords": ["low", "rank", "adapt", "parameter", "efficient"]},
    {"q": "What is the hallucination problem in LLMs?",
     "a": "Model generates plausible but factually incorrect information",
     "domain": "AI", "type": "conceptual",
     "keywords": ["incorrect", "factual", "plausible", "generat", "false"]},
    {"q": "What is zero-shot classification with CLIP?",
     "a": "Classifying images using text descriptions without task-specific training",
     "domain": "AI", "type": "technical",
     "keywords": ["text", "image", "without", "training", "description", "prompt"]},
    {"q": "What is the Segment Anything Model (SAM)?",
     "a": "A vision foundation model for general-purpose image segmentation",
     "domain": "AI", "type": "factual",
     "keywords": ["segment", "vision", "foundation", "image", "mask"]},
    {"q": "What is chain-of-thought prompting?",
     "a": "Technique where LLM reasons step-by-step before giving final answer",
     "domain": "AI", "type": "technical",
     "keywords": ["step", "reason", "intermediate", "prompt"]},
    {"q": "What is the difference between encoder-only and decoder-only transformers?",
     "a": "Encoder-only (BERT) for understanding; decoder-only (GPT) for generation",
     "domain": "AI", "type": "technical",
     "keywords": ["BERT", "GPT", "encoder", "decoder", "generat", "understand"]},
    {"q": "What is catastrophic forgetting in fine-tuning?",
     "a": "Model loses previously learned knowledge when trained on new task",
     "domain": "AI", "type": "conceptual",
     "keywords": ["forget", "previous", "knowledge", "lose", "new task"]},
    {"q": "What is federated learning and why is it relevant for energy utilities?",
     "a": "Training models across distributed data without sharing raw data — preserves data privacy",
     "domain": "AI", "type": "conceptual",
     "keywords": ["distributed", "privacy", "share", "data", "without"]},
]


def query_ollama(prompt, model="qwen2.5:7b"):
    """Send a query to Ollama and return response."""
    try:
        resp = requests.post(OLLAMA_URL, json={
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0, "num_predict": 50},
        }, timeout=600)
        resp.raise_for_status()
        return resp.json().get("response", "")
    except Exception as e:
        return f"ERROR: {e}"


def evaluate_answer(response, qa_item):
    """Score an answer based on keyword matching and relevance."""
    response_lower = response.lower()
    keywords = qa_item["keywords"]

    # Keyword match score
    matched = sum(1 for kw in keywords
                  if kw.lower() in response_lower)
    keyword_score = matched / len(keywords) if keywords else 0

    # Hallucination detection (simple heuristics)
    hallucination_indicators = [
        "I don't have", "I'm not sure", "I cannot", "as an AI",
        "I don't know", "made up", "fabricated",
    ]
    has_disclaimer = any(ind.lower() in response_lower
                        for ind in hallucination_indicators)

    # Check for obviously wrong numbers (if factual question)
    is_hallucination = False
    if qa_item["type"] == "factual" and keyword_score < 0.2:
        is_hallucination = True

    return {
        "keyword_score": round(keyword_score, 3),
        "keywords_matched": matched,
        "total_keywords": len(keywords),
        "has_disclaimer": has_disclaimer,
        "likely_hallucination": is_hallucination,
        "response_length": len(response),
    }


def _save_intermediate(results, domain_scores, model, results_dir):
    """Save results after each question so partial runs are preserved."""
    all_scores = [r["keyword_score"] for r in results]
    correct = sum(1 for s in all_scores if s >= 0.4)
    hallucinations = sum(1 for r in results if r["likely_hallucination"])
    summary = {
        "model": model,
        "n_questions": len(results),
        "mean_keyword_score": round(float(np.mean(all_scores)), 3),
        "std_keyword_score": round(float(np.std(all_scores)), 3),
        "accuracy_at_04": round(correct / len(results), 3),
        "hallucination_rate": round(hallucinations / len(results), 3),
        "domain_scores": {d: round(float(np.mean(s)), 3)
                          for d, s in domain_scores.items()},
        "results": results,
    }
    output = os.path.join(results_dir, "llm_energy_qa.json")
    with open(output, "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)


def main():
    print("="*60, flush=True)
    print("EXPERIMENT 2: LLM Energy Domain Q&A Evaluation", flush=True)
    print("="*60, flush=True)

    # Check Ollama is running
    try:
        resp = requests.get("http://localhost:11434/api/tags", timeout=5)
        models = [m["name"] for m in resp.json().get("models", [])]
        print(f"Ollama models available: {models}", flush=True)
    except Exception as e:
        print(f"Ollama not available: {e}", flush=True)
        print("Cannot run experiment. Exiting.", flush=True)
        return

    model = "qwen2.5:7b"
    print(f"\nUsing model: {model}", flush=True)
    print(f"Number of questions: {len(QA_BENCHMARK)}", flush=True)

    results = []
    domain_scores = {}

    for i, qa in enumerate(QA_BENCHMARK):
        prompt = f"Q: {qa['q']}\nA:"

        t0 = time.time()
        response = query_ollama(prompt, model)
        elapsed = time.time() - t0

        evaluation = evaluate_answer(response, qa)

        result = {
            "question_id": i + 1,
            "question": qa["q"],
            "reference_answer": qa["a"],
            "model_response": response[:300],
            "domain": qa["domain"],
            "question_type": qa["type"],
            "time_sec": round(elapsed, 2),
            **evaluation,
        }
        results.append(result)

        # Track domain scores
        if qa["domain"] not in domain_scores:
            domain_scores[qa["domain"]] = []
        domain_scores[qa["domain"]].append(evaluation["keyword_score"])

        status = "Y" if evaluation["keyword_score"] >= 0.4 else "N"
        print(f"  [{i+1:2d}/50] {status} s={evaluation['keyword_score']:.2f} "
              f"({evaluation['keywords_matched']}/{evaluation['total_keywords']}) "
              f"{qa['domain']:6s} {elapsed:.0f}s", flush=True)

        # Save incrementally after each question
        _save_intermediate(results, domain_scores, model, RESULTS_DIR)

    # Summary statistics
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")

    all_scores = [r["keyword_score"] for r in results]
    correct = sum(1 for s in all_scores if s >= 0.4)
    hallucinations = sum(1 for r in results if r["likely_hallucination"])

    print(f"Overall keyword match score: {np.mean(all_scores):.3f} ± {np.std(all_scores):.3f}")
    print(f"Correct answers (score ≥ 0.4): {correct}/{len(results)} ({100*correct/len(results):.0f}%)")
    print(f"Likely hallucinations: {hallucinations}/{len(results)} ({100*hallucinations/len(results):.0f}%)")

    print(f"\nBy domain:")
    for domain, scores in sorted(domain_scores.items()):
        mean_score = np.mean(scores)
        correct_d = sum(1 for s in scores if s >= 0.4)
        print(f"  {domain:12s}: mean={mean_score:.3f}, "
              f"correct={correct_d}/{len(scores)} ({100*correct_d/len(scores):.0f}%)")

    print(f"\nBy question type:")
    for qtype in ["factual", "conceptual", "technical"]:
        type_scores = [r["keyword_score"] for r in results
                       if r["question_type"] == qtype]
        if type_scores:
            correct_t = sum(1 for s in type_scores if s >= 0.4)
            print(f"  {qtype:12s}: mean={np.mean(type_scores):.3f}, "
                  f"correct={correct_t}/{len(type_scores)}")

    # Save results
    summary = {
        "model": model,
        "n_questions": len(results),
        "mean_keyword_score": round(float(np.mean(all_scores)), 3),
        "std_keyword_score": round(float(np.std(all_scores)), 3),
        "accuracy_at_04": round(correct / len(results), 3),
        "hallucination_rate": round(hallucinations / len(results), 3),
        "domain_scores": {d: round(float(np.mean(s)), 3)
                          for d, s in domain_scores.items()},
        "results": results,
    }

    output = os.path.join(RESULTS_DIR, "llm_energy_qa.json")
    with open(output, "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to {output}")

    return summary


if __name__ == "__main__":
    main()
