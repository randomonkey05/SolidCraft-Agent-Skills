---
name: solidcraft-delivery-gate
description: Use before telling the user that a SolidCraft model, export or drawing is finished, ready to print or ready to send: checks that final files are fresh, non-empty and match the last measured design, re-checks holes, pockets and gears against the reference values, and separates verified from unverified claims.
---

# Delivery gate

An export that succeeded only proves a file was written. Check the final files, not the working design, before saying "done".

(Idea source: the final-verification, artifact-inspection and evidence-ledger gates of capwitf/mechanical-cad-skills, MIT. Rewritten for SolidCraft; no text copied.)

## Checks on the final files

| Check | How |
|---|---|
| Exists and is fresh | every promised file is in the model's folder and newer than the last design change; no leftovers from an earlier version (new versions get a new name, e.g. `_v2`) |
| Non-empty | size > 0; STL: triangle count > 0 and a bounding box; DXF: entity count by type and layer names; PDF: page count; STEP: header and entity count |
| Matches the design | bounding box and volume of the export (re-open the STEP in SolidCraft, or parse the STL/DXF) agree with the last `measure`, in mm |
| Final look | `screenshot` of the model (iso, plus top or underside when features hide there) and send it to the user |
| Source can regenerate | the saved `.solidcraft` or the parameter list is next to the exports |

Limits to remember:
- Reading a STEP as text proves a STEP container with entities, not valid solid geometry. Re-open it to confirm.
- STL triangle count and bounding box do not prove a watertight, printable mesh.
- DXF entity counts do not prove dimensions or layers are right; compare with the flat size you computed.
- A PDF or screenshot never proves the native design is healthy.

## Extra checks for holes, pockets and gears
When the final design has screw holes, tapped holes, counterbores, slots, pockets or spur gears, re-check them on the final geometry against the values in `solidcraft-hole-fastener-rules`:
- smallest hole edge distance, web between holes, wall, and remaining floor under pockets and counterbores (measured from the model, a section or a top-view screenshot);
- hole type per hole (clearance, counterbore or tapped) and, for tapped holes, whether the model carries the thread or only the tap drill;
- for a gear: single solid, bounding box equal to the tip diameter, bore diameter, face width.

A value measured on the final design is **Verified**. A value taken from the build parameters is **Inferred**. A value with no known process or load behind its limit is **Unverified**: say which starting value was used and that it still needs confirming.

## Process limits: where to look
This skill holds no design-for-manufacturing numbers of its own. Take the process from the design lock (see `solidcraft-requirements-and-sanity`), load the skills for it, and check the final geometry against what they say. Do not rely on memory of their values.

| Process or feature | Load |
|---|---|
| FDM print | `solidcraft-3d-print-dfm` (walls, overhang, bridges, clearances, orientation, bed; `references/process-limits.md` for published limits) |
| Bent sheet metal, building it | `solidcraft-sheet-metal` (rule, bend radius, relief, flat size, DXF) |
| Flat-pack sheet metal | `solidcraft-sheet-metal-flatpack` (tabs, bend slits, perforation budget, declared simplifications) |
| Sheet metal or CNC manufacturability, or a DXF going to a shop | `solidcraft-dfm-review` (evidence per feature; SendCutSend per-SKU limits) |
| Holes, slots, pockets, edge distance, web, wall (any process) | `solidcraft-hole-fastener-rules` |
| Spur gears | `solidcraft-hole-fastener-rules`, section 3 |
| Real screws, nuts, bearings, standoffs, motors | `solidcraft-step-parts` (catalogue dimensions instead of guessed ones) |
| Several parts, instances, static clearances | `solidcraft-assemblies` |
| Joints, motion, closed loops, degrees of freedom | `solidcraft-mechanisms`, plus the verification sweep in `solidcraft-assemblies` |
| Exact STEP comparison, parameter ranges, regression tests | `solidcraft-checking` |
| A drawing or dimensioned sheet is a deliverable | `solidcraft-engineering-drawing` (read-back checklist) |
| Built from a drawing under time pressure, or the build crashed or hung | `solidcraft-speed-modeling-lessons` |
| Process or material still unknown | `solidcraft-requirements-and-sanity`; until it is answered, those rows stay Unverified |

Filling gaps between skills:
1. Check every applicable row of the table, not only the first skill that matches. A printed part with screw holes needs both `solidcraft-3d-print-dfm` and `solidcraft-hole-fastener-rules`; a laser-cut part with screw holes needs `solidcraft-dfm-review` and `solidcraft-hole-fastener-rules`.
2. If the process skill has no value for a feature (for example hole edge distance in a flat-pack plate), take it from the next skill in the table and say where it came from.
3. If two skills give different limits for the same feature, use the stricter one and name both.
4. If no skill has a value, mark the claim Unverified and list the missing value under open risks. Do not invent a limit, and do not edit another skill from here: report the gap so it can be added there.

## Optional manifest
For files that go to other people, write `<model>_manifest.json` next to them: file name, size, modified time, SHA-256, the source design, tool versions, checks actually run, and the three claim lists below. Only record checks that really ran.

## Report shape
Keep it short:
1. Final files (names, in the model's folder).
2. **Verified**: checked directly on the final files.
3. **Inferred**: likely from the build logic, not measured.
4. **Unverified**: not checked or blocked, with the next smallest action.
5. Open risks.

Do not write "all good" unless every required check passed.

## When a check fails
Name the check, classify the cause (stale file, export failed, blank result, wrong format, geometry, missing tool), fix the design rather than the preview, re-export, and re-check from the new file.
