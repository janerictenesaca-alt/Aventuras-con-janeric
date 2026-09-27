"""Modelo 3D, DXF y archivos por pieza del bípode tipo Vortex (v3).

Uso:  python3 vortex_build.py   ->  ../v3/
"""
import json
import math
import os

import cadquery as cq
import ezdxf
from shapely.geometry import Point, box

import vortex_geo as g

OUT = os.path.join(os.path.dirname(__file__), "..", "v3")
for d in ("dxf", "step", "stl", "glb"):
    os.makedirs(os.path.join(OUT, d), exist_ok=True)

AZUL = cq.Color(0.10, 0.36, 0.78)
NARANJA = cq.Color(0.93, 0.42, 0.10)
ALU = cq.Color(0.80, 0.82, 0.85)
GRIS = cq.Color(0.68, 0.70, 0.72)
ACERO = cq.Color(0.28, 0.30, 0.33)
LATON = cq.Color(0.85, 0.66, 0.28)
CUERDA = cq.Color(0.95, 0.55, 0.10)
VIENTO = cq.Color(0.15, 0.55, 0.30)


# ------------------------------------------------------------------ utilidades
def extruir(contorno, espesor, huecos=(), cortes=()):
    wp = cq.Workplane("XY").polyline(list(contorno.exterior.coords)[:-1]).close().extrude(espesor)
    for _, x, y, d in huecos:
        wp = wp.cut(cq.Workplane("XY").center(x, y).circle(d / 2).extrude(espesor))
    for c in cortes:
        wp = wp.cut(cq.Workplane("XY").polyline(list(c.exterior.coords)[:-1]).close().extrude(espesor))
    return wp


def tubo(od, idi, largo):
    """Tubo a lo largo de -Z desde z=0 (punta de arriba)."""
    return cq.Workplane("XY").circle(od / 2).circle(idi / 2).extrude(largo).translate((0, 0, -largo))


def cil_y(d, largo):
    return cq.Workplane("XZ").circle(d / 2).extrude(largo / 2, both=True)


def hueco_y(sol, d, z, largo=200):
    return sol.cut(cil_y(d, largo).translate((0, 0, z)))


def dxf(nombre, contorno, huecos=(), cortes=(), nota=""):
    doc = ezdxf.new("R2010", setup=True)
    doc.units = ezdxf.units.MM
    doc.layers.add("CORTE", color=1)
    doc.layers.add("NOTAS", color=3)
    msp = doc.modelspace()
    msp.add_lwpolyline(list(contorno.exterior.coords), close=True, dxfattribs={"layer": "CORTE"})
    for i in contorno.interiors:
        msp.add_lwpolyline(list(i.coords), close=True, dxfattribs={"layer": "CORTE"})
    for _, x, y, d in huecos:
        msp.add_circle((x, y), d / 2, dxfattribs={"layer": "CORTE"})
    for c in cortes:
        msp.add_lwpolyline(list(c.exterior.coords), close=True, dxfattribs={"layer": "CORTE"})
    minx, miny, *_ = contorno.bounds
    msp.add_text(nota, height=5, dxfattribs={"layer": "NOTAS"}).set_placement((minx, miny - 14))
    doc.saveas(os.path.join(OUT, "dxf", nombre + ".dxf"))


def guardar(nombre, sol, color):
    cq.exporters.export(sol, os.path.join(OUT, "step", nombre + ".step"))
    cq.exporters.export(sol, os.path.join(OUT, "stl", nombre + ".stl"), tolerance=0.05, angularTolerance=0.2)
    a = cq.Assembly(name="pieza")
    a.add(sol, name=nombre, color=color)
    a.export(os.path.join(OUT, "glb", nombre + ".glb"))


# ------------------------------------------------------------------ piezas
ventanas = [g.ventana(*v) for v in g.VENTANAS]
C2_BARRA = 25.8
HUECOS_PLACA = [(n, x, z, (C2_BARRA if n == "C2" else d)) for n, x, z, d in g.HUECOS_PLACA]


def placa_cuerpo():
    return extruir(g.contorno_placa(), g.PL_T, HUECOS_PLACA, ventanas)


def casquillo():
    t = tubo(g.CAS_OD, g.CAS_ID, g.CAS_L)
    t = hueco_y(t, g.D_PATA, -(g.S_TOPE + g.CAS_L / 2))
    t = hueco_y(t, g.D_PATA, -(g.S_PASADOR + g.CAS_L / 2))
    return t


NERVIO_H = g.NERVIO_Z[1] - g.NERVIO_Z[0]


def nervio():
    return cq.Workplane("XY").box(g.PL_T, g.PL_GAP, NERVIO_H)


def barra_carga():
    L = g.PL_GAP + 2 * g.PL_T + 28
    b = cil_y(25.4, L)
    for s in (-1, 1):
        b = b.cut(cq.Workplane("XY").circle(2.6).extrude(20, both=True).translate((0, s * (L / 2 - 7), 0)))
    return b


