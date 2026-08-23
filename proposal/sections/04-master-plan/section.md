## Master plan and spatial logic

![Stage 8 dimension-controlled top-down plan]({{repo:sources/images/stages/top-down/stage_08_topdown.png}})

The current master geometry uses source coordinates in feet: +X east, +Z north, and +Y up. The displayed top-down and perspective images receive the same final horizontal mirror so the architectural view reads north up and east right.

| Element | Footprint / key location | Courtyard relationship |
|---|---|---|
| Principal home | 24 x 20 ft; source origin X=40, Z=72 | North edge; principal facade faces south |
| Firepit | Center X=54, Z=50; 10.5 ft gravel radius | Fixed center of the outdoor room |
| Bathhouse | 16 x 16 ft; origin X=14, Z=38 | West; east facade faces inward |
| Cold plunge | 4.2 x 5 ft; X=31.3, Z=39 | Immediately east of shower-side bathhouse wall |
| Hot tub | Center X=25.5, Z=34.6; radius 3.25 ft | South and slightly west of plunge |
| ADU | 22 x 20 ft; origin X=52, Z=10 | South-east, clear of firepit pad |
| Guest cabin | 16 x 12 ft; origin X=31, Z=12 | Between bathhouse and ADU |
| Outdoor kitchen | Approx. 18 x 16 ft; origin X=81, Z=41 | East; open bar face points west toward courtyard |

The top-down camera remains identical across all stages. Only visibility changes, allowing direct comparison without scale or framing drift. The exact polygons, stage visibility, and camera definitions live in [cameras-and-geometry.json]({{repo:sources/data/cameras-and-geometry.json}}).

The geometry is dimension-controlled concept work, not a surveyed site plan. It must ultimately be transformed into parcel coordinates and adjusted around actual grade, trees, rock, drainage, septic, well, access, and regulated resources.

