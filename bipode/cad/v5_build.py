"""Modelo 3D del trípode tipo Vortex (v5): cabeza A-frame y gin pole maquinadas, patas, pies, pasadores.

Uso:  python3 v5_build.py   ->  ../v5/
"""
import json
import math
import os
import sys

import cadquery as cq
import ezdxf
from shapely.geometry import Point, box

import v4_geo as g4
import v5_geo as g

sys.argv = sys.argv[:1]
OUT = os.path.join(os.path.dirname(__file__), "..", "v5")
for d in ("dxf", "step", "stl", "glb"):
    os.makedirs(os.path.join(OUT, d), exist_ok=True)

AZUL = cq.Color(0.07, 0.30, 0.72)
NARANJA = cq.Color(0.95, 0.42, 0.08)
PLATA = cq.Color(0.80, 0.82, 0.85)
GRIS = cq.Color(0.56, 0.59, 0.63)
ACERO = cq.Color(0.22, 0.24, 0.27)
ORO = cq.Color(0.86, 0.68, 0.28)
CINTA = cq.Color(0.98, 0.72, 0.10)
CUERDA = cq.Color(0.95, 0.30, 0.20)


# ------------------------------------------------------------------ utilidades
def cil_y(d, largo):
    return cq.Workplane("XZ").circle(d / 2).extrude(largo / 2, both=True)


def cil_x(d, largo):
    return cq.Workplane("YZ").circle(d / 2).extrude(largo / 2, both=True)


def tubo(od, idi, largo):
    return cq.Workplane("XY").circle(od / 2).circle(idi / 2).extrude(largo).translate((0, 0, -largo))


def perfil_y(poly, fondo):
    """Extruye un polígono del plano XZ, centrado en Y."""
    return cq.Workplane("XZ").polyline(list(poly.exterior.coords)[:-1]).close().extrude(fondo / 2, both=True)


def a_eje(sol, lado, s):
    """Pone en el eje del casquillo un sólido construido hacia -Z desde z=0."""
    x, z = g.eje(lado, s)
    return sol.rotate((0, 0, 0), (0, 1, 0), -g.ANG * lado).translate((x, 0, z))


def ranuras(sol, z_boca, od):
    for a in g.RANURAS_ANG:
        r = cq.Workplane("XY").box(od, g.RANURA_A, g.RANURA_P * 2).translate((od / 2, 0, z_boca)) \
            .rotate((0, 0, 0), (0, 0, 1), a + 90)
        sol = sol.cut(r)
    return sol


def guardar(nombre, sol, color):
    cq.exporters.export(sol, os.path.join(OUT, "step", nombre + ".step"))
    cq.exporters.export(sol, os.path.join(OUT, "stl", nombre + ".stl"), tolerance=0.05, angularTolerance=0.15)
    a = cq.Assembly(name="pieza")
    a.add(sol, name=nombre, color=color)
    a.export(os.path.join(OUT, "glb", nombre + ".glb"), tolerance=0.05, angularTolerance=0.15)


# ------------------------------------------------------------------ cabeza A-frame
G_HUECOS = (50.0, 80.0, 110.0)          # 110 queda dentro del cuerpo: atraviesa todo          # huecos G a lo largo del casquillo, desde la boca


