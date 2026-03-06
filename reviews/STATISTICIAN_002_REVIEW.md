# STATISTICIAN REVIEW 002 -- Foundation Models for Clean Energy Systems

**Reviewer:** Statistician (Fisher)
**Date:** 2026-03-06
**Manuscript:** `manuscript/main.tex` (913 lines, 45 pages, 35 content + 10 references/appendix)
**References:** `manuscript/references.bib` (94 entries)
**Review type:** Second statistical/methodological review — full re-evaluation after major revision

---

## EXECUTIVE SUMMARY

The paper has improved substantially since STATISTICIAN_001 (4/10). All three CRITICAL items and most HIGH/MEDIUM items from the first review have been addressed: the PRISMA-ScR flow diagram now has counts (427->289->91->31), the 31 included studies are explicitly stated, a study distribution table (Table 4) provides coded aggregate counts, the maturity matrix has explicit thresholds, inter-rater agreement is reported (88% on 8/31), and a performance metrics table (Table 5) presents quantitative results from 11 Level A studies. Five benchmark experiments with real data and real models add original quantitative evidence. These are genuine improvements.

However, this review identifies **new statistical issues** that became visible only after the computational experiments were added:

1. **CRITICAL: The exponential growth claim (R^2=0.95, doubling time 1.3 years) is inconsistent with the data and internally contradicted by a separate analysis (R^2=0.49, doubling time 3.3 years).** The underlying data shows flat publication counts 2019-2022 followed by a step-change in 2023, not genuine exponential growth. The high R^2 is an artefact of scale dominance in nonlinear least squares.

2. **CRITICAL: The RAG experiment's 136.7% improvement claim is confounded by infrastructure failures.** 7 of 15 direct-LLM queries timed out (receiving zero scores), inflating the improvement figure. This is not a fair comparison of RAG vs direct LLM.

3. **HIGH: No benchmark experiment reports confidence intervals, standard errors, or significance tests.** All five experiments report single point estimates without uncertainty quantification.

The scoping review methodology is now sound. The new issues are concentrated in the benchmark experiments (Section 10), which have moved from "absent" to "present but statistically incomplete."

---

## STATISTICIAN_001 RESOLUTION AUDIT

| # | Issue (STAT_001) | Status | Evidence |
|---|------------------|--------|----------|
| M1 | PRISMA-ScR flow lacks counts | **RESOLVED** | Fig 1: 427->289->91->31 with approximate notation |
| M2 | Included study count not stated | **RESOLVED** | "31 included application studies" in abstract, S2.3, S5, conclusions |
| R1 | Zero performance metrics from literature | **RESOLVED** | Table 5: 11 Level A studies with FM result, baseline, metric |
| M3 | Inter-rater agreement not quantified | **RESOLVED** | Line 111: 8/31 studies, 88% raw agreement, limitation acknowledged |
| M5 | Coding scheme no aggregate output | **RESOLVED** | Table 4: 31 studies cross-tabulated by domain x FM type |
| M6 | Maturity matrix criteria undefined | **RESOLVED** | Table 3 caption: Active >= 3 studies with >= 1 Level A; Emerging = 1-2; Gap = 0 |
| R2 | "Competitive" without statistical basis | **RESOLVED** | Replaced with specific metrics in domain sections and Table 5 |
| M4 | Level A/B/C distribution not reported | **RESOLVED** | Line 118: 20 Level A (65%), 8 Level B (26%), 3 Level C (10%) |
| R3 | UQ in reviewed studies not assessed | **RESOLVED** | Section 10.1: "Only 6 of 20 Level A studies report prediction intervals" |
| R4 | Comparison table lacks methodology | **RESOLVED** | Section 11: self-assessment bias acknowledged |
| E1 | CNKI excluded despite Chinese emphasis | **RESOLVED** | Line 90: explicit justification |
| E3 | No search completeness check | **RESOLVED** | Line 92: validated against Zhou et al. and Lotfi et al. |
| E2 | arXiv temporal bias | **RESOLVED** | Line 88: acknowledged as limitation |
| E4 | Sensitivity analysis on maturity matrix | **RESOLVED** | Section 5.2: three perturbations tested, Gap cells robust |

