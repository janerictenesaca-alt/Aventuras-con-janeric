"""Trípode tipo Arizona Vortex, versión 9: copia de la cabeza A-frame y de la gin pole hecha con PLACAS DE
CORTE LÁSER de 10 mm soldadas con TIG. Medidas sacadas de las fotos y de los dibujos del manual del Vortex.

Cabeza A-frame · ejes: X = ancho, Y = fondo (la cara lisa mira a +Y), Z = alto. Z = 0 es el borde de abajo
de la placa frontal. Todas las medidas en mm.
Medidas generales: 417 de ancho × 165 de alto × 98 de fondo (igual al Vortex).
"""
import math

from shapely.affinity import translate, rotate as srot, scale as sscale
from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union

T = 12.7                          # plancha de aluminio 6061-T6 de 1/2" (12,7 mm): aletas, puente, gin pole, discos
T_FR = 15.875                     # placa frontal 01: 5/8" (15,9 mm)
ANG = 26.5                        # cada casquillo a 26,5° de la vertical (medido en el dibujo del manual)
SA, CA = math.sin(math.radians(ANG)), math.cos(math.radians(ANG))
XC, ZT = 111.8, 142.7             # centro de la boca de arriba de cada casquillo
CAS_OD, CAS_ID, CAS_L = 63.5, 51.4, 153.0
D12 = 13.1                        # hueco para pasador de cabeza 1/2"
D38 = 9.9                         # hueco para pasador de pata 3/8"
D_MOSQ = 22.0                     # hueco para mosquetón

# posiciones en X (cara de adentro de cada placa; la placa ocupa x … x+T)
X_ALETA_INT = 33.3                # aletas de adentro: |x| = 33,3 … 46
X_ALETA_EXT = 64.0                # aletas de afuera:  |x| = 64 … 76,7 (ranura de 18 entre las dos)
X_RANURA = (X_ALETA_INT + T + X_ALETA_EXT) / 2        # 55: centro de la ranura (orejas de la gin pole)
Y_FRENTE = (22.0 - T_FR, 22.0)    # placa frontal: y = 6,1 … 22 (la cara lisa en y = 22)
Y_ATRAS = -66.0                   # las aletas llegan hasta y = −66  (fondo total 22 + 66 + … = 98 con el tubo)
Y_TRASERA = (-66.0, -56.0)        # placa trasera central
Z_FONDO = (0.0, 10.0)             # placa de fondo central
PIN_Y = -46.0
PIN_ARRIBA = (PIN_Y, 92.0)        # I1: pasador de arriba (también bisagra de la gin pole)
PIN_ABAJO = (PIN_Y, 20.0)         # I2: pasador de abajo (polea / amarres)
ALETA_TOPE = 110.0


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
OFF_BORDE = round(math.sqrt((CAS_OD / 2) ** 2 - Y_FRENTE[0] ** 2) + 0.1, 2)                  # el borde lateral toca el tubo en la cara de atrás: adelante queda una V para soldar


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


D_DOBLE = 25.0                    # 2 huecos para mosquetón grande (reemplazan el corazón)
X_DOBLE, Z_DOBLE = 19.0, 28.0


def huecos_dobles():
    return [Point(sx * X_DOBLE, Z_DOBLE).buffer(D_DOBLE / 2, quad_segs=64) for sx in (-1, 1)]


def cortes_frontal():
    return [ventana(-1), ventana(1)] + huecos_dobles()


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
C_HUECO = (0.0, -20.0)            # hueco C (x, y)
C_BORDE = 14.0                    # metal alrededor del hueco C hacia atrás
PUENTE_Y = (C_HUECO[1] - D_MOSQ / 2 - C_BORDE, Y_FRENTE[0])