def pata_sup():
    t = tubo(g.SUP_OD, g.SUP_OD - 2 * g.SUP_E, g.SUP_L)
    t = t.cut(cq.Workplane("XY").box(g.MUESCA_A, 100, 2 * g.MUESCA_P).translate((0, 0, 0)))
    t = t.cut(cil_y(g.MUESCA_A, 100).translate((0, 0, -g.MUESCA_P)))
    for h in g.HUECOS_SUP:
        t = hueco_y(t, g.D_PATA, -h)
    return t


def pata_inf():
    t = tubo(g.INF_OD, g.INF_OD - 2 * g.INF_E, g.INF_TUBO)
    t = hueco_y(t, g.D_PATA, -g.INF_HUECO_ARRIBA)
    esp = tubo(g.SUP_OD, g.SUP_OD - 2 * g.SUP_E, g.ESP_L).translate((0, 0, -(g.INF_TUBO - g.ESP_DENTRO)))
    t = t.union(esp)
    for p in g.ESP_PERNOS:  # pernos fijos (se ven como huecos en X)
        t = t.cut(cq.Workplane("YZ").circle(g.D_PATA / 2).extrude(100, both=True).translate((0, 0, -g.INF_TUBO + p)))
    t = hueco_y(t, g.D_PATA, -(g.INF_TUBO + g.ESP_L - g.ESP_DENTRO - g.ESP_HUECO))
    return t


def garra_placa():
    return extruir(g.contorno_garra(), g.PIE_PLACA_T, g.HUECOS_GARRA)


def pie_garra():
    cas = tubo(g.INF_OD, g.INF_OD - 2 * g.INF_E, g.PIE_CAS_L)
    cas = hueco_y(cas, g.D_PATA, -g.PIE_HUECO)
    ranura = cq.Workplane("XY").box(g.INF_OD + 10, g.PIE_PLACA_T + 0.5, 55).translate((0, 0, -g.PIE_CAS_L + 27.5))
    cas = cas.cut(ranura)
    pl = garra_placa().translate((0, 0, -g.PIE_PLACA_T / 2)).rotate((0, 0, 0), (1, 0, 0), 90) \
        .translate((0, 0, -g.PIE_CAS_L))
    return cas.union(pl)


def carrete():
    t = tubo(g.INF_OD, g.INF_OD - 2 * g.INF_E, g.CAR_TUBO_L)
    t = hueco_y(t, g.D_PATA, -g.CAR_TUBO_L / 2, 200)
    disco = extruir(Point(0, 0).buffer(g.CAR_DISCO / 2, quad_segs=64), g.CAR_T,
                    g.huecos_circulo(g.CAR_HUECOS, g.CAR_PCD, g.D_CAR, 22.5) + [("C", 0, 0, g.INF_OD + 0.4)])
    return t, disco.translate((0, 0, -g.CAR_T)), disco.translate((0, 0, -g.CAR_TUBO_L))


def union():
    cas = tubo(g.INF_OD, g.INF_OD - 2 * g.INF_E, g.UNI_CAS_L)
    cas = hueco_y(cas, g.D_PATA, -g.INF_HUECO_ARRIBA)
    disco = extruir(Point(0, 0).buffer(g.UNI_DISCO / 2, quad_segs=64), g.UNI_T,
                    g.huecos_circulo(g.UNI_HUECOS, g.UNI_PCD, g.D_AM, 18) + [("C", 0, 0, g.SUP_OD + 0.4)]) \
        .translate((0, 0, -g.UNI_CAS_L - g.UNI_T))
    esp = tubo(g.SUP_OD, g.SUP_OD - 2 * g.SUP_E, g.ESP_L).translate((0, 0, -(g.UNI_CAS_L + g.UNI_T - g.ESP_DENTRO)))
    esp = hueco_y(esp, g.D_PATA, -(g.UNI_CAS_L + g.UNI_T + g.ESP_L - g.ESP_DENTRO - g.ESP_HUECO))
    return cas.union(esp), disco


def pasador(d, largo, cabeza=1.6):
    p = cil_y(d, largo)
    p = p.union(cil_y(d * cabeza, 4).translate((0, largo / 2 + 2, 0)))
    anillo = cq.Workplane("XZ").center(0, 0).circle(d * 1.4).circle(d * 1.4 - 2).extrude(1.5) \
        .rotate((0, 0, 0), (0, 0, 1), 90).translate((0, largo / 2 + 4 + d * 1.4, 0))
    return p.union(anillo)


