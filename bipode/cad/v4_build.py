"""Modelo 3D, DXF y archivos por pieza del bípode tipo Vortex (v4).

Uso:  python3 v4_build.py   ->  ../v4/
"""
import json
import math
import os

import cadquery as cq
import ezdxf
from shapely.geometry import Point, box

import v4_geo as g

OUT = os.path.join(os.path.dirname(__file__), "..", "v4")
for d in ("dxf", "step", "stl", "glb"):
    os.makedirs(os.path.join(OUT, d), exist_ok=True)

AZUL = cq.Color(0.07, 0.30, 0.72)
NARANJA = cq.Color(0.95, 0.42, 0.08)
PLATA = cq.Color(0.80, 0.82, 0.85)
GRIS = cq.Color(0.55, 0.58, 0.62)
ACERO = cq.Color(0.22, 0.24, 0.27)
ORO = cq.Color(0.86, 0.68, 0.28)
CUERDA = cq.Color(0.98, 0.72, 0.10)
VIENTO = cq.Color(0.10, 0.45, 0.85)


# ------------------------------------------------------------------ utilidades
def extruir(contorno, espesor, huecos=(), cortes=(), redondeo=1.2):
    wp = cq.Workplane("XY").polyline(list(contorno.exterior.coords)[:-1]).close().extrude(espesor)
    for c in cortes:
        wp = wp.cut(cq.Workplane("XY").polyline(list(c.exterior.coords)[:-1]).close().extrude(espesor))
    for h in huecos:
        wp = wp.cut(cq.Workplane("XY").center(h[1], h[2]).circle(h[3] / 2).extrude(espesor))
    if redondeo:
        try:
            wp = wp.edges("not |Z").fillet(redondeo)
        except Exception:
            pass
    return wp


def tubo(od, idi, largo):
    """Tubo a lo largo de -Z desde z=0 (punta de arriba)."""
    return cq.Workplane("XY").circle(od / 2).circle(idi / 2).extrude(largo).translate((0, 0, -largo))


def cil_y(d, largo):
    return cq.Workplane("XZ").circle(d / 2).extrude(largo / 2, both=True)


def cil_x(d, largo):
    return cq.Workplane("YZ").circle(d / 2).extrude(largo / 2, both=True)


def hueco_y(sol, d, z, largo=300):
    return sol.cut(cil_y(d, largo).translate((0, 0, z)))


def ranuras_boca(sol, z_boca, od):
    """3 ranuras de alineación F en la boca (z_boca), abiertas hacia abajo."""
    for a in g.RANURAS_ANG:
        r = cq.Workplane("XY").box(od, g.RANURA_A, g.RANURA_P * 2).translate((od / 2, 0, z_boca)) \
            .rotate((0, 0, 0), (0, 0, 1), a + 90)
        sol = sol.cut(r)
    return sol


def dxf(nombre, contorno, huecos=(), cortes=(), nota=""):
    doc = ezdxf.new("R2010", setup=True)
    doc.units = ezdxf.units.MM
    doc.layers.add("CORTE", color=1)
    doc.layers.add("NOTAS", color=3)
    msp = doc.modelspace()
    msp.add_lwpolyline(list(contorno.exterior.coords), close=True, dxfattribs={"layer": "CORTE"})
    for c in cortes:
        msp.add_lwpolyline(list(c.exterior.coords), close=True, dxfattribs={"layer": "CORTE"})
    for h in huecos:
        msp.add_circle((h[1], h[2]), h[3] / 2, dxfattribs={"layer": "CORTE"})
    minx, miny, *_ = contorno.bounds
    msp.add_text(nota, height=5, dxfattribs={"layer": "NOTAS"}).set_placement((minx, miny - 14))
    doc.saveas(os.path.join(OUT, "dxf", nombre + ".dxf"))


def guardar(nombre, sol, color):
    cq.exporters.export(sol, os.path.join(OUT, "step", nombre + ".step"))
    cq.exporters.export(sol, os.path.join(OUT, "stl", nombre + ".stl"), tolerance=0.05, angularTolerance=0.15)
    a = cq.Assembly(name="pieza")
    a.add(sol, name=nombre, color=color)
    a.export(os.path.join(OUT, "glb", nombre + ".glb"), tolerance=0.05, angularTolerance=0.15)