def cabeza_aframe():
    P = g.perfil_cuerpo()
    top = P.bounds[3]
    cuerpo = perfil_y(P, g.FONDO)
    # casquillos macizos
    for lado in (-1, 1):
        c = cq.Workplane("XY").circle(g.HEMBRA_OD / 2).extrude(g.CAS_L).translate((0, 0, -g.CAS_L))
        cuerpo = cuerpo.union(a_eje(c, lado, 0))
    # orejas A
    for sx in (-1, 1):
        x0, x1 = g.OREJA_X
        o = cq.Workplane("XY").box(x1 - x0, g.FONDO, g.OREJA_Z[1] - g.OREJA_Z[0]) \
            .translate((sx * (x0 + x1) / 2, 0, (g.OREJA_Z[0] + g.OREJA_Z[1]) / 2))
        o = o.edges("|X and >Z").fillet(g.FONDO / 2 - 0.5)
        cuerpo = cuerpo.union(o)
    # bahías entre las paredes
    for b in g.bahias():
        cuerpo = cuerpo.cut(perfil_y(b, g.BAHIA))
    # rebajes de 5 mm en las 2 caras
    for bb in g.bolsillos():
        for sy in (-1, 1):
            cuerpo = cuerpo.cut(perfil_y(bb, 10).translate((0, sy * (g.FONDO / 2), 0)))
    # ventanas E
    for lado in (-1, 1):
        cuerpo = cuerpo.cut(perfil_y(g.ventana(lado), 200))
    # canal D para la cuerda (entre las orejas)
    cuerpo = cuerpo.cut(cil_y(30.4, 200).translate((0, 0, top + 2)))
    cuerpo = cuerpo.cut(cq.Workplane("XY").box(30.4, 200, 60).translate((0, 0, top + 32)))
    # huecos en Y
    for n, x, z, d, _ in g.HUECOS:
        cuerpo = cuerpo.cut(cil_y(d, 200).translate((x, 0, z)))
    # hueco en X de las orejas
    cuerpo = cuerpo.cut(cil_x(g.D12, 200).translate((0, 0, g.OREJA_HUECO_Z)))
    # hueco vertical C
    x, z0, z1 = g.C_HUECO
    cuerpo = cuerpo.cut(cq.Workplane("XY").circle(g.D12 / 2).extrude(z1 - z0 + 40).translate((x, 0, z0)))
    # interior de los casquillos, huecos G y ranuras F
    for lado in (-1, 1):
        bore = cq.Workplane("XY").circle(g.HEMBRA_ID / 2).extrude(g.CAS_L - 10 + 1).translate((0, 0, -g.CAS_L - 1))
        cuerpo = cuerpo.cut(a_eje(bore, lado, 0))
        for gb in G_HUECOS:
            cuerpo = cuerpo.cut(a_eje(cil_y(g.D38, 200).translate((0, 0, -(g.CAS_L - gb))), lado, 0))
        rr = None
        for a in g.RANURAS_ANG:
            r = cq.Workplane("XY").box(g.HEMBRA_OD + 4, g.RANURA_A, g.RANURA_P * 2).translate(((g.HEMBRA_OD + 4) / 2, 0, -g.CAS_L)) \
                .rotate((0, 0, 0), (0, 0, 1), a + 90)
            rr = r if rr is None else rr.union(r)
        cuerpo = cuerpo.cut(a_eje(rr, lado, 0))
    try:
        cuerpo = cuerpo.faces(">Y or <Y").edges().chamfer(1.0)
    except Exception:
        pass
    return cuerpo


# ------------------------------------------------------------------ cabeza gin pole
def cabeza_gin():
    L = g.GP_CAS_L
    cas = cq.Workplane("XY").circle(g.HEMBRA_OD / 2).extrude(L).translate((0, 0, -L))
    ax, ay, at = g.GP_ALA
    ala = cq.Workplane("XY").rect(ax, ay).extrude(at).edges("|Z").fillet(22).faces(">Z").edges().fillet(4)
    for n, x, y in g.GP_ALA_HUECOS:
        ala = ala.cut(cq.Workplane("XY").center(x, y).circle(8).extrude(at))
    lx, ly, lz = g.GP_LENGUA
    lengua = cq.Workplane("XY").box(lx, ly, lz).translate((0, 0, at + lz / 2)).edges("|X and >Z").fillet(ly / 2 - 0.5)
    lengua = lengua.cut(cil_x(g.D12, 100).translate((0, 0, at + g.GP_HUECO_Z)))
    # ventana de la horquilla central (paso de mosquetón)
    lengua = lengua.cut(cq.Workplane("YZ").center(0, at + 14).rect(22, 14).extrude(100, both=True).edges("|X").fillet(5))
    s = cas.union(ala).union(lengua)
    s = s.cut(cq.Workplane("XY").circle(g.HEMBRA_ID / 2).extrude(L - 8).translate((0, 0, -L)))
    for gb in (50.0, 80.0):
        s = s.cut(cil_y(g.D38, 200).translate((0, 0, -L + gb)))
    s = ranuras(s, -L, g.HEMBRA_OD + 4)
    return s


