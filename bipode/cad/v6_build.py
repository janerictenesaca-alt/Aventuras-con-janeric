"""Trípode tipo Vortex v6: piezas de corte láser, modelo 3D armado (una pieza por nodo) y DXF.

Uso:  python3 v6_build.py   ->  ../v6/
"""
import json
import math
import os

import cadquery as cq
import ezdxf
import numpy as np
from scipy.optimize import fsolve
from shapely.geometry import Point

import v4_geo as g4
import v6_geo as g

AQUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(AQUI, "..", "v6")
for d in ("dxf", "step", "stl"):
    os.makedirs(os.path.join(OUT, d), exist_ok=True)

# piezas de patas, pies y pasadores: se reutilizan de v4_build
_src = open(os.path.join(AQUI, "v4_build.py")).read()
_src = _src[:_src.index("# ------------------------------------------------------------------ guardar piezas")]
_ns = {"__name__": "v4b", "__file__": os.path.join(AQUI, "v4_build.py")}
exec(compile(_src, "v4_build_parts", "exec"), _ns)
pata_afuera, pata_adentro, pie_raptor, pasador = _ns["pata_afuera"], _ns["pata_adentro"], _ns["pie_raptor"], _ns["pasador"]

AZUL = cq.Color(0.07, 0.30, 0.72)
NARANJA = cq.Color(0.95, 0.42, 0.08)
PLATA = cq.Color(0.82, 0.84, 0.87)
GRIS = cq.Color(0.60, 0.63, 0.67)
ACERO = cq.Color(0.25, 0.27, 0.30)
ORO = cq.Color(0.86, 0.68, 0.28)
CINTA = cq.Color(0.98, 0.25, 0.20)

T = g.T


# ------------------------------------------------------------------ utilidades
def extruir(poly, t, huecos=(), cortes=()):
    wp = cq.Workplane("XY").polyline(list(poly.exterior.coords)[:-1]).close().extrude(t)
    for c in cortes:
        wp = wp.cut(cq.Workplane("XY").polyline(list(c.exterior.coords)[:-1]).close().extrude(t))
    for h in huecos:
        wp = wp.cut(cq.Workplane("XY").center(h[1], h[2]).circle(h[3] / 2).extrude(t))
    try:
        wp = wp.edges("not |Z").chamfer(0.8)
    except Exception:
        pass
    return wp


def placa_xz(poly, t, huecos=(), cortes=(), y_frente=0.0):
    """Placa dibujada en (x, z), grosor hacia −Y desde y_frente."""
    return extruir(poly, t, huecos, cortes).rotate((0, 0, 0), (1, 0, 0), 90).translate((0, y_frente, 0))


def placa_yz(poly, t, huecos=(), x0=0.0):
    """Placa dibujada en (y, z), grosor hacia +X desde x0."""
    s = extruir(poly, t, huecos).rotate((0, 0, 0), (1, 0, 0), 90).rotate((0, 0, 0), (0, 0, 1), 90)
    return s.translate((x0, 0, 0))


def placa_xy(poly, t, huecos=(), z0=0.0):
    return extruir(poly, t, huecos).translate((0, 0, z0))


def cil(d, largo, eje="y"):
    wp = {"y": "XZ", "x": "YZ", "z": "XY"}[eje]
    return cq.Workplane(wp).circle(d / 2).extrude(largo / 2, both=True)


def dxf(nombre, poly, huecos=(), cortes=(), nota=""):
    doc = ezdxf.new("R2010", setup=True)
    doc.units = ezdxf.units.MM
    doc.layers.add("CORTE", color=1)
    doc.layers.add("NOTAS", color=3)
    m = doc.modelspace()
    m.add_lwpolyline(list(poly.exterior.coords), close=True, dxfattribs={"layer": "CORTE"})
    for c in cortes:
        m.add_lwpolyline(list(c.exterior.coords), close=True, dxfattribs={"layer": "CORTE"})
    for h in huecos:
        m.add_circle((h[1], h[2]), h[3] / 2, dxfattribs={"layer": "CORTE"})
    x0, y0, *_ = poly.bounds
    m.add_text(nota, height=4, dxfattribs={"layer": "NOTAS"}).set_placement((x0, y0 - 12))
    doc.saveas(os.path.join(OUT, "dxf", nombre + ".dxf"))