**Verdict:** 14/14 items from STATISTICIAN_001 are resolved. Strong and thorough response.

---

## METHODOLOGY (50% of evaluation)

### M1. Scoping Review Methodology -- Now Adequate

The PRISMA-ScR framework is properly executed. The flow diagram has approximate counts at each stage. The eligibility criteria are clear and the FM vs standard-DL distinction (line 99) is well-defined. The risk-of-bias scheme (Level A/B/C) with distribution (20/8/3) is useful. The sensitivity analysis on maturity matrix thresholds (Section 5.2) is a genuine methodological strength rare in survey papers.

**Remaining concern:** Inter-rater reliability. The 88% agreement on 8/31 studies (7/8 concordant) is honestly reported, but with n=8 the Wilson 95% confidence interval is approximately [47%, 99.7%]. This CI is too wide to be statistically informative — it is consistent with both excellent and mediocre agreement. The paper acknowledges "a larger subset and formal Cohen's kappa would strengthen reliability" (line 111), which is appropriate. This is a limitation, not an error.

### M2. Exponential Growth Fit -- CRITICAL: Internally Contradictory and Misleading

The manuscript claims (line 186, abstract, conclusions): "Growth follows an exponential trajectory (R^2 = 0.95, p < 0.001) with a doubling time of 1.3 years and an annualised growth rate of 74%."

This claim has three problems:

**Problem 1: Internal inconsistency.** Two different scripts produce dramatically different exponential fit results from the same data:

| Source | Method | Year range | R^2 | Doubling time | Annual growth |
|--------|--------|-----------|------|---------------|---------------|
| `fig_publication_trend.py` (line 32) | Nonlinear `curve_fit` on raw counts | 2019-2025 | 0.95 | 1.3 yr | 74% |
| `summary_statistics.py` (line 55) | OLS on log(counts) | 2017-2026 | 0.49 | 3.3 yr | 23% |

The manuscript reports only the favourable fit (R^2=0.95). Both analyses use the same underlying dataset (`classified_papers.csv`). The difference arises from (a) different year ranges and (b) different fitting methodologies. When two legitimate statistical approaches give R^2 values differing by 0.46, the "exponential growth" characterisation is not robust.

**Problem 2: The data does not show exponential growth.** The yearly counts from `summary_statistics.json` are:

| Year | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|------|------|------|------|------|------|------|------|
| Count | 144 | 134 | 126 | 136 | 370 | 975 | 1319 |
| Growth | -- | -7% | -6% | +8% | +172% | +164% | +35% |

The 2019-2022 period is essentially flat (mean ~135, growth rates -7%, -6%, +8%). The explosion begins in 2023, coinciding with ChatGPT's public release. This is a **regime shift** or **hockey-stick pattern**, not genuine exponential growth. Exponential growth would show consistent positive growth rates throughout the period; here, three of the first four growth rates are negative or near-zero.

**Problem 3: The R^2=0.95 is inflated by scale dominance.** In nonlinear least squares, residuals are computed in the original scale. The three large values (370, 975, 1319) dominate the total sum of squares (SS_tot). An exponential that captures the 2023-2025 rise achieves high R^2 even if it badly misfits the flat 2019-2022 period, because the residuals at counts ~130 are tiny compared to SS_tot driven by counts ~1000. This is a well-known problem with R^2 for nonlinear models.

**Required:**
1. Report both fits (or at minimum, the one on log-transformed data) and acknowledge the discrepancy.
2. Replace "exponential growth" with a more honest characterisation: "Publication counts were approximately stable at ~135/year from 2019-2022, then surged dramatically from 2023, reaching 1,319 in 2025 (partial year). An exponential fit to 2019-2025 yields R^2 = 0.95 on raw counts but only R^2 = 0.49 on log-transformed counts, indicating a regime shift rather than sustained exponential growth."
3. Report the p-value for the exponential fit from the figure script (currently only "p < 0.001" is stated; this refers to the log-linear fit, not the `curve_fit` model).

### M3. Bibliometric Classification Validation -- Adequate but Thinly Reported

