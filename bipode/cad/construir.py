"""Genera el modelo 3D (STEP, STL, GLB) y los DXF de corte del bípode.

Uso:  python3 construir.py
Salida: ../archivos/
"""
import math
import os

import cadquery as cq
import ezdxf

import geometria as g

OUT = os.path.join(os.path.dirname(__file__), "..", "archivos")
os.makedirs(os.path.join(OUT, "dxf"), exist_ok=True)
os.makedirs(os.path.join(OUT, "stl"), exist_ok=True)
os.makedirs(os.path.join(OUT, "step"), exist_ok=True)

H_ARMADO = 675.0          # hueco de unión que se muestra en el modelo armado
Y = cq.Vector(0, 1, 0)

AZUL = cq.Color(0.12, 0.36, 0.72)
NARANJA = cq.Color(0.90, 0.40, 0.10)
ALU = cq.Color(0.78, 0.80, 0.83)
ACERO = cq.Color(0.30, 0.32, 0.35)
LATON = cq.Color(0.80, 0.62, 0.25)
CUERDA = cq.Color(0.95, 0.55, 0.10)
CUERDA2 = cq.Color(0.15, 0.55, 0.30)


# ------------------------------------------------------------------ 2D -> 3D
def placa(contorno, huecos, espesor, ventana=None, hueco_central=None):
    """Extruye un contorno de shapely en XY (espesor en +Z) y corta los huecos."""
    pts = list(contorno.exterior.coords)[:-1]
    wp = cq.Workplane("XY").polyline(pts).close().extrude(espesor)
    for _, x, y, d in huecos:
        wp = wp.cut(cq.Workplane("XY").center(x, y).circle(d / 2).extrude(espesor))
    if ventana:
        cx, cy, L, W = ventana
        wp = wp.cut(cq.Workplane("XY").center(cx, cy).slot2D(L, W).extrude(espesor))
    if hueco_central:
        wp = wp.cut(cq.Workplane("XY").circle(hueco_central / 2).extrude(espesor))
    return wp


def dxf(nombre, contorno, huecos, ventana=None, hueco_central=None, nota=""):
    doc = ezdxf.new("R2010", setup=True)
    doc.units = ezdxf.units.MM
    doc.layers.add("CORTE", color=1)
    doc.layers.add("NOTAS", color=3)
    msp = doc.modelspace()
    msp.add_lwpolyline(list(contorno.exterior.coords), close=True, dxfattribs={"layer": "CORTE"})
    for _, x, y, d in huecos:
        msp.add_circle((x, y), d / 2, dxfattribs={"layer": "CORTE"})
    if ventana:
        cx, cy, L, W = ventana
        r, a = W / 2, L / 2 - W / 2
        msp.add_lwpolyline([(cx - a, cy - r, 0, 0, 1), (cx + a, cy - r, 0, 0, 1),
                            (cx + a, cy + r, 0, 0, 1), (cx - a, cy + r, 0, 0, 1)],
                           format="xyseb", close=True, dxfattribs={"layer": "CORTE"})
        # arcos de los extremos: bulge 1 = media vuelta
        pl = msp.query("LWPOLYLINE")[-1]
        pl.set_points([(cx - a, cy - r, 0), (cx + a, cy - r, 1), (cx + a, cy + r, 0),
                       (cx - a, cy + r, 1)], format="xyb")
    if hueco_central:
        msp.add_circle((0, 0), hueco_central / 2, dxfattribs={"layer": "CORTE"})
    minx, miny, maxx, maxy = contorno.bounds
    msp.add_text(nota, height=6, dxfattribs={"layer": "NOTAS"}).set_placement((minx, miny - 15))
    doc.saveas(os.path.join(OUT, "dxf", nombre + ".dxf"))


def tubo(od, esp, largo):
    return (cq.Workplane("XY").circle(od / 2).circle(od / 2 - esp).extrude(largo))


