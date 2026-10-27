---
name: "solidcraft-assemblies"
description: "Use when building multi-part assemblies in SolidCraft, static or moving (rovers, linkages, robots, enclosures): minimise distinct bodies, reuse and mirror instances, and keep moving parts collision-free."
---

# SolidCraft assemblies: repeatability first, no collisions in motion

Applies to any assembly: static (enclosures, frames, fixtures) and moving (linkages, suspensions, legs, arms). The goal is an assembly that is easy to edit later: change one body and every instance follows.

## 0. Housekeeping
- One folder per model, all its files inside. Changes go in the same folder under a new name (`model_v2`); never overwrite earlier versions. If your setup restricts where the app may save files, create the folder first.
- Always deliver a screenshot of the result (and, for moving assemblies, one in a non-home pose).
- Reply in the user's language.

## 1. Plan repeatability BEFORE modelling
Write a short part table first: part type, how many instances, how each instance is derived. Target: number of distinct bodies = number of part types, not number of physical parts.

Look for, in this order:
1. **Identical parts** -> one component, N instances (wheels, fasteners, standoffs, identical links, brackets).
2. **Mirrored parts** -> model one side only; the other side is a mirror instance (left/right suspension arms, left/right brackets). Only create a genuinely separate body if the part is NOT a mirror image (different features, handedness-specific features).
3. **Symmetric parts** -> if a part is symmetric about its own mid-plane, a plain translation or rotation of the instance is enough; no mirror needed.
4. **Patterns** -> rotational or linear repeats (3 or 4 legs, 6 wheels, bolt circles) are instances of one component placed by matrix.
5. **Single rigid bodies that span several places** (a chassis, a frame, a rocker plate connecting several joints) stay ONE body. Do not split it into pieces, and do not replace it with several lookalikes.
6. **Parametrise** shared dimensions (wheel diameter, link length, track width) with parameters so one edit propagates.

Example, lunar rover: 1 wheel body x 6, 1 hub/motor body x 6, rocker arm A + mirror for the other side, bogie arm A + mirror, 1 chassis. Not 6 wheels, not 2 different arms for the same function.

Sanity check before building: could a user edit one body and expect all copies to change? If yes, they must be instances.

## 2. Building instances
- Build the part once in its own component, in a convenient local frame (origin at the joint axis or the part centre), then `occurrence.copy` + `occurrence.move` with a rigid 3x4 matrix (row-major). Use `"tolerance": 1e-6` on `occurrence.move` to avoid 'matrix is not rigid' errors.
- Mirror instances use a reflected matrix (determinant -1), e.g. mirror about XZ: diag(1,-1,1). If the move command refuses reflections, use the mirror feature/component mirror instead; do not rebuild a second body by hand.
- Planar parts: model flat, thickness along the stack axis, and offset instances along that axis; only flip parts that are not symmetric about their own plane.
- Sketches on a custom plane: pass an explicit plane `{origin, x_dir, y_dir}` instead of a named plane when orientation matters (named planes can flip an axis).
- Keep names meaningful (`Wheel`, `RockerArm`, `RockerArm_mirror`) so the browser tree reads like the part table.

## 3. Static assemblies
- Place parts with exact coordinates from the part table; verify with `measure`/bounding boxes, not by eye.
- Check interferences between touching parts (shared faces are fine, overlapping volumes are not). Fasteners and holes: same instance pattern, same hole spacing from one parameter.
- Keep clearance consistent (e.g. 0.2-0.4 mm for printed parts) via one parameter.

## 4. Moving assemblies (mechanisms)
**Core rule: moving parts must not collide with each other or with fixed parts at any point of the motion.**

Design rules
- **Layer map**: for planar linkages, give every moving link its own layer along the rotation axis (distinct coordinate on that axis, >= 1 mm gap between neighbours). Make the layer table (part -> axial position) before building.
- **No pins in the middle of the working plane**: a pin or bar belonging to a part must lie outside the layers of the parts that sweep across it. If one rigid body connects several joints, make it ONE body with its pins/bars extending axially outside the moving layers, rather than several bodies with pins in the middle.
- Fixed parts (chassis, frame) sit outside the moving layer range, with stubs/pins only where a joint needs them.
- Pins and holes: pin diameter < bore by the clearance parameter; shoulders/washers to hold the axial position.

Joints
- Put parts in their start pose first, then create joints with `joint.as_built` (type `revolute`/`rigid`/`slider`, `a`/`b` occurrence ids, `at: {point, z: axis}`, `quiet: true`). The joint axis `z` must equal the real rotation axis.
- Ground only the fixed part. Each moving occurrence should end with the expected degrees of freedom (normally 1 in a single-DOF mechanism; check the `dof` list).
- Several drives that must stay in sync: `joint.motion_link` with ratio/offset.
- Drive with `joint.drive {joint, value}`.

Verification (mandatory)
1. Drive through the full range (for a rotary input: 0, 90, 180, 270, 360 deg and back to 0). Fine steps for tight mechanisms.
2. Each result must have `conflicts: []`, `errors: []`, `stopped_by_contact: null`, `stopped_by_loop: null`.
3. After returning to the start, positions match the start pose (check with `occurrence.properties` bounding boxes).
4. Check clearance of the moving parts against each other and against the fixed parts across the sweep, not just in the home pose. If something touches, change layers/offsets/part geometry, not the motion.
5. Check the end result still has the minimum number of distinct bodies (count bodies in the browser).

## 5. Finishing
- Colour by body (`appearance.assign` with `bodies: [names]`), so all instances share one colour; make fixed housings semi-transparent so the mechanism is visible.
- Hide joint glyphs for screenshots (`browser.visibility` with the joint names, `visible: false`).
- Set the camera with `view.apply`, take the screenshot, return the mechanism to its home pose, save, export STEP.
- In the final message: number of distinct bodies vs. total instances, which parts are mirrored/shared, how to animate it, files, known limitations.

## Pitfalls
- Do not model both sides separately 'to be safe'. Mirror or instance.
- Do not split a single rigid part into several; do not merge parts that must move relative to each other.
- A batch with one invalid command rolls back entirely; fix and resend.
- Do not kill processes by pattern in the shell (it can kill your own session).