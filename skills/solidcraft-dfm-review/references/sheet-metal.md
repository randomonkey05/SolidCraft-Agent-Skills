# Sheet-metal review

## Sources (start here when the user supplies no shop spec)
- Hubs, Sheet metal fabrication design guide: https://www.hubs.com/guides/sheet-metal-fabrication/ (K factor, bend allowance, bend radius and relief, hems, hole and edge spacing, kerf, welding, tolerances).
- Protolabs sheet-metal design guidelines: https://www.protolabs.com/services/sheet-metal-fabrication/design-guidelines/ (component size, material and thickness range, tolerances, flange, hem, relief and hole rules).
Read the current tables for the exact stock and tooling. Do not import a universal minimum radius or flange length.

**If the shop is SendCutSend**, their own limits replace these starting points: continue with [sendcutsend.md](sendcutsend.md), which gives the per-SKU limits and the scripts that measure the DXF you would upload.

## Inputs to collect
Alloy and temper, nominal thickness and units, cutting and forming process, critical dimensions, any shop bend table or tooling. Ask only for what changes the decision; otherwise state a provisional assumption.

## Checks
1. **Constant thickness.** Does each body represent sheet of constant thickness? Compare the matched inner and outer faces; a bounding box is not a thickness measurement. In SolidCraft a body made by `sheet.flange`, `sheet.fold` or `sheet.convert` carries its rule: read it with `sheet.rules`.
2. **Bends.** List each bend with inside radius, angle and flange length. Distinguish inside from outside radius. Compare with the shop's radius for that thickness: it comes from tooling and is not adjustable.
3. **Features near bends.** Compare hole-to-bend, slot-to-bend and relief dimensions with the shop's rules, after stating the convention (bend tangent, bend centreline or edge).
4. **Flat cutting.** Closed contours, no duplicate or intersecting curves, correct units, small features against the cutter's limits. A projection of a bent solid is not an unfolded blank: use `sheet.flat_pattern` or `sheet.export_dxf`, and measure the exported file with `scripts/dxf_facts.py` (units, closure, duplicates, smallest hole, bend-line lengths).
5. **Bend allowance.** BA = angle (radians) x (inside radius + K x thickness), only with a stated convention and a K factor from the shop or a bend table. A guessed K factor is not a production dimension. For small parts compare the flat length with the shop's own flat pattern.
6. **Forming feasibility.** Bend order, tooling access, hems, hardware, grain direction and collisions are `unverified` unless tooling is known. A valid STEP solid does not prove the part can be formed.
7. **Flat-pack and perforated bends.** Slots and bridges along a bend line weaken it: not for structural bends. See `solidcraft-sheet-metal-flatpack`.

## Worked example (illustrative numbers, not default limits)
A hole is 3 mm from a bend tangent, but the shop gives a 5 mm minimum measured from that same tangent: report a 2 mm shortfall and propose relocating the hole or a shop-approved relief. If the drawing instead dimensions from the bend centreline, resolve the convention first.
Measure it in SolidCraft with `measure` on two items (the hole's cylindrical face and the bend face or edge) and read `min` and `center_distance`.
