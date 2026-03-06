# STATISTICIAN REVIEW 001 — Foundation Models for Clean Energy Systems

**Reviewer:** Statistician (Fisher)
**Date:** 2026-03-05
**Manuscript:** `manuscript/main.tex` (797 lines, ~59 pages double-spaced)
**References:** `manuscript/references.bib` (111 entries)
**Review type:** First statistical/methodological review of revised draft (post-Judge)

---

## EXECUTIVE SUMMARY

This paper is a scoping review, not a simulation or experimental paper. My role here
is therefore focused on: (a) the rigour of the scoping review methodology, (b) whether
the claims made in the synthesis are properly supported by the evidence cited, (c)
whether the analytical outputs (maturity matrix, comparisons) have transparent criteria
and are reproducible, and (d) whether quantitative information from the reviewed
literature is accurately reported with appropriate uncertainty/caveats.

The Worker has correctly reframed the paper from a PRISMA systematic review to a
PRISMA-ScR scoping review, which is methodologically honest. The three-level
validation scheme (Level A/B/C) in Section 2.5 is a welcome addition. However,
significant methodological gaps remain: the scoping review lacks the quantitative
"charting" that PRISMA-ScR expects, the maturity matrix has no transparent threshold
criteria, no study counts are reported anywhere, inter-rater agreement is
unquantified, and the domain sections report zero performance metrics from the
reviewed literature. A scoping review that maps a field should show the map
quantitatively, not just describe it in prose.

---

## METHODOLOGY (50% of evaluation)

### M1. PRISMA-ScR Flow Diagram Lacks Counts — CRITICAL

The PRISMA-ScR flow diagram (Fig. 1, lines 154–192) is entirely qualitative: boxes
say "Records identified from database searches and citation chasing" and "Studies
included in scoping review synthesis" without any numbers. While the move away from
fabricated counts is correct and honest, a PRISMA-ScR flow diagram should still
report the actual counts at each stage.

Tricco et al. (2018) — which the paper cites — state that the flow diagram should
present "the number of sources of evidence screened, assessed for eligibility, and
included in the review." Even approximate counts are acceptable for a scoping review.
Reporting zero numbers makes the screening process unverifiable and unreproducible.

**Required:** Add the actual counts to the flow diagram boxes — at minimum: records
identified (total across databases), records after deduplication, records screened at
title/abstract, records assessed at full text, and studies included in synthesis.
These numbers must come from an actual search export, not be invented.

### M2. Total Included Study Count Never Stated — CRITICAL

Nowhere in the paper does the reader learn how many studies were actually included in
the scoping review. The abstract says "we identify and synthesise the emerging
literature" — how many studies? Section 2.3 says "The final scoping review synthesis
includes the studies discussed in Sections 6–9" — how many? The bibliography has 111
entries, but many are foundational architecture papers, review methodology references,
and competing survey papers that are not themselves "included studies."

For a scoping review, the number of included studies is a fundamental descriptive
statistic. Without it, the reader cannot assess coverage, completeness, or whether the
maturity assessments are based on 20 studies or 200.

**Required:** State the total number of included application studies explicitly in the
abstract, the methodology section, and the conclusions. Separate foundational/
methodological references from included application studies.

### M3. Inter-Rater Reliability — No Quantitative Agreement Reported — HIGH

Section 2.4 (line 136) states: "The charting was performed by the first author and
verified by the second author (BR) on a stratified subset spanning all energy domains
and model types. Disagreements were resolved through discussion."

This is procedurally acceptable but statistically incomplete:
- What fraction of studies were in the "stratified subset"? (10%? 20%? 50%?)
- What was the initial agreement rate before discussion?
- Even for a scoping review, reporting percentage agreement or Cohen's kappa on the
  verification subset provides a quality signal

The prior draft had fabricated kappa values (0.82, 0.78–0.91), which the Worker
correctly removed. But the replacement provides no quantitative agreement measure at
all. The solution is to report the real agreement on the actual verification subset.

**Required:** Report the fraction of studies verified and the observed agreement rate.
If the verification has not been conducted yet, acknowledge this as a limitation and
plan to complete it before submission.

### M4. Risk of Bias Scheme — Useful but Not a Formal Assessment — MEDIUM

Section 2.5 introduces a three-level validation scheme:
- Level A: quantitative benchmark with held-out test set and baseline comparisons
- Level B: case study / proof of concept
- Level C: conceptual framework only

This is a pragmatic quality indicator and is appropriate for a scoping review (which
is not required by PRISMA-ScR to conduct formal risk-of-bias assessment). However:

