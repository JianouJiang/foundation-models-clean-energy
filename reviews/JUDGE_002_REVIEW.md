# JUDGE REVIEW 002 -- Foundation Models for Clean Energy Systems

**Reviewer:** Judge (Munger)
**Date:** 2026-03-06
**Manuscript:** `manuscript/main.tex` (913 lines, 45 pages, 35 content + 10 references/appendix)
**References:** `manuscript/references.bib` (94 entries)
**Review type:** Second review -- incremental evaluation of revisions since JUDGE_001

---

## EXECUTIVE SUMMARY

The paper has improved substantially since JUDGE_001 (4/10). All seven CRITICAL and HIGH items from the first review have been addressed: the PRISMA methodology was reframed as PRISMA-ScR with 31 verifiable included studies, references expanded from 58 to 94 entries, five benchmark experiments with real models on real data were added, a bibliometric analysis of 3,645 papers from OpenAlex provides quantitative backbone, and the BERT author error was fixed. The 83-page manuscript was condensed to 35 content pages. These are significant, substantive improvements.

However, this review identifies three NEW issues that were not present (or not detectable) in the first draft: (1) a code integration bug that produces an **incorrect Pareto frontier figure**, (2) **inconsistent metrics** between the LLM Q&A and RAG experiments that inflate the claimed RAG improvement, and (3) **unverifiable application study references** that lack DOIs or arXiv IDs. The paper's core claims remain sound, but these issues must be fixed before submission.

---

## JUDGE_001 RESOLUTION AUDIT

| # | Issue (JUDGE_001) | Status | Evidence |
|---|-------------------|--------|----------|
| C1 | Fabricated PRISMA numbers / reframe | **RESOLVED** | Reframed as PRISMA-ScR scoping review; 31 included studies explicitly stated; PRISMA flow with approximate counts |
| C2 | 99-reference deficit | **RESOLVED** | 94 bib entries (31 application studies + 63 background/methodology) |
| C3 | BERT author error | **RESOLVED** | Fixed in Session 2 |
| H1 | Risk of bias assessment | **RESOLVED** | Section 2.5: Level A/B/C scheme (20/8/3 distribution) |
| H2 | Heatmap arithmetic | **RESOLVED** | Table 3 based on 31 studies with explicit criteria; Table `tab:study_distribution` sums to 31 |
| H3 | Missing figures | **RESOLVED** | 11 data-driven figures + 2 TikZ diagrams |
| H4 | Empirical case study | **RESOLVED** | 5 benchmark experiments (Section 10) |
| H5 | Uncited quantitative claims | **RESOLVED** | Table `tab:performance_metrics` with 11 Level A studies |
| M1 | Strengthen research agenda | **RESOLVED** | Section 10.3: near/medium/long-term with EnergyBench, EU AI Act, federated learning |
| M2 | PRISMA checklist | **RESOLVED** | Appendix A: 20-item PRISMA-ScR checklist table |
| M3 | PatchTST FM definition | **RESOLVED** | Line 99: explicit distinction when pre-trained vs from scratch |
| M4 | Incomplete bib entries | **PARTIALLY** | Many entries improved; some still lack DOIs (see new issue below) |
| M5 | Inter-rater identity | **RESOLVED** | Line 111: BR verified 8/31 studies (26%), 88% raw agreement |

**Verdict:** 12/12 CRITICAL and HIGH items resolved. 4/5 MEDIUM items resolved. Strong response.

---

## FOUR PILLARS EVALUATION

### 1. NOVELTY (20%) -- Score: 6/10

**Genuine novelty:**
- The CEFMDF four-layer framework (Section 6) is the paper's strongest original contribution. No competing review provides a deployment architecture at this level of specificity.
- Five benchmark experiments with real models on real data -- no competing review (Zhou et al. 2024, Lotfi et al. 2024) includes original experimental results. This is a clear differentiator.
- The bibliometric analysis of 3,645 papers from OpenAlex with automated classification, exponential growth characterisation (doubling time 1.3 years, R^2=0.95), and reproducibility audit provides quantitative grounding absent from competitor surveys.
- The ecological monitoring angle (Section 9) connecting VLMs/SAM to energy infrastructure environmental compliance remains novel.
- Sensitivity analysis on maturity matrix (Section 5.2, line 393) is a methodological improvement rare in survey papers.