# ------------------------------------------------------------------ cabeza A-frame (coordenadas de la cabeza)
def casquillo():
    """Tubo 2½" × 1/4" torneado a Ø 51,4. z = 0 arriba, boca en z = −145."""
    L = g.CAS_L
    t = cq.Workplane("XY").circle(g.CAS_OD / 2).circle(g.CAS_ID / 2).extrude(L).translate((0, 0, -L))
    for gb in (50.0, 80.0, 110.0):
        t = t.cut(cil(g.D38, 200).translate((0, 0, -L + gb)))
    for a in (0.0, 120.0, 240.0):
        r = cq.Workplane("XY").box(g.CAS_OD + 4, 11.0, 28.0).translate(((g.CAS_OD + 4) / 2, 0, -L)).rotate((0, 0, 0), (0, 0, 1), a + 90)
        t = t.cut(r)
    t = t.cut(cil(5.0, 200, "x").translate((0, 0, -L + 30.0)))          # hueco M6 del cordón del pasador
    return t


def en_casquillo(sol, lado):
    x, z = g.eje(lado, 0)
    return sol.rotate((0, 0, 0), (0, 1, 0), -g.ANG * lado).translate((x, 0, z))


P = []          # (id, nombre, solido_en_cabeza, color, grupo, material, cantidad_fabricar)

fr = g.placa_frontal()
P.append(("01", "Placa frontal (cara lisa)", placa_xz(fr, T, cortes=g.cortes_frontal(), y_frente=g.Y_FRENTE[1]),
          AZUL, "cabeza", "Al 6061-T6 · 10 mm · láser", 1))
for lado, t in ((-1, "izq."), (1, "der.")):
    P.append(("02" + ("a" if lado < 0 else "b"), f"Casquillo {t}", en_casquillo(casquillo(), lado), AZUL, "cabeza",
              "Tubo Al 6061-T6 2½\" × 1/4\" · torno", 1))
for lado in (-1, 1):
    pe_, he_ = g.NERV_EXT
    pi_, hi_ = g.NERV_INT
    xe = g.X_NERV_EXT if lado > 0 else -g.X_NERV_EXT - T
    xi = g.X_NERV_INT if lado > 0 else -g.X_NERV_INT - T
    ld = "izq." if lado < 0 else "der."
    P.append(("03" + ("a" if lado < 0 else "b"), f"Nervio exterior {ld}", placa_yz(pe_, T, he_, xe), AZUL, "cabeza",
              "Al 6061-T6 · 10 mm · láser", 1))
    P.append(("04" + ("a" if lado < 0 else "b"), f"Nervio interior {ld}", placa_yz(pi_, T, hi_, xi), AZUL, "cabeza",
              "Al 6061-T6 · 10 mm · láser", 1))
for lado in (-1, 1):
    pc, hc = g.CENTRAL
    xc = g.X_CENTRAL if lado > 0 else -g.X_CENTRAL - T
    P.append(("05" + ("a" if lado < 0 else "b"), "Placa central con oreja A " + ("izq." if lado < 0 else "der."),
              placa_yz(pc, T, hc, xc), AZUL, "cabeza", "Al 6061-T6 · 10 mm · láser", 1))
pp, hp = g.PUENTE
P.append(("06", "Puente del canal D", placa_xy(pp, T, hp, g.Z_PUENTE[0]), AZUL, "cabeza", "Al 6061-T6 · 10 mm · láser", 1))
pb, hb = g.BASE
P.append(("07", "Placa de base", placa_xy(pb, T, hb, g.Z_BASE[0]), AZUL, "cabeza", "Al 6061-T6 · 10 mm · láser", 1))