1. The paper states "a disproportionate fraction of current studies fall at Levels B
   and C" (line 149) but never reports the actual distribution. How many are A? How
   many B? How many C? This is a key finding of the review — it should be quantified.

2. The Level A/B/C assignments are stated in narrative prose in Sections 6–9 (e.g.,
   "Level B–C validation" for offshore site assessment, line 606) but inconsistently.
   Not every cited study is tagged with its level. If this is a coding dimension, apply
   it consistently and report the totals.

**Required:** Report the distribution of included studies across Levels A/B/C, either
in a summary table or in the text. Tag all cited application studies with their level.

### M5. Coding Scheme Produces No Aggregated Quantitative Output — HIGH

Section 2.4 defines six coding dimensions (energy domain, FM type, deployment
strategy, task type, validation approach, dataset availability). This is a well-
designed coding framework. However, the results of the coding are never presented as
aggregated statistics.

PRISMA-ScR step 4 ("charting the data") expects a structured presentation of the
charted data, typically as:
- A frequency table showing study counts per energy domain
- A frequency table showing study counts per FM type
- A cross-tabulation of FM type × task type (with counts, not just maturity symbols)
- A bar chart or table of temporal distribution (studies per year)
- Distribution by deployment strategy
- Distribution by dataset availability (public vs. proprietary vs. none)

Instead, the paper presents only: (a) a qualitative maturity matrix (Table 3) with
three-level symbols, and (b) purely narrative descriptions of temporal and domain
distributions (Sections 4.3–4.4). The reader learns that "wind energy applications
are the most extensively studied" (line 383) but not how many studies are in each
domain.

**Required:** Add at least one summary table or figure showing the distribution of
included studies across the six coding dimensions with actual counts. This is the
core analytical output of a scoping review.

### M6. Maturity Matrix Criteria Are Undefined — HIGH

Table 3 (lines 352–373) is the paper's central analytical contribution — a 7×5
maturity matrix with three levels (Active/Emerging/Gap). The caption defines these as:
- Active = "multiple quantitative studies"
- Emerging = "proof-of-concept studies exist"
- Gap = "no or minimal investigation"

These criteria are vague:
- How many is "multiple"? 3? 5? 10? Is 2 studies "emerging" or "active"?
- "Proof-of-concept" is Level B/C — does a single Level B study make a cell "Emerging"?
- "Minimal" — does 1 study count as minimal or as emerging?
- Are these thresholds applied consistently across all 35 cells?

Without explicit, reproducible thresholds, the maturity matrix is a subjective
assessment presented as a structured analytical output. Another reviewer applying
the same literature would likely produce different assignments.

**Required:** Define explicit numerical thresholds (e.g., Active ≥ 5 Level A studies,
Emerging = 1–4 studies with at least 1 Level A or B, Gap = 0–1 studies all Level C)
and apply them consistently. Document the specific studies supporting each cell
assignment, at least in supplementary material.

---

## RESULTS (30% of evaluation)

### R1. Zero Performance Metrics Reported from Reviewed Literature — CRITICAL

This is the most significant statistical deficiency in the paper. Sections 6–9
synthesise foundation model applications across four domains but report no quantitative
performance metrics from the reviewed studies. Not a single RMSE, MAE, F1 score,
accuracy value, MAPE, or R² appears in the domain synthesis.

Examples of claims without quantification:
- "achieving forecast skill comparable to LSTM models trained on 10+ years of data"
  (line 544) — what RMSE? Comparable within what margin?
- "competitive with persistence baselines for short horizons" (line 544) — what
  forecasting skill score? On what benchmark?
- "competitive accuracy on blade defect classification with zero-shot or few-shot
  prompting" (line 601) — what accuracy? Compared to what CNN baseline?
- "well-calibrated prediction intervals" (line 592) — what calibration metric?
  PICP? CRPS? Winkler score?

The Worker removed the earlier fabricated numbers ("12% improvement," "85% accuracy")
per the Judge's instructions. This was correct. But the replacement should be actual
numbers from the cited studies, not vaguer prose. When Xu et al. (2024) report TSFM
streamflow forecasting results, what were the actual error metrics? When Xiao et al.
(2024) compare TSFM to site-specific models, what was the performance gap?

A scoping review is not required to conduct meta-analysis, but a quality scoping
review should report representative performance metrics from Level A studies. Without
any numbers, the reader cannot assess whether foundation models actually work for
these tasks or just "show promise."

**Required:** For each domain section, report key performance metrics from at least
2–3 Level A studies (if available). Present these in a summary table or inline. Include
the baseline performance for comparison. If the original studies do not report
uncertainty (CI, std), note this as a limitation of the evidence base.