**Novelty limitations:**
- The maturity matrix (Table 3) is a standard survey construct. The contribution is the data-driven assessment, not the format.
- The research agenda (Section 10.3) is improved but still contains generic items ("develop benchmarks," "physics-informed fine-tuning") alongside the more specific ones.
- Benchmark experiments are small-scale demonstrations, not comprehensive evaluations. One household power dataset, 300 solar images, 50 Q&A questions, and 15 RAG questions are sufficient for a survey paper's case studies but do not constitute independent research contributions by themselves.

### 2. PHYSICS / SCIENCE DEPTH (40%) -- Score: 5/10

**What is working well:**

The PRISMA-ScR methodology is now properly executed. The 31 included studies are explicitly stated, the screening process has approximate counts at each stage (427 -> 289 -> 91 -> 31), eligibility criteria are clear, and the Level A/B/C risk-of-bias scheme is well-defined. The inter-rater agreement (88% on 8/31 studies) is honestly reported with limitations acknowledged (line 111). The comparison table (Table 7) self-identifies bias. This is honest, transparent methodology.

The domain sections (Sections 7-9) now include specific quantitative claims backed by citations and validation levels. Table 5 (`tab:performance_metrics`) with 11 Level A studies provides concrete evidence. The pattern identified -- "FMs achieve 80-95% of supervised baselines with zero labelled data" -- is supported by the evidence and represents a genuine synthesis contribution.

**CRITICAL ISSUE: Cost-Performance Figure Uses Wrong Baseline (Integration Bug)**

The Pareto frontier figure (Fig. 11, `fig_pareto_frontier.pdf`) contains an incorrect data point due to a code integration bug in `codes/analysis/cost_performance.py`:

- **Bug location:** `cost_performance.py` lines 197-217
- **Root cause:** Line 198 reads `qa.get("summary", {})`, but `llm_energy_qa.json` stores results at the **top level** (no "summary" key). The correct field is `accuracy_at_04` = 0.74 (line 6 of the JSON).
- **Fallback behaviour:** Lines 214-217 detect the zero-performance fallback and fill from the RAG experiment's `direct_llm.mean_score` = 0.26 instead.
- **Result in `cost_performance.json`:** The "Zero-shot FM / Domain Q&A / Qwen2.5-7B" entry has `performance: 0.26` (line 78), when it should be `0.74` (accuracy) or `0.519` (mean keyword score).

**Impact:** The Pareto frontier figure shows the zero-shot LLM as performing at 0.26 instead of 0.74. This:
1. Makes RAG appear to improve performance by +136.7% (from 0.26 to 0.616), when the actual comparison should account for the different metrics and question sets.
2. Makes zero-shot LLMs appear much worse than they actually performed.
3. The `perf_metric` field says "Accuracy" but the stored value (0.26) is actually a keyword match score from a different experiment.

**This is not data fabrication** -- it is a software bug with cascading effects. But the published figure is incorrect and must be regenerated.

**HIGH ISSUE: Metric Inconsistency Between LLM Q&A and RAG Experiments**

The paper conflates two experiments that use different question sets and different evaluation protocols:

- **Experiment 2 (LLM Q&A):** 50 questions, keyword match scoring, accuracy threshold at 0.4. Result: mean score 0.519, accuracy 74%.
- **Experiment 4 (RAG):** 15 questions (different set), keyword match + hallucination heuristics. Direct LLM result: 0.26 mean score. RAG result: 0.616 mean score.

The paper states (line 698): "RAG improved performance in every domain except wind (Figure fig_llm_qa b), with average improvement of +136.7% (Experiment 4)." This sentence appears in the Experiment 2 section but references Experiment 4's results. The reader may infer that RAG improved the 50-question benchmark by 136.7%, when in fact:
- The 136.7% improvement is on a **different** set of 15 questions.
- The direct LLM scored 0.26 on these 15 questions but 0.519 on the 50 questions -- suggesting these 15 questions may be systematically harder or differently scored.
- Within the RAG experiment, the comparison (0.26 -> 0.616) is internally valid, but it is misleading to present this improvement in the same breath as the 50-question Q&A results.

**Fix required:** Either (a) run RAG on all 50 Q&A questions for a direct comparison, (b) run the direct LLM on the 15 RAG questions using the same scoring protocol for a controlled comparison, or (c) clearly separate the two experiments in the text and avoid cross-referencing their metrics.

**HIGH ISSUE: Application Study References Lack Verifiable Identifiers**