# ------------------------------------------------------------------ archivos por pieza
piezas = {
    "01_casquillo_cabeza": (casquillo(), AZUL),
    "02_placa_cuerpo_cabeza": (placa_cuerpo(), AZUL),
    "03_nervio_cabeza": (nervio(), AZUL),
    "04_barra_carga": (barra_carga(), ACERO),
    "05_pata_superior": (pata_sup(), ALU),
    "06_pata_inferior": (pata_inf(), GRIS),
    "07_pie_garra": (pie_garra(), NARANJA),
    "08_carrete_amarre": (carrete()[0].union(carrete()[1]).union(carrete()[2]), AZUL),
    "09_placa_union": (union()[0].union(union()[1]), NARANJA),
}
for n, (s, c) in piezas.items():
    guardar(n, s, c)

dxf("02_placa_cuerpo_cabeza_Al6061_12.7mm_x2", g.contorno_placa(), HUECOS_PLACA, ventanas,
    "Placa del cuerpo de la cabeza - aluminio 6061-T6 1/2\" (12,7 mm) - cantidad 2")
dxf("03_nervio_cabeza_Al6061_12.7mm_x2", box(-g.PL_GAP / 2, 0, g.PL_GAP / 2, NERVIO_H), nota=
    "Nervio interno - aluminio 6061-T6 12,7 mm - 63,5 x 82 - cantidad 2")
dxf("07_garra_A36_12mm_x2", g.contorno_garra(), g.HUECOS_GARRA, nota="Garra del pie - acero A36 12 mm - cantidad 2")
dxf("08_disco_carrete_Al6061_9.5mm_x4", Point(0, 0).buffer(g.CAR_DISCO / 2, quad_segs=90),
    g.huecos_circulo(g.CAR_HUECOS, g.CAR_PCD, g.D_CAR, 22.5) + [("C", 0, 0, g.INF_OD + 0.4)],
    nota="Disco del carrete de amarre - aluminio 6061-T6 3/8\" - cantidad 4 (2 azules, 2 naranjas)")
dxf("09_disco_union_Al6061_12.7mm_x2", Point(0, 0).buffer(g.UNI_DISCO / 2, quad_segs=90),
    g.huecos_circulo(g.UNI_HUECOS, g.UNI_PCD, g.D_AM, 18) + [("C", 0, 0, g.SUP_OD + 0.4)],
    nota="Disco de la placa de unión - aluminio 6061-T6 1/2\" - cantidad 2")

# ------------------------------------------------------------------ armado (2 patas de abajo por lado, hueco 563)
H = 563.0
s_sup = g.S_PUNTA_PATA
s_i1 = s_sup + H - g.INF_HUECO_ARRIBA
s_i1_fin = s_i1 + g.INF_TUBO
s_uni = s_i1_fin
s_i2 = s_uni + g.UNI_CAS_L + g.UNI_T
s_i2_fin = s_i2 + g.INF_TUBO
s_pie = s_i2_fin
s_punta = s_pie + g.PIE_CAS_L - g.GARRA_PUNTA
ZH = s_punta * g.CA        # centro de la cabeza sobre el suelo (eje z=0 en el centro de la cabeza)


def en_eje(sol, lado, s):
    x, z = g.eje(lado, s)
    return sol.rotate((0, 0, 0), (0, 1, 0), -g.ANG * lado).translate((x, 0, z + ZH))


asm = cq.Assembly(name="bipode_vortex")
pl = placa_cuerpo().rotate((0, 0, 0), (1, 0, 0), 90)       # (x, y, t) -> (x, -t, y)
asm.add(pl.translate((0, g.PL_GAP / 2 + g.PL_T, ZH)), name="placa_delantera", color=AZUL)
asm.add(pl.translate((0, -g.PL_GAP / 2, ZH)), name="placa_trasera", color=AZUL)
for sx in (-1, 1):
    asm.add(nervio().translate((sx * g.NERVIO_X, 0, ZH + (g.NERVIO_Z[0] + g.NERVIO_Z[1]) / 2)), name=f"nervio{sx}", color=AZUL)
L_PAS = g.PL_GAP + 2 * g.PL_T + 12
for n, x, z, d in HUECOS_PLACA:
    if n.startswith("P"):
        asm.add(pasador(15.9, L_PAS).translate((x, 0, z + ZH)), name="pas_" + n, color=LATON)
    if n == "C2":
        asm.add(barra_carga().translate((x, 0, z + ZH)), name="barra_carga", color=ACERO)

