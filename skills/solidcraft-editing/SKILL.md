---
name: solidcraft-editing
description: "Use when changing, fixing or extending an existing SolidCraft design through its MCP server - a .solidcraft file or the design open in the app. Typical requests: resize it, move a cut, change a hole or standoff, add a fillet or chamfer, make a fixed value parametric, or a feature shows an error after a change or after the app crashed."
---

# SolidCraft editing

## Overview
Edit an existing design through its parameters instead of rebuilding it. Every sketch dimension and feature input is already a parameter (`d1`, `d2`, ...), so most edits are a `parameters.change` each, sent together in one batch. Map the design with a few compact calls rather than walking the timeline one feature at a time. For command shapes and traps, in SolidCraft's own chat or any MCP client, call `skill_reference {"skill":"solidcraft-modeling"}`. Elsewhere, use `reference.md` from the `solidcraft-modeling` skill.

## Map the design (3-4 calls)
1. **Open:** if the design is not open yet, run `open {path}`. When the server is bridged to the app and the current design is `dirty`, ask before opening anything.
   - `open` of a path that is already open and changed keeps the changed design (tested on 0.29.0: volume and sketches were not reloaded). To get back to the saved file, copy it to a new name and open the copy.
2. **Overview:** `inspect_design {"measure":false,"sketches":false}` lists the user parameters, the sketch dimensions (`d1`, `d2`, ... with their expressions), the features in order, and their errors.
3. **Feature inputs:** `execute parameters.list {"filter":"feature"}` gives every feature input as an object such as `{"name":"d9","expression":"(6) / 2","feature":"Cylinder1","input":"Radius"}`. `inspect_design` leaves these out.
   - Match sketch dimensions by expression.
   - If that is ambiguous, `sketch.inspect {sketch}` that one sketch, which also shows its points in world coordinates.
4. **Baseline:** `measure {}`, so you can predict every change against it.

`timeline.inspect {feature}` is only for two cases:
- changing more than a number: profiles, direction, operation or edges
- checking whether a position follows a parameter, for example a cylinder `base` written as `width/2 - wall - 6`

Inspect one feature of each kind, not every copy.

## Change
- **A number:** `parameters.change {"name":"d9","expression":"..."}`.
  - **To make a fixed value parametric:** add a user parameter first (`parameters.add standoff_d`), then set each input to an expression of it (`standoff_d/2`).
  - **Several changes:** one `batch`. (Release 0.28 says several parameter changes can be applied together as one rebuild and one undo step: only from the video, not tested here. `batch` with `coalesce_parameters` is the documented way.)
- **A user parameter:** `set_parameter` or `parameters.change`. Every expression that uses it follows.
- **Structure:** `timeline.edit {"feature":..., "set":{...}}`, with the field shapes `timeline.inspect` shows.
- **A new feature** goes at the end of the timeline. To place it earlier:
  1. `timeline.roll_to {"position":N}`. A position is safer than a name, since a sketch and a feature can share one.
  2. Add the feature.
  3. `timeline.roll_to {}` to return to the end.

  Everything after the insert recomputes, and a feature that worked can now fail. Seen: a corner fillet after an inserted chamfer.
  - Seen on 0.29.0: a cut failed with "boolean Cut: the operation failed: no result" once a joined plate was inserted before it, because a vertex of the plate and the edge where a chamfer begins fell exactly on the cut tool's wall and top face. Distances up to 19.9 mm worked, 20 mm or more failed. Moving the cut sketch 0.002 mm (`sketch.move {entities,translate:[0,-0.002]}`) made it pass, with a volume change far below tolerance. Tell the user about such a nudge.
- **Adding a fillet to an edited design:** the pick snaps to the nearest edge and fails with "no edge at [x,y,z]: nearest edge is N mm away" when an earlier fillet moved the edge (tested on 0.29.0: after three corner fillets the edge midpoint [300,20,40] had moved to [305,20,40]). Re-pick from `body_topology` (edge `mid`) after every fillet or chamfer. Several edges meeting at one vertex can go in one call or one by one; the result is the same.
- **Risky or multi-step edits:** take `edit.checkpoint` in its own call first. `edit.restore_checkpoint {checkpoint}` goes back exactly. A `batch` rolls itself back; separate `execute` calls do not.
- **Deleting:** `timeline.dependents {feature}` first. It lists what is deleted with it and what would fail.
- **Ambiguous wording:** "2 mm higher" on a value written as `wall + 6` can be relative (`wall + 8`) or absolute.
  - Keep the design's intent, which is the relative reading.
  - Tell the user which reading you used. This matters most when the same request also changes `wall`, because then the two readings give different heights.
- **New constants** such as a chamfer size go in user parameters, so the user can change them later.