# ------------------------------------------------------------------ patas, pies y pasadores (de v4)
import importlib.util

spec = importlib.util.spec_from_file_location("v4b", os.path.join(os.path.dirname(__file__), "v4_build.py"))
_src = open(os.path.join(os.path.dirname(__file__), "v4_build.py")).read()
_src = _src[:_src.index("# ------------------------------------------------------------------ guardar piezas")]
_ns = {"__name__": "v4b", "__file__": os.path.join(os.path.dirname(__file__), "v4_build.py")}
exec(compile(_src, "v4_build_parts", "exec"), _ns)
pata_afuera, pata_adentro, pie_raptor, pie_plano, pasador = (_ns["pata_afuera"], _ns["pata_adentro"],
                                                           _ns["pie_raptor"], _ns["pie_plano"], _ns["pasador"])


def polea():
    """Polea de 1,5" (38 mm) con placas laterales, colgada de un pasador de cabeza."""
    rueda = cq.Workplane("XZ").circle(19).circle(6.5).extrude(6, both=True)
    rueda = rueda.cut(cq.Workplane("XZ").circle(19.5).circle(15).extrude(3, both=True))
    lado = cq.Workplane("XZ").center(0, -8).rect(46, 70).extrude(2.5).edges("|Y").fillet(18)
    lado = lado.cut(cq.Workplane("XZ").center(0, 18).circle(6.6).extrude(3))
    lado = lado.cut(cq.Workplane("XZ").center(0, -34).circle(9).extrude(3))
    p = rueda.union(lado.translate((0, -7.5, 0))).union(lado.translate((0, 10, 0)))
    return p.translate((0, 0, -26))


pe, pi, raptor = pata_afuera(), pata_adentro(), pie_raptor()
pp_a, pp_b, pp_g = pie_plano()
cab = cabeza_aframe()
gin = cabeza_gin()

piezas = {
    "01_cabeza_aframe": (cab, AZUL),
    "02_cabeza_gin_pole": (gin, NARANJA),
    "03_pata_afuera": (pe, GRIS),
    "04_pata_adentro": (pi, PLATA),
    "05_pie_raptor": (raptor, NARANJA),
    "06_pie_plano": (pp_a.union(pp_b), NARANJA),
    "07_pasador_cabeza_1-2": (pasador(12.7, 88.9), ORO),
    "08_pasador_pata_3-8": (pasador(9.5, 64.0), ORO),
    "09_polea": (polea(), ACERO),
}
for n, (s, c) in piezas.items():
    guardar(n, s, c)

vols = {n: sum(x.Volume() for x in s.solids().vals()) for n, (s, c) in piezas.items()}


# ------------------------------------------------------------------ cabeza de trípode (A-frame + gin pole)
def pie_de_pata(n_ext, hueco):
    """Distancias a lo largo de la pata, desde la boca del casquillo (s=0 en la boca)."""
    tramos = []
    s = -g4.ESPIGA_DENTRO
    for k in range(n_ext):
        tramos.append(("pe", s))
        s += g4.PE_TUBO
    boca = -g4.ESPIGA_DENTRO + (g4.PE_ESPIGA - g4.PE_ESPIGA_DENTRO) + n_ext * g4.PE_TUBO
    p = g4.PI_HUECOS[hueco - 1]
    s_pi = boca - g4.PE_HUECO_BOCA - p
    s_pie = s_pi + g4.PI_L - g4.ESPIGA_DENTRO
    punta = s_pie + g4.PIE_CAS_L - g4.GARRA_PUNTA
    return tramos, s_pi, s_pie, punta, boca


