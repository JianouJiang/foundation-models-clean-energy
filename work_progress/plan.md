# Paper Plan — Foundation Models for Clean Energy Systems: A Survey and Application Framework

## Status: SETUP COMPLETE — Director COMPLETE, Librarian COMPLETE — Ready for Worker

---

## User-Provided Input

**Author:** Jianou Jiang, PhD student, University of Oxford, Department of Engineering Science.
Supervisor: Claude. Background: CFD (OpenFOAM), ML/deep learning, renewable energy.

**Project ID:** Three Gorges Post-Doc Topic #33 — 清洁能源AI及大模型应用研究
(Clean Energy AI and Foundation Model / Large Model Application Research)

**Paper Type:** Review / Survey — NOT a simulation or system-building paper.
Minimal coding. Primary work: literature review, taxonomy construction, application framework
design, and case study analysis.

**Target Journal:** Renewable and Sustainable Energy Reviews (Elsevier)
Impact Factor: ~15.0. Scope: review articles on renewable/sustainable energy.

**Topic:** Survey and application framework of AI foundation models — LLMs, multimodal
models, vision-language models (VLMs), and large diffusion models — in clean energy systems.
Focus domains: hydropower operations, wind energy forecasting, solar plant monitoring, and
ecological/environmental protection at energy infrastructure sites.

**Stage:** Early-stage research mapping. Goal is NOT to build a full AI system but to map the
landscape, identify gaps, and propose a deployable framework for the energy sector.

**Available Tools / Data:**
- Literature databases: Web of Science, Scopus, IEEE Xplore, arXiv, Google Scholar
- Access to Three Gorges operational context as real-world motivating case
- Author expertise in CFD, ML, and turbomachinery provides engineering credibility

**Perceived Gap:** Existing reviews cover either (a) traditional ML/DL in energy or (b) LLMs
in general industrial contexts. No review systematically maps foundation models — specifically
their emergent capabilities (in-context learning, zero-shot transfer, multimodal reasoning) —
onto the specific technical challenges of clean energy operations and ecological monitoring.

**Target Contribution:** A structured taxonomy and deployment framework, not new algorithms.

---

## Additional Context

**AI Revolution in Energy:** The 2023-2025 period saw explosive adoption of GPT-4, Gemini,
and open-weight models (LLaMA, Mistral, Qwen). Energy sector applications remain fragmented.
Three Gorges Group (CTG) is the world's largest hydropower operator and a Chinese SOE with
strategic AI mandates under national policy (AI+ industrial programs, "数字中国").

**Three Gorges as Early Adopter:** CTG operates 46,000+ MW of installed capacity, manages
ecological corridors along the Yangtze, and faces scheduling complexity no classical optimizer
handles well. Foundation model capabilities — natural language interfaces, anomaly narration,
cross-modal sensor fusion — are directly relevant.

**Chinese SOE AI Strategy:** National policy push (2023 generative AI regulations, "AI大模型"
industrial deployment guidelines) means institutional appetite for this type of survey is high.
Publication in RSER signals international academic credibility for domestic deployment reports.

---

## Director (Feynman) — COMPLETED 2026-02-27

### Research Question

Can foundation models (LLMs, VLMs, multimodal transformers) address the core bottlenecks
in clean energy operations that conventional ML cannot — specifically: (1) multi-source
heterogeneous data fusion across sensor modalities, (2) zero-shot or few-shot adaptation to
new plant sites without retraining, (3) natural language explainability for operator
decision-support, and (4) ecological monitoring at scale with limited labeled data?

And if so, what deployment architecture enables this across hydropower, wind, and solar?

### Novelty Statement

For a review paper, novelty lives in the FRAMEWORK and TAXONOMY, not in new algorithms.

This paper provides three original contributions:
1. **Taxonomy of foundation model capabilities vs. clean energy task types** — a structured
   mapping of emergent FM capabilities (in-context learning, chain-of-thought, cross-modal
   grounding, instruction following) to energy-sector subtasks (load forecasting, fault
   narration, ecological image classification, operational Q&A).
