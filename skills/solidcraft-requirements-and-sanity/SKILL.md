---
name: solidcraft-requirements-and-sanity
description: Use when a SolidCraft part or assembly must be designed from a vague brief, a sketch or a few dimensions with no drawing to copy: asks the missing blocking questions in one round before building, then checks walls, hole edge distances, clearances, fasteners, material and process before the design is called finished.
---

# Clarify first, then build, then check plausibility

A part can build cleanly and still be wrong because units, interfaces or loads were guessed. Building on too little information costs a rebuild; one round of good questions costs seconds. Get the facts first, check plausibility at the end, and label every claim.

(Idea source: the process gates of capwitf/mechanical-cad-skills, MIT. Rewritten for SolidCraft; no text copied.)

## 1. Clarify before the first build call

### 1.1 Fill the lock from what is already known
Read the message, attached files and any drawing first. Fill what you can; never ask for something you can read or measure.

| Field | Blocking when missing? |
|---|---|
| What it is and what it must do | always |
| Governing dimension(s): overall envelope, or the one size everything else follows | always |
| Process and material: printed, machined, sheet metal, laser cut, purchased stock | when it changes the geometry (wall, bend radius, tolerances) |
| Interfaces to real parts: mounting holes, shafts, bearings, fasteners, mating part sizes | when the part must fit something that exists |
| Loads | only when the part is structural; otherwise record `unknown` |
| Deliverables: .solidcraft, .step, .3mf/.stl, .dxf, screenshot | when it changes how the model is built or exported |
| Units | assume mm unless stated |
| Acceptance: the `measure` values or checks that prove it is done | derive it yourself from the answers |

Classify every unknown:
- **Blocking**: no correct result without it.
- **Assumable**: a conservative default exists; write it down as an assumption.
- **Decorative**: appearance only; choose and move on.

### 1.2 Is the request too vague to build?
It is when at least one blocking field cannot be taken from the message or files. Examples: "make me a bracket", "a box for my electronics" with no board size, "a gear" with no ratio or module. It is not vague when the unknowns are all assumable.

Skip the questions and build straight away, with the assumptions stated at the top of the reply, when the part is simple and cheap to redo (a plate, a spacer, a single bracket with the governing size given).

### 1.3 Ask once, ask well
- Ask **in one round**: 1 to 4 questions together, never one at a time and never a second round.
- Use the interface's multiple-choice question tool when it exists (the user can always type their own answer); otherwise a short numbered list.
- Put the recommended or most conservative option first and mark it, so an answer can be "ok".
- Make each question concrete: a unit, a range, or a few labelled options. Not "what size?" but "Outer size? (A) 100 x 60 x 40 mm (recommended, fits a Raspberry Pi 4 board) (B) 80 x 50 x 30 mm (C) other".
- Ask in the language the user writes in.
- Ask only blocking questions. Everything assumable goes into the assumptions list instead.

### 1.4 Hard gate
Until the blocking answers arrive, do not call `new_design` or any feature command. Read-only preparation is fine: `inspect_design`, reading attachments, computing the plan and expected volume.

After the answers, anything still unknown becomes a written assumption and the related claims stay Inferred or Unverified. If the user says to assume, or nobody is present to answer, take the most reasonable reading, put the assumptions at the top of the reply, and carry on. The exception is a decision that cannot be undone and could reasonably go either way: do the preparation, set out the decision, and stop there.

Write the final lock (locked facts, assumptions, acceptance values) in the reply and in the model notes before building.

## 2. Pre-build number check
With the lock written and before the first feature call, check the planned numbers on paper. Stop and fix the plan, or ask, when:
- a dimension is not a finite positive number;
- a hole, slot or pocket envelope (not just its centre) crosses the part edge or another feature, for example a locating hole that runs into a centre slot;
- a wall, web between holes, hole edge distance or remaining pocket or counterbore floor is below the starting values for the process (see `solidcraft-hole-fastener-rules`);
- a counterbore is not wider than its through hole, or a tapped hole is not smaller than its thread;
- a fillet or chamfer is larger than the narrowest wall or step next to it;
- a rectangular pocket has sharp inside corners (prefer slot-ended pockets or corner radii).

Record the smallest margin found in each category: these numbers go into the sanity table below. If the process is unknown, a category stays `unknown`; do not invent a limit.

## 3. Sanity table
Before calling a no-reference design finished, fill the rows that apply. Each row gets a number with a unit, or the word `unknown`.

| Check | Evidence |
|---|---|
| Function and load path | where force enters, where it leaves |
| Interfaces | dimensioned, not only drawn |
| Material and process | and the limits that follow (see `solidcraft-3d-print-dfm`, `solidcraft-sheet-metal`, `solidcraft-sheet-metal-flatpack`) |
| Minimum wall or section | measured value vs the process minimum |
| Hole edge and hole-to-hole distance | smallest value in the part, vs the starting values in `solidcraft-hole-fastener-rules` |
| Clearances and fits | shaft, bearing, fastener, tool and assembly access |
| Standard parts | fastener sizes, clearance holes, counterbores, stock thicknesses |
| Interference | checked (assembly or motion) or explicitly unverified |
| Failure modes | bending, shear, pull-out, buckling, wear, loosening |

Do not invent process numbers: take them from the process skills above, from `solidcraft-hole-fastener-rules` or from the user's data. Ribs, fillets and holes added for looks are not a load path.

## 4. Claim labels
- **Verified**: measured or inspected in the final design (`measure`, `body_topology`, `set_parameter` test, section or top-view screenshot).
- **Inferred**: plausible from geometry or common practice, not measured.
- **Unverified**: missing load, material grade, tolerance, or the real mating part.

Not allowed without evidence: "strong enough", "fits the real X", "no interference", "manufacturable", "production ready".

## 5. Gate result
- **Pass**: every applicable row has a number or an honest `unknown`, and no claim is stronger than its evidence.
- **Partial**: some rows unknown; say which and what would close them.
- **Fail**: no interfaces, no load path on a structural part, or an unquantified minimum wall.

A good-looking model does not compensate for a failed row. Report the gate result next to the screenshot.