def puente_central():
    """Placa acostada entre las aletas de adentro, con el hueco C. Borde de atrás redondo alrededor del hueco."""
    r = D_MOSQ / 2 + C_BORDE
    p = unary_union([box(-X_ALETA_INT, C_HUECO[1], X_ALETA_INT, Y_FRENTE[0]), Point(*C_HUECO).buffer(r, quad_segs=64),
                     Polygon([(-X_ALETA_INT, C_HUECO[1]), (X_ALETA_INT, C_HUECO[1]), (r, C_HUECO[1] - 6), (-r, C_HUECO[1] - 6)])])
    p = p.intersection(box(-X_ALETA_INT, -200, X_ALETA_INT, Y_FRENTE[0])).buffer(3, quad_segs=8).buffer(-3, quad_segs=8)
    p = p.intersection(box(-X_ALETA_INT, -200, X_ALETA_INT, Y_FRENTE[0]))
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
PIE_L = 215.0                     # 60 de garra adentro + 152 del macho + 3 de luz
# carrete (15 naranja, 16 azul)
CAR_DISCO = 172.0
CAR_PCD = 122.0
CAR_HUECO = 24.0
CAR_CHICO = 10.0
CAR_ALTO_N = 2 * 63.5  # 127: alto total del naranja (simétrico: sirve de pie o de cabeza)
CAR_ALTO_A = 63.5 + (63.5 + 27.94) - T   # 142,2: alto total del azul (luz 129,5 entre discos: cabe la gin pole de lado)
CAR_N_ALTO = CAR_ALTO_N - T     # tubo naranja bajo el disco
CAR_A_ALTO = CAR_ALTO_A - T     # tubo azul sobre el disco
CAR_A_OD = 73.0
CAR_HUECOS = [H_BOCA - VERNIER, H_BOCA, H_BOCA + VERNIER]   # 35,6 · 63,5 · 91,4 desde la cara del disco
CAR_HUECOS_A2 = [CAR_ALTO_A - h for h in CAR_HUECOS]      # fila 2 del azul (a 90°): 35,6 · 63,5 · 91,4 desde la boca del tubo


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

# ------------------------------------------------------------------ 17 AHP v9 (poste de enganche del carro), acero A36 12,7 mm, soldado
AHP_T = 12.7
AHP_U = 52.0                       # luz entre brazos: entra la pata de adentro Ø 50,8
AHP_BRAZO_L = 150.0                # largo de los brazos (y = 0 … 150)
AHP_PIN = (24.0, 0.0)              # (y, z) del pasador 3/8" en los brazos
AHP_YUGO_Y = (AHP_BRAZO_L, AHP_BRAZO_L + AHP_T)
AHP_TUBO = (50.8, 6.35, 300.0)     # espiga de tubo cuadrado 2" × 1/4" que entra en el enganche
AHP_Z_ABAJO = -52.7                # cara de abajo de la placa de anclajes


def ahp_brazo():
    """17c: brazo (y, z). Punta redonda con el hueco del pasador."""
    p = unary_union([box(AHP_PIN[0], -40, AHP_BRAZO_L, 25.4), Point(*AHP_PIN).buffer(32, quad_segs=48)])
    p = p.intersection(box(-20, -40, AHP_BRAZO_L, 25.4)).buffer(4, quad_segs=8).buffer(-4, quad_segs=8)
    return Polygon(p.exterior).simplify(0.02), [("P", *AHP_PIN, D38)]


def ahp_yugo():
    """17b: placa en C / yugo (x, z): une los 2 brazos y recibe la espiga cuadrada."""
    p = box(-80, AHP_Z_ABAJO, 80, 25.4).buffer(-6, quad_segs=8).buffer(6, quad_segs=8)
    return Polygon(p.exterior).simplify(0.02), []


def ahp_anclajes():
    """17d: placa de anclajes (x, y), abajo de los brazos: 4 huecos Ø 25 para mosquetón."""
    p = box(-98, 40, 98, AHP_YUGO_Y[0]).difference(box(-AHP_U / 2 - 6, 0, AHP_U / 2 + 6, 100))
    p = p.buffer(-8, quad_segs=8).buffer(8, quad_segs=12).buffer(4, quad_segs=8).buffer(-4, quad_segs=8)
    p = unary_union([p, box(-98, AHP_YUGO_Y[0] - 20, 98, AHP_YUGO_Y[0])]).intersection(box(-98, 40, 98, AHP_YUGO_Y[0]))
    hs = [(f"A{i + 1}", sx * 72.0, y, 25.0) for i, (sx, y) in enumerate(((-1, 70.0), (-1, 118.0), (1, 70.0), (1, 118.0)))]
    return Polygon(p.exterior).simplify(0.02), hs


