---
name: solidcraft-sheet-metal
description: Use when modelling sheet-metal or bent-plate parts in SolidCraft (flanges, bends, hem, fold, path flange, convert, flat pattern, DXF, bend table), especially when a drawing or an expected flat pattern is given.
---

# SolidCraft sheet metal: complete reference

Validated on an edge-flange bracket (75 and 45 deg flanges), a U-channel (contour flange), a box converted to sheet metal (convert plus edge flange), a C-clamp (contour R50 plus hem plus holes), a reference test plate (angles, then-bends, `height_from`, `position`, fold, path flange, perforate), a phone stand (contour plus flat-state cuts) and a chamfered block converted with a hole (convert). Commands go through the SolidCraft MCP server. `batch` takes the key `command` plus `params`, never `cmd`. If your client defers tool schemas, load them first. The two tutorial-based models (phone stand, converted block) are written up in [`references/elite-engineers-phone-stand-and-convert.md`](references/elite-engineers-phone-stand-and-convert.md), and their files (3MF, design, flat pattern, bend table) are in [`examples/sheet-metal-tutorials/`](../../examples/sheet-metal-tutorials/README.md).

Suggested habits: send a screenshot of the folded and the flat state, and keep one folder per model with `_v2` names for changes.

**Flat-pack enclosures** (laser-cut plates, ear tabs, bend slits, perforation, side plates; for example a CD-ROM player enclosure): use the separate skill [`solidcraft-sheet-metal-flatpack`](../solidcraft-sheet-metal-flatpack/SKILL.md) together with this one. Key limits found there: `sheet.fold` is a half-plane fold; a fold whose moving side already has a bend is refused (fold from the fixed side outward); the default direction of an edge flange is the bottom-face normal (`flip:true` for the opposite); about 700 real holes per sheet is the boolean budget.

## 1. Read the source first
- A bent part has TWO sets of dimensions, folded and flat. If no flat pattern is given, build the part, then state that the flat dimensions are assumed and ask for the expected flat pattern. (On the edge-flange bracket the first build gave 98.069 against 103.217 expected.)
- Tutorial videos: transcribe the audio first. A silent video (mean volume around -91 dB gives an empty transcript) needs its dimensions read from frames: make contact sheets with ffmpeg and timestamps, then take full-resolution frames of the dimensioned sketch and of the Create Flat Pattern dialog, and measure unlabeled positions in pixels against a known width, for example 50 mm = 260 px. The flat-pattern dialog lists the bend count, the angles and the flat size, so use them as a check (phone stand: 7 bends, matched).
- Spoken numbers are often wrong. The frames give the numbers.
- When real flat patterns are provided, compare them against the model feature by feature (perforation, windows, steps, ears, holes, relief notches) before rebuilding.

## 2. Rule first
`sheet.manage_rules {name, thickness, k_factor (0.44 default), bend_radius ("Thickness" or a number as a string), relief_width, relief_depth, corner_relief, corner_relief_shape notch|round|rectangular|tear, hem_gap, gap, angle_display, active:true}`. `sheet.rules` lists them.

Bend maths: BA = (R + K*t) * angle_rad. The outer setback at 90 deg = R + t. Flat length = sum of leg lengths (outer mould lines) - sum(2*setback - BA) per bend. U-channel check: t2, K0.44, R = t, legs 40+50+40 give a flat length of 123.05. Box check: t2.5 with 15 mm flanges gives 182.619 x 172.619 mm with 8 bends. The tool's setback for obtuse bends (a turn of more than 90 deg) does NOT follow (R+t)*tan(a/2), so do not predict the flat length of such profiles by hand (phone stand: hand formula 273.4, tool 282.2). Measure with `sheet.unfold` plus the flat pattern.

