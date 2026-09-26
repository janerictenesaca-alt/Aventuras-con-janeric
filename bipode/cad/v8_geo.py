"""Trípode tipo Arizona Vortex, versión 8: copia de la cabeza A-frame y de la gin pole hecha con PLACAS DE
CORTE LÁSER de 10 mm soldadas con TIG. Medidas sacadas de las fotos y de los dibujos del manual del Vortex.

Cabeza A-frame · ejes: X = ancho, Y = fondo (la cara lisa mira a +Y), Z = alto. Z = 0 es el borde de abajo
de la placa frontal. Todas las medidas en mm.
Medidas generales: 417 de ancho × 165 de alto × 98 de fondo (igual al Vortex).
"""
import math

from shapely.affinity import rotate as srot, scale as sscale
from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union

T = 10.0                          # plancha de aluminio 6061-T6 de 10 mm (todas las placas)
ANG = 26.5                        # cada casquillo a 26,5° de la vertical (medido en el dibujo del manual)
SA, CA = math.sin(math.radians(ANG)), math.cos(math.radians(ANG))
XC, ZT = 111.8, 142.7             # centro de la boca de arriba de cada casquillo
CAS_OD, CAS_ID, CAS_L = 63.5, 51.4, 153.0
D12 = 13.1                        # hueco para pasador de cabeza 1/2"
D38 = 9.9                         # hueco para pasador de pata 3/8"
D_MOSQ = 22.0                     # hueco para mosquetón

# posiciones en X (cara de adentro de cada placa; la placa ocupa x … x+T)
X_ALETA_INT = 36.0                # aletas de adentro: |x| = 36 … 46
X_ALETA_EXT = 64.0                # aletas de afuera:  |x| = 64 … 74   (ranura de 18 entre las dos)
X_RANURA = (X_ALETA_INT + T + X_ALETA_EXT) / 2        # 55: centro de la ranura (orejas de la gin pole)
Y_FRENTE = (12.0, 22.0)           # placa frontal: y = 12 … 22 (la cara lisa en y = 22)
Y_ATRAS = -66.0                   # las aletas llegan hasta y = −66  (fondo total 22 + 66 + … = 98 con el tubo)
Y_TRASERA = (-66.0, -56.0)        # placa trasera central
Z_FONDO = (0.0, 10.0)             # placa de fondo central
PIN_Y = -46.0
PIN_ARRIBA = (PIN_Y, 92.0)        # I1: pasador de arriba (también bisagra de la gin pole)
PIN_ABAJO = (PIN_Y, 20.0)         # I2: pasador de abajo (polea / amarres)
ALETA_TOPE = 110.0
C_HUECO = (0.0, -22.0)            # C: unión central vertical, en la placa de fondo (x, y)


def eje(lado, s, off=0.0):
    """Punto (x, z) sobre el eje del casquillo; s desde la boca de arriba hacia abajo; off > 0 hacia afuera."""
    x = XC + s * SA + off * CA
    z = ZT - s * CA + off * SA
    return (lado * x, z)


def alto(pz):
    """Alto total de la cabeza (de la esquina de abajo del tubo a la de arriba)."""
    return pz


# ------------------------------------------------------------------ 01 placa frontal (cara lisa)
ARCO_R, ARCO_Z = 500.0, 608.0     # borde de arriba cóncavo: 108 al centro, 116 junto a los tubos
OFF_BORDE = 29.5                  # el borde lateral toca el tubo en la cara de atrás: adelante queda una V para soldar


def placa_frontal():
    tr = Polygon([eje(-1, -30, -OFF_BORDE), eje(-1, CAS_L + 20, -OFF_BORDE),
                  eje(1, CAS_L + 20, -OFF_BORDE), eje(1, -30, -OFF_BORDE)])
    p = tr.intersection(box(-400, 0, 400, 300))
    p = p.difference(Point(0, ARCO_Z).buffer(ARCO_R, quad_segs=128))
    for sx in (-1, 1):
        p = p.difference(Point(sx * X_RANURA, 0.0).buffer(9.0, quad_segs=32))      # muescas de abajo (canal D)
    p = p.buffer(2, quad_segs=8).buffer(-2, quad_segs=8)
    return Polygon(p.exterior).simplify(0.02)


def ventana(lado):
    """E: ventana triangular redondeada (anclaje izquierdo / derecho)."""
    c = [Point(lado * 87.5, 72.0).buffer(5.5, quad_segs=24), Point(lado * 89.0, 28.0).buffer(7.0, quad_segs=24),
         Point(lado * 111.0, 28.0).buffer(7.0, quad_segs=24)]
    return unary_union(c).convex_hull