### R2. "Competitive" Used Without Statistical Basis — HIGH

The word "competitive" appears multiple times to describe FM performance vs.
baselines:
- "competitive with site-specific models" (line 544)
- "competitive forecasting performance" (line 776)
- "competitive accuracy" (line 601)
- "competitive performance" (line 592)

In statistics, "competitive" is meaningless without a quantitative basis. Does it
mean within 5% of baseline RMSE? Within one standard error? Not statistically
significantly different? The word papers over what should be a precise comparison.

**Required:** Replace every instance of "competitive" with actual performance figures,
or qualify it explicitly (e.g., "within 5–10% of the MAE achieved by site-specific
LSTMs trained on 10 years of data, as reported by Xu et al. [2024]").

### R3. Uncertainty Quantification in Reviewed Studies Not Assessed — MEDIUM

The paper discusses TSFM probabilistic forecasting (prediction intervals, calibrated
uncertainty estimates) as a capability (Sections 3.4, 6.1, 7.1) but never assesses
whether the reviewed studies actually report proper uncertainty quantification.

Key questions left unanswered:
- How many of the reviewed TSFM studies report prediction intervals?
- Are the prediction intervals calibrated (do they achieve nominal coverage)?
- Do the reviewed VLM defect detection studies report confidence scores, and are
  these calibrated?
- Do the reviewed LLM Q&A studies report any measure of response reliability?

This is directly relevant to the paper's claims about FM advantages over conventional
DL. If the paper argues FMs provide "calibrated uncertainty estimates" (line 542),
it should assess whether the cited studies actually deliver on this promise.

**Required:** Add a subsection or paragraph in the synthesis assessing the state of
uncertainty quantification across the reviewed FM studies. Report how many provide
prediction intervals, calibration metrics, or confidence measures.

### R4. Comparison Table (Table 4) Lacks Methodology — MEDIUM

Table 4 (lines 741–766) compares this review against four competing surveys using
checkmarks, dashes, and "Partial." No methodology for this comparison is described:
- Who evaluated the competing reviews?
- What criteria distinguish a checkmark from "Partial" from a dash?
- Were the competing reviews actually read and coded, or is this based on abstracts?
- Is the comparison fair? (The paper gives itself checkmarks in every row.)

A comparison table where the authors evaluate their own paper vs. competitors,
granting themselves perfect marks in every dimension, is inherently biased. At
minimum, the criteria for each checkmark should be defined transparently.

**Required:** Define the assessment criteria for each row in Table 4. Acknowledge that
self-assessment introduces bias. Consider noting specific sections/pages of competing
reviews that justify each "Partial" vs. dash assessment.

---

## EXPERIMENTAL DESIGN (20% of evaluation)

### E1. CNKI Not Included in Formal Search — MEDIUM

The plan (plan.md, line 226) lists CNKI (中国知网) as a database to be searched,
and the paper emphasises Chinese AI deployment (Qwen, ChatGLM, Three Gorges, Baichuan)
as a differentiating contribution. However, the methodology section (Section 2.1)
lists only WoS, Scopus, IEEE Xplore, arXiv, and Google Scholar. CNKI is absent.

This introduces a systematic bias: Chinese-language FM application studies published
in domestic journals (particularly those relevant to Three Gorges and CTG operations)
may be systematically underrepresented. Given the paper's emphasis on the Chinese
deployment context, this omission is methodologically concerning.

**Required:** Either include CNKI in the formal search or explicitly acknowledge its
exclusion as a limitation and explain why (e.g., access constraints, English-language
scope decision).

### E2. arXiv Inclusion Criterion Creates Temporal Bias — LOW

Section 2.1 (line 96) includes arXiv preprints with "citations ≥ 5 or accepted at
a peer-reviewed venue by February 2026." For papers published in 2025–2026 (the most
recent and arguably most relevant period), accumulating ≥5 citations within a few
months is unlikely. This creates a bias against the most recent work unless it has
been accepted at a venue.

This is a minor issue but should be acknowledged as a limitation, particularly since
the paper notes that the field lags the broader FM research curve by "approximately
12–18 months" (line 378).

### E3. No Search Completeness Check — MEDIUM

Standard practice in systematic/scoping reviews includes at least one check of search
completeness:
- Forward citation search from key anchor papers to identify missed studies
- Hand-search of proceedings from key venues (NeurIPS, ICML 2024–2025 energy
  workshops, IEEE PES General Meeting)
- Comparison with reference lists of competing review papers