# ------------------------------------------------------------------ piezas
def placa():
    return extruir(g.contorno_placa(), g.PL_T, g.HUECOS_PLACA, g.cortes_placa())


def casquillo():
    """z=0 arriba (s=0), boca en z=-190."""
    t = tubo(g.HEMBRA_OD, g.HEMBRA_ID, g.CAS_L)
    for s in g.S_PERNOS:
        t = hueco_y(t, g.D12, -s)
    for gb in g.G_DESDE_BOCA:
        t = hueco_y(t, g.D38, -(g.CAS_L - gb))
    t = ranuras_boca(t, -g.CAS_L, g.HEMBRA_OD + 2)
    try:
        t = t.faces("<Z").edges().chamfer(1.0)
    except Exception:
        pass
    return t


def separador():
    return cq.Workplane("XZ").circle(12.7).circle(12.7 - 3.2).extrude(g.GAP / 2, both=True)


def bloque_c():
    w, h, y0 = g.BLOQUE_C
    b = cq.Workplane("XY").box(w, g.GAP, h).translate((0, 0, y0 + h / 2))
    b = b.cut(cq.Workplane("XY").circle(g.D_C_VERT / 2).extrude(200, both=True))
    for x in (-16.0, 16.0):
        b = b.cut(cil_y(g.D_M10, 200).translate((x, 0, 31.0)))
    return b.edges("|Y").fillet(4)


def barra_carga():
    L = g.GAP + 2 * g.PL_T + 28
    b = cil_y(25.4, L)
    for s in (-1, 1):
        b = b.cut(cil_x(5.2, 40).translate((0, s * (L / 2 - 7), 0)))
    return b.edges().chamfer(1.0)


def pata_afuera():
    """z=0 = punta del espigón (arriba). Tubo desde z=-(espiga fuera) hacia abajo."""
    fuera = g.PE_ESPIGA - g.PE_ESPIGA_DENTRO
    esp = tubo(g.MACHO_OD, g.MACHO_OD - 2 * g.MACHO_E, g.PE_ESPIGA)
    esp = hueco_y(esp, g.D38, -g.PE_HUECO_ESPIGA)
    t = tubo(g.EXT_OD, g.EXT_OD - 2 * g.EXT_E, g.PE_TUBO).translate((0, 0, -fuera))
    t = t.union(esp)
    for p in g.PE_PERNOS:
        t = t.cut(cil_x(g.D38, 200).translate((0, 0, -fuera - p)))
    boca = -fuera - g.PE_TUBO
    t = hueco_y(t, g.D38, boca + g.PE_HUECO_BOCA)
    t = ranuras_boca(t, boca, g.EXT_OD + 2)
    tope = cq.Workplane("YZ").circle(4.75).extrude(g.MACHO_OD / 2 + 6).translate((0, 0, -g.TOPE_DESDE_PUNTA)) \
        .rotate((0, 0, 0), (0, 0, 1), 90)
    return t.union(tope)


def pata_adentro():
    t = tubo(g.MACHO_OD, g.MACHO_OD - 2 * g.MACHO_E, g.PI_L)
    t = t.cut(cq.Workplane("XY").box(g.MUESCA_A, 100, 2 * g.MUESCA_P))
    t = t.cut(cil_y(g.MUESCA_A, 100).translate((0, 0, -g.MUESCA_P)))
    for h in g.PI_HUECOS + [g.PI_HUECO_PIE]:
        t = hueco_y(t, g.D38, -h)
    return t


def garra():
    return extruir(g.contorno_garra(), g.GARRA_T, g.HUECOS_GARRA, redondeo=1.0)


def pie_raptor():
    cas = tubo(g.HEMBRA_OD, 51.5, g.PIE_CAS_L)
    cas = hueco_y(cas, g.D38, -g.PIE_HUECO)
    cas = cas.cut(cq.Workplane("XY").box(g.HEMBRA_OD + 10, g.GARRA_T + 0.4, 60).translate((0, 0, -g.PIE_CAS_L + 30)))
    pl = garra().translate((0, 0, -g.GARRA_T / 2)).rotate((0, 0, 0), (1, 0, 0), 90).translate((0, 0, -g.PIE_CAS_L))
    return cas.union(pl)


