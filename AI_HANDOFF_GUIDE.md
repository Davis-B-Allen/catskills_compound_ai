# Catskills Compound — AI Agent Handoff Guide

## 1. Purpose

This package captures the accepted geometry, staging, camera system, rendering pipeline, and reference stills for a conceptual Catskills woodland compound. A future AI agent should be able to:

- resume the exact staged model;
- make small layout changes while preserving dimensional consistency;
- move windows/doors or adjust a building footprint;
- select a new camera and create a spatially faithful reference render;
- regenerate the identical top-down stage sequence;
- regenerate or refine the intermediate render sequence;
- use the crude/intermediate renders as constrained underlays for later photorealistic rendering.

The central principle is **geometry first, imagery second**. Do not allow an image-generation model to invent site geometry.

---

## 2. Files to treat as authoritative

### Crude/master site model

`01_crude_site_model/Catskills_Compound_Master_3D_Model_appblock_v13.html`

This is the final accepted interactive Three.js/App Block source at the point of handoff. It contains:

- all master site coordinates;
- stage visibility logic;
- deck polygons;
- building dimensions;
- bathhouse orientation;
- hot-tub/cold-plunge positions;
- top-down camera;
- eight accepted stage-specific perspective cameras;
- the display mirroring convention.

`01_crude_site_model/master_model_spec.json` and root `CAMERAS_AND_GEOMETRY.json` restate the important values in a tool-neutral form.

### Intermediate renderer

`02_intermediate_renderer/render_intermediate_stages.py`

This is the deterministic VTK/Python rendering pipeline used for the accepted "intermediate 3D render" approach. It reconstructs the same site geometry using more architectural detail, including roof seams, facade battens, glazing, simple interiors, procedural deck/ground/gravel textures, simple lighting, and stage-specific camera positions.

The procedural textures are included under `02_intermediate_renderer/textures/` and are reproducible because the script uses `random.seed(7)`.

### Convenience 3D exports

- `01_crude_site_model/crude_master_compound.glb`
- `02_intermediate_renderer/intermediate_master_compound.glb`

These are convenience exports for Blender/three.js/CAD inspection. Node names include stage prefixes. The procedural sources and JSON remain authoritative because the staged visibility logic, facade details, and some rendering-only elements are richer there.

---

## 3. Coordinate system and the orientation trap

### Source site coordinates

- +X = east
- +Z = north
- +Y = vertical/up
- units = feet

The original positive-coordinate site is translated by:

- X: -56.5 ft
- Z: -49.0 ft

so the final compound is centered around world origin for stable cameras.

### Critical display convention

The accepted browser model and still renders apply a **horizontal image mirror after rendering**.

This was necessary because the raw 3D camera basis and the desired architectural plan convention originally disagreed. The user explicitly validated the following relationship:

> If an observer stands in the firepit courtyard looking toward the bathhouse, the hot tub must appear on the same side of the bathhouse in both the top-down plan and the 3D perspective.

Therefore:

1. build and aim the camera in normal world coordinates;
2. render;
3. horizontally mirror the final raster/canvas display;
4. do this for **both** top-down and perspective images.

Do not "fix" east/west by changing geometry unless the human driver asks for an actual site-layout change.

---

## 4. Accepted final site geometry

All coordinates below are uncentered site coordinates in feet. See `CAMERAS_AND_GEOMETRY.json` for machine-readable data.

### Main tiny home — Stage 1

- footprint: 24 × 20 ft = 480 sf
- southwest/source origin: X=40, Z=72
- wall height: 8.5 ft
- gable roof rise: 2.7 ft
- principal courtyard-facing facade is on its south side

### Bathhouse — Stage 4

- footprint: 16 × 16 ft = 256 sf
- origin: X=14, Z=38
- wall height: 8 ft
- roof rise: 2.7 ft
- **courtyard-facing facade is the EAST wall**
- sauna glazing occupies the **northern portion** of that east wall
- the southern portion of that east wall corresponds to the shower zone and remains solid

This orientation must not be silently rotated. The 16-ft bathhouse plan and cutaway are included in `06_bathhouse_reference/`.

### ADU — Stage 6