The 88% agreement between automated keyword classification and manual coding on 100 random papers (line 181) is acceptable. However:
- No breakdown is given by FM type or domain — where does the 12% disagreement concentrate?
- No confusion matrix for the automated classifier is provided.
- The Wilson 95% CI for 88/100 agreement is [80%, 93%], which should be reported.

**Suggested:** Report the CI and note which categories had higher/lower agreement.

---

## RESULTS (30% of evaluation)

### R1. RAG Improvement Claim Confounded by Timeouts -- CRITICAL

The paper claims (line 743): "RAG-augmented answers outperformed direct LLM on the same 15 questions: mean keyword score 0.616 vs. 0.260 (+136.7%)."

Inspection of `rag_pipeline.json` reveals:
- **Direct LLM:** 7 of 15 queries timed out (q2, q10, q11, q12, q13, q14, q15), receiving scores of 0. Only 8/15 queries produced actual LLM responses.
- **RAG:** 3 of 15 queries timed out (q2, q12, q15), receiving scores of 0. 12/15 queries produced responses.

The "improvement" is thus largely an artefact of differential timeout rates (47% for direct vs 20% for RAG), not a true comparison of answer quality. The direct LLM baseline of 0.260 is depressed by 7 zero-scores from timeouts, not by the LLM giving wrong answers.

The manuscript partially acknowledges this (line 743): "7 of 15 queries timed out under the 300s limit, receiving zero scores; thus this comparison primarily demonstrates RAG's value rather than absolute LLM performance." This caveat is appropriate but insufficient — the 136.7% figure still appears in the abstract-adjacent conclusions (line 847) and the Pareto figure caption without qualification.

**Required:**
1. Report the timeout-adjusted comparison: excluding timed-out questions from both conditions, what is the improvement? For the 5 questions where both direct and RAG produced responses (q1, q3, q4, q5, q6, q7, q8, q9 — actually need to check which pairs both succeeded), compute the paired improvement.
2. At minimum, report: "On the 8 questions where both direct LLM and RAG produced responses, mean scores were X vs Y (Z% improvement)." This removes the timeout confound.
3. The 136.7% headline figure should either be replaced with the timeout-adjusted figure or always accompanied by the timeout caveat (including in conclusions and figure captions).
4. Report why timeouts were more frequent for direct LLM than RAG — was this due to system load, prompt length, or a systematic difference?

### R2. No Confidence Intervals or Significance Tests on Benchmark Results -- HIGH

All five benchmark experiments report only point estimates. No experiment reports standard errors, confidence intervals, or hypothesis tests.

**Experiment 1 (Time-series):** Chronos MAE=0.483 vs XGBoost MAE=0.540. Is this difference statistically significant? With a 168-hour test set, the standard error of the difference is computable from the residuals. Without it, we cannot distinguish a meaningful improvement from noise.

Additionally, both ARIMA and Chronos use a **10-window nearest-neighbour approximation** (lines 112, 264 of `timeseries_benchmark.py`) where only 10 of the 7 prediction windows are actually evaluated and the rest are filled by nearest-neighbour interpolation. This means the reported metrics are computed on partially duplicated predictions, not independent forecasts. The effective sample size is closer to 10 windows (240 hours) than 168 hours, and the reported MAE/RMSE/MAPE include an unknown approximation bias from the nearest-neighbour filling.

**Experiment 2 (LLM Q&A):** Mean keyword score 0.519 +/- 0.224 (the std dev IS reported — this is good). But domain-level comparisons (wind 0.675 vs AI 0.405) are reported without significance tests. With n=10 per domain, a two-sample t-test or Mann-Whitney U test is straightforward and necessary to determine whether domain differences are real or noise.

**Experiment 3 (VLM):** F1=0.606 (zero-shot) vs F1=0.755 (supervised). No confidence interval on F1 via bootstrapping or other methods. With n=300, bootstrap CIs are computationally trivial and would clarify whether the gap is statistically significant.

**Experiment 5 (Reproducibility):** Code mention rate = 5.5%. For n=3,645, the Wilson 95% CI is approximately [4.8%, 6.3%]. This should be reported.

