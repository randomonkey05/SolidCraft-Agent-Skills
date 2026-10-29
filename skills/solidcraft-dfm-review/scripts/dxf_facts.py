#!/usr/bin/env python3
"""Fact-only inspector for ASCII DXF flat patterns (standard library only).

It measures; it never says pass or fail. Comparisons belong to the review.
Reads LINE, ARC, CIRCLE, LWPOLYLINE (bulges included); counts but does not
measure SPLINE, ELLIPSE, TEXT, MTEXT, POLYLINE.

Usage: dxf_facts.py part.dxf [--tol 0.001]   (prints JSON, units = file units)
"""
import argparse, json, math, sys
from collections import Counter, defaultdict

MEASURED = {"LINE", "ARC", "CIRCLE", "LWPOLYLINE"}


def read_pairs(path):
    with open(path, "r", errors="replace") as f:
        lines = [l.rstrip("\r\n") for l in f]
    for i in range(0, len(lines) - 1, 2):
        try:
            yield int(lines[i].strip()), lines[i + 1].strip()
        except ValueError:
            continue


def parse(path):
    header, ents = {}, []
    section, cur, hvar = None, None, None
    pending_section_name = False
    for code, val in read_pairs(path):
        if code == 0 and val == "SECTION":
            pending_section_name = True
            continue
        if pending_section_name and code == 2:
            section, pending_section_name = val, False
            continue
        if code == 0 and val == "ENDSEC":
            if cur:
                ents.append(cur)
            cur, section = None, None
            continue
        if section == "HEADER":
            if code == 9:
                hvar = val
            elif hvar:
                header.setdefault(hvar, {})[code] = val
        elif section == "ENTITIES":
            if code == 0:
                if cur:
                    ents.append(cur)
                cur = {"type": val, "layer": "0", "d": defaultdict(list)}
            elif cur is not None:
                if code == 8:
                    cur["layer"] = val
                else:
                    cur["d"][code].append(val)
    return header, ents


def f(ent, code, i=0, default=0.0):
    try:
        return float(ent["d"][code][i])
    except (KeyError, IndexError, ValueError):
        return default


def arc_points(cx, cy, r, a0, a1, step=2.0):
    if a1 <= a0:
        a1 += 360.0
    n = max(2, int((a1 - a0) / step) + 1)
    return [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * k / n)),
             cy + r * math.sin(math.radians(a0 + (a1 - a0) * k / n))) for k in range(n + 1)]


def bulge_points(p, q, b, step=2.0):
    if abs(b) < 1e-12:
        return [p, q]
    d = math.dist(p, q)
    theta = 4 * math.atan(b)
    r = d / (2 * math.sin(abs(theta) / 2))
    mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    h = math.sqrt(max(r * r - (d / 2) ** 2, 0))
    ux, uy = (q[0] - p[0]) / d, (q[1] - p[1]) / d
    sgn = 1 if b > 0 else -1
    big = abs(theta) > math.pi
    s = sgn * (-1 if big else 1)
    cx, cy = mx - s * uy * h, my + s * ux * h
    a0 = math.atan2(p[1] - cy, p[0] - cx)
    n = max(2, int(abs(math.degrees(theta)) / step) + 1)
    return [(cx + r * math.cos(a0 + theta * k / n), cy + r * math.sin(a0 + theta * k / n)) for k in range(n + 1)]


def polyline(ent):
    xs, ys = ent["d"].get(10, []), ent["d"].get(20, [])
    bs = ent["d"].get(42, [])
    pts = [(float(x), float(y)) for x, y in zip(xs, ys)]
    flags = int(float(ent["d"].get(70, ["0"])[0]))
    closed = bool(flags & 1)
    # bulges are listed per vertex only when non-zero in some files; map by order is unreliable
    # so only apply them when one bulge per vertex is present.
    bul = [float(b) for b in bs] if len(bs) == len(pts) else [0.0] * len(pts)
    out = []
    n = len(pts)
    for i in range(n if closed else n - 1):
        seg = bulge_points(pts[i], pts[(i + 1) % n], bul[i])
        out.extend(seg if not out else seg[1:])
    return pts, closed, out


def geometry(ent):
    """returns (polyline points for distance/bounds, endpoints for closure or None)"""
    t = ent["type"]
    if t == "LINE":
        a, b = (f(ent, 10), f(ent, 20)), (f(ent, 11), f(ent, 21))
        return [a, b], [a, b]
    if t == "CIRCLE":
        cx, cy, r = f(ent, 10), f(ent, 20), f(ent, 40)
        return arc_points(cx, cy, r, 0, 360), None
    if t == "ARC":
        cx, cy, r, a0, a1 = f(ent, 10), f(ent, 20), f(ent, 40), f(ent, 50), f(ent, 51)
        pts = arc_points(cx, cy, r, a0, a1)
        return pts, [pts[0], pts[-1]]
    if t == "LWPOLYLINE":
        pts, closed, path = polyline(ent)
        return path, (None if closed else [path[0], path[-1]]) if path else None
    return None, None