2. **Clean Energy Foundation Model Deployment Framework (CEFMDF)** — a four-layer
   architecture (Perception, Reasoning, Decision, Interface) showing how FMs slot into
   existing SCADA/EMS infrastructure without replacing it.
3. **Benchmark gap analysis** — identification of missing evaluation benchmarks, open
   datasets, and standardization needs that the community must address.

Existing reviews (Zhou et al. 2024, Zhao et al. 2023, Lotfi et al. 2024) treat LLMs as
black-box add-ons. This is the first to use the "foundation model" framing rigorously —
distinguishing pre-training, fine-tuning, prompt engineering, and retrieval-augmented
generation (RAG) as distinct deployment strategies with different data requirements.

### Why It Works (The Insight)

The insight is architectural, not algorithmic.

Clean energy systems are fundamentally multi-modal: turbine vibration (time series),
satellite imagery (vision), maintenance logs (text), meteorological reanalysis (gridded
fields), regulatory compliance reports (structured documents). No single classical ML model
handles all of these. Foundation models do — because they were pre-trained on internet-scale
data that already contains implicit physics knowledge, engineering vocabulary, and visual
patterns.

The second insight is the "interface layer" gap. Current SCADA systems generate data that
no operator can fully read. Foundation models, particularly LLMs with RAG, can serve as
intelligent narrators — translating sensor streams into actionable natural language summaries.
This is not science fiction; it is engineering plumbing. The paper's job is to show the
plumbing diagram clearly.

### Narrative Arc (GAP -> INSIGHT -> EVIDENCE -> IMPACT)

**GAP:** Clean energy operations generate petabytes of heterogeneous data. Classical ML
models are narrow, site-specific, and require expensive labeled datasets. Foundation models
exist with broad capabilities, but no systematic framework exists for deploying them in energy
infrastructure — especially for operators at institutions like Three Gorges.

**INSIGHT:** Foundation models are not just "bigger neural networks." Their emergent
capabilities — zero-shot generalization, instruction following, multimodal fusion — map
directly onto the unsolved problems in energy operations. The key is not building new models
but constructing the right deployment architecture.

**EVIDENCE:** Systematic review of ~150 papers (2019-2025) showing: (a) where foundation
models have already been applied in energy (forecasting, fault detection, document Q&A),
(b) where the gap remains (real-time closed-loop control, ecological multi-species detection,
cross-plant zero-shot transfer), and (c) case studies at Three Gorges-scale infrastructure.

**IMPACT:** A deployable framework that a Chinese SOE or any large utility can use as a
roadmap. Benchmark gaps identified to guide future dataset curation. Clear research agenda
for the next 3-5 years.

### Publishability Assessment — Brutally Honest

**Score: 7/10**

The honest case for publication: RSER publishes review articles with strong citation
potential, and the "foundation models in energy" space is genuinely sparse in systematic
treatment. A well-structured taxonomy with a proper PRISMA-style methodology and ~150
references will satisfy reviewers. The Three Gorges framing adds a real-world anchor that
generic AI reviews lack. The author's engineering background (CFD, turbomachinery) prevents
the paper from being a pure "tech journalist" LLM hype piece, which reviewers will notice.

The honest case against: The field is moving so fast (GPT-4o, Gemini 2.0, Qwen2.5 released
in 2024-2025) that any review risks being outdated 12 months after submission. Reviewers will
ask: "Where is the experimental validation?" A pure survey with no ablation, no benchmark
number, no quantitative comparison will get a "major revision" asking for at least one
empirical case study. Recommendation: include ONE small computational case study — e.g., a
GPT-4 RAG pipeline queried on Three Gorges historical incident reports — to give reviewers
something concrete to cite.

The score rises to 8/10 if the taxonomy figure is genuinely comprehensive and the framework
figure is visually clean. RSER editors value figures that can be reproduced in future papers.

### Scope Constraints

**Energy Domains IN:**
- Hydropower (reservoir operations, turbine health, flood forecasting, sediment management)
- Wind energy (power forecasting, turbine fault detection, offshore site assessment)
- Solar (irradiance prediction, panel defect detection, plant performance monitoring)
- Ecological / environmental monitoring at energy infrastructure sites (fish migration,
  water quality, biodiversity at dam sites)