def pata_armada(n_ext, hueco, nombre):
    """Pata completa construida hacia -Z desde la boca del casquillo (z=0)."""
    a = cq.Assembly(name=nombre)
    tramos, s_pi, s_pie, punta, boca = pie_de_pata(n_ext, hueco)
    for k, (t, s) in enumerate(tramos):
        a.add(pe.translate((0, 0, -s)), name=f"pe{k}", color=GRIS)
        if k > 0:
            a.add(pasador(9.5, g4.EXT_OD + 2).translate((0, 0, -(s + g4.PE_HUECO_ESPIGA))), name=f"pp{k}", color=ORO)
    a.add(pasador(9.5, g4.HEMBRA_OD + 2).translate((0, 0, -(-g4.ESPIGA_DENTRO + g4.PE_HUECO_ESPIGA))), name="ppc", color=ORO)
    a.add(pi.translate((0, 0, -s_pi)), name="pi", color=PLATA)
    a.add(pasador(9.5, g4.EXT_OD + 2).translate((0, 0, -(boca - g4.PE_HUECO_BOCA))), name="ppi", color=ORO)
    a.add(raptor.translate((0, 0, -s_pie)), name="pie", color=NARANJA)
    a.add(pasador(9.5, g4.HEMBRA_OD + 2).translate((0, 0, -(s_pie + g4.PIE_HUECO))), name="ppp", color=ORO)
    return a, punta


N_EXT, HUECO = 2, 1
TAU, BETA = g.TAU, g.BETA


def rotx(p, ang):
    a = math.radians(ang)
    x, y, z = p
    return (x, y * math.cos(a) - z * math.sin(a), y * math.sin(a) + z * math.cos(a))


# punto de bisagra (orejas) y puntas de las patas de la cabeza A-frame, en el marco de la cabeza
_, _, _, punta_s, _ = pie_de_pata(N_EXT, HUECO)
xA, zA = g.eje(1, g.CAS_L + punta_s)
tipA = rotx((xA, 0, zA), TAU)
bis = rotx((0, 0, g.OREJA_HUECO_Z), TAU)
Lg = g.GP_ALA[2] + g.GP_HUECO_Z + g.GP_CAS_L + punta_s
beta_real = math.degrees(math.acos((bis[2] - tipA[2]) / Lg))
Z0 = -tipA[2]                               # sube todo para que las puntas toquen el suelo
tipG = (0, bis[1] - Lg * math.sin(math.radians(beta_real)), bis[2] - Lg * math.cos(math.radians(beta_real)))

tri = cq.Assembly(name="tripode_vortex_v5")
cabeza = cq.Assembly(name="cabeza")
cabeza.add(cab, name="aframe", color=AZUL)
for n, x, z, d, _ in g.HUECOS:
    if n.startswith("I"):
        cabeza.add(pasador(12.7, g.FONDO + 2).translate((x, 0, z)), name="pas_" + n, color=ORO)
cabeza.add(pasador(12.7, g.FONDO + 2).translate((0, 0, 0)), name="pas_B", color=ORO)
cabeza.add(polea(), name="polea", color=ACERO)
for lado in (-1, 1):
    pa, _ = pata_armada(N_EXT, HUECO, f"pata{lado}")
    x, z = g.eje(lado, g.CAS_L)
    cabeza.add(pa, name=f"pata_{lado}", loc=cq.Location(cq.Vector(x, 0, z), cq.Vector(0, 1, 0), -g.ANG * lado))
tri.add(cabeza, name="cabeza_y_patas", loc=cq.Location(cq.Vector(0, 0, Z0), cq.Vector(1, 0, 0), TAU))

ginas = cq.Assembly(name="gin")
ginas.add(gin, name="gin_pole", color=NARANJA)
pg, _ = pata_armada(N_EXT, HUECO, "pata_gin")
ginas.add(pg, name="pata_gin", loc=cq.Location(cq.Vector(0, 0, -g.GP_CAS_L)))
for sx in (-1, 1):
    ginas.add(pasador(12.7, 30.0).rotate((0, 0, 0), (0, 0, 1), 90 * sx).translate(
        (sx * (g.OREJA_X[1] + 2), 0, g.GP_ALA[2] + g.GP_HUECO_Z)), name=f"bis{sx}", color=ORO)
gin_loc = cq.Location(cq.Vector(bis[0], bis[1], bis[2] + Z0), cq.Vector(1, 0, 0), -beta_real) * \
    cq.Location(cq.Vector(0, 0, -(g.GP_ALA[2] + g.GP_HUECO_Z)))
