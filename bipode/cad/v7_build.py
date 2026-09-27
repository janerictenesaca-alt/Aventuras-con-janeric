"""Trípode tipo Vortex v7: piezas de corte láser, modelo 3D armado (una pieza por nodo) y DXF.

Uso:  python3 v7_build.py   ->  ../v7/
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
import v7_geo as g

AQUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(AQUI, "..", "v7")
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
        ch = wp.edges("not |Z").chamfer(0.8)
        if len(ch.solids().vals()) == 1 and ch.val().isValid():
            wp = ch
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


# ------------------------------------------------------------------ geometría del trípode de patas iguales
N_EXT, HUECO = 2, 1
G_FILA1 = [38.0, 59.7, 81.4, 103.0, 124.8]          # huecos G de pasador 3/8" (de adelante a atrás), desde arriba
G_FILA2 = [85.0, 106.0]                             # huecos G de costado, desde arriba
GP_BAJO = 115.0                                     # largo del tubo de la gin pole bajo el ala (por su eje)


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


HING = np.array([0.0, *g.PIN_ARRIBA])               # bisagra de la gin pole = pasador de arriba (I1)


def gin_d(alfa):
    a = math.radians(alfa)
    return np.array([0.0, -math.sin(a), -math.cos(a)])


def gin_boca(alfa):
    return np.array([0.0, g.GP_TUBO_Y, g.GP_ALA_Z[0]]) + GP_BAJO * gin_d(alfa)


def pies(tau, phi, alfa):
    fa = []
    for lado in (-1, 1):
        x, z = g.eje(lado, g.CAS_L)
        d = np.array([lado * g.SA, 0, -g.CA])
        fa.append(Rx(tau) @ (np.array([x, 0, z]) + PUNTA * d))
    fg = Rx(tau) @ (HING + Rx(phi) @ (gin_boca(alfa) + PUNTA * gin_d(alfa)))
    return fa, fg


def ecuaciones(v):
    tau, phi, alfa = v
    (a1, a2), fg = pies(tau, phi, math.degrees(alfa))
    lado_a = np.linalg.norm((a1 - a2)[:2])
    return [fg[2] - a1[2], np.linalg.norm((a1 - fg)[:2]) - lado_a, tau + phi]


TAU, PHI, ALFA = fsolve(ecuaciones, [math.radians(19), math.radians(-19), math.radians(25)])
ALFA_D = round(math.degrees(ALFA), 1)
TAU, PHI = fsolve(lambda v: ecuaciones([*v, math.radians(ALFA_D)])[:2], [TAU, PHI])
(FA1, FA2), FG = pies(TAU, PHI, ALFA_D)
Z0 = -FA1[2]
TAU_D, PHI_D = math.degrees(TAU), math.degrees(PHI)
print("tau", round(TAU_D, 2), "phi", round(PHI_D, 2), "alfa", ALFA_D, "Z0", round(Z0, 1))


def a_mundo(sol):
    return sol.rotate((0, 0, 0), (1, 0, 0), TAU_D).translate((0, 0, Z0))


def gin_a_cabeza(sol):
    return sol.rotate((0, 0, 0), (1, 0, 0), PHI_D).translate(tuple(HING))


# ------------------------------------------------------------------ cabeza A-frame (coordenadas de la cabeza)
def tubo_base(L, filas):
    """Tubo 2½" × 1/4" con bore Ø 51,4, boca de arriba en z = 0, boca de abajo en z = −L."""
    t = cq.Workplane("XY").circle(g.CAS_OD / 2).circle(g.CAS_ID / 2).extrude(L).translate((0, 0, -L))
    for eje_h, lista in filas:
        for d in lista:
            t = t.cut(cil(g.D38, 200, eje_h).translate((0, 0, -d)))
    for a in (0.0, 120.0, 240.0):          # F: ranuras de alineación en la boca
        r = cq.Workplane("XY").box(g.CAS_OD + 4, 11.0, 28.0).translate(((g.CAS_OD + 4) / 2, 0, -L)).rotate((0, 0, 0), (0, 0, 1), a + 90)
        t = t.cut(r)
    return t


def casquillo():
    t = tubo_base(g.CAS_L, [("y", G_FILA1), ("x", G_FILA2)])
    return t.cut(cil(5.0, 200, "y").translate((0, 0, -g.CAS_L + 22.0)))        # hueco M5 del cordón del pasador


def en_casquillo(sol, lado):
    x, z = g.eje(lado, 0)
    return sol.rotate((0, 0, 0), (0, 1, 0), -g.ANG * lado).translate((x, 0, z))


def espejo_x(poly):
    from shapely.affinity import scale as sc
    return sc(poly, -1, 1, origin=(0, 0))


P = []          # (id, nombre, solido_en_cabeza, color, grupo, material, cantidad_fabricar)
MAT = "Al 6061-T6 · 10 mm · láser"
fr = g.placa_frontal()
P.append(("01", "Placa frontal (cara lisa)", placa_xz(fr, T, cortes=g.cortes_frontal(), y_frente=g.Y_FRENTE[1]), AZUL, "cabeza", MAT, 1))
for lado, t in ((-1, "izq."), (1, "der.")):
    P.append(("02" + ("a" if lado < 0 else "b"), f"Casquillo {t}", en_casquillo(casquillo(), lado), AZUL, "cabeza",
              "Tubo Al 6061-T6 2½\" × 1/4\" · torno", 1))
pa, ha = g.ALETA
for k, (x0, nom) in enumerate(((-g.X_ALETA_EXT - T, "de afuera izq."), (-g.X_ALETA_INT - T, "de adentro izq."),
                               (g.X_ALETA_INT, "de adentro der."), (g.X_ALETA_EXT, "de afuera der."))):
    P.append((f"03{'abcd'[k]}", f"Aleta {nom}", placa_yz(pa, T, ha, x0), AZUL, "cabeza", MAT, 1))
pt, ct = g.TRASERA
P.append(("04", "Placa trasera central", placa_xz(pt, T, cortes=ct, y_frente=g.Y_TRASERA[1]), AZUL, "cabeza", MAT, 1))
pf, hf = g.FONDO
P.append(("05", "Placa de fondo (hueco C)", placa_xy(pf, T, hf, g.Z_FONDO[0]), AZUL, "cabeza", MAT, 1))
P.append(("06a", "Escuadra lateral izq.", placa_xy(espejo_x(g.ESCUADRA), T, (), g.ESC_Z[0]), AZUL, "cabeza", MAT, 1))
P.append(("06b", "Escuadra lateral der.", placa_xy(g.ESCUADRA, T, (), g.ESC_Z[0]), AZUL, "cabeza", MAT, 1))

# pasadores de cabeza (4, como el Vortex): atraviesan aleta de afuera + ranura + aleta de adentro
for lado in (-1, 1):
    for n, (y, z) in (("arriba", g.PIN_ARRIBA), ("abajo", g.PIN_ABAJO)):
        s = pasador(12.7, 50.8).rotate((0, 0, 0), (0, 0, 1), -90 * lado).translate((lado * g.X_RANURA, y, z))
        P.append((f"P-I{'1' if n == 'arriba' else '2'}{'i' if lado < 0 else 'd'}", f"Pasador de cabeza 1/2\" · {n}",
                  s, ORO, "pasadores", "Se compra (tipo VXQR500)", 1))


def polea():
    """Polea Ø 38 colgada: agujero de las placas en el origen, eje de la rueda en X."""
    rueda = cil(38, 12, "x").cut(cil(13, 20, "x"))
    rueda = rueda.cut(cq.Workplane("YZ").circle(19.5).circle(15).extrude(3, both=True)).translate((0, 0, -34))
    lado = cq.Workplane("YZ").center(0, -24).rect(44, 72).extrude(0.6, both=True).edges("|X").fillet(16)
    lado = lado.cut(cil(13.4, 10, "x")).cut(cil(10, 10, "x").translate((0, 0, -34)))
    return rueda.union(lado.translate((-7.8, 0, 0))).union(lado.translate((7.8, 0, 0)))


P.append(("PL", "Polea Ø 38 mm (en el pasador de abajo izq.)", polea().translate((-g.X_RANURA, *g.PIN_ABAJO)), ACERO,
          "pasadores", "Se compra", 1))


# ------------------------------------------------------------------ gin pole (coordenadas propias: origen en la bisagra)
def tubo_gin():
    a = math.radians(ALFA_D)
    z_top = g.GP_ALA_Z[1] + g.GP_TUBO_ARRIBA + g.CAS_OD * math.sin(a) + 5
    s_up = (z_top - g.GP_ALA_Z[0]) / math.cos(a)
    L = s_up + GP_BAJO
    t = tubo_base(L, [("y", [L - 50.0, L - 80.0])])
    top = np.array([0.0, g.GP_TUBO_Y, g.GP_ALA_Z[0]]) - s_up * gin_d(ALFA_D)
    t = t.rotate((0, 0, 0), (1, 0, 0), -ALFA_D).translate(tuple(top))
    corte = g.GP_ALA_Z[1] + g.GP_TUBO_ARRIBA                  # la boca de arriba se corta paralela al ala, 8 mm sobre ella
    t = t.cut(cq.Workplane("XY").box(200, 400, 200).translate((0, g.GP_TUBO_Y, corte + 100)))
    return t, L


ala, ovalos, hueco_tubo = g.perfil_ala(ALFA_D)
TG, GP_L = tubo_gin()
GIN = [
    ("07", "Ala de la gin pole (escudo)", extruir(ala, T, (), ovalos + [hueco_tubo]).translate((0, 0, g.GP_ALA_Z[0])),
     NARANJA, "gin", MAT, 1),
    ("08", "Tubo de la gin pole", TG, NARANJA, "gin", "Tubo Al 6061-T6 2½\" × 1/4\" · torno", 1),
]
po, ho = g.OREJA
for lado in (-1, 1):
    x0 = g.GP_OREJA_X[0] if lado > 0 else -g.GP_OREJA_X[1]
    GIN.append(("09" + ("a" if lado < 0 else "b"), "Oreja de la gin pole " + ("izq." if lado < 0 else "der."),
                placa_yz(po, T, ho, x0), NARANJA, "gin", MAT, 1))
pj, hj = g.OJO
GIN.append(("10", "Ojo central de la gin pole", placa_xz(pj, T, hj, y_frente=g.GP_OJO_Y[1]), NARANJA, "gin", MAT, 1))
pc = g.perfil_cartela(ALFA_D)
for lado in (-1, 1):
    x0 = g.CART_X[0] if lado > 0 else -g.CART_X[1]
    GIN.append(("11" + ("a" if lado < 0 else "b"), "Cartela de la gin pole " + ("izq." if lado < 0 else "der."),
                placa_yz(pc, T, (), x0), NARANJA, "gin", MAT, 1))

# ------------------------------------------------------------------ patas
pe, pi, raptor = pata_afuera(), pata_adentro(), pie_raptor()


def pata(sufijo):
    """Piezas de una pata en sus coordenadas (boca del casquillo en z = 0, hacia −Z)."""
    out = []
    for k, s in enumerate(TRAMOS):
        out.append((f"21{sufijo}{k + 1}", f"Pata de afuera {k + 1}", pe.translate((0, 0, -s)), GRIS, "patas",
                    "Tubo Al 6061-T6 2\" céd. 40 + espigón", 1))
        out.append((f"PP-{sufijo}{k + 1}", "Pasador de pata 3/8\"",
                    pasador(9.5, 76.2).translate((0, 0, -(s + g4.PE_HUECO_ESPIGA))), ORO, "pasadores", "Se compra", 1))
    out.append((f"22{sufijo}", "Pata de adentro", pi.translate((0, 0, -S_PI)), PLATA, "patas", "Tubo Al 6061-T6 2\" × 1/4\"", 1))
    out.append((f"PP-{sufijo}i", "Pasador de pata 3/8\"", pasador(9.5, 76.2).translate((0, 0, -(BOCA - g4.PE_HUECO_BOCA))),
                ORO, "pasadores", "Se compra", 1))
    out.append((f"23{sufijo}", "Pie Raptor", raptor.translate((0, 0, -S_PIE)), NARANJA, "patas", "Acero A36 · láser + MIG", 1))
    out.append((f"PP-{sufijo}p", "Pasador de pata 3/8\"", pasador(9.5, 76.2).translate((0, 0, -(S_PIE + g4.PIE_HUECO))),
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
    MUNDO.append((pid, nom + " · pata de atrás", a_mundo(gin_a_cabeza(s.rotate((0, 0, 0), (1, 0, 0), -ALFA_D).translate(tuple(gin_boca(ALFA_D))))), col, grp, mat, q))

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
    if grp in ("cabeza", "gin") or pid in ("P-B", "PL") or pid.startswith("P-I"):
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


glb([(f"n{i:02d}_{it[0]}", it[2], it[3]) for i, it in enumerate(MUNDO)], os.path.join(OUT, "tripode_v7.glb"))
asm.export(os.path.join(OUT, "tripode_v7.step"))

# cabeza sola (A-frame + gin pole + pasadores) para las vistas de detalle
cab = cq.Assembly(name="cabeza_v7")
for pid, nom, s, col, grp, mat, q in P:
    cab.add(s, name=f"c_{pid}", color=col)
for pid, nom, s, col, grp, mat, q in GIN:
    cab.add(gin_a_cabeza(s), name=f"g_{pid}", color=col)
glb([(f"c_{it[0]}", it[2], it[3]) for it in P] + [(f"g_{it[0]}", gin_a_cabeza(it[2]), it[3]) for it in GIN],
    os.path.join(OUT, "cabeza_v7.glb"), 0.03)
cab.export(os.path.join(OUT, "cabeza_v7.step"))
cabA = cq.Assembly(name="aframe_v7")
for pid, nom, s, col, grp, mat, q in P:
    if grp == "cabeza":
        cabA.add(s, name=f"c_{pid}", color=col)
glb([(f"c_{it[0]}", it[2], it[3]) for it in P if it[4] == "cabeza"], os.path.join(OUT, "aframe_v7.glb"), 0.03)

# piezas sueltas (STEP y STL)
for pid, nom, s, col, grp, mat, q in P + GIN:
    if grp in ("cabeza", "gin"):
        nombre = f"{pid}_{nom.split(' (')[0].replace(' ', '_').replace('.', '')}"
        cq.exporters.export(s, os.path.join(OUT, "step", nombre + ".step"))
        cq.exporters.export(s, os.path.join(OUT, "stl", nombre + ".stl"), tolerance=0.05, angularTolerance=0.15)

# DXF de corte (una pieza por archivo, dibujada plana, en mm)
DXF = [
    ("01_placa_frontal", "01 Placa frontal (cara lisa)", fr, [], g.cortes_frontal(), 1),
    ("03_aleta", "03 Aleta (oreja) de la cabeza", g.ALETA[0], g.ALETA[1], [], 4),
    ("04_placa_trasera", "04 Placa trasera central", g.TRASERA[0], [], g.TRASERA[1], 1),
    ("05_placa_fondo", "05 Placa de fondo (hueco C)", g.FONDO[0], g.FONDO[1], [], 1),
    ("06_escuadra_lateral", "06 Escuadra lateral (1 normal + 1 dada vuelta)", g.ESCUADRA, [], [], 2),
    ("07_ala_gin_pole", "07 Ala de la gin pole", ala, [], ovalos + [hueco_tubo], 1),
    ("09_oreja_gin_pole", "09 Oreja de la gin pole", g.OREJA[0], g.OREJA[1], [], 2),
    ("10_ojo_gin_pole", "10 Ojo central de la gin pole", g.OJO[0], g.OJO[1], [], 1),
    ("11_cartela_gin_pole", "11 Cartela de la gin pole", pc, [], [], 2),
]
for arch, tit, poly, hs, cs, q in DXF:
    dxf(f"{arch}_Al6061-T6_10mm_x{q}", poly, hs, cs, nota=f"{tit} - Al 6061-T6 10 mm - cantidad {q} - medidas en mm")

res = dict(tau=float(TAU_D), phi=float(PHI_D), Z0=float(Z0), altura_I2=float(Z0 + (Rx(TAU) @ np.array([0, *g.PIN_ABAJO]))[2]), alfa=ALFA_D, gin_tubo_L=float(GP_L),
           pies=[[round(float(x), 1) for x in f] for f in (FA1, FA2, FG)],
           lado_triangulo=float(np.linalg.norm((FA1 - FA2)[:2])), piezas=meta)
json.dump(res, open(os.path.join(OUT, "armado.json"), "w"), indent=1, ensure_ascii=False)
print({k: (round(v, 1) if isinstance(v, float) else v) for k, v in res.items() if k != "piezas"}, "piezas", len(meta))
