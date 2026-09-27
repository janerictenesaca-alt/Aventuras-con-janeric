"""Trípode tipo Arizona Vortex (v5): medidas de la cabeza A-frame maquinada, la cabeza gin pole y el armado.

Las patas, los pies y los pasadores son los de v4_geo (sacados del catálogo y del manual del Vortex).
Geometría del trípode de patas iguales: las patas de la cabeza A-frame se abren 30° cada una; para que las
3 patas queden iguales, la cabeza se inclina 19,47° y cada pata queda a 35,26° de la vertical. Con eso la
altura sale 2,44 m (2 patas de afuera) y 3,20 m (3 patas de afuera): la tabla del Vortex dice 2,41 y 3,20 m.
"""
import math

from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union

import v4_geo as g4
from v4_geo import (ANG, SA, CA, HEMBRA_OD, HEMBRA_ID, D38, D12, D_MOSQ,
                    G_DESDE_BOCA, RANURA_A, RANURA_P, RANURAS_ANG)

YT = 70.0                    # altura del eje de cada casquillo arriba
XC = 99.0                    # arriba del eje de cada casquillo: con 99 la cabeza mide 417 de ancho, igual al Vortex


def eje(lado, s, off=0.0):
    """Punto sobre el eje del casquillo. lado +1 derecho, -1 izquierdo. off: hacia afuera."""
    x = XC + s * SA + off * CA
    y = YT - s * CA + off * SA
    return (lado * x, y)


CAS_L = 145.0                # casquillo de la cabeza: con 145 la cabeza mide 165 de alto, igual al Vortex

# ------------------------------------------------------------------ trípode
TAU = math.degrees(math.asin(SA / (CA * math.sqrt(3))))       # 19,47°: inclinación de la cabeza
BETA = math.degrees(math.asin(2 * CA * math.sin(math.radians(TAU))))   # 35,26°: cada pata

# ------------------------------------------------------------------ cabeza A-frame (una pieza, CNC)
FONDO = HEMBRA_OD            # 63,5: fondo del cuerpo (en Y)
PARED = 9.5                  # pared delantera y trasera
BAHIA = FONDO - 2 * PARED    # 44,5: hueco entre paredes donde entran los mosquetones
R_CUBRE = HEMBRA_OD / 2 + 13.0
CUBRE = 100.0

HUECOS = [   # (nombre, x, z, diámetro, uso) · todos atraviesan en Y (de frente a atrás)
    ("B", 0.0, 0.0, D12, "Unión central horizontal: pasador de cabeza 1/2\" (polea)"),
    ("I1", -62.0, 34.0, D12, "Unión 1/2\" izquierda de arriba"),
    ("I2", 62.0, 34.0, D12, "Unión 1/2\" derecha de arriba"),
    ("I3", -38.0, -32.0, D12, "Unión 1/2\" izquierda de abajo"),
    ("I4", 38.0, -32.0, D12, "Unión 1/2\" derecha de abajo"),
]
for lado, t in ((-1, "I"), (1, "D")):
    x, z = eje(lado, 62.0, 58.0)
    HUECOS.append((f"H{t}", round(x, 1), round(z, 1), D_MOSQ, "Punto de amarre lateral, hacia afuera"))

OREJA_X = (15.2, 29.2)       # cada oreja A va de x = 15,2 a 29,2 (14 de grueso)
OREJA_Z = (44.0, 92.0)       # de la base a la punta (arriba de todo = 92)
OREJA_HUECO_Z = 74.0         # hueco 1/2" en X
C_HUECO = (0.0, 12.0, 60.0)  # hueco vertical C: x, z abajo, z arriba
TOPE_CUERPO = 48.0           # altura del lomo del cuerpo entre las orejas (canal D)


def cubre(lado):
    return LineString([eje(lado, 0), eje(lado, CUBRE)]).buffer(R_CUBRE, cap_style=2)