tri.add(ginas, name="gin_y_pata", loc=gin_loc)

# maniotas en triángulo entre los pies y línea de carga
pies = [(tipA[0], tipA[1], 40.0), (-tipA[0], tipA[1], 40.0), (tipG[0], tipG[1], 40.0)]


def cuerda(a, b, r=5.0):
    a, b = cq.Vector(*a), cq.Vector(*b)
    return cq.Workplane(obj=cq.Solid.makeCylinder(r, (b - a).Length, a, (b - a).normalized()))


for i in range(3):
    tri.add(cuerda(pies[i], pies[(i + 1) % 3], 7), name=f"maniota{i}", color=CINTA)
B = rotx((0, 0, -26 - 19), TAU)
tri.add(cuerda((B[0], B[1], B[2] + Z0), (B[0], B[1], 250), 5.5), name="linea_carga", color=CUERDA)

tri.export(os.path.join(OUT, "tripode_armado.glb"), tolerance=0.08, angularTolerance=0.2)
tri.export(os.path.join(OUT, "tripode_armado.step"))

# cabeza de trípode sola (A-frame + gin pole unidas), para las vistas
ct = cq.Assembly(name="cabeza_tripode")
ct.add(cabeza.children[0].obj, name="aframe", color=AZUL)
for n, x, z, d, _ in g.HUECOS:
    if n.startswith("I"):
        ct.add(pasador(12.7, g.FONDO + 2).translate((x, 0, z)), name="pas_" + n, color=ORO)
gsol = gin.rotate((0, 0, 0), (1, 0, 0), -(beta_real + TAU)).translate((0, 0, 0))
off = rotx((0, 0, g.GP_ALA[2] + g.GP_HUECO_Z), -(beta_real + TAU))
ct.add(gin.translate((0, 0, -(g.GP_ALA[2] + g.GP_HUECO_Z))), name="gin", color=NARANJA,
       loc=cq.Location(cq.Vector(0, 0, g.OREJA_HUECO_Z), cq.Vector(1, 0, 0), -(beta_real + TAU)))
for sx in (-1, 1):
    ct.add(pasador(12.7, 30.0).rotate((0, 0, 0), (0, 0, 1), 90 * sx).translate((sx * (g.OREJA_X[1] + 2), 0, g.OREJA_HUECO_Z)),
           name=f"bis{sx}", color=ORO)
ct.export(os.path.join(OUT, "glb", "00_cabeza_tripode.glb"), tolerance=0.05, angularTolerance=0.15)
ct.export(os.path.join(OUT, "step", "00_cabeza_tripode.step"))

# kit desarmado
kit = cq.Assembly(name="kit")
kit.add(cab.translate((0, 0, 400)), name="aframe", color=AZUL)
kit.add(gin.translate((330, 0, 420)), name="gin", color=NARANJA)
for i in range(3):
    kit.add(pi.rotate((0, 0, 0), (0, 1, 0), 90).translate((-500, -140 - i * 75, 0)), name=f"pi{i}", color=PLATA)
for i in range(7):
    kit.add(pe.rotate((0, 0, 0), (0, 1, 0), 90).translate((-500, 120 + i * 75, 0)), name=f"pe{i}", color=GRIS)
for i in range(3):
    kit.add(raptor.translate((520 + i * 150, -250, 300)), name=f"ra{i}", color=NARANJA)
kit.export(os.path.join(OUT, "glb", "00_kit.glb"), tolerance=0.08, angularTolerance=0.2)

res = dict(tau=TAU, beta_calc=BETA, beta_real=beta_real, Z0=Z0, altura_B=rotx((0, 0, 0), TAU)[2] + Z0,
           altura_bisagra=bis[2] + Z0, pies=pies, volumenes=vols)
json.dump(res, open(os.path.join(OUT, "armado.json"), "w"), indent=1)
print({k: (round(v, 1) if isinstance(v, float) else v) for k, v in res.items() if k != "volumenes"})
print({k: round(v) for k, v in vols.items()})