- footprint: 22 × 20 ft = 440 sf
- origin: X=52, Z=10
- wall height: 8.2 ft
- roof rise: 2.7 ft
- deliberately similar in overall size to the 480-sf main tiny home
- located south/east of the firepit but set back far enough that its deck does not intrude into the firepit pad

### Guest sleeping cabin — Stage 7

- footprint: 16 × 12 ft = 192 sf
- origin: X=31, Z=12
- wall height: 7.7 ft
- roof rise: 2.7 ft
- located between the bathhouse and ADU, slightly west of the ADU

### Outdoor kitchen/bar — Stage 8

- pavilion footprint: approximately 18 × 16 ft
- origin: X=81, Z=41
- post/eave height: ~8 ft
- roof rise: 2.7 ft
- **open/front bar face points west, inward toward the firepit courtyard**

---

## 5. Firepit and spa geometry

### Firepit — Stage 3

- center: X=54, Z=50
- flat gravel pad radius: 10.5 ft
- stone fire-ring major radius: ~2.15 ft
- no sunken landscaping; site is intentionally relatively flat

The firepit was moved during iteration to read as centrally as practical among the surrounding buildings.

### Firepit seating — Stage 5

Six simple chairs/benches are placed around the firepit at angles:

15°, 70°, 125°, 195°, 250°, 310°

The exact furniture design is conceptual; the radial placement is the important site relationship.

### Cold plunge — Stage 5

- rectangular small plunge
- X=31.3, Z=39
- 4.2 × 5 ft footprint
- on the bathhouse deck
- immediately east of the southern/shower portion of the bathhouse east wall
- must not obstruct the sauna glazing

### Wood-fired hot tub — Stage 5

- center: X=25.5, Z=34.6
- outer radius: 3.25 ft
- height: 1.65 ft
- positioned south and slightly west of the cold plunge
- overlaps the bathhouse in east-west dimension
- sits on / is integrated with the bathhouse deck

The bathhouse deck must **envelop the bathhouse and both tubs**.

---

## 6. Deck logic

The user rejected fragmented, zig-zagging deck components. The accepted intent is:

- clean straight edges;
- broad, obvious connections;
- no hairline joins;
- no gaps between supposedly connected deck phases;
- by Stage 8 the deck reads as **one contiguous circulation system surrounding/enclosing the central firepit courtyard**;
- future-oriented geometry in earlier stages is acceptable if it produces cleaner later joins.

Deck construction is defined procedurally as additive polygons, then rendered as a **union of all deck polygons present by the current stage**. This is important: rendering separate coplanar pieces can cause seams/z-fighting. The intermediate renderer intentionally unions the polygons before creating the deck mesh.

The exact polygons are in `CAMERAS_AND_GEOMETRY.json` and the source scripts.

Stage additions:

- Stage 2: main-home courtyard deck
- Stage 4: bathhouse wrap/platform + wide main-house connection
- Stage 6: ADU platform + broad south deck band
- Stage 7: guest-cabin platform filling the southwest part of that band
- Stage 8: outdoor-kitchen platform + broad east connector, closing the circulation system

---

## 7. Staging

The development sequence is cumulative:

1. **Principal tiny home** only
2. Add **main courtyard deck**
3. Add **flat gravel firepit + stone fire ring**
4. Add **16×16 bathhouse + bathhouse wrap/connecting deck**
5. Add **firepit seating + cold plunge + wood-fired hot tub**
6. Add **440-sf ADU + south deck connection**
7. Add **guest sleeping cabin + deck**
8. Add **covered outdoor kitchen/bar + final deck connection**

Do not introduce later-stage objects in earlier stages.

---

## 8. Top-down camera — must remain identical for all stages

The user spent substantial iteration establishing this. Do not auto-frame each stage separately.

Use one fixed true direct-overhead orthographic camera for every stage:

- camera position: `(0, 120, 0)`
- target: `(0, 0, 0)`
- view-up: `(0, 0, 1)`
- projection: orthographic
- Three.js bounds: left=-56, right=56, top=50, bottom=-50
- VTK parallel scale: 50 with 1120×1000 output
- render the **same full final-compound frame** at all eight stages
- horizontally mirror the displayed/final image

