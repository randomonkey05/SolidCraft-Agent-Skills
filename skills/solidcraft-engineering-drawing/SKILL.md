---
name: solidcraft-engineering-drawing
description: Use when asked for an engineering drawing, a dimensioned sheet, a shop drawing or "2D views" of a SolidCraft part: what a manufacturing drawing must contain, how to get views, dimensions and flat patterns out of SolidCraft, the classic SolidWorks A2 sheet template, which placeholder bodies to omit, and a read-back checklist.
---

# Engineering drawings from SolidCraft

The content checklist is adapted from the `engineering-drawing` skill of earthtojake/text-to-cad (MIT, see NOTICE). That skill generates a PDF through its own `cadgen` engine, which SolidCraft does not have, so this skill covers what a drawing must contain and what SolidCraft can supply. SolidCraft 0.25.1 does not lay out a dimensioned ISO sheet by itself, so the sheet comes from `assets/sheet-template-a2.dxf`.

A drawing is a document derived from the part. Every number on it should come from the model (measured), not retyped, so that changing the model changes the drawing.

## What SolidCraft can supply
- **View linework (verified).** `view.apply {view: "top"}` returns the camera. Pass that exact camera object to `file.export_view_dxf {camera, hidden: "dashed", path}`: `camera` is required, and a shortened or hand-made camera was rejected as "invalid camera". The result is an orthographic DXF in mm (`$INSUNITS` 4) with layers `VISIBLE` (LINE) and `HIDDEN` (LWPOLYLINE, dashed); sketch curves go on `SKETCH`. Export one file per standard view (front, top, right, plus iso if useful).
- Curves are tessellated into short segments (a top view of a bolt and a bearing gave about 1,500 visible lines). Raise `tolerance` (0.01 to 0.1 mm) if the file is too heavy for the drafting tool. The segments are not dimensionable arcs, so dimensions must be added from measured values, not from the exported curves.
- **Flat pattern** for sheet metal: `sheet.export_dxf` (layers OUTLINE, CUT, BEND_UP, BEND_DOWN, BEND_NOTES) and `sheet.export_bend_table` (CSV). Send these as the manufacturing drawing for laser-cut and bent parts.
- **Numbers**: `measure` for overall size, hole diameters, centre distances, wall thickness; `inspect_design` for parameters.
- **Sketch outlines**: `sketch.export_dxf` for a single profile.

## What a good drawing contains
1. **Sheet**: ISO size (A4 297 x 210, A3 420 x 297 mm), frame, third-angle projection unless the shop works in first angle (state it).
2. **Views**: enough to define the part: usually front, top and right, plus an isometric in the free corner for orientation. Hidden lines dashed where features are behind faces. Centre marks on every hole and revolved feature. No dashed tangent edges for fillets or cylinder seams.
3. **Dimensions**, measured from the geometry, placed where the feature is visible: overall size in each view, feature positions and sizes, then holes as callouts (through or depth, counterbore, countersink, thread such as M3x0.5). Add a tolerance or fit only where the function requires one. Dimension each feature once. Do not chain tolerances in a way that accumulates.
4. **Notes**: numbered, few and short. Put the general tolerance as note 1 (the standard and class, for example ISO 2768-m). Add edge treatment ("break sharp edges"), finish, heat treatment and the material and thickness here if not in the title block.
5. **Title block**: title, part number, material, author, scale, units (mm), projection symbol, revision, sheet n of m, date.
6. **Sheet-metal parts**: add the flat pattern with bend lines and a bend table (angle, direction, inside radius), the K factor used, and the material and thickness.
7. **Assemblies**: a parts list with item numbers, quantity, part number and description, and balloons on the view. Hardware from `solidcraft-step-parts` goes in as standard parts with their designation (ISO 4762 M3x12).

## SolidWorks-classic sheet (house format)
The user's preferred drawing format is the classic SolidWorks A2 sheet. A ready template and a worked example are included:
- `assets/sheet-template-a2.dxf`: empty A2 sheet (mm, `$INSUNITS` 4); other sizes (A4 portrait, A3, A1) come from the script. A2: outer frame 15..589 x 5..415, inner frame 20..584 x 10..410 (outer 5 mm from the sheet edge, inner 5 mm further, same on every size), zone ticks every 50 mm (columns 12..1 right to left, rows A..H bottom to top), title block 180 wide, 404..584 x 10..65.2 with DRAWN / CHK'D / APPV'D / MFG / Q.A, NAME / SIGNATURE / DATE, FINISH, MATERIAL, WEIGHT, TITLE, DWG NO., REVISION, SCALE, SHEET n OF m, size "A2", the "unless otherwise specified" block (dimensions in millimetres, surface finish, linear and angular tolerance) and "DEBURR AND BREAK SHARP EDGES". Regenerate with a size, title and scale: `python scripts/make_sheet_template.py out.dxf --size A2 --title NAME --scale 1:10 [--material ...]` (needs `ezdxf`). The educational watermark of the source file is deliberately not copied.
- `references/playseat-wood.DXF` and `references/playseat-wood.STEP.gz` (gunzip first): the SolidWorks 2026 export that the template was taken from, and the model it shows. Use it to see how a full sheet is laid out. It is a reference for the format, not a part to reuse.

