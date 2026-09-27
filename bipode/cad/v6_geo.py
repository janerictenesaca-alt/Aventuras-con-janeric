"""Trípode tipo Arizona Vortex, versión 6: cabeza A-frame y gin pole hechas con PLACAS DE CORTE LÁSER
soldadas con TIG, como copia de la pieza maquinada original.

Ejes (cabeza A-frame): X = ancho, Y = fondo (la cara lisa mira a +Y), Z = alto.
Todas las medidas en mm. Medidas generales iguales al Vortex: 417 de ancho × 165 de alto.
"""
import math

from shapely.affinity import rotate as srot
from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union

T = 10.0                          # plancha de aluminio 6061-T6 de 10 mm (todas las placas)
ANG = 30.0                        # cada casquillo a 30° de la vertical (60° entre patas)
SA, CA = math.sin(math.radians(ANG)), math.cos(math.radians(ANG))
XC, ZT = 108.0, 70.0              # punto de arriba del eje de cada casquillo
CAS_OD, CAS_ID, CAS_L = 63.5, 51.4, 145.0
D12 = 13.1                        # hueco para pasador de cabeza 1/2"
D38 = 9.9                         # hueco para pasador de pata 3/8"
D_MOSQ = 22.0                     # hueco para mosquetón (barra hasta 13 mm)

# posiciones de las placas en X (cara izquierda de cada placa; la placa ocupa x .. x+T)
X_NERV_EXT = 63.0                 # nervios exteriores: x = ±63 … ±73
X_NERV_INT = 33.0                 # nervios interiores: x = ±33 … ±43
X_CENTRAL = 13.0                  # placas centrales (orejas A): x = ±13 … ±23
Y_FRENTE = (10.0, 20.0)           # placa frontal: y = 10 … 20
Y_ATRAS = -52.0                   # los nervios llegan hasta y = −52
Z_BASE = (-48.0, -38.0)           # placa de base
Z_PUENTE = (36.0, 46.0)           # puente del canal D

# huecos de los nervios (y, z)
PIN_ARRIBA = (-26.0, 34.0)
PIN_ABAJO = (-26.0, -18.0)
H_HUECO = (-26.0, 8.0)            # H: punto de amarre lateral (solo nervio exterior)
A_HUECO = (-22.0, 72.0)           # A: unión de la gin pole
B_HUECO = (-22.0, 12.0)           # B: unión central horizontal (polea)
C_HUECO = (0.0, -22.0)            # C: unión central vertical (x, y) en el puente


def eje(lado, s, off=0.0):
    """Punto (x, z) sobre el eje del casquillo. off > 0 hacia afuera."""
    x = XC + s * SA + off * CA
    z = ZT - s * CA + off * SA
    return (lado * x, z)


# ------------------------------------------------------------------ 01 placa frontal (cara lisa)
ARCO_R, ARCO_Z = 218.75, 274.75   # borde de arriba cóncavo: baja 14 mm en el centro
OFF_BORDE = 26.0                  # el borde lateral queda a 26 del eje del casquillo (dentro de la pared)


def placa_frontal():
    tr = Polygon([eje(-1, -30, -OFF_BORDE), eje(-1, 160, -OFF_BORDE), eje(1, 160, -OFF_BORDE), eje(1, -30, -OFF_BORDE)])
    p = tr.intersection(box(-400, Z_BASE[0], 400, 200))
    p = p.difference(Point(0, ARCO_Z).buffer(ARCO_R, quad_segs=96))
    for sx in (-1, 1):
        p = p.difference(Point(sx * 53.0, Z_BASE[0]).buffer(9.0, quad_segs=32))      # muescas de abajo
    p = p.buffer(2, quad_segs=8).buffer(-2, quad_segs=8)
    return Polygon(p.exterior).simplify(0.02)


def ventana(lado):
    """E: ventana triangular redondeada (anclaje de abajo, se ve el nervio detrás)."""
    t = Polygon([(lado * 84.0, 26.0), (lado * 118.0, -30.0), (lado * 84.0, -30.0)])
    return t.buffer(-5, quad_segs=8).buffer(5, quad_segs=12)


def corazon():
    """Hueco central en forma de corazón (se ve el hueco C y la polea)."""
    c = unary_union([Point(-7.5, -4.0).buffer(8.5, quad_segs=24), Point(7.5, -4.0).buffer(8.5, quad_segs=24),
                     Polygon([(-15.5, -6.0), (15.5, -6.0), (0.0, -27.0)])])
    return c.buffer(1.5, quad_segs=8).buffer(-1.5, quad_segs=8)


def cortes_frontal():
    return [ventana(-1), ventana(1), corazon()]


