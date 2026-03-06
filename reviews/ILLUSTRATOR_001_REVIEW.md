# ILLUSTRATOR (Tufte) — Figure Quality & Data Visualization Review
**Project**: clean_energy_ai_foundation  
**Date**: 2026-03-06  
**Scope**: Review of *existing* figures in `manuscript/figures/` (do not penalize missing/in-progress figures).

## Update Note (state checked 2026-03-06 ~17:20)
- `manuscript/main.tex` now includes figures as **PDF** (vector) rather than PNG — good; do not regress.
- `pdffonts` spot-check on `manuscript/figures/*.pdf` shows **embedded CID TrueType fonts** (no Type 3 observed) — good; do not regress.
- New figure programmatic report regenerated at `manuscript/figure_report.md` timestamp **2026-03-06 16:36:53**; scores/flags below reflect this updated report (not the earlier run).
- Note: several figure PDFs/PNGs were regenerated later (**~17:12** by file mtime). Re-run the figure inspector/report after the latest regeneration so the scores/AI-lazy flags are strictly aligned with the current figure binaries.

## Constraints / Evidence Used
- I did **not** run `figure_inspector.py` because (a) it is not present in this repo root and (b) I am explicitly constrained to **not run scripts** in this role.
- I **did** use the existing programmatic report `manuscript/figure_report.md` plus code inspection of figure scripts in `codes/`.
- I could not perform a true “eyeball” inspection (text overlap, label collisions) in this environment; I instead flag *high-risk* spots from the scripts + automated metrics and request the Worker to confirm by visual check at print size.

## Must-Fix (Global) — Before Submission
1. **Correctness before aesthetics (Pareto)**: `fig_pareto_frontier` is explicitly flagged by JUDGE_002 as containing an **incorrect point** due to an integration bug. A pretty but wrong frontier is fatal — regenerate only after data integration is correct and re-validate labels/points against the table/text.
2. **Stop bar-charting paired comparisons**: several experiment/comparison figures still summarize *paired* outcomes (Direct vs RAG; model variants) with bars. This hides variance, confounds interpretation, and (per STATISTICIAN_002) can mask infrastructure artifacts (timeouts → zeros). Use paired plots + distributions.
3. **Uncertainty is missing in most figures**: where claims are quantitative (benchmarks, proportions), show uncertainty bands/intervals (bootstrap/Wilson) or at minimum annotate sample sizes and variability.
4. **Figure placement / overflow** (from USER REVIEW `reviews/USER_REVIEW_20260306_141841.md`): figures must appear **inline near first reference** and must **not overflow margins**. Several figures have very wide aspect ratios; ensure they remain legible at `\textwidth` in final PDF (9–11pt figure text).
5. **Do-not-regress (production hygiene)**: keep figures included as **PDF**, and keep **embedded TrueType/Type 1 fonts** (avoid Type 3).

## Programmatic Figure Inspector Summary (copied from `manuscript/figure_report.md`)
Image scores (PNG):
- `fig_publication_trend.png`: **6.0/10**
- `fig_geographic.png`: **5.0/10**
- `fig_domain_heatmap.png`: **7.0/10**
- `fig_taxonomy_heatmap.png`: **6.5/10**
- `fig_reproducibility.png`: **5.5/10**
- `fig_timeseries_benchmark.png`: **6.5/10**
- `fig_timeseries_predictions.png`: **8.0/10**
- `fig_llm_qa.png`: **5.5/10**
- `fig_vlm_inspection.png`: **5.5/10**
- `fig_rag_comparison.png`: **5.0/10**
- `fig_pareto_frontier.png`: **5.5/10**
- `fig_deployment_comparison.png`: **5.0/10**
- `fig_setup_effort.png`: **5.0/10**

Notable measured issues repeated across many figures:
- **Very high “white space”** (often ~70–97%): suggests plots are visually undersized relative to canvas or margins are too generous.
- `manuscript/figure_report.md` now reports **Total AI-lazy flags: 4** (down from earlier runs), but several key figures remain visually bar-dominant even when not flagged by the tool.
- Cross-check: `reviews/EDITOR_001_REVIEW.md` cites **6 AI-lazy flags**. Treat the *latest* `manuscript/figure_report.md` as source of truth once it is regenerated against the current figure files.