General assets inside the DXF (reusable as they are):
| Asset | Detail |
|---|---|
| Dimension arrow | block `_Closed`: closed triangle drawn with lines, 1 unit long, half-width 0.17, tip at the origin; `dimasz` 3.556 scales it |
| Leader end dot | block `_Dot`: tiny closed polyline plus a 0.5 stub, `dimasz` 0.762; used where a balloon leader ends on a face |
| Dimension style | text style `SLDTEXTSTYLE0` (font TXT), text height 3.5, gap 0.875, 2 decimals, text above the line (`dimtad` 1), horizontal text, extension offset 0 / extension 0, arrows `_Closed`, `dimlfac` = scale denominator (10 for 1:10) so the number shown is the model value |
| Leader styles | `SLDDIMSTYLE1` (default arrow, no text gap) for balloon leaders, `SLDDIMSTYLE2` (`_Dot`) for leaders that end inside the part |
| Balloon / note | `SW_NOTE_0_n` blocks: MTEXT height 1.5 (title block) or a circled item number (balloons) |
| View arrow | `SW_PROJECTIONARROW_0` (section/view arrows with a letter, 3.5 high) and `SW_SYMBOL_VIEW_CTRWISE` (circular direction symbol) |
| Dimension blocks | each DIMENSION points to a block `_D_n` made of the two extension lines, the dimension line cut into two segments around the text, and the text |
| Linetypes | HIDDEN (dashed), CENTER, PHANTOM, DOT2; layer `FORMAT` (frame and title block) and `0` for everything else |

## Sheet and view layout rules (not fixed)
The reference sheet is one example, not a layout to copy. Decide the layout for each model:
- **Sheet size and orientation**: A4 to A1. A4 is portrait (210 x 297); A3, A2 and A1 are landscape. The title block (180 x 55.2) always sits in the bottom-right inner corner, so it also fits the 180 mm inner width of a portrait A4.
- **Zone grid**: zones are always 50 mm, whatever the size. A smaller sheet has fewer zones (A4: 4 columns x 6 rows, A3: 8 x 6, A2: 12 x 8, A1: 18 x 12). Ticks sit at the sheet centre +/- 50 mm steps; the end zones are the remainders. Columns are numbered right to left, rows lettered bottom to top. `scripts/make_sheet_template.py --size A4|A3|A2|A1` does this.
- **Isometric view**: fixed in position, in the upper-right corner of the sheet. Its scale (and the scale of the other views) is adjusted so that everything fits on the sheet; state the scale in the title block, and mark any view with a different scale.
- **Which views to show**: choose the views that show the most information about the part (not always front/top/right; a side view plus a cut panel can be enough). Do not add a view that repeats what another already shows.
- **Hidden lines (dashed, "picotado")**: use them only when parts or features hidden behind a face matter for understanding. In that view the hidden geometry shows through as dashed lines, as if the face were transparent. Do not dash everything by default.
- **Assemblies**: the separate parts can go on the same sheet or on an adjacent sheet, depending on the size of the assembly and the number of different parts. Sheet numbering ("SHEET n OF m") and the parts list/balloons tie the sheets together.
- **Balloons and dimensions**: balloons number the items as in the parts list; a balloon leader ends with `_Dot` on the part. Dimensions sit outside the view with extension lines, overall first, then features, one per feature.
- To build it from SolidCraft: export each view with `file.export_view_dxf`, place it inside the inner frame at the chosen scale, add dimensions with the style above, fill the title block, and check that nothing overlaps the title block or leaves the frame.

## Placeholder bodies: omit from drawings until told otherwise
Some bodies in an imported or assembled model are placeholders, not parts to manufacture: bodies that stand in for the user, equipment or bought items and give size and ergonomics (seat occupant, monitor, steering wheel, pedals, shifter, mounting plates of bought equipment, anything imported from a mesh/IGES with an anonymous name). Rule: **leave placeholder bodies out of drawings, views, balloons, parts list and bill of materials, unless the user asks for them.** Show only the fabricated parts (for example the wood panels). If a placeholder is needed to understand the layout, ask first or show it as a phantom-line (CENTER/PHANTOM) outline.
How to tell them apart: fabricated panels are plain boxes (6 faces, constant thickness) or simple profiles with few faces; placeholders have hundreds of faces, organic or tiny shapes, or sit far from the structure. STEP names do not help (the reference file names every body "playseat 999.igs<1>"), so decide from geometry and confirm with the user the first time.
In the reference model `playseat-wood.STEP` (22 solids) the plain wood parts are the boxes (for example 1220 x 610 x 10 base, 1500 x 35 x 70 rails, 540 x 20 x 35 cross pieces). Candidate placeholders by geometry (not yet confirmed by the user): the 404-face body of about 54,000 cm3 (occupant/seat form), the two 65-face bodies of about 66 x 155 x 101 mm (pedals), the 57-face body of 16 cm3, the 43-face body 713 mm wide (monitor/wheel), and the small plates and post (3 mm thick 240 x 240, 120 x 120, 40 x 40 x 454). Ask the user to confirm this list when a drawing of this model is requested.

## Read-back checklist (before handing over)
- No dimension text sits on a view line; no leader crosses the part.
- Every hole has a centre mark and a callout; small dimensions (a few mm) are dimensioned on the larger feature or on an extension line.
- Hidden lines appear where they should, not where a tangent seam sits.
- The dimensions agree with `measure` on the model (check three at random).
- The scale and the units are stated, and the views are not mixed scales.
- Revision and date match the saved design name (`name_v2`).

## Producing the document
The agent can build the dimension schedule and notes (Markdown, a table in a document or spreadsheet) and hand over the DXF views. If the user wants a finished PDF sheet, say that SolidCraft has no sheet layout, and offer: (a) the DXF views plus a dimension table, to be laid out in a drafting program, or (b) a PDF built from the views and the measured table. Say which one you made.

## Source
Upstream skill: https://github.com/earthtojake/text-to-cad/tree/main/skills/engineering-drawing
