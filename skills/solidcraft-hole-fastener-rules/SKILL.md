---
name: solidcraft-hole-fastener-rules
description: Use when a SolidCraft part needs screw holes, tapped holes, counterbores, slots, pockets or spur gears and you need starting values: clearance and tap-drill sizes, hole edge distance, web and wall minimums by process, and spur gear formulas. Reference data for the requirements, sanity and delivery checks; confirm per process before relying on it.
---

# Holes, fasteners, pockets and spur gears: reference values

This skill holds data, not a procedure. The checks that use it live in `solidcraft-requirements-and-sanity` (before building) and `solidcraft-delivery-gate` (before delivering).

(Idea source: wzyn20051216/solidworks-automation-skill, MIT. Process values there are initial suggestions for CNC, sheet metal and plastic parts; restated here, not copied. Confirm against the real process, supplier and load.)

## 1. Decide the hole type before modelling
"An M5 screw hole" is ambiguous. State or ask which one it is, and never default it to a tapped hole:
- **Clearance** (through, screw passes freely)
- **Counterbore or countersink** (head sits below the surface)
- **Tapped** (the thread is cut in the part)

Starting diameters, mm:

| Thread | M3 | M4 | M5 | M6 | M8 | M10 | M12 |
|---|---|---|---|---|---|---|---|
| Clearance hole, ISO 273 medium | 3.4 | 4.5 | 5.5 | 6.6 | 9 | 11 | 13.5 |
| Tap drill, coarse pitch | 2.5 | 3.3 | 4.2 | 5.0 | 6.8 | 8.5 | 10.2 |

Other pitches, plastics or soft metals need the tap chart for that case; do not assume the table holds.

Tapped holes:
- The drilled hole must be smaller than the nominal thread; a counterbore must be wider than its through hole.
- Starting thread depth about 2 x the nominal diameter; check that thread engagement is at least 1.5 x the nominal diameter. A blind drill must be deeper than the thread depth.
- A small mouth chamfer (about 0.3 mm for M3 up to 1.2 mm for M12) helps the tap start.
- Find out how SolidCraft represents threads (`list_commands` with a filter such as `thread`). If only the tap-drill hole is modelled, write that in the notes: the model carries the tap drill, not the thread.
- A flat-bottom blind hole has no drill point, no incomplete thread zone and no tap run-out or chip room. It is a good model of the hole, not a finished tapping design.

## 2. Starting values to confirm per process
Hole edge distance is measured from the hole edge to the part edge. State whether a ratio multiplies the hole diameter or its radius.

| Part type | Min wall or thickness | Hole edge to part edge | Web between holes |
|---|---|---|---|
| Machined bracket | 1.5 | 0.75 x diameter, at least 2 | 3 |
| Machined drilled panel | n/a | 1 x diameter, at least 3 | 3 |
| Sheet-metal panel | 0.8 | 1 x diameter, at least 2 | 2 |
| Injection-moulded shell | 1.0 (smallest feature 0.8) | 0.5 x diameter | n/a |

Other starting values:
- Machined mounting plate: at least 4 thick (8 as a default), pocket side wall at least 3, pocket floor at least 2, slot end radius at least 1.5.
- Holes under 3 mm in machined parts: warn (drill stiffness, chips). Holes under 1.5 mm in moulded parts: warn (fragile core pin).
- Where a sibling skill gives its own numbers (`solidcraft-3d-print-dfm`, `solidcraft-sheet-metal`, `solidcraft-sheet-metal-flatpack`), use the stricter value and say which one you used.

## 3. Spur gears
Ask for module, number of teeth, pressure angle, face width and bore. For a part that will be made, do not invent them; for a visual demo, defaults are fine if the reply says so.

Standard full-depth external spur gear:
- pitch diameter d = m x z
- base diameter db = d x cos(alpha)
- tip diameter da = d + 2m
- root diameter df = d - 2.5m
- tooth thickness on the pitch circle = pi x m / 2
- centre distance of a mating pair = m x (z1 + z2) / 2

Check undercut risk when the root circle falls below the base circle; at 20 degrees that starts at roughly 17 teeth or fewer.

Not covered without a specialist route or an engineer: helical, bevel, internal, rack, worm, profile-shifted gears, backlash, tolerance grades, strength, and a true hobbed root shape. A gear that measures right (single solid, tip diameter, bore, face width, volume) is not production ready.

## 4. Report
List the hole types chosen and which values are starting values still to confirm.