## Visual Language Consistency (Across All Figures)
**Good**:
- Centralized style exists: `codes/utils/plotting_utils.py` (serif font, 9–11pt ticks/labels, 300 dpi saving).
- Consistent palette (`pu.COLORS`) is used across most scripts.

**Needs tightening**:
- **Panel labels**: Current approach uses panel letters inside titles (e.g., `"(a) ..."`) rather than consistent corner-anchored labels. Titles vary in boldness and placement across scripts.
- **Gridlines**: `plotting_utils.py` enables `axes.grid=True` globally. For Tufte-style graphics, use gridlines sparingly and very lightly, or only on panels that truly need reference structure.
- **Legends vs direct labeling**: Many bar charts rely on legends; direct labeling is usually clearer and higher data-ink.

---

# Cross-Agent Outstanding Items (Figure Implications)
These are *not* stylistic quibbles; they affect what the figures are allowed to claim.

1. **Pareto frontier correctness (JUDGE_002)**: treat `fig_pareto_frontier` as *invalid until re-generated from corrected data*. After fix, label fewer points and directly label Pareto points only (avoid annotation clutter).
2. **RAG improvement figure integrity (STATISTICIAN_002)**: if timeouts produced zeros, bar summaries can silently exaggerate improvement. The figure should show *per-question paired deltas* and explicitly mark/omit timeout cases (or show a separate “failed queries” count).
3. **Publication growth story (STATISTICIAN_002)**: the growth curve is plausibly a **step-change post-2023**, not a single exponential regime. The figure should either (a) show two regimes / changepoint, or (b) annotate the fit window and show residuals so the viewer sees misfit.
4. **Incommensurate metrics (Pareto) (STATISTICIAN_002)**: mixing `1-nMAE`, `F1`, and “keyword match” as one “performance” axis is inherently approximate. A journal-quality graphic would separate modalities (small multiples) or add explicit caveats in-axis labeling.

# Per-Figure Review (existing files)

## 1) `fig_publication_trend` (Score 6.0/10) — Acceptable, but not yet “journal figure”
**What works**
- Two-panel story aligns with caption: exponential fit + stacked area by FM type.

**Issues / risks**
- Panel (a) uses **bars** + fit; bars are often too “thick” for time trends and waste ink.
- Missing explicit marking of the **fit window/regime** (2019–2025) on the plot itself (visual honesty).
- Per STATISTICIAN_002: the data likely reflects a **regime shift (post-2023 step-change)** rather than a single exponential. The figure must not visually “sell” a global exponential if the fit is window-sensitive.

**Upgrade suggestion**
- Switch panel (a) to a **line with point markers** + shaded fit band; add a vertical marker at 2023 (ChatGPT era) and either (a) fit only the post-2023 segment or (b) show two fits (pre vs post) with residual inset.

## 2) `fig_geographic` (Score 5.0/10) — **AI-lazy** (barh + grouped bars)
Current (`codes/figures/fig_geographic.py`) is a bar chart + grouped bar chart. A top reviewer will expect a geographic encoding.

