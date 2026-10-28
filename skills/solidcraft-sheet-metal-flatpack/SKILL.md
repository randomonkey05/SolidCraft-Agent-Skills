---
name: solidcraft-sheet-metal-flatpack
description: Use when modelling flat-pack sheet-metal enclosures in SolidCraft (laser-cut plates with ear tabs, bend slits, perforation, side plates), from real flat patterns, videos or photos, for example a CD-ROM player enclosure.
---

# SolidCraft flat-pack sheet metal (extends solidcraft-sheet-metal)

Load `solidcraft-sheet-metal` first for the base commands. This skill adds the flat-pack method learned on a CD-ROM player enclosure (the das_POD CD-ROM Player 01, second version of the model). Send several screenshots from different views, keep one folder per model and name changes `_v2`.

Background material is in `references/`:
- [`references/flat-pack-dfm-and-bend-formulas.md`](references/flat-pack-dfm-and-bend-formulas.md): design rules for slits, bridges and tabs, bend formulas and K-factors.
- [`references/cdrom-player-das-pod-analysis.md`](references/cdrom-player-das-pod-analysis.md): architecture and dimensions read from the maker's assembly video, and what the reference build did.
- [`examples/cdrom-player-flatpack/`](../../examples/cdrom-player-flatpack/README.md): the two CD-ROM player models (3MF and SolidCraft design files). v1 folds tall walls straight from the base. v2 uses large folded panels with round ear tabs at the screw locations.

## 1. Read the architecture first
- A flat pack is a few flat sheets: 2 main plates joined by a perforated or slit bend line, 2 separate side plates and hardware. Side plates are NOT folded from the base. Check the real flat patterns or photos before modelling: the first version of the CD-ROM model was wrong because the walls were assumed instead of read.
- Typical set: BASE sheet (rear plus bottom), LID sheet (top plus front), 2 side plates, rear panel, fasteners (M3/M4 plus nut), feet, placeholders for internals.
- Dimensions taken from video frames or photos carry about +-8-10 %. Say so. Spoken numbers are unreliable. Use a known part as the scale (a 5.25" drive bezel is 148 mm wide).
- If real flat patterns are supplied later, diff them against the model list: perforation, windows and grids, steps, ear count and positions, feet and fan holes, relief notches, part count.

## 2. Build recipe that works
Constants used: t 1.5, R 1, K 0.4, BA 2.5133, outer setback 2.5, outer mould corner at b+1.2433, inner at b-0.2567.
1. Base flange from the full outline (with relief notches at the lip corners).
2. Main folds first, ordered from the fixed side outward (near to far). A fold whose moving side already has a bend is refused (`fold through a flange's bend`). `sheet.fold` is a half-plane fold: it bends everything beyond the line.
3. Edge flanges for lips and ears (height 30, 90 deg, `height_from` outer, `position` inside). The default direction is toward the sheet's BOTTOM-face normal. Use `flip:true` for the opposite and verify with the bbox. Overlapping lips at a corner give `sew: ambiguous edge contact`: fix it with notches in the base outline.
4. Anything that crosses bends or non-parallel panels: `sheet.unfold`, cut sketches in flat coordinates (plane at z = zoff-1, extrude through t), `sheet.refold`. Cuts on folded bends are refused.
5. The fold line must be on a flat face and the bend zone free of outline corners. On later folds the bottom-face offset from neutral is 0.9 if the previous bend was "+" and 0.6 if it was flipped.
6. Place the sheets with `component.from_bodies` plus `occurrence.move`. In the reference build the matrix of `occurrence.move` in world space COMPOSED with the current transform instead of replacing it, so test once and measure before relying on absolute positions. Group colours: Aluminum - Satin for plates, Aluminum - Anodized Black for side plates.

## 3. Ear tabs (round, bolted) and bend slits
- Tab: about 34 long x 21 wide with a fully round tip R10 (R10.5 in the CD-ROM model) and a hole of 2.5-3.2 mm about 20 from the edge (M3 plus nut in the CD-ROM model).
- Make the flanges for the full length, unfold, cut the gap between ears with the round tip radius plus two bend slits (slot width = BA, for example 2.5133, slot centre-to-centre about 3.8 long, pitch about 9) plus the hole, then refold.
- Slots on the bend line are real cuts in the unfolded state (sketch on XY, extrude = t). Slot corners get a radius >= 0.2-0.5, the bridge is about 1-1.5 t and the slot width about 1.2-1.5 t for hand bending (see [`references/flat-pack-dfm-and-bend-formulas.md`](references/flat-pack-dfm-and-bend-formulas.md)). Perforated bend lines run only part of the width (keep about 14 mm uncut at each end).
- Do NOT rely on slits alone: add tabs and slots that lock at the final angle.

## 4. Perforation and vents
- Cut real holes. `sheet.perforate` does not cut the B-rep. Budget: about 700 holes in one sheet (flat plus folded cuts). Beyond that you get `flat geometry exceeds the bounded processing budget` or `planar boolean sampled geometry exceeds its budget`. Chunk the cuts into <= about 480 holes per extrude. The last 224 failed after 476 plus 224. Accept a partial pattern and state it, or use a larger pitch.
- Use one sketch with all circles or slots and one extrude per chunk. Start the cut planes 1 mm outside the sheet.

## 5. Assembly and checks
- Fasteners, feet and standoffs: one component with copies. Mirror side plates only if they are symmetric about their plane, otherwise use `solid.mirror`.
- `inspect.interference` is slow with about 70 bodies (a full run hit its 40 s budget with 113 pairs unchecked). Pass `bodies:[...]` with the few bodies you moved, sheet pieces last because they are the slowest (30-60 s each). A call can exceed the 60 s device limit and still finish in the app: call `running`, then wait. Do not resend.
- Typical clashes: internals against stepped front or bottom, screw heads against lips, an I/O board against recesses. Fix placeholders by cutting (sketch plus extrude cut) or moving them, not by changing the plates.
- Old components of replaced parts stay in the Bodies list. Delete them with `component.delete` or `timeline.delete` of their sketches (this can take about 3 minutes: wait, do not resend).
- Save a checkpoint before risky operations. Export the design file, `.3mf` and `.stl`, and take screenshots from several views (`view.apply` with `view:"back"` or `camera:{target,distance,yaw,pitch}`, no `up`).

## 6. Simplifications to declare in the report
Slit rows on bends, narrower sections and strip flaps, rounded plate corners, logo emboss, partial perforation, keyhole slots. Always list the differences from the real flat pattern and what was simplified.