# pasadores de cabeza
for lado in (-1, 1):
    xm = lado * (g.X_NERV_INT + g.X_NERV_EXT + T) / 2
    for n, (y, z) in (("arriba", g.PIN_ARRIBA), ("abajo", g.PIN_ABAJO)):
        s = pasador(12.7, 50.8).rotate((0, 0, 0), (0, 0, 1), -90 * lado).translate((xm, y, z))
        P.append((f"P-I{'1' if n == 'arriba' else '2'}{'i' if lado < 0 else 'd'}", f"Pasador de cabeza 1/2\" · I {n}",
                  s, ORO, "pasadores", "Se compra", 1))
sB = pasador(12.7, 50.8).rotate((0, 0, 0), (0, 0, 1), 90).translate((0, *g.B_HUECO))


def polea():
    rueda = cil(38, 12, "x").cut(cil(13, 20, "x"))
    rueda = rueda.cut(cq.Workplane("YZ").circle(19.5).circle(15).extrude(3, both=True))
    lado = cq.Workplane("YZ").center(0, -8).rect(46, 66).extrude(1.2, both=True).edges("|X").fillet(18)
    lado = lado.cut(cil(13, 10, "x").translate((0, 0, 18))).cut(cil(16, 10, "x").translate((0, 0, -30)))
    p = rueda.union(lado.translate((-7.5, 0, 0))).union(lado.translate((7.5, 0, 0)))
    return p.translate((0, 0, -26))


P.append(("P-B", "Pasador de cabeza 1/2\" · B (polea)", sB, ORO, "pasadores", "Se compra", 1))
P.append(("PL", "Polea de cabeza Ø 38 mm", polea().translate((0, g.B_HUECO[0], g.B_HUECO[1] + 26)), ACERO, "pasadores",
          "Se compra", 1))


# ------------------------------------------------------------------ gin pole (coordenadas propias: tubo en −Z)
def tubo_gin():
    L = g.GP_TUBO_L
    t = cq.Workplane("XY").circle(g.CAS_OD / 2).circle(g.CAS_ID / 2).extrude(L).translate((0, 0, g.GP_T - L))
    boca = g.GP_T - L
    for gb in (50.0, 80.0):
        t = t.cut(cil(g.D38, 200).translate((0, 0, boca + gb)))
    for a in (0.0, 120.0, 240.0):
        r = cq.Workplane("XY").box(g.CAS_OD + 4, 11.0, 28.0).translate(((g.CAS_OD + 4) / 2, 0, boca)).rotate((0, 0, 0), (0, 0, 1), a + 90)
        t = t.cut(r)
    return t


ala, ovalos, hueco_tubo = g.ALA
GIN = [
    ("08", "Ala de la gin pole", extruir(ala, g.GP_T, hueco_tubo, ovalos), NARANJA, "gin", "Al 6061-T6 · 10 mm · láser", 1),
    ("09", "Tubo de la gin pole", tubo_gin(), NARANJA, "gin", "Tubo Al 6061-T6 2½\" × 1/4\" · torno", 1),
]
ph, hh = g.HORQ
for lado in (-1, 1):
    x0 = g.GP_FORK_X if lado > 0 else -g.GP_FORK_X - g.GP_T
    GIN.append(("10" + ("a" if lado < 0 else "b"), "Horquilla de la gin pole " + ("izq." if lado < 0 else "der."),
                placa_yz(ph, g.GP_T, hh, x0), NARANJA, "gin", "Al 6061-T6 · 10 mm · láser", 1))
for lado in (-1, 1):
    x = lado * (g.X_CENTRAL + g.GP_FORK_X + g.GP_T) / 2
    s = pasador(12.7, 25.4).rotate((0, 0, 0), (0, 0, 1), -90 * lado).translate((x, *g.GP_BISAGRA))
    GIN.append(("P-A" + ("i" if lado < 0 else "d"), "Pasador de cabeza 1/2\" · A (bisagra)", s, ORO, "pasadores", "Se compra", 1))

# ------------------------------------------------------------------ geometría del trípode de patas iguales
N_EXT, HUECO = 2, 1


