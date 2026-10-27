---
name: solidcraft-sheet-metal
description: Use when modelling sheet-metal or bent-plate parts in SolidCraft (flanges, bends, hem, fold, path flange, convert, flat pattern, DXF, bend table), especially when a drawing or an expected flat pattern is given.
---

# SolidCraft sheet metal: complete reference

Validated on an edge-flange bracket (75 and 45 deg flanges), a U-channel (contour flange), a box converted to sheet metal (convert plus edge flange), a C-clamp (contour R50 plus hem plus holes) and a reference test plate (angles, then-bends, `height_from`, `position`, fold, path flange, perforate). Commands go through the SolidCraft MCP server. `batch` takes the key `command` plus `params`, never `cmd`. If your client defers tool schemas, load them first.

Suggested habits: send a screenshot of the folded and the flat state, and keep one folder per model with `_v2` names for changes.

## 1. Read the source first
- A bent part has TWO sets of dimensions, folded and flat. If no flat pattern is given, build the part, then state that the flat dimensions are assumed and ask for the expected flat pattern. (On the edge-flange bracket the first build gave 98.069 against 103.217 expected.)
- Tutorial videos: transcribe the audio first. A silent video (mean volume around -91 dB gives an empty transcript) needs its dimensions read from frames: make contact sheets with ffmpeg and measure unlabeled positions in pixels against a known width, for example 50 mm = 260 px.
- Spoken numbers are often wrong. The frames give the numbers.

## 2. Rule first
`sheet.manage_rules {name, thickness, k_factor (0.44 default), bend_radius ("Thickness" or a number as a string), relief_width, relief_depth, corner_relief, corner_relief_shape notch|round|rectangular|tear, hem_gap, gap, angle_display, active:true}`. `sheet.rules` lists them.

Bend maths: BA = (R + K*t) * angle_rad. The outer setback at 90 deg = R + t. Flat length = sum of leg lengths (outer mould lines) - sum(2*setback - BA) per bend. U-channel check: t2, K0.44, R = t, legs 40+50+40 give a flat length of 123.05. Box check: t2.5 with 15 mm flanges gives 182.619 x 172.619 mm with 8 bends.

## 3. Flange types (which command for which curve)
| Need | Command |
|---|---|
| First plate from a closed profile | `sheet.flange {type:"base", sketch, body_name}` (only the first profile; inner circles are NOT cut; the sheet occupies z 0..t) |
| Open profile with several bends in one go (U, Z, hat, C) | `sheet.flange {type:"contour", sketch, curves:[l1,l2,l3], distance (width), flip?, reverse?, body_name}`. The sketch lines are the OUTER mould lines. Draw the sketch on an upright plane (`{origin, x_dir:[1,0,0], y_dir:[0,0,1]}`); the strip extrudes by `distance` along the plane normal. Validated U: sketch [[-25,40],[-25,0],[25,0],[25,40]], distance 50, flip true |
| Big-radius bends (semicircle) | contour with a large `bend_radius` in the rule (R50, t5, legs 100 across gave a semicircular back, accepted even when 100 < 2*(R+t)); check the bbox |
| Single bend on an existing edge | `sheet.flange {type:"edge", edges:[[x,y,z] on the top or bottom edge], height, angle:"90 deg" (bend angle, default 90), radius?, height_from outer|inner|tangent, position inside|outside|middle|material_outside|tangent, flip, corner_relief_shape}`. 45, 75 and 120 deg all work |
| Joggle or several bends from one edge | edge flange with `then:[{angle,height,flip}]` (up to 16 further bends), for example {height:25,angle:"90 deg",then:[{angle:"90 deg",height:10,flip:true}]} |
| Flange following a path along the edge | `sheet.path_flange {edge:[x,y,z], sketch, curves:[l1,l2], radius?}`: the sketch is an open chain of lines on a plane across the edge, for example plane {origin:[0,30,0], x_dir:[1,0,0], y_dir:[0,0,1]} with lines [[0,1],[0,16],[-10,16]]. It starts at the edge and goes outward |
| Folded edge (teardrop, open, closed hem) | `sheet.hem {edges:[[x,y,z]], length (to the outer face), gap?, flip?}` |
| Bend a flat plate along a drawn line | `sheet.fold {sketch, curve, angle:"60 deg", radius, position centerline|start|end|mould, fixed:[x,y,z] on the side that stays, flip}` (sketch on the plate plane, line crossing the whole width) |
| Turn a solid box or shell into sheet metal | `sheet.convert {body, face:[x,y,z] (fixed face), bends:[[x,y,z] on each sharp edge], rule}`, then edge flanges for the lips |
| Hole pattern for flat pattern or DXF only | `sheet.perforate {diameter, pitch, margin, pattern staggered|square}`: affects the flat pattern, DXF and volume, NOT the B-rep |
| Back to flat or re-bend | `sheet.unfold`, `sheet.refold` |

