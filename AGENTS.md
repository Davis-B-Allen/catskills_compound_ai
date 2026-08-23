# Repository instructions for agents

Read `README.md` and `docs/PROJECT_STRUCTURE.md` before making project-wide changes.

## Deliverable contract

- Treat `output/proposal.md` as generated output. Edit `proposal/sections/*/section.md`, then run `python3 tools/build_proposal.py`.
- Run `python3 tools/build_proposal.py --check` before handing off proposal changes.
- Keep section folders lexically ordered. Use `{{repo:path/from/repository/root}}` for repository assets and links.
- Do not silently convert uncertain assumptions into facts. Label estimates, design intent, open questions, and professional-verification needs.

## Geometry and imagery

- Treat `sources/data/cameras-and-geometry.json` and the current procedural model sources as authoritative.
- Preserve +X east, +Z north, +Y up, units in feet, and the accepted final horizontal mirror for both top-down and perspective images.
- Validate layout changes in geometry-driven renders before requesting photorealistic refinement.
- Treat photorealistic images as visual intent, not dimensional evidence.

## Legal research

- Keep downloaded authorities in `legal/sources/` and generated interpretation in `legal/analysis/`.
- Record source URL, publisher, retrieval date, effective/amendment date when known, and page/section citations.
- Prefer official municipal, county, and New York State sources. Clearly label secondary sources.
- Research current law before changing a legal conclusion; archived material can become stale.
- State that analysis is planning research, not legal advice or an approval.

## Preservation

- Do not overwrite original models, prior proposals, or accepted images merely to improve organization.
- Put superseded but historically useful material under `sources/project-history/` or `sources/prior-proposals/`.
- Preserve unrelated user changes in a dirty worktree.