**Required redesign (journal-quality)**: Choropleth + composition small multiples (30+ line outline)
```python
# Goal: (a) world choropleth of paper counts; (b) top countries composition by FM type
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.colors import Normalize
import matplotlib.cm as cm
import plotting_utils as pu

df = pd.read_csv("data/classified_papers.csv")

# --- Aggregate counts by country code ---
country_counts = (
    df["countries"].fillna("")
      .str.split("; ")
      .explode()
      .str.strip()
)
country_counts = country_counts[country_counts.ne("")]
counts = country_counts.value_counts().rename_axis("iso2").reset_index(name="n_papers")

# --- Load world geometry (Natural Earth) ---
world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
# Map iso2 -> iso3: you may need a lookup table; keep this explicit and audited.
iso2_to_iso3 = pd.read_csv("data/iso2_iso3_lookup.csv")  # Worker: create once
counts = counts.merge(iso2_to_iso3, on="iso2", how="left")
world = world.merge(counts, left_on="iso_a3", right_on="iso3", how="left")
world["n_papers"] = world["n_papers"].fillna(0)

# --- Figure layout ---
fig = plt.figure(figsize=(14, 6))
gs = GridSpec(1, 2, width_ratios=[1.35, 1.0], wspace=0.15)

# (a) Choropleth
ax_map = fig.add_subplot(gs[0, 0])
norm = Normalize(vmin=0, vmax=np.percentile(world["n_papers"], 95))
cmap = cm.get_cmap("viridis")  # perceptually uniform
world.plot(
    column="n_papers", ax=ax_map, cmap=cmap, norm=norm,
    linewidth=0.2, edgecolor="white"
)
ax_map.set_title("(a) Global FM+Energy publications (author affiliations)")
ax_map.set_axis_off()
sm = cm.ScalarMappable(norm=norm, cmap=cmap)
cb = fig.colorbar(sm, ax=ax_map, fraction=0.025, pad=0.01)
cb.set_label("Paper count")

# (b) Composition for top-K countries: 100% stacked bars
ax_comp = fig.add_subplot(gs[0, 1])
topK = counts.sort_values("n_papers", ascending=False).head(5)["iso2"].tolist()
fm_types = ["LLM", "TSFM", "VLM", "diffusion", "multimodal"]

rows = []
for cc in topK:
    mask_cc = df["countries"].fillna("").str.contains(cc, na=False)
    for fm in fm_types:
        mask_fm = df["fm_types"].fillna("").str.contains(fm, na=False)
        rows.append({"iso2": cc, "fm": fm, "n": int((mask_cc & mask_fm).sum())})
comp = pd.DataFrame(rows)
comp["pct"] = comp.groupby("iso2")["n"].transform(lambda s: s / max(s.sum(), 1))

pivot = comp.pivot(index="iso2", columns="fm", values="pct").fillna(0)
left = np.zeros(len(pivot))
palette = [pu.COLORS["primary"], pu.COLORS["secondary"], pu.COLORS["tertiary"],
           pu.COLORS["quaternary"], pu.COLORS["quinary"]]
for fm, color in zip(fm_types, palette):
    ax_comp.barh(pivot.index, pivot[fm], left=left, color=color, edgecolor="white", linewidth=0.3)
    left += pivot[fm].values
ax_comp.set_xlim(0, 1)
ax_comp.set_xlabel("Share of publications")
ax_comp.set_title("(b) FM-type portfolio (top countries)")
ax_comp.legend(fm_types, fontsize=8, frameon=False, loc="lower right")
ax_comp.grid(False)

pu.save_figure(fig, "fig_geographic")
```

## 3) `fig_domain_heatmap` (Score 7.0/10) — Solid, but improve inference density
Current is a single annotated heatmap with dashed red gap boxes.

**Recommendations**
- Add **marginal totals** (domain totals + FM totals) and/or **hierarchical clustering** ordering to reveal structure.
- Consider a second panel: **normalised** heatmap (row-wise %) to separate “volume” from “preference”.

## 4) `fig_taxonomy_heatmap` (Score 6.5/10) — Good base, but flagged “single-panel”
The heatmap is the right object; the issue is storytelling: it needs context and annotation.

**Upgrade suggestion**
- Make it a 2×1 composite: (a) raw counts (current), (b) row-normalised proportions, with callouts on the most important “gap” cells (not just red boxes everywhere).

## 5) `fig_reproducibility` (Score 5.5/10) — Important content; still too bar-forward
The latest `manuscript/figure_report.md` rates the *script* highly (uncertainty band present), but the *image* remains marginal — likely a scaling/whitespace/readability issue at print size.

