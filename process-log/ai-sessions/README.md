# AI Session Logs

This directory documents the AI tools used throughout the research process.

## Tool Used

- **Claude** (Anthropic, Claude Opus 4) via Claude Code CLI
- Used for: literature synthesis, code generation, figure scripting, LaTeX drafting, data analysis pipeline development

## Session Summary

The paper was produced using Claude Code as an interactive research assistant. The human author (Jianou Jiang) directed all research decisions, defined the scope, selected methodologies, and reviewed all outputs. Claude assisted with:

1. **Literature search and synthesis** — drafting search strings, summarising papers, building the taxonomy table
2. **Code development** — writing Python scripts for bibliometric analysis, benchmark experiments, and figure generation
3. **Manuscript drafting** — generating LaTeX sections under human direction, with iterative review and revision
4. **Data processing** — OpenAlex API queries, paper classification pipeline, statistical analysis

## How to Access Full Logs

The complete interaction history is available in the Claude Code session logs stored locally during development. Due to the volume of conversational data (hundreds of exchanges over multiple sessions), representative excerpts are provided below rather than full transcripts.

## Key Decision Points Where AI Output Was Overridden or Modified

1. Claude initially proposed including nuclear energy in scope — human decision to exclude (see `human-decisions/decisions.md`)
2. Claude suggested using GPT-4 API for Q&A benchmark — changed to local Qwen2.5 via Ollama for reproducibility
3. Claude proposed more aggressive claims about FM superiority — human moderated language throughout
4. Taxonomy maturity ratings were reviewed and adjusted by the human author based on domain expertise
5. CEFMDF architecture layers were debated across multiple iterations before finalising the four-layer design