**Required:**
1. For the time-series benchmark: report prediction intervals or at minimum note the 10-window approximation and its implications for metric reliability.
2. For the LLM Q&A: perform pairwise significance tests on domain differences (10 questions per domain is marginal but testable).
3. For the VLM experiment: report bootstrap 95% CIs on F1 for each method.
4. For reproducibility metrics: report Wilson CIs for proportions.

### R3. Time-Series Benchmark Design Issues -- HIGH

Several design choices in `timeseries_benchmark.py` systematically disadvantage baselines and advantage Chronos:

**a) ARIMA approximation (lines 112-132):** Only 10 of 7 windows are actually fitted; the remainder use nearest-neighbour interpolation from the 10 fitted windows. ARIMA is a sequential model where each window should use the latest available data as context. The approximation degrades ARIMA performance more than it degrades Chronos (which also uses 10 windows but has richer context representation).

**b) LSTM training truncation (line 178):** The LSTM is trained on only the last 3,000 hours (~4 months) of data with only 5 epochs and a single layer of 32 hidden units. This is a deliberately weak baseline. A properly tuned LSTM trained on the full training set with hyperparameter search would likely perform better. The paper claims Chronos beats "LSTM" but it really beats "a barely-trained single-layer LSTM with minimal data."

**c) XGBoost uses GradientBoostingRegressor (line 153):** The code uses sklearn's `GradientBoostingRegressor`, not actual XGBoost (`xgboost.XGBRegressor`). This is mislabeled in the manuscript. `GradientBoostingRegressor` with 100 estimators and no hyperparameter tuning is a weak baseline.

**d) Test set size (line 94):** 7 days (168 hours) is a very small test set for load forecasting. Standard practice uses at least 30-90 days. With only 7 days, a single unusual day (holiday, extreme weather) could dominate the metrics.

**e) No cross-validation or repeated evaluation:** A single train/test split on 7 days provides no measure of variability. Rolling-window evaluation (common in forecasting literature) would provide multiple test windows and enable CI computation.

**Required:**
1. Acknowledge that baselines use simplified configurations and that the comparison favours the zero-shot FM. State something like: "Baselines use default hyperparameters without tuning; the comparison demonstrates FM zero-shot capability rather than establishing superiority over optimised baselines."
2. Correct the "XGBoost" label to "Gradient Boosting" or actually use the XGBoost library.
3. Consider reporting results on a longer test period or with rolling-window evaluation.

### R4. VLM Experiment: Domain-Specific Prompt Is Degenerate -- MEDIUM

The CLIP zero-shot (domain) result in Table 8 shows: accuracy=0.500, precision=0.500, recall=1.000, F1=0.667. This is a **trivial all-positive classifier** — it classifies every image as defective. The confusion matrix confirms this (the domain prompt would show 0 true negatives, 150 false positives, 0 false negatives, 150 true positives).

The manuscript correctly notes this (line 731): "domain-specific prompts achieve perfect recall but trivially classify all images as defective." However, this degenerate result is still presented in Table 8 alongside meaningful results, and its F1 (0.667) exceeds the generic prompt's F1 (0.606), which could mislead a reader scanning the table.

**Suggested:** Add a footnote to Table 8 noting that the domain prompt's F1 reflects a degenerate all-positive prediction, not meaningful classification. Consider reporting balanced accuracy alongside F1 to expose such degenerate behaviour.

### R5. LLM Q&A: 0% Hallucination Rate Is Implausible -- MEDIUM

The paper reports (line 698): "zero hallucinations" from the 50-question LLM Q&A benchmark. Inspection of `llm_energy_qa.json` shows that the hallucination detection method is the field `likely_hallucination`, which is `false` for all 50 questions.

However, several responses contain factual inaccuracies that a domain expert would classify as hallucinations:
- Q46 (SAM): "developed by researchers at Adobe and Stanford University" — SAM was developed by Meta AI. This is a factual error.
- Q29 (inverter architectures): "Single-Stage Inverters" and voltage boosting description instead of the expected "string inverters and microinverters" — this is a hallucination of a non-standard category.
- Q1 (hydropower capacity factor): Response says "40-60%" range is typical but then trails off without completing the answer, matching only 1/4 keywords.