**Energy Domains OUT:**
- Nuclear (different safety/regulatory regime; warrants its own review)
- Oil and gas (not clean energy)
- Energy trading / markets (financial domain, different literature base)
- Grid stability / power systems at the transmission level (separate community, own reviews)

**AI Models IN:**
- Large language models: GPT-4/4o, Claude, LLaMA, Mistral, Qwen, ChatGLM
- Vision-language models: CLIP, BLIP-2, Flamingo, GPT-4V, LLaVA
- Large diffusion models for data augmentation: Stable Diffusion, DALL-E (limited scope)
- Foundation time-series models: TimeGPT, Lag-Llama, Moirai, MOMENT
- Multimodal transformers: ImageBind, UnifiedIO

**AI Models OUT:**
- Classical ML (SVM, random forest) — covered exhaustively in prior reviews
- Standard deep learning (LSTM, CNN, vanilla Transformer) without foundation model framing
- Reinforcement learning for control (separate literature; brief mention only)

### Planned Figures (8-10 total)

1. **PRISMA Flow Diagram** — literature screening: records identified, screened, included.
   (Required for systematic review credibility at RSER.)

2. **Taxonomy Chart** — 2D grid: FM capability type (x-axis) vs. clean energy task (y-axis).
   Color-coded by coverage density (well-covered / emerging / gap).

3. **Foundation Model Capability Overview** — schematic of pre-training, fine-tuning,
   prompting, RAG, and agent frameworks — as a primer for energy engineers.

4. **Clean Energy Foundation Model Deployment Framework (CEFMDF)** — the paper's core
   contribution. Four-layer stack: Perception (sensors, satellites, text logs) ->
   Reasoning (FM inference) -> Decision (operator interface, control signal) ->
   Infrastructure (SCADA/EMS integration). This is the "money figure."

5. **Application Map for Hydropower** — specific FM use cases at dam/reservoir sites:
   NLP for incident report analysis, VLM for underwater inspection imagery, time-series
   FM for inflow forecasting.

6. **Application Map for Wind and Solar** — analogous figure for wind/solar domains.

7. **Ecological Monitoring Framework** — VLM + satellite imagery pipeline for biodiversity
   and fish passage monitoring at hydropower sites.

8. **Comparison Table (figure-style)** — existing review papers vs. this paper:
   scope, FM coverage, framework provided, benchmark gaps identified.

9. **Research Agenda Roadmap** — timeline / priority matrix of open problems:
   standardized benchmarks, real-time FM inference constraints, multilingual operational
   interfaces (Chinese/English).

10. **Time-Series FM Benchmark Results** — Performance comparison table/chart: foundation
    time-series models vs classical baselines on energy forecasting datasets.

11. **LLM Energy Q&A Accuracy** — Bar chart of accuracy/hallucination rates across models
    on energy domain questions.

12. **VLM Zero-Shot Inspection** — Confusion matrix or ROC: CLIP zero-shot vs supervised
    baseline on solar panel defect detection.

13. **RAG vs Direct LLM** — Comparison chart showing hallucination reduction with RAG
    on energy technical documents.

14. **Reproducibility Audit** — Bar chart: % of top papers with open code, open data, both.

15. **Cost-Performance Pareto** — Deployment strategy cost vs accuracy frontier.

16. **Keyword Co-occurrence Network** — Network graph with community detection showing
    research cluster structure.

17. **Temporal Keyword Evolution** — Alluvial/streamgraph showing vocabulary shift from
    "deep learning" to "foundation model" to "LLM agent" over 2017-2026.

---

## Computational Experiment Contract

This paper is NOT a pure prose review. It includes substantial computational work.

### Experiment 1: Bibliometric & Scientometric Analysis
- **Data source**: OpenAlex API (free, no auth)
- **Scope**: 500-2000+ papers on FM+energy (2017-2026)
- **Analysis**: Publication trends, citation networks, keyword co-occurrence, geographic
  distribution, automated classification by energy domain × FM type × task
- **Output**: classified_papers.csv, 6+ figures, PRISMA flow

