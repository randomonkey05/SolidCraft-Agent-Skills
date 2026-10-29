#!/usr/bin/env python3
"""Look up SendCutSend catalog and engineering specs (standard library only).

  scs_specs.py find <words...> [--thickness-mm 1.6] [--limit 15]
  scs_specs.py sku <SKU>

Fetches the official public JSON each run (override with --dir to read local copies).
Source values are in INCHES; every number is also shown in mm. Fact-only: no verdicts.
Treat the feeds as evidence, not a stable API: fields may be missing or "N/A".
"""
import argparse, datetime, json, os, re, sys, urllib.request

BASE = "https://cdn.sendcutsend.com/specs/"
IN = 25.4
NOT_LENGTH = ("gauge", "k_factor", "angle", "largest_tap", "smallest_tap")  # keys whose values are not inch lengths


def load(name, d):
    if d:
        with open(os.path.join(d, name), encoding="utf-8") as fh:
            return json.load(fh)
    req = urllib.request.Request(BASE + name, headers={"User-Agent": "solidcraft-dfm-review"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def mm(v):
    """number-like string/float in inches -> mm string, else None"""
    try:
        return round(float(v) * IN, 3)
    except (TypeError, ValueError):
        pass
    if isinstance(v, str):
        m = re.fullmatch(r"\s*([\d.]+)\s*[xX]\s*([\d.]+)\s*", v)
        if m:
            return [round(float(m.group(1)) * IN, 2), round(float(m.group(2)) * IN, 2)]
    return None


def show(title, block):
    print(f"\n[{title}]")
    for k, v in (block or {}).items():
        conv = None if isinstance(v, bool) or any(x in k for x in NOT_LENGTH) else mm(v)
        if conv is not None:
            print(f"  {k}: {v} in  = {conv} mm")
        else:
            print(f"  {k}: {v}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["find", "sku"])
    ap.add_argument("words", nargs="+")
    ap.add_argument("--dir")
    ap.add_argument("--thickness-mm", type=float)
    ap.add_argument("--limit", type=int, default=15)
    a = ap.parse_args()

    cat = load("sendcutsend-catalog.json", a.dir)
    spec = load("sendcutsend-specs.json", a.dir)
    meta = spec.get("_meta", {})
    print(f"# sources: {BASE}sendcutsend-catalog.json, {BASE}sendcutsend-specs.json")
    print(f"# accessed {datetime.date.today()}; specs generated_at {meta.get('generated_at')}; schema {meta.get('schema_version')}")

    if a.cmd == "find":
        toks = [w.lower() for w in a.words]
        n = 0
        for m in cat["materials"]:
            hay = " ".join(str(m.get(k, "")) for k in ("sku", "name", "category", "grade", "group")).lower()
            if not all(t in hay for t in toks):
                continue
            t_mm = mm(m.get("thickness"))
            if a.thickness_mm is not None and (t_mm is None or abs(t_mm - a.thickness_mm) > 0.15):
                continue
            n += 1
            if n <= a.limit:
                print(f"{m['sku']:<26} {m.get('name','')[:34]:<34} t={m.get('thickness')} in ({t_mm} mm)  {m.get('cutting_process')}  "
                      f"{'OUT OF STOCK ' if m.get('out_of_stock') else ''}services={','.join(m.get('available_services', []))}")
        print(f"# {n} match(es)" + (f", first {a.limit} shown" if n > a.limit else ""))
        return

    sku = a.words[0]
    c = next((m for m in cat["materials"] if m["sku"] == sku), None)
    s = next((m for m in spec["materials"] if m["sku"] == sku), None)
    if not c and not s:
        sys.exit(f"SKU {sku!r} not found (exact SKU is the only authoritative join). Use `find` first.")
    if c:
        print("\n[catalog]", json.dumps({k: c.get(k) for k in ("name", "thickness", "out_of_stock", "cutting_process", "min_part_size", "max_part_size", "available_services")}))
    if not s:
        print("\n(no engineering specs for this SKU: every dependent check is 'need more info')")
        return
    show("general_specs", {k: v for k, v in s.get("general_specs", {}).items() if k not in ("photo_url",)})
    for blk in ("cutting_specs", "bending_specs", "tapping_specs", "countersinking_specs"):
        if s.get(blk):
            show(blk, s[blk])
    print("\nOther blocks present:", [k for k in s if k not in ("sku", "general_specs", "cutting_specs", "bending_specs", "tapping_specs", "countersinking_specs") and s[k]])


if __name__ == "__main__":
    main()
