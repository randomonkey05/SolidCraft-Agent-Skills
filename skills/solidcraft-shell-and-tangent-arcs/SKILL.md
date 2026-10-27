---
name: solidcraft-shell-and-tangent-arcs
description: Use when applying solid.shell (hollowing, underside cavities, open face) in SolidCraft, or when a shell fails or hangs: causes, safe order, tangent-arc precision and the pocket-cut fallback.
---

# solid.shell in SolidCraft: how it works, how it fails, how to get around it

## Syntax
`solid.shell {faces:[[x,y,z]], thickness, direction:"inside"|"outside"|"both", tangent_chain?, body?}`
- `faces` are points on the faces to REMOVE (open). For an underside cavity pick a point on the bottom face z=0 that lies inside the outline and outside bosses and bores, for example [-38,0,0].
- `direction:"inside"` keeps the outer shape. `body` names the target body.

## Failure 1: "offset: a corner whose faces don't meet the same way after the move"
- Cause: arcs that are meant to be tangent (for example a convex R12 around a hole boss and concave R75 side arcs) were entered with 5-decimal coordinates, so the faces are only nearly tangent. The offset treats the joints as real corners and fails for any thickness, even on the bare extruded base.
- Fix: compute the tangent points analytically (the point on the line between the two arc centres at distance r1 from the first centre) and enter the coordinates with 10 decimals in `sketch.arc.three_point` (start, end, through). The shell then works on the base and on base plus cylinder.
- `solid.fillet` on such an edge answers `edge is smooth` when the joint is truly tangent, so you can use it as a tangency test.
- `tangent_chain:true` did not help for this failure.

## Failure 2: shell hangs SolidCraft (minutes, needs a restart)
- Seen when the body already has a bore whose wall equals the shell thickness: a bore R25 inside a cylinder R30 with thickness 5 (4.9 as well). The offset of the outer face and of the bore face meet and collapse into degenerate geometry and an endless computation. A 60 s timeout does not mean it stopped: check `running` and do not resend. Nothing can be done until it ends or the app is restarted.
- Prevention: shell BEFORE cutting bores or holes whose wall to another face is <= thickness (plus a small margin). A working order is base, cylinder, ear or joins, shell, bores, small cuts. Save a checkpoint before the shell.
- A batch that contains a failing shell rolls back everything, so run the shell as a separate call.

## Safe order that worked
base extrude, cylinder join, shell (thickness 5, bottom face open). Adding the bore afterwards is the open point to test: the cavity wall at R25 coincides with an R25 bore, so expect a degenerate boolean. Consider a slightly different shell thickness or build the bore as part of a pocket.

## Fallback: emulate an underside shell with a pocket cut (validated)
1. Sketch on XY at the open face with the outline offset INWARD by the wall thickness t: convex arcs R become R-t and concave arcs R become R+t (same centres), keeping tangency exact.
2. Add circles for the material that must stay: a boss ring (for example R30). Rings around holes are already in the offset outline (hole radius plus t).
3. `solid.extrude {operation:"cut", start_offset:-1, distance: depth+1, profiles:[{point:[x,y]}], exact_regions:true}`. Pick a point INSIDE the wanted region only. A point outside the offset outline gives `unknown profile`.
4. Verify with `measure` (volume, shells=1) and tell the user it is an emulation, not `solid.shell`.

## Checks after a shell
`measure`: 1 shell, closed, and a plausible volume drop (area x t). Then take a screenshot from below (camera yaw 225, pitch -40) to confirm the cavity.
