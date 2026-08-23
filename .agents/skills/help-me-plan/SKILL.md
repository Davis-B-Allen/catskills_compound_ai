---
name: help-me-plan
description: Collaboratively develop and implement a proposed change to the Catskills micro-compound plan or proposal through an interactive, evidence-based workflow. Use when the owner wants help shaping a design, phasing, feasibility, budget, visual, or proposal change; do not use for a narrowly specified edit that needs no discovery.
---

# Plan a change together

Help the owner turn an idea into a reviewed, documented update to this repository. The user may invoke this skill with a brief hint, such as “make Stage 4 work better in winter” or “reduce the final footprint.” Treat that hint as a starting point for discovery, not as permission to choose consequential design assumptions.

Do not modify project files solely because this skill was invoked. First establish what the owner wants to decide or change, then implement only the direction they approve.

## Begin the conversation

Read `README.md`, `docs/PROJECT_STRUCTURE.md`, and `output/proposal.md`. Check the working-tree status before making changes and preserve unrelated user changes.

If the user supplied an intention, restate it briefly in terms of the decision it would support. Ask only the smallest set of questions needed to identify:

- the desired outcome and why it matters;
- what must remain fixed and what may change;
- the preferred tradeoffs, such as cost, capacity, phasing, comfort, complexity, or permitting risk; and
- any deadline, budget, site, or professional input that constrains the work.

If no usable intention was supplied, begin by asking: “What would you like to change or decide about the compound plan or proposal?” Follow with targeted questions after the owner responds; do not overwhelm them with a broad questionnaire.

## Turn the idea into a change brief

Inspect only the sources relevant to the owner's response. State a compact change brief before implementing: outcome, fixed constraints, options or recommendation, affected artifacts, evidence still needed, and the proposed done condition. Distinguish established facts from design intent, estimates, assumptions, and open questions.

For a meaningful choice, offer a small number of legible alternatives and explain their main tradeoffs. Ask for a decision when the choice would materially change the layout, program, cost, legal exposure, or irreversible work. Do not silently resolve it.

## Implement the approved direction

Apply the repository's source precedence and authoring rules throughout.

- **Proposal-only change:** edit the affected `proposal/sections/*/section.md` files, not `output/proposal.md`; trace changed shared facts into every dependent section.
- **Layout or staging change:** update the authoritative geometry and procedural model sources first. Preserve +X east, +Z north, +Y up, feet, fixed camera framing, and the accepted horizontal mirror. Regenerate and inspect affected geometry-driven images before changing proposal prose or requesting visual refinement.
- **Visual change:** use an accepted crude or intermediate image as the geometry lock. Restrict the change to approved material, landscape, atmosphere, furnishing, or detail changes unless the owner has approved a geometry change. Keep accepted sources and save new candidates with descriptive names.
- **Legal or permit change:** research current official authority before revising conclusions. Archive authorities in `legal/sources/`; record dated, cited interpretation in `legal/analysis/`; identify uncertainty and professional or agency confirmation needs. State that this is planning research, not legal advice or an approval.
- **Budget or phasing change:** record scope, location/date, comparable inputs, exclusions, confidence, and assumptions. Preserve useful prior figures as history rather than overwriting their provenance.

Pause for owner direction whenever new evidence reveals a material conflict with their stated vision or an unresolved choice with consequential tradeoffs.

## Finish cleanly

Before handoff, make the repository internally consistent:

1. Confirm each changed conclusion is reflected in every affected proposal section, source, render, budget, and legal analysis.
2. Keep original and accepted evidence; move historically useful superseded material under `sources/project-history/` or `sources/prior-proposals/` when appropriate rather than deleting it.
3. Update concise repository documentation when the workflow, source authority, or use of a reusable asset has changed. Do not add documentation merely to narrate an ordinary edit.
4. Run `python3 tools/build_proposal.py` and `python3 tools/build_proposal.py --check` for proposal changes. Run the relevant render or source validation for geometry/image changes and inspect the output.
5. Review the final diff for unrelated edits, unresolved repository references, and claims that present uncertain information as fact.

Hand off with: the owner's approved decision, what changed and why, evidence used, verification performed, and clearly labeled remaining questions or professional confirmations.