The only thing that changes between the eight top-down images is component visibility.

This is what makes objects appear to "pop in" from stage to stage without the camera moving.

---

## 9. Accepted perspective cameras

All values are in the centered world coordinate system (after subtracting 56.5 from site X and 49 from site Z). View-up is `(0,1,0)`. Output reference size is 1600×1000. Horizontally mirror the final image.

| Stage | Camera position | Target | FOV | Intended composition |
|---|---|---|---:|---|
| 1 | (-4, 16.79, 1.28) | (-4, 2, 33) | 44° | South/courtyard approach; establishes main house |
| 2 | (-4, 20.07, -5.99) | (-4, 2, 28) | 45° | New main deck in foreground against house |
| 3 | (23.83, 29.46, -30.73) | (-2, 2, 14) | 46° | Firepit emphasized with home/deck context |
| 4 | (23.83, 33.45, -33.83) | (-18, 2, 8) | 48° | Bathhouse and connection in courtyard context |
| 5 | (25.99, 35.14, -46.99) | (-20, 2, -1) | 48° | Spa tubs + firepit seating + bathhouse |
| 6 | (32.65, 42.80, -71.55) | (0, 2, -15) | 50° | ADU from rear, with compound context |
| 7 | (-8, 28, -70) | (-8, 2, -15) | 58° | Guest cabin from front; ADU one side, bathhouse/tubs other side |
| 8 | (-74, 30, -8) | (18, 2, 1) | 58° | Looking toward courtyard-facing open kitchen/bar front |

These are accepted reference views, not immutable design rules. If a human asks for a new viewpoint, adjust the camera while keeping model coordinates unchanged.

### Camera-change workflow

When asked for a new perspective:

1. keep the master geometry fixed;
2. select a camera position/target that emphasizes the requested element;
3. render the crude model first;
4. visually check for clipping, mirror/orientation errors, and whether contextual structures appear on the expected sides;
5. only after the crude view is accepted, render the intermediate or photorealistic version with the exact same camera;
6. preserve the horizontal-display mirror convention.

---

## 10. Crude model rendering

The crude model is intentionally simple. Its purpose is spatial verification, not beauty.

`01_crude_site_model/render_crude_reference_stills.py` provides a reproducible VTK implementation using the accepted geometry and cameras. It creates:

- eight fixed top-down images;
- eight fixed crude perspective images.

Colors are deliberately simple:

- dark building masses;
- near-black roofs;
- tan/orange deck;
- teal water;
- gray stone/gravel;
- simple green perimeter trees.

### Why static reconstructed references are included

The accepted Three.js images originally existed as runtime canvas renders inside the interactive App Block, not as separate persistent PNG files. The package therefore includes **static re-renders from the accepted current geometry and camera definitions** rather than stale screenshots from earlier, superseded model iterations. The App Block source is also included so the original interactive implementation remains available.

---

## 11. Intermediate renderer

The intermediate renderer was adopted after AI image generation repeatedly changed geometry. It is deterministic and geometry-driven.

Pipeline:

1. reconstruct exact accepted site coordinates in VTK;
2. show/hide actors by stage;
3. union all deck polygons present at that stage into a clean deck surface;
4. add actual sloping gable-roof planes rather than a flat roof block;
5. add standing-seam roof ribs;
6. add vertical siding battens;
7. add facade glazing/doors;
8. add simplified sauna benches/heater behind bathhouse glass;
9. use procedural ground/deck/gravel textures;
10. add architectural lights;
11. use the accepted stage camera;
12. render at 1600×1000;
13. horizontally flip the image to the accepted orientation;
14. apply only subtle contrast/color/brightness grading.

### Intermediate design language

The intended shared architectural language is:

- modern-rustic / Scandinavian-Catskills;
- near-black / charred vertical wood siding;
- dark matte standing-seam metal gable roofs;
- black/dark window frames;
- warm cedar-toned decking;
- warm amber interior illumination;
- subdued natural gravel/woodland ground;
- restrained, relatively flat site work;
- coniferous woodland context.

