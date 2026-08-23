# Catskills Compound — AI Handoff Package

This archive is intended to let a future AI agent continue the site-model and rendering work without reconstructing the project from conversation history.

Start with **AI_HANDOFF_GUIDE.md**, then inspect **CAMERAS_AND_GEOMETRY.json**.

The procedural source files are the authoritative model definitions:

- `01_crude_site_model/Catskills_Compound_Master_3D_Model_appblock_v13.html` — accepted browser/Three.js staged site model.
- `01_crude_site_model/render_crude_reference_stills.py` — static VTK reconstruction of that accepted model for reproducible top-down and crude perspective stills.
- `02_intermediate_renderer/render_intermediate_stages.py` — deterministic VTK intermediate renderer used for the nicer Stage 1–8 reference images.

The `.glb` files are convenience exports for inspection/import into a conventional 3D application. They are **not more authoritative than the procedural sources and geometry JSON**.

Important orientation convention: source site coordinates use **+X east, +Z north, +Y up**. Both accepted top-down and perspective images are horizontally mirrored after rendering so that the displayed architectural convention is **north up, east right**. Never mirror only one family of images.
