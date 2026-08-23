---
name: how-to-work-agentic
description: Explain how a user can advance the Catskills micro-compound proposal with a repository-aware coding agent such as Codex or Claude Code. Use when the user asks how to work agentically, what to do next in this repository, how to delegate planning or proposal work, or how to structure an agent task. Do not use merely because an agent is already editing the repository.
---

# Work agentically on the compound proposal

Orient the user to a productive, verifiable collaboration with a repository-aware agent. When invoked only for guidance, explain and recommend; do not modify files unless the user also asks to begin a task.

## Orient to the current repository

1. Read `README.md`, `docs/PROJECT_STRUCTURE.md`, and `output/proposal.md`.
2. Check repository status and recent changes when available.
3. Identify the user's desired decision or outcome, not just a file operation.
4. Point to the exact source, proposal section, legal analysis, or tool involved.
5. Explain the smallest useful task, the evidence it needs, and how the result will be verified.

## Offer relevant workstreams

Tailor the menu instead of reciting every option. Useful patterns include:

- **Proposal development:** name the section folder, identify supporting sources, draft the change, run `python3 tools/build_proposal.py`, and run the `--check` form.
- **Layout change:** update authoritative geometry and procedural sources, regenerate fixed-camera crude/top-down evidence, inspect Stage 8 and affected stages, then update prose and higher-fidelity visuals.
- **Visual refinement:** select one accepted crude/intermediate image as the geometry lock, describe only allowed material/atmosphere changes, compare the result against the top-down plan, and save accepted output as a source.
- **Legal feasibility:** retrieve current official authority, archive it under `legal/sources/`, create dated and cited analysis under `legal/analysis/`, state uncertainty, and update the proposal only after reviewing the evidence.
- **Budget refresh:** define scope and location/date, collect comparable local inputs, record exclusions and confidence, update `07-budget` plus affected stage sections, and preserve prior numbers as history when useful.
- **Professional brief:** turn open issues into a compact packet for the Town, surveyor, septic/well professional, architect/engineer, insurer, or builder; include the relevant plan and a request for written answers.

## Give the user a strong task shape

Recommend prompts with four parts:

1. **Outcome:** the decision or artifact wanted.
2. **Constraints:** facts and relationships that must remain fixed.
3. **Evidence:** files or official sources the agent must use.
4. **Done condition:** build, visual, citation, or review checks required.

Example:

> Revise the Stage 4 bathhouse section so it supports a Town pre-application meeting. Preserve the accepted bathhouse orientation and dimensions. Use the current geometry, bathhouse plan, and legal analysis. Add unresolved questions rather than guessing. Rebuild the proposal and verify all links.

## Explain the collaboration loop

Set the expectation that the agent should inspect, propose or implement within scope, show evidence, verify, and hand off open decisions. Encourage small, reviewable iterations that preserve source history. For a broad goal, suggest beginning with one decision gate or one proposal section rather than requesting an unbounded redesign.

Finish with one recommended next prompt the user can send immediately. If the user already supplied a concrete goal, explain the approach briefly and offer to begin that exact task.

