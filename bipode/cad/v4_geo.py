"""Bípode tipo Arizona Vortex, versión 4. Todas las medidas en milímetros.

De dónde salen las medidas (ver notas-archivos.md):
- Pata de adentro Ø 50,8 × 978 y pata de afuera Ø 59,7 × 1054: catálogo Rock Exotica (VXUL, VXLL).
- Cabeza 417 × 98 × 165: catálogo Rock Exotica (VXAF).
- Huecos cada 150 mm, pasadores de pata 3/8" y de cabeza 1/2": manual del Vortex.
- Ángulo de las patas: con la tabla de la pág. 31 del manual (2,41 m → 3,05 m al sumar
  1 pata de afuera y tapar 1 hueco) sale 30° a 36° por pata. Se usa 30° en la cabeza:
  con un casquillo de 190 mm da exactamente los 165 mm de alto de la cabeza original.
"""
import math

from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union

ANG = 30.0
SA, CA = math.sin(math.radians(ANG)), math.cos(math.radians(ANG))
PULG = 25.4

# ------------------------------------------------------------------ materiales
# Aluminio 6061-T6 salvo que se diga otra cosa
MACHO_OD, MACHO_E = 50.8, 6.35          # tubo 2" × 1/4": pata de adentro y espigones
HEMBRA_OD, HEMBRA_ID = 63.5, 51.4       # tubo 2½" × 1/4" (ID 50,8) torneado por dentro a 51,4
EXT_OD, EXT_E = 60.3, 3.91              # tubo 2" cédula 40 (ID 52,5): cuerpo de la pata de afuera

PL_T = 12.7                             # placas de la cabeza: 1/2"
GAP = HEMBRA_OD                         # separación entre placas = diámetro del casquillo

D38 = 9.9                               # hueco para pasador de bola 3/8" (broca 25/64")
D12 = 13.1                              # hueco para perno o pasador 1/2" (broca 33/64")
D_BARRA = 25.8                          # barra de carga de 1"
D_MOSQ = 25.0                           # hueco para mosquetón
D_M10 = 10.5

# ------------------------------------------------------------------ cabeza
XC, YT = 80.0, 75.0                     # arriba del eje de cada casquillo
CAS_L = 190.0                           # casquillo: de s=0 (arriba) a s=190 (boca)
CUBRE = 100.0                           # las placas cubren el casquillo de s=0 a s=100
R_CUBRE = HEMBRA_OD / 2 + 16.0
S_PERNOS = (25.0, 70.0)                 # pernos 1/2" que sujetan cada casquillo
ESPIGA_DENTRO = 110.0                   # lo que entra un espigón o una pata de adentro
G_DESDE_BOCA = (50.0, 80.0)             # huecos G del pasador de pata (desde la boca)
RANURA_A, RANURA_P = 11.0, 14.0         # ranuras de alineación F en la boca
RANURAS_ANG = (0.0, 120.0, 240.0)


def eje(lado, s, off=0.0):
    """Punto sobre el eje del casquillo. lado +1 derecho, -1 izquierdo. off: hacia afuera."""
    x = XC + s * SA + off * CA
    y = YT - s * CA + off * SA
    return (lado * x, y)


# huecos de la placa: (nombre, x, y, diámetro, para qué)
HUECOS_PLACA = [
    ("A1", -46.0, 100.0, D12, "Oreja: pasador 1/2\" para cabeza gin pole o vientos"),
    ("A2", 46.0, 100.0, D12, "Oreja: pasador 1/2\" para cabeza gin pole o vientos"),
    ("B", 0.0, 0.0, D_BARRA, "Barra de carga central de 1\" (polea o carga)"),
    ("I1", -56.0, 40.0, D12, "Pasador 1/2\" con separador: anclaje de arriba"),
    ("I2", 56.0, 40.0, D12, "Pasador 1/2\" con separador: anclaje de arriba"),
    ("I3", -34.0, -32.0, D12, "Pasador 1/2\" con separador: anclaje de abajo"),
    ("I4", 34.0, -32.0, D12, "Pasador 1/2\" con separador: anclaje de abajo"),
    ("C1", -16.0, 31.0, D_M10, "Perno M10 del bloque C"),
    ("C2", 16.0, 31.0, D_M10, "Perno M10 del bloque C"),
]
for lado, t in ((-1, "I"), (1, "D")):
    for i, s in enumerate(S_PERNOS, 1):
        x, y = eje(lado, s)
        HUECOS_PLACA.append((f"S{t}{i}", round(x, 1), round(y, 1), D12, "Perno 1/2\" que sujeta el casquillo"))
    x, y = eje(lado, 38.0, 64.0)
    HUECOS_PLACA.append((f"H{t}", round(x, 1), round(y, 1), D_MOSQ, "Punto de amarre lateral hacia afuera"))


def cubre(lado):
    return LineString([eje(lado, 0), eje(lado, CUBRE)]).buffer(R_CUBRE, cap_style=2)


def ventana(lado):
    """Ventana triangular E: por aquí entra el mosquetón al perno I3 / I4."""
    a, b, c = (lado * 50.0, -2.0), (lado * 74.0, -4.0), (lado * 58.0, -22.0)
    return Polygon([a, b, c]).buffer(6, quad_segs=12)


