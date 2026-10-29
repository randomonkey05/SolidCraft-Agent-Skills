"""Build the classic SolidWorks-style A2 drawing sheet template as a DXF (mm).

Geometry is taken from a SolidWorks A2 export (references/playseat-wood.DXF):
outer frame 15..589 x 5..415, inner frame 20..584 x 10..410, zone ticks every
50 mm (columns 12..1 right-to-left, rows A..H bottom-to-top), title block
404..584 x 10..65.2. The educational watermark of the original is NOT copied.

Sizes A4 (portrait) to A1 (landscape). Zones are always 50 mm: ticks sit at
the sheet centre +/- k*50 mm, so a smaller sheet simply has fewer zones.
The title block (180 x 55.2) is anchored to the bottom-right inner corner.

usage: python make_sheet_template.py out.dxf [--size A2] [--title NAME] [--scale 1:10]
"""
import argparse, ezdxf

ap = argparse.ArgumentParser()
ap.add_argument("out")
ap.add_argument("--size", default="A2", choices=["A4","A3","A2","A1"])
ap.add_argument("--title", default="TITLE")
ap.add_argument("--scale", default="1:10")
ap.add_argument("--material", default="")
a = ap.parse_args()

doc = ezdxf.new("R2000", setup=False)
doc.header["$INSUNITS"] = 4
SIZES = {"A4": (210, 297), "A3": (420, 297), "A2": (594, 420), "A1": (841, 594)}
W, H = SIZES[a.size]
doc.header["$LIMMAX"] = (W, H)
for n, d in [("Continuous", "Solid line"), ]:
    pass
doc.linetypes.add("HIDDEN", pattern=[6.0, 3.0, -3.0], description="Hidden __ __")
doc.linetypes.add("CENTER", pattern=[28.0, 20.0, -6.0, 2.0, -6.0], description="Center ____ _ ____")
doc.linetypes.add("PHANTOM", pattern=[22.5, 12.5, -3.75, 3.75, -3.75, 3.75, -3.75],
                  description="Phantom")
for name, col in [("FORMAT", 7), ("VISIBLE", 7), ("HIDDEN", 7), ("CENTER", 7), ("DIM", 7), ("NOTES", 7)]:
    lt = {"HIDDEN": "HIDDEN", "CENTER": "CENTER"}.get(name, "Continuous")
    doc.layers.add(name, color=col, linetype=lt, lineweight=30 if name in ("FORMAT", "VISIBLE") else 18)
doc.styles.add("SLDTEXTSTYLE0", font="txt.shx")
# arrow blocks, same geometry as SolidWorks _Closed / _Dot (unit length, tip at origin)
b = doc.blocks.new("_Closed")
for p, q in [((-1, .17), (0, 0)), ((0, 0), (-1, -.17)), ((-1, .17), (-1, -.17)), ((0, 0), (-1, 0))]:
    b.add_line(p, q)
b = doc.blocks.new("_Dot")
b.add_lwpolyline([(-.25, 0), (.25, 0)], close=True)
b.add_line((-.5, 0), (-1, 0))
# dimension style (SLDDIMSTYLE0 values; dimlfac 10 = drawing at 1:10 showing model dims)
ds = doc.dimstyles.new("SLDDIMSTYLE0")
ds.dxf.dimtxsty = "SLDTEXTSTYLE0"; ds.dxf.dimtxt = 3.5; ds.dxf.dimasz = 3.556
ds.dxf.dimexo = 0; ds.dxf.dimexe = 0; ds.dxf.dimgap = 0.875; ds.dxf.dimdec = 2
ds.dxf.dimtad = 1; ds.dxf.dimtih = 0; ds.dxf.dimtoh = 0
ds.dxf.dimblk1 = "_Closed"; ds.dxf.dimblk2 = "_Closed"
den = float(a.scale.split(":")[1]) / float(a.scale.split(":")[0])
ds.dxf.dimlfac = den
ds2 = doc.dimstyles.new("SLDDIMSTYLE_LEADER")   # balloon leader: closed arrow
ds2.dxf.dimasz = 3.556; ds2.dxf.dimblk1 = "_Closed"
ds3 = doc.dimstyles.new("SLDDIMSTYLE_DOT")      # leader ending on the part: dot
ds3.dxf.dimasz = 0.762; ds3.dxf.dimblk1 = "_Dot"