def corazon():
    """B: hueco central en forma de corazón (atraviesa placa frontal y placa trasera)."""
    c = unary_union([Point(-8.0, 32.0).buffer(8.5, quad_segs=24), Point(8.0, 32.0).buffer(8.5, quad_segs=24),
                     Polygon([(-16.2, 30.0), (16.2, 30.0), (0.0, 9.0)])])
    return c.buffer(1.8, quad_segs=8).buffer(-3.0, quad_segs=8).buffer(1.2, quad_segs=8)


def cortes_frontal():
    return [ventana(-1), ventana(1), corazon()]


def alto_frontal(x):
    return ARCO_Z - math.sqrt(ARCO_R ** 2 - x ** 2)


# ------------------------------------------------------------------ 03 aleta (4 iguales, perfil en y, z)
def perfil_aleta():
    yb = PIN_Y
    p = box(Y_ATRAS - 5, Z_FONDO[0], Y_FRENTE[0], ALETA_TOPE)
    # esquinas de atrás redondeadas con centro en cada pasador (R 20)
    quitar = unary_union([box(Y_ATRAS - 10, ALETA_TOPE - 20, yb, ALETA_TOPE + 10),
                          box(Y_ATRAS - 10, -10, yb, PIN_ABAJO[1]),
                          box(Y_ATRAS - 10, -10, Y_ATRAS, 200)])
    p = p.difference(quitar).union(Point(PIN_Y, ALETA_TOPE - 20).buffer(20, quad_segs=48).intersection(box(-200, 0, 200, 200))) \
        .union(Point(*PIN_ABAJO).buffer(20, quad_segs=48).intersection(box(-200, 0, 200, 200))) \
        .intersection(box(Y_ATRAS, 0, Y_FRENTE[0], ALETA_TOPE))
    p = p.union(box(Y_ATRAS, PIN_ABAJO[1], PIN_Y, ALETA_TOPE - 20))
    p = p.buffer(1, quad_segs=8).buffer(-1, quad_segs=8)
    huecos = [("I1", *PIN_ARRIBA, D12), ("I2", *PIN_ABAJO, D12)]
    return Polygon(p.exterior).simplify(0.02), huecos


ALETA = perfil_aleta()

# ------------------------------------------------------------------ 04 puente central (x, y): chico, abierto atrás (como el Vortex)
PUENTE_Y = (-58.0, Y_FRENTE[0])   # de la placa 01 hacia atrás; el centro de atrás queda ABIERTO (U entre aletas)


def puente_central():
    """Placa acostada abajo (z = 0 … 10) entre las aletas de adentro, con el hueco C. Borde de atrás redondo."""
    p = unary_union([box(-X_ALETA_INT, C_HUECO[1], X_ALETA_INT, Y_FRENTE[0]),
                     Point(*C_HUECO).buffer(X_ALETA_INT, quad_segs=64)]).intersection(box(-X_ALETA_INT, -200, X_ALETA_INT, Y_FRENTE[0]))
    return Polygon(p.exterior).simplify(0.02), [("C", *C_HUECO, D_MOSQ)]


PUENTE = puente_central()

# ------------------------------------------------------------------ REGLA DE HUECOS (igual para todo el sistema)
H_BOCA = 63.5          # todo hueco de pasador 3/8" queda a 63,5 (2½") de la boca de su casquillo / hembra
PASO = 139.7           # paso entre huecos de la pata de adentro (5½")
VERNIER = PASO / 5     # 27,94: huecos de ajuste fino en casquillos y carretes
D_PATA = 50.8          # pata de adentro y macho de la pata de afuera (2")
D_BOCA = 51.4          # interior de todas las bocas que reciben Ø 50,8
D_AFUERA = 60.3        # pata de afuera (2" céd. 40), casquillo del pie y tubo del carrete naranja
D_AZUL = 61.0          # interior del tubo del carrete azul (recibe Ø 60,3)
# pata de afuera (10 + 11 + 12)
PA_CUERPO = 902.0      # cuerpo 2" céd. 40 (Ø 60,3 × 3,91, interior 52,5)
PA_MACHO = 152.0       # la espiga sale 152 del cuerpo (escalón)
PA_ESPIGA_DENTRO = 120.0
PA_ESPIGA = PA_MACHO + PA_ESPIGA_DENTRO                  # 272
PA_HUECO_MACHO = PA_MACHO - H_BOCA                       # 88,5 desde la punta del macho
PA_REMACHES = (34.0, 94.0)                               # pernos fijos de la espiga, desde el escalón hacia el cuerpo
PA_TOTAL = PA_CUERPO + PA_MACHO                          # 1054 (Vortex 1054)
# pata de adentro (13)
PI_L = 2 * H_BOCA + 6 * PASO                             # 965,2
PI_HUECOS = [H_BOCA + k * PASO for k in range(7)]        # 63,5 … 901,7 (simétrica)
# pie de flecha (14)
PIE_L = 140.0
# carrete (15 naranja, 16 azul)
CAR_DISCO = 165.0
CAR_PCD = 118.0
CAR_HUECO = 24.0
CAR_CHICO = 10.0
CAR_N_ALTO = 100.0     # tubo naranja bajo el disco
CAR_A_ALTO = 107.0     # tubo azul sobre el disco
CAR_A_OD = 73.0
CAR_HUECOS = [H_BOCA - VERNIER, H_BOCA, H_BOCA + VERNIER]   # 35,6 · 63,5 · 91,4 desde la cara del disco