The 0% hallucination rate likely reflects a limitation of the automated detection method (keyword-based heuristic), not a genuine absence of hallucinations. The paper acknowledges keyword scoring limitations (line 698) but not the hallucination detection limitation.

**Required:** Acknowledge that "the keyword-based hallucination detection is a conservative heuristic that may undercount factual errors; the reported 0% rate should be interpreted as an absence of detected hallucinations, not an absence of factual errors."

### R6. Performance Metrics Table (Table 5) -- Improvement but with Caveats

Table 5 now reports 11 Level A study results — a major improvement from the zero metrics reported in the first draft. However:

1. **No uncertainty information from cited studies.** None of the 11 entries in Table 5 include error bars, standard deviations, or confidence intervals from the original studies. The paper notes (Section 10.1, line 781): "Only 6 of 20 Level A studies report prediction intervals" — but Table 5 does not indicate WHICH of its 11 entries report uncertainty and which do not.

2. **Unverifiable references.** The Worker flagged (progress.md, line 8) that approximately 30 references could not be verified via web search. Several of these populate Table 5 (e.g., xu2024tsfm_streamflow, wang2024vlm_blade_defect, huang2024clip_pv_defect, zhang2024sam_fish_monitoring, liu2024clip_bird_wind). If these references are fabricated or incorrect, the metrics in Table 5 are unverifiable. This is not a statistical issue per se, but it directly undermines the statistical claims.

**Required:** Flag which Table 5 entries report uncertainty measures in the original study. The reference verification issue is for the Worker/Judge to resolve.

---

## EXPERIMENTAL DESIGN (20% of evaluation)

### E1. Scoping Review Design -- Now Adequate

The search strategy, eligibility criteria, screening process, and coding scheme are properly described. The sensitivity analysis on maturity thresholds is a genuine strength. The acknowledgement of CNKI exclusion, arXiv temporal bias, and small inter-rater sample are appropriate.

### E2. Benchmark Experiment Sample Sizes -- MEDIUM

| Experiment | Sample size | Adequacy |
|-----------|------------|----------|
| Time-series | 168 hours (7-day test), 10 evaluated windows | Small; standard is 30-90 days |
| LLM Q&A | 50 questions (10/domain) | Marginal; insufficient for robust domain comparisons |
| VLM | 300 images (150/class) | Adequate for binary classification |
| RAG | 15 questions (2-3/domain) | Very small; domain-level analysis unreliable |
| Reproducibility | 3,645 papers | Large; adequate |

The RAG experiment with 15 questions (2-3 per domain) does not support domain-level analysis. Reporting "improvement by domain" (e.g., ecological +0.717, grid +0.444) with n=2-3 per domain is not statistically meaningful. The VLM experiment with 300 balanced images is adequately powered for binary classification.

### E3. Cross-Experiment Pareto Synthesis -- MEDIUM

The Pareto analysis (Section 10.6) mixes three incommensurable metrics (1-nMAE, F1, keyword score) on a single plot. The manuscript now acknowledges this (line 753, figure caption): "cross-category comparisons are approximate." This is acceptable but could be strengthened:

1. The performance normalisation for time-series uses `1 - MAE/max_MAE*1.1` (cost_performance.py line 171). The 1.1 multiplier on max_MAE is arbitrary and affects the normalised values. Without justification, this introduces a non-transparent transformation.

2. The compute cost estimates (TFLOPS) and setup hours are author estimates, not measured values. These should be flagged as approximate.

**Suggested:** Note in the text that TFLOPS and setup hours are rough estimates, and that the 1.1x padding in normalisation is a modelling choice.

---

## WHAT IS WORKING WELL

1. **All 14 STATISTICIAN_001 items resolved.** The response to the first review was thorough and honest. The maturity matrix sensitivity analysis, the Level A/B/C distribution, the UQ assessment of the evidence base, and the study distribution table all demonstrate genuine engagement with statistical rigour.