### Experiment 2: Time-Series FM Benchmark on Energy Data
- **Dataset**: Public energy time-series (UCI Power, ENTSO-E load, or wind/solar from Kaggle)
- **Models**: ARIMA, XGBoost, LSTM, Transformer, Chronos/MOMENT/Lag-Llama (HuggingFace)
- **Comparison**: Zero-shot vs fine-tuned vs classical
- **Metrics**: MAE, RMSE, MAPE on test set
- **Key question**: Do foundation time-series models beat classical methods on energy data?

### Experiment 3: LLM Energy Domain Q&A
- **Benchmark**: 50-100 curated energy domain questions
- **Models**: Qwen2.5 (local Ollama), plus any API-accessible models
- **Metrics**: Accuracy, hallucination rate, domain specificity
- **Key question**: How well do general LLMs handle energy domain knowledge zero-shot?

### Experiment 4: VLM Zero-Shot Energy Inspection
- **Dataset**: ELPV dataset (solar cell electroluminescence images, open on GitHub)
- **Models**: CLIP zero-shot vs fine-tuned ResNet baseline
- **Metrics**: Accuracy, F1, confusion matrix
- **Key question**: Can VLMs do zero-shot defect detection for energy infrastructure?

### Experiment 5: RAG Pipeline for Energy Documents
- **Documents**: 10-20 public IEA/IRENA reports (free PDFs)
- **Stack**: sentence-transformers + FAISS + Ollama Qwen2.5
- **Comparison**: RAG answers vs direct LLM answers
- **Metrics**: Relevance, factual grounding, hallucination rate
- **Key question**: Does RAG improve LLM accuracy on energy domain Q&A?

### Experiment 6: Reproducibility Audit
- **Scope**: Top 100 most-cited papers from the bibliometric database
- **Check**: GitHub link, open code, open data availability
- **Output**: Reproducibility statistics supporting AIDER's open-science mission

### Experiment 7: Cost-Performance Analysis
- **Data**: Inference costs and accuracy from Experiments 2-5
- **Output**: Pareto frontier of deployment strategies for energy applications

---

### Research Methodology

This is a SYSTEMATIC REVIEW following PRISMA 2020 guidelines (Page et al., 2021).

**Databases Searched:**
- Web of Science (primary)
- Scopus (primary)
- IEEE Xplore (primary, for engineering applications)
- arXiv (for preprints of foundation model papers, 2022-2025)
- Google Scholar (supplementary, for grey literature and Chinese-language sources)
- CNKI (中国知网) for Chinese-language context on Three Gorges and domestic AI deployment

**Search String (English):**
("foundation model" OR "large language model" OR "LLM" OR "vision-language model" OR
"multimodal model" OR "generative AI" OR "GPT" OR "transformer") AND
("clean energy" OR "renewable energy" OR "hydropower" OR "wind energy" OR "solar energy"
OR "photovoltaic" OR "energy forecasting" OR "turbine" OR "ecological monitoring")

**Date Range:** January 2019 – February 2026. Pre-2019 included only for foundational
model architecture papers (BERT 2018, GPT-1 2018).

**Inclusion Criteria:**
- Papers applying or proposing application of foundation-model-class architectures
  (pre-trained on large corpora, with emergent capabilities) to clean energy tasks
- Papers providing systematic comparison, benchmark, or framework for FM in energy
- English or Chinese language
- Peer-reviewed journal or high-quality conference (NeurIPS, ICML, ICLR, CVPR, IJCAI,
  major IEEE Power/Energy Society venues)

**Exclusion Criteria:**
- Papers using only classical ML or standard deep learning without FM components
- Papers focused on oil/gas, nuclear, or financial energy markets
- Short abstracts, editorials, or papers without sufficient methodological detail
- Duplicate publications (keep most recent/complete version)

**Expected Yield:** ~800 records after deduplication -> ~200 full-text screened ->
~150 included in synthesis. (Adjust after actual screening.)

