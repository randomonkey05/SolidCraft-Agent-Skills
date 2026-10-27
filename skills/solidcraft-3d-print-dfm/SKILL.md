---
name: solidcraft-3d-print-dfm
description: Use when designing any SolidCraft model meant for FDM 3D printing (written for a Bambu Lab A1 mini): wall, overhang and clearance rules, print-in-place hinges, orientation and pre-export checks.
---

# FDM design-for-print checklist (SolidCraft -> desktop FDM printer)

Written for a 0.4 mm nozzle on a Bambu Lab A1 mini (180 x 180 x 180 mm bed). The rules come from a public DFM guide (Unionfab, 2026) plus lessons from real prints. Items marked (UNVERIFIED) are working values that no real print has confirmed yet. Adjust them to your own printer and tell the maintainers what you measured.

## Before modelling
- Decide the PRINT ORIENTATION first and model in that pose (flat face on Z=0). Layers are weakest along Z, so loads must not pull layers apart.
- Keep the part inside about 170 mm on the A1 mini bed. Avoid tall thin features.
- Prefer a self-supporting design over supports. Target: no support at all.

## Geometry rules (0.4 mm nozzle)
- Walls: minimum 0.8 mm, in multiples of 0.4 (0.8, 1.2, 1.6, ...). Structural plates >= 2 mm. Thin tall plates need ribs or gussets rather than more thickness.
- Overhangs: <= 45 deg from vertical. Use 45 deg chamfers or teardrop profiles under horizontal holes and lips.
- Bridges: unsupported spans <= about 5 mm.
- Horizontal holes print slightly oval and undersize: add about 0.2 mm radius or use a teardrop. Vertical holes are more accurate. (compensation value UNVERIFIED)
- Features smaller than the nozzle (< 0.4 mm) are dropped. Keep >= 0.4-0.5 mm between separate features unless it is an intentional clearance.
- Text and embossing: >= 0.5 mm deep or high.
- Fillet or chamfer the bottom edges of large flat bases to reduce warping and elephant foot.
- Use ribs for stiffness instead of thick walls, and keep thickness uniform.

## Clearances
- Sliding or mating parts: 0.2-0.5 mm gaps, never zero.
- Print-in-place hinges: radial and axial gap 0.4 mm (UNVERIFIED), layer height <= 0.20 mm (0.16 is better), supports OFF, pin/bore axis horizontal, 45 deg chamfer or teardrop on bores > 6 mm. Fuse the pins to ONE part and put the bore on the other.
- Bodies that must stay separate must not touch: keep them as separate bodies (no join) and check with `measure` that they do not overlap.

## SolidCraft build notes
- Build prisms from side profiles (sketch on the YZ or XZ plane) extruded symmetrically. Avoid cones plus spheres (drafts and spherical faces hang the boolean kernel, see `solidcraft-sweep-and-boolean-hangs`).
- Joins need real overlap. If a join reports that it cannot preserve the original faces, draw one combined profile instead of joining.
- Check polygon vertex order: a self-crossing polygon becomes two profiles.
- Export one folder per model with the design file, `.3mf`, `.stl`, a preview image and short notes. 3MF exports one object per body. Bambu Studio then asks whether to load it as one object with several parts: answer yes for assemblies.

## Slicer advice to hand over with the model (Bambu Studio)
- Print-in-place: 0.16-0.20 mm layers, supports OFF (or build-plate only and checked in the preview), 3-4 walls for thin plates.
- Avoid the 0.28 mm "Extra Draft" profile for parts with 0.4 mm gaps.
- After slicing, inspect the preview for support material inside gaps.

## Final review before handing over the model
1. Minimum wall >= 0.8 mm everywhere, including at fillet and hole edges.
2. No overhang > 45 deg without a chamfer, and no bridge > 5 mm.
3. Gaps are present and not filled (check a section view).
4. The part fits the bed, has a flat first layer and no tiny floating bodies.
5. Send an isometric preview plus notes on orientation and slicer settings.