The intermediate renderer is not a final visualization engine. Vegetation is geometric, glass is simplified, global illumination is approximate, and interiors are schematic. Its purpose is to preserve geometry while creating a better underlay for photorealistic work.

---

## 12. Lighting used by the intermediate renderer

The VTK script uses a small architectural-lighting rig rather than physically exact daylight simulation.

### Global lights

**Warm sun / key**

- position: approximately `(-55, 75, 60)`
- focal point: origin
- color: warm `(1.0, 0.72, 0.48)`
- intensity: ~2.0

**Cool fill**

- position: approximately `(55, 45, -55)`
- focal point: origin
- color: cool `(0.52, 0.68, 0.82)`
- intensity: ~0.8

**Ambient/top fill**

- position: `(0, 60, 0)`
- color: neutral `(0.75, 0.78, 0.75)`
- intensity: ~0.55

### Local warm lights

Simple warm point/positional lights are associated with:

- main-home glazing;
- bathhouse sauna glazing;
- ADU/guest glazing;
- firepit;
- outdoor kitchen.

The purpose is legibility and warm/cool architectural contrast, not exact photometry.

---

## 13. Materials and textures

Procedural texture generation lives in `render_intermediate_stages.py`.

- `random.seed(7)` ensures reproducibility.
- `deck.jpg`: warm wood plank/grain texture with dark joints.
- `ground.jpg`: mottled woodland/grass/soil approximation.
- `gravel.jpg`: randomized aggregate texture.

PBR-ish VTK material settings are used for:

- siding: very dark, high roughness;
- roofing: very dark, lower roughness, modest metallic response;
- cedar/wood: warm brown, high roughness;
- stone: neutral gray, high roughness;
- metal: dark, modest metallic response;
- water: desaturated teal, low roughness;
- glazing: dark/translucent plus warm emissive interior proxy surfaces.

If moving to Blender/Cycles, preserve the color/material intent but upgrade to physically based materials and true glass rather than copying VTK numerical parameters literally.

---

## 14. Bathhouse-specific constraints

The bathhouse has had the most iteration and should not be casually redesigned.

Reference assets are under `06_bathhouse_reference/`.

Core external/site facts:

- 16 × 16 ft footprint;
- sauna and shower share the northern portion of the floor plan;
- the site orientation was chosen so the sauna/shower exterior wall faces into the firepit courtyard;
- on the courtyard-facing east wall, sauna glazing is toward the north; the shower portion toward the south is solid;
- cold plunge is outside that solid shower portion;
- hot tub is south/southwest of the cold plunge;
- bathhouse deck wraps the structure and both tubs;
- bathhouse main entry is on the opposite/south side, with decking continuing around to it.

Interior 16-ft plan references include sauna, shower, soaking tub, vanity, toilet, service zone and south entry. The cutaway is conceptual but useful for preserving the established spatial intent.

---

## 15. Recommended workflow for future edits

### A. Layout edit

Example: "move the ADU 3 ft east and 2 ft north."

1. modify the coordinates in the authoritative model source and JSON;
2. move all ADU-specific facade geometry with the building;
3. revise its deck polygon(s) to maintain clean contiguous connections;
4. check clearance against firepit and outdoor kitchen;
5. regenerate all eight top-down views with the **same fixed top-down camera**;
6. compare Stage 8 before/after first;
7. regenerate affected perspective/intermediate stages only after geometry is accepted.

### B. Window/door edit

Example: "move guest-cabin door to east side."

1. footprint stays fixed;
2. modify only facade aperture/details in both procedural renderers;
3. do not move the camera automatically;
4. regenerate the relevant crude perspective;
5. then regenerate the intermediate render.

### C. New perspective

1. leave all geometry untouched;
2. work from a crude block render;
3. inspect which side each contextual object appears on;
4. explicitly check the bathhouse/hot-tub side test described above;
5. lock camera coordinates and FOV;
6. reuse those exact values in the intermediate/final renderer.

### D. High-fidelity photorealistic pass

Do **not** ask an image model to independently recreate the compound from prose.

Preferred sequence:

1. render a spatially exact crude perspective;
2. render the deterministic intermediate perspective from the same camera;
3. use that intermediate image as the edit/paint-over target;
4. instruct the image renderer to preserve every silhouette, horizon, camera, building outline, deck edge, and object position;
5. alter only surface detail, realistic vegetation, glass, interiors, atmospheric light and material quality;
6. compare the photorealistic result against both the intermediate image and top-down plan before accepting it.

If the image model changes roof type, moves a building, invents a deck, or swaps east/west relationships, reject and rerun.

---

## 16. Known technical pitfalls

### 1. Mirroring mismatch

This was a real failure mode. Top-down and perspective images must share the same final horizontal mirror treatment.

### 2. Auto-framing each top-down stage

Do not do this. It destroys the incremental visual comparison. Use one fixed final-compound orthographic frame.

### 3. Coplanar deck pieces / z-fighting

Separate deck slabs can visually clip or flicker. Union stage deck polygons before meshing/rendering.

### 4. Camera validation by numbers alone

The project previously suffered from mathematically plausible camera settings that rendered incorrectly in the client. Always inspect the actual output raster. The user's target for top-down is a true direct-overhead bird's-eye view with the whole compound in frame.

### 5. Image-generation geometry drift

Generative renderers repeatedly turned rectangular one-story buildings into taller cabins/A-frames, moved tubs, and changed site relationships. Use them only after a geometry-faithful underlay is locked.

### 6. Bathhouse facade direction

Keep the accepted site orientation: courtyard-facing east facade, sauna glazing on the northern part. Do not revert to an older north-facing assumption from earlier conversation iterations.

---

## 17. Reproduction commands

### Crude reference stills

From a Python environment with VTK, Pillow and Shapely:

```bash
python 01_crude_site_model/render_crude_reference_stills.py
```

Set `CATSKILLS_CRUDE_OUT` if you want a custom output directory.

### Intermediate stills

```bash
python 02_intermediate_renderer/render_intermediate_stages.py
```

The packaged `render_intermediate_stages.py` is made portable: by default it writes to a `generated_intermediate/` folder beside the script, or to the directory named by `CATSKILLS_INTERMEDIATE_OUT`. The untouched original working source is also included as `render_intermediate_stages_original_working_source.py`.

Recommended dependencies:

- Python 3.11+
- VTK
- Pillow
- Shapely

The convenience GLB files can be inspected in Blender without those Python dependencies.

---

## 18. Reference image directories

- `03_top_down_stage_images/` — fixed-camera Stage 1–8 plan-like renders
- `04_crude_perspective_stage_images/` — Stage 1–8 rough geometry/camera references
- `05_intermediate_stage_images/` — Stage 1–8 deterministic intermediate renders accepted as the next layer of visual fidelity
- `06_bathhouse_reference/` — latest 16×16 plan/cutaway context
- `07_reference_context/` — earlier proposal PDF for project-history context; do not use its superseded site geometry in preference to the current model

---

## 19. Priority order when sources disagree

If a future agent sees contradictory information, use this order:

1. explicit new human direction;
2. current `CAMERAS_AND_GEOMETRY.json` + current procedural model source;
3. current top-down Stage 8 image;
4. current crude perspective stage image;
5. current intermediate stage image;
6. bathhouse Rev 5 plan/cutaway for bathhouse-internal details;
7. earlier proposal PDF or older imagery.

Older proposal renders and image-generation experiments contain superseded geometry and should be treated as aesthetic/context references only.

---

## 20. Final design intent summary

The end state is a relatively flat woodland compound organized around a central firepit courtyard:

- main 480-sf tiny home to the north;
- 16×16 bathhouse to the west/northwest side of courtyard;
- cold plunge and wood-fired hot tub integrated with its deck;
- ~440-sf full ADU to the south/east;
- smaller guest sleeping cabin between bathhouse and ADU;
- covered open-air kitchen/bar on the east side, open toward the courtyard;
- one clean, continuous deck circulation network tying the buildings together while enclosing the firepit area;
- dark modern-rustic buildings, warm wood deck, matte black roofs and a Catskills coniferous setting.

The model is conceptual architectural planning, not construction documentation. Dimensional fidelity is intentional at the site-plan/model level, but code, structural, civil, septic, utility, grading, and permit design require professional verification.