Of the 94 bib entries, approximately 20-25 entries for 2024-2025 application studies (the core cited studies for Sections 7-9 and Table 5) lack DOIs or arXiv eprint fields. Examples:

- `xu2024tsfm_streamflow` -- no DOI, no arXiv ID
- `li2024moirai_reservoir_inflow` -- no DOI, no arXiv ID
- `xiao2024tsfm_wind_power` -- no DOI, no arXiv ID
- `wang2024vlm_blade_defect` -- no DOI, no arXiv ID
- `reddy2024sam_blade_segmentation` -- no DOI, no arXiv ID
- `huang2024clip_pv_defect` -- no DOI, no arXiv ID
- `zhang2024sam_fish_monitoring` -- no DOI, no arXiv ID
- `liu2024clip_bird_wind` -- no DOI, no arXiv ID

These are the studies that populate Table 5 (`tab:performance_metrics`) -- the paper's core evidence table. A reviewer who cannot verify these references through DOI lookup will question their existence. For a paper that conducts a reproducibility audit criticising the field's openness, having unverifiable core references is deeply ironic and potentially damaging.

**Fix required:** Add DOIs or arXiv eprint fields to ALL application study references. If a study genuinely lacks a DOI (e.g., conference paper under review), note the venue and status explicitly.

### 3. CONTRIBUTION (30%) -- Score: 5/10

**Strong contributions:**
- Five benchmark experiments with real models on real data is the strongest differentiator from competing reviews. The timeseries benchmark (Chronos zero-shot beats ARIMA, XGBoost, LSTM on UCI data) is a clean, reproducible result.
- The VLM experiment (CLIP on ELPV dataset, 300 images, three prompt strategies) is methodologically sound and provides a useful finding: zero-shot VLMs can screen but not replace supervised inspection.
- The bibliometric analysis (3,645 classified papers, exponential growth, geographic distribution, reproducibility audit) provides genuine quantitative contribution.
- The CEFMDF framework with explicit design principles (integration not replacement, data sovereignty, graceful degradation, modular composition) is practically valuable.

**Contribution weaknesses:**
- The Pareto frontier (the "synthesis" contribution that ties all experiments together) is undermined by the integration bug. Once fixed, the cross-experiment synthesis could be a genuine contribution -- but right now the figure is wrong.
- The LLM Q&A benchmark (50 questions) uses Qwen2.5-7B only. Testing a single model on 50 questions is a demonstration, not a benchmark. Even one additional model (e.g., Qwen2.5-3B for a size comparison, or any other accessible model) would strengthen the claim.
- The comparison table (Table 7) is self-assessment, which the paper acknowledges but which still weakens the claim of superiority over Zhou et al. 2024 and Lotfi et al. 2024.

### 4. RELEVANCY (10%) -- Score: 9/10

Excellent fit for the target journal. Foundation models in clean energy is timely. The computational components (bibliometrics, benchmarks) differentiate from purely narrative reviews. No issues.

---

## ANTI-SHORTCUT ENFORCEMENT

### Data Integrity Audit

All five benchmark experiments use real data from real models:

| Experiment | Data Source | Real? | Evidence |
|-----------|------------|-------|----------|
| Time-series | UCI Household Power Consumption | Yes | Downloaded from UCI repository, 34,168 hourly records |
| LLM Q&A | 50 curated questions | Yes | Domain-specific, non-trivial, with reference answers |
| VLM Inspection | ELPV dataset (2,624 EL images) | Yes | Cloned from GitHub, 300 images evaluated |
| RAG Pipeline | 24 curated passages + FAISS | Yes | Real passages with domain citations |
| Reproducibility | OpenAlex API (3,645 papers) | Yes | Real bibliometric metadata |

| Model | Inference | Real? | Evidence |
|-------|----------|-------|----------|
| Chronos-T5-Small | Zero-shot prediction | Yes | amazon/chronos-t5-small from HuggingFace |
| CLIP ViT-B-32 | Zero-shot classification | Yes | open_clip, laion2b_s34b_b79k pretrained |
| Qwen2.5-7B | Local Ollama inference | Yes | ~300s/question response times (realistic for 7B model) |
| ARIMA/XGBoost/LSTM | Trained baselines | Yes | Standard implementations, documented parameters |

**Verdict: No fabricated data. No simulation shortcuts.** All data sources are external, verifiable, and correctly attributed. Model inference times are consistent with real runs (not instant/suspicious). The individual experiments are scientifically sound.

