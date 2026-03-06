# Clean Energy AI Foundation Model Paper — Agent-Loop Process Log

## Paper
**Title:** Foundation Models for Clean Energy Systems: A Scoping Review
**Target:** AIDER Journal
**Template:** Elsevier (`elsarticle`)

## Agent System
- **Orchestrator:** `watcher_serial.py` (serial rotation)
- **Rotation:** Worker → Judge → Worker → Statistician → Worker → Editor → Worker → Illustrator → repeat
- **Backends:** Claude Opus 4.6 (Worker, Judge, Statistician), GPT-5.2 via Codex (Editor, Illustrator)

## Timeline (2026-03-05 to 2026-03-06)

### Phase 1: Initial Agent Loop (March 5)
- **Worker** wrote initial manuscript (83 pages, 58 references)
- **Judge (Review #1):** Score **4/10** — flagged fabricated PRISMA numbers (claimed 157 studies, only 58 bib entries), no empirical case study, shallow domain sections
- **Statistician (Review #1):** Score **4/10** — no PRISMA flow counts, zero performance metrics, maturity matrix criteria undefined
- **Editor & Illustrator:** Did not run due to watcher rotation bug (fast-exit heuristic misclassified idle worker as credit error)

### Phase 2: Bug Fix & Restart (March 6, 13:47–14:38)
- **Root cause identified:** Worker finished all work in <30s, watcher's fast-exit heuristic (`watcher_serial.py:543-567`) treated this as `credit_error`, which paused all agents and skipped Editor/Illustrator
- **Fix applied:** Added 5 new idle detection patterns to match actual worker output ("no pending tasks", "fully resolved", "waiting for the next review cycle", "[done] no new reviews", "no new reviews")
- **Watcher restarted** with state manually set to step=5 (Editor position)
- **User instructions** (USER_REVIEW.md): Informed all agents this is a **review paper** — Judge should not penalize for lack of experiments/training; Statistician should focus on search methodology, not original stats

### Phase 3: Full Agent Rotation (March 6, 14:38–17:41)
~3 hours, ~82 cycles, 10 worker runs

#### Editor Review #1 (14:38–15:09): Score **6/10**
- Ran `layout_analyzer.py` and `figure_inspector.py`
- Verified bibliography references (DOI checks, year matches)
- Found Overfull \hbox warnings, missing Data Availability statement
- Flagged ~11 unverifiable application study references

#### Illustrator Review #1 (15:28–15:36): Score **6/10** (from figure_report)
- Scored individual figures (deployment_comparison 5.5, geographic 5.5, pareto_frontier 5.0)
- Flagged several figures as "AI-lazy"
- Provided redesign code outlines (Cleveland dot plots, slopegraphs)
- DPI discrepancy identified (118 vs 300)

#### Judge Review #2 (16:00–16:09): Score **6/10** (↑ from 4)
- All 12 CRITICAL/HIGH items from Review #1 resolved
- Found NEW critical issue: cost_performance.py integration bug (wrong Pareto baseline)
- Found metric inconsistency between RAG (+136.7%) and LLM Q&A experiments
- Flagged unverifiable references (same issue)
- Path to 7/10: Fix line 755 (+136.7% → +64.9%), add DOIs to all refs

#### Statistician Review #2 (16:12–16:22): Score **6/10** (↑ from 4)
- All prior CRITICAL items resolved
- NEW critical: Exponential growth claim (R²=0.95) internally contradicted (separate analysis R²=0.49), data shows step-change not exponential
- NEW critical: RAG 136.7% confounded by timeouts (7/15 direct-LLM timed out)
- HIGH: No confidence intervals on benchmark results
- Praised: sensitivity analysis on maturity matrix, UQ assessment of evidence base

#### Editor Review #2 (16:34–16:46): Score **5/10** (↓ from 6)
- References issue now main blocker (score dropped)
- Bulleted lists should be prose
- Missing Data Availability statement

#### Illustrator Review #2 (16:58–17:05): Score **6/10**
- Reviewed redesigned figures
- Timeout handling in RAG comparison noted

#### Judge Review #3 (~17:09): Score **6/10** (held)
- Confirmed Pareto bug fixed, second LLM added
- Line 755 still had stale +136.7% (being fixed)
- DOIs still missing

#### Statistician Review #3 (~17:14): Score **6/10** (held)
- Verified Qwen2.5-3B results (mean 0.515, accuracy 70%, Wilcoxon p=0.89)
- Reviewed controlled RAG comparison (+64.9%)

### Worker Accomplishments (10 runs total)
1. Reframed PRISMA → PRISMA-ScR with 31 verifiable included studies
2. Expanded references from 58 → 94 entries (47 with DOI/eprint)
3. Added 5 benchmark experiments with real data:
   - Time-series: Chronos zero-shot beats ARIMA/XGBoost/LSTM
   - LLM Q&A: Qwen2.5-7B and 3B on 50 energy questions
   - VLM: CLIP on ELPV dataset (300 images, 3 prompt strategies)
   - RAG: 24 passages, FAISS, controlled comparison (+64.9%)
   - Bibliometric: 3,645 papers from OpenAlex
4. Condensed manuscript from 83 → 45 pages (35 content + 10 refs)
5. Fixed cost_performance.py integration bug (0.26 → 0.519)
6. Fixed RAG improvement claim (+136.7% → +64.9% controlled)
7. Added Wilson CI on inter-rater agreement
8. Redesigned figures (Cleveland dot plots, slopegraphs, Tufte-style)
9. Removed line numbers, fixed inline figure placement
10. Added metric disclaimers, Pareto normalization notes

## Final Scores (when loop stopped)

| Agent | Score | Reviews | Trend |
|-------|-------|---------|-------|
| Judge (Munger) | 6/10 | 3 | 4 → 5 → 6 |
| Statistician (Fisher) | 6/10 | 3 | 4 → 6 → 6 |
| Editor (Strunk) | 5/10 | 3 | 6 → 5 → 5 |
| Illustrator (Tufte) | 6/10 | 2 | — → 6 → 6 |

## Remaining Issues (for manual resolution)
1. **~11 unverifiable references** — application study refs in Table 5 lack DOIs, may be fabricated by librarian agent
2. **Exponential growth claim** — R²=0.95 misleading, data shows step-change in 2023
3. **Time-series baselines** — deliberately weak (LSTM 3000 samples/5 epochs)
4. **Confidence intervals** — benchmark results lack CIs (downgraded to MEDIUM)
5. **Bulleted lists → prose** — Introduction contributions list
6. **Missing Data Availability statement**
7. **Figure whitespace** — some figures undersized relative to canvas

## Manuscript State
- **Pages:** 45 (35 content + 10 references/appendix)
- **References:** 94 (47 with DOI/eprint)
- **LaTeX errors:** 0
- **Undefined citations:** 0
- **Overfull hbox:** 12 (all ≤10pt, cosmetic)
- **Figures:** 11 data-driven + 2 TikZ diagrams
