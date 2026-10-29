# CNC machining review (milling and turning)

## Sources (start here when the user supplies no shop spec)
- Hubs, How to design parts for CNC machining: https://www.hubs.com/knowledge-base/how-design-parts-cnc-machining/ (cavities and pockets, internal edges, thin walls, holes, threads, small features, tolerances, setups, undercuts).
- Protolabs CNC milling design guidelines: https://www.protolabs.com/services/cnc-machining/cnc-milling/design-guidelines/ (size limits, materials, finishes, thread conventions, radii).
Neither describes an arbitrary lathe, five-axis machine or custom fixture. For turning or special tooling, ask for the shop's own specification.

## Inputs to collect
Material, stock form, milling or turning, available axes, critical fits and tolerances, the shop's tooling limits. If the process is unspecified, discuss candidate setups without claiming a verified machining plan.

## Checks (milling)
- Identify pockets, internal corner radii, holes, thin walls and the direction each feature is approached from. A cutter fitting a pocket does not prove the tool holder can reach it.
- Compare actual internal radii with the proposed cutter radius. Report pocket depth, hole depth over diameter and wall height over thickness separately, using the shop's material-specific reach limits. Do not apply one universal ratio.
- In-plane pocket corners differ from floor-to-wall roots: a flat end mill makes a sharp floor-to-wall junction. A root fillet is optional and may need a corner-radius or ball tool and an extra pass. For sharp in-plane internal corners, suggest a larger radius or a relief if the function allows.
- A feature infeasible with one end mill is not infeasible for all processes: propose another setup, another tool or EDM as an alternative, not as a finding.
- Threads: engagement, drill-tip clearance, runout. Distinguish a modelled thread from a drawing callout and follow the shop's preferred representation.

## Checks (turning)
Identify the rotation axis, diameters, bores, shoulders, grooves, parting and workholding regions. Off-axis features need live tooling or another setup. Rotational symmetry alone does not prove tool access.

## Always
- Stock allowance, fixture contact, setup changes, inaccessible cavities, collisions. Setup counts are estimates until tool and fixture envelopes have been checked. No exact cycle time or quote without that evidence.
- Separate geometry constraints from cost suggestions. Preserve functional interfaces; relax tolerances only where function allows.

## Measuring in SolidCraft
`measure` with `items` gives a hole or cylinder's `diameter`/`radius`, an arc's `radius`, and the `min`/`max` and `center_distance` between two selections (wall thickness: two parallel faces; hole depth: hole face to the face it starts from). Face and edge counts come from `body_topology`.

## Worked example (illustrative numbers, not default limits)
A measured 2 mm internal corner radius cannot be produced by a 6 mm diameter end mill: its 3 mm radius is too large. A smaller cutter may fit, but reach, holder clearance, material and pocket depth remain separate checks.
