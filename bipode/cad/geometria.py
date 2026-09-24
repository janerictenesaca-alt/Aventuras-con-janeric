"""Geometría 2D y medidas del bípode (A-frame) de aluminio.

Todas las medidas en milímetros. Este archivo es la única fuente de medidas:
el modelo 3D, los DXF para corte y los planos salen de aquí.
"""
import math
from shapely.geometry import Point, LineString, Polygon, box
from shapely.ops import unary_union

# ---------------------------------------------------------------- materiales
PLACA_AL = 9.53          # plancha aluminio 6061-T6 de 3/8"
PLACA_AC = 10.0          # plancha acero A36 de 10 mm (pies)
PLACA_AC_BASE = 8.0      # plancha acero A36 de 8 mm (base pie plano)

# Tubos (aluminio 6061-T6)
SUP_OD, SUP_ESP, SUP_L = 50.8, 6.35, 1500.0     # pata de arriba: tubo 2" x 1/4"
INF_OD, INF_ESP, INF_L = 60.3, 3.91, 1500.0     # pata de abajo: tubo 2" cédula 40
CAS_OD, CAS_ESP, CAS_L = 60.3, 3.91, 160.0      # casquillo de la cabeza (mismo tubo)
MAN_OD, MAN_ESP, MAN_L = 73.0, 5.16, 90.0       # manguito del anillo: tubo 2 1/2" céd. 40

GAP = 60.5               # separación interna entre placas de la cabeza
ANG = 18.0               # inclinación de cada pata respecto a la vertical (grados)

# Huecos
D_PATA = 9.9             # pasador de bola 3/8" (broca 25/64")
D_PERNO12 = 13.1         # perno / pasador 1/2" (broca 33/64")
D_BARRA = 25.8           # barra de carga de 1" (25,4)
D_AMARRE = 25.0          # hueco para mosquetón

# ------------------------------------------------------------ cabeza (placa)
_s, _c = math.sin(math.radians(ANG)), math.cos(math.radians(ANG))
P_DER = (150.0, 20.0)                     # punto de referencia del eje del casquillo derecho
D_DER = (_s, -_c)                          # dirección del eje hacia abajo
S_PERNO_FIJO, S_PASADOR = -45.0, 35.0     # posición de los 2 huecos del casquillo sobre su eje
S_TOPE_PATA = -40.0                        # la punta de la pata de arriba queda aquí


def eje(lado, s):
    """Punto sobre el eje del casquillo. lado=+1 derecho, -1 izquierdo."""
    x = P_DER[0] + s * D_DER[0]
    y = P_DER[1] + s * D_DER[1]
    return (lado * x, y)


# huecos de la placa: (nombre, x, y, diámetro)
HUECOS_PLACA = [
    ("A1", 0.0, 82.0, D_AMARRE),
    ("A4", -120.0, -112.0, D_AMARRE),
    ("A5", 120.0, -112.0, D_AMARRE),
    ("B1", 0.0, -78.0, D_BARRA),
    ("B2", -72.0, -62.0, D_BARRA),
    ("B3", 72.0, -62.0, D_BARRA),
    ("D1", -58.0, 78.0, D_PERNO12),
    ("D2", 58.0, 78.0, D_PERNO12),
]
for lado, tag in ((-1, "I"), (1, "D")):
    x, y = eje(lado, S_PERNO_FIJO)
    HUECOS_PLACA.append((f"C{tag}1", round(x, 1), round(y, 1), D_PATA))
    x, y = eje(lado, S_PASADOR)
    HUECOS_PLACA.append((f"C{tag}2", round(x, 1), round(y, 1), D_PATA))

VENTANA = (0.0, 8.0, 70.0, 28.0)          # ranura para cinta: centro x, y, largo, ancho


def contorno_placa():
    partes = []
    for lado in (-1, 1):
        seg = LineString([eje(lado, -70), eje(lado, 70)])
        partes.append(seg.buffer(34, quad_segs=32))
    for n, x, y, d in HUECOS_PLACA:
        if n.startswith("A"):
            m = 22
        elif n.startswith("B"):
            m = 25
        elif n.startswith("D"):
            m = 20
        else:
            continue
        partes.append(Point(x, y).buffer(d / 2 + m, quad_segs=32))
    u = unary_union(partes)
    return u.buffer(40, quad_segs=32).buffer(-40, quad_segs=32).simplify(0.05)