**Required redesign (journal-quality)**: time trend + dot plot + bullet charts (30+ line outline)
```python
# Goal: (a) OA over time (line + uncertainty); (b) OA by FM type (Cleveland dot plot);
# (c) reproducibility metrics as bullet charts with benchmark targets.
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import plotting_utils as pu

with open("codes/results/reproducibility_audit.json") as f:
    data = json.load(f)

fig = plt.figure(figsize=(14, 5))
gs = GridSpec(1, 3, width_ratios=[1.2, 1.0, 1.4], wspace=0.25)

# (a) OA by year: show counts + Wilson CI on proportion (visual honesty)
ax0 = fig.add_subplot(gs[0, 0])
years = sorted(data["open_access"]["by_year"]["pct"].keys())
pct = np.array([data["open_access"]["by_year"]["pct"][y] for y in years]) / 100.0
n = np.array([data["open_access"]["by_year"]["count"][y] for y in years])

# Wilson interval (approx): Worker can compute precisely; plot band regardless
z = 1.96
phat = pct
den = 1 + z**2 / np.maximum(n, 1)
center = (phat + z**2/(2*np.maximum(n,1))) / den
half = (z*np.sqrt((phat*(1-phat) + z**2/(4*np.maximum(n,1))) / np.maximum(n,1))) / den
lo, hi = (center - half), (center + half)

ax0.plot(years, 100*pct, color=pu.COLORS["primary"], lw=2)
ax0.fill_between(years, 100*lo, 100*hi, color=pu.COLORS["primary"], alpha=0.2, linewidth=0)
ax0.axhline(data["open_access"]["open_access_pct"], color=pu.COLORS["secondary"], ls="--", lw=1)
ax0.set_title("(a) Open-access rate over time")
ax0.set_xlabel("Year"); ax0.set_ylabel("Open access (%)")
ax0.set_ylim(0, 100)
ax0.grid(False)

# (b) OA by FM type: dot plot (less ink than bars)
ax1 = fig.add_subplot(gs[0, 1])
fm = sorted(data["open_access"]["by_fm_type"]["pct"].keys())
fm_pct = np.array([data["open_access"]["by_fm_type"]["pct"][k] for k in fm])
y = np.arange(len(fm))
ax1.hlines(y, 0, fm_pct, color="0.85", lw=1)
ax1.plot(fm_pct, y, "o", color=pu.COLORS["tertiary"], ms=6)
for yy, vv in zip(y, fm_pct):
    ax1.text(vv + 1, yy, f"{vv:.0f}%", va="center", fontsize=8)
ax1.set_yticks(y); ax1.set_yticklabels(fm)
ax1.set_xlim(0, 100)
ax1.set_title("(b) Open access by FM type")
ax1.set_xlabel("Open access (%)")
ax1.grid(False)

# (c) Bullet charts for reproducibility components
ax2 = fig.add_subplot(gs[0, 2])
metrics = [
    ("Has DOI", data["doi"]["doi_pct"], 95),
    ("Open Access", data["open_access"]["open_access_pct"], 80),
    ("Code in Abstract", data["code_estimate"]["code_mention_pct"], 50),
    ("On Papers w/ Code", data["pwc_check"]["found_pct"], 50),
]
y2 = np.arange(len(metrics))[::-1]
for (label, val, target), yy in zip(metrics, y2):
    ax2.barh(yy, 100, color="0.93", height=0.55)               # background
    ax2.barh(yy, val, color=pu.COLORS["primary"], height=0.55)  # actual
    ax2.axvline(target, color=pu.COLORS["secondary"], lw=1, ls="--")
    ax2.text(val + 1, yy, f"{val:.1f}%", va="center", fontsize=8)
ax2.set_yticks(y2); ax2.set_yticklabels([m[0] for m in metrics])
ax2.set_xlim(0, 110)
ax2.set_title("(c) Reproducibility scorecard (bullet charts)")
ax2.set_xlabel("Percent (%)")
ax2.grid(False)

fig.suptitle(f"Reproducibility audit (n={data['open_access']['total_papers']:,}, index={data['reproducibility_index']:.2f})", y=1.02)
pu.save_figure(fig, "fig_reproducibility")
```

## 6) `fig_timeseries_predictions` (Score 8.0/10) — Best of the set, but needs journal polish
**Strength**
- This is the right idea: actual vs multiple model traces.

**Upgrade suggestions**
- Add a second (small) panel: **residuals** over time (or absolute error) + a **zoomed inset** of a difficult interval (peak/valley).
- Replace legend with **end-of-line labels** to reduce clutter.

## 7) `fig_llm_qa` (Score 5.5/10) — **AI-lazy** (barh + grouped bars)
The scientific question is comparative, paired, and distributional; bars hide that.
Per STATISTICIAN_002, infrastructure artifacts (timeouts → zeros) can make aggregate bar improvements meaningless unless failures are explicitly handled/visualized.

