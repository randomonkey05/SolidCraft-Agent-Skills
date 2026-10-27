---
name: solidcraft-tutorial-recipes
description: Use when a SolidCraft task is described in GUI terms (sketch, constraint, dimension, extrude, revolve, hole, shell, fillet, offset plane, circular pattern) or follows the public tutorials, to translate it into validated MCP commands.
---

# SolidCraft: GUI tutorial steps -> MCP commands (validated)

Public SolidCraft video tutorials teach the GUI. Every recipe below was re-run through the MCP server and checked with `measure` against hand-computed volumes. The tutorials themselves are not reproduced here, only the numbers needed to check a rebuild. Use together with `solidcraft-modeling` (command shapes, plane table, ids). For sweep recipes (twist, scale, vase, cup) and the rules for booleans that hang the app see `solidcraft-sweep-and-boolean-hangs`.

## GUI -> MCP mapping
| GUI step | MCP |
|---|---|
| New design | `new_design` (ask first if the open design has unsaved work) |
| Create sketch on the Right / Front / Top plane | `sketch.create plane` `YZ` / `XZ` / `XY`. On XZ the sketch y axis is -Z, so for a profile drawn upright use a custom plane `{origin:[0,0,0], x_dir:[1,0,0], y_dir:[0,0,1]}` (normal -Y) |
| Sketch on a top face or offset plane | `sketch.create {plane:"XY", offset:10}` or `construct.plane.offset` |
| Draw a line chain with horizontal/vertical constraints | `sketch.line {points:[[..],..]}`. A polyline already gets horizontal and vertical constraints where lines are axis-aligned. Give exact coordinates instead of constrain-and-dimension steps |
| Polygon with a dimension across flats | `sketch.polygon.inscribed {center, radius, sides, angle}`; radius = across-flats / (2 cos(180/n)), for example a hexagon across flats 40 gives radius 23.0940108 |
| Sketch fillet on polygon corners | `sketch.fillet {points:[p1..pn], radius}` |
| Offset a closed profile inward | `sketch.offset {curves:[all curve ids after the fillet], distance, side:[0,0]}` gives 2 profiles (a ring) |
| Centre-point arc | `sketch.arc.center_point {center, radius, start, end}` |
| Equal constraint, dimensions, Tie | Only needed for parametric designs. For speed, compute the points and skip them. Use `sketch.dimension` when parameters must drive the geometry |
| Finish sketch | `sketch.finish` |
| Extrude, Symmetric, New body | `solid.extrude {distance, direction:"symmetric", operation:"new", body_name}`. A symmetric distance is the TOTAL length. `direction:"negative"` goes below the sketch plane |
| Hole by a reference sketch point | a sketch with `sketch.point`, then `sketch.finish`, then `solid.hole {sketch, diameter}` (through all by default, drills along -normal of the sketch plane) |
| Counterbore hole | `solid.hole {sketch, diameter, cb_diameter, cb_depth}` with the point sketch on the face (XY offset = face height) |
| Hole by clicking a face | `solid.hole {position:[x,y,z] on the face, diameter}` |
| Extrude cut, Extent All, Symmetric | `solid.extrude {through_all:true, direction:"symmetric", operation:"cut", targets:[body]}` |
| Revolve with an axis line | `solid.revolve {axis:"y" (sketch axis) or a line id, angle:"360 deg", operation:"new"}`. For a partial turn such as `"270 deg"` use 360 minus the GUI's -90. On a custom upright plane the axis `"y"` is world Z |
| Offset plane | `construct.plane.offset {base:"XY", offset:"11.5", name}` then `sketch.create {plane:"<name>"}` |
| Fillet | `solid.fillet {edges:[[x,y,z]..], radius}` (one call per fillet group) |
| Shell, remove the top face | `solid.shell {faces:[[x,y,z] on the face], thickness, direction:"inside"}` |
| Circular or polar pattern | `solid.pattern.circular {features:[...], axis:"Z", count:n}`; see trap 1 |
| Parameters panel (D15 and so on) | `parameters.add {name, value}` and use the name in the dimension |

