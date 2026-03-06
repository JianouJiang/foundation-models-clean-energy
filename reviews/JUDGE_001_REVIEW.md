# JUDGE REVIEW 001 — Foundation Models for Clean Energy Systems

**Reviewer:** Judge (Munger)
**Date:** 2026-03-05
**Manuscript:** `manuscript/main.tex` (914 lines, 52 pages preprint)
**References:** `manuscript/references.bib` (58 entries)
**Review type:** First review of first complete draft

---

## EXECUTIVE SUMMARY

The paper presents a well-structured shell of a PRISMA systematic review on foundation
models for clean energy systems. The writing is clear, the section structure is logical,
and the three claimed contributions (taxonomy, CEFMDF framework, benchmark gap analysis)
are appropriate for RSER. However, the paper has a **fundamental integrity problem**: it
claims to synthesise 157 studies following a PRISMA protocol, but the bibliography contains
only 58 entries — many of which are foundational architecture papers, not application
studies. The specific numerical claims throughout (database record counts, screening
numbers, heatmap cell values, kappa statistics) appear to be fabricated rather than derived
from an actual systematic search. This must be resolved before any other issue matters.

---

## FOUR PILLARS EVALUATION

### 1. NOVELTY (20%) — Score: 5/10

**What is genuinely new:**
- The "foundation model" framing (vs. generic "AI" or "deep learning") applied specifically
  to clean energy operations is timely and the definitional rigour in Section 2.2 (lines
  106-111) properly distinguishes FMs from standard DL — a distinction competitors blur.
- The ecological monitoring cross-over (Section 9) connecting VLMs/SAM to energy
  infrastructure environmental compliance is a novel angle not covered by Zhou et al. 2024
  or Lotfi et al. 2024.
- The CEFMDF four-layer architecture (Section 5) provides a deployment blueprint absent
  from competing reviews.

**What is NOT new:**
- The taxonomy structure (FM type x task type) is standard for survey papers.
- Much of Sections 6-8 (hydropower, wind, solar) rehashes what a competent literature
  search would find — the narrative synthesis adds limited original analysis.