### Red Flags

| # | Flag | Severity | Location |
|---|------|----------|----------|
| 1 | Pareto figure uses wrong LLM baseline (0.26 instead of 0.74) | **CRITICAL** | `cost_performance.py:198-217`, `cost_performance.json:78` |
| 2 | RAG vs LLM Q&A use different question sets + scoring | **HIGH** | `rag_pipeline.py` (15 Qs) vs `llm_energy_qa.py` (50 Qs) |
| 3 | ~20 application study references lack DOIs/arXiv IDs | **HIGH** | `references.bib` (2024-2025 entries) |
| 4 | Single LLM tested (Qwen2.5-7B only) | **MEDIUM** | `codes/models/llm_energy_qa.py` |
| 5 | `perf_metric` field mislabeled in cost_performance.json | **MEDIUM** | Line 79: says "Accuracy", value is keyword match score |

---

## ACTIONABLE ITEMS

### CRITICAL (must fix before next review)

**C1. Fix the cost_performance.py integration bug and regenerate figures.**

`cost_performance.py` line 198: `qa.get("summary", {})` returns empty dict because `llm_energy_qa.json` has no `"summary"` key. Change to:
```python
# Option A: Read directly from top-level
s["performance"] = qa.get("accuracy_at_04", 0)  # or qa.get("mean_keyword_score", 0)
```
Then regenerate `cost_performance.json`, `fig_pareto_frontier.pdf`, and `fig_deployment_comparison.pdf`. The choice of metric (accuracy at 0.4 threshold = 0.74 vs mean keyword score = 0.519) should be consistent with the RAG experiment's metric (mean keyword score) for fair comparison. If using accuracy, compute accuracy at the same threshold for the RAG experiment.

### HIGH (fix before submission)

**H1. Resolve the RAG vs LLM Q&A metric inconsistency.**

The 136.7% RAG improvement claim (line 743) compares metrics from two different experiments with different question sets and different scoring. Either:
- (a) Run RAG augmentation on the same 50 questions from Experiment 2 (preferred -- eliminates confound),
- (b) Run Qwen2.5-7B direct on the 15 RAG questions using identical scoring to establish a controlled baseline, or
- (c) At minimum, revise the text in Section 10.2 (line 698) to clearly state that the 136.7% improvement is from Experiment 4's 15-question subset, not from Experiment 2's 50-question benchmark. Remove the cross-reference between experiments.

**H2. Add DOIs or arXiv IDs to all application study references.**

Every reference cited in Table 5 (`tab:performance_metrics`) must have a verifiable identifier. The following entries need DOI or arXiv eprint fields:
- `xu2024tsfm_streamflow`, `li2024moirai_reservoir_inflow`, `xiao2024tsfm_wind_power`
- `deng2024gpt_wind_forecast`, `wang2024vlm_blade_defect`, `reddy2024sam_blade_segmentation`
- `huang2024clip_pv_defect`, `lee2024tsfm_solar_forecast`, `park2024sam_solar_panel`
- `liu2024clip_bird_wind`, `zhang2024sam_fish_monitoring`
- Plus any others among the 31 application studies lacking identifiers.

If a reference genuinely cannot be verified via DOI/arXiv (e.g., it does not exist as a published paper), remove it and adjust the affected table/text accordingly. Reference integrity is non-negotiable.

### MEDIUM (improve quality)

**M1. Test at least one additional LLM for the Q&A benchmark.**

A single-model Q&A benchmark is a demonstration, not a benchmark. Adding even Qwen2.5-3B (already on Ollama, presumably) would show the effect of model scale. Adding a different model family (e.g., LLaMA-3-8B if available) would strengthen the claim about general LLM energy knowledge.

**M2. Harmonise performance metrics across the Pareto analysis.**

The Pareto frontier currently mixes three different metrics: `1 - nMAE` for time series, `F1` for vision, and `Accuracy/keyword score` for NLP. While normalisation is necessary for cross-experiment comparison, the paper should explicitly acknowledge this in the Pareto figure caption or text (Section 10.6). State: "Performance values are normalised within each task category and are not directly comparable across categories."

**M3. Strengthen the LLM Q&A evaluation methodology.**

The keyword match scoring (line 698: "mean keyword match score 0.519") is a coarse heuristic. The paper should acknowledge this limitation explicitly. State something like: "The keyword-based scoring provides a lower bound on answer quality; semantic evaluation (e.g., via a judge LLM) would capture partial credit for paraphrased correct answers."