for lado, t in ((-1, "i"), (1, "d")):
    asm.add(en_eje(casquillo(), lado, -g.CAS_L / 2), name="cas_" + t, color=AZUL)
    asm.add(en_eje(pata_sup(), lado, s_sup), name="sup_" + t, color=ALU)
    asm.add(en_eje(pata_inf(), lado, s_i1), name="inf1_" + t, color=GRIS)
    a, b = union()
    asm.add(en_eje(a, lado, s_uni), name="uni_" + t, color=GRIS)
    asm.add(en_eje(b, lado, s_uni), name="unid_" + t, color=NARANJA)
    asm.add(en_eje(pata_inf(), lado, s_i2), name="inf2_" + t, color=GRIS)
    asm.add(en_eje(pie_garra(), lado, s_pie), name="pie_" + t, color=NARANJA)
    tc, d1, d2 = carrete()
    s_car = s_sup + g.HUECOS_SUP[1] - g.CAR_TUBO_L / 2
    asm.add(en_eje(tc, lado, s_car), name="car_" + t, color=AZUL)
    asm.add(en_eje(d1, lado, s_car), name="card1_" + t, color=AZUL)
    asm.add(en_eje(d2, lado, s_car), name="card2_" + t, color=NARANJA)
    # pasadores de bola 3/8" (latón) y pernos de tope
    for s, od in ((g.S_PASADOR, g.CAS_OD), (s_i1 + g.INF_HUECO_ARRIBA, g.INF_OD),
                  (s_uni + g.INF_HUECO_ARRIBA, g.INF_OD), (s_i2 + g.INF_HUECO_ARRIBA, g.INF_OD),
                  (s_pie + g.PIE_HUECO, g.INF_OD), (s_sup + g.HUECOS_SUP[1], g.INF_OD)):
        x, z = g.eje(lado, s)
        asm.add(pasador(9.5, od + 14).translate((x, 0, z + ZH)), name=f"pp_{t}_{int(s)}", color=LATON)
    x, z = g.eje(lado, g.S_TOPE)
    asm.add(cil_y(9.5, g.CAS_OD + 16).translate((x, 0, z + ZH)), name="tope_" + t, color=ACERO)


def cuerda(a, b, r=5.5):
    a, b = cq.Vector(*a), cq.Vector(*b)
    return cq.Workplane(obj=cq.Solid.makeCylinder(r, (b - a).Length, a, (b - a).normalized()))


def p_pie(lado, hx, hy):
    ang = math.radians(-g.ANG * lado)
    lx = hx * math.cos(ang) + hy * math.sin(ang)
    ly = -hx * math.sin(ang) + hy * math.cos(ang)
    x, z = g.eje(lado, s_pie + g.PIE_CAS_L)
    return (x + lx, 0, z + ZH + ly)


asm.add(cuerda(p_pie(-1, -36, -24), p_pie(1, 36, -24)), name="maniota", color=CUERDA)
for n, x, z, d in HUECOS_PLACA:
    if n.startswith("O"):
        for sy in (-1, 1):
            asm.add(cuerda((x, 0, z + ZH), (x * 1.5, sy * (z + ZH), 0), 4.5), name=f"viento_{n}_{sy}", color=VIENTO)

asm.export(os.path.join(OUT, "bipode_vortex_armado.step"))
asm.export(os.path.join(OUT, "bipode_vortex_armado.glb"))
# cabeza sola (para el plano)
cab = cq.Assembly(name="cabeza")
cab.add(pl.translate((0, g.PL_GAP / 2 + g.PL_T, 0)), name="pd", color=AZUL)
cab.add(pl.translate((0, -g.PL_GAP / 2, 0)), name="pt", color=AZUL)
for sx in (-1, 1):
    cab.add(nervio().translate((sx * g.NERVIO_X, 0, (g.NERVIO_Z[0] + g.NERVIO_Z[1]) / 2)), name=f"n{sx}", color=AZUL)
for lado in (-1, 1):
    x, z = g.eje(lado, -g.CAS_L / 2)
    cab.add(casquillo().rotate((0, 0, 0), (0, 1, 0), -g.ANG * lado).translate((x, 0, z)), name=f"c{lado}", color=AZUL)
    x, z = g.eje(lado, g.S_PASADOR)
    cab.add(pasador(9.5, g.CAS_OD + 14).translate((x, 0, z)), name=f"pp{lado}", color=LATON)
    x, z = g.eje(lado, g.S_TOPE)
    cab.add(cil_y(9.5, g.CAS_OD + 16).translate((x, 0, z)), name=f"t{lado}", color=ACERO)
for n, x, z, d in HUECOS_PLACA:
    if n.startswith("P"):
        cab.add(pasador(15.9, L_PAS).translate((x, 0, z)), name="p" + n, color=LATON)
    if n == "C2":
        cab.add(barra_carga().translate((x, 0, z)), name="bc", color=ACERO)
cab.export(os.path.join(OUT, "glb", "00_cabeza_armada.glb"))
cab.export(os.path.join(OUT, "step", "00_cabeza_armada.step"))

json.dump(dict(ZH=ZH, s_punta=s_punta, carga=ZH - 66, arriba=ZH + 82), open(os.path.join(OUT, "armado.json"), "w"))
print("altura carga", round(ZH - 66), "arriba", round(ZH + 82))