# ---------------------------------------------------------- anillo de amarre
ANI_OD = 200.0
ANI_HUECO_C = 73.5
ANI_PCD = 130.0
ANI_N = 8
HUECOS_ANILLO = [("R%d" % (i + 1),
                  round(ANI_PCD / 2 * math.cos(math.radians(22.5 + 45 * i)), 1),
                  round(ANI_PCD / 2 * math.sin(math.radians(22.5 + 45 * i)), 1),
                  D_AMARRE) for i in range(ANI_N)]
MAN_PASADOR_Z = 20.0      # hueco del pasador medido desde la punta de abajo del manguito
MAN_DISCO_Z = 55.0        # centro del disco medido desde la punta de abajo del manguito

# ---------------------------------------------------------- pie de garra
# origen = eje de la pata en la punta de abajo del tubo; y hacia arriba
PIE_RANURA_L = 75.0       # largo de las ranuras en la punta del tubo
PIE_RANURA_A = PLACA_AC + 0.5
PIE_PERNO_Y = 40.0        # hueco del perno 1/2" sobre la punta del tubo


def contorno_pie_garra():
    lengua = box(-40, 0, 40, PIE_RANURA_L)
    cuerpo = Polygon([(-75, 0), (75, 0), (55, -60), (-55, -60)])
    punta = Polygon([(-20, -58), (20, -58), (0, -120)])
    return unary_union([lengua, cuerpo, punta]).buffer(4, quad_segs=16).buffer(-4, quad_segs=16).simplify(0.05)


HUECOS_PIE_GARRA = [("P1", 0.0, PIE_PERNO_Y, D_PERNO12),
                    ("L1", -35.0, -25.0, D_AMARRE),
                    ("L2", 35.0, -25.0, D_AMARRE)]
PIE_PUNTA_Y = -120.0

# ---------------------------------------------------------- pie plano (opcional)
def contorno_pie_plano_lengua():
    lengua = box(-40, 0, 40, PIE_RANURA_L)
    bajo = box(-30, -55, 30, 0)
    return unary_union([lengua, bajo]).buffer(4, quad_segs=16).buffer(-4, quad_segs=16)


HUECOS_PIE_PLANO_LENGUA = [("P1", 0.0, PIE_PERNO_Y, D_PERNO12),
                           ("P2", 0.0, -30.0, D_PERNO12)]
BASE_LADO = 160.0
HUECOS_BASE = [("F%d" % (i + 1), sx * 60.0, sy * 60.0, 14.0)
               for i, (sx, sy) in enumerate(((-1, -1), (1, -1), (1, 1), (-1, 1)))]
OREJA = (70.0, 60.0)      # ancho x alto de cada oreja de la base


def contorno_oreja():
    w, h = OREJA
    return box(-w / 2, 0, w / 2, h).buffer(0)


HUECOS_OREJA = [("O1", 0.0, 35.0, D_PERNO12)]

# ---------------------------------------------------------- tubos
HUECOS_SUP = [75.0 + 150.0 * i for i in range(10)]        # desde la punta de arriba
ULTIMO_HUECO_UNION = 1125.0
HUECOS_INF = [30.0, 180.0, 480.0, 780.0, 1080.0]         # desde la punta de arriba
PERNO_PIE_DESDE_ABAJO = PIE_PERNO_Y


def alturas():
    """Tabla de alturas para cada hueco de unión de la pata de arriba."""
    filas = []
    for h in HUECOS_SUP:
        if h < 225 or h > ULTIMO_HUECO_UNION:
            continue
        # distancia entre el pasador de la cabeza y el perno del pie, sobre el eje
        pp = (h - 75.0) + (INF_L - HUECOS_INF[0] - PERNO_PIE_DESDE_ABAJO)
        eje_total = pp + (PIE_PERNO_Y - PIE_PUNTA_Y)       # hasta la punta del pie
        pin_x, pin_y = eje(1, S_PASADOR)
        z_pin = eje_total * _c                               # altura del pasador de la cabeza
        filas.append(dict(hueco=h, pasador_a_pie=pp,
                          altura_barra=z_pin + (-78.0 - pin_y),
                          altura_total=z_pin + (contorno_placa().bounds[3] - pin_y),
                          abertura=2 * (pin_x + eje_total * _s),
                          traslape=(SUP_L - h) + HUECOS_INF[0]))
    return filas
