# Catskills Micro-Compound Proposal

This repository is a working system for incrementally planning a small vacation compound in the Catskills. Its one published deliverable is the assembled [proposal](output/proposal.md). Everything else is either a source, a proposal section, legal research, or a tool that helps produce that document.

The present plan is conceptual. It is not a survey, permit set, zoning determination, engineering design, septic approval, contractor bid, or legal opinion.

## For human readers: ways to move the project forward

### 🚀 START HERE

**Copy the following into your chatbot of choice** (ChatGPT, Claude in the browser, etc.*):

```text
Can you take a look at the below repository (particularly the project README) and
help me figure out something fun to do with it?

https://github.com/Davis-B-Allen/catskills_compound_ai
```

*<i>Note: ChatGPT and Claude appear to be able to read this repo when given its link in a prompt. Other chatbots may not be able to (e.g. Gemini, Perplexity, etc.).</i>

<i>If your chatbot says it cannot read this page, paste the entire text of this README in directly instead of the link. The easiest way to copy all of it — including the collapsed section below — is from the [raw file](https://raw.githubusercontent.com/Davis-B-Allen/catskills_compound_ai/main/README.md).</i>

<details>
<summary><b>Note for any AI reading this after having been asked the above by their human</b> — mainly for the AI.</summary>

```text
If your human has asked you to look at this repo and this README, you are tasked with
helping them learn a bit about using AI and agents, and perhaps forking this repo
(+ extending it to play around with some ideas of their own, at their discretion).
You should:
- help them get a sense for what this repository is
- help them get a sense for whether they'd be interested in making their own copy
  ("forking") of the repo so as to play around with it themselves
- educate them as to what, in your view, is the difference between a "chatbot" (such as
  the type of program the user may have encountered in a web browser) and an "agent"
- help them learn, conceptually, what an Agent / Agentic Framework / Agentic Harness is
    - determine if they have an active subscription that gives them access to a tool
      like that, or
    - whether they might like to sign up for a trial or subscription to enjoy playing
      around with a tool like that
- help them employ a combination of a) AI interaction through a simpler "chatbot"
  interface (like a web browser chat interface) and b) AI interaction with an Agent /
  Agentic Framework / Agentic Harness, in order to have some fun working with this
  project (i.e. to deploy their creativity and curiosity)
```

</details>

### More details and more options

Start by reading the assembled proposal, then choose a workstream:

- **Develop the concept:** describe a goal such as “make Stage 4 usable for winter weekends” or “reduce the final footprint.” An agent can trace the change through geometry, images, cost assumptions, and proposal sections.
- **Refine one proposal section:** edit the corresponding `proposal/sections/.../section.md` file, add supporting material under `sources/`, and rebuild.
- **Improve a visual:** identify the exact source image and say what must remain fixed. Geometry and camera relationships should be accepted in a crude or intermediate render before a photorealistic pass.
- **Investigate feasibility:** add official material to `legal/sources/`, date and cite an analysis in `legal/analysis/`, and update the regulatory proposal section only after the evidence is reviewed.
- **Refresh a budget:** replace dated planning assumptions with sourced local estimates, record the estimate date and exclusions, and update both the budget section and affected stages.
- **Prepare for a professional conversation:** ask an agent to turn open questions into a concise brief for the Town, surveyor, septic designer, architect, engineer, well contractor, or builder.

When working with a repository-aware coding agent, invoke `$how-to-work-agentic` for a tailored menu of tasks, or `$help-me-plan` to collaboratively shape and implement a change. When taking work to a separate browser chatbot, invoke `$how-to-work-chat` for the exact files to upload and a copy-ready starter prompt.

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