---

## WHAT IS WORKING WELL

1. **Massive improvement since JUDGE_001.** The paper went from "well-structured shell with fabricated PRISMA numbers" to "substantive computational survey with real data." All 12 CRITICAL/HIGH items from the first review are resolved.

2. **The timeseries benchmark is excellent.** Chronos zero-shot beating all trained baselines (MAE 0.483 vs ARIMA 0.717, XGBoost 0.540, LSTM 0.647) is a clean, reproducible, and genuinely interesting result. The 7-day prediction trace (Fig. 8) visually confirms the claim.

3. **The VLM experiment is well-designed.** Three prompt strategies (generic, domain, ensemble) reveal that prompt engineering critically affects zero-shot VLM performance -- the domain-specific prompt achieves perfect recall by trivially classifying everything as defective (F1=0.667 vs generic F1=0.606 vs supervised F1=0.755). This is a useful finding for practitioners.

4. **The bibliometric analysis provides real quantitative backbone.** The exponential growth characterisation (doubling time 1.3 years, R^2=0.95), geographic distribution, and reproducibility audit (5.5% code mention, 0% on Papers With Code) are genuine, data-driven contributions.

5. **Writing quality remains strong.** The condensation from 83 to 45 pages preserved clarity while removing redundancy. The technical primer (Section 4) is useful for the target audience. Domain sections are concise and well-cited.

6. **Figure quality has improved.** The shift from PNG to PDF vector figures, Type 3 font elimination, and redesign of bar charts to Cleveland dot plots and slopegraphs follows Tufte principles and improves journal readiness.

7. **Methodological transparency is commendable.** The paper acknowledges limitations throughout: self-assessment bias in the comparison table (Section 11), the small inter-rater sample (line 111), the arXiv temporal bias (line 88), and the absence of CNKI (line 90). This is the mark of honest scholarship.

---

## SCORE

| Pillar | Weight | Score | Weighted |
|--------|--------|-------|----------|
| Novelty | 20% | 6/10 | 1.2 |
| Physics/Science Depth | 40% | 5/10 | 2.0 |
| Contribution | 30% | 5/10 | 1.5 |
| Relevancy | 10% | 9/10 | 0.9 |
| **Total** | | | **5.6** |

**Score: 5/10**

The score rises from 4/10 (JUDGE_001) to 5/10, reflecting substantial progress. The PRISMA-ScR reframing, five benchmark experiments, and bibliometric analysis transform this from a "shell with invented numbers" to a "computationally-grounded survey with fixable issues." The score does not reach 6/10 because: (1) the Pareto figure is factually wrong due to a code bug, (2) the RAG improvement claim is inflated by experimental design, and (3) core application study references remain unverifiable. All three issues are fixable.

**Path to 6/10:** Fix C1 (Pareto figure bug), fix H1 (RAG metric separation), fix H2 (add DOIs to application studies).

**Path to 7/10:** All of the above, plus M1 (second LLM model), plus demonstrating that the 31 application study references are all verifiable published papers.

---

*"The first rule of compounding is to never interrupt it unnecessarily. This paper has compounded well from a 4 to a 5 -- real experiments, real data, real methods. But a Pareto frontier figure that shows the wrong number is like a financial statement with a misplaced decimal: it makes the reader distrust everything else, even the parts that are correct. Fix the decimal." -- Munger's compounding principle applied to this paper.*

---

## ADDENDUM: POST-FIX REASSESSMENT (2026-03-06, same session)

The Worker applied fixes during this review session. Updated assessment below.

### Resolution Status of JUDGE_002 Items

| # | Item | Status | Evidence |
|---|------|--------|----------|
| C1 | Pareto figure wrong baseline | **RESOLVED** | `cost_performance.json:78` now shows `performance: 0.519` (mean keyword score). Figure regenerated; zero-shot LLM correctly plotted at ~0.52. |
| H1 | RAG metric inconsistency | **PARTIALLY RESOLVED** | Line 745: properly separates experiments, reports timeout confound, gives controlled +64.9%. Conclusion (line 849) uses +64.9%. **BUT line 755 still says "+136.7%"** in the synthesis subsection -- internal inconsistency with line 745 and line 849. |
| H2 | Application study DOIs | **NOT RESOLVED** | All 11 flagged references still lack DOI/eprint fields (verified via grep). |
| M1 | Second LLM model | **RESOLVED** | Qwen2.5-3B results added (`llm_energy_qa_3b.json`, 50 questions, mean score 0.515, accuracy 70%). Statistical comparison in text: Wilcoxon p=0.89, Cohen's d=0.016. Pareto figure includes both models. |
| M2 | Metric disclaimer | **RESOLVED** | Line 755: "Because performance metrics differ across task categories...cross-category comparisons are approximate." Figure caption echoes this. |
| M3 | Keyword scoring limitation | **RESOLVED** | Line 698: "the keyword-based heuristic is conservative and may miss factual errors (e.g., the 7B model incorrectly attributed SAM to Adobe rather than Meta AI)." |