## 3. Flange types (which command for which curve)
| Need | Command |
|---|---|
| First plate from a closed profile | `sheet.flange {type:"base", sketch, body_name}` (only the first profile; inner circles are NOT cut; the sheet occupies z 0..t) |
| Open profile with several bends in one go (U, Z, hat, C, stands) | `sheet.flange {type:"contour", sketch, curves:[l1,l2,l3], distance (width), flip?, reverse?, body_name}`. The sketch lines are the OUTER mould lines. Draw the sketch on an upright plane (`{origin, x_dir:[1,0,0], y_dir:[0,0,1]}`); the strip extrudes by `distance` along the plane normal. Validated U: sketch [[-25,40],[-25,0],[25,0],[25,40]], distance 50, flip true. Validated 5-segment profile (4 bends, 100 and 140 deg one way, 90 and 75 deg the other) drawn as ONE `sketch.line` chain of points, curves l1..l5, distance 80, flip true: the strip went to -y |
| Big-radius bends (semicircle) | contour with a large `bend_radius` in the rule (R50, t5, legs 100 across gave a semicircular back, accepted even when 100 < 2*(R+t)); check the bbox |
| Single bend on an existing edge | `sheet.flange {type:"edge", edges:[[x,y,z] on the top or bottom edge], height, angle:"90 deg" (bend angle, default 90), radius?, height_from outer|inner|tangent, position inside|outside|middle|material_outside|tangent, flip, corner_relief_shape}`. 45, 75 and 120 deg all work |
| Joggle or several bends from one edge | edge flange with `then:[{angle,height,flip}]` (up to 16 further bends), for example {height:25,angle:"90 deg",then:[{angle:"90 deg",height:10,flip:true}]} |
| Flange following a path along the edge | `sheet.path_flange {edge:[x,y,z], sketch, curves:[l1,l2], radius?}`: the sketch is an open chain of lines on a plane across the edge, for example plane {origin:[0,30,0], x_dir:[1,0,0], y_dir:[0,0,1]} with lines [[0,1],[0,16],[-10,16]]. It starts at the edge and goes outward |
| Folded edge (teardrop, open, closed hem) | `sheet.hem {edges:[[x,y,z]], length (to the outer face), gap?, flip?}` |
| Bend a flat plate along a drawn line | `sheet.fold {sketch, curve, angle:"60 deg", radius, position centerline|start|end|mould, fixed:[x,y,z] on the side that stays, flip}` (sketch on the plate plane, line crossing the whole width). Half-plane semantics: it bends everything beyond the line |
| Turn a solid box, shell or prism into sheet metal | `sheet.convert {body, face:[x,y,z] (fixed face), bends:[[x,y,z] on each sharp edge], rule}`, then edge flanges for the lips. The fixed face is one face of the solid (for example the bottom) and the bend edges are its boundary edges. Selecting only some of them gives `not supported yet: converting bodies that are not a plate of even thickness without bend edges`, so select ALL bottom edges (4 for a prism) |
| Hole pattern for flat pattern or DXF only | `sheet.perforate {diameter, pitch, margin, pattern staggered|square}`: affects the flat pattern, DXF and volume, NOT the B-rep |
| Back to flat or re-bend | `sheet.unfold`, `sheet.refold` |

## 4. Validated recipes
1. **U-channel (contour):** rule t2 K0.44 R=Thickness; the upright sketch above; flange contour curves l1,l2,l3 distance 50 flip true. Unfolded it spans x -25..-23, y -50..0, z -83.048..40 (L = 123.05). Cuts while flat: 4 triangles 10x10 at the corners plus a dia 35 circle centred at the bend (z = 36 + BA/2) on plane YZ offset -26, extrude distance 4 positive cut; then refold. Final 10005 mm3, bbox 50x50x40.
2. **Box via convert:** rule t2.5; XY rectangle +-35 x +-40 extruded 45 as a new body; `sheet.convert {body, face:[0,0,0], bends:[[35,0,0],[-35,0,0],[0,40,0],[0,-40,0]]}`; edge flange on the four top edges height 15, angle 90, position inside, height_from outer (the lip goes outward). Flat 182.619 x 172.619, 8 bends, volume 50152 mm3.
3. **C-clamp with hem:** rule t5 K0.44 R=50; XY sketch [[100,50],[0,50],[0,-50],[100,-50]]; contour distance 40; hems on the two VERTICAL end edges `{edges:[[100,55,20]], length:60}` and `{edges:[[100,-55,20]], length:60}` (flip false folds inward, flip true folds outward). Picking the bottom horizontal edge folds along Z, which is wrong. Holes: an upright sketch circle dia 25 at [75,20] and `solid.extrude through_all symmetric cut` targeting the body goes through both hem layers. Final 68319 mm3, bbox x -5..105, y +-55, z 0..40.
4. **Reference plate** (base 100x60, t2): edge flanges 45 deg h20, a joggle with `then`, 120 deg with height_from tangent, 90 deg with position material_outside. Fold test: plate 120x60, line x=80, fold 60 deg fixed at [20,30,2]. Path flange on the edge at y=30 with profile [[0,1],[0,16],[-10,16]]. Perforate dia 4 pitch 10 returns with no warning.
5. **Edge-flange bracket:** XY sketch with rounded corners as arcs, base flange, edge flange 75 deg then 45 deg (height measured to the outer face), holes cut while folded on flat panels, slots and corner rounds in the unfolded state.
6. **Phone stand (from a public tutorial video, built):** rule Steel t2.5 K0.44 R=Thickness. Profile on the plane x_dir [1,0,0], y_dir [0,0,1], as one `sketch.line` chain (0,0) (90,0) (72.635,98.481) (35.135,33.529) (13.484,46.029) (17.366,60.518). The legs are 90/100/75/25/15 and the bend angles are 100 and 140 deg (same way), then 90 and 75 deg (the other way). Contour flange curves l1..l5, distance 80, flip true, then `sheet.unfold`: flat 282.2 x 80 (the video shows 286), bend centres at x 87.2, 175.0, 241.0 and 266.8 (from `bend_zones` and `bends` of `sheet.flat_pattern`: use them to place features). Flat-state cut sketch on a plane at z=-1 (the frame equals the build frame, sheet at z 0..t, y -80..0), ONE sketch with 4 closed profiles, extrude distance 4 cut: (a) taper strips on each side, polygon edge offsets 0 at x=0, 15 at the first bend and 10 at x=245, constant to the end, with the corner rounded by a tangent R10 arc drawn with `sketch.arc.three_point` (tangent points computed by hand); (b) a slot c2c 55 x 20 wide crossing bend 2 (`sketch.slot.center_to_center`); (c) a second slot reaching past the strip end, an open U notch that splits the end tab. Then `sheet.refold`. The flat pattern then has 7 bends (4 bends, two of them split by the slots), as in the video. Cuts through bends are only possible this way.
7. **Chamfered block with a hole, converted (from a public tutorial video, built):** pentagon profile on the plane x_dir [1,0,0], y_dir [0,0,1]: (-60,0) (60,0) (60,120) (-10,120) (-60,70), `solid.extrude` new_body 120 (NOTE: the body went to -y even with `flip`, so read the bbox with `measure` before placing the next sketch). Hole sketch on a plane 10 mm outside the block, circle dia 50 at (0,55), extrude cut distance 140 through both pentagon faces. Rule Steel t5 K0.44 R=Thickness. `sheet.convert {body, face:[0,-120,0] (the bottom), bends:[the 4 bottom edge midpoints], rule}` gives bottom plus 4 walls. Both pentagon walls keep the dia 50 hole, there are 4 bends and the DXF export works.

