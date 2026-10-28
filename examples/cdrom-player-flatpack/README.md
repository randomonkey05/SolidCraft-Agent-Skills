# Example: CD-ROM player flat-pack enclosure, two versions

Two models of the same laser-cut flat-pack enclosure (the das_POD CD-ROM Player 01), built in SolidCraft. They show the range of the [`solidcraft-sheet-metal-flatpack`](../../skills/solidcraft-sheet-metal-flatpack/SKILL.md) skill: **large folded panels** and **round ear tabs placed where the screws go**.

These are the repository author's own approximate reconstructions, made for teaching. Dimensions were read from video frames and carry about +-8-10 % (see [the analysis](../../skills/solidcraft-sheet-metal-flatpack/references/cdrom-player-das-pod-analysis.md)). The internals (drive, boards, jacks, fasteners) are placeholders. They are **not manufacturing files**, there are no cut-ready flat patterns here, and the repository has no affiliation with the maker.

## Files

| Version | 3D model (any viewer or slicer) | Editable SolidCraft design |
|---|---|---|
| v1 | [`v1/cdrom-player-flatpack-v1.3mf`](v1/cdrom-player-flatpack-v1.3mf) | [`v1/cdrom-player-flatpack-v1.json`](v1/cdrom-player-flatpack-v1.json) |
| v2 | [`v2/cdrom-player-flatpack-v2.3mf`](v2/cdrom-player-flatpack-v2.3mf) | [`v2/cdrom-player-flatpack-v2.json`](v2/cdrom-player-flatpack-v2.json) |

## What each version shows (read from the design files)

**v1, first attempt: tall walls folded straight from the base.**
- Two sheets, `Corpo` (body) and `Tampa` (lid).
- The body is a base flange plus a 93.5 mm edge flange on two edges and a 95.5 mm edge flange on the rear edge, all 90 degrees.
- The lid is a base flange plus a 46 mm flange and a 16 mm flange.
- Good example of **large bends from a single base**. It is also the version that was wrong: the walls were assumed instead of read from the real product, which has side plates as separate parts.

**v2, rebuilt from the real architecture: large panels plus localized ear tabs.**
- Two folded sheets, `Base` and `Lid`, plus two separate side plates.
- `Base`: a 123.5 mm edge flange (the rear panel) and four 34 mm flanges, which are the ear tabs. `Lid`: a 78 mm edge flange (the front panel) and five 34 mm flanges.
- The tabs are unfolded, cut with a round tip, bend slits and an M3 hole, then refolded. They sit exactly where the screws go. This is the **ear-tab-at-screw-location** pattern from the skill.
- Placeholders for the drive, two boards, jacks, a switch, feet, standoffs and 18 M3 screws are components with instances.

## Part names in v1 are in Portuguese

| v1 name | Meaning |
|---|---|
| `Corpo` | Body (base sheet: rear, bottom, walls) |
| `Tampa` | Lid |
| `Paredes`, `Traseira` | Walls, rear (feature names) |
| `Parafuso_M3x12`, `_M3x6`, `_M3x5` | M3 screws, by length |
| `Porca_M3`, `PEM_M3`, `Arruela_M3`, `Standoff_M3` | M3 nut, self-clinching nut, washer, standoff |
| `Porca_Jack` | Jack nut |
| `Botao` | Button |
| `Pe_Borracha` | Rubber foot |
| `Jack_Audio`, `Jack_DC` | Audio jack, DC jack |
| `Drive_CD` | CD drive (placeholder) |
| `PCB_Controlo`, `PCBs_Traseira` | Control board, rear boards |

v2 uses English names.