## Constraining sketches of an existing design (tested on 0.29.0)
Sketches drawn with `sketch.line` or `sketch.rectangle` come out at dof 4 to 16 and can move when a parameter changes. Close them with `sketch.edit {sketch}` ... `sketch.finish {}`. Check `dof` per sketch with `inspect_design {"measure":false,"sketches":false}`.
- **Anchor to the model:** `sketch.project {refs:[{edge:[x,y,z]}]}` or `{vertex:[x,y,z]}` adds fixed points and lines that follow the model. Then constrain to them: `sketch.constraint.parallel {a,b}`, `perpendicular {a,b}`, `coincident {a:"p1", b:"l4"}` (a point on a line), and `sketch.dimension {entities:["l1.start","l5"], type:"distance", value:"..."}` for a point-to-line distance.
- **Positions from the origin:** `sketch.dimension {entities:["origin","p1"], type:"distance_x"|"distance_y", value:N}`. The value is an unsigned distance, so a point at x = -1 takes `1`.
- **Parameters on the way:** `value:"name = expression"` (for example `"larg_aba = sqrt(60^2 + 30^2)"`) creates the user parameter and dimensions with it. A later dimension can reuse the name as `value:"larg_aba"`.
- **Command shapes that failed once:** `sketch.constraint.horizontal_vertical` takes `line:` (one id per call), `sketch.construction` takes `curves:`, `sketch.delete` takes `entities:` (curves, points or constraints).
- **Wrong end, flipped sketch:** a point-on-line constraint on the wrong end (the point at the far end of a projected edge) makes the solver mirror the whole rectangle. Check the projected points' coordinates with `sketch.inspect` first (which of `p1`/`p2` is which end), and send the dimensions before the position constraint. "the new values would flip the sketch over" means a dimension was given a value that reverses the sketch (for example `0.002` where `29.998` was meant).
- **Do not delete and redraw the lines of a sketch that later features use.** Edge names come from the curve ids (`F27:side:l2`). New curves get new ids (`l6` ... `l9`), so later sketches and fillets report "projected reference lost: edge ... no longer exists; last geometry retained" and "edge ... no longer exists; using the edge at the picked point", and the volume changes with no error. Constrain the lines that are there. After any sketch edit, compare the volume with the baseline.
- **A batch is all or nothing:** if one step fails, `sketch.edit` and `sketch.finish` in the same batch are undone too, and the sketch is left as it was.
- **A call that times out** (the bridge answers after 60 s) may still have run. Read the state with `sketch.inspect` or `inspect_design` before sending it again.


## Verify
1. **Predict, then measure once.** Send the independent changes in one batch, predict the total volume change, then run `measure` once.
   - A move does not change the volume. To confirm a moved sketch, read its points' world coordinates with `sketch.inspect`. You can also predict the COM shift, `Δcom = V_moved · Δz / V_body`, but only when nothing else in that batch changes the volume.
   - If it matches to about 0.01%, you are done.
   - If not, restore the checkpoint, then apply the changes one at a time, measuring after each.
   - A cut or chamfer that leaves the volume unchanged has missed.
2. **Timeline health:** run `inspect_design {"measure":false,"sketches":false}`. Every `error` and `warning` must be null. If something broke, restore or `undo` before you try anything else.
3. **Interior features:** take one top-view screenshot, `{"source":"model","view":"top","width":480,"height":320}`. When the server is bridged, `view` also turns the user's camera. The iso view hides standoffs behind the walls.
4. **Still parametric:** if the user wants it kept parametric, change one driving size, `measure`, then set it back.

## When something is already broken
- **A feature has an `error` after opening:** read it with `timeline.inspect`, fix the input or definition, and recompute.
- **The app crashed:**
  - `crash_reports` lists the reports, and `crash_reports {id}` gives the command that crashed.
  - `execute doc.recovery_list` and then `doc.recover {id}` reopen the autosaved design.
  - Never retry the crashing command unchanged.

## Save
`save {"path":"...-v2.solidcraft"}` writes a copy. `save {}` overwrites the opened file; do that only when the user asked for it.

**File format and older versions.** SolidCraft 0.29.0 saves `solidcraft/46` (seen in a saved design on 0.29.0). The release videos say 0.28 and earlier cannot open it, and that each release from 0.25 changed the native format (41 in 0.25, 43 in 0.26, 44 in 0.27: only from the videos). Keep the original and save the upgraded design as a new name such as `-v2`; a STEP export keeps solids but not sketches or feature history.

## Red flags

| Thought | Do instead |
|---|---|
| "timeline.inspect each feature to understand it" | `parameters.list {"filter":"feature"}` shows every input in one call. |
| "Delete and remodel the feature" | Change its `dN` input, or use `timeline.edit`. History and downstream picks stay intact. |
| "The insert worked, done" | Check the errors of every later feature. |
| "Edge points with expressions, so the chamfer follows the size" | They are rejected, and stored picks already follow size changes. |
| "Pick all 8 rim edges" | One pick on a tangent chain fillets or chamfers the whole chain. |
| "Reuse the old edge point for the next fillet" | After a fillet the edge moved ("no edge at ...: nearest edge is 5 mm away"). Take the new midpoint from `body_topology`. |
| "Delete the sketch lines and draw them again so they constrain cleanly" | Later features reference the curve ids. Constrain the existing lines; a redraw gives "projected reference lost" warnings and a wrong volume. |
| "open the file again to discard my changes" | A changed design that is already open is not reloaded. Copy the file to a new name and open that. |
| "The cut fails, so the model is wrong" | A cut whose tool face, wall or vertex coincides with a vertex or edge of the body can fail ("no result"). Change the distance by 0.1 to see, then nudge the sketch 0.002 mm. |
| "Measure after every edit" | One batch, one `measure` against the summed prediction. Split only when it misses. |
