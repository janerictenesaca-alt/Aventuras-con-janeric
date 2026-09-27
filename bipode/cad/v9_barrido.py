"""Barrido del giro de la gin pole (plano y-z) para ubicar el puente central sin choques."""
import math

from shapely.affinity import rotate as srot, translate as stra
from shapely.geometry import Polygon, box
from shapely.ops import unary_union


def formas_gin(g, alfa, gp_bajo=115.0):
    """Siluetas (y, z) de las piezas de la gin pole en sus coordenadas, con el rango de x que ocupan."""
    a = math.radians(alfa)
    d = (-math.sin(a), -math.cos(a))
    n = (math.cos(a), -math.sin(a))
    r = g.CAS_OD / 2
    zc = g.GP_ALA_Z[1] + g.GP_TUBO_ARRIBA
    pts = []
    for k in (1, -1):
        p = (g.GP_TUBO_Y + k * r * n[0], g.GP_ALA_Z[0] + k * r * n[1])
        t_top = (zc - p[1]) / (-d[1])
        pts.append(((p[0] - t_top * d[0], zc), (p[0] + gp_bajo * d[0], p[1] + gp_bajo * d[1])))
    tubo = Polygon([pts[0][0], pts[0][1], pts[1][1], pts[1][0]])
    ojo_z = g.OJO[0].bounds[1]
    return [
        ("ala", box(g.GP_PUNTA - g.GP_LARGO, g.GP_ALA_Z[0], -23.0, g.GP_ALA_Z[1]), (0.0, g.GP_ANCHO / 2)),
        ("ojo", box(g.GP_OJO_Y[0], ojo_z, g.GP_OJO_Y[1], g.GP_ALA_Z[0]), (0.0, 22.0)),
        ("cartela", g.perfil_cartela(alfa), g.CART_X),
        ("tubo", tubo, (0.0, r)),
    ]


def barrido(g, alfa, phi0_deg, paso=1.0, maximo=80.0):
    """Gira la gin pole desde phi0 hacia la cabeza (se junta la pata). Devuelve el giro máximo antes de tocar
    aletas o placa frontal, y la z más baja que alcanza cada pieza sobre la zona del puente (|x| < aleta de adentro)."""
    hy, hz = g.PIN_ARRIBA
    aleta = g.ALETA[0]
    frente = box(g.Y_FRENTE[0], 0, g.Y_FRENTE[1], 130)
    zona = box(g.PUENTE_Y[0] - 2, -50, g.PUENTE_Y[1], 200)
    formas = formas_gin(g, alfa)
    zmin, tope = 1e9, None
    th = 0.0
    while th <= maximo:
        ph = phi0_deg + th
        choque = False
        for nom, f, (x0, x1) in formas:
            w = stra(srot(f, ph, origin=(0, 0)), hy, hz)
            if w.intersects(frente) or (x1 > g.X_ALETA_INT and x0 < g.X_ALETA_EXT + g.T and w.intersects(aleta)):
                choque = True
                tope = (th, nom)
                break
            if x0 < g.X_ALETA_INT:
                s = w.intersection(zona)
                if not s.is_empty:
                    zmin = min(zmin, s.bounds[1])
        if choque:
            break
        th += paso
    return tope, zmin