def pie_plano():
    cas = tubo(g.HEMBRA_OD, 51.5, g.PIE_CAS_L)
    cas = hueco_y(cas, g.D38, -g.PIE_HUECO)
    oreja = cq.Workplane("XZ").rect(50, 70).extrude(5, both=True)
    oreja = oreja.cut(cil_y(g.D12, 20).translate((0, 0, -15)))
    lengua = oreja.translate((0, 0, -g.PIE_CAS_L - 25))
    base = cq.Workplane("XY").rect(g.BASE_LADO, g.BASE_LADO).extrude(g.BASE_T).edges("|Z").fillet(14)
    base = base.cut(cq.Workplane("XY").pushPoints([(h[1], h[2]) for h in g.HUECOS_BASE]).circle(7).extrude(40))
    orejas = None
    for sy in (-1, 1):
        o = cq.Workplane("XZ").rect(60, 60).extrude(4, both=True).edges("|Y").fillet(8)
        o = o.cut(cil_y(g.D12, 20).translate((0, 0, 10)))
        o = o.translate((0, sy * (5 + 0.5 + 4), g.BASE_T + 30))
        orejas = o if orejas is None else orejas.union(o)
    goma = cq.Workplane("XY").rect(g.BASE_LADO, g.BASE_LADO).extrude(5).edges("|Z").fillet(14).translate((0, 0, -5))
    abajo = base.union(orejas).translate((0, 0, -g.PIE_CAS_L - 25 - 15 - (g.BASE_T + 40)))
    return cas.union(lengua), abajo, goma.translate((0, 0, -g.PIE_CAS_L - 25 - 15 - (g.BASE_T + 40)))


def disco_amarre():
    return extruir(Point(0, 0).buffer(g.AM_DISCO_D / 2, quad_segs=64), g.AM_DISCO_T,
                   g.huecos_circulo(g.AM_HUECOS, g.AM_PCD, g.AM_D) + [("C", 0, 0, g.HEMBRA_OD + 0.4)], redondeo=1.5)


def placa_amarre():
    cuerpo = tubo(g.HEMBRA_OD, g.HEMBRA_ID, g.AM_CUERPO)
    cuerpo = hueco_y(cuerpo, g.D38, -g.G_DESDE_BOCA[0] + 0.0 - (g.AM_CUERPO - g.ESPIGA_DENTRO) * 0)
    cuerpo = ranuras_boca(cuerpo.rotate((0, 0, 0), (1, 0, 0), 180).translate((0, 0, -g.AM_CUERPO)), -g.AM_CUERPO,
                          g.HEMBRA_OD + 2).rotate((0, 0, 0), (1, 0, 0), 180).translate((0, 0, -g.AM_CUERPO))
    fuera = g.AM_ESPIGA - g.AM_ESPIGA_DENTRO
    esp = tubo(g.MACHO_OD, g.MACHO_OD - 2 * g.MACHO_E, g.AM_ESPIGA).translate((0, 0, -(g.AM_CUERPO - g.AM_ESPIGA_DENTRO)))
    esp = hueco_y(esp, g.D38, -(g.AM_CUERPO + fuera - g.PE_HUECO_ESPIGA))
    for p in (30.0, 90.0):
        esp = esp.cut(cil_x(g.D38, 200).translate((0, 0, -(g.AM_CUERPO - p))))
    tope = cq.Workplane("YZ").circle(4.75).extrude(g.MACHO_OD / 2 + 6).translate(
        (0, 0, -(g.AM_CUERPO + fuera - g.TOPE_DESDE_PUNTA))).rotate((0, 0, 0), (0, 0, 1), 90)
    d = disco_amarre()
    arriba = d.translate((0, 0, -g.AM_DISCOS_Z[0] - g.AM_DISCO_T / 2))
    abajo = d.translate((0, 0, -g.AM_DISCOS_Z[1] - g.AM_DISCO_T / 2))
    return cuerpo.union(esp).union(tope), arriba, abajo


def pasador(d, agarre, color_anillo=True):
    """Pasador de bola con botón y anillo, eje en Y, centrado."""
    p = cil_y(d, agarre + 6)
    p = p.union(cil_y(d * 1.9, 9).translate((0, agarre / 2 + 7.5, 0)))
    p = p.union(cil_y(d * 0.9, 5).translate((0, agarre / 2 + 14, 0)))
    for a in (0, 180):
        p = p.union(cq.Workplane("XY").sphere(d * 0.18).translate((d * 0.45, -agarre / 2 - 2, 0))
                    .rotate((0, 0, 0), (0, 1, 0), a))
    if color_anillo:
        anillo = cq.Workplane("XZ").circle(d * 1.6).circle(d * 1.6 - 1.8).extrude(1.2) \
            .rotate((0, 0, 0), (0, 0, 1), 90).translate((0, agarre / 2 + 12 + d * 1.6, 0))
        p = p.union(anillo)
    return p


