# Roadmap & Revisit Checkpoint (Personal Reminder)

> **Checkpoint Note for the Author**:  
> Right now, `ai-study-workbench` cleanly ships as an open-source, domain-neutral **Skill Package + Multi-Domain Template Repo** (`v1.0.0-draft`), ready for publication or further evolution *after* you finish your current systems-architecture study sprint.

---

## Revisit Reminder (After Finishing Your Current Study Sprint)

Once you complete your active learning sprint and interviews, revisit this repository for three high-ROI upgrades:

1. **Plug In Real Before/After Case Evidence**:
   - Add anonymized quantitative metrics from your sprint (e.g., total units completed, average pseudocode compile iterations from fail -> green tests, interview recall speed improvement).
   - Optionally showcase sanitized lesson patterns (or keep `examples/` strictly neutral with 1–2 richer real-world scenarios).
2. **Evolve Packaging Format (`Skill -> Plugin / CLI`)**:
   - Add a `plugin.json` manifest if targeting Antigravity/Claude plugin marketplaces directly.
   - Expand `scripts/init_workbench.py` into an installable Python/Node CLI (`pipx` / `npx ai-study-workbench`) that can batch-parse arbitrary Markdown syllabi or textbook TOCs into `workbench.md` + `answer_key.md` skeletons.
3. **Execute Pre-Publish GitHub SEO & GEO Checklist**:
   - Replace `<your-handle>` placeholders in `README.md`, `README.zh-CN.md`, and `CITATION.cff`.
   - Set GitHub Topics listed in `docs/GEO_SEO_GUIDE.md` and run `python3 skills/socratic-workbench/scripts/init_workbench.py --check` on every example folder before tagging `v1.0.0`.