def pie_de_pata():
    s = -g4.ESPIGA_DENTRO
    tramos = []
    for k in range(N_EXT):
        tramos.append(s)
        s += g4.PE_TUBO
    boca = -g4.ESPIGA_DENTRO + (g4.PE_ESPIGA - g4.PE_ESPIGA_DENTRO) + N_EXT * g4.PE_TUBO
    s_pi = boca - g4.PE_HUECO_BOCA - g4.PI_HUECOS[HUECO - 1]
    s_pie = s_pi + g4.PI_L - g4.ESPIGA_DENTRO
    punta = s_pie + g4.PIE_CAS_L - g4.GARRA_PUNTA
    return tramos, boca, s_pi, s_pie, punta


TRAMOS, BOCA, S_PI, S_PIE, PUNTA = pie_de_pata()


def Rx(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


HING_H = np.array([0.0, g.A_HUECO[0], g.A_HUECO[1]])
HING_G = np.array([0.0, *g.GP_BISAGRA])
BOCA_G = np.array([0.0, 0.0, g.GP_T - g.GP_TUBO_L])


def pies(tau, phi):
    fa = []
    for lado in (-1, 1):
        x, z = g.eje(lado, g.CAS_L)
        d = np.array([lado * g.SA, 0, -g.CA])
        fa.append(Rx(tau) @ (np.array([x, 0, z]) + PUNTA * d))
    fg = Rx(tau) @ (HING_H + Rx(phi) @ (BOCA_G - HING_G + PUNTA * np.array([0, 0, -1.0])))
    return fa, fg


def ecuaciones(v):
    (a1, a2), fg = pies(*v)
    lado_a = np.linalg.norm((a1 - a2)[:2])
    return [fg[2] - a1[2], np.linalg.norm((a1 - fg)[:2]) - lado_a]


TAU, PHI = fsolve(ecuaciones, [math.radians(19), math.radians(-40)])
(FA1, FA2), FG = pies(TAU, PHI)
Z0 = -FA1[2]
TAU_D, PHI_D = math.degrees(TAU), math.degrees(PHI)


def a_mundo(sol):
    return sol.rotate((0, 0, 0), (1, 0, 0), TAU_D).translate((0, 0, Z0))


def gin_a_cabeza(sol):
    return sol.translate(tuple(-HING_G)).rotate((0, 0, 0), (1, 0, 0), PHI_D).translate(tuple(HING_H))


# ------------------------------------------------------------------ patas
pe, pi, raptor = pata_afuera(), pata_adentro(), pie_raptor()


def pata(sufijo):
    """Piezas de una pata en sus coordenadas (boca del casquillo en z = 0, hacia −Z)."""
    out = []
    for k, s in enumerate(TRAMOS):
        out.append((f"11{sufijo}{k + 1}", f"Pata de afuera {k + 1}", pe.translate((0, 0, -s)), GRIS, "patas",
                    "Tubo Al 6061-T6 2\" céd. 40 + espigón", 1))
        out.append((f"P-{sufijo}{k + 1}", "Pasador de pata 3/8\"",
                    pasador(9.5, 76.2).translate((0, 0, -(s + g4.PE_HUECO_ESPIGA))), ORO, "pasadores", "Se compra", 1))
    out.append((f"12{sufijo}", "Pata de adentro", pi.translate((0, 0, -S_PI)), PLATA, "patas", "Tubo Al 6061-T6 2\" × 1/4\"", 1))
    out.append((f"P-{sufijo}i", "Pasador de pata 3/8\"", pasador(9.5, 76.2).translate((0, 0, -(BOCA - g4.PE_HUECO_BOCA))),
                ORO, "pasadores", "Se compra", 1))
    out.append((f"13{sufijo}", "Pie Raptor", raptor.translate((0, 0, -S_PIE)), NARANJA, "patas", "Acero A36 · láser + MIG", 1))
    out.append((f"P-{sufijo}p", "Pasador de pata 3/8\"", pasador(9.5, 76.2).translate((0, 0, -(S_PIE + g4.PIE_HUECO))),
                ORO, "pasadores", "Se compra", 1))
    return out


def pata_en_cabeza(sol, lado):
    x, z = g.eje(lado, g.CAS_L)
    return sol.rotate((0, 0, 0), (0, 1, 0), -g.ANG * lado).translate((x, 0, z))


# ------------------------------------------------------------------ montaje final (todo en coordenadas del mundo)
MUNDO = []
for pid, nom, s, col, grp, mat, q in P:
    MUNDO.append((pid, nom, a_mundo(s), col, grp, mat, q))
for pid, nom, s, col, grp, mat, q in GIN:
    MUNDO.append((pid, nom, a_mundo(gin_a_cabeza(s)), col, grp, mat, q))
for lado, suf in ((-1, "I"), (1, "D")):
    for pid, nom, s, col, grp, mat, q in pata(suf):
        MUNDO.append((pid, nom + (" · pata izq." if lado < 0 else " · pata der."), a_mundo(pata_en_cabeza(s, lado)), col, grp, mat, q))
for pid, nom, s, col, grp, mat, q in pata("G"):
    MUNDO.append((pid, nom + " · pata de atrás", a_mundo(gin_a_cabeza(s.translate(tuple(BOCA_G)))), col, grp, mat, q))

# maniotas (cintas) en triángulo
pies_w = [np.array([f[0], f[1], f[2] + Z0 + 35]) for f in (Rx(TAU) @ Rx(0) @ np.zeros(3),)]
F = [np.array([p[0], p[1], p[2] + Z0 + 35.0]) for p in (FA1, FA2, FG)]
for i in range(3):
    a, b = F[i], F[(i + 1) % 3]
    v = cq.Vector(*b) - cq.Vector(*a)
    s = cq.Workplane(obj=cq.Solid.makeBox(v.Length, 25, 2).translate(cq.Vector(0, -12.5, -1)))
    ang = math.degrees(math.atan2(v.y, v.x))
    s = s.rotate((0, 0, 0), (0, 0, 1), ang).translate(tuple(a))
    MUNDO.append((f"M{i + 1}", "Maniota (cinta 25 mm con hebilla)", s, CINTA, "maniotas", "Se compra", 1))

# ------------------------------------------------------------------ exportar
asm = cq.Assembly(name="tripode_vx")
meta = []
cab_c = np.array([0, 0, Z0])
for i, (pid, nom, s, col, grp, mat, q) in enumerate(MUNDO):
    node = f"n{i:02d}_{pid}"
    asm.add(s, name=node, color=col)
    bb = s.val().BoundingBox()
    c = np.array([(bb.xmin + bb.xmax) / 2, (bb.ymin + bb.ymax) / 2, (bb.zmin + bb.zmax) / 2])
    if grp in ("cabeza", "gin") or pid in ("P-B", "PL") or pid.startswith("P-I") or pid.startswith("P-A"):
        v = (c - cab_c) * 2.6 + np.array([0, 0, 350.0])
    else:
        h = np.array([c[0], c[1], 0.0])
        n = np.linalg.norm(h) or 1.0
        v = h / n * 650.0 + np.array([0, 0, 80.0 if pid.startswith("P-") else 0.0])
    meta.append(dict(node=node, id=pid, nombre=nom, grupo=grp, material=mat, orden=i, explota=[round(float(x), 1) for x in v],
                     vol=round(s.val().Volume(), 1)))
import trimesh


def glb(items, ruta, tol=0.08):
    """GLB con un nodo por pieza (Y hacia arriba), colores por pieza."""
    esc = trimesh.Scene()
    for nombre, sol, col in items:
        vs, fs = [], []
        for so in sol.solids().vals():
            v, f = so.tessellate(tol, 0.2)
            base = len(vs)
            vs += [(p.x, p.z, -p.y) for p in v]
            fs += [(a + base, b + base, c + base) for a, b, c in f]
        m = trimesh.Trimesh(vertices=np.array(vs), faces=np.array(fs), process=False)
        r, gg, b, _ = col.toTuple()
        m.visual = trimesh.visual.TextureVisuals(material=trimesh.visual.material.PBRMaterial(
            baseColorFactor=[r, gg, b, 1.0], metallicFactor=0.35, roughnessFactor=0.4))
        esc.add_geometry(m, node_name=nombre, geom_name=nombre)
    esc.export(ruta)


glb([(f"n{i:02d}_{it[0]}", it[2], it[3]) for i, it in enumerate(MUNDO)], os.path.join(OUT, "tripode_v6.glb"))
asm.export(os.path.join(OUT, "tripode_v6.step"))

# cabeza sola (A-frame + gin pole + pasadores) para las vistas de detalle
cab = cq.Assembly(name="cabeza_v6")
for pid, nom, s, col, grp, mat, q in P:
    cab.add(s, name=f"c_{pid}", color=col)
for pid, nom, s, col, grp, mat, q in GIN:
    cab.add(gin_a_cabeza(s), name=f"g_{pid}", color=col)
glb([(f"c_{it[0]}", it[2], it[3]) for it in P] + [(f"g_{it[0]}", gin_a_cabeza(it[2]), it[3]) for it in GIN],
    os.path.join(OUT, "cabeza_v6.glb"), 0.03)
cab.export(os.path.join(OUT, "cabeza_v6.step"))
cabA = cq.Assembly(name="aframe_v6")
for pid, nom, s, col, grp, mat, q in P:
    if grp == "cabeza":
        cabA.add(s, name=f"c_{pid}", color=col)
glb([(f"c_{it[0]}", it[2], it[3]) for it in P if it[4] == "cabeza"], os.path.join(OUT, "aframe_v6.glb"), 0.03)

# piezas sueltas (STEP y STL)
for pid, nom, s, col, grp, mat, q in P + GIN:
    if grp in ("cabeza", "gin"):
        nombre = f"{pid}_{nom.split(' (')[0].replace(' ', '_').replace('.', '')}"
        cq.exporters.export(s, os.path.join(OUT, "step", nombre + ".step"))
        cq.exporters.export(s, os.path.join(OUT, "stl", nombre + ".stl"), tolerance=0.05, angularTolerance=0.15)

# DXF de corte (una pieza por archivo, dibujada plana)
dxf("01_placa_frontal_Al6061-T6_10mm_x1", fr, cortes=g.cortes_frontal(),
    nota="01 Placa frontal - Al 6061-T6 10 mm - cantidad 1 - grabar texto ARIZONA VORTEX / USA / logo")
dxf("03_nervio_exterior_Al6061-T6_10mm_x2", g.NERV_EXT[0], g.NERV_EXT[1], nota="03 Nervio exterior - Al 6061-T6 10 mm - cantidad 2")
dxf("04_nervio_interior_Al6061-T6_10mm_x2", g.NERV_INT[0], g.NERV_INT[1], nota="04 Nervio interior - Al 6061-T6 10 mm - cantidad 2")
dxf("05_placa_central_oreja_A_Al6061-T6_10mm_x2", g.CENTRAL[0], g.CENTRAL[1], nota="05 Placa central con oreja A - Al 6061-T6 10 mm - cantidad 2")
dxf("06_puente_canal_D_Al6061-T6_10mm_x1", g.PUENTE[0], g.PUENTE[1], nota="06 Puente del canal D - Al 6061-T6 10 mm - cantidad 1")
dxf("07_placa_base_Al6061-T6_10mm_x1", g.BASE[0], g.BASE[1], nota="07 Placa de base - Al 6061-T6 10 mm - cantidad 1")
dxf("08_ala_gin_pole_Al6061-T6_10mm_x1", ala, hueco_tubo, ovalos, nota="08 Ala de la gin pole - Al 6061-T6 10 mm - cantidad 1")
dxf("10_horquilla_gin_pole_Al6061-T6_10mm_x2", g.HORQ[0], g.HORQ[1], nota="10 Horquilla de la gin pole - Al 6061-T6 10 mm - cantidad 2")

res = dict(tau=float(TAU_D), phi=float(PHI_D), Z0=float(Z0), altura_B=float(Z0 + (Rx(TAU) @ np.array([0, *g.B_HUECO]))[2]),
           pies=[[round(float(x), 1) for x in f] for f in (FA1, FA2, FG)],
           lado_triangulo=float(np.linalg.norm((FA1 - FA2)[:2])), piezas=meta)
json.dump(res, open(os.path.join(OUT, "armado.json"), "w"), indent=1, ensure_ascii=False)
print({k: (round(v, 1) if isinstance(v, float) else v) for k, v in res.items() if k != "piezas"}, "piezas", len(meta))
