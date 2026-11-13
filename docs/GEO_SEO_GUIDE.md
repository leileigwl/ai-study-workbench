# Open-Source SEO & GEO (Generative Engine Optimization) Playbook

This guide explains why `ai-study-workbench` is structured the way it is—and the exact steps to complete when pushing the repository to GitHub so both traditional search engines (**SEO**) and AI answer engines like ChatGPT Search, Perplexity, Claude, and Google AI Overviews (**GEO**) discover and cite it.

---

## 1. GEO Architecture Built Into This Repository

AI search engines prioritize sources with **verifiable definitions, structured comparison tables, unique terminology, clear Q&A anchors, and machine-readable sitemaps (`llms.txt`)**:

1. **Quotable Canonical Definition (Top 100 Words)**: `README.md` opens with a crisp, self-contained definition of *Socratic Workbench*, the *"1+3" multi-domain learning architecture*, and the *4-Slot Pseudocode Compilation* pattern.
2. **Structured Comparison Matrix**: Explicit Markdown table comparing *Passive AI Chat* vs *Traditional Flashcards* vs *Socratic Workbench (`socratic-workbench`)* on quantifiable attributes (spoiler isolation, logic vs syntax split, model-drift resistance).
3. **`llms.txt` & `llms-full.txt`**: Follows the open `llmstxt.org` specification so LLM crawlers ingest canonical links and architectural definitions cleanly without HTML noise.
4. **`CITATION.cff`**: Machine-readable citation metadata parsed natively by GitHub ("Cite this repository") and research crawlers.
5. **FAQ Section**: Written as natural-language search queries ("How do you stop AI from spoiling answers while studying?", "Can you learn coding concepts with AI without memorizing syntax?", "Does this work with Flash or smaller models?").

---

## 2. GitHub Publishing Checklist (Complete When Ready to Push)

- **Recommended Repository Name**: `ai-study-workbench`
- **Repository Description (Under 160 chars, keyword-rich)**:
  > Anti-spoiler AI study coach & Skill ("1+3" architecture): dual-file blind recall + 4-slot pseudocode compiler for Antigravity, Claude Code, Cursor & Web LLMs.
- **Recommended GitHub Topics (Copy-Paste All 10–14)**:
  `ai-tutor` `agent-skills` `active-recall` `socratic-method` `claude-code` `cursor-rules` `antigravity` `prompt-engineering` `pseudocode` `system-design` `interview-prep` `study-tools` `spaced-repetition` `llms-txt`
- **Social Preview Banner**: Upload a clean 1280x640 architecture diagram showing `workbench.md (Blind)` vs `answer_key.md (Hidden)` + `4-Slot Pseudocode -> Tests`.
- **Replace Placeholder URLs**: Once pushed to `https://github.com/<your-handle>/ai-study-workbench`, update placeholder `<your-handle>` links in `README.md`, `README.zh-CN.md`, and `CITATION.cff`.