2. **Performance metrics table (Table 5) is a major addition.** Reporting FM result, baseline result, metric, and baseline type for 11 studies enables readers to assess claims quantitatively. The synthesis paragraph (Section 5.3, line 408) — "zero-shot TSFM performance falls within 10-20% of site-specific baselines" — is now grounded in evidence.

3. **The sensitivity analysis (Section 5.2) is excellent.** Testing three perturbations (higher Active threshold, Level C exclusion, date restriction) and finding 19 Gap cells unchanged is a rigorous approach to establishing robustness of the maturity matrix. This is rare and commendable in survey papers.

4. **UQ assessment of the evidence base (Section 10.1, line 781).** Reporting that "only 6 of 20 Level A studies report prediction intervals" is a genuine finding that highlights a critical gap in the field. This is exactly the kind of synthesis a statistician wants to see.

5. **Benchmark experiments use real data and real models.** The Chronos, CLIP, and Qwen2.5-7B results are reproducible with the documented code and fixed random seeds. The experimental approach is fundamentally sound; the issues are about statistical completeness, not scientific integrity.

6. **The keyword scoring limitation is acknowledged** (line 698). The RAG timeout issue is partially acknowledged (line 743). These are honest disclosures that should be expanded, not retracted.

7. **The chi-squared test** confirming FM type and energy domain are not independent (p < 0.001) is a proper use of statistical testing on the bibliometric data.

---

## SUMMARY OF FINDINGS

| # | Finding | Severity | Section |
|---|---------|----------|---------|
| M2 | Exponential growth claim internally contradicted (R^2=0.95 vs 0.49) and data shows step-change not exponential | **CRITICAL** | S3.2, abstract, conclusions |
| R1 | RAG 136.7% improvement confounded by differential timeout rates (7/15 vs 3/15) | **CRITICAL** | S10.4, conclusions |
| R2 | No confidence intervals or significance tests on any benchmark result | **HIGH** | S10.1-10.5 |
| R3 | Time-series baselines are deliberately weak (LSTM: 3000 samples, 5 epochs; XGBoost mislabeled; ARIMA approximated) | **HIGH** | S10.1 |
| R4 | VLM domain prompt is degenerate all-positive classifier, F1 misleading | **MEDIUM** | Table 8, S10.3 |
| R5 | 0% hallucination rate reflects detection method limitation, not absence | **MEDIUM** | S10.2 |
| R6 | Table 5 metrics from cited studies lack uncertainty; some references unverifiable | **MEDIUM** | Table 5 |
| E2 | RAG domain-level analysis with n=2-3 per domain not statistically meaningful | **MEDIUM** | S10.4 |
| E3 | Cost-performance normalisation uses arbitrary 1.1x padding; costs are estimates | **MEDIUM** | S10.6 |
| M3 | Bibliometric classifier validation lacks per-category breakdown and CI | **LOW** | S3.1 |
| M1 | Inter-rater Wilson CI ~[47%, 99.7%] — too wide to be informative | **LOW** | S2.4 |

---

## SCORING

| Component | Weight | STAT_001 | STAT_002 | Notes |
|-----------|--------|----------|----------|-------|
| Methodology | 50% | 4/10 | 6/10 | PRISMA-ScR proper; exponential fit issue drags score |
| Results | 30% | 3/10 | 5/10 | Table 5 and benchmarks present but lack UQ; RAG confounded |
| Experimental Design | 20% | 5/10 | 6/10 | Scoping review design good; benchmark design has weaknesses |
| **Weighted Total** | | **3.9** | **5.6** |  |

**Score: 6/10**

The score rises from 4/10 to 6/10, reflecting resolution of all 14 prior items plus the addition of five benchmark experiments with genuine quantitative evidence. The paper now has real data, real numbers, and real methodology. The critical gap is that the benchmark experiments lack the statistical completeness expected of quantitative claims: no confidence intervals, no significance tests, confounded comparisons, and an internally inconsistent growth characterisation.

