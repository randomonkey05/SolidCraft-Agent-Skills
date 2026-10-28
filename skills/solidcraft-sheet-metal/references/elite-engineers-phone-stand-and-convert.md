# Two silent sheet-metal tutorials, read from frames and rebuilt in SolidCraft

Two public SolidCraft sheet-metal tutorial videos by the YouTube channel Elite Engineers ("Sheet Metal Kickoff", a phone stand, and "Convert to Sheet Metal First Test"). Both are silent, so every dimension below was read from video frames (about +-2-3 %). The first video was recorded on SolidCraft 0.25.1. The numbers here are this repository's own reading and rebuild, not the author's drawings, and the repository has no affiliation with the channel. Watch the videos for the full demonstration.

How the dimensions were obtained, and the checks that worked, are in section 1 of [`../SKILL.md`](../SKILL.md). The two validated rebuilds are recipes 6 and 7 there. This note adds what was read from the video and where the rebuild differs.

## Video 1: phone stand

**Rule read from the video.** Material Steel, thickness 2.5 mm, K 0.44, bend radius = Thickness (the flat-pattern table shows R4, not confirmed), relief width and depth = Thickness, corner relief notch, hem gap 0.01.

**Open profile.** The lines are the outer mould lines, fully dimensioned, on the YZ or XZ plane:
- base 90 horizontal;
- a 100 leg at 80 degrees from the base (leaning toward the origin);
- a 75 leg at 40 degrees from the previous one (back down and left);
- a 25 flange at 90 degrees from the 75 leg;
- a 15 end flange at 105 degrees (interior) from the 25.

**Bend directions** (from the flat-pattern table): Down 100, Down 140, Up 90, Up 75. The first two bend the same way and the last two the opposite way.

**Computed points** (x, z): P0 (0, 0), P1 (90, 0), P2 (72.635, 98.481), P3 (35.135, 33.529), P4 (13.484, 46.029), P5 (17.366, 60.518).

**Strip.** Contour flange with width (distance) 80 mm, then Unfold.

**Flat size.** The video shows 286 mm long (and about 74 wide). The rebuild with K 0.44 and R = t gives 282.2 x 80. A hand calculation with the standard setback formula gives about 273.4. The video and the tool therefore differ by a few millimetres, and the hand formula is off by about 9. The cause was not found: measure with unfold, do not predict.

**Cuts made in the flat state.**
- Narrow the strip: 80 wide at the base end, about 50 at the first bend (about 85 from the start), then about 60 to the end. Two wedges or triangles are cut by extrude (the video uses distance 36 mm with Reverse direction).
- Two slots, 55 x 20 and 60 x 20, cut through the bend zones, which is why the part is cut unfolded. One slot opens to the edge and forms a U that splits the end tab into two, which gives 7 bends in the flat pattern.
- 3 circles at the base corners are cut to round them.
- Refold. Result: a base with rounded corners, an inclined back with a slot or U notch, and 2 support tabs.

**Flat pattern.** The Create Flat Pattern dialog lists the bends (angle, radius) and the flat size. Export DXF and Export Bend Table are on the Sheet Metal tab.

**Rebuild (recipe 6).** The tapers, slots and rounded corners go into ONE flat-state sketch with 4 closed profiles and one extrude cut. The flat pattern then has 7 bends as in the video. The bend centres to place features at are x 87.2, 175.0, 241.0 and 266.8, read from `bend_zones` and `bends` of `sheet.flat_pattern`.

## Video 2: convert to sheet metal

**Solid.** A centred rectangle extruded symmetric 56 mm (New Body), a 1 mm test chamfer and then a large chamfer on one corner (a prism with a cut top), and a dia 50 hole cut in the side (extrude Cut -180).

**Rules.** Steel, thickness 2.5 first and then 5 mm, K 0.44, R = Thickness.

**Convert to Sheet Metal.** Fixed Face (one face of the body) plus Bend Edges (4 edges) plus Rule.
- With 1 edge only: error `not supported yet: converting bodies that are not a plate of even thickness without bend edges`.
- With 2 edges the dialog still asks for more.
- With all 4 edges it works.

**Result.** A 5 mm sheet with a base, 2 side walls carrying the dia 50 hole and the chamfered flange, with rounded bends.

**Rebuild (recipe 7).** The pentagon profile (-60,0) (60,0) (60,120) (-10,120) (-60,70) is extruded 120 mm. The dia 50 hole is cut through both pentagon faces, and converting from the bottom face with its 4 edges gives bottom plus 4 walls with 4 bends. Both pentagon walls keep the hole, and the DXF export works. One trap: the new-body extrude went to -y even with `flip`, so read the bbox with `measure` before placing the next sketch.

## Differences to remember

| Item | In the video | In the SolidCraft rebuild |
|---|---|---|
| Phone stand flat length | 286 mm | 282.2 mm (hand formula 273.4) |
| Phone stand flat width | about 74 | 80 (strip distance), narrower after the taper cuts |
| Bend radius | table shows R4 | rule R = Thickness (2.5), not reconciled |
| Convert test solid | rectangle 120 x (not read) extruded 56 symmetric, chamfered, dia 50 hole cut -180 | pentagon profile extruded 120, dia 50 hole cut 140: the rebuild uses its own dimensions to reproduce the shape and the convert workflow |
| Convert, bend edges | 4 edges accepted, 1 or 2 refused | same: select all 4 bottom edges |
