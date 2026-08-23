# Catskills Micro-Compound Proposal

This repository is a working system for incrementally planning a small vacation compound in the Catskills. Its one published deliverable is the assembled [proposal](output/proposal.md). Everything else is either a source, a proposal section, legal research, or a tool that helps produce that document.

The present plan is conceptual. It is not a survey, permit set, zoning determination, engineering design, septic approval, contractor bid, or legal opinion.

## For human readers: ways to move the project forward

Start by reading the assembled proposal, then choose a workstream:

- **Develop the concept:** describe a goal such as “make Stage 4 usable for winter weekends” or “reduce the final footprint.” An agent can trace the change through geometry, images, cost assumptions, and proposal sections.
- **Refine one proposal section:** edit the corresponding `proposal/sections/.../section.md` file, add supporting material under `sources/`, and rebuild.
- **Improve a visual:** identify the exact source image and say what must remain fixed. Geometry and camera relationships should be accepted in a crude or intermediate render before a photorealistic pass.
- **Investigate feasibility:** add official material to `legal/sources/`, date and cite an analysis in `legal/analysis/`, and update the regulatory proposal section only after the evidence is reviewed.
- **Refresh a budget:** replace dated planning assumptions with sourced local estimates, record the estimate date and exclusions, and update both the budget section and affected stages.
- **Prepare for a professional conversation:** ask an agent to turn open questions into a concise brief for the Town, surveyor, septic designer, architect, engineer, well contractor, or builder.

When working with a repository-aware coding agent, invoke `$how-to-work-agentic` for a tailored menu of tasks. When taking work to a separate browser chatbot, invoke `$how-to-work-chat` for the exact files to upload and a copy-ready starter prompt.

## Repository map

```text
.
├── README.md                     Human starting point
├── AGENTS.md                     Standing instructions for repository agents
├── docs/PROJECT_STRUCTURE.md     Detailed source and authoring guide
├── sources/                      Models, images, data, and prior-proposal evidence
├── proposal/sections/            Ordered, editable proposal sections
├── legal/
│   ├── sources/                  Archived authorities and reference material
│   └── analysis/                 Dated, cited agent analysis
├── .agents/skills/               Repository-local collaboration skills
├── tools/build_proposal.py       Deterministic Markdown assembler
└── output/proposal.md            The single generated deliverable
```

See [Project structure and authoring guide](docs/PROJECT_STRUCTURE.md) for source precedence, image conventions, legal-research rules, and section syntax.

## Build the proposal

Requires Python 3.10 or later and no third-party packages.

```bash
python3 tools/build_proposal.py
python3 tools/build_proposal.py --check
```

The first command assembles every `proposal/sections/*/section.md` file in lexical order into `output/proposal.md`. The second verifies that the checked-in output is current and that all `{{repo:...}}` references resolve.

Edit section files, not `output/proposal.md`; the output is overwritten on the next build.

## Source authority

When project materials disagree, use this order:

1. explicit new direction from the owner;
2. `sources/data/cameras-and-geometry.json` and current procedural model sources;
3. accepted top-down, crude-perspective, and intermediate renders;
4. bathhouse plan references for bathhouse interior intent;
5. photorealistic renders for atmosphere and materials only;
6. prior proposal PDFs and legacy handoff documents for history.

For law and regulation, an official, current source outranks analysis, summaries, private websites, and prior proposal language. Confirm consequential interpretations with the authority having jurisdiction and qualified professionals.

