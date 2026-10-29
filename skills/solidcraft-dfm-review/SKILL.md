---
name: solidcraft-dfm-review
description: Use when asked whether a SolidCraft part can be bent, laser-cut, machined or turned, for a design-for-manufacturing review or redesign of sheet-metal or CNC parts, or before ordering a flat pattern (DXF) from SendCutSend: evidence first, one result per feature, no blanket approval.
---

# Design-for-manufacturing review (sheet metal and CNC)

Adapted from the `dfm` skill of earthtojake/text-to-cad (MIT, see NOTICE), rewritten for SolidCraft's measuring tools. Injection moulding is not covered here. For FDM printing use `solidcraft-3d-print-dfm`. For building the sheet-metal part itself use `solidcraft-sheet-metal`; this skill is the review that follows it.

This is a guided review, not an automatic feature-recognition engine and not a manufacturing certificate. Report the checks you could not make.

## 1. Pick the process, then read its reference
| Process | Reference |
|---|---|
| Sheet metal (laser, bend, flat pack) | [references/sheet-metal.md](references/sheet-metal.md) |
| Sheet metal made by SendCutSend (their per-SKU limits and DXF measurement) | [references/sendcutsend.md](references/sendcutsend.md), after sheet-metal.md |
| CNC milling and turning | [references/cnc.md](references/cnc.md) |

When comparing processes, review each one separately.

## 2. Evidence first
- Identify the file and revision, units and bodies. Quote the design name or file, not "the model".
- Take geometry from SolidCraft, not from a screenshot: `measure` (bodies, or two selections for min distance and centre distance, a hole's diameter and radius, a cylinder's radius), `body_topology` for faces and edges, `inspect_design` for parameters and the timeline. A render supports a suspected issue, never a pass or fail.
- Sheet metal: `sheet.rules` / `sheet.manage_rules` (thickness, K factor, bend radius, relief), `sheet.flat_pattern` (bends, bend zones, flat size), `sheet.export_bend_table`, `sheet.export_dxf`.
- For a DXF you intend to upload, measure the file itself, not the model: `python scripts/dxf_facts.py part.dxf` (facts only, standard library, ASCII DXF).
- Never infer material, alloy, temper or stock thickness from a body's colour or appearance. Ask, or state the assumption.
- Source code or parameters describe intent. Check they match the body you are reviewing before using them as evidence.

## 3. Choose the rules
1. The selected shop's specification for the actual material and process wins. For SendCutSend it is published as data: follow references/sendcutsend.md.
2. If none is supplied, use the two sources named in the process reference as a starting point. Neither describes an arbitrary machine, tool or fixture.
3. Record, for every limit you adopt: document or URL, access date, section or field, units, and the material and tooling conditions it applies to. If a source cannot be checked, report the missing rule, do not invent a default.
4. Do not turn a supplier's recommendation into a physical law. Keep cost advice separate from manufacturing constraints.
5. Always state the distance convention before comparing two distances (bend tangent, bend centreline, hole edge, hole centre, outer or inner radius). They are not interchangeable.

## 4. Report
Return a concise report:
- **Scope**: file and revision, parts, process, material and thickness, units, tooling assumptions.
- **Findings** table, one row per feature:

| Part / feature | Evidence | Rule (source) | Result | Suggested action |
|---|---|---|---|---|
| Named feature and where | Measured value, units, method | Source section, threshold, conditions | pass / fail / review / unverified | Specific change or missing evidence |

- `pass`: a measured feature satisfies a cited, applicable limit.
- `fail`: a measured violation.
- `review`: a qualitative risk.
- `unverified`: evidence or process context is missing, or the uncertainty straddles the threshold.
- **Coverage**: checks done and checks not measured, with what is needed to close them. "No findings" is never a blanket approval.

If only a render is available, list visible concerns as `review` and ask for the dimensions.

## 5. Redesign
Keep the original design; save the change under a new name (`name_v2`). Edit with `solidcraft-editing`, rebuild, re-measure, and check neighbouring features as well as the original finding. A review request alone is not a request to edit, order or upload.
