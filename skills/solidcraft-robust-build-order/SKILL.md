---
name: solidcraft-robust-build-order
description: Use when modeling any part in SolidCraft (not only timed tests): reliable build order, boolean and fillet traps, verification against analytic values, and parametric configuration generators.
---

# SolidCraft: robust general modeling workflow

General lessons validated on tapered and pocketed arm parts from timed speed-modeling tests and on a tutorial hook. Apply them to any part, timed or not.

## 1. Build order (fewest failures)
1. Base body from one profile sketch, extruded symmetric (operation new).
2. Second profile (other plane) extruded with operation `intersect` on the base body. Do the intersect BEFORE other cuts. Never intersect after a bore is cut: it once returned a silently wrong solid (centre of mass shifted, volume +60%) with no error.
3. Bores and holes as `solid.cylinder` cuts with explicit base, axis and targets (then a circular or linear pattern of the cylinder cut if repeated), or a simple sketch-circle extrude cut.
4. Pockets and cavities: sketch a polygon, extrude it as a separate "Cutter" body, trim it with `solid.box` or cylinders (targets `[Cutter]`). A cut through the middle splits it into `Cutter` and `Cutter (1)`. Finish with `solid.combine` cut using ALL tool bodies.
5. Fillets and chamfers: on a simple prismatic body do them right after the base and holes (section 3a). On a complex body (sphere, loft, sweep, draft, cavity) do them last, or before the complex feature is added (section 3b).

Keep the model as few features and as few bodies as you can. Fillets work best on one simple body, and the kernel has less to compute.

## 2. Boolean rules
- A tool surface must not be coincident or tangent with a cylindrical face of the target. Offset the tool radius by +1 mm (R+0.3 failed with `boolean Cut: no result`).
- A tool face coplanar with an existing face (for example a cut that starts exactly on a wall an earlier cut already opened) can hang the app. Start the tool 0.5-1 mm inside empty space and lengthen the distance accordingly.
- Risky steps (combine, big fillets) go in their own call, because a failed batch rolls back everything.
- A `Boolean retry: tool displacement` warning is a yellow flag: verify with `measure`.
- Booleans touching swept bodies: see `solidcraft-sweep-and-boolean-hangs`.

## 3. Fillets and chamfers: two regimes
### 3a. Simple prismatic body
A profile extruded, straight edges parallel to the extrusion, only planar neighbour faces. Validated on a tutorial hook (12 corner edges, 15 mm thick): R4 on 3 edges took 0.4 s, R2 on 9 edges 1 s, chamfer loops 1 s, and the volume matched the analytic value within 0.001 %. Corner correction: area change = +/- r^2 (tan(d/2) - d/2), where d = deflection angle = 180 - interior angle, negative for convex corners and positive for concave corners or holes.
- Do the fillets right after the base extrude and the simple holes, before any complicating feature.
- Group by radius: ONE `solid.fillet` call with all edges of that radius (pick a point on each edge at mid-thickness), largest radius first.
- Chamfers after the fillets. One pick per face outline loop is enough because the tangent chain takes the whole loop, also through the fillet arcs. Chamfer hole edges in a separate call.
- Still `save` a checkpoint before the first fillet and `measure` after each call (compare cylinder-face count and volume).

### 3b. Complex body
Sphere, loft, sweep, draft, torus crown, thin lip, shell.
- One `solid.fillet` call per small group of edges (for example 4 picks) with `fit:"reduce"`. Never put several fillets in one batch: a device call times out at about 60 s, fillets on a body with a sphere took 35-100 s, and 6 edges at once ran for more than 20 minutes.
- `save` a checkpoint before each fillet group.
- Prefer filleting the flat part BEFORE joining the sphere, cavity or sweep (1-50 s) instead of after (35-100 s).
- Read the warnings. `radius is reduced to 0.06 mm` is useless, so undo it. Fillets near narrow ends or knife-edge lips (`blend larger than neighbouring faces`, `both faces must be planar`) can take minutes or block the app. Skip or reduce them and record that in the notes.
- Fillet the vertical edge first, then the horizontal ones (`blend ending in an earlier round`).

### 3c. Both regimes
- Edge picks must lie on the edge, and one pick takes the whole tangent chain.
- Fillet before shell unless the edge belongs to the removed face.
- Prefer doing every feature in the drawing over skipping fillets to save time, but pick the regime first so the risk is contained.

## 4. Verification
- After the body stage, `measure` and compare the volume with an analytic estimate (numeric integration in Python, or the corner formula above). The centre of mass must lie on symmetry planes.
- `inspect_design {measure:false, sketches:false}` shows per-feature warnings.

## 5. Device behaviour
- A device call that times out (about 60 s) may still be running, so do not resend it. Call `running` once. If the app does not answer, tell the user, who restarts it, then reopen the last checkpoint. Do not poll with `sleep`. If the user says not to retry a failed step, deliver without it and state what is missing.
- A design named "Untitled" means the app restarted: rebuild from the last checkpoint.

## 6. Parametric configurations (design-table style)
- Write a Python generator `gen(D, L, A, ...)` that emits the whole command list from the drawing's formulas (tangent points from a circle centre and an angle, offset lines via w/cos(slope), pick points computed at a fixed x). Each configuration is one `new_design`, one build batch, a checkpoint and the fillets per regime 3a/3b. Compare the volumes of the configurations for sanity.
- Example formulas: R = D/2 + wall, tangent point T = (L - R sinA, R cosA), line back to x = -e: y = T.y - (T.x + e) tanA.

## 7. Ideas not yet tested
- `solid.draft` for wall drafts, and `solid.shell` plus `solid.mirror` for half-model workflows.