def en_eje(solido, lado, s_arriba, giro_extra=None):
    """Coloca un sólido construido a lo largo de -Z desde z=0 (arriba) sobre el eje de una pata."""
    ang = -g.ANG if lado > 0 else g.ANG
    x, v = g.eje(lado, s_arriba)
    return solido.rotate((0, 0, 0), (0, 1, 0), ang).translate((x, 0, v + Z_CAB))


def barra_y(d, largo):
    return cq.Workplane("XZ").circle(d / 2).extrude(largo / 2, both=True)


# ------------------------------------------------------------------ medidas del armado
S_SUP_ARRIBA = g.S_TOPE_PATA
S_INF_ARRIBA = S_SUP_ARRIBA + H_ARMADO - g.HUECOS_INF[0]
S_INF_ABAJO = S_INF_ARRIBA + g.INF_L
S_PUNTA = S_INF_ABAJO - g.PIE_PUNTA_Y
Z_CAB = S_PUNTA * math.cos(math.radians(g.ANG)) - g.P_DER[1]   # la punta del pie queda en z = 0


# ------------------------------------------------------------------ piezas
def pieza_placa():
    return placa(g.contorno_placa(), g.HUECOS_PLACA, g.PLACA_AL, ventana=g.VENTANA)


def pieza_casquillo():
    t = tubo(g.CAS_OD, g.CAS_ESP, g.CAS_L).translate((0, 0, -g.CAS_L))
    for s in (g.S_PERNO_FIJO, g.S_PASADOR):
        z = -(s + 80.0)
        t = t.cut(barra_y(g.D_PATA, 100).translate((0, 0, z)))
    return t


def pieza_pata_sup():
    t = tubo(g.SUP_OD, g.SUP_ESP, g.SUP_L).translate((0, 0, -g.SUP_L))
    for h in g.HUECOS_SUP:
        t = t.cut(barra_y(g.D_PATA, 100).translate((0, 0, -h)))
    return t


def pieza_pata_inf():
    t = tubo(g.INF_OD, g.INF_ESP, g.INF_L).translate((0, 0, -g.INF_L))
    for h in g.HUECOS_INF:
        t = t.cut(barra_y(g.D_PATA, 100).translate((0, 0, -h)))
    ranura = cq.Workplane("XY").box(g.INF_OD + 10, g.PIE_RANURA_A, g.PIE_RANURA_L) \
        .translate((0, 0, -g.INF_L + g.PIE_RANURA_L / 2))
    t = t.cut(ranura)
    t = t.cut(barra_y(g.D_PERNO12, 100).translate((0, 0, -g.INF_L + g.PIE_PERNO_Y)))
    return t


def pieza_anillo_disco():
    from shapely.geometry import Point
    return placa(Point(0, 0).buffer(g.ANI_OD / 2, quad_segs=64), g.HUECOS_ANILLO,
                 g.PLACA_AL, hueco_central=g.ANI_HUECO_C)


def pieza_anillo():
    """Manguito + disco. z=0 es la punta de arriba del manguito, crece hacia -Z."""
    man = tubo(g.MAN_OD, g.MAN_ESP, g.MAN_L).translate((0, 0, -g.MAN_L))
    man = man.cut(barra_y(g.D_PATA, 120).translate((0, 0, -g.MAN_L + g.MAN_PASADOR_Z)))
    disco = pieza_anillo_disco().translate((0, 0, -g.MAN_L + g.MAN_DISCO_Z - g.PLACA_AL / 2))
    return man.union(disco)


def pieza_pie_garra():
    return placa(g.contorno_pie_garra(), g.HUECOS_PIE_GARRA, g.PLACA_AC)


def pieza_barra_carga():
    largo = g.GAP + 2 * g.PLACA_AL + 2 * 14
    b = barra_y(25.4, largo)
    for sgn in (-1, 1):
        b = b.cut(cq.Workplane("XY").circle(2.6).extrude(20, both=True)
                  .translate((0, sgn * (largo / 2 - 7), 0)))
    return b


def pieza_distanciador():
    return cq.Workplane("XZ").circle(12.7).circle(12.7 - 3.2).extrude(g.GAP / 2, both=True)