## 5. Cuts and features
- Holes on flat panels parallel to the sketch plane can be cut folded (sketch plus `solid.extrude cut distance t`).
- Features on bends or on non-parallel panels: `sheet.unfold`, sketch on XY at z=0 in FLAT coordinates, extrude cut, then `sheet.refold`. Cutting folded is refused (`machining intersects a folded bend`). Shape changes of the whole strip (tapers, wide slots, U notches, rounded corners) are done this way, in one sketch.
- Use cut planes just outside the sheet (offset) with distance > thickness. Avoid tool faces coplanar with sheet faces (they can hang the app).
- Rounded corners: never `solid.fillet` on sheet metal (it is dropped after refold). Cut each corner in the unfolded state with a closed sketch (lines plus an arc, tangent to both edges). Slots: `sketch.slot.center_to_center`.
- A sketch plane's normal is x_dir x y_dir, and a cut with a positive distance goes along that normal. Use a negative distance (or flip the plane) when the cut changes no bodies. A new-body extrude may ignore `flip`: measure the bbox.

## 6. Fitting to a target flat pattern
- Measure the flat size with `sheet.unfold` plus `measure` bbox, then `undo`. Never read `sheet.flat_pattern` in full unless the part is small (it is short for simple parts: `bends`, `bend_zones`, `flat_size_mm`). If needed pick only `flat_size_mm` and the bends.
- Flat length is linear in the flange heights: adjust the last flange by (current - target). On the bracket a lip of 9.458 gave 103.217.
- Keep an 8 mm straight run between a bend edge and the start of a diagonal (acute corners trim the flange). Slots must lie in the flat part (the flat starts at the bend line plus half the allowance).

## 7. Export
`save`, `sheet.export_dxf {body, path, bend_notes:true}`, `sheet.export_bend_table {body, format:"csv", path}`, `export` as 3mf or stl, and an isometric screenshot. The folder must exist before `save` or `export` (error `its folder does not exist`), so create it first.

## 8. Traps
- Device calls time out at about 60 s. Save a checkpoint before risky operations. If a function fails or hangs, do not retry it: call `running` once and tell the user. If every call says no SolidCraft app is listening on 127.0.0.1:7878, the app is closed: ask the user to open it.
- Name sketches uniquely. Reusing a name after `undo` keeps the old geometry.
- The hem edge choice and `flip` decide the direction. Verify the bbox after each hem and `undo` if it is wrong.
- Cylinder or counterbore tools starting coplanar with a face hung the app twice: start 0.5-1 mm inside empty space.
- Perforate is not geometry. Cut real holes if the B-rep needs them (budget about 700 holes per sheet, see `solidcraft-sheet-metal-flatpack`).
- Use the counts as a sanity check: after contour, hem and holes the clamp had 10 cylinder faces (`face_types` in `measure`).