# ------------------------------------------------------------------ 02/03 nervios (perfil en y, z)
def perfil_nervio(z_arriba, exterior):
    p = box(Y_ATRAS, Z_BASE[1], Y_FRENTE[0], z_arriba)
    p = p.difference(box(Y_ATRAS - 1, z_arriba - 16, Y_ATRAS + 16, z_arriba + 1)).union(
        Point(Y_ATRAS + 16, z_arriba - 16).buffer(16, quad_segs=24)).intersection(box(Y_ATRAS, Z_BASE[1], Y_FRENTE[0], z_arriba))
    huecos = [("I1", *PIN_ARRIBA, D12), ("I2", *PIN_ABAJO, D12)]
    if exterior:
        huecos.append(("H", *H_HUECO, D_MOSQ))
    return p, huecos


def alto_frontal(x):
    """Altura del borde de arriba de la placa frontal en la posición x."""
    return ARCO_Z - math.sqrt(ARCO_R ** 2 - x ** 2)


NERV_EXT = perfil_nervio(48.0, True)
NERV_INT = perfil_nervio(48.0, False)


# ------------------------------------------------------------------ 04 placas centrales con orejas A
def perfil_central():
    cuerpo = box(Y_ATRAS, Z_BASE[1], Y_FRENTE[0], 56.0)
    oreja = unary_union([box(A_HUECO[0] - 20, 40.0, A_HUECO[0] + 20, A_HUECO[1]),
                         Point(*A_HUECO).buffer(20, quad_segs=32)])
    p = unary_union([cuerpo, oreja])
    p = p.buffer(4, quad_segs=8).buffer(-8, quad_segs=8).buffer(4, quad_segs=8)
    p = p.union(box(Y_ATRAS, Z_BASE[1], Y_FRENTE[0], 30))          # base recta para soldar
    huecos = [("A", *A_HUECO, D12), ("B", *B_HUECO, D12)]
    return Polygon(p.exterior).simplify(0.02), huecos


CENTRAL = perfil_central()


# ------------------------------------------------------------------ 05 puente del canal D (x, y)
def perfil_puente():
    p = box(-X_CENTRAL, Y_ATRAS, X_CENTRAL, Y_FRENTE[0])
    return p, [("C", *C_HUECO, D12)]


PUENTE = perfil_puente()


# ------------------------------------------------------------------ 06 placa de base (x, y)
def perfil_base():
    ancho = X_NERV_EXT + T
    p = box(-ancho, Y_ATRAS, ancho, Y_FRENTE[0])
    p = p.buffer(-6, quad_segs=8).buffer(6, quad_segs=8)
    huecos = [("E1", -53.0, -24.0, D_MOSQ), ("E2", 53.0, -24.0, D_MOSQ)]
    return p, huecos


BASE = perfil_base()

# ------------------------------------------------------------------ gin pole (ejes propios: tubo sobre −Z)
GP_T = 10.0
GP_TUBO_L = 142.0                 # del borde de arriba del ala a la boca
GP_FORK_X = X_CENTRAL + T + 0.5   # las horquillas quedan por fuera de las orejas A (23,5 … 33,5)
GP_BISAGRA = (84.0, -22.0)        # (y, z) del hueco de la horquilla


def perfil_ala():
    """Ala de la gin pole (escudo con 4 huecos ovalados y el tubo al centro), en (x, y)."""
    p = unary_union([Point(0, 0).buffer(66, quad_segs=64), box(-GP_FORK_X - GP_T, 0, GP_FORK_X + GP_T, 96)])
    p = p.intersection(box(-63.5, -66, 63.5, 96))
    p = p.buffer(-8, quad_segs=8).buffer(8, quad_segs=16)
    ovalos = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            o = LineString([(sx * 44, sy * 16 - 6), (sx * 44, sy * 16 + 6)]).buffer(9.5, quad_segs=16)
            ovalos.append(srot(o, -sx * sy * 20, origin=(sx * 44, sy * 16)))
    return Polygon(p.exterior).simplify(0.02), ovalos, [("T", 0.0, 0.0, CAS_OD + 0.4)]


ALA = perfil_ala()


def perfil_horquilla():
    """Horquilla de la gin pole (y, z): cuelga del ala hacia abajo, con el hueco de la bisagra."""
    y0, z0 = GP_BISAGRA
    p = unary_union([box(y0 - 20, z0, y0 + 12, 0), Point(y0, z0).buffer(20, quad_segs=32)])
    p = p.intersection(box(-200, -200, 96, 0))
    return p, [("A", y0, z0, D12)]


HORQ = perfil_horquilla()
