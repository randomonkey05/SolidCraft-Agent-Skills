---
name: solidcraft-speed-modeling-lessons
description: Use when modelling a part from a drawing under time pressure in SolidCraft (speed-modeling challenges such as SolidWorks Model Mania) or when a build crashes, hangs or returns a wrong volume: recorded failures, workarounds and bent-plate or angled-tube tactics.
---

# SolidCraft speed-modeling lessons

Collected from about a dozen timed builds of SolidWorks Model Mania speed-modeling drawings (2001-2005 editions) plus a 2024 phase-1 part. The drawings and solution files belong to their authors and are not included. Only the lessons are. Each build was done blind from the drawing first and then redone after watching the author's solution video. Use with `solidcraft-modeling`, `solidcraft-robust-build-order` and `solidcraft-drawing-and-tutorial-reading`.

## 1. Habits that worked
- Save a checkpoint before fillets and before any heavy batch.
- Order: flat parts and fillets, then holes, then spheres and cavities LAST.
- Watch and transcribe the audio of the solution video BEFORE rebuilding, and only then measure against the solution file.
- Compare every `measure` with an analytic estimate. The bounding box can match while the volume still exposes wrong details.
- For several configurations of one drawing, generate the commands with a parametric Python script (D, L, A, ...). This produced all configurations of one test without boolean errors.
- Keep to one simple body and few features when fillets are needed (see `solidcraft-robust-build-order`).

## 2. Failures: the app (crash, timeout)
- A device call times out at about 60 s. Heavy batches and slow fillets exceed it, but the work may still finish. Check with `inspect_design` before resending.
- The app can restart or crash and lose the design when nothing was saved. Typical triggers: a fillet on an arm arc, joins with spherical faces, a shell on fillet faces.
- Any join between a body with a spherical face and a plateau (a sphere R170 or a flat prism) hung the app five times. Cones from 15 deg drafts plus the sphere were the cause. Without the drafts the union took 38 s.
- Native `solid.shell` crashes or fails with fillet faces. A cavity that ends flush with or crosses the back face crashed three times. Ending it 0.1 mm short and cutting the rest with a planar box worked.
- Reopening a checkpoint that already contains fillets does not reliably finish (a long rebuild). Save it, but reopen the version without fillets and reapply them.

## 3. Failures: booleans
- **Coplanar faces:** a tube end coplanar with the side of a plate made SolidCraft nudge the tool by 0.0002 mm and rotate it 2e-6 rad. That creates slivers and every later fillet fails (`rounds would leave openings`). Make the parts longer and trim at the end with an intersect.
- A cutter ring with the same radius as an eye or boss gives `boolean Cut: no result`. R+0.3 failed too, R+1 worked.
- An intersect of the side profile with a large hole returned a WRONG solid with no error (volume 357k instead of about 216k). Build the side profile as the base body, the plan view as an intersect, and the holes afterwards. Compare against an analytic volume every time.
- Intersect with a sphere: the sphere must be the TARGET (the reverse order blocks or gives `no result`). A rib that does not touch the lobe gives an empty intersect. Use Fill and confirm the body is 1 shell.
- Booleans after the sphere take 7-50 s each. Join the flat parts first, drill before the sphere, add the sphere last, and never repeat the same join more than twice.
- Sketch errors seen: an arc through 3 collinear points, and `sketch.create` takes `offset` next to `plane`.
- A join (loft, combine or cylinder) with an exactly coincident circular face or edge blocks the app and restarts it without a report. Workarounds: make the loft a new body (7 ms), start the first circle 0.05 mm smaller, make the cylinder taller and join (12 s), or start a prism 0.01 mm lower with the outline scaled x1.001 (40 s).
- A second crossing curved surface on the same top (an intersect with a cylinder R75 after R250, or an extrude cut of an R75 arc) blocked the app three times. One revolve cut (15 s) worked.
- Extrude with taper: `-3 deg` shrinks upward and `+3 deg` widens (for cut and join). The first prism with +3 came out the wrong way round (bbox x 38.01 instead of 37.54).
- Native `solid.draft` fails on a boss next to a loft (`neighbouring faces must be planes or cylinders`). Put the draft into the construction (extrude the boss circle with a taper, 35 s) instead of drafting later.
- A revolve cut of a thin triangular sliver around a boss (to create a draft) blocked the app twice. Do not use it.
- A cavity with a 3 deg draft worked as an extrude cut of the sketch (outline offset -4.214 mm plus the column circle R13.45, overlapping, profiles picked by point) with taper -3 deg: 99 s, no crash. Reopening that checkpoint takes 3-4 minutes because everything recomputes.

