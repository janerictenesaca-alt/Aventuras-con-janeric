"""Trípode tipo Arizona Vortex, versión 7: copia de la cabeza A-frame y de la gin pole hecha con PLACAS DE
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

# ------------------------------------------------------------------ 04 placa trasera central (x, z)
SILLA_Z = 96.0                    # fondo de la silla de arriba (paso de cuerda)
TRASERA_TOPE = 104.0              # alto de la placa trasera en sus bordes (deja girar la gin pole)


def placa_trasera():
    w = X_ALETA_INT
    p = box(-w, 0, w, TRASERA_TOPE)
    r = (w ** 2 + (TRASERA_TOPE - SILLA_Z) ** 2) / (2 * (TRASERA_TOPE - SILLA_Z))
    p = p.difference(Point(0, SILLA_Z + r).buffer(r, quad_segs=96))
    ventana_sup = box(-22, 54, 22, 84).buffer(-9, quad_segs=8).buffer(9, quad_segs=16)
    return Polygon(p.exterior).simplify(0.02), [ventana_sup, corazon()]


TRASERA = placa_trasera()


# ------------------------------------------------------------------ 05 placa de fondo central (x, y)
def placa_fondo():
    p = box(-X_ALETA_INT, Y_TRASERA[1], X_ALETA_INT, Y_FRENTE[0])
    return p, [("C", *C_HUECO, D_MOSQ)]


FONDO = placa_fondo()


# ------------------------------------------------------------------ 06 escuadra lateral (x, y), arriba, une aleta de afuera con el tubo
ESC_Z = (ALETA_TOPE - T, ALETA_TOPE)


def escuadra():
    """Placa horizontal de z = 102 a 112, de la aleta de afuera (x = 74) al tubo. Lado derecho (x > 0)."""
    zc = sum(ESC_Z) / 2
    s = (ZT - zc) / CA                                  # punto del eje a esa altura
    xa = XC + s * SA
    ex = CAS_OD / 2 / CA + (T / 2) * SA / CA                      # la placa corta el tubo inclinado: +2,5 por el grosor
    elipse = sscale(Point(xa, 0).buffer(CAS_OD / 2, quad_segs=64), ex / (CAS_OD / 2), 1.0, origin=(xa, 0))
    p = Polygon([(X_ALETA_EXT + T, Y_FRENTE[0]), (xa, Y_FRENTE[0]), (xa, -26.0), (X_ALETA_EXT + T, -30.0)])
    p = p.difference(elipse.buffer(0.4, quad_segs=16))
    p = [g for g in getattr(p, "geoms", [p]) if g.area > 50][0]
    return Polygon(p.exterior).simplify(0.02)


ESCUADRA = escuadra()

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