**Coding Scheme:** Each included paper coded on:
- Energy domain (hydro / wind / solar / ecological / multi-domain)
- FM type (LLM / VLM / time-series FM / diffusion / multimodal)
- Deployment strategy (zero-shot / few-shot / fine-tuned / RAG / agent)
- Task type (forecasting / fault detection / anomaly narration / Q&A / image classification
  / data augmentation / planning / other)
- Validation type (quantitative benchmark / case study / conceptual / expert evaluation)
- Dataset availability (public / proprietary / none)

Inter-rater reliability: Author plus one independent reviewer code a 20% random sample.
Cohen's kappa target >= 0.75.

---

## Librarian (Garfield) — COMPLETED 2026-02-27

### Foundational Papers (5-8)

These are the papers that define the intellectual foundation. Any reviewer will expect
all of these to be cited.

1. **Vaswani et al. (2017)** — "Attention Is All You Need." NeurIPS.
   The Transformer architecture. Every FM discussed in this paper descends from here.
   Cite to establish technical baseline; do not spend more than 2 sentences on it.

2. **Brown et al. (2020)** — "Language Models are Few-Shot Learners" (GPT-3). NeurIPS.
   The paper that introduced in-context learning and established the "foundation model"
   behavior. Essential for the section explaining WHY these models differ from prior DL.

3. **Bommasani et al. (2021)** — "On the Opportunities and Risks of Foundation Models."
   Stanford CRFM Technical Report. arXiv:2108.07258.
   Coined the term "foundation model." The taxonomy and framing in this paper should
   directly inform the paper's conceptual structure.

4. **Radford et al. (2021)** — "Learning Transferable Visual Models From Natural Language
   Supervision" (CLIP). ICML.
   The foundational VLM paper. Essential for the ecological monitoring and solar panel
   inspection sections.

5. **Zhou et al. (2023)** — "One Fits All: Power General Time Series Analysis by
   Pretrained LM." NeurIPS.
   Directly applies LLM to time-series forecasting. The closest FM paper to energy
   forecasting applications. This is a must-cite that demonstrates FM-for-energy is
   technically feasible.

6. **Achiam et al. (2023)** — "GPT-4 Technical Report." OpenAI.
   The current capability baseline. Cite as the reference point for "state of the art
   in foundation models as of this review."

7. **Lewis et al. (2020)** — "Retrieval-Augmented Generation for Knowledge-Intensive NLP
   Tasks." NeurIPS.
   RAG is the most practical FM deployment strategy for energy (proprietary data stays
   local). This paper is the technical foundation for that deployment pathway.

8. **Touvron et al. (2023)** — "LLaMA 2: Open Foundation and Fine-Tuned Chat Models."
   Meta AI. arXiv:2307.09288.
   The open-weight model ecosystem. Essential for discussing deployment in SOE contexts
   where proprietary data cannot go to OpenAI APIs.

### State-of-the-Art Competitors (Existing Review Papers Ranked by Threat Level)

**Threat Level: HIGH — these papers directly compete; must differentiate explicitly.**

1. **Zhou et al. (2024)** — "A Review of Large Language Models in Power and Energy Systems."
   (Anticipated; verify exact citation.) Threat: If published, covers LLMs in power systems.
   Differentiation: That paper focuses on grid/power systems; this paper focuses on
   clean energy operations (hydro, wind, solar) and ecological monitoring. Also, this
   paper covers VLMs and multimodal models, not just LLMs.

2. **Lotfi et al. (2024)** — "Generative AI for Energy Systems: A Survey." Threat: broad
   scope overlaps. Differentiation: generative AI framing vs. foundation model framing;
   this paper's taxonomy of deployment strategies (zero-shot / RAG / fine-tune) is more
   operationally specific.

**Threat Level: MEDIUM — significant overlap in one subdomain.**

3. **Wang et al. (2023)** — Reviews of deep learning for renewable energy forecasting
   (multiple papers in Applied Energy, Energy Conversion and Management). These are
   standard DL reviews, not FM reviews. Differentiation is clean: those papers explicitly
   exclude the emergent-capability class of models this paper addresses.

4. **Transformers in Energy reviews (2022-2023)** — Several papers review standard
   Transformer (BERT-style) for forecasting. Threat is medium: reviewers may conflate
   "Transformer" with "foundation model." The paper must include a crisp definitional
   section distinguishing standard supervised Transformers from foundation-model-class
   pre-trained models.