def disco_carrete(naranja):
    """Disco del carrete (x, y): 9 huecos de anclaje + 1 hueco chico arriba, centro con o sin llave."""
    p = Point(0, 0).buffer(CAR_DISCO / 2, quad_segs=128)
    huecos = []
    for i in range(10):
        a = math.radians(90 + 36 * i)
        x, y = CAR_PCD / 2 * math.cos(a), CAR_PCD / 2 * math.sin(a)
        huecos.append(("S" if i == 0 else f"D{i}", round(x, 2), round(y, 2), CAR_CHICO if i == 0 else CAR_HUECO))
    if naranja:
        centro = unary_union([Point(0, 0).buffer(D_BOCA / 2, quad_segs=96),
                              box(-5.25, 0, 5.25, D_AFUERA / 2 + 1.0), box(-5.25, -(D_AFUERA / 2 + 1.0), 5.25, 0)])
        centro = centro.buffer(0.8, quad_segs=8).buffer(-0.8, quad_segs=8)
    else:
        centro = Point(0, 0).buffer(D_AZUL / 2, quad_segs=96)
    return Polygon(p.exterior).simplify(0.02), huecos, [centro]


CAR_N = disco_carrete(True)
CAR_A = disco_carrete(False)

# ------------------------------------------------------------------ AHP (poste para el enganche del carro), placa de 25,4 mm
AHP_T = 25.4
AHP_U = 52.0           # ancho de la U (pata Ø 50,8)
AHP_PIN_Y = 24.0       # pasador 3/8" que cruza las puntas de la U (a 24 de la punta)


def perfil_ahp():
    u, w = AHP_U / 2, 30.0
    horq = unary_union([box(-u - w, 12, -u, 150), box(u, 12, u + w, 150),
                        Point(-u - w / 2, 12).buffer(w / 2, quad_segs=32), Point(u + w / 2, 12).buffer(w / 2, quad_segs=32)])
    cuerpo = Polygon([(-96, 150), (96, 150), (96, 232), (70, 262), (27, 262), (27, 380), (-27, 380), (-27, 262), (-70, 262), (-96, 232)])
    orejas = [box(sx * (u + w) - (30 if sx < 0 else 0), 62, sx * (u + w) + (0 if sx < 0 else 30), 100) for sx in (-1, 1)]
    p = unary_union([horq, cuerpo] + orejas)
    for sx in (-1, 1):                                   # bordes ondulados entre los 2 huecos de cada lado
        p = p.difference(Point(sx * 104, 192, ).buffer(12, quad_segs=24))
    p = p.buffer(4, quad_segs=12).buffer(-8, quad_segs=12).buffer(4, quad_segs=12)
    huecos = [("A1", -66.0, 170.0, 25.0), ("A2", -66.0, 214.0, 25.0), ("A3", 66.0, 170.0, 25.0), ("A4", 66.0, 214.0, 25.0),
              ("E", 0.0, 350.0, 16.5)]
    cortes = [LineString([(sx * (u + w + 12), 81), (sx * (u + w + 20), 81)]).buffer(8, quad_segs=16) for sx in (-1, 1)]
    return Polygon(p.exterior).simplify(0.02), huecos, cortes


AHP = perfil_ahp()

# ------------------------------------------------------------------ gin pole (ejes propios, origen en el pasador de bisagra)
# X igual a la cabeza; −Y se aleja de la cabeza A-frame; Z arriba (con la gin pole horizontal).
GP_ALA_Z = (10.0, 20.0)           # el ala queda de z = 10 a 20 (su cara de arriba al ras con las aletas)
GP_OREJA_X = (X_RANURA - T / 2, X_RANURA + T / 2)     # orejas de x = 50 a 60 (entran en la ranura de 18)
GP_PUNTA = 16.0                   # la oreja pasa 16 más allá del pasador
GP_LARGO = 212.0                  # largo total del ala + orejas (Vortex 212)
GP_ANCHO = 135.0                  # ancho del ala (Vortex 127; +8 para que los huecos D queden con buen borde)
GP_TUBO_Y = -147.0                # el eje del tubo cruza la cara de abajo del ala (z = 10) en y = −147
GP_TUBO_L = 140.0
GP_TUBO_ARRIBA = 8.0              # el tubo sobresale 8 sobre el ala
GP_ALFA = 25.0                    # inclinación del tubo respecto a la vertical del ala (se recalcula en v7_build)
CART_X = (12.0, 22.0)             # cartelas a cada lado del tubo: |x| = 12 … 22


