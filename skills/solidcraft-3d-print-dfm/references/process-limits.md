# Published DfAM limits per process (for cross-checking)

Conservative default design-rule limits for additive processes, as tabulated in the `dfam-check` skill of earthtojake/text-to-cad (MIT, see NOTICE), which cites the Hubs FDM/SLS/SLA/metal guides, Formlabs design guides, HP MJF design guidelines and EOS design rules, and says they are consistent with ISO/ASTM 52910 (general DfAM guidance) and ISO/ASTM 52911-1 (laser powder bed fusion of metals). A machine, material or parameter datasheet overrides any value here. Cite whichever source you use. I have not re-checked the underlying guides.

| Limit | FDM/FFF | SLS (PA12) | SLA/DLP | PBF-LB metal | MJF |
|---|---|---|---|---|---|
| Min supported wall (mm) | 1.2 | 0.7 | 0.5 | 0.4 | 0.5 |
| Min unsupported wall (mm) | 1.6 | 0.7 | 1.0 | 0.5 | 0.5 |
| Self-supporting angle (deg from horizontal) | 45 | n/a (powder) | 30 | 45 | n/a (powder) |
| Min hole diameter (mm) | 2.0 | 1.5 | 0.5 | 1.5 | 1.0 |
| Min positive feature (mm) | 0.8 | 0.8 | 0.2 | 0.4 | 0.5 |
| Max unsupported bridge (mm) | 10 | n/a | 5 | 2 | n/a |

## How to read a measurement against these limits
- Wall thickness from ray-cast sampling gives a sampled minimum. Treat the 5th percentile below the limit as a strong violation signal even when the minimum alone could be an outlier. On an assembly, attribute a thin wall to the body it belongs to; a mating clearance must not be read as a wall.
- Overhang analysis must exclude faces resting on the build plate. Powder processes (SLS, MJF) do not need support-angle checks; their relevant check is powder escape from trapped cavities.
- Support volume is a coarse upper bound: a ratio above about 30% of the part volume usually justifies a new orientation or a redesign for support-requiring processes.
- Check watertightness first. An open mesh blocks slicing for every process.
- Orientation candidates: try the six axis-aligned rotations and report any that cuts support area materially, with its build-height cost.
- Suspect units: if the bounding-box diagonal is tiny or huge the file is probably in metres or inches, and every overhang figure of zero means nothing. Ask before comparing.
- A limit with no measurement behind it is not a finding. Report it as not checked.
