# Example: two sheet-metal tutorials rebuilt in SolidCraft

Rebuilds of the two silent sheet-metal tutorial videos by the YouTube channel [Elite Engineers](https://www.youtube.com/@elite_engineers): a **phone stand** (contour flange plus cuts made in the flat state) and a **chamfered block converted to sheet metal** (`sheet.convert`). They are the reference models for recipes 6 and 7 of the [`solidcraft-sheet-metal`](../../skills/solidcraft-sheet-metal/SKILL.md) skill. How the dimensions were read and where the rebuilds differ from the videos is in [the reference note](../../skills/solidcraft-sheet-metal/references/elite-engineers-phone-stand-and-convert.md).

These are the repository author's own rebuilds, with dimensions read from video frames (about +-2-3 %). The repository has no affiliation with the channel. Watch the original videos for the full demonstration.

## Files

| Model | 3D model (any viewer) | Editable SolidCraft design | Flat pattern | Bend table |
|---|---|---|---|---|
| Phone stand | [`phone-stand.3mf`](phone-stand/phone-stand.3mf) | [`phone-stand.json`](phone-stand/phone-stand.json) | [`phone-stand-flat.dxf`](phone-stand/phone-stand-flat.dxf) | [`phone-stand-bends.csv`](phone-stand/phone-stand-bends.csv) |
| Converted block | [`converted-block.3mf`](converted-block/converted-block.3mf) | [`converted-block.json`](converted-block/converted-block.json) | [`converted-block-flat.dxf`](converted-block/converted-block-flat.dxf) | none |

## What each one shows

**Phone stand** (6 features: `Perfil`, `ContourFlange1`, `Unfold1`, `CortePlano`, `Extrude1`, `Refold1`).
- Steel, t 2.5, K 0.44, R = Thickness. One 5-segment profile gives 4 bends (100 and 140 degrees one way, 90 and 75 degrees the other), contour flange width 80.
- Flat length 282.2 mm (the video shows 286). The bend table has 7 rows because the two slots split bends 2, 3 and 4. Bend centres: x 87.2, 175.0, 241.0 and 266.8.
- The tapers, the 55 x 20 slot, the U notch and the rounded corners are ONE sketch with 4 closed profiles, cut in the unfolded state (`CortePlano`, `Extrude1`) and then refolded. Cutting through bends is only possible this way.
- The bend table labels the first two bends `up` and the last two `down`. The video's table says the opposite. Both split the bends 2 and 2, and which side the tool measures from was not checked.

**Converted block** (5 features: `Perfil`, `Extrude1`, `Furo`, `Extrude2`, `ConvertToSheetMetal1`).
- A pentagon profile extruded 120 mm, a dia 50 hole cut through both pentagon faces, then `sheet.convert` from the bottom face with all 4 bottom edges as bend edges: bottom plus 4 walls, 4 bends, t 5.
- Selecting fewer than all the bottom edges is refused (`not supported yet: converting bodies that are not a plate of even thickness without bend edges`).
- The solid uses the rebuild's own dimensions, not the video's (see the differences table in the reference note).

## Names in the files

Feature and body names are in Portuguese.

| Name | Meaning |
|---|---|
| `Perfil` | Profile (sketch) |
| `CortePlano` | Cut in the flat state |
| `Furo` | Hole |
| `Suporte` | Stand (body name in the phone-stand 3MF and bend table) |