msp = doc.modelspace()
at = {"layer": "FORMAT"}
def rect(x0, y0, x1, y1):
    msp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], close=True, dxfattribs=at)
rect(15, 5, W - 5, H - 5); rect(20, 10, W - 10, H - 10)
X0, X1, Y0, Y1 = 20, W - 10, 10, H - 10
def ticks(lo, hi):
    c = (lo + hi) / 2; out = []; k = 0
    while c - 50 * k > lo + 1e-6:
        out += [c - 50 * k] + ([c + 50 * k] if k else []); k += 1
    return sorted(out)
tx, ty = ticks(X0, X1), ticks(Y0, Y1)
for y in ty:
    msp.add_line((X0, y), (X0 - 5, y), dxfattribs=at); msp.add_line((X1, y), (X1 + 5, y), dxfattribs=at)
for x in tx:
    msp.add_line((x, Y1), (x, Y1 + 5), dxfattribs=at); msp.add_line((x, Y0), (x, Y0 - 5), dxfattribs=at)
def lab(t, x, y):
    msp.add_mtext(t, dxfattribs={"insert": (x, y), "char_height": 3.97, "layer": "FORMAT"})
yb = [Y0] + ty + [Y1]
for i in range(len(yb) - 1):                      # rows A.. bottom to top
    m = (yb[i] + yb[i + 1]) / 2 + 2
    lab(chr(65 + i), X0 - 2.7, m); lab(chr(65 + i), X1 + 2.3, m)
xb = [X0] + tx + [X1]
n = len(xb) - 1
for i in range(n):                                # columns n..1 right to left
    m = (xb[i] + xb[i + 1]) / 2
    lab(str(n - i), m, Y0 - 0.5); lab(str(n - i), m, Y1 + 4.5)
# title block grid (x0=404..584, y 10..65.2) -- coordinates as in the source sheet
L = [(404,14.2,584,14.2),(404,48.2,584,48.2),(404,65.2,584,65.2),(431,48.2,431,10),
     (404,31.2,502.8,31.2),(404,35.5,502.8,35.5),(404,39.8,502.8,39.8),(404,44,502.8,44),
     (458.6,10,458.6,48.2),(404,65.2,404,10),(411.8,48.2,411.8,10),(437.8,48.2,437.8,65.2),
     (448.4,48.2,448.4,10),(469,31.2,469,48.2),(404,18.5,458.6,18.5),(484.6,65.2,484.6,27),
     (404,22.7,458.6,22.7),(404,27,584,27),(502.8,65.2,502.8,10),(547,10,547,14.2),
     (554.8,58.9,554.8,65.2),(571,14.2,571,27),(502.8,58.9,584,58.9),(571,18.5,584,18.5)]
DX = W - 594
for x0, y0, x1, y1 in L:
    msp.add_line((x0 + DX, y0), (x1 + DX, y1), dxfattribs=at)
T = lambda s, x, y, h=1.5: msp.add_mtext(s, dxfattribs={"insert": (x + DX, y), "char_height": h, "layer": "FORMAT", "style": "SLDTEXTSTYLE0"})
for s, x, y in [("DRAWN",404.6,42.4),("CHK'D",404.9,38.2),("APPV'D",404.4,34.1),("MFG",405.1,29.7),("Q.A",405.5,25.5),
                ("FINISH:",438.4,63.9),("NAME",418.3,46.5),("SIGNATURE",434,46.6),("DATE",451.2,46.6),
                ("MATERIAL:",459.6,26),("DO NOT SCALE DRAWING",516.6,62.5),("REVISION",557.3,62.3),
                ("TITLE:",504.1,46.6),("DWG NO.",504,26),("SCALE:" + a.scale,504.1,12.9),
                ("SHEET 1 OF 1",548.5,12.9),("WEIGHT:",459.6,12.9)]:
    T(s, x, y)
T(a.size, 574.9, 24.4, 2.91); T(a.title, 538.9, 23.6, 6.35)
if a.material: T(a.material, 459.6, 21.5)
T("UNLESS OTHERWISE SPECIFIED:\\PDIMENSIONS ARE IN MILLIMETERS\\PSURFACE FINISH:\\PTOLERANCES:\\P  LINEAR:\\P  ANGULAR:", 404.6, 62)
T("DEBURR AND\\PBREAK SHARP\\PEDGES", 485.3, 62.1)
doc.saveas(a.out)
print("wrote", a.out)