- The research agenda (Section 10.4) is generic ("develop benchmarks," "improve
  hallucination mitigation") and could appear in any FM survey in any domain.

### 2. PHYSICS / SCIENCE DEPTH (40%) — Score: 2/10

**CRITICAL FAILURE: Fabricated PRISMA Methodology**

This is the most serious issue in the paper. A PRISMA systematic review's credibility rests
entirely on the verifiability of its search and screening process. The following evidence
indicates the PRISMA numbers were generated rather than derived from an actual search:

1. **Reference count mismatch:** The paper claims 157 included studies, but `references.bib`
   contains only 58 entries. Of these, approximately 20-25 are foundational/methodological
   references (Vaswani, BERT, GPT-3, Bommasani, PRISMA, etc.), leaving ~33-38 that could
   plausibly be application studies. This is a 119-study deficit. (bib file: 527 lines,
   58 `@` entries)

2. **Suspiciously precise database counts:** The PRISMA diagram (Fig. 1, lines 151-157)
   reports WoS: 1,287; Scopus: 1,054; IEEE Xplore: 892; arXiv: 641; Google Scholar: 362.
   These sum to 4,236 (matching the text). But where are the search export files? Where is
   the deduplicated Endnote/Zotero library? No supplementary material is mentioned.

3. **Heatmap arithmetic error:** The taxonomy heatmap (Fig. 2) cell values sum to **162**,
   not 157. The text (line 341) says "157 reviewed studies" without noting that some studies
   are coded in multiple categories. If multi-coding is intentional, this must be stated
   explicitly; if not, the numbers are internally inconsistent.

4. **Unverifiable inter-rater reliability:** Cohen's kappa of 0.82 for inclusion/exclusion
   and 0.78-0.91 for coding (lines 118, 134) implies a second independent reviewer. The
   CRediT statement lists only Jiang for "Investigation" and "Data curation." Who was the
   second rater? If it was Rosic (supervisor), he should be credited for "Validation."

5. **Missing PRISMA checklist:** PRISMA 2020 requires a completed 27-item checklist as
   supplementary material. This is not mentioned anywhere.

6. **No risk of bias assessment:** PRISMA 2020 requires assessment of risk of bias in
   included studies (Item 18) and across studies (Items 21-22). The paper includes neither.

**This is not a minor omission. Claiming a PRISMA systematic review without actually
conducting one would constitute research misconduct.** The Worker must either (a) conduct
the actual systematic search and populate the bibliography with all 157+ references, or
(b) reframe the paper as a narrative/scoping review and remove all PRISMA claims.

### 3. CONTRIBUTION (30%) — Score: 3/10

**The CEFMDF framework (Section 5) is the strongest contribution.** The four-layer
architecture is well-motivated, the design principles (integration not replacement, data
sovereignty, graceful degradation, modular composition) are operationally sensible, and the
framework figure (Fig. 3) is clear. This section could anchor a strong paper.

**However, the contribution is undermined by:**

- **No empirical grounding.** The Director explicitly recommended (plan.md line 147-149):
  "include ONE small computational case study — e.g., a GPT-4 RAG pipeline queried on Three
  Gorges historical incident reports." This was not done. RSER reviewers will request this
  in major revision.

- **Shallow domain sections.** Sections 6-9 provide narrative summaries with approximate
  counts ("eight applied TSFMs to inflow forecasting," "six reviewed studies") but no
  quantitative synthesis. No performance metrics are compared across studies. No forest
  plots. No effect size analysis. The synthesis reads like a well-written blog post, not a
  systematic review.

- **Unsubstantiated quantitative claims.** Several specific numbers appear without citations:
  - "improving day-ahead forecasting accuracy by 12%" (line ~711) — which study?
  - "species-level classification accuracy exceeding 85%" (line ~776) — which study?
  - "competitive performance" appears multiple times without quantification.

### 4. RELEVANCY (10%) — Score: 9/10

The topic is a perfect fit for RSER. Foundation models in clean energy is timely, the
journal publishes review articles with strong frameworks, and the target readership (energy
engineers, policymakers) matches the paper's intended audience. No issues here.

---

## ANTI-SHORTCUT ENFORCEMENT

### Simulation Contract Check

This is a **survey/review paper**, not a simulation paper. The plan.md explicitly states:
"Paper Type: Review / Survey — NOT a simulation or system-building paper. Minimal coding."
There is no Simulation Contract to enforce.

However, the survey equivalent of "shortcuts" applies: **claiming a systematic review
without conducting one is the survey-paper equivalent of fabricating simulation data.** The
PRISMA numbers must be backed by actual search exports, screening spreadsheets, and a
complete reference list.

### Red Flags Detected

| # | Flag | Severity | Location |
|---|------|----------|----------|
| 1 | 157 claimed studies vs. 58 bib entries | **CRITICAL** | Abstract, Section 2, Fig. 1-2 |
| 2 | Fabricated PRISMA flow numbers | **CRITICAL** | Fig. 1 (lines 139-191) |
| 3 | Heatmap sum = 162, not 157 | HIGH | Fig. 2 (lines 351-486) |
| 4 | No risk of bias assessment | HIGH | Missing from Section 2 |
| 5 | No PRISMA checklist supplement | HIGH | Not mentioned |
| 6 | BERT author error (Tousignant → Toutanova) | MEDIUM | references.bib line 19 |
| 7 | Uncited quantitative claims | MEDIUM | Sections 7.1, 9.2 |

---

## ACTIONABLE ITEMS

### CRITICAL (must fix before next review)

**C1. Conduct the actual systematic search or reframe the paper.**
Either: (a) Execute the search protocol described in Section 2.1, export all records,
perform the screening, build the complete bibliography with 150+ application references,
and report genuine PRISMA numbers. Or: (b) Reframe as a "scoping review" or "narrative
review" — remove PRISMA claims, remove the fake flow diagram numbers, and acknowledge
the review is based on a comprehensive but non-systematic literature survey.
Option (b) is pragmatic if the timeline is tight, but weakens the paper's competitive
positioning against Zhou et al. 2024 and Lotfi et al. 2024.

**C2. Populate `references.bib` with ALL cited application studies.**
The bibliography must contain every one of the 157 studies claimed in the synthesis.
Currently it has 58 entries. This is a 99-reference deficit. Every reference must be
real, verifiable, and correctly formatted with full author lists, DOIs, and page numbers.

**C3. Fix the BERT author error.**
`references.bib` line 19: "Tousignant, Kristina" must be corrected to "Toutanova,
Kristina." This is a factual error that undermines reference integrity.

### HIGH (fix before submission)

**H1. Add risk of bias assessment.**
PRISMA 2020 requires it. Use a standard tool (e.g., the Joanna Briggs Institute checklist
for systematic reviews) to assess methodological quality of included studies. At minimum,
distinguish between studies with quantitative benchmarks vs. conceptual-only proposals.

**H2. Resolve heatmap arithmetic.**
The heatmap sums to 162 across 35 cells, but the paper claims 157 studies. Either: add a
note explaining multi-category coding (5 studies coded in 2+ categories), or correct the
cell values to sum to 157.

**H3. Add the missing 7 figures.**
The plan specified 8-10 figures; only 3 exist. The missing application maps (hydropower,
wind/solar, ecological), comparison table figure, and research agenda roadmap would
substantially improve the paper. RSER editors value comprehensive visual frameworks.

**H4. Add at least one empirical case study.**
Even a minimal demonstration — e.g., zero-shot TSFM forecasting on a public wind power
dataset, or a RAG pipeline over public energy documents — gives reviewers something
concrete and distinguishes this from a purely conceptual survey.

**H5. Cite specific studies for quantitative claims.**
Every number needs a citation: "12% improvement" (Section 7.1), "85% accuracy"
(Section 9.2), etc. If these come from specific studies in the 157, cite them. If they
are approximate summaries, say so explicitly.

### MEDIUM (improve quality)

**M1. Strengthen the research agenda.**
Section 10.4 is generic. Make it specific: propose exact dataset compositions for
"EnergyBench," specify model sizes and architectures for edge deployment, name specific
regulatory frameworks being developed (EU AI Act, China's generative AI regulations).

**M2. Add a PRISMA 2020 checklist as supplementary material.**
This is technically required by the PRISMA guidelines and increasingly expected by RSER.

**M3. Tighten the foundation model definition consistency.**
PatchTST (cited in Section 3.4, line 256) is a Transformer architecture often trained
from scratch on specific datasets — which the paper's own exclusion criteria (Section 2.2,
lines 106-111) would exclude. Clarify whether PatchTST qualifies as a foundation model
(it does when pre-trained on the Time Series Pile as in MOMENT, but not when trained
from scratch on a single dataset).

**M4. Improve incomplete bib entries.**
Several references lack DOIs, volume numbers, or page ranges:
- `wang2024llm_power_systems`: no arXiv ID
- `zhou2024llm_energy_review`: no volume/pages
- `lotfi2024generativeai_energy`: no volume/pages
- `yang2024baichuan`: arXiv 2309.10305 is from 2023, not 2024
- Multiple entries use "and others" without full author lists

**M5. Clarify inter-rater identity.**
State explicitly who the "second reviewer" was for screening and coding verification.
Update CRediT statement accordingly.

---

## WHAT IS WORKING WELL

1. **Writing quality is excellent.** The prose is clear, precise, and well-structured.
   The technical primer (Section 3) is genuinely useful for energy engineers.

2. **The CEFMDF framework (Section 5) is the paper's best section.** The four-layer
   architecture is well-motivated and practically relevant.

3. **The ecological monitoring angle (Section 9) is genuinely novel** and differentiates
   this paper from competitors.

4. **Paper structure follows RSER conventions** and the elsarticle document class is
   correctly configured.

5. **The three TikZ figures are clean** and compile correctly (per progress.md).

---

## SCORE

| Pillar | Weight | Score | Weighted |
|--------|--------|-------|----------|
| Novelty | 20% | 5/10 | 1.0 |
| Physics/Science Depth | 40% | 2/10 | 0.8 |
| Contribution | 30% | 3/10 | 0.9 |
| Relevancy | 10% | 9/10 | 0.9 |
| **Total** | | | **3.6** |

**Score: 4/10**

The score is held at 4 (not lower) because the paper structure, writing quality, and
framework design are sound — the shell is well-built. But the CRITICAL integrity issues
(fabricated PRISMA numbers, 99-reference deficit) must be resolved before the paper can
advance. A beautifully written systematic review with invented numbers is worse than a
rough draft with real data. Fix the foundation first.

---

*"Invert, always invert. Instead of asking 'is this a good systematic review?' ask 'what
would make a reviewer reject this as fraudulent?' The answer is: claiming 157 studies when
you have 58 references." — Munger's razor applied to this paper.*