**Path to 7/10:**
1. Fix the exponential growth characterisation (honest description of the regime shift, report both fit statistics, or restrict the claim to 2023-2025)
2. Report timeout-adjusted RAG improvement alongside the raw figure
3. Add confidence intervals to at least the timeseries and VLM benchmarks (bootstrap CIs are computationally trivial)
4. Acknowledge baseline weakness in the timeseries benchmark

**Path to 8/10:**
All of the above, plus:
- Significance tests on LLM Q&A domain differences
- Rolling-window evaluation for the timeseries benchmark
- Corrected "XGBoost" label
- Bootstrap CIs on VLM F1 scores
- Wilson CIs on reproducibility proportions

---

*"To consult the statistician after an experiment is finished is merely to ask him to conduct a post-mortem examination. He can perhaps say what the experiment died of." The experiments in this paper are alive, but they need proper vital signs — confidence intervals are the heartbeat of any quantitative claim. Show me the intervals, and the numbers will speak for themselves." — Fisher's prescription for this manuscript.*

---

## ADDENDUM: POST-FIX REASSESSMENT (2026-03-06, same session)

The Worker applied fixes during Sessions 15-18. Updated assessment below.

### Resolution Status of STATISTICIAN_002 Items

| # | Item | Severity | Status | Evidence |
|---|------|----------|--------|----------|
| M2 | Exponential growth claim | **CRITICAL** | **RESOLVED** | Line 186: "regime shift coinciding with ChatGPT's release rather than sustained exponential growth." Both R^2 values reported (0.95 raw, 0.49 log). Abstract updated: "regime shift in publication activity." Figure caption updated. Excellent rewrite. |
| R1 | RAG timeout confound | **CRITICAL** | **RESOLVED** | Line 745: raw (0.616 vs 0.260, +136.7%) clearly labeled as confounded; controlled comparison (0.804 vs 0.488, +64.9%) on 8 paired non-timeout questions. Line 755: uses +64.9%. Line 849 (conclusions): uses +64.9%. No remaining stale 136.7% figures outside the properly-qualified raw comparison. |
| R2 | No CIs on benchmarks | **HIGH** | **PARTIALLY RESOLVED** | Wilson CIs added for VLM accuracy ([0.57, 0.68] vs [0.71, 0.81], line 733) and reproducibility metrics (line 750). **BUT** the time-series benchmark (Table 6) still reports only point estimates — no CIs on MAE, RMSE, or MAPE. See new item below. |
| R3 | Weak baselines, XGBoost label | **HIGH** | **RESOLVED** | "Gradient Boosting" label (line 679). Disclaimer: "All baselines use default hyperparameters; the comparison demonstrates FM zero-shot capability rather than superiority over optimised baselines" (line 667). Caveat: "Optimised baselines with longer test periods may narrow the gap" (line 686). |
| R4 | VLM degenerate prompt | **MEDIUM** | **RESOLVED** | Footnote on Table 8 (line 730): "Degenerate all-positive classifier... F1 reflects class balance, not meaningful discrimination." |
| R5 | Hallucination detection | **MEDIUM** | **RESOLVED** | Line 698: "detected hallucinations, though the keyword-based heuristic is conservative and may miss factual errors (e.g., the 7B model incorrectly attributed SAM to Adobe rather than Meta AI)." |
| R6 | Table 5 uncertainty | **MEDIUM** | **RESOLVED** | Table caption (line 412): "All values are point estimates as reported; none of the cited studies provide confidence intervals or standard errors." |
| E2 | RAG domain n too small | **MEDIUM** | **NOTED** | Limitation inherent to the 15-question design; acknowledged implicitly by the paired comparison approach. |
| E3 | Pareto normalization | **MEDIUM** | **RESOLVED** | Line 755: "Because performance metrics differ across task categories... cross-category comparisons are approximate." |
| M3 | Classifier validation CI | **LOW** | **RESOLVED** | Line 181: "88% agreement with manual coding; Wilson 95% CI [80%, 93%]." |
| M1 | Inter-rater CI too wide | **LOW** | **NOTED** | Limitation acknowledged in line 111. Acceptable. |

### New Positive Finding: Dual-Model Statistical Comparison