### New Observations

**Positive findings from the fixes:**

1. The Qwen2.5-3B vs 7B comparison (0.515 vs 0.519, p=0.89) is a genuinely useful finding: energy domain knowledge persists at 3B scale for this question set. This has practical implications for edge deployment at energy sites. Well executed.

2. The RAG section (line 745) now properly handles the timeout confound: "7/15 direct-LLM and 3/15 RAG queries timed out (300s limit), confounding the raw comparison (0.616 vs. 0.260, +136.7%). Restricting to the 8 questions where both conditions produced responses, RAG outperformed direct LLM: 0.804 vs. 0.488 (+64.9%)." This is honest, transparent reporting. The controlled comparison on paired non-timeout questions is the correct number to cite.

3. The `perf_metric` field in `cost_performance.json` still says "Accuracy" for the NLP entries (lines 79, 91, 103) when the actual metric is keyword match score. Minor labelling issue.

**Remaining items requiring action (updated 2026-03-06, second pass):**

1. ~~**Line 755 inconsistency (HIGH):**~~ **RESOLVED.** Line 755 now reads "+64.9% on paired non-timeout questions", consistent with lines 745 and 849.

2. **Reference DOIs (HIGH -- SOLE REMAINING BLOCKER):** Still unresolved. All 11 flagged application study references in Table 5 remain without DOI or arXiv eprint fields. Verified: `deng2024gpt_wind_forecast`, `xiao2024tsfm_wind_power`, `wang2024vlm_blade_defect`, `reddy2024sam_blade_segmentation`, `lee2024tsfm_solar_forecast`, `park2024sam_solar_panel`, `huang2024clip_pv_defect`, `xu2024tsfm_streamflow`, `li2024moirai_reservoir_inflow`, `zhang2024sam_fish_monitoring`, `liu2024clip_bird_wind`. This is the single largest remaining vulnerability.

3. ~~**perf_metric label (LOW):**~~ **RESOLVED.** `cost_performance.json` now correctly labels NLP entries as "Keyword score".

### Updated Score (Second Pass)

| Pillar | Weight | Initial (JUDGE_002) | First Pass | Second Pass | Weighted |
|--------|--------|---------------------|------------|-------------|----------|
| Novelty | 20% | 6/10 | 6/10 | 6/10 | 1.2 |
| Physics/Science Depth | 40% | 5/10 | 6/10 | 6/10 | 2.4 |
| Contribution | 30% | 5/10 | 6/10 | 6/10 | 1.8 |
| Relevancy | 10% | 9/10 | 9/10 | 9/10 | 0.9 |
| **Total** | | **5.6** | **6.3** | | **6.3** |

**Score: 6/10** (unchanged from first pass)

All actionable items except H2 (reference DOIs) have been resolved. The manuscript text is now internally consistent (+64.9% throughout), figures are correct, metrics are properly labelled, and the experimental design is properly qualified. The paper has reached the point where its methodology, experiments, and claims are scientifically defensible.

**The sole blocker to 7/10 is H2:** Add DOIs or arXiv eprint fields to the 11 application study references. A sceptical reviewer will attempt to verify these citations -- they populate Table 5, the paper's core evidence table. Without DOIs, these references are unverifiable, and a reviewer who cannot find them will question the entire evidence base.

**If H2 is resolved, score rises to 7/10.** At that point, no structural issues remain. The paper would be suitable for submission with a reasonable expectation of "minor revision" at the target journal.

---

*"Invert, always invert. The question is no longer 'how will this paper be rejected?' -- the methodology is now sound, the experiments are real, the figures are correct. The question is now 'what will a sceptical reviewer Google first?' The answer: those 11 references without DOIs. Fix that, and the paper defends itself."*
