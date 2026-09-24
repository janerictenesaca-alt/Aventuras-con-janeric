"""Bípode tipo Arizona Vortex (versión 3): todas las medidas en mm.

Medidas sacadas de las fotos del Vortex usando como referencia las medidas oficiales:
pata de arriba Ø 50,8 × 978, pata de abajo Ø 59,7 × 1054, cabeza 417 × 98 × 165.
"""
import math
from shapely.geometry import Point, Polygon, LineString, box
from shapely.affinity import rotate as srot
from shapely.ops import unary_union

ANG = 20.0                                   # cada pata respecto a la vertical
SA, CA = math.sin(math.radians(ANG)), math.cos(math.radians(ANG))

# ---------------------------------------------------------------- tubos (aluminio 6061-T6)
CAS_OD, CAS_ID, CAS_L = 63.5, 51.4, 152.0    # casquillo: tubo 2½" × 1/4", interior torneado a 51,4
SUP_OD, SUP_E, SUP_L = 50.8, 6.35, 980.0     # pata de arriba: tubo 2" × 1/4"
INF_OD, INF_E, INF_TUBO = 60.3, 3.91, 930.0  # pata de abajo: tubo 2" céd. 40 (ID 52,5)
ESP_L, ESP_DENTRO = 240.0, 120.0             # espiga de la pata de abajo (tubo 2" × 1/4")
INF_TOTAL = INF_TUBO + (ESP_L - ESP_DENTRO)  # 1050

# ---------------------------------------------------------------- cabeza
XC = 154.0                                   # centro de cada casquillo (a lo ancho)
PL_T = 12.7                                  # placas del cuerpo: 1/2"
PL_GAP = 19.05                               # espacio entre las 2 placas (3/4")
S_TOPE = -56.0                               # perno tope (entra en la muesca de la pata)
S_PASADOR = 40.0                             # pasador de la pata en el casquillo
MUESCA_A, MUESCA_P = 11.0, 22.0              # muesca en U de la pata de arriba
S_PUNTA_PATA = S_TOPE - MUESCA_P + 4.75      # dónde queda la punta de la pata de arriba


def eje(lado, s, off=0.0):
    """Punto en el eje del casquillo (lado +1 derecho). off = desplazamiento perpendicular hacia afuera/arriba."""
    x = XC + s * SA + off * CA
    z = -s * CA + off * SA
    return (lado * x, z)


D_PATA = 9.9        # pasador de bola 3/8"
D_P58 = 16.3        # pasador de bola 5/8"
D_P34 = 19.4        # pasador de bola 3/4" (carga principal)
D_AM = 25.0         # hueco para mosquetón

HUECOS_PLACA = [
    ("O1", -45.0, 38.0, D_AM),      # orejas de arriba (vientos)
    ("O2", 45.0, 38.0, D_AM),
    ("P1", -86.0, 0.0, D_P58),     # 4 pasadores de cabeza (como los dorados del Vortex)
    ("P2", 86.0, 0.0, D_P58),
    ("P3", -77.0, -62.0, D_P58),
    ("P4", 77.0, -62.0, D_P58),
    ("C1", 0.0, -14.0, D_AM),        # hueco central horizontal
    ("C2", 0.0, -66.0, D_P34),      # pasador principal de carga
]
VENTANAS = [(-115.0, -32.0), (115.0, -32.0)]   # ventanas de amarre junto a los casquillos
VENT_L, VENT_A = 44.0, 18.0


def contorno_placa():
    # cuadrilátero entre las caras internas de los casquillos
    r = CAS_OD / 2
    fin = -math.sqrt(r ** 2 - (PL_GAP / 2 + PL_T) ** 2)   # la cara de afuera de la placa toca el tubo
    a = eje(1, -38, fin)
    b = eje(1, 74, fin)
    base = Polygon([(-a[0], a[1]), a, b, (-b[0], b[1])])
    # hundimiento de arriba (curva cóncava como el Vortex)
    base = base.difference(Point(0, 400).buffer(400 - 16, quad_segs=64))
    # orejas de arriba
    orejas = [Point(x, z).buffer(D_AM / 2 + 13, quad_segs=32) for n, x, z, d in HUECOS_PLACA if n.startswith("O")]
    # lóbulo central de abajo (pasador principal)
    lobulo = Point(0, -66).buffer(D_P34 / 2 + 22, quad_segs=32)
    lobs = [Point(x, z).buffer(D_P58 / 2 + 15, quad_segs=32) for n, x, z, d in HUECOS_PLACA if n in ("P3", "P4")]
    u = unary_union([base] + orejas + [lobulo] + lobs)
    # entrantes de abajo que forman la "H"
    for sx in (-1, 1):
        u = u.difference(Point(sx * 40, -112).buffer(24, quad_segs=32))
    u = u.buffer(3, quad_segs=16).buffer(-3, quad_segs=16)
    return u.simplify(0.05)