def perno(d, largo):
    """Perno Allen (cabeza cilíndrica) con tuerca de seguridad, eje en Y."""
    b = cil_y(d, largo)
    cab = cq.Workplane("XZ").circle(d * 0.75).extrude(d * 0.7).edges(">Y").fillet(d * 0.12)
    cab = cab.cut(cq.Workplane("XZ").polygon(6, d * 0.5).extrude(d * 0.4).translate((0, d * 0.7, 0)))
    b = b.union(cab.translate((0, largo / 2 + d * 0.7, 0)))
    tuerca = cq.Workplane("XZ").polygon(6, d * 1.7).extrude(d * 0.8).edges("|Y").fillet(d * 0.08)
    b = b.union(tuerca.translate((0, -largo / 2, 0)))
    return b


# ------------------------------------------------------------------ guardar piezas
pe = pata_afuera()
pi = pata_adentro()
raptor = pie_raptor()
pp_a, pp_b, pp_g = pie_plano()
am_c, am_d1, am_d2 = placa_amarre()
piezas = {
    "01_placa_cabeza": (placa(), AZUL),
    "02_casquillo_cabeza": (casquillo(), AZUL),
    "03_separador": (separador(), ACERO),
    "04_bloque_c": (bloque_c(), AZUL),
    "05_barra_carga": (barra_carga(), ACERO),
    "06_pata_afuera": (pe, GRIS),
    "07_pata_adentro": (pi, PLATA),
    "08_pie_raptor": (raptor, NARANJA),
    "09_pie_plano": (pp_a.union(pp_b), NARANJA),
    "10_placa_amarre": (am_c.union(am_d1).union(am_d2), AZUL),
}
for n, (s, c) in piezas.items():
    guardar(n, s, c)

dxf("01_placa_cabeza_Al6061-T6_12.7mm_x2", g.contorno_placa(), g.HUECOS_PLACA, g.cortes_placa(),
    "01 Placa de cabeza - aluminio 6061-T6 1/2\" (12,7 mm) - cantidad 2")
dxf("08_garra_raptor_A36_12mm_x2", g.contorno_garra(), g.HUECOS_GARRA, nota="08 Garra del pie Raptor - acero A36 12 mm - cantidad 2")
dxf("10_disco_amarre_Al6061-T6_12.7mm_x4", Point(0, 0).buffer(g.AM_DISCO_D / 2, quad_segs=90),
    g.huecos_circulo(g.AM_HUECOS, g.AM_PCD, g.AM_D) + [("C", 0, 0, g.HEMBRA_OD + 0.4)],
    nota="10 Disco de la placa de amarre - aluminio 6061-T6 1/2\" - cantidad 4")
dxf("09_base_pie_plano_A36_10mm_x2", box(-75, -75, 75, 75).buffer(-14).buffer(14, quad_segs=16), g.HUECOS_BASE,
    nota="09 Base del pie plano - acero A36 10 mm - cantidad 2")
dxf("04_bloque_c_perfil_x1", box(-25, 14, 25, 48), [("V", 0, 31, 0.001)], nota="04 Bloque C (vista frontal) - Al 6061-T6")