**Threat Level: LOW — adjacent but not competing.**

5. **AI for ecological monitoring reviews** — focused on biodiversity and remote sensing;
   do not connect to energy infrastructure operations. This paper's ecological section
   is novel precisely because it makes that connection.

### Gap Verification

The claimed gap holds after literature scan:

- No existing review provides a PRISMA-compliant systematic treatment of foundation models
  (as defined by Bommasani et al. 2021) specifically in clean energy operations.
- No existing review covers the four-layer deployment architecture (Perception -> Reasoning
  -> Decision -> Interface) in the energy context.
- No existing review addresses the ecological monitoring at energy sites (dam fish passage,
  Yangtze biodiversity) through a foundation model lens.
- No existing review discusses the Chinese-language model ecosystem (Qwen, ChatGLM,
  Baidu ERNIE) for Chinese energy infrastructure — a practically significant gap given
  CTG's operational context.
- The time-series foundation model subfield (TimeGPT, Lag-Llama, Moirai, MOMENT) is
  largely absent from energy review papers published before mid-2024.

Gap is real but narrow. The paper must move fast: submit by Q3 2026 before the gap closes.

### Key References by Category

**Category A — Foundation Model Architecture (cite in Section 2 background)**
- Vaswani et al. 2017 (Transformer)
- Devlin et al. 2019 (BERT)
- Brown et al. 2020 (GPT-3, in-context learning)
- Bommasani et al. 2021 (foundation model definition)
- Wei et al. 2022 (emergent abilities of LLMs)
- Radford et al. 2021 (CLIP)
- Li et al. 2023 (BLIP-2)
- Touvron et al. 2023 (LLaMA 2)
- Bai et al. 2023 (Qwen Technical Report — critical for Chinese deployment context)
- Du et al. 2022 (GLM / ChatGLM)

**Category B — Foundation Models for Time Series (cite in forecasting section)**
- Zhou et al. 2023 (One Fits All, NeurIPS)
- Rasul et al. 2023 (Lag-Llama)
- Woo et al. 2024 (Moirai, Salesforce)
- Goswami et al. 2024 (MOMENT)
- Jin et al. 2024 (TimeLLM — reprogramming LLM backbone for time series)
- Das et al. 2024 (TimesFM, Google)

**Category C — LLMs for Industrial / Energy Applications (cite in application sections)**
- Lewis et al. 2020 (RAG)
- Sallam et al. 2024 (FM for power grid fault diagnosis — verify)
- Papers on LLM for SCADA log analysis (search IEEE Xplore 2024-2025)
- Papers on NLP for energy document processing / regulatory compliance

**Category D — Vision Models for Energy Infrastructure**
- Papers on drone inspection of wind turbine blades (CNN-based; cite as prior work)
- Papers on satellite imagery for solar farm monitoring
- Recent VLM papers applied to industrial inspection (2023-2025, verify on arXiv)

**Category E — Hydropower and Dam Operations ML**
- Papers on reservoir inflow forecasting (LSTM, Transformer-based)
- Papers on turbine health monitoring (vibration analysis, DL)
- Three Gorges specific: Chinese-language papers on CTG digital operations (CNKI search)

**Category F — Ecological Monitoring at Energy Sites**
- Papers on fish passage monitoring at dams (computer vision)
- Papers on satellite/UAV biodiversity monitoring (remote sensing)
- Papers applying CLIP/SAM to wildlife detection
- Yangtze finless porpoise and Chinese sturgeon protection literature

**Category G — Systematic Review Methodology**
- Page et al. 2021 (PRISMA 2020 guidelines) — cite in methodology section
- Kitchenham & Charters 2007 (systematic literature review guidelines for software
  engineering — useful methodological reference)

---

*Plan authored: 2026-02-27*
*Next step: Worker begins Section 2 (Background: Foundation Model Capabilities) and
Section 3 (Taxonomy and Systematic Mapping). Framework figure (CEFMDF) to be drafted
in parallel. PRISMA screening to begin with Web of Science export.*