def ventana(lado):
    """Ventana triangular E (anclaje de abajo)."""
    a, b, c = (lado * 54.0, -2.0), (lado * 82.0, -4.0), (lado * 64.0, -22.0)
    return Polygon([a, b, c]).buffer(6, quad_segs=12)


def perfil_cuerpo():
    """Perfil del cuerpo visto de frente (plano XZ)."""
    r = R_CUBRE
    centro = Polygon([eje(-1, 0, -r), eje(1, 0, -r), eje(1, CUBRE, -r), (66.0, -40.0), (30.0, -54.0),
                      (-30.0, -54.0), (-66.0, -40.0), eje(-1, CUBRE, -r)])
    lomo = Polygon([eje(-1, 0, r * 0.2), (-34.0, TOPE_CUERPO), (34.0, TOPE_CUERPO), eje(1, 0, r * 0.2)])
    lobulos = [Point(x, z).buffer(d / 2 + 16, quad_segs=32) for n, x, z, d, _ in HUECOS if n[0] == "H"]
    u = unary_union([cubre(-1), cubre(1), centro, lomo] + lobulos).buffer(12, quad_segs=24).buffer(-12, quad_segs=24)
    u = Polygon(u.exterior)
    for sx in (-1, 1):
        u = u.difference(Point(sx * 88.0, -62.0).buffer(26, quad_segs=48))
    u = u.buffer(5, quad_segs=12).buffer(-5, quad_segs=12)
    return u.simplify(0.03)


def bolsillos():
    """Rebajes de 5 mm en las caras de adelante y atrás (alivianan y dan el acabado maquinado)."""
    return [b.buffer(-5, quad_segs=12) for b in bahias() if b.buffer(-5).area > 200]


def bahias():
    """Zonas vaciadas entre las 2 paredes (los mosquetones entran por aquí a los pasadores I)."""
    P = perfil_cuerpo().buffer(-10)
    quitar = unary_union([cubre(-1).buffer(3), cubre(1).buffer(3), Point(0, 0).buffer(22, quad_segs=32),
                          box(-17, -200, 17, 300)] +
                         [Point(x, z).buffer(d / 2 + 16) for n, x, z, d, _ in HUECOS if n[0] == "H"])
    b = P.difference(quitar)
    partes = [p for p in getattr(b, "geoms", [b]) if p.area > 400]
    return [p.buffer(-3).buffer(3, quad_segs=12) for p in partes]


# ------------------------------------------------------------------ cabeza gin pole (una pieza, CNC, naranja)
GP_CAS_L = 130.0             # casquillo para la pata (igual al de la cabeza A-frame)
GP_ALA = (127.0, 76.0, 20.0)  # ala de amarre: ancho X, fondo Y, grueso Z  (medidas totales del Vortex)
GP_ALA_HUECOS = [("G1", -44.0, 17.0), ("G2", 44.0, 17.0), ("G3", -44.0, -17.0), ("G4", 44.0, -17.0)]
GP_LENGUA = (30.0, 54.0, 62.0)   # lengüeta: grueso X (entra entre las orejas), fondo Y, alto Z
GP_HUECO_Z = 40.0            # hueco 1/2" de la lengüeta, sobre el ala
GP_TOTAL = GP_CAS_L + GP_ALA[2] + GP_LENGUA[2]    # 212 (Vortex 212)

# ------------------------------------------------------------------ alturas del trípode
def largo(n_ext, hueco):
    return g4.largo_pata(n_ext, hueco)


def altura(n_ext, hueco):
    """Del suelo al hueco B, trípode de patas iguales."""
    _, zm = eje(1, CAS_L)
    return largo(n_ext, hueco) * math.cos(math.radians(BETA)) - zm * math.cos(math.radians(TAU))


def radio_pies(n_ext, hueco):
    return largo(n_ext, hueco) * math.sin(math.radians(BETA))


def lado_triangulo(n_ext, hueco):
    return radio_pies(n_ext, hueco) * math.sqrt(3)
