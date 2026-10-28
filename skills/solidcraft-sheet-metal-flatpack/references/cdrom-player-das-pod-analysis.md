# das_POD CD-ROM Player 01: flat-pack architecture read from the assembly video

This is an independent analysis, not an official drawing. The maker publishes no dimensions. Public coverage ([Designboom](https://www.designboom.com/technology/used-cd-rom-drives-modular-aluminum-audio-player-das-pod/), [Tom's Hardware](https://www.tomshardware.com/pc-components/enclosures/boutique-diy-hi-fi-solution-lets-you-repurpose-your-old-ide-optical-drives-as-a-standalone-audio-player-usd190-cd-rom-player-01-features-a-laser-cut-enclosure-and-a-custom-pcb)) says only "laser-cut aluminium, powder-coated orange". The repository has no affiliation with the maker and contains none of the maker's files, video or frames.

Source of the numbers: frames of the 4K assembly-instructions video (9 min 55 s), taken from above with the sheets in the maker's hands. **Uncertainty about +-8-10 %.** Scale: the 5.25" drive bezel (about 148 mm wide) in the final front view gives about 2.07 px/mm at 1280 px, so the front width is about 165 mm.

## Architecture (4 sheet-metal parts plus hardware)

1. **BASE sheet:** rear panel plus bottom panel joined by a perforated line. Round tabs on the sides of the rear panel (1 per side) and of the bottom (2 per side, plus 1 at the middle of each side).
2. **LID sheet:** top panel plus front panel (display window, 5 buttons) joined by a perforated line. The top has 4 tabs along one long side plus 1 tab at the end. The front panel has tabs at top and bottom.
3. **Two separate SIDE plates:** rectangular, with holes for the drive and the power board, and a strip with perforated slits that folds into a flange.
4. **Hardware:** M3 Torx screws plus nuts, 2 brackets for the power board, rubber feet, aux jack, DC jack, switch.

Assembly order in the video: 01 fold the sheets, 02 base plus rear, 03 upper part (lid plus front), 04 drive, cables and board, 05 final (side plates, lid, M3 Torx screws).

## Bends and cuts (mm, about 2.76 px/mm in the flat views, +-10 %)

- Panel width about 165 (rear and front). The bottom panel is a little narrower (about 157).
- Rear panel about 165 x 125-130. Front about 165 x 75-80. Box about 165 wide x 125 high x 230-240 deep (to be validated).
- Perforated line between panels: about 12 slots, pitch about 12, slot about 9 x 1.8, bridge about 3.4. About 14 mm of full sheet is left at each end, so the perforation does not run the full width.
- Tabs: about 34 long x 21 wide, fully round tip (R about 10), hole 2.5-3.2 about 20 from the edge.
- Tab bend: 2 slots about 2.2 x 6.3, pitch about 9 (bridge about 2.7), in the body next to the edge.
- Rear panel: aux hole dia about 8 (x about 24, y about 62 from the corner), 12 V DC dia about 8 (x about 113, y about 60), switch dia about 20 (x about 140, y about 60), 2 small holes dia about 2.5 (x about 26, y about 24 and x about 140, y about 22).
- Front panel: display window about 66 x 12 with its centre about 16 from the top. 5 oblong buttons about 11.7 x 6.2 at pitch 20, centred (-40, -20, 0, 20, 40), about 50-53 from the top. 2 small holes at +-57 (LED and IR). 2 screws in the top corners at about +-73.
- Base: two long thin slots (about 30 x 1) parallel to the sides, about 16 from the edge (for the side plates to key into).

## Lessons from the first model, which was wrong

- The first version used 2 parts (a body with full walls plus a lid). The real product uses 2 flat sheets plus 2 separate side plates, so the side plates are not folded from the base.
- Long round tabs bolted with M3 plus a nut, instead of rectangular tabs and slots that snap together.
- The perforation does not run the full width.
- The box height is about 125 (drive 41 plus the space for the front and the board), not 93.5.

## Reference build (second version)

- Base (bbox 155 x 233.5 x 123.5) and lid (155 x 235 x 78) as folded sheets (t 1.5, R 1, K 0.4) with 30 and 33 bends. 2 side plates (the left one made with `solid.mirror`). Placeholders: the drive, a control board (plus 4 spacers), a power board, DC and aux jacks, a switch, 4 feet and 18 M3 screws (components with instances).
- Interferences: 0 (the base and lid pair cannot be verified by the checker).
- Round-tab recipe: flanges over the full length, unfold, cut the gap with an R10.5 round tip plus 2 bend slits (width = BA) plus the hole, refold. Holes off the plane (the rear panel) are cut folded from an XZ plane.
- `occurrence.move` with a matrix in world space COMPOSES with the current transform (new = M applied after the current one). For absolute positions start from a copy without a translate, or compensate. Copies use `translate`. Mirror axisymmetric parts by a 180 degree rotation (det +1) and asymmetric parts with `solid.mirror`.
- Screws: a head inside the side plate collides with the lips and the drive. Put the head outside where there is no wall (between z 34 and 91) and add recesses in the drive at the M3 holes.