def tubo_y(z, alfa):
    """y del eje del tubo de la gin pole a la altura z (el tubo baja alejándose de la cabeza)."""
    return GP_TUBO_Y + (z - GP_ALA_Z[0]) * math.tan(math.radians(alfa))


def perfil_ala(alfa=GP_ALFA):
    """Ala (escudo) de la gin pole en (x, y): 4 huecos D (anclajes radiales) y hueco elíptico del tubo."""
    a = GP_ANCHO / 2
    ta, ca = math.tan(math.radians(alfa)), math.cos(math.radians(alfa))
    yc = tubo_y(sum(GP_ALA_Z) / 2, alfa)
    ry = (CAS_OD / 2 + 0.3) / ca + (T / 2) * ta               # el tubo pasa inclinado por los 10 mm del ala
    y_fin = GP_PUNTA - GP_LARGO                                # −196: punta de atrás
    y_ini = -23.0                                              # borde de adelante del ala (entre orejas)
    p = Polygon([(-16, y_fin), (16, y_fin), (a, y_fin + 44), (a, -74), (GP_OREJA_X[1], -52), (GP_OREJA_X[1], y_ini),
                 (-GP_OREJA_X[1], y_ini), (-GP_OREJA_X[1], -52), (-a, -74), (-a, y_fin + 44)])
    p = p.buffer(-8, quad_segs=8).buffer(8, quad_segs=16)
    tubo = sscale(Point(0, yc).buffer(CAS_OD / 2 + 0.3, quad_segs=96), 1.0, ry / (CAS_OD / 2 + 0.3), origin=(0, yc))
    ovalos = []
    for sx in (-1, 1):
        ovalos.append(LineString([(sx * 51.0, yc + 18), (sx * 51.0, yc + 34)]).buffer(9.0, quad_segs=24))
        o2 = LineString([(sx * 42.0, yc + 58), (sx * 42.0, yc + 74)]).buffer(10.5, quad_segs=24)
        ovalos.append(srot(o2, sx * 30, origin=(sx * 42.0, yc + 66)))
    return Polygon(p.exterior).simplify(0.02), ovalos, tubo


def perfil_oreja():
    """Oreja (C) de la gin pole en (y, z): entra en la ranura entre aletas, hueco 1/2" en el origen."""
    p = unary_union([Point(0, 0).buffer(16, quad_segs=48), box(-40, -16, 0, GP_ALA_Z[0]),
                     box(-40, 0, GP_PUNTA, GP_ALA_Z[0]).intersection(Point(0, 0).buffer(16).union(box(-40, -16, 0, 20)))])
    p = p.difference(Polygon([(-40, -16), (-40, -2), (-26, -16)]))
    return Polygon(p.exterior).simplify(0.02), [("C", 0.0, 0.0, D12)]


OREJA = perfil_oreja()


def perfil_ojo():
    """B: ojo central de la gin pole (x, z), placa colgada bajo el ala, hueco para mosquetón."""
    zc = -24.0
    p = unary_union([Point(0, zc).buffer(22, quad_segs=48), box(-22, zc, 22, GP_ALA_Z[0])])
    p = p.buffer(-3, quad_segs=8).buffer(3, quad_segs=8)
    return Polygon(p.exterior).simplify(0.02), [("B", 0.0, zc, 25.0)]


OJO = perfil_ojo()
GP_OJO_Y = (-40.0, -30.0)         # el ojo va de y = −40 a −30 (atrás de la cabeza A-frame)


def perfil_cartela(alfa=GP_ALFA):
    """Cartela de la gin pole (y, z): une la cara de abajo del ala con el tubo (lado de la cabeza). 2 piezas."""
    sa, ca = math.sin(math.radians(alfa)), math.cos(math.radians(alfa))
    off = math.sqrt((CAS_OD / 2) ** 2 - CART_X[0] ** 2)       # la cara de adentro de la cartela toca el tubo

    def en_tubo(z):
        return (tubo_y(z, alfa) + off / ca, z)

    a = en_tubo(GP_ALA_Z[0])
    b = en_tubo(GP_ALA_Z[0] - 62.0 * ca)
    p = Polygon([a, (-66.0, GP_ALA_Z[0]), (-66.0, GP_ALA_Z[0] - 8), b])
    p = p.buffer(-4, quad_segs=8).buffer(4, quad_segs=8)
    return Polygon(p.exterior).simplify(0.02)