def contorno_placa():
    r = R_CUBRE
    centro = Polygon([eje(-1, 0, -r), eje(1, 0, -r), eje(1, CUBRE, -r), (58.0, -40.0), (30.0, -54.0),
                      (-30.0, -54.0), (-58.0, -40.0), eje(-1, CUBRE, -r)])
    orejas = [Point(x, y).buffer(d / 2 + 16, quad_segs=32) for n, x, y, d, _ in HUECOS_PLACA if n[0] in "AH"]
    arriba = Polygon([eje(-1, 0, r * 0.2), (-46.0, 100.0), (46.0, 100.0), eje(1, 0, r * 0.2)])
    u = unary_union([cubre(-1), cubre(1), centro, arriba] + orejas).buffer(12, quad_segs=24).buffer(-12, quad_segs=24)
    u = Polygon(u.exterior)
    # canal D para la cuerda, arriba entre las orejas
    u = u.difference(Point(0, 110).buffer(26, quad_segs=48)).difference(box(-26, 110, 26, 300))
    # arcos de abajo entre el lóbulo central y los casquillos
    for sx in (-1, 1):
        u = u.difference(Point(sx * 76.0, -62.0).buffer(24, quad_segs=48))
    u = u.buffer(5, quad_segs=12).buffer(-5, quad_segs=12)
    return u.simplify(0.03)


def cortes_placa():
    return [ventana(-1), ventana(1)]


BLOQUE_C = (50.0, 34.0, 14.0)           # ancho, alto, y de abajo  (hueco vertical Ø 22)
D_C_VERT = 22.0

# ------------------------------------------------------------------ pata de afuera (PE)
PE_TUBO = 940.0                         # tubo 2" céd. 40
PE_ESPIGA = 230.0                       # espigón 2" × 1/4"
PE_ESPIGA_DENTRO = 120.0                # lo que entra el espigón en el tubo
PE_PERNOS = (30.0, 90.0)                # pernos 3/8" fijos, desde la punta de arriba del tubo
PE_TOTAL = PE_TUBO + PE_ESPIGA - PE_ESPIGA_DENTRO       # 1050
PE_HUECO_ESPIGA = ESPIGA_DENTRO - G_DESDE_BOCA[0]        # 60 desde la punta del espigón
TOPE_DESDE_PUNTA = ESPIGA_DENTRO - 8.0                   # tope de alineación, 102 de la punta
PE_HUECO_BOCA = G_DESDE_BOCA[0]                          # 50 desde la boca de abajo

# ------------------------------------------------------------------ pata de adentro (PI)
PI_L = 980.0
PI_HUECOS = [60.0 + 150.0 * i for i in range(6)]        # 60, 210, 360, 510, 660, 810
PI_HUECO_PIE = PI_L - 50.0                               # 930
MUESCA_A, MUESCA_P = 11.0, 22.0

# ------------------------------------------------------------------ pie Raptor (acero)
PIE_CAS_L = 120.0                       # tubo acero Ø 63,5 × 6 (ID 51,5)
PIE_HUECO = 50.0
GARRA_T = 12.0


def contorno_garra():
    """Garra tipo Raptor. Origen: eje de la pata en la boca de abajo del casquillo; y hacia arriba."""
    lengua = box(-38, 0, 38, 60)
    cuerpo = Polygon([(-72, 0), (72, 0), (60, -40), (24, -58), (-24, -58), (-60, -40)])
    pico = Polygon([(-18, -54), (18, -54), (3, -112), (-3, -112)])
    talon = Polygon([(60, -40), (72, 0), (96, -22), (88, -70), (70, -62)])
    return unary_union([lengua, cuerpo, pico, talon]).buffer(4, quad_segs=12).buffer(-4, quad_segs=12).simplify(0.03)


HUECOS_GARRA = [("L1", -38.0, -24.0, D_MOSQ, "Maniota o anclaje"),
                ("L2", 36.0, -24.0, D_MOSQ, "Maniota o anclaje")]
GARRA_PUNTA = -112.0

# ------------------------------------------------------------------ pie plano
BASE_LADO, BASE_T = 150.0, 10.0
HUECOS_BASE = [(f"F{i + 1}", sx * 55.0, sy * 55.0, 14.0, "Perno de anclaje 1/2\" a la roca")
               for i, (sx, sy) in enumerate(((-1, -1), (1, -1), (1, 1), (-1, 1)))]

# ------------------------------------------------------------------ placa de amarre de 2 pisos (mejora)
AM_CUERPO = 150.0                       # tubo 2½" × 1/4" (hembra arriba)
AM_ESPIGA = 230.0
AM_ESPIGA_DENTRO = 120.0
AM_DISCO_D, AM_DISCO_T = 160.0, 12.7
AM_HUECOS, AM_PCD, AM_D = 8, 116.0, 22.0
AM_DISCOS_Z = (22.0, 128.0)             # centro de cada disco, desde la punta de arriba


def huecos_circulo(n, pcd, d, desfase=22.5, pref="R"):
    return [(f"{pref}{i + 1}", round(pcd / 2 * math.cos(math.radians(desfase + 360 / n * i)), 1),
             round(pcd / 2 * math.sin(math.radians(desfase + 360 / n * i)), 1), d, "Mosquetón")
            for i in range(n)]


# ------------------------------------------------------------------ alturas
def largo_pata(n_ext, hueco):
    """Distancia a lo largo de la pata desde la boca del casquillo hasta la punta del pie."""
    p = PI_HUECOS[hueco - 1]
    fuera = PI_L - (PE_HUECO_BOCA + p)              # pata de adentro que queda afuera
    return n_ext * PE_TUBO + fuera + (PIE_CAS_L - ESPIGA_DENTRO) - GARRA_PUNTA


def altura(n_ext, hueco, incl=0.0):
    """Altura vertical del suelo al centro de la barra de carga B."""
    L = largo_pata(n_ext, hueco)
    _, yb = eje(1, CAS_L)
    return (L * CA - yb) * math.cos(math.radians(incl))


def abertura(n_ext, hueco):
    L = largo_pata(n_ext, hueco)
    xb, _ = eje(1, CAS_L)
    return 2 * (xb + L * SA)


def expuestos(hueco):
    return len(PI_HUECOS) - hueco