The methodology mentions "targeted citation chasing (forward and backward)" from
anchor papers (line 87), which is good. But no assessment of search completeness
is reported (e.g., "X% of studies found in competing reviews were also identified
by our search").

**Required:** Report a search completeness check. At minimum, verify that all relevant
studies cited in Zhou et al. (2024) and Lotfi et al. (2024) were captured by the
search.

### E4. No Sensitivity Analysis on Maturity Assessments — LOW

The maturity matrix (Table 3) is the paper's core analytical output. No sensitivity
analysis is presented:
- Would the matrix change if the FM definition threshold were more/less strict?
- Would it change if arXiv preprints were excluded (restricting to peer-reviewed only)?
- Would it change if the date range were restricted to 2023–2026?

For a scoping review, this is a "nice to have" rather than strictly required, but it
would substantially strengthen the paper's methodological credibility.

---

## WHAT IS WORKING WELL

1. **Honest reframing as scoping review.** The move from "PRISMA systematic review"
   to "PRISMA-ScR scoping review" is methodologically honest and appropriate given the
   nascent, heterogeneous nature of the field. This was the right call.

2. **Well-designed coding scheme.** The six coding dimensions (Section 2.4) are
   comprehensive and well-defined. The challenge is that the coded data is not
   presented quantitatively.

3. **Level A/B/C validation scheme.** The three-level quality indicator (Section 2.5)
   is a useful addition that helps readers assess evidence strength. It needs to be
   applied consistently and aggregated.

4. **Appropriate scope delimitation.** The FM definition (Section 2.2, line 115) with
   the PatchTST clarification properly distinguishes foundation models from standard
   supervised Transformers. This is methodologically sound.

5. **Transparent search protocol.** The search string, date range, database list, and
   inclusion/exclusion criteria are all clearly specified. This provides the framework
   for reproducibility — it just needs the actual execution data (counts, screening
   results).

---

## SUMMARY OF FINDINGS

| # | Finding | Severity | Section |
|---|---------|----------|---------|
| M1 | PRISMA-ScR flow diagram has no counts | CRITICAL | Fig. 1 |
| M2 | Total included study count never stated | CRITICAL | Abstract, S2.3 |
| R1 | Zero performance metrics from reviewed literature | CRITICAL | S6–S9 |
| M3 | Inter-rater agreement not quantified | HIGH | S2.4 |
| M5 | Coding scheme produces no aggregated quantitative output | HIGH | S4 |
| M6 | Maturity matrix criteria undefined | HIGH | Table 3 |
| R2 | "Competitive" used without statistical basis | HIGH | S6–S9 |
| M4 | Level A/B/C distribution not reported | MEDIUM | S2.5 |
| R3 | UQ in reviewed studies not assessed | MEDIUM | S3.4, S6–S9 |
| R4 | Comparison table lacks methodology | MEDIUM | Table 4 |
| E1 | CNKI excluded despite Chinese emphasis | MEDIUM | S2.1 |
| E3 | No search completeness check reported | MEDIUM | S2.1 |
| E2 | arXiv criterion creates temporal bias | LOW | S2.1 |
| E4 | No sensitivity analysis on maturity matrix | LOW | S4.2 |

---

## SCORING

| Component | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| Methodology | 50% | 4/10 | 2.0 |
| Results | 30% | 3/10 | 0.9 |
| Experimental Design | 20% | 5/10 | 1.0 |
| **Total** | | | **3.9** |

**Score: 4/10**

The methodology section demonstrates awareness of scoping review best practices
(PRISMA-ScR, Arksey & O'Malley, coding scheme, validation levels) — the framework
is sound. The critical gap is that the framework has not produced quantitative
outputs: no study counts, no frequency distributions, no performance metrics, no
inter-rater agreement, no aggregated coding results. A scoping review that maps a
field must show the map in numbers, not just in words. The maturity matrix (Table 3)
is the paper's central analytical claim but lacks reproducible criteria and
traceability to underlying evidence.

The score rises to 6–7/10 if the Worker:
1. Adds actual PRISMA-ScR flow diagram counts
2. Reports the total number of included studies
3. Presents at least one summary table of coded study distributions
4. Reports representative performance metrics from Level A studies
5. Defines explicit maturity matrix thresholds
6. Reports inter-rater agreement on the verification subset

The score reaches 8+/10 if additionally:
- Performance metrics are presented in a structured comparison table
- Uncertainty quantification across the reviewed literature is assessed
- A search completeness check is reported

---

*"The null hypothesis is always: 'This claim is unsupported.' The burden falls on
the paper to reject that null. Currently, the paper asserts maturity levels and
competitive performance without the quantitative evidence needed to reject the null.
Show me the numbers." — Fisher's challenge to this manuscript.*