def ahp_cartela():
    """17e: alma de la T (y, z): baja del tubo cuadrado a la placa de anclajes, detrás del yugo."""
    y0 = AHP_YUGO_Y[1]
    p = Polygon([(y0, AHP_Z_ABAJO), (y0, -25.4), (y0 + 170, -25.4), (y0 + 30, AHP_Z_ABAJO)])
    return p, []


def ahp_argolla():
    """17f: argolla inclinada (u, v) que va soldada al costado de cada brazo; hueco Ø 22 para maniota."""
    p = unary_union([box(0, -24, 34, 24), Point(34, 0).buffer(24, quad_segs=48)])
    return Polygon(p.exterior).simplify(0.02), [("M", 34.0, 0.0, 22.0)]


AHP_PIEZAS = {"17b": ahp_yugo(), "17c": ahp_brazo(), "17d": ahp_anclajes(), "17e": ahp_cartela(), "17f": ahp_argolla()}

# ------------------------------------------------------------------ 18 pie plano con rótula (bola de enganche 2")
ROT_BOLA = 50.8
ROT_BASE = (250.0, 120.0, 10.0)    # base A36: largo × ancho × grosor


def rot_base():
    L, W, _ = ROT_BASE
    p = box(-L / 2, -W / 2, L / 2, W / 2).buffer(-14, quad_segs=8).buffer(14, quad_segs=12)
    hs = [(f"F{i + 1}", sx * 62.0, sy * 40.0, 14.0) for i, (sx, sy) in enumerate(((-1, -1), (1, -1), (1, 1), (-1, 1)))]
    hs += [("M1", -100.0, 0.0, 25.0), ("M2", 100.0, 0.0, 25.0)]
    return Polygon(p.exterior).simplify(0.02), hs


def rot_anillo():
    p = Point(0, 0).buffer(55, quad_segs=96)
    hs = [(f"T{i + 1}", round(45 * math.cos(math.radians(22.5 + 45 * i)), 2), round(45 * math.sin(math.radians(22.5 + 45 * i)), 2), 8.6)
          for i in range(8)]
    return Polygon(p.exterior).simplify(0.02), hs, [Point(0, 0).buffer(22, quad_segs=96)]


# ------------------------------------------------------------------ gin pole (ejes propios, origen en el pasador de bisagra)
# X igual a la cabeza; −Y se aleja de la cabeza A-frame; Z arriba (con la gin pole horizontal).
GP_ALA_Z = (10.0, 10.0 + T)       # el ala queda de z = 10 a 22,7
GP_OREJA_X = (X_RANURA - T / 2, X_RANURA + T / 2)     # orejas de x = 48,65 a 61,35 (entran en la ranura de 18)
GP_PUNTA = 16.0                   # la oreja pasa 16 más allá del pasador
GP_LARGO = 257.0                  # largo total (punta alargada 45 mm para el hueco de anclaje P)
GP_ANCHO = 150.0                  # ancho del ala: ≥ 12 mm de metal alrededor de cada hueco de mosquetón
GP_TUBO_Y = -147.0                # el eje del tubo cruza la cara de abajo del ala (z = 10) en y = −147
GP_TUBO_L = 140.0
GP_TUBO_ARRIBA = 8.0              # el tubo sobresale 8 sobre el ala
GP_ALFA = 25.0                    # inclinación del tubo respecto a la vertical del ala (se recalcula en v7_build)
CART_X = (12.0, 12.0 + T)         # cartelas a cada lado del tubo: |x| = 12 … 24,7
OREJA_ATRAS = -110.0              # las orejas siguen 110 mm bajo el ala
RANURA_ALA = (-55.0, -35.0)       # ranura en el ala donde pasa la lengüeta de cada oreja
D_PUNTA = 22.0


def tubo_y(z, alfa):
    """y del eje del tubo de la gin pole a la altura z (el tubo baja alejándose de la cabeza)."""
    return GP_TUBO_Y + (z - GP_ALA_Z[0]) * math.tan(math.radians(alfa))