def ventana(x, z):
    s = LineString([(x, z - VENT_L / 2 + VENT_A / 2), (x, z + VENT_L / 2 - VENT_A / 2)]).buffer(VENT_A / 2, quad_segs=16)
    return srot(s, ANG if x > 0 else -ANG, origin=(x, z))


# nervios internos (la "H" que se ve en el Vortex): 2 placas entre las placas del cuerpo
NERVIO_X = 32.0
NERVIO_Z = (-60.0, 22.0)

# ---------------------------------------------------------------- patas
HUECOS_SUP = [113.0 + 150.0 * i for i in range(5)]      # 113, 263, 413, 563, 713
ULTIMO = 713.0
INF_HUECO_ARRIBA = 40.0                                   # desde la punta de arriba del tubo
ESP_HUECO = 80.0                                          # hueco de la espiga, desde su punta
ESP_PERNOS = (30.0, 90.0)                                 # pernos fijos, desde la punta de abajo del tubo

# ---------------------------------------------------------------- pies
PIE_CAS_L = 130.0          # casquillo del pie (tubo acero 2" céd. 40)
PIE_HUECO = 40.0
PIE_PLACA_T = 12.0         # garra: plancha A36 12 mm


def contorno_garra():
    """Pie de garra (tipo Raptor). Origen = eje, en la punta de abajo del casquillo. y hacia arriba."""
    lengua = box(-36, 0, 36, 55)                             # parte que entra en las ranuras del casquillo
    cuerpo = Polygon([(-70, 0), (70, 0), (58, -48), (20, -62), (-20, -62), (-58, -48)])
    punta = Polygon([(-16, -60), (16, -60), (0, -105)])
    gancho = Polygon([(58, -48), (70, 0), (86, -30), (80, -62)])
    return unary_union([lengua, cuerpo, punta, gancho]).buffer(4, quad_segs=16).buffer(-4, quad_segs=16).simplify(0.05)


HUECOS_GARRA = [("L1", -36.0, -24.0, D_AM), ("L2", 36.0, -24.0, D_AM)]
RANURA_GARRA = (68.0, -38.0, 10.0, 26.0)   # ranura para cinta: x, y, ancho, largo (girada)
GARRA_PUNTA = -105.0
PIE_ALTO = PIE_CAS_L - GARRA_PUNTA          # de la boca del casquillo a la punta: 235 … se entierra ~30

# ---------------------------------------------------------------- accesorios de amarre
# Placa de amarre de pata (tipo AZORP): carrete que se pone en la pata de arriba
CAR_TUBO_L = 110.0         # tubo 2" céd. 40 (ID 52,5 sobre la pata de 50,8)
CAR_DISCO = 150.0
CAR_T = 9.53
CAR_HUECOS = 8
CAR_PCD = 110.0
D_CAR = 22.0

# Placa de amarre de unión (disco con casquillo y espiga): va entre dos patas de abajo o entre pata y pie
UNI_DISCO = 190.0
UNI_T = 12.7
UNI_HUECOS = 10
UNI_PCD = 145.0
UNI_CAS_L = 120.0


def huecos_circulo(n, pcd, d, desfase=0.0):
    return [(f"R{i + 1}", round(pcd / 2 * math.cos(math.radians(desfase + 360 / n * i)), 1),
             round(pcd / 2 * math.sin(math.radians(desfase + 360 / n * i)), 1), d) for i in range(n)]


# ---------------------------------------------------------------- alturas
def alturas():
    filas = []
    for n in (1, 2, 3):
        for h in HUECOS_SUP[1:]:
            L = (h - HUECOS_SUP[0]) + (INF_TUBO - INF_HUECO_ARRIBA) + INF_TUBO * (n - 1) + PIE_ALTO - 30
            px, pz = eje(1, S_PASADOR)
            z_pas = L * CA
            carga = z_pas + (-66.0 - pz)
            filas.append(dict(n=n, hueco=h, largo=L, carga=carga,
                              arriba=z_pas + (82.0 - pz),
                              abertura=2 * (px + L * SA)))
    return filas