# ------------------------------------------------------------------ piezas sueltas
piezas = {
    "01_placa_cabeza": pieza_placa(),
    "02_casquillo": pieza_casquillo(),
    "03_barra_carga": pieza_barra_carga(),
    "04_distanciador": pieza_distanciador(),
    "05_pata_superior": pieza_pata_sup(),
    "06_pata_inferior": pieza_pata_inf(),
    "07_anillo_amarre": pieza_anillo(),
    "08_pie_garra": pieza_pie_garra(),
    "09a_pie_plano_lengua": placa(g.contorno_pie_plano_lengua(), g.HUECOS_PIE_PLANO_LENGUA, g.PLACA_AC),
    "09b_pie_plano_base": cq.Workplane("XY").rect(g.BASE_LADO, g.BASE_LADO).extrude(g.PLACA_AC_BASE)
        .edges("|Z").fillet(10)
        .cut(cq.Workplane("XY").pushPoints([(x, y) for _, x, y, _ in g.HUECOS_BASE]).circle(7).extrude(20)),
    "09c_pie_plano_oreja": placa(g.contorno_oreja(), g.HUECOS_OREJA, g.PLACA_AC_BASE),
}
for n, p in piezas.items():
    cq.exporters.export(p, os.path.join(OUT, "step", n + ".step"))
    cq.exporters.export(p, os.path.join(OUT, "stl", n + ".stl"), tolerance=0.05, angularTolerance=0.2)

# ------------------------------------------------------------------ DXF para corte
dxf("01_placa_cabeza_aluminio_6061_3-8in_x2", g.contorno_placa(), g.HUECOS_PLACA, ventana=g.VENTANA,
    nota="Placa de cabeza - aluminio 6061-T6 9,53 mm (3/8\") - cantidad 2")
from shapely.geometry import Point
dxf("07_disco_anillo_aluminio_6061_3-8in_x2", Point(0, 0).buffer(g.ANI_OD / 2, quad_segs=90),
    g.HUECOS_ANILLO, hueco_central=g.ANI_HUECO_C,
    nota="Disco de anillo de amarre - aluminio 6061-T6 9,53 mm - cantidad 2")
dxf("08_pie_garra_acero_A36_10mm_x2", g.contorno_pie_garra(), g.HUECOS_PIE_GARRA,
    nota="Pie de garra - acero A36 10 mm - cantidad 2")
dxf("09a_pie_plano_lengua_acero_A36_10mm_x2", g.contorno_pie_plano_lengua(), g.HUECOS_PIE_PLANO_LENGUA,
    nota="Lengua del pie plano - acero A36 10 mm - cantidad 2 (opcional)")
from shapely.geometry import box
dxf("09b_pie_plano_base_acero_A36_8mm_x2",
    box(-80, -80, 80, 80).buffer(-10).buffer(10, quad_segs=16), g.HUECOS_BASE,
    nota="Base del pie plano - acero A36 8 mm - cantidad 2 (opcional)")
dxf("09c_pie_plano_oreja_acero_A36_8mm_x4", g.contorno_oreja(), g.HUECOS_OREJA,
    nota="Oreja del pie plano - acero A36 8 mm - cantidad 4 (opcional)")

# ------------------------------------------------------------------ armado
asm = cq.Assembly(name="bipode")
pl = pieza_placa()
# placa en XY -> girar para que quede vertical (grosor en Y)
pl_v = pl.rotate((0, 0, 0), (1, 0, 0), 90)       # (u, v, t) -> (u, -t, v)
asm.add(pl_v.translate((0, g.GAP / 2 + g.PLACA_AL, Z_CAB)), name="placa_delantera", color=AZUL)
asm.add(pl_v.translate((0, -g.GAP / 2, Z_CAB)), name="placa_trasera", color=AZUL)