def perfil_ala(alfa=GP_ALFA):
    """Ala (escudo) de la gin pole en (x, y): 4 óvalos D, hueco P en la punta, hueco elíptico del tubo, 2 ranuras de encastre."""
    a = GP_ANCHO / 2
    ta, ca = math.tan(math.radians(alfa)), math.cos(math.radians(alfa))
    yc = tubo_y(sum(GP_ALA_Z) / 2, alfa)
    ry = (CAS_OD / 2 + 0.3) / ca + (T / 2) * ta
    y_fin = GP_PUNTA - GP_LARGO                                # −241: punta de atrás
    y_ini = -23.0
    p = Polygon([(-26, y_fin), (26, y_fin), (a, y_fin + 60), (a, y_ini - 13), (a - 13, y_ini), (13 - a, y_ini), (-a, y_ini - 13),
                 (-a, y_fin + 60)])                                # chaflán 13 × 45° adelante: la gin pole cabe de lado entre los discos
    p = p.buffer(-8, quad_segs=8).buffer(8, quad_segs=16)
    e0 = sscale(Point(0, yc).buffer(CAS_OD / 2 + 0.3, quad_segs=96), 1.0, 1.0 / ca, origin=(0, yc))
    tubo = unary_union([translate(e0, 0, s * (T / 2) * ta) for s in (-1, 1)]).convex_hull     # largo total = 2·ry
    cortes = []
    for sx in (-1, 1):
        cortes.append(LineString([(sx * 53.5, yc + 18), (sx * 53.5, yc + 34)]).buffer(9.0, quad_segs=24))
        o2 = LineString([(sx * 36.0, yc + 62), (sx * 36.0, yc + 74)]).buffer(10.5, quad_segs=24)
        cortes.append(srot(o2, sx * 55, origin=(sx * 36.0, yc + 68)))
    cortes.append(Point(0, y_fin + D_PUNTA / 2 + 12.0).buffer(D_PUNTA / 2, quad_segs=48))       # P: anclaje de la punta
    ranuras = [box(GP_OREJA_X[0] - 0.2, RANURA_ALA[0] - 0.2, GP_OREJA_X[1] + 0.2, RANURA_ALA[1] + 0.2),
               box(-GP_OREJA_X[1] - 0.2, RANURA_ALA[0] - 0.2, -GP_OREJA_X[0] + 0.2, RANURA_ALA[1] + 0.2)]
    return Polygon(p.exterior).simplify(0.02), cortes + ranuras, tubo


def perfil_oreja():
    """Oreja (C) de la gin pole en (y, z): lengüeta que atraviesa el ala + cuerpo largo bajo el ala + ojo del pasador 1/2"."""
    zt = GP_ALA_Z[1]
    cuerpo = Polygon([(0, -16), (0, 16), (-23, 16), (-23, GP_ALA_Z[0]), (OREJA_ATRAS, GP_ALA_Z[0]), (OREJA_ATRAS, GP_ALA_Z[0] - 10),
                      (-40, -16)])
    p = unary_union([cuerpo, Point(0, 0).buffer(16, quad_segs=48)])
    p = p.buffer(1.5, quad_segs=8).buffer(-1.5, quad_segs=8).difference(box(-400, GP_ALA_Z[0], -23, 100))
    p = unary_union([p, box(RANURA_ALA[0], GP_ALA_Z[0] - 1, RANURA_ALA[1], zt)])            # lengüeta que atraviesa el ala
    return Polygon(p.exterior).simplify(0.02), [("C", 0.0, 0.0, D12)]


OREJA = perfil_oreja()


def perfil_ojo():
    """B: ojo central de la gin pole (x, z), placa colgada bajo el ala, hueco para mosquetón."""
    zc = -24.0
    p = unary_union([Point(0, zc).buffer(22, quad_segs=48), box(-22, zc, 22, GP_ALA_Z[0])])
    p = p.buffer(-3, quad_segs=8).buffer(3, quad_segs=8)
    return Polygon(p.exterior).simplify(0.02), [("B", 0.0, zc, 25.0)]


OJO = perfil_ojo()
GP_OJO_Y = (-40.0, -40.0 + T)     # el ojo va de y = −40 a −27,3 (atrás de la cabeza A-frame)


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
