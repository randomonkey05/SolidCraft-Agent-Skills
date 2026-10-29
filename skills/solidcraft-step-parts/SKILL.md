---
name: solidcraft-step-parts
description: Use when a SolidCraft assembly needs real purchasable parts (screws, nuts, washers, bearings, standoffs, motors, boards, profiles) instead of placeholder geometry: find them in the step.parts catalog, download the STEP with a checksum, insert it with file.insert_step and place it.
---

# Real hardware in assemblies (step.parts to SolidCraft)

Adapted from the `step-parts` skill of earthtojake/text-to-cad (MIT, see NOTICE). The workflow and the helper script are rewritten for SolidCraft. Everything marked "verified" was run on SolidCraft 0.25.1 in October 2026.

Search the catalog BEFORE modelling a placeholder cylinder for a screw or a bearing. A real part gives the right envelope, mass and hole size, and the assembly stays honest.

## Workflow
1. **Search.** `python scripts/step_parts.py "M3 socket head 12" --standard "ISO 4762" --limit 5` (standard library only, prints JSON). Facets: `--category`, `--family`, `--standard`, `--tag`. Catalog about 16,800 parts (about 2,100 fasteners, 86 bearings, standoffs, motors, boards, profiles).
2. **Check the attributes, not the name.** Query tokens match as substrings, so "M3" also returns M30 parts. Read `attributes.thread`, `lengthMm`, the standard and the bore before choosing. If several fit, show the best two or three with their ids.
3. **Download into the model's own folder.** `python scripts/step_parts.py --id <id> --download --out-dir <model folder>/parts`. The script verifies the SHA-256 against the catalog and refuses to save on a mismatch. `--download` takes the first result, so use `--id` once you have chosen.
4. **Insert.** `file.insert_step {path, name, matrix?}`. The path must be a path the SolidCraft app can open (a Windows path when the app runs on Windows, not a path inside the agent's shell).
5. **Verify** with `measure` (bounding box against the catalog attributes) and a screenshot.
6. **Place.** Pass `matrix` at insert time, or move the occurrence afterwards (`occurrence.move`, which composes with the current transform; see `solidcraft-assemblies`).

## Verified behaviour (SolidCraft 0.25.1)
- `file.insert_step {path, name}` creates a component named `name` holding the part's solid in the active component. The result lists `component`, `occurrence`, `bodies` and a `system` field with the step.parts page URL. The body keeps the name from the file (for example `Chamfer001`), so refer to parts by component name.
- The file's axes are kept (Z up). `matrix` is a row-major 3x4 `[r11 r12 r13 tx, r21 r22 r23 ty, r31 r32 r33 tz]`; `[1,0,0,30, 0,1,0,0, 0,0,1,0]` placed a bearing with its centre at x = 30 mm.
- ISO 4762 M3x12 socket head cap screw (`iso4762_socket_head_cap_screw_m3x12`): axis along Z, the plane under the head at z = 0, head up to z = +3 (diameter 5.5), shank down to z = -12. 16 faces, no thread geometry (plain cylinder), volume 142 mm3.
- 608ZZ bearing (`bearing_608zz`): axis along Z, centred on the origin, outside diameter 22, width 7 (z from -3.5 to +3.5), volume 2243 mm3.
- Rotate with the matrix to point a screw along another axis, and remember where its reference plane is (under the head, not the centre).
- A Y-up file opens lying down and the app offers "Stand this part up?"; use `up: "y"` in `file.insert_step`, or accept the offer. step.parts files were already Z up.
- An imported part (or assembly) is one rigid group until `component.unlock`.

## Assembly rules (see also `solidcraft-assemblies`)
- Insert each part type ONCE, then add the other placements as instances of that component. Do not insert the same STEP twelve times.
- Screws and nuts are fixtures: keep their placeholders out of the final body count, and do not join them to the plates. Keep gaps real (clearance holes slightly larger than the thread, per the standard).
- Size holes from the part: for a clearance hole take the catalog `attributes` (thread, diameter) and the standard's clearance column, then verify with `measure` between the hole face and the screw body.
- Check interferences after placing hardware.

## Provenance and licensing
- Record the part `id`, its `pageUrl` and the `sha256` in the model notes.
- Each part page states its source; check the terms there before redistributing a model that embeds the part.
- Do not commit downloaded STEP files into a public skills repository. Keep them in the model folder.

## When the service is unreachable
A network or DNS failure is inconclusive. Retry once. Do not tell the user a part does not exist unless the API answered and returned no relevant candidates. If it still fails, use a documented envelope (a cylinder with the datasheet dimensions), label it as a placeholder in the notes, and say so in the report.

## Sources
- Catalog and API: https://api.step.parts (`/v1/parts`, `/v1/parts/{id}`), site https://www.step.parts
- Upstream skill: https://github.com/earthtojake/text-to-cad/tree/main/skills/step-parts