# ------------------------------------------------------------------ cabeza armada
def cabeza():
    a = cq.Assembly(name="cabeza")
    pl = placa().rotate((0, 0, 0), (1, 0, 0), 90)            # (x, y, t) -> (x, -t, y)
    a.add(pl.translate((0, g.GAP / 2 + g.PL_T, 0)), name="placa_delantera", color=AZUL)
    a.add(pl.translate((0, -g.GAP / 2, 0)), name="placa_trasera", color=AZUL)
    a.add(bloque_c(), name="bloque_c", color=AZUL)
    L = g.GAP + 2 * g.PL_T
    for n, x, y, d, _ in g.HUECOS_PLACA:
        if n.startswith("I"):
            a.add(separador().translate((x, 0, y)), name="sep_" + n, color=ACERO)
            a.add(pasador(12.7, L + 2).translate((x, 0, y)), name="pas_" + n, color=ORO)
        if n.startswith("S"):
            a.add(perno(12.7, L + 4).translate((x, 0, y)), name="perno_" + n, color=ACERO)
        if n.startswith("C"):
            a.add(perno(10, L + 4).translate((x, 0, y)), name="perno_" + n, color=ACERO)
        if n.startswith("A"):
            a.add(pasador(12.7, L + 2).translate((x, 0, y)), name="pas_" + n, color=ORO)
        if n == "B":
            a.add(barra_carga(), name="barra_B", color=ACERO)
    for lado, t in ((-1, "i"), (1, "d")):
        x, y = g.eje(lado, 0)
        a.add(casquillo().rotate((0, 0, 0), (0, 1, 0), -g.ANG * lado).translate((x, 0, y)), name="cas_" + t, color=AZUL)
        x, y = g.eje(lado, g.CAS_L - g.G_DESDE_BOCA[0])
        a.add(pasador(9.5, g.HEMBRA_OD + 2).translate((x, 0, y)), name="pp_" + t, color=ORO)
    return a


cab = cabeza()
cab.export(os.path.join(OUT, "glb", "00_cabeza_armada.glb"), tolerance=0.05, angularTolerance=0.15)
cab.export(os.path.join(OUT, "step", "00_cabeza_armada.step"))

# ------------------------------------------------------------------ bípode armado: 2 patas de afuera + adentro en hueco 2
N_EXT, HUECO = 2, 2
s_boca = g.CAS_L
L = g.largo_pata(N_EXT, HUECO)
ZH = L * g.CA - g.eje(1, g.CAS_L)[1]       # altura del centro B sobre el suelo


def en_eje(sol, lado, s):
    x, y = g.eje(lado, s)
    return sol.rotate((0, 0, 0), (0, 1, 0), -g.ANG * lado).translate((x, 0, y + ZH))


asm = cq.Assembly(name="bipode_vortex_v4")
asm.add(cab, name="cabeza", loc=cq.Location(cq.Vector(0, 0, ZH)))
for lado, t in ((-1, "i"), (1, "d")):
    s = s_boca - g.ESPIGA_DENTRO                  # punta del espigón de la 1.ª pata de afuera
    for k in range(N_EXT):
        asm.add(en_eje(pe, lado, s), name=f"pe{k}_{t}", color=GRIS)
        x, y = g.eje(lado, s + g.PE_HUECO_ESPIGA)
        if k > 0:
            asm.add(pasador(9.5, g.EXT_OD + 2).translate((x, 0, y + ZH)), name=f"pp{k}_{t}", color=ORO)
        s += g.PE_TUBO
    boca = s + (g.PE_ESPIGA - g.PE_ESPIGA_DENTRO) - (g.PE_ESPIGA - g.PE_ESPIGA_DENTRO)
    boca = s_boca - g.ESPIGA_DENTRO + (g.PE_ESPIGA - g.PE_ESPIGA_DENTRO) + N_EXT * g.PE_TUBO
    p = g.PI_HUECOS[HUECO - 1]
    s_pi = boca - g.PE_HUECO_BOCA - p
    asm.add(en_eje(pi, lado, s_pi), name="pi_" + t, color=PLATA)
    x, y = g.eje(lado, boca - g.PE_HUECO_BOCA)
    asm.add(pasador(9.5, g.EXT_OD + 2).translate((x, 0, y + ZH)), name="ppi_" + t, color=ORO)
    s_pie = s_pi + g.PI_L - g.ESPIGA_DENTRO
    asm.add(en_eje(raptor, lado, s_pie), name="pie_" + t, color=NARANJA)
    x, y = g.eje(lado, s_pie + g.PIE_HUECO)
    asm.add(pasador(9.5, g.HEMBRA_OD + 2).translate((x, 0, y + ZH)), name="ppp_" + t, color=ORO)
    # placa de amarre de 2 pisos entre las 2 patas de afuera? se muestra en la unión de la 1.ª y 2.ª
s_final = s_pie + g.PIE_CAS_L - g.GARRA_PUNTA


def cuerda(a, b, r=5.5):
    a, b = cq.Vector(*a), cq.Vector(*b)
    return cq.Workplane(obj=cq.Solid.makeCylinder(r, (b - a).Length, a, (b - a).normalized()))