**Required redesign (journal-quality)**: paired per-question deltas + domain facets (30+ line outline)
```python
# Goal: show distributions and paired changes (Direct vs RAG) instead of bars.
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import seaborn as sns
import plotting_utils as pu

with open("codes/results/rag_pipeline.json") as f:
    rag = json.load(f)

# Worker: store per-question scores (domain, q_id, direct_score, rag_score, direct_ok, rag_ok)
qa = pd.read_csv("codes/results/qa_per_question_scores.csv")
qa["delta"] = qa["rag_score"] - qa["direct_score"]

fig = plt.figure(figsize=(14, 5))
gs = GridSpec(1, 3, width_ratios=[1.2, 1.2, 0.8], wspace=0.25)

# (a) Paired scatter: each question is a line (slopegraph)
ax0 = fig.add_subplot(gs[0, 0])
qa_sorted = qa.sort_values(["domain", "direct_score"])
for _, r in qa_sorted.iterrows():
    ax0.plot([0, 1], [r["direct_score"], r["rag_score"]],
             color="0.75", lw=0.8, zorder=1)
ax0.scatter(np.zeros(len(qa_sorted)), qa_sorted["direct_score"],
            s=14, color=pu.COLORS["octonary"], label="Direct", zorder=2)
ax0.scatter(np.ones(len(qa_sorted)), qa_sorted["rag_score"],
            s=14, color=pu.COLORS["primary"], label="RAG", zorder=2)
ax0.set_xticks([0, 1]); ax0.set_xticklabels(["Direct", "RAG"])
ax0.set_ylim(0, 1)
ax0.set_title("(a) Per-question paired scores")
ax0.set_ylabel("Keyword match score")
ax0.legend(frameon=False, fontsize=8, loc="lower right")
ax0.grid(False)

# (b) Domain-wise distributions: violin + swarm (data-rich)
ax1 = fig.add_subplot(gs[0, 1])
long = pd.concat([
    qa.assign(method="Direct", score=qa["direct_score"])[["domain", "method", "score"]],
    qa.assign(method="RAG", score=qa["rag_score"])[["domain", "method", "score"]],
])
sns.violinplot(data=long, x="domain", y="score", hue="method",
               split=True, inner="quartile", ax=ax1,
               palette=[pu.COLORS["octonary"], pu.COLORS["primary"]], cut=0)
ax1.set_title("(b) Score distributions by domain")
ax1.set_xlabel("Domain"); ax1.set_ylabel("Score")
ax1.set_ylim(0, 1)
ax1.tick_params(axis="x", rotation=25)
ax1.legend(frameon=False, fontsize=8, loc="lower right")
ax1.grid(False)

# (c) Improvement distribution (delta): histogram + rug (or KDE)
ax2 = fig.add_subplot(gs[0, 2])
ax2.axvline(0, color="0.5", lw=1)
ax2.hist(qa["delta"], bins=12, color=pu.COLORS["secondary"], alpha=0.75, edgecolor="white")
ax2.set_title("(c) RAG − Direct")
ax2.set_xlabel("Δ score")
ax2.set_ylabel("Questions")
ax2.grid(False)

fig.suptitle("LLM energy Q&A: paired effects and distributions (avoid bar-chart summaries)", y=1.02)
pu.save_figure(fig, "fig_llm_qa")
```

## 8) `fig_vlm_inspection` (Score 5.5/10) — Mixed: one good panel, one bar-summary panel
**Good**
- Confusion matrix panel is appropriate (though ensure numbers remain readable at print size).

**Weak**
- Accuracy/F1 as grouped bars is low information density.

**Upgrade suggestion**
- Replace bars with: (a) **precision–recall points** for variants, or (b) distribution of CLIP similarity scores with **ROC operating points**, plus confusion matrix as (b).

## 9) `fig_rag_comparison` (Score 5.0/10) — Borderline AI-lazy summary
Grouped bars hide question-level variance and paired nature.
Per STATISTICIAN_002, report the count of **failed/time-out queries** separately (or exclude with clear rule) so the viewer can see whether “improvement” is driven by missing baseline responses.

**Upgrade suggestion**
- Use the same paired + distribution approach proposed for `fig_llm_qa`, but applied to the 15-question subset; emphasize *grounding* (e.g., citations present/absent) as an additional visual channel.

## 10) `fig_pareto_frontier` (Score 5.5/10) — Borderline; fix correctness + readability
The idea is correct (log-cost vs performance), but current labeling likely creates clutter and contributes to “white space” warnings.
Per JUDGE_002, the current frontier is also **numerically wrong** due to a baseline/integration bug; treat any present graphic as provisional until re-generated from corrected inputs.

Also per STATISTICIAN_002: the y-axis collapses **incommensurate metrics** (1−nMAE, F1, keyword score). If kept, make the approximation explicit, or switch to small multiples by task/modality.