## 4. Failures: fillets
- Fillets that never came out: the top of a rib (`fillet larger than faces`), the flange of a tube (`degenerate rolling-ball spine`), a lower step R6 (reduced to 0.001 mm after 154 s), a pocket rim (175 s, 0.06 mm), an outer arc of an arm (`faces at the edge ends must be planar`), a plate bottom edge (`ball doesn't fit`), a block's lower arc (`only straight edges`).
- `blend ending in an earlier round`: fillet the vertical edge first, then the horizontal ones.
- Fillets on a body with a sphere take 35-100 s. On the flat part BEFORE joining the sphere or cavity they take 1-50 s and do not crash.
- A batch of 3 fillets exceeds the 60 s timeout. Send one fillet per call with a checkpoint first.
- A fillet picked by point propagates along the tangent chain (one point on the top perimeter rounded the whole outline). At R2 the fit reduced it to 1.999 mm.
- A 1 mm fillet on 6 edges of a cavity roof in one call ran for more than 20 minutes without an answer (probably blocked).
- Features not done for crash risk in some builds: 1 deg and 15 deg drafts, an R3 fillet, an internal spherical cavity. Say so in the notes rather than leaving it unmentioned.

## 5. Failures: reading the drawing (the blind build diverges from the solution)
- Only the video or transcript fixes these:
  - A hemisphere D70 (revolve 180 deg) UNITED with a lobe was drawn as a dome that cut the part. Only the audio showed it, after which the bbox matched the solution.
  - A 75 mm radius that is a revolve cut of the R250 arc around an axis parallel to X, 75 mm from the peak (a toroid), not a second arc.
- Assumptions that cost volume: a counterbore size assumed, a web width read from the wrong view, a dimension not used directly (a curve R55 plus a tangent arc), a missing dome on a plate, a bent plate or underside rib missed (-16 % volume), an eye height and web thickness assumed, a 7 deg inclination and 3 mm fillets omitted (+12.5 %), a 4 mm wall made by subtracting an inner body (+41 %), a step without its own thickness, a missing draft and fillet.
- Compare with the solution file (STEP): the bounding box can match (right layout) while the volume reveals wrong details.
- Timings do not include the time spent reading the drawing before the file was created. Report both if a time matters.

## 6. Bent plate, angled tube and revolve tactics (verified with `measure` and screenshots)
- Read the drawing:
  - A thickness dimension on a bent profile means a bent plate, not a solid web. Cross-check widths in the plan view.
  - A tube whose axis is at 45 deg lies in the side-view plane. The dimension to the end face gives its centre, and the section view gives body and flange lengths.
  - Do the geometry in the (z, y) coordinates of the side view and convert to the sketch coordinates of the plane you use.
- Side-profile sketch on `{origin:[x0,0,0], x_dir:[0,1,0], y_dir:[0,0,1]}` (sketch x = world Y, sketch y = world Z). Extrude with a positive `distance` for a rib and `direction:"symmetric"` for a centred plate.
- Arcs: `sketch.arc.three_point {start,end,through}` with a computed midpoint is easier than `center_point`. Lines from `sketch.line {points:[...]}` chain automatically.
- A bent plate is ONE closed polygon with two concentric arcs (R outside, R+thickness inside), extruded symmetric to the plate width.
- A rib under a plate: let its top edge sit several mm INSIDE the plate (an offset arc R-4, concentric) to avoid coplanar booleans.
- An angled tube: sketch on the plane `{origin: end_face_centre, x_dir: axis_dir, y_dir:[1,0,0]}` with the profile (axial, radial) closed on the axis. `solid.revolve axis:"x"` join, then a second revolve cut for the bore.
- Counterbored holes: a point sketch on an XY plane at the top face offset, then `solid.hole sketch diameter type:counterbore cb_diameter cb_depth`.
- A rib base fillet: `solid.fillet edges:[[x,y,z_top]] fit:"reduce"` worked.
- Fillet traps: a pick on a circular edge that hits the seam gives `edge is smooth`, so pick a point opposite the seam. A concave tube-step fillet next to a plate gave `degenerate rolling-ball spine`: try the other side, or skip it and say so.
- If the plate is wider than the tube body, the corners stay. A dome fixes it: intersect the plate end with a cylinder about the tube axis.

## 7. Other command notes
- Batch commands use the key `command` (not `cmd`). `undo` has no `steps` parameter, and there is no undo after opening a file.
- `inspect_design` with many sketches returns enormous replies. Use `measure` or `body_topology` instead.
