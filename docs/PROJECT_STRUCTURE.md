# Project structure and authoring guide

## Purpose

The repository converts many small, inspectable source artifacts into one long-form Markdown proposal. The proposal is intentionally modular: each page-like section can be developed independently, reviewed with its supporting sources, and assembled deterministically.

## Content layers

### 1. Sources

`sources/` contains evidence and design inputs. Sources are not automatically copied into the proposal; proposal sections cite or embed them.

- `sources/models/crude-site-model/` — accepted interactive/procedural site model, tool-neutral model specification, convenience GLB, and crude still renderer.
- `sources/models/intermediate-renderer/` — deterministic architectural renderer, textures, tool-neutral specification, and convenience GLB.
- `sources/images/stages/top-down/` — fixed-camera Stage 1–8 plan-like renders.
- `sources/images/stages/crude-perspective/` — geometry and camera-checking renders.
- `sources/images/stages/intermediate/` — deterministic higher-detail renders.
- `sources/images/stages/high-fidelity/` — photorealistic intent images; never use these to overrule geometry.
- `sources/images/bathhouse/` — the current bathhouse plan, SVG, and conceptual cutaway.
- `sources/data/` — machine-readable geometry and camera data.
- `sources/prior-proposals/` — previous assembled proposals used as historical and editorial context.
- `sources/project-history/` — legacy handoff documents and other superseded explanations.
- `sources/manifests/` — historical or current integrity manifests.

New material should have a stable, descriptive filename. Prefer lowercase hyphenated names except where retaining an original source filename is important. Keep accepted inputs; place experimental or regenerated output in a clearly named subfolder until the owner accepts it.

### 2. Legal sources and analysis

`legal/sources/` stores copies of official laws, regulations, code books, permit packets, and government guidance. `legal/analysis/` stores dated project-specific interpretation.

Never blend these layers. A source is evidence; an analysis is a revisable conclusion. Every legal analysis should identify the authority, citation, retrieval date, uncertainty, impact on this concept, and the person or agency who should confirm it.

The model-code link supplied with the original project points to the generic 2021 IRC. New York’s currently effective state code must be checked first; comparison text is not itself a determination of governing law.

### 3. Proposal sections

Each folder under `proposal/sections/` represents one page or coherent section and contains a `section.md`. Folder names begin with a two-digit order key. A section may also contain notes or local working assets, but reusable evidence belongs under `sources/` or `legal/`.

Use ordinary Markdown plus this repository-reference token:

```markdown
![Stage 8 plan]({{repo:sources/images/stages/top-down/stage_08_topdown.png}})

See the [zoning analysis]({{repo:legal/analysis/01-hardenburgh-zoning.md}}).
```

The builder resolves each token relative to the generated output file and fails if the target is missing or escapes the repository. The title section uses the document’s only level-one heading; subsequent sections begin with level-two headings.

### 4. Generated output

`output/proposal.md` is the sole assembled deliverable. It is committed so a human can read the proposal without installing tooling, but it should never be edited directly.

## Building and checking

From the repository root:

```bash
python3 tools/build_proposal.py
python3 tools/build_proposal.py --check
```

The builder:

1. discovers section folders in lexical order;
2. validates each `{{repo:...}}` target;
3. rewrites repository references for `output/proposal.md`;
4. inserts section boundaries and a generated-file warning;
5. writes the assembled document or checks it for drift.

## Authoring workflow

1. State the decision or reader question the section must support.
2. Identify authoritative design, visual, legal, and cost inputs.
3. Add or update sources before writing conclusions.
4. Edit only the affected section files; trace shared facts into every dependent section.
5. Build and check the proposal.
6. Review image links, headings, unresolved assumptions, and legal citations in the assembled output.

## Model and image conventions

The source coordinate system uses +X east, +Z north, +Y up, in feet. Accepted top-down and perspective images are horizontally mirrored after rendering so the displayed architectural convention is north up and east right. Apply the mirror consistently to both image families.

Use one fixed overhead camera across all stages. Stage visibility changes; framing does not. Preserve the accepted site geometry unless the owner requests a layout change. For new photorealistic work, lock the geometry and camera in a crude/intermediate render first, then modify materials, vegetation, atmosphere, and fine detail.

The accepted overhead camera is orthographic at `(0, 120, 0)`, targets the origin, uses view-up `(0, 0, 1)`, and renders the same final-compound frame at every stage. Perspective camera positions, targets, fields of view, site translations, deck polygons, and component coordinates are machine-readable in `sources/data/cameras-and-geometry.json`.

Deck phases are additive polygons rendered as a union for each stage. Do not render separate coplanar pieces where they can create seams or z-fighting. Preserve broad connections, straight edges, and the final continuous courtyard circulation system.

The bathhouse keeps its accepted 16 x 16 ft footprint and site orientation: its east sauna/shower facade faces the courtyard; glazing is on the northern portion; the southern shower-side portion is solid; the plunge is immediately east of that wall; and the hot tub is south and slightly west. The plan/cutaway controls interior intent, while the site geometry controls exterior placement.

### Reproduce geometry-driven images

Install the requirements listed beside each renderer, then run from the repository root:

```bash
python3 sources/models/crude-site-model/render_crude_reference_stills.py
python3 sources/models/intermediate-renderer/render_intermediate_stages.py
```

By default, new renders go to `sources/images/generated/crude/` and `sources/images/generated/intermediate/`. Override those paths with `CATSKILLS_CRUDE_OUT` and `CATSKILLS_INTERMEDIATE_OUT`. Review generated files before promoting them into an accepted stage-image folder.

The GLB files are convenience exports for inspection in Blender or other 3D tools. They do not supersede the procedural sources or geometry JSON, which contain richer stage, facade, camera, and display behavior.

### Common failure modes

- Mirroring only one image family and reversing the plan/perspective relationship.
- Auto-framing each stage and destroying incremental comparison.
- Moving geometry to compensate for a display-orientation problem.
- Allowing an image generator to change footprints, roof types, deck edges, tubs, or contextual left/right relationships.
- Treating a plausible camera number as accepted without inspecting the raster.
- Rotating the bathhouse back to a superseded facade direction.

## Source conflicts

For design conflicts, follow the priority order in `README.md`. For legal conflicts, prefer the current official text and record the discrepancy. For example, the posted Hardenburgh zoning law and its permit application show different setback numbers; this repository treats that as an unresolved confirmation item.

## Collaboration paths

- Repository-aware work: invoke `$how-to-work-agentic` or open `.agents/skills/how-to-work-agentic/SKILL.md`.
- Interactive change planning: invoke `$help-me-plan` or open `.agents/skills/help-me-plan/SKILL.md`.
- Separate web chat: invoke `$how-to-work-chat` or open `.agents/skills/how-to-work-chat/SKILL.md`.
- Human-only editing: change the relevant section, keep source links explicit, and run the two build commands.