def seg_dist(p, a, b):
    ax, ay, bx, by = a[0], a[1], b[0], b[1]
    dx, dy = bx - ax, by - ay
    L = dx * dx + dy * dy
    t = 0 if L == 0 else max(0, min(1, ((p[0] - ax) * dx + (p[1] - ay) * dy) / L))
    return math.hypot(p[0] - (ax + t * dx), p[1] - (ay + t * dy))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dxf")
    ap.add_argument("--tol", type=float, default=0.001, help="endpoint join tolerance in file units")
    a = ap.parse_args()

    header, ents = parse(a.dxf)
    res = {"file": a.dxf, "acadver": header.get("$ACADVER", {}).get(1),
           "insunits": int(header["$INSUNITS"][70]) if "$INSUNITS" in header else None,
           "header_extents": None, "layers": {}, "notes": []}
    if "$EXTMIN" in header and "$EXTMAX" in header:
        res["header_extents"] = {"min": [float(header["$EXTMIN"].get(10, 0)), float(header["$EXTMIN"].get(20, 0))],
                                 "max": [float(header["$EXTMAX"].get(10, 0)), float(header["$EXTMAX"].get(20, 0))]}
    if res["insunits"] is None:
        res["notes"].append("$INSUNITS missing: units unknown")

    allpts, per_layer = [], defaultdict(list)
    types = defaultdict(Counter)
    for e in ents:
        types[e["layer"]][e["type"]] += 1
        pts, ends = geometry(e)
        if pts:
            allpts += pts
            per_layer[e["layer"]].append((e, pts, ends))
    res["layers"] = {k: dict(v) for k, v in sorted(types.items())}
    unmeasured = {t for c in types.values() for t in c if t not in MEASURED}
    if unmeasured:
        res["notes"].append("counted but not measured: " + ", ".join(sorted(unmeasured)))
    if allpts:
        xs, ys = [p[0] for p in allpts], [p[1] for p in allpts]
        res["measured_bounds"] = {"min": [min(xs), min(ys)], "max": [max(xs), max(ys)],
                                  "width": max(xs) - min(xs), "height": max(ys) - min(ys)}

    # holes: full circles
    circles = [(e, f(e, 10), f(e, 20), f(e, 40)) for e in ents if e["type"] == "CIRCLE"]
    if circles:
        ds = sorted(2 * c[3] for c in circles)
        sm = min(circles, key=lambda c: c[3])
        res["circles"] = {"count": len(circles), "min_diameter": ds[0], "max_diameter": ds[-1],
                          "smallest_at": [sm[1], sm[2]], "layer_of_smallest": sm[0]["layer"]}

    # closure: endpoint degree per layer
    closure = {}
    for layer, items in per_layer.items():
        if layer.startswith("BEND_"):
            continue  # bend lines are open by nature
        deg = Counter()
        key = lambda p: (round(p[0] / a.tol), round(p[1] / a.tol))
        closed_poly = open_poly = 0
        for e, pts, ends in items:
            if e["type"] == "LWPOLYLINE":
                if ends is None:
                    closed_poly += 1
                else:
                    open_poly += 1
            if ends:
                for p in ends:
                    deg[key(p)] += 1
        odd = [k for k, v in deg.items() if v % 2]
        closure[layer] = {"closed_polylines": closed_poly, "open_polylines_or_chains": open_poly,
                          "odd_degree_endpoints": len(odd),
                          "sample_odd_endpoints": [[k[0] * a.tol, k[1] * a.tol] for k in odd[:5]]}
    res["closure"] = closure

    # duplicates and zero-length
    seen, dup, zero = Counter(), 0, 0
    for e in ents:
        pts, _ = geometry(e)
        if not pts:
            continue
        sig = (e["layer"], e["type"], tuple(round(c, 3) for p in (pts[0], pts[len(pts) // 2], pts[-1]) for c in p))
        seen[sig] += 1
        if e["type"] == "LINE" and math.dist(pts[0], pts[1]) < a.tol:
            zero += 1
    dup = sum(v - 1 for v in seen.values() if v > 1)
    res["duplicate_entities"] = dup
    res["zero_length_lines"] = zero

    # bend lines
    bends = {}
    for layer in per_layer:
        if layer.startswith("BEND_") and layer != "BEND_NOTES":
            bends[layer] = sorted(round(math.dist(p[1][0], p[1][-1]), 3) for p in per_layer[layer])
    if bends:
        res["bend_line_lengths"] = bends

    # hole centre to nearest outline edge (needs an OUTLINE layer)
    outline = per_layer.get("OUTLINE")
    if outline and circles:
        segs = []
        for _, pts, _ in outline:
            segs += list(zip(pts, pts[1:]))
        worst = None
        for e, cx, cy, r in circles:
            if e["layer"] == "OUTLINE":
                continue
            d = min(seg_dist((cx, cy), s0, s1) for s0, s1 in segs) - r
            if worst is None or d < worst[0]:
                worst = (d, cx, cy, 2 * r)
        if worst:
            res["min_hole_edge_to_outline"] = {"value": round(worst[0], 4), "hole_at": [worst[1], worst[2]],
                                               "hole_diameter": worst[3], "method": "arcs sampled every 2 degrees"}
    elif not circles:
        res["notes"].append("no full-circle holes: hole-to-edge distance not applicable")
    else:
        res["notes"].append("min hole-to-edge not measured: no OUTLINE layer")

    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    sys.exit(main())