## 4. Validated recipes
1. **U-channel (contour):** rule t2 K0.44 R=Thickness; the upright sketch above; flange contour curves l1,l2,l3 distance 50 flip true. Unfolded it spans x -25..-23, y -50..0, z -83.048..40 (L = 123.05). Cuts while flat: 4 triangles 10x10 at the corners plus a dia 35 circle centred at the bend (z = 36 + BA/2) on plane YZ offset -26, extrude distance 4 positive cut; then refold. Final 10005 mm3, bbox 50x50x40.
2. **Box via convert:** rule t2.5; XY rectangle +-35 x +-40 extruded 45 as a new body; `sheet.convert {body, face:[0,0,0], bends:[[35,0,0],[-35,0,0],[0,40,0],[0,-40,0]]}`; edge flange on the four top edges height 15, angle 90, position inside, height_from outer (the lip goes outward). Flat 182.619 x 172.619, 8 bends, volume 50152 mm3.
3. **C-clamp with hem:** rule t5 K0.44 R=50; XY sketch [[100,50],[0,50],[0,-50],[100,-50]]; contour distance 40; hems on the two VERTICAL end edges `{edges:[[100,55,20]], length:60}` and `{edges:[[100,-55,20]], length:60}` (flip false folds inward, flip true folds outward). Picking the bottom horizontal edge folds along Z, which is wrong. Holes: an upright sketch circle dia 25 at [75,20] and `solid.extrude through_all symmetric cut` targeting the body goes through both hem layers. Final 68319 mm3, bbox x -5..105, y +-55, z 0..40.
4. **Reference plate** (base 100x60, t2): edge flanges 45 deg h20, a joggle with `then`, 120 deg with height_from tangent, 90 deg with position material_outside. Fold test: plate 120x60, line x=80, fold 60 deg fixed at [20,30,2]. Path flange on the edge at y=30 with profile [[0,1],[0,16],[-10,16]]. Perforate dia 4 pitch 10 returns with no warning.
5. **Edge-flange bracket:** XY sketch with rounded corners as arcs, base flange, edge flange 75 deg then 45 deg (height measured to the outer face), holes cut while folded on flat panels, slots and corner rounds in the unfolded state.

## 5. Cuts and features
- Holes on flat panels parallel to the sketch plane can be cut folded (sketch plus `solid.extrude cut distance t`).
- Features on bends or on non-parallel panels: `sheet.unfold`, sketch on XY at z=0 in FLAT coordinates, extrude cut, then `sheet.refold`. Cutting folded is refused.
- Use cut planes just outside the sheet (offset) with distance > thickness. Avoid tool faces coplanar with sheet faces (they can hang the app).
- Rounded corners: never `solid.fillet` on sheet metal (it is dropped after refold). Cut each corner in the unfolded state with a closed sketch (two lines plus an R arc). Slots: `sketch.slot.center_to_center`.

## 6. Fitting to a target flat pattern
- Measure the flat size with `sheet.unfold` plus `measure` bbox, then `undo`. Never read `sheet.flat_pattern` in full (huge JSON). If needed pick only `flat_size_mm` and the bends.
- Flat length is linear in the flange heights: adjust the last flange by (current - target). On the bracket a lip of 9.458 gave 103.217.
- Keep an 8 mm straight run between a bend edge and the start of a diagonal (acute corners trim the flange). Slots must lie in the flat part (the flat starts at the bend line plus half the allowance).

## 7. Export
`save`, `sheet.export_dxf {body, path, bend_notes:true}`, `sheet.export_bend_table {body, format:"csv", path}`, `export` as 3mf or stl, and an isometric screenshot.

## 8. Traps
- Device calls time out at about 60 s. Save a checkpoint before risky operations. If a function fails or hangs, do not retry it: call `running` once and tell the user.
- Name sketches uniquely. Reusing a name after `undo` keeps the old geometry.
- The hem edge choice and `flip` decide the direction. Verify the bbox after each hem and `undo` if it is wrong.
- Cylinder or counterbore tools starting coplanar with a face hung the app twice: start 0.5-1 mm inside empty space.
- Perforate is not geometry. Cut real holes if the B-rep needs them.
- Use the counts as a sanity check: after contour, hem and holes the clamp had 10 cylinder faces (`face_types` in `measure`).