for n, x, y, d in g.HUECOS_PLACA:
    if n.startswith("B"):
        asm.add(pieza_barra_carga().translate((x, 0, y + Z_CAB)), name="barra_" + n, color=ACERO)
    if n.startswith("D"):
        asm.add(pieza_distanciador().translate((x, 0, y + Z_CAB)), name="dist_" + n, color=ACERO)
        asm.add(barra_y(12.7, g.GAP + 2 * g.PLACA_AL + 30).translate((x, 0, y + Z_CAB)),
                name="perno_" + n, color=ACERO)
    if n.startswith("C"):
        asm.add(barra_y(9.5, g.GAP + 2 * g.PLACA_AL + 26).translate((x, 0, y + Z_CAB)),
                name="pasador_" + n, color=LATON)

for lado, tag in ((-1, "izq"), (1, "der")):
    asm.add(en_eje(pieza_casquillo(), lado, -80.0), name="casquillo_" + tag, color=AZUL)
    asm.add(en_eje(pieza_pata_sup(), lado, S_SUP_ARRIBA), name="pata_sup_" + tag, color=ALU)
    asm.add(en_eje(pieza_pata_inf(), lado, S_INF_ARRIBA), name="pata_inf_" + tag, color=ALU)
    # pasadores de unión (2 por pata)
    for hi in g.HUECOS_INF[:2]:
        x, v = g.eje(lado, S_INF_ARRIBA + hi)
        asm.add(barra_y(9.5, g.INF_OD + 30).translate((x, 0, v + Z_CAB)),
                name=f"pasador_union_{tag}_{int(hi)}", color=LATON)
    # anillo de amarre en el hueco 480
    s_pas = S_INF_ARRIBA + g.HUECOS_INF[2]
    s_arriba_man = s_pas - (g.MAN_L - g.MAN_PASADOR_Z)
    asm.add(en_eje(pieza_anillo(), lado, s_arriba_man), name="anillo_" + tag, color=NARANJA)
    x, v = g.eje(lado, s_pas)
    asm.add(barra_y(9.5, g.MAN_OD + 30).translate((x, 0, v + Z_CAB)), name="pasador_anillo_" + tag, color=LATON)
    # pie de garra: placa en el plano XZ
    pie = pieza_pie_garra().translate((0, 0, -g.PLACA_AC / 2)).rotate((0, 0, 0), (1, 0, 0), 90)
    asm.add(en_eje(pie, lado, S_INF_ABAJO), name="pie_" + tag, color=NARANJA)
    x, v = g.eje(lado, S_INF_ABAJO - g.PIE_PERNO_Y)
    asm.add(barra_y(12.7, g.INF_OD + 30).translate((x, 0, v + Z_CAB)), name="perno_pie_" + tag, color=ACERO)


def cuerda(a, b, r=5.5):
    a, b = cq.Vector(*a), cq.Vector(*b)
    return cq.Workplane(obj=cq.Solid.makeCylinder(r, (b - a).Length, a, (b - a).normalized()))


# maniota entre los huecos L de los pies
def punto_pie(lado, hx, hy):
    ang = math.radians(-g.ANG if lado > 0 else g.ANG)
    # coordenadas del pie: x a lo ancho, y hacia arriba por el eje
    lx, ly = hx * math.cos(ang) + hy * math.sin(ang), -hx * math.sin(ang) + hy * math.cos(ang)
    x, v = g.eje(lado, S_INF_ABAJO)
    return (x + lx, 0, v + Z_CAB + ly)


asm.add(cuerda(punto_pie(-1, -35, -25), punto_pie(1, 35, -25)), name="maniota", color=CUERDA)
# vientos adelante y atrás desde los distanciadores, a 45 grados
for sgn, nom in ((1, "adelante"), (-1, "atras")):
    for n, x, y, d in g.HUECOS_PLACA:
        if n.startswith("D"):
            z = y + Z_CAB
            asm.add(cuerda((x, 0, z), (x * 2.2, sgn * z, 0), 4.5), name=f"viento_{nom}_{n}", color=CUERDA2)

asm.save(os.path.join(OUT, "bipode_armado.step"))
asm.save(os.path.join(OUT, "bipode_armado.glb"))
print("Z cabeza", round(Z_CAB), "altura barra", round(Z_CAB - 78))