def p_pie(lado, hx, hy):
    ang = math.radians(-g.ANG * lado)
    lx = hx * math.cos(ang) + hy * math.sin(ang)
    ly = -hx * math.sin(ang) + hy * math.cos(ang)
    x, y = g.eje(lado, s_pie + g.PIE_CAS_L)
    return (x + lx, 0, y + ZH + ly)


asm.add(cuerda(p_pie(-1, -38, -24), p_pie(1, 36, -24), 6), name="maniota", color=CUERDA)
xa, ya = -30.0, 100.0
for sy, nom in ((1, "adelante"), (-1, "atras")):
    for sx in (-1, 1):
        asm.add(cuerda((sx * 46, 0, 100 + ZH), (sx * 700, sy * 0.55 * (ZH + 100), 0.45 * (ZH + 100)), 4.5), name=f"viento_{nom}_{sx}", color=VIENTO)
asm.export(os.path.join(OUT, "bipode_armado.glb"), tolerance=0.08, angularTolerance=0.2)
asm.export(os.path.join(OUT, "bipode_armado.step"))

json.dump(dict(ZH=ZH, largo_pata=L, abertura=g.abertura(N_EXT, HUECO)), open(os.path.join(OUT, "armado.json"), "w"))
print("altura B", round(ZH), "abertura", round(g.abertura(N_EXT, HUECO)))


# ------------------------------------------------------------------ vistas explotadas (para el plano)
def cabeza_explotada():
    a = cq.Assembly(name="cabeza_explotada")
    pl = placa().rotate((0, 0, 0), (1, 0, 0), 90)
    a.add(pl.translate((0, g.GAP / 2 + g.PL_T + 170, 0)), name="placa_delantera", color=AZUL)
    a.add(pl.translate((0, -g.GAP / 2 - 170, 0)), name="placa_trasera", color=AZUL)
    a.add(bloque_c().translate((0, 0, 60)), name="bloque_c", color=AZUL)
    L = g.GAP + 2 * g.PL_T
    for n, x, y, d, _ in g.HUECOS_PLACA:
        if n.startswith("I"):
            a.add(separador().translate((x, 0, y)), name="sep_" + n, color=ACERO)
            a.add(pasador(12.7, L + 2).translate((x, 330, y)), name="pas_" + n, color=ORO)
        if n.startswith("S") or n.startswith("C"):
            a.add(perno(12.7 if n[0] == "S" else 10, L + 4).translate((x, 330, y)), name="perno_" + n, color=ACERO)
        if n.startswith("A"):
            a.add(pasador(12.7, L + 2).translate((x, 330, y)), name="pas_" + n, color=ORO)
        if n == "B":
            a.add(barra_carga().translate((0, 0, -70)), name="barra_B", color=ACERO)
    for lado, t in ((-1, "i"), (1, "d")):
        x, y = g.eje(lado, 0)
        a.add(casquillo().rotate((0, 0, 0), (0, 1, 0), -g.ANG * lado).translate((x + lado * 60, 0, y - 40)),
              name="cas_" + t, color=AZUL)
    return a


cabeza_explotada().export(os.path.join(OUT, "glb", "00_cabeza_explotada.glb"), tolerance=0.05, angularTolerance=0.15)


def pata_explotada():
    a = cq.Assembly(name="pata_explotada")
    z = 0.0
    a.add(pe, name="pe1", color=GRIS)
    a.add(pe.translate((0, 0, -g.PE_TOTAL - 160)), name="pe2", color=GRIS)
    a.add(pi.translate((0, 0, -2 * g.PE_TOTAL - 320)), name="pi", color=PLATA)
    a.add(raptor.translate((0, 0, -2 * g.PE_TOTAL - 320 - g.PI_L - 120)), name="pie", color=NARANJA)
    for k, zz in enumerate((-g.PE_TOTAL - 60, -2 * g.PE_TOTAL - 220, -2 * g.PE_TOTAL - 320 - g.PI_L - 40)):
        a.add(pasador(9.5, g.EXT_OD + 2).translate((110, 0, zz)), name=f"pp{k}", color=ORO)
    return a


pata_explotada().export(os.path.join(OUT, "glb", "00_pata_explotada.glb"), tolerance=0.05, angularTolerance=0.15)
