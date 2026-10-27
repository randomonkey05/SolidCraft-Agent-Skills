---
name: solidcraft-sweep-and-boolean-hangs
description: Use when a SolidCraft model needs solid.sweep (twist, scale, vases, cups, pipes) or any cut or join on a swept or very-high-face-count body, to avoid hangs that need an app restart.
---

# SolidCraft: sweep recipes and boolean hang avoidance

Use with `solidcraft-modeling` and `solidcraft-tutorial-recipes`. Validated on public sweep tutorials (a twisted vase and a hex cup) and consistent with the timed-test lessons in `solidcraft-speed-modeling-lessons` (joins with coincident circular faces hang the app).

## 1. Sweep recipe (MCP)
1. Profile sketch on the plane where the profile lives (XY, or XY with an offset when it sits on top of a base).
2. Path sketch as a SEPARATE sketch on an upright plane `{origin:[0,0,0], x_dir:[1,0,0], y_dir:[0,0,1]}`: `sketch.line [[0,0],[0,H]]`.
3. `solid.sweep {sketch:"Profile", profiles:[{point:[x,y]}...], path_sketch:"Path", path:["l1"], twist:"90 deg", scale:2.2, operation:"new", body_name:"X"}`. Pick every closed region with a point inside it (for crossing arcs or circles pick all the lens regions and the ring).
4. Always use `operation:"new"`. A sweep joined to another body is a Boolean and very slow (the tutorial author says the same).
5. `measure` right after: the bbox height is the path length (plus the base), compare the volume with a numeric estimate. 400-1000+ faces are normal for twisted bodies.

## 2. Verified examples
- **Hex cup:** hexagon across flats 40 (`sketch.polygon.inscribed radius 23.0940108 sides 6 angle 0`), `sketch.fillet` R4 on the 6 corners, `sketch.offset` 2 inward (2 profiles give a wall ring), path 80 mm, twist 90 deg, end scale 2.2, profile pick [0,19]: 55 612.7 mm3, z 0-80. The transcript said 14 / 18 / 19 but the frames show 40 / 80 / 90. Bottom: `solid.extrude` of the outer profile 2 mm negative as a separate body (2 760.9 mm3).
- **Vase:** base dia 120 x 10. Profile sketch on XY offset 10 with circles r50 and r45 plus 8 arcs R6 (centres on the r49.6387 circle every 45 deg). Path 120 mm, twist 100 deg, scale 2, new body: 537 948 mm3, z 10-130.

## 3. Booleans touching a swept body HANG the app
- On the vase (revolve cut, twice) and the cup (join with the 2 mm bottom) every cut or join involving the swept body ran for more than 12 minutes and the app had to be restarted. There is no cancel tool. In the tutorial video the same revolve cut took 30 s, so a hang points to coincident or tangent geometry, not only to slowness.
- Likely causes: the bottom disc coplanar with the sweep start face with identical edges, or a cut tool whose edge or vertex lies exactly on the swept top face.
- Rules:
  - `save` a checkpoint BEFORE the boolean.
  - Overlap the tool by a clear margin (for example start the bottom 0.5-1 mm inside the cup, outline scaled 0.99-1.001) instead of using coplanar faces.
  - Run the first boolean alone in its own call.
  - If it hangs once, deliver separate bodies (a `.3mf` with 2 objects), say so, and do not retry.
  - Do not poll with `sleep`. Call `running` once, then tell the user.
- Cheaper alternatives: include the bottom as an extra closed region of the sweep profile, or build the bottom disc first and sweep from its top.

## 4. After a restart
Reopen the last checkpoint (check errors = 0 and the feature count) and `measure`. If your setup restricts where the app may save files, create the target folder first.
