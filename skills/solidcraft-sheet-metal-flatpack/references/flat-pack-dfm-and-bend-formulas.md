# Sheet metal reference: flat-pack design rules and bend formulas

A working summary, in the repository's own words, of two sources:

1. A "design for manufacture and assembly (DfM/DfA) guidelines for flat-pack sheet metal" note supplied by the repository author (Section A).
2. The Hackaday article [The Art And Science Of Bending Sheet Metal](https://hackaday.com/2016/05/18/the-art-and-science-of-bending-sheet-metal/) (Sections B, C and D). Read the article for the full explanation and the figures. The formulas and the K-factor table below are standard sheet-metal engineering data.

Symbols: a = bend angle in degrees, r = inside radius, T = thickness, k = K-factor.

## A. Flat pack and perforated bends

- Goal: cut in 2D (laser), ship flat, fold by hand with pliers or a simple jig.
- Elements: slots along the bend line, bridges (webs, micro-joints) between slots that act as the hinge axis, and relief radii at the slot corners.
- Material: malleable sheet (aluminium 1050 or 5052, mild steel), thickness typically 0.8-2.0 mm.
- Slot width w >= T (ideal 1.2 T to 1.5 T) so the walls do not collide when rotating.
- Bridge width b about 1.0 T to 1.5 T (for T <= 1.5 mm). Too narrow and it collapses in transport. Too wide and the hand force and the deformation get excessive.
- Slot corners get a radius R >= 0.2-0.5 mm. Never sharp 90 degree corners: fatigue and cracking.
- Locking tabs and slots (male and female) that lock when the final angle is reached (90 or 180 degrees). Do not depend on the perforation alone.
- Bend marks: laser engraving at 10-20 % of T, or a vector line only, with the direction (up or down) and the angle.
- Grain: bend lines and slots perpendicular to the rolling direction.
- Further reading named in the source note: Howell, Compliant Mechanisms; kerf bending; micro-joint guides from laser-cutter makers; origami and Miura-ori in sheet metal.

## B. Press-brake bending (Hackaday)

- Air bending: the punch sets the radius and the stroke depth sets the angle. The V-die opening is about 6-12 T. There is springback (overbend). Angular accuracy is low, but no tool changes are needed.
- Bottoming: the sheet seats in the die and the die angle sets the bend angle. More force, more accurate, less springback. The opening is about 8 T. One die per angle.
- Slotting (bench or vise, up to about 1/4" steel): weaken the bend line. Do not use it on parts that carry structural load at the bend. Material density about 20 % (bridge w = 1/4 of the slot length s, bridge >= 3/4 T). Straight slots: slot width d = the bend allowance, small bend radius (< 2/3 T). "Engineered" patterns (smiley, self-indexing, patented industrial-origami patterns) bend at about zero radius and do not need a K-factor (the outside setback still applies).

## C. Formulas

- Bend allowance: BA = a x pi/180 x (r + k T)
- Outside setback, a < 90 degrees (sides A and B measured from the vertex to the edge): OSSB = (r + T) x tan(a/2). For a >= 90 degrees with A and B measured from the bend tangent: OSSB = r + T (independent of the angle).
- Legs: a' = A - OSSB and b' = B - OSSB. Flat length L = a' + b' + BA.
- Bend deduction: BD = 2 OSSB - BA = 2 (r + T) tan(a/2) - a x pi/180 x (r + k T). Then L = A + B - BD.
- Worked check (T = 3, r = 3, k = 0.44): 75 degrees gives BA 5.655 and 45 degrees gives BA 3.393. SolidCraft gives the same values.

## D. Generic K-factors

| Radius | Soft aluminium | Medium aluminium | Hard steel |
|---|---|---|---|
| Air bending 0-T | 0.33 | 0.38 | 0.40 |
| Air bending T-3T | 0.40 | 0.43 | 0.45 |
| Air bending > 3T | 0.50 | 0.50 | 0.50 |
| Bottoming 0-T | 0.42 | 0.44 | 0.46 |
| Bottoming T-3T | 0.46 | 0.47 | 0.48 |
| Bottoming > 3T | 0.50 | 0.50 | 0.50 |

## E. Notes for SolidCraft

- Related skill: `solidcraft-sheet-metal` (flanges, unfold/cut/refold, flat pattern, DXF).
- Flat pack: build the slots and bridges on the bend line as cuts in the UNFOLDED state (sketch on XY at z=0, extrude cut = T). The width of the perforated zone should equal the intended BA (straight slots). Relief radii at the slot corners are arcs in the sketch.
- The flat-pack guideline assumes T of 0.8-2 mm. A 3 mm plate is outside that range: use the K-factor and bridges proportional to T, and check the bending force.