**Upgrade suggestion (30+ line outline)**: label only Pareto points + add iso-setup contours
```python
# Goal: reduce annotation clutter, emphasize the frontier, and encode setup effort as color.
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import plotting_utils as pu

strategies = load_strategies_somehow()  # Worker: existing pipeline output
xs = np.array([s["compute_tflops"] for s in strategies if s["performance"] > 0])
ys = np.array([s["performance"] for s in strategies if s["performance"] > 0])
setup = np.array([s["setup_hours"] for s in strategies if s["performance"] > 0])
is_pareto = np.array([bool(s.get("pareto_optimal")) for s in strategies if s["performance"] > 0])
labels = [f'{s["model"]} ({s["strategy"]})' for s in strategies if s["performance"] > 0]

fig, ax = plt.subplots(figsize=(10, 6))
norm = Normalize(vmin=np.min(setup), vmax=np.max(setup))
cmap = cm.get_cmap("plasma")

ax.scatter(xs, ys, c=setup, cmap=cmap, norm=norm, s=60,
           edgecolors="0.3", linewidths=0.5, alpha=0.85)

# Emphasize Pareto points
ax.scatter(xs[is_pareto], ys[is_pareto], facecolors="none",
           edgecolors="black", linewidths=2, s=120, zorder=5)

# Frontier polyline
pareto_pts = sorted([(x, y, lab) for x, y, lab, p in zip(xs, ys, labels, is_pareto) if p], key=lambda t: t[0])
if len(pareto_pts) >= 2:
    px, py, _ = zip(*pareto_pts)
    ax.plot(px, py, color="black", ls="--", lw=1.5, alpha=0.7)

# Label only Pareto points (direct labels), with collision-avoid heuristics
for i, (x, y, lab) in enumerate(pareto_pts):
    ax.text(x*1.03, y + (0.01 if i % 2 == 0 else -0.015), lab,
            fontsize=8, ha="left", va="center")

ax.set_xscale("log")
ax.set_xlabel("Compute cost (relative TFLOPS, log scale)")
ax.set_ylabel("Performance (normalized)")
ax.set_ylim(0, 1.05)
ax.grid(False)
cb = fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, fraction=0.03, pad=0.02)
cb.set_label("Setup effort (hours)")
ax.set_title("Deployment strategies: Pareto frontier (color = setup effort)")

pu.save_figure(fig, "fig_pareto_frontier")
```

## 11) `fig_deployment_comparison` (Score 5.0/10) — Borderline AI-lazy (barh across tasks)
Replace with a higher-density comparison:
- per-task **dot plots** with confidence intervals (or bootstrapped variability),
- and/or a **parallel coordinates** view across multiple metrics (performance, cost, setup hours, labeled data).

## 12) `fig_setup_effort` (Score 5.0/10) — Acceptable, but integrate with Pareto story
Bubble charts are fine, but current design likely duplicates the Pareto frontier narrative.
Suggestion: merge into a single 2×1 figure: top = Pareto (color=setup), bottom = setup vs performance (size=labeled data), with consistent labeling scheme.

---

## Anti-Patterns Found (Flagged)
- **AI-lazy figures**: heavy use of `ax.bar` / `ax.barh` where paired effects or distributions are central (`fig_geographic`, `fig_llm_qa`, `fig_rag_comparison`, `fig_reproducibility`, parts of `fig_vlm_inspection`, `fig_deployment_comparison`).
- **Over-annotation risk**: widespread `ax.text(...)` on bars; likely overlap at print scale.
- **High whitespace** warnings across many exported images: tighten layouts and scale plot elements to fill canvas.

## Requested Worker Checks (Quick Visual QA)
- Print to PDF and check each figure at final size: **no text overlap**, tick labels readable, legends not covering data.
- Confirm that panel labels (a,b,…) are consistent in position, font size, and weight across the entire paper.
- Confirm figures do not exceed margins and appear inline (per user review).
- Validate **figure-to-claim integrity**: (a) Pareto points match the underlying table/results; (b) RAG vs Direct comparisons explicitly handle timeouts/failures; (c) publication-growth plot is honest about fit window/regime shift.
- Re-check `pdffonts` on a few key figure PDFs before submission to ensure fonts remain embedded (avoid accidental Type 3 regressions).

## Score
Score: 6/10