The Worker added Qwen2.5-3B (Session 17) with proper statistical testing:
- Wilcoxon signed-rank test: p = 0.89 (appropriate for paired, non-parametric data)
- Cohen's d = 0.016 (negligible effect size)
- 95% CI for difference: [-0.069, +0.077] (crosses zero, confirming no significant difference)
- Win/loss/tie: 7B wins 15, 3B wins 12, ties 23

This is well-executed. The Wilcoxon test is the correct choice for paired ordinal scores. The effect size quantification via Cohen's d is a best practice. The conclusion — "energy domain knowledge is retained even at 3B scale" — is appropriately cautious and properly supported by the statistical evidence. This addresses both the Judge's request for a second model and my request for significance testing on at least one comparison.

### Remaining Items

**R2-residual (MEDIUM, downgraded from HIGH): Time-series benchmark still lacks CIs.**

The time-series table (lines 674-683) reports MAE, RMSE, and MAPE as point estimates only. This is the paper's strongest quantitative claim ("MAE 33% below ARIMA") and the one most in need of uncertainty bounds. The VLM and reproducibility CIs are welcome, but the timeseries experiment — with only a 7-day test set and 10-window approximation — is where CIs matter most.

The disclaimer "All baselines use default hyperparameters" (line 667) and "Optimised baselines with longer test periods may narrow the gap" (line 686) partially mitigate this by framing the comparison as demonstrative rather than definitive. Given the survey context, I downgrade this from HIGH to MEDIUM.

**Suggested fix:** Add a sentence: "With a 7-day test set, individual daily MAEs range from [X] to [Y], reflecting the variability that a rolling-window evaluation would capture." This requires no new computation — just computing per-day MAE from the existing predictions.

**E2-residual (LOW): LLM Q&A domain differences untested.**

Domain scores range from 0.405 (AI) to 0.675 (wind) but no omnibus test (e.g., Kruskal-Wallis) is reported. With n=10 per domain, a test is feasible. However, the dual-model comparison (Wilcoxon p=0.89) demonstrates that the Worker is capable of proper testing; the domain differences are presented descriptively rather than as statistical claims, and the figure caption appropriately says "uneven parametric knowledge" rather than "significantly different." This is acceptable. Downgraded to LOW.

### Updated Scoring

| Component | Weight | Original | Updated | Notes |
|-----------|--------|----------|---------|-------|
| Methodology | 50% | 6/10 | 8/10 | Regime shift honest; both R^2 reported; classifier CI added |
| Results | 30% | 5/10 | 7/10 | RAG adjusted; VLM CIs; dual-model Wilcoxon; TS CIs still missing |
| Experimental Design | 20% | 6/10 | 7/10 | Baseline disclaimer; second model; honest framing |
| **Weighted Total** | | **5.6** | **7.5** | |

**Revised Score: 7/10**

The score rises from 6/10 to 7/10. The key drivers:

1. The regime shift rewrite (M2) is textbook-quality honest characterization — reporting both R^2 values and letting the reader decide is exactly what Fisher would demand.
2. The timeout-adjusted RAG comparison (R1) with clean paired analysis (+64.9%) replaces the confounded raw figure — proper experimental methodology.
3. The Wilcoxon/Cohen's d dual-model comparison is genuine statistical testing applied to the benchmark results.
4. The Wilson CIs on VLM accuracy and reproducibility metrics show the uncertainty quantification culture is improving.
5. The baseline disclaimers transform the timeseries comparison from a misleading superiority claim to an honest demonstration.

**Path to 8/10:**
1. Add per-day MAE range or bootstrap CIs for the time-series benchmark
2. Kruskal-Wallis test on LLM Q&A domain differences (or explicitly state the comparison is descriptive)
3. Bootstrap CIs on VLM F1 (not just accuracy)

**Path to 9/10:**
All of the above, plus rolling-window evaluation for the timeseries benchmark and a larger RAG question set to enable domain-level analysis.

---

*"The regime shift rewrite is the most important fix. A scientist who reports R^2 = 0.95 AND R^2 = 0.49 from two legitimate analyses of the same data, and explains why they differ, earns more trust than one who cherry-picks the favourable number. This paper now earns that trust." — Fisher's revised assessment.*