## Validated recipes (mm)
1. **L-bracket plus hole:** sketch `YZ`, polyline [[0,0],[100,0],[100,80],[75,80],[75,25],[0,25],[0,0]], extrude 50 symmetric new; `solid.hole position [25,87.5,55] diameter 20`. Volume 178 044.6 mm3 (193 750 minus the hole through the 50 mm arm).
2. **Notched profile plus hole by point:** `YZ` polyline [[0,0],[10,0],[10,10],[40,10],[40,0],[50,0],[50,30],[35,30],[35,40],[15,40],[15,30],[0,30],[0,0]], extrude 25 symmetric; a point sketch on plane `{origin:[12.5,0,0], x_dir:[0,1,0], y_dir:[0,0,1]}` at [20,20], then `solid.hole sketch diameter 10`. Volume 33 036.8 mm3.
3. **Revolve 270 deg:** upright plane, polyline [[0,0],[50,0],[38.453,20],[15,20],[15,65],[0,80],[0,0]], `solid.revolve axis "y" angle "270 deg"`. Volume 119 197 mm3.
4. **Flange with 4 holes:** polyline [[0,0],[5,0],[5,8.5],[15,8.5],[15,11.5],[5,11.5],[5,32],[0,37],[0,0]], revolve 360 (volume 4528.6). Holes via the cylinder-cut pattern in trap 1 (final volume 4293.07).
5. **Dish: revolve, fillet, shell, cross hole:** polyline [[0,0],[25,0],[50,43.301],[75,43.301],[75,75],[0,75],[0,0]], revolve 360; `solid.fillet` R10 on [25,0,0] and [50,0,43.301]; `solid.shell faces [[0,0,75]] thickness 5 inside`; then a sketch on `XZ` with a circle centre [60,-60] r5 and `solid.extrude through_all symmetric cut`.
6. **Dish v2 (different numbers from recipe 5):** upright plane polyline [[0,0],[50,0],[75,43.30127],[150,43.30127],[150,68.30127],[0,68.30127],[0,0]], revolve 360 axis y; fillet R10 at [[50,0,0],[75,0,43.30127],[150,0,43.30127]]; shell faces [[0,0,68.30127]] thickness 5 inside; a circle dia 10 at [0,60] on the upright plane, extrude cut symmetric through_all targeting the body. Tutorials with the same name can have different dimensions, so read them on the frames.
7. **Revolved flange with counterbore holes (from a Fusion 360 to SolidCraft tutorial):** profile (20,0)-(70,0)-(70,7.6)-(40,7.6)-(34.24264,14.75736)-(34.24264,22.75736)-arc(centre (34.24264,25.25736), r 2.5, through (31.74264,25.25736))-(34.24264,27.75736)-(34.24264,30.75736)-(30,35)-(25,35)-(25,5)-(20,5)-(20,0); revolve 360; parameter `R_holes=56`; hole sketch on XY offset 7.6 with a point at (0,-56); `solid.hole` counterbore dia 5 / dia 12 / depth 3; `solid.pattern.circular` count 6; fillet R10 at [40,0,7.6], then R2 at [70,0,7.6], one per call. Final volume 151 384.4 mm3, within 0.002 % of the analytic value.

## Traps found
1. **`solid.hole` plus `solid.pattern.circular` can be wrong.** On the small flange of recipe 4 the patterned through-all hole removed extra material (4213.8 instead of 4293.1). On recipe 7 (counterbore hole from a face sketch, 6 copies) the pattern matched the analytic volume. Rule: try hole plus pattern, `measure`, and compare with the analytic volume. If it is off, build the hole as `solid.cylinder {diameter, height, base, operation:"cut", targets:[body]}` and pattern that (`solid.pattern.circular {features:["cutname"], axis:"Z", count:4}` gave exactly the analytic volume).
2. **Edge picks on circular edges** must lie ON the circle (for example [50,0,43.301] for a radius-50 circle at z=43.301), not at a profile midpoint, or you get a `no edge near` error.
3. **A fillet bigger than the neighbouring wall** fails (`blend is taller than the walls`): the rim of a dish must be taller than the radius.
4. **Shell with a fillet on the open-face rim** fails when radius > thickness. Fillet the other edges first, shell, and fillet the rim afterwards only if radius < thickness.
5. A failed step in a batch rolls the WHOLE batch back (including the sketch and revolve before it). Re-send everything with the fix.
6. **Spoken numbers in transcripts are often wrong** (seen: "14 / 18 / 19" for 40 / 80 / 90 deg, "100" for 90). Extract frames with `ffmpeg -ss <t> -i video.mp4 -frames:v 1` at the dimension moments and read the on-screen labels.
7. Do not call `sketch.inspect` on large sketches (huge reply). Use `measure` or `sketch.solve`.
