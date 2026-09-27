"""Trípode tipo Vortex v8: piezas de corte láser, modelo 3D armado (una pieza por nodo) y DXF.

Uso:  python3 v8_build.py   ->  ../v8/
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
import v8_geo as g

AQUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(AQUI, "..", "v8")
for d in ("dxf", "step", "stl", "iges"):
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


# ------------------------------------------------------------------ piezas redondas (tubos) · regla de huecos única
garra = _ns["garra"]
H, PASO, VER = g.H_BOCA, g.PASO, g.VERNIER
ANG_F = (90.0, 210.0, 330.0)        # ranuras F de alineación; el tope va a 90° (+Y, del lado del hueco del pasador)


def tubo(od, idi, largo, z0=0.0):
    """Tubo sobre el eje Z, de z0 hacia abajo (−Z)."""
    return cq.Workplane("XY").circle(od / 2).circle(idi / 2).extrude(largo).translate((0, 0, z0 - largo))


def huecos(sol, zs, eje="y", d=None):
    for z in zs:
        sol = sol.cut(cil(d or g.D38, 300, eje).translate((0, 0, z)))
    return sol


def ranuras(sol, z_boca, od, hacia=-1, angs=ANG_F, ancho=10.5, fondo=11.0):
    """Ranuras F en una boca en z_boca; 'hacia' = −1 si la boca mira hacia abajo."""
    for a in angs:
        r = cq.Workplane("XY").box(od, ancho, 2 * fondo).translate((od / 2, 0, z_boca)).rotate((0, 0, 0), (0, 0, 1), a)
        sol = sol.cut(r)
    return sol


def tope(z):
    """Tope de alineación: perno de acero Ø 9,5 que sale 6 mm, radial hacia +Y (90°)."""
    return cq.Workplane("XZ").circle(4.75).extrude(-12).translate((0, 20.0, z))


def pata_afuera8():
    """10 + 11 + 12. z = 0 en el escalón; macho (espiga Ø 50,8) hacia +Z, hembra (boca) en z = −902."""
    cuerpo = tubo(g.D_AFUERA, 52.5, g.PA_CUERPO)
    cuerpo = huecos(cuerpo, [-g.PA_CUERPO + H])
    cuerpo = ranuras(cuerpo, -g.PA_CUERPO, g.D_AFUERA, angs=(90.0,))
    espiga = tubo(g.D_PATA, 38.1, g.PA_ESPIGA, g.PA_MACHO)
    espiga = huecos(espiga, [g.PA_MACHO - g.PA_HUECO_MACHO])
    t = cuerpo.union(espiga).union(tope(5.5))
    return huecos(t, [-z for z in g.PA_REMACHES], "x")


def pata_adentro8():
    t = tubo(g.D_PATA, 38.1, g.PI_L)
    return huecos(t, [-h for h in g.PI_HUECOS])


def pie_flecha():
    cas = tubo(g.D_AFUERA, g.D_BOCA, g.PIE_L)
    cas = huecos(cas, [-H])
    cas = ranuras(cas, 0.0, g.D_AFUERA, hacia=1)
    cas = cas.cut(cq.Workplane("XY").box(g.D_AFUERA + 10, g4.GARRA_T + 0.4, 60).translate((0, 0, -g.PIE_L + 30)))
    pl = garra().translate((0, 0, -g4.GARRA_T / 2)).rotate((0, 0, 0), (1, 0, 0), 90).translate((0, 0, -g.PIE_L))
    return cas.union(pl)


def carrete_naranja():
    """15. z = 0 en la cara de arriba del disco; el tubo baja 100."""
    p, hs, cs = g.CAR_N
    d = extruir(p, T, hs, cs).translate((0, 0, -T))
    t = tubo(g.D_AFUERA, g.D_BOCA, g.CAR_N_ALTO, -T)
    return huecos(d.union(t), [-z for z in g.CAR_HUECOS])


def carrete_azul():
    """16. z = 0 en la cara de abajo del disco; el tubo sube 107."""
    p, hs, cs = g.CAR_A
    d = extruir(p, T, hs, cs)
    t = tubo(g.CAR_A_OD, g.D_AZUL, g.CAR_A_ALTO, T + g.CAR_A_ALTO)
    t = huecos(huecos(t, g.CAR_HUECOS), g.CAR_HUECOS, "x")
    return d.union(t)


# ------------------------------------------------------------------ cadenas de una pata (s = distancia desde la boca del casquillo)
PA, PI_, PIE = pata_afuera8(), pata_adentro8(), pie_flecha()
PIN = pasador(9.5, 76.2)
N_EXT, J_HUECO = 2, 0


def cadena_larga(n=N_EXT, j=J_HUECO):
    """Configuración A (patas largas): macho arriba en el casquillo, pata de adentro abajo, pie."""
    items, pins = [], []
    for k in range(n):
        items.append(("10", f"Pata de afuera {k + 1}", 902.0 * k, False))
        pins.append(902.0 * k - H)
    s_top = 902.0 * n - 2 * H - PASO * j
    items.append(("13", "Pata de adentro", s_top, False))
    pins.append(902.0 * n - H)
    s_pie = s_top + g.PI_L - 2 * H
    items.append(("14", "Pie de flecha", s_pie, False))
    pins.append(s_pie + H)
    return items, pins, s_pie + g.PIE_L - g4.GARRA_PUNTA


def cadena_arriba(n=N_EXT):
    """Configuración B (tubo arriba): la pata de adentro atraviesa la cabeza y sale 114 mm; abajo las de afuera dadas vuelta."""
    s_top = -H - (H + PASO)
    items = [("13", "Pata de adentro (sale arriba)", s_top, False)]
    pins = [-H]
    boca = s_top + g.PI_L - 2 * H
    for k in range(n):
        items.append(("10", f"Pata de afuera {k + 1} (dada vuelta)", boca + 902.0, True))
        pins.append(boca + H)
        boca += 902.0
    items.append(("14", "Pie de flecha", boca, False))
    pins.append(boca + H)
    return items, pins, boca + g.PIE_L - g4.GARRA_PUNTA, s_top


ITEMS_A, PINS_A, PUNTA_A = cadena_larga()
ITEMS_B, PINS_B, PUNTA_B, TOP_B = cadena_arriba()


def pieza_cadena(pid, s, rev):
    base = {"10": PA, "13": PI_, "14": PIE}[pid]
    if rev:
        base = base.rotate((0, 0, 0), (1, 0, 0), 180)
    return base.translate((0, 0, -s))


def Rx(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


HING = np.array([0.0, *g.PIN_ARRIBA])               # bisagra de la gin pole = pasador de arriba (I1)
GP_BAJO = 115.0                                     # largo del tubo de la gin pole bajo el ala (por su eje)


def gin_d(alfa):
    a = math.radians(alfa)
    return np.array([0.0, -math.sin(a), -math.cos(a)])


def gin_boca(alfa):
    return np.array([0.0, g.GP_TUBO_Y, g.GP_ALA_Z[0]]) + GP_BAJO * gin_d(alfa)


def pies(tau, phi, alfa, punta):
    fa = []
    for lado in (-1, 1):
        x, z = g.eje(lado, g.CAS_L)
        d = np.array([lado * g.SA, 0, -g.CA])
        fa.append(Rx(tau) @ (np.array([x, 0, z]) + punta * d))
    fg = Rx(tau) @ (HING + Rx(phi) @ (gin_boca(alfa) + punta * gin_d(alfa)))
    return fa, fg


def ecuaciones(v, punta, alfa=None):
    tau, phi = v[0], v[1]
    al = math.degrees(v[2]) if alfa is None else alfa
    (a1, a2), fg = pies(tau, phi, al, punta)
    e = [fg[2] - a1[2], np.linalg.norm((a1 - fg)[:2]) - np.linalg.norm((a1 - a2)[:2])]
    return e + ([tau + phi] if alfa is None else [])


_t, _p, _a = fsolve(lambda v: ecuaciones(v, PUNTA_A), [math.radians(17), math.radians(-17), math.radians(31)])
ALFA_D = round(math.degrees(_a), 1)


def resolver(punta):
    tau, phi = fsolve(lambda v: ecuaciones(v, punta, ALFA_D), [_t, _p])
    (a1, a2), fg = pies(tau, phi, ALFA_D, punta)
    return tau, phi, a1, a2, fg, -a1[2]


SOL = {"A": resolver(PUNTA_A), "B": resolver(PUNTA_B)}
print("alfa", ALFA_D, {k: (round(math.degrees(v[0]), 2), round(math.degrees(v[1]), 2), round(v[5], 1)) for k, v in SOL.items()})


# ------------------------------------------------------------------ cabeza A-frame (coordenadas de la cabeza)
CAS_Y = [g.CAS_L - z for z in (H - VER, H, H + VER, H + 2 * VER)]     # desde arriba; 63,5 = hueco principal
CAS_X = [g.CAS_L - z for z in (H, H + VER)]


def tubo_base(L, filas):
    """Tubo 2½" × 1/4" con bore Ø 51,4, boca de arriba en z = 0, boca de abajo en z = −L (abierto en las 2 puntas)."""
    t = cq.Workplane("XY").circle(g.CAS_OD / 2).circle(g.CAS_ID / 2).extrude(L).translate((0, 0, -L))
    for eje_h, lista in filas:
        for d in lista:
            t = t.cut(cil(g.D38, 200, eje_h).translate((0, 0, -d)))
    return ranuras(t, -L, g.CAS_OD + 4)


def casquillo():
    t = tubo_base(g.CAS_L, [("y", CAS_Y), ("x", CAS_X)])
    return t.cut(cil(5.0, 200, "x").translate((0, 0, -g.CAS_L + 22.0)))        # hueco M5 del cordón del pasador


def en_casquillo(sol, lado):
    x, z = g.eje(lado, 0)
    return sol.rotate((0, 0, 0), (0, 1, 0), -g.ANG * lado).translate((x, 0, z))


def en_boca(sol, lado):
    x, z = g.eje(lado, g.CAS_L)
    return sol.rotate((0, 0, 0), (0, 1, 0), -g.ANG * lado).translate((x, 0, z))


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
pf, hf = g.PUENTE
P.append(("04", "Puente central (hueco C)", placa_xy(pf, T, hf, g.Z_FONDO[0]), AZUL, "cabeza", MAT, 1))

for lado in (-1, 1):
    for n, (y, z) in (("arriba", g.PIN_ARRIBA), ("abajo", g.PIN_ABAJO)):
        s_ = pasador(12.7, 50.8).rotate((0, 0, 0), (0, 0, 1), -90 * lado).translate((lado * g.X_RANURA, y, z))
        P.append((f"P-I{'1' if n == 'arriba' else '2'}{'i' if lado < 0 else 'd'}", f"Pasador de cabeza 1/2\" · {n}",
                  s_, ORO, "pasadores", "Se compra (tipo VXQR500)", 1))


def polea():
    """Polea Ø 38 colgada: agujero de las placas en el origen, eje de la rueda en X."""
    rueda = cil(38, 12, "x").cut(cil(13, 20, "x"))
    rueda = rueda.cut(cq.Workplane("YZ").circle(19.5).circle(15).extrude(3, both=True)).translate((0, 0, -34))
    lado = cq.Workplane("YZ").center(0, -24).rect(44, 72).extrude(0.6, both=True).edges("|X").fillet(16)
    lado = lado.cut(cil(13.4, 10, "x")).cut(cil(10, 10, "x").translate((0, 0, -34)))
    return rueda.union(lado.translate((-7.8, 0, 0))).union(lado.translate((7.8, 0, 0)))


for lado, t in ((-1, "izq."), (1, "der.")):
    P.append(("PL" + ("i" if lado < 0 else "d"), f"Polea Ø 38 mm (pasador de abajo {t})",
              polea().translate((lado * g.X_RANURA, *g.PIN_ABAJO)), ACERO, "pasadores", "Se compra", 1))


# ------------------------------------------------------------------ gin pole (coordenadas propias: origen en la bisagra)
def tubo_gin():
    a = math.radians(ALFA_D)
    z_top = g.GP_ALA_Z[1] + g.GP_TUBO_ARRIBA + g.CAS_OD * math.sin(a) + 5
    s_up = (z_top - g.GP_ALA_Z[0]) / math.cos(a)
    L = s_up + GP_BAJO
    t = tubo_base(L, [("y", [L - H, L - H - VER])])
    top = np.array([0.0, g.GP_TUBO_Y, g.GP_ALA_Z[0]]) - s_up * gin_d(ALFA_D)
    t = t.rotate((0, 0, 0), (1, 0, 0), -ALFA_D).translate(tuple(top))
    corte = g.GP_ALA_Z[1] + g.GP_TUBO_ARRIBA
    t = t.cut(cq.Workplane("XY").box(200, 400, 200).translate((0, g.GP_TUBO_Y, corte + 100)))
    return t, L


ala, ovalos, hueco_tubo = g.perfil_ala(ALFA_D)
TG, GP_L = tubo_gin()
GIN = [
    ("05", "Ala de la gin pole (escudo)", extruir(ala, T, (), ovalos + [hueco_tubo]).translate((0, 0, g.GP_ALA_Z[0])),
     NARANJA, "gin", MAT, 1),
    ("06", "Tubo de la gin pole", TG, NARANJA, "gin", "Tubo Al 6061-T6 2½\" × 1/4\" · torno", 1),
]
po, ho = g.OREJA
for lado in (-1, 1):
    x0 = g.GP_OREJA_X[0] if lado > 0 else -g.GP_OREJA_X[1]
    GIN.append(("07" + ("a" if lado < 0 else "b"), "Oreja de la gin pole " + ("izq." if lado < 0 else "der."),
                placa_yz(po, T, ho, x0), NARANJA, "gin", MAT, 1))
pj, hj = g.OJO
GIN.append(("08", "Ojo central de la gin pole", placa_xz(pj, T, hj, y_frente=g.GP_OJO_Y[1]), NARANJA, "gin", MAT, 1))
pc = g.perfil_cartela(ALFA_D)
for lado in (-1, 1):
    x0 = g.CART_X[0] if lado > 0 else -g.CART_X[1]
    GIN.append(("09" + ("a" if lado < 0 else "b"), "Cartela de la gin pole " + ("izq." if lado < 0 else "der."),
                placa_yz(pc, T, (), x0), NARANJA, "gin", MAT, 1))

# ------------------------------------------------------------------ montaje
NOM_PATA = {"10": ("Pata de afuera (cuerpo + espiga + tope)", GRIS, "Tubo 2\" céd. 40 + espiga 2\" × 1/4\""),
            "13": ("Pata de adentro", PLATA, "Tubo Al 6061-T6 2\" × 1/4\""),
            "14": ("Pie de flecha", NARANJA, "Casquillo Al + garra acero A36 12 mm")}


def pata(suf, items, pins):
    out = []
    cnt = {}
    for pid, nom, s, rev in items:
        cnt[pid] = cnt.get(pid, 0) + 1
        out.append((f"{pid}{suf}{cnt[pid]}", nom, pieza_cadena(pid, s, rev), NOM_PATA[pid][1], "patas", NOM_PATA[pid][2], 1))
    for i, sp in enumerate(pins):
        out.append((f"PP-{suf}{i + 1}", "Pasador de pata 3/8\"", PIN.translate((0, 0, -sp)), ORO, "pasadores", "Se compra (tipo VXQR375)", 1))
    return out


def armar(cfg):
    tau, phi, a1, a2, fg, z0 = SOL[cfg]
    TD, PD = math.degrees(tau), math.degrees(phi)

    def mundo(sol):
        return sol.rotate((0, 0, 0), (1, 0, 0), TD).translate((0, 0, z0))

    def gin(sol):
        return sol.rotate((0, 0, 0), (1, 0, 0), PD).translate(tuple(HING))

    items, pins = (ITEMS_A, PINS_A) if cfg == "A" else (ITEMS_B, PINS_B)
    M = []
    for pid, nom, s_, col, grp, mat, q in P:
        M.append((pid, nom, mundo(s_), col, grp, mat, q))
    for pid, nom, s_, col, grp, mat, q in GIN:
        M.append((pid, nom, mundo(gin(s_)), col, grp, mat, q))
    for lado, suf, txt in ((-1, "I", " · pata izq."), (1, "D", " · pata der.")):
        for pid, nom, s_, col, grp, mat, q in pata(suf, items, pins):
            M.append((pid, nom + txt, mundo(en_boca(s_, lado)), col, grp, mat, q))
    for pid, nom, s_, col, grp, mat, q in pata("G", items, pins):
        s2 = s_.rotate((0, 0, 0), (1, 0, 0), -ALFA_D).translate(tuple(gin_boca(ALFA_D)))
        M.append((pid, nom + " · pata de atrás", mundo(gin(s2)), col, grp, mat, q))
    if cfg == "B":                   # carrete sobre el tubo que sale del casquillo izquierdo
        z_pin = -(TOP_B + H)                                  # hueco 1 de la pata de adentro (50,2 sobre el casquillo)
        zb = z_pin - (H - VER)                                # cara de abajo del disco azul (hueco de 35,6)
        azul = carrete_azul().translate((0, 0, zb))
        nar = carrete_naranja().translate((0, 0, zb + g.CAR_A_ALTO + 2 * T))
        pin = PIN.translate((0, 0, z_pin))
        for pid, nom, s_, col in (("16", "Carrete azul (de afuera)", azul, AZUL), ("15", "Carrete naranja (de adentro)", nar, NARANJA),
                                  ("PP-C", "Pasador del carrete 3/8\"", pin, ORO)):
            M.append((pid, nom, mundo(en_boca(s_, -1)), col, "carrete" if pid != "PP-C" else "pasadores", "", 1))
    F = [np.array([p[0], p[1], p[2] + z0 + 35.0]) for p in (a1, a2, fg)]
    for i in range(3):
        a, b = F[i], F[(i + 1) % 3]
        v = cq.Vector(*b) - cq.Vector(*a)
        s_ = cq.Workplane(obj=cq.Solid.makeBox(v.Length, 25, 2).translate(cq.Vector(0, -12.5, -1)))
        s_ = s_.rotate((0, 0, 0), (0, 0, 1), math.degrees(math.atan2(v.y, v.x))).translate(tuple(a))
        M.append((f"M{i + 1}", "Maniota (cinta 25 mm con hebilla)", s_, CINTA, "maniotas", "Se compra", 1))
    return M, z0


MUNDO, Z0 = armar("A")
MUNDO_B, Z0_B = armar("B")

# ------------------------------------------------------------------ accesorios (carrete y AHP), fuera del trípode
def ahp():
    p, hs, cs = g.AHP
    s_ = extruir(p, g.AHP_T, hs, cs).translate((0, 0, -g.AHP_T / 2))
    return s_.cut(cil(g.D38, 200, "x").translate((0, g.AHP_PIN_Y, 0)))


def adaptador():
    """18. Adaptador de acero para el enganche de 2": caja con ranura para la lengüeta + espiga cuadrada 2"."""
    caja = cq.Workplane("XY").box(90, 80, 44).translate((0, 340, 0))
    caja = caja.cut(cq.Workplane("XY").box(55.0, 90, g.AHP_T + 0.8).translate((0, 335, 0)))
    esp = cq.Workplane("XY").box(50.8, 230, 50.8).translate((0, 380 + 115, 0))
    esp = esp.cut(cq.Workplane("XY").box(38.1, 240, 38.1).translate((0, 380 + 115, 0)))
    s_ = caja.union(esp)
    s_ = s_.cut(cil(16.5, 100, "z").translate((0, 350, 0)))
    return s_.cut(cil(16.5, 100, "x").translate((0, 380 + 230 - 60, 0)))


ACC = [
    ("15", "Carrete naranja (de adentro)", carrete_naranja().translate((-420, 0, 250)), NARANJA, "carrete", "Al 6061-T6", 1),
    ("16", "Carrete azul (de afuera)", carrete_azul().translate((-420, 0, 0)), AZUL, "carrete", "Al 6061-T6", 1),
    ("17", "AHP (poste de enganche)", ahp(), NARANJA, "ahp", "Al 6061-T6 1\" · chorro de agua", 1),
    ("18", "Adaptador de enganche 2\"", adaptador(), ACERO, "ahp", "Acero A36 · MIG", 1),
    ("13x", "Pata de adentro en el AHP", PI_.translate((0, 0, g.H_BOCA)).rotate((0, 0, 0), (1, 0, 0), -120)
     .translate((0, g.AHP_PIN_Y, 0)), PLATA, "ahp", "", 1),
    ("PP-A", "Pasador del AHP 3/8\"", pasador(9.5, 76.2).rotate((0, 0, 0), (0, 0, 1), 90).translate((0, g.AHP_PIN_Y, 0)), ORO, "ahp", "", 1),
]

# ------------------------------------------------------------------ exportar
import trimesh


def glb(items, ruta, tol=0.08):
    """GLB con un nodo por pieza (Y hacia arriba), colores por pieza."""
    esc = trimesh.Scene()
    for nombre, sol, col in items:
        vs, fs = [], []
        for so in sol.solids().vals():
            v, f_ = so.tessellate(tol, 0.2)
            base = len(vs)
            vs += [(p.x, p.z, -p.y) for p in v]
            fs += [(a + base, b + base, c + base) for a, b, c in f_]
        m = trimesh.Trimesh(vertices=np.array(vs), faces=np.array(fs), process=False)
        r, gg, b, _ = col.toTuple()
        m.visual = trimesh.visual.TextureVisuals(material=trimesh.visual.material.PBRMaterial(
            baseColorFactor=[r, gg, b, 1.0], metallicFactor=0.35, roughnessFactor=0.4))
        esc.add_geometry(m, node_name=nombre, geom_name=nombre)
    esc.export(ruta)


def meta_de(M, z0):
    meta = []
    cab_c = np.array([0, 0, z0])
    for i, (pid, nom, s_, col, grp, mat, q) in enumerate(M):
        bb = s_.val().BoundingBox()
        c = np.array([(bb.xmin + bb.xmax) / 2, (bb.ymin + bb.ymax) / 2, (bb.zmin + bb.zmax) / 2])
        if grp in ("cabeza", "gin", "carrete") or pid.startswith("PL") or pid.startswith("P-I") or pid == "PP-C":
            v = (c - cab_c) * 2.6 + np.array([0, 0, 350.0])
        else:
            h_ = np.array([c[0], c[1], 0.0])
            n = np.linalg.norm(h_) or 1.0
            v = h_ / n * 650.0 + np.array([0, 0, 80.0 if pid.startswith("PP-") else 0.0])
        meta.append(dict(node=f"n{i:02d}_{pid}", id=pid, nombre=nom, grupo=grp, material=mat, orden=i,
                         explota=[round(float(x), 1) for x in v], vol=round(s_.val().Volume(), 1)))
    return meta


meta = meta_de(MUNDO, Z0)
glb([(f"n{i:02d}_{it[0]}", it[2], it[3]) for i, it in enumerate(MUNDO)], os.path.join(OUT, "tripode_v8.glb"))
glb([(f"n{i:02d}_{it[0]}", it[2], it[3]) for i, it in enumerate(MUNDO_B)], os.path.join(OUT, "tripode_v8_tubo_arriba.glb"))
asm = cq.Assembly(name="tripode_v8")
for i, it in enumerate(MUNDO):
    asm.add(it[2], name=f"n{i:02d}_{it[0]}", color=it[3])
asm.export(os.path.join(OUT, "tripode_v8.step"))


def gin_cab(sol):
    return sol.rotate((0, 0, 0), (1, 0, 0), math.degrees(SOL["A"][1])).translate(tuple(HING))


cab = cq.Assembly(name="cabeza_v8")
for pid, nom, s_, col, grp, mat, q in P:
    cab.add(s_, name=f"c_{pid}", color=col)
for pid, nom, s_, col, grp, mat, q in GIN:
    cab.add(gin_cab(s_), name=f"g_{pid}", color=col)
glb([(f"c_{it[0]}", it[2], it[3]) for it in P] + [(f"g_{it[0]}", gin_cab(it[2]), it[3]) for it in GIN],
    os.path.join(OUT, "cabeza_v8.glb"), 0.03)
cab.export(os.path.join(OUT, "cabeza_v8.step"))
glb([(f"c_{it[0]}", it[2], it[3]) for it in P if it[4] == "cabeza"], os.path.join(OUT, "aframe_v8.glb"), 0.03)
glb([(f"a_{it[0]}", it[2], it[3]) for it in ACC], os.path.join(OUT, "accesorios_v8.glb"), 0.05)
acc = cq.Assembly(name="accesorios_v8")
for it in ACC:
    acc.add(it[2], name=f"a_{it[0]}", color=it[3])
acc.export(os.path.join(OUT, "accesorios_v8.step"))

# piezas sueltas para fabricar (STEP, IGES y STL)
from OCP.IGESControl import IGESControl_Writer
SUELTAS = [(pid, nom, s_) for pid, nom, s_, col, grp, mat, q in P + GIN if grp in ("cabeza", "gin")] + [
    ("10", "Pata de afuera", PA), ("13", "Pata de adentro", PI_), ("14", "Pie de flecha", PIE),
    ("15", "Carrete naranja", carrete_naranja()), ("16", "Carrete azul", carrete_azul()),
    ("17", "AHP", ahp()), ("18", "Adaptador de enganche", adaptador())]
for pid, nom, s_ in SUELTAS:
    nombre = f"{pid}_{nom.split(' (')[0].replace(' ', '_').replace('.', '')}"
    cq.exporters.export(s_, os.path.join(OUT, "step", nombre + ".step"))
    cq.exporters.export(s_, os.path.join(OUT, "stl", nombre + ".stl"), tolerance=0.05, angularTolerance=0.15)
    w = IGESControl_Writer("MM", 1)
    for so in s_.solids().vals():
        w.AddShape(so.wrapped)
    w.ComputeModel()
    w.Write(os.path.join(OUT, "iges", nombre + ".igs"))

# DXF de corte (una pieza por archivo, plana, en mm)
DXF = [
    ("01_placa_frontal", "01 Placa frontal (cara lisa)", fr, [], g.cortes_frontal(), 1, "Al6061-T6_10mm"),
    ("03_aleta", "03 Aleta de la cabeza", g.ALETA[0], g.ALETA[1], [], 4, "Al6061-T6_10mm"),
    ("04_puente_central", "04 Puente central (hueco C)", g.PUENTE[0], g.PUENTE[1], [], 1, "Al6061-T6_10mm"),
    ("05_ala_gin_pole", "05 Ala de la gin pole", ala, [], ovalos + [hueco_tubo], 1, "Al6061-T6_10mm"),
    ("07_oreja_gin_pole", "07 Oreja de la gin pole", g.OREJA[0], g.OREJA[1], [], 2, "Al6061-T6_10mm"),
    ("08_ojo_gin_pole", "08 Ojo central de la gin pole", g.OJO[0], g.OJO[1], [], 1, "Al6061-T6_10mm"),
    ("09_cartela_gin_pole", "09 Cartela de la gin pole", pc, [], [], 2, "Al6061-T6_10mm"),
    ("14_garra_pie", "14 Garra del pie de flecha", g4.contorno_garra(), [h[:4] for h in g4.HUECOS_GARRA], [], 3, "acero_A36_12mm"),
    ("15_disco_carrete_naranja", "15 Disco del carrete naranja", g.CAR_N[0], g.CAR_N[1], g.CAR_N[2], 1, "Al6061-T6_10mm"),
    ("16_disco_carrete_azul", "16 Disco del carrete azul", g.CAR_A[0], g.CAR_A[1], g.CAR_A[2], 1, "Al6061-T6_10mm"),
    ("17_AHP", "17 AHP poste de enganche", g.AHP[0], g.AHP[1], g.AHP[2], 1, "Al6061-T6_25,4mm_chorro_de_agua"),
]
for arch, tit, poly, hs, cs, q, mat in DXF:
    dxf(f"{arch}_{mat}_x{q}", poly, hs, cs, nota=f"{tit} - {mat.replace('_', ' ')} - cantidad {q} - MEDIDAS EN MILIMETROS")


def altura(cfg):
    tau, phi, a1, a2, fg, z0 = SOL[cfg]
    return float(z0 + (Rx(tau) @ np.array([0, *g.PIN_ABAJO]))[2]), float(np.linalg.norm((a1 - a2)[:2]))


res = dict(tau=math.degrees(SOL["A"][0]), phi=math.degrees(SOL["A"][1]), Z0=float(Z0), alfa=ALFA_D, gin_tubo_L=float(GP_L),
           altura_I2=altura("A")[0], lado_triangulo=altura("A")[1], altura_B=altura("B")[0], lado_B=altura("B")[1],
           punta_A=float(PUNTA_A), punta_B=float(PUNTA_B), sale_arriba=float(-TOP_B - g.CAS_L),
           piezas=meta, piezas_B=meta_de(MUNDO_B, Z0_B),
           acc=[dict(node=f"a_{it[0]}", id=it[0], nombre=it[1], grupo=it[4], vol=round(it[2].val().Volume(), 1)) for it in ACC],
           vol_sueltas={pid: round(s_.val().Volume(), 1) for pid, nom, s_ in SUELTAS})
json.dump(res, open(os.path.join(OUT, "armado.json"), "w"), indent=1, ensure_ascii=False)
print({k: (round(v, 1) if isinstance(v, float) else v) for k, v in res.items() if not isinstance(v, (list, dict))})
