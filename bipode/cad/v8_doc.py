"""Planos del trípode tipo Vortex v8 (placas de corte láser soldadas con TIG), A3 horizontal.

Uso:  python3 v8_doc.py <carpeta_imagenes> <carpeta_fuentes>
Salida:  ../v8/plano/index.html (para imprimir a PDF), ../v8/svg/*.svg (piezas planas a escala 1:1)
         ../v8/web/dibujos.json (dibujos para la página)
Reutiliza el estilo y el rótulo de v4_doc.py y el dibujo de v4_dibujo.py.
"""
import json
import math
import os
import sys
from html import escape

import numpy as np
from scipy.optimize import fsolve
from shapely.affinity import rotate as srot
from shapely.geometry import Point, Polygon, box

AQUI = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(AQUI, "v4_doc.py"), encoding="utf-8").read()
src = src[:src.index("# ------------------------------------------------------------------ generar")]
ns = {"__name__": "v4doc", "__file__": os.path.join(AQUI, "v4_doc.py")}
exec(compile(src, "v4_doc", "exec"), ns)

import v4_geo as g4
import v8_geo as g
from v8_dibujo import Vista, f
ns["Vista"] = Vista

img, hoja, render_hoja, CSS, vista_tubo, pulg = (ns["img"], ns["hoja"], ns["render_hoja"], ns["CSS"],
                                                  ns["vista_tubo"], ns["pulg"])
HOJAS = ns["HOJAS"]
HOJAS.clear()
ns["TITULO"] = "Trípode tipo Vortex · placas soldadas"
ns["PROY"] = "VX-EC"
ns["REV"] = "D"
ns["FECHA"] = "26-09-2026"
INDICE = []

BASE = os.path.join(AQUI, "..", "v8")
OUT = os.path.join(BASE, "plano")
for d in ("plano", "svg", "web"):
    os.makedirs(os.path.join(BASE, d), exist_ok=True)
ARM = json.load(open(os.path.join(BASE, "armado.json")))
VOL = {p["id"]: p["vol"] for p in ARM["piezas"]}
VOL.update(ARM["vol_sueltas"])
AL, AC = 2.70e-6, 7.85e-6
ALFA = ARM["alfa"]
T = g.T
WEB = {}          # dibujos para la página: id -> svg


def kg(pid, dens=AL):
    return VOL[pid] * dens


def indice(t):
    INDICE.append(t)


def guardar(nombre, vista_svg):
    WEB[nombre] = vista_svg
    return vista_svg


def svg_corte(nombre, poly, huecos=(), cortes=(), titulo=""):
    """Archivo SVG a escala 1:1 (mm) con solo el contorno de corte, para láser o para el diseñador."""
    x0, y0, x1, y1 = poly.bounds
    m = 5
    W, H = x1 - x0 + 2 * m, y1 - y0 + 2 * m

    def P(x, y):
        return f"{x - x0 + m:.3f},{y1 - y + m:.3f}"
    d = "M" + " L".join(P(x, y) for x, y in poly.exterior.coords) + "Z"
    for c in cortes:
        d += " M" + " L".join(P(x, y) for x, y in c.exterior.coords) + "Z"
    circ = "".join(f'<circle cx="{h[1] - x0 + m:.3f}" cy="{y1 - h[2] + m:.3f}" r="{h[3] / 2:.3f}"/>' for h in huecos)
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.2f}mm" height="{H:.2f}mm" viewBox="0 0 {W:.3f} {H:.3f}">'
         f'<title>{escape(titulo)}</title><g fill="none" stroke="#ff0000" stroke-width="0.1">'
         f'<path d="{d}"/>{circ}</g></svg>')
    open(os.path.join(BASE, "svg", nombre + ".svg"), "w").write(s)


# ------------------------------------------------------------------ trípode: alturas
def pie_de_pata(n_ext, hueco):
    """Distancia de la boca del casquillo a la punta del pie (configuración de patas largas)."""
    s_top = 902.0 * n_ext - 2 * g.H_BOCA - g.PASO * (hueco - 1)
    s_pie = s_top + g.PI_L - 2 * g.H_BOCA
    return s_pie + g.PIE_L - g4.GARRA_PUNTA


def Rx(a):
    c, s = math.cos(a), math.sin(a)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


GP_BAJO = 115.0
HING = np.array([0.0, *g.PIN_ARRIBA])


def trip(n_ext, hueco):
    a = math.radians(ALFA)
    d = np.array([0.0, -math.sin(a), -math.cos(a)])
    boca = np.array([0.0, g.GP_TUBO_Y, g.GP_ALA_Z[0]]) + GP_BAJO * d
    punta = pie_de_pata(n_ext, hueco)

    def pies(tau, phi):
        fa = []
        for lado in (-1, 1):
            x, z = g.eje(lado, g.CAS_L)
            fa.append(Rx(tau) @ (np.array([x, 0, z]) + punta * np.array([lado * g.SA, 0, -g.CA])))
        return fa, Rx(tau) @ (HING + Rx(phi) @ (boca + punta * d))

    def ec(v):
        (a1, a2), fg = pies(*v)
        return [fg[2] - a1[2], np.linalg.norm((a1 - fg)[:2]) - np.linalg.norm((a1 - a2)[:2])]
    tau, phi = fsolve(ec, [0.29, -0.29])
    (a1, a2), fg = pies(tau, phi)
    z0 = -a1[2]
    h = z0 + (Rx(tau) @ np.array([0, *g.PIN_ABAJO]))[2]
    lado = np.linalg.norm((a1 - a2)[:2])
    return h, lado, math.degrees(tau), math.degrees(phi)


def esc(v):
    return f"Escala 1:{f(v.k, 2)}"


def m2(v):
    return f"{v:.2f}".replace(".", ",")


# ------------------------------------------------------------------ dibujos de piezas planas
def dib_frontal(ancho):
    fr = g.placa_frontal()
    minx, miny, maxx, maxy = fr.bounds
    v = Vista(minx - 118, miny - 42, maxx + 40, maxy + 30, ancho)
    v.forma(fr.difference(g.ventana(-1)).difference(g.ventana(1)).difference(g.corazon()), "pieza")
    v.linea((0, -8), (0, maxy + 10), "eje")
    for sx in (-1, 1):
        v.linea((sx * g.X_RANURA, -6), (sx * g.X_RANURA, 16), "eje")
    v.cota_h(minx, maxx, 0, -28, f"{f(maxx - minx)}")
    v.cota_h(-g.X_RANURA, g.X_RANURA, 0, -14, f"{f(2 * g.X_RANURA)}")
    v.cota_v(0, g.alto_frontal(0), 0, -8, f(g.alto_frontal(0)))
    ytop = max(y for x, y in fr.exterior.coords if x > maxx - 20)
    v.cota_v(0, ytop, maxx, maxx + 20, f(ytop, 1))
    v.cota_h(82.0, 118.0, 21.0, 8, "36")
    v.cota_v(21.0, 77.5, 118.0, 132, f(56.5))
    v.cota_h(0, 82.0, 77.5, 92, "82")
    v.nota(-60, 108.5, -150, 136, "arco R 500 (baja 8,5 al centro)")
    v.nota(-(maxx - 18), 30, -(maxx + 8), 70, f"borde a {f(g.ANG)}°")
    v.texto(-(maxx + 14), 63, "(paralelo al tubo)", 0.9, "end", "ct")
    v.nota(-g.X_RANURA, 9, -g.X_RANURA - 30, -8, "muesca R 9 (2)")
    v.nota(-100, 40, -60, 64, "ventana E: R 7 abajo, R 5,5 arriba")
    v.nota(10, 20, 40, 55, "corazón B: 33 × 31")
    v.cota_v(g.corazon().bounds[1], g.corazon().bounds[3], 16.5, 30, f"{f(g.corazon().bounds[1])}–{f(g.corazon().bounds[3])}")
    return v


def dib_aleta(ancho):
    p, hs = g.ALETA
    v = Vista(-92, -28, 30, 128, ancho)
    v.forma(p, "pieza")
    for n, y, z, d in hs:
        v.circulo(y, z, d / 2)
        v.eje_cruz(y, z, d / 2)
        v.texto(y + 13, z + 1.5, n, 0.85, cls="etq")
    v.cota_h(g.Y_ATRAS, g.Y_FRENTE[0], 0, -16, f(g.Y_FRENTE[0] - g.Y_ATRAS))
    v.cota_h(g.Y_ATRAS, g.PIN_Y, g.ALETA_TOPE, g.ALETA_TOPE + 12, "20")
    v.cota_v(0, g.ALETA_TOPE, g.Y_FRENTE[0], g.Y_FRENTE[0] + 12, f(g.ALETA_TOPE))
    v.cota_v(0, g.PIN_ABAJO[1], g.Y_ATRAS, g.Y_ATRAS - 10, f(g.PIN_ABAJO[1]))
    v.cota_v(0, g.PIN_ARRIBA[1], g.Y_ATRAS, g.Y_ATRAS - 20, f(g.PIN_ARRIBA[1]))
    v.diametro(*g.PIN_ARRIBA, g.D12 / 2, 35, "2 × Ø 13,1")
    v.nota(-58, 104, -80, 120, "R 20")
    v.texto(-10, 50, "lado que va", 0.8)
    v.texto(-10, 44, "contra la placa 01 →", 0.8)
    return v


def dib_puente(ancho):
    p, hs = g.PUENTE
    v = Vista(-58, -74, 62, 26, ancho)
    v.forma(p, "pieza")
    for n, x, y, d in hs:
        v.circulo(x, y, d / 2)
        v.eje_cruz(x, y, d / 2)
    v.cota_h(-g.X_ALETA_INT, g.X_ALETA_INT, g.Y_FRENTE[0], 20, f(2 * g.X_ALETA_INT))
    v.cota_v(g.PUENTE_Y[0], g.Y_FRENTE[0], g.X_ALETA_INT, g.X_ALETA_INT + 12, f(g.Y_FRENTE[0] - g.PUENTE_Y[0]))
    v.cota_v(g.C_HUECO[1], g.Y_FRENTE[0], -g.X_ALETA_INT, -g.X_ALETA_INT - 10, f(g.Y_FRENTE[0] - g.C_HUECO[1]))
    v.diametro(*g.C_HUECO, g.D_MOSQ / 2, 300, "C · Ø 22")
    v.nota(-25, -48, -50, -66, "R 36 (centro en el hueco C)")
    v.texto(0, 16, "lado de la placa 01", 0.75)
    return v


def dib_ala(ancho):
    ala, ovalos, tubo = g.perfil_ala(ALFA)
    minx, miny, maxx, maxy = ala.bounds
    v = Vista(minx - 92, miny - 22, maxx + 30, maxy + 26, ancho)
    s = ala
    for o in ovalos + [tubo]:
        s = s.difference(o)
    v.forma(s, "pieza2")
    v.linea((0, miny - 8), (0, maxy + 8), "eje")
    tb = tubo.bounds
    yc = (tb[1] + tb[3]) / 2
    v.linea((-45, yc), (45, yc), "eje")
    v.cota_h(minx, maxx, miny, miny - 12, f(maxx - minx))
    v.cota_v(miny, maxy, maxx, maxx + 20, f(maxy - miny))
    v.cota_v(yc, maxy, maxx, maxx + 8, f(maxy - yc))
    v.cota_h(tb[0], tb[2], tb[1], tb[1] - 4 if False else miny + 8, f"{f(tb[2] - tb[0])}")
    v.nota(0, tb[3], 12, tb[3] + 26, f"elipse {f(tb[2] - tb[0])} × {f(tb[3] - tb[1])}")
    ob = ovalos[0].bounds
    v.nota(ob[0] + 2, (ob[1] + ob[3]) / 2, minx - 4, miny + 20, "D: 18 × 34")
    v.nota(ovalos[1].centroid.x, ovalos[1].centroid.y, minx - 4, maxy - 22, "D: 21 × 37")
    v.cota_h(-g.GP_OREJA_X[1], g.GP_OREJA_X[1], maxy, maxy + 12, f(2 * g.GP_OREJA_X[1]))
    v.texto(0, maxy - 6, "lado de la cabeza A-frame", 0.75)
    return v


def dib_oreja(ancho):
    p, hs = g.OREJA
    v = Vista(-58, -30, 34, 30, ancho)
    v.forma(p, "pieza2")
    v.circulo(0, 0, g.D12 / 2)
    v.eje_cruz(0, 0, g.D12 / 2)
    minx, miny, maxx, maxy = p.bounds
    v.cota_h(minx, maxx, miny, miny - 8, f(maxx - minx))
    v.cota_v(miny, g.GP_ALA_Z[0], minx, minx - 8, f(g.GP_ALA_Z[0] - miny))
    v.diametro(0, 0, g.D12 / 2, 40, "C · Ø 13,1 · R 16")
    v.texto(-20, 13, "va bajo el ala", 0.7)
    return v


def dib_ojo(ancho):
    p, hs = g.OJO
    v = Vista(-36, -56, 50, 20, ancho)
    v.forma(p, "pieza2")
    for n, x, y, d in hs:
        v.circulo(x, y, d / 2)
        v.eje_cruz(x, y, d / 2)
    minx, miny, maxx, maxy = p.bounds
    v.cota_h(minx, maxx, maxy, maxy + 7, f(maxx - minx))
    v.cota_v(miny, maxy, maxx, maxx + 8, f(maxy - miny))
    v.diametro(0, hs[0][2], 12.5, 330, "B · Ø 25")
    return v


def dib_cartela(ancho):
    p = g.perfil_cartela(ALFA)
    minx, miny, maxx, maxy = p.bounds
    v = Vista(minx - 14, miny - 18, maxx + 18, maxy + 14, ancho)
    v.forma(p, "pieza2")
    v.cota_h(minx, maxx, maxy, maxy + 8, f(maxx - minx))
    v.cota_v(miny, maxy, maxx, maxx + 9, f(maxy - miny))
    v.nota(minx + 12, miny + 22, minx + 34, miny - 8, f"borde que toca el tubo · {f(ALFA)}°")
    return v


# ------------------------------------------------------------------ tubos
CAS_DESDE_BOCA = [g.H_BOCA - g.VERNIER, g.H_BOCA, g.H_BOCA + g.VERNIER, g.H_BOCA + 2 * g.VERNIER]


def tubo_cas(ancho):
    """Casquillo dibujado con la boca de abajo (la de la pata) a la izquierda."""
    hu = [(p, g.D38, "") for p in CAS_DESDE_BOCA]
    v = vista_tubo(g.CAS_L, g.CAS_OD, g.CAS_ID, hu, "02 · Casquillo · huecos medidos desde la boca de la pata",
                   f"Escala 1:{f((g.CAS_L + 90) / ancho, 2)}", ancho, ranuras=[(0.0, 10.5, 11.0)],
                   arriba_txt="boca de la pata (3 ranuras F)", abajo_txt="boca de arriba (abierta)")
    return v


def tubo_gin(ancho):
    a = math.radians(ALFA)
    r = g.CAS_OD / 2
    t0 = (g.GP_ALA_Z[1] + g.GP_TUBO_ARRIBA - g.GP_ALA_Z[0]) / math.cos(a)
    largo = GP_BAJO + t0 + r * math.tan(a)
    corto = GP_BAJO + t0 - r * math.tan(a)
    k = (largo + 90) / ancho
    v = Vista(-45, -r - 60, largo + 45, r + 36, ancho)
    v.poli([(0, -r), (corto, -r), (largo, r), (0, r)], "pieza2")
    v.linea((0, g.CAS_ID / 2), (largo, g.CAS_ID / 2), "oculta")
    v.linea((0, -g.CAS_ID / 2), (corto, -g.CAS_ID / 2), "oculta")
    v.linea((-12, 0), (largo + 12, 0), "eje")
    v.rect(0, -5.25, 11, 10.5, "hueco")
    for p in (g.H_BOCA, g.H_BOCA + g.VERNIER):
        v.circulo(p, 0, g.D38 / 2)
        v.eje_cruz(p, 0, g.D38 / 2)
    v.cota_h(0, g.H_BOCA, r, r + 10, f(g.H_BOCA))
    v.cota_h(0, g.H_BOCA + g.VERNIER, r, r + 20, f(g.H_BOCA + g.VERNIER))
    v.cota_h(0, largo, r, r + 30, f(largo))
    v.cota_h(0, corto, -r, -r - 16, f(corto))
    v.cota_v(-r, r, 0, -18, f"Ø {f(g.CAS_OD)}")
    v.texto(0, -r - 34, "boca (pata)", 0.8, "start")
    v.texto(largo, -r - 34, f"corte a {f(90 - ALFA)}° (queda paralelo al ala)", 0.8, "end")
    return v, largo, corto


# ------------------------------------------------------------------ vistas de armado
def conjunto_cabeza(ancho_f, ancho_s, ancho_t):
    r = g.CAS_OD / 2
    fr = g.placa_frontal()
    # vista de frente (cara lisa)
    v = Vista(-240, -40, 240, 190, ancho_f)
    for lado in (-1, 1):
        v.poli([g.eje(lado, 0, -r), g.eje(lado, 0, r), g.eje(lado, g.CAS_L, r), g.eje(lado, g.CAS_L, -r)], "pieza3")
        v.linea(g.eje(lado, -12), g.eje(lado, g.CAS_L + 12), "eje")
    v.forma(fr.difference(g.ventana(-1)).difference(g.ventana(1)).difference(g.corazon()), "pieza")
    for x0 in (g.X_ALETA_INT, g.X_ALETA_EXT):
        for sx in (-1, 1):
            for x in (x0, x0 + T):
                v.linea((sx * x, 0), (sx * x, g.ALETA_TOPE), "oculta")
    v.cota_h(-208.5, 208.5, -8.4, -30, "417")
    v.cota_v(-8.4, 156.9, 208.5, 228, "165")
    v.cota_h(-g.XC, g.XC, g.ZT, 176, f(2 * g.XC))
    v.nota(g.eje(1, 40)[0], g.eje(1, 40)[1], 190, 120, f"eje del tubo a {f(g.ANG)}°")
    v.cota_v(0, g.ZT, -g.XC, -175, f(g.ZT))
    v.texto(0, -22, "Z = 0: borde de abajo de la placa 01", 0.8)
    frente = v

    # vista de lado (corte por una aleta)
    s = Vista(-100, -30, 60, 175, ancho_s)
    s.rect(-r, -8.4, 2 * r, 165.3, "pieza3")
    s.linea((0, -14), (0, 162), "eje")
    s.forma(g.ALETA[0], "pieza")
    for n, y, z, d in g.ALETA[1]:
        s.circulo(y, z, d / 2)
        s.eje_cruz(y, z, d / 2)
    s.rect(g.Y_FRENTE[0], 0, T, g.alto_frontal(g.X_ALETA_INT), "pieza")
    s.rect(g.PUENTE_Y[0], 0, g.Y_FRENTE[0] - g.PUENTE_Y[0], T, "oculta")
    s.cota_h(g.Y_ATRAS, g.Y_FRENTE[1], 0, -18, f(g.Y_FRENTE[1] - g.Y_ATRAS))
    s.cota_h(g.PIN_Y, 0, 110, 118, f(-g.PIN_Y))
    s.cota_h(0, g.Y_FRENTE[1], 156.9, 166, f(g.Y_FRENTE[1]))
    s.cota_h(-r, r, -8.4, -26, "63,5")
    s.texto(-44, 150, "tubo (casquillo)", 0.75, "end")
    s.texto(g.Y_FRENTE[1] + 2, 60, "01", 0.9, "start", "etq")
    s.texto(g.Y_ATRAS + 3, 58, "03", 0.9, "start", "etq")
    s.texto(-25, -6, "04", 0.8, "middle", "etq")
    lado = s

    # vista de arriba
    t = Vista(-230, -95, 230, 55, ancho_t)
    for lado_ in (-1, 1):
        xs = sorted([lado_ * 83.4, lado_ * 208.5])
        t.rect(xs[0], -r, xs[1] - xs[0], 2 * r, "pieza3")
    t.rect(-150, g.Y_FRENTE[0], 300, T, "pieza")
    for x0 in (g.X_ALETA_INT, g.X_ALETA_EXT):
        for sx in (-1, 1):
            t.rect(sx * x0 if sx > 0 else -x0 - T, g.Y_ATRAS, T, g.Y_FRENTE[0] - g.Y_ATRAS, "pieza")
    t.forma(g.PUENTE[0], "pieza3")
    t.circulo(*g.C_HUECO, g.D_MOSQ / 2)
    t.eje_cruz(*g.C_HUECO, g.D_MOSQ / 2)
    t.texto(0, -40, "04", 0.8, "middle", "etq")
    for sx in (-1, 1):
        t.rect(sx * g.X_RANURA - 31, g.PIN_Y - 6.35, 62, 12.7, "pieza2")
    t.linea((0, -80), (0, 40), "eje")
    t.cota_h(0, g.X_ALETA_INT, g.Y_ATRAS, -76, f(g.X_ALETA_INT))
    t.cota_h(0, g.X_ALETA_INT + T, g.Y_ATRAS, -84, f(g.X_ALETA_INT + T))
    t.cota_h(0, g.X_ALETA_EXT, g.Y_ATRAS, -92, f(g.X_ALETA_EXT))
    t.cota_h(-g.X_ALETA_EXT - T, 0, g.Y_ATRAS, -76, f(g.X_ALETA_EXT + T))
    t.cota_h(-g.X_ALETA_EXT, -g.X_ALETA_INT - T, g.PIN_Y, -30, f(g.X_ALETA_EXT - g.X_ALETA_INT - T))
    t.texto(-g.X_RANURA, -60, "ranura", 0.7)
    t.texto(0, 30, "cara lisa (adelante)", 0.75)
    arriba = t
    return frente, lado, arriba


def conjunto_gin(ancho):
    a = math.radians(ALFA)
    d = np.array([-math.sin(a), -math.cos(a)])
    n = np.array([math.cos(a), -math.sin(a)])
    r = g.CAS_OD / 2
    ax0 = np.array([g.GP_TUBO_Y, g.GP_ALA_Z[0]])
    zc = g.GP_ALA_Z[1] + g.GP_TUBO_ARRIBA

    def gen(k):
        p = ax0 + k * r * n
        t_top = (zc - p[1]) / (-d[1])
        return p - t_top * d, p + GP_BAJO * d + (k * r * n * 0)
    pts = []
    for k in (1, -1):
        top, _ = gen(k)
        bot = ax0 + GP_BAJO * d + k * r * n
        pts.append((top, bot))
    v = Vista(-250, -150, 60, 70, ancho)
    v.poli([tuple(pts[0][0]), tuple(pts[0][1]), tuple(pts[1][1]), tuple(pts[1][0])], "pieza2")
    v.linea(tuple(ax0 - 30 * d), tuple(ax0 + (GP_BAJO + 12) * d), "eje")
    v.forma(g.perfil_cartela(ALFA), "pieza2")
    v.rect(g.GP_PUNTA - g.GP_LARGO, g.GP_ALA_Z[0], -23 - (g.GP_PUNTA - g.GP_LARGO), T, "pieza2")
    v.forma(g.OREJA[0], "pieza2")
    v.circulo(0, 0, g.D12 / 2)
    v.eje_cruz(0, 0, 12)
    v.rect(g.GP_OJO_Y[0], g.OJO[0].bounds[1], T, g.GP_ALA_Z[0] - g.OJO[0].bounds[1], "pieza2")
    v.cota_h(g.GP_PUNTA - g.GP_LARGO, g.GP_PUNTA, g.GP_ALA_Z[1], 48, f(g.GP_LARGO))
    v.cota_h(g.GP_TUBO_Y, 0, g.GP_ALA_Z[1], 36, f(-g.GP_TUBO_Y))
    v.cota_v(0, g.GP_ALA_Z[1], 0, 30, f(g.GP_ALA_Z[1]))
    v.nota(*(ax0 + 90 * d), -120, -120, f"tubo a {f(ALFA)}° del ala")
    v.texto(-180, 26, "05 ala", 0.8, "middle", "etq")
    v.texto(-100, -8, "09 cartela", 0.8, "middle", "etq")
    v.texto(10, -24, "07 oreja", 0.8, "start", "etq")
    v.texto(-35, -52, "08 ojo", 0.8, "middle", "etq")
    v.texto(-200, -60, "06 tubo", 0.8, "middle", "etq")
    v.texto(0, 16, "pasador de arriba", 0.7, "middle")
    return v


# ------------------------------------------------------------------ dibujos nuevos (patas, pie, carrete, AHP, cadenas)
def dib_pata_afuera(v):
    """Pata de afuera acostada: x = 0 en la punta del macho, x = 1054 en la boca de la hembra."""
    M, L = g.PA_MACHO, g.PA_TOTAL
    rb, re_ = g.D_AFUERA / 2, g.D_PATA / 2
    v.rect(0, -re_, M, 2 * re_, "pieza3")
    v.linea((M, re_), (M + g.PA_ESPIGA_DENTRO, re_), "oculta")
    v.linea((M, -re_), (M + g.PA_ESPIGA_DENTRO, -re_), "oculta")
    v.linea((M + g.PA_ESPIGA_DENTRO, -re_), (M + g.PA_ESPIGA_DENTRO, re_), "oculta")
    v.rect(M, -rb, g.PA_CUERPO, 2 * rb, "pieza")
    v.linea((M, 52.5 / 2), (L, 52.5 / 2), "oculta")
    v.linea((M, -52.5 / 2), (L, -52.5 / 2), "oculta")
    v.rect(L - 11, -5.25, 11, 10.5, "hueco")
    v.linea((-12, 0), (L + 12, 0), "eje")
    for x in (g.PA_HUECO_MACHO, L - g.H_BOCA):
        v.circulo(x, 0, g.D38 / 2)
        v.eje_cruz(x, 0, g.D38 / 2)
    for x in g.PA_REMACHES:
        v.circulo(M + x, -rb + 6, 4.95, "hueco")
    v.rect(M - 10.25, re_, 9.5, 6, "pieza2")                  # tope de alineación


def pata_afuera_vistas():
    L, M = g.PA_TOTAL, g.PA_MACHO
    rb = g.D_AFUERA / 2
    tot = Vista(-40, -rb - 60, L + 50, rb + 40, 240)
    dib_pata_afuera(tot)
    tot.cota_h(0, L, -rb, -rb - 22, f"{f(L)}")
    tot.cota_h(0, M, rb, rb + 14, f(M))
    tot.cota_h(M, L, rb, rb + 28, f(g.PA_CUERPO))
    tot.texto(0, -rb - 44, "macho (a la cabeza, a otra pata o al pie)", 0.8, "start")
    tot.texto(L, -rb - 44, "hembra (recibe un macho o la pata de adentro)", 0.8, "end")
    mac = Vista(-25, -60, 300, 60, 150)
    dib_pata_afuera(mac)
    mac.cota_h(0, g.PA_HUECO_MACHO, g.D_PATA / 2, 44, f(g.PA_HUECO_MACHO))
    mac.cota_h(g.PA_HUECO_MACHO, M, g.D_PATA / 2, 44, f(g.H_BOCA))
    mac.cota_h(M, M + g.PA_REMACHES[0], -rb, -44, f(g.PA_REMACHES[0]))
    mac.cota_h(M, M + g.PA_REMACHES[1], -rb, -54, f(g.PA_REMACHES[1]))
    mac.cota_v(-g.D_PATA / 2, g.D_PATA / 2, 20, 8, f"Ø {f(g.D_PATA)}")
    mac.cota_v(-rb, rb, 280, 292, f"Ø {f(g.D_AFUERA)}")
    mac.nota(M - 5.5, g.D_PATA / 2 + 6, M + 30, 52, "tope Ø 9,5 sale 6")
    mac.nota(M + g.PA_REMACHES[0], -rb + 6, M + 60, -28, "2 pernos fijos 3/8\"")
    hem = Vista(g.PA_TOTAL - 170, -60, g.PA_TOTAL + 40, 60, 110)
    dib_pata_afuera(hem)
    hem.cota_h(L - g.H_BOCA, L, rb, 44, f(g.H_BOCA))
    hem.cota_h(L - 11, L, -rb, -46, "11")
    hem.nota(L - 5, 0, L - 80, -40, "ranura 10,5 × 11 (va el tope)")
    return tot, mac, hem


def dib_cadena(items, pins, titulo_arriba=None, sale=None, ancho=330):
    """Esquema de una pata: x = distancia desde la boca del casquillo (positivo hacia el pie)."""
    fin = max(s + (g.PI_L if p == "13" else g.PA_CUERPO if p == "10" else g.PIE_L + 112) for p, _, s, _ in items)
    ini = -g.CAS_L - (g.CAR_A_ALTO + 60 if sale else 20)
    v = Vista(ini - 30, -70, fin + 40, 70, ancho)
    v.rect(-g.CAS_L, -g.CAS_OD / 2, g.CAS_L, g.CAS_OD, "pieza")
    v.texto(-g.CAS_L / 2, g.CAS_OD / 2 + 6, "casquillo", 0.75)
    for p, nom, s, rev in items:
        if p == "13":
            v.rect(s, -g.D_PATA / 2, g.PI_L, g.D_PATA, "pieza3")
            for h in g.PI_HUECOS:
                v.circulo(s + h, 0, 3.0, "hueco")
        elif p == "10":
            if rev:
                v.rect(s - g.PA_CUERPO, -g.D_AFUERA / 2, g.PA_CUERPO, g.D_AFUERA, "pieza")
                v.rect(s, -g.D_PATA / 2, g.PA_MACHO, g.D_PATA, "pieza")
            else:
                v.rect(s, -g.D_AFUERA / 2, g.PA_CUERPO, g.D_AFUERA, "pieza")
                v.rect(s - g.PA_MACHO, -g.D_PATA / 2, g.PA_MACHO, g.D_PATA, "pieza")
        else:
            v.rect(s, -g.D_AFUERA / 2, g.PIE_L, g.D_AFUERA, "pieza2")
            v.poli([(s + g.PIE_L, -30), (s + g.PIE_L + 112, 0), (s + g.PIE_L, 30)], "pieza2")
    if sale:
        v.rect(-sale[0] - 10, -g.CAR_DISCO / 2 * 0.4, 10, g.CAR_DISCO * 0.4, "pieza2")
        v.texto(-sale[0] - 30, 40, "carrete", 0.75)
    for i, sp in enumerate(pins):
        v.linea((sp, -48), (sp, 48), "cruz")
        v.texto(sp, 54 + (i % 2) * 9, f"{f(sp)}", 0.75, cls="ct")
    v.linea((0, -64), (0, 64), "eje")
    v.texto(4, -62, "boca del casquillo (0)", 0.7, "start")
    return v


def dib_pie(ancho):
    G = g4.contorno_garra()
    minx, miny, maxx, maxy = G.bounds
    v = Vista(minx - 35, miny - 28, maxx + 40, g.PIE_L + 30, ancho)
    v.rect(-g.D_AFUERA / 2, 0, g.D_AFUERA, g.PIE_L, "pieza3")
    v.linea((-g.D_BOCA / 2, 0), (-g.D_BOCA / 2, g.PIE_L), "oculta")
    v.linea((g.D_BOCA / 2, 0), (g.D_BOCA / 2, g.PIE_L), "oculta")
    v.forma(G.difference(box(-g.D_AFUERA / 2, 0, g.D_AFUERA / 2, 200)), "pieza2")
    for n, x, y, d, _ in g4.HUECOS_GARRA:
        v.circulo(x, y, d / 2)
        v.eje_cruz(x, y, d / 2)
    v.circulo(0, g.PIE_L - g.H_BOCA, g.D38 / 2)
    v.eje_cruz(0, g.PIE_L - g.H_BOCA, g.D38 / 2)
    v.linea((0, miny - 8), (0, g.PIE_L + 8), "eje")
    v.cota_h(minx, maxx, miny, miny - 14)
    v.cota_v(g4.GARRA_PUNTA, g.PIE_L, maxx, maxx + 24, f(g.PIE_L - g4.GARRA_PUNTA))
    v.cota_v(g.PIE_L - g.H_BOCA, g.PIE_L, -g.D_AFUERA / 2, -g.D_AFUERA / 2 - 12, f(g.H_BOCA))
    v.cota_h(-g.D_AFUERA / 2, g.D_AFUERA / 2, g.PIE_L, g.PIE_L + 12, f"Ø {f(g.D_AFUERA)}")
    return v


def dib_disco(naranja, ancho):
    p, hs, cs = g.CAR_N if naranja else g.CAR_A
    r = g.CAR_DISCO / 2
    v = Vista(-r - 40, -r - 30, r + 60, r + 26, ancho)
    s_ = p
    for c in cs:
        s_ = s_.difference(c)
    v.forma(s_, "pieza2" if naranja else "pieza")
    for n, x, y, d in hs:
        v.circulo(x, y, d / 2)
        v.eje_cruz(x, y, d / 2)
    v.eje_cruz(0, 0, 36)
    v.circulo(0, 0, g.CAR_PCD / 2, "eje")
    v.cota_h(-r, r, -r, -r - 14, f"Ø {f(g.CAR_DISCO)}")
    v.diametro(0, 0, g.CAR_PCD / 2, 20, f"9 × Ø {f(g.CAR_HUECO)} en Ø {f(g.CAR_PCD)}")
    v.nota(0, g.CAR_PCD / 2 + g.CAR_CHICO / 2, 40, r + 14, f"hueco chico Ø {f(g.CAR_CHICO)} (marca)")
    if naranja:
        v.nota(0, -g.D_AFUERA / 2, -50, -r - 4, "llave: 2 ranuras 10,5 a R 31,2")
        v.cota_h(-g.D_BOCA / 2, g.D_BOCA / 2, 0, 12, f"Ø {f(g.D_BOCA)}")
    else:
        v.cota_h(-g.D_AZUL / 2, g.D_AZUL / 2, 0, 12, f"Ø {f(g.D_AZUL)}")
    return v


def dib_carrete_lado(ancho):
    """Vista de lado de las 2 piezas del carrete armadas (corte por el eje)."""
    v = Vista(-125, -30, 150, 170, ancho)
    r = g.CAR_DISCO / 2
    v.rect(-r, 0, 2 * r, T, "pieza")
    for sx in (-1, 1):
        v.rect(sx * g.D_AZUL / 2 if sx > 0 else -g.CAR_A_OD / 2, T, (g.CAR_A_OD - g.D_AZUL) / 2, g.CAR_A_ALTO, "pieza")
    top = g.CAR_A_ALTO + 2 * T
    v.rect(-r, top - T, 2 * r, T, "pieza2")
    for sx in (-1, 1):
        v.rect(sx * g.D_BOCA / 2 if sx > 0 else -g.D_AFUERA / 2, top - T - g.CAR_N_ALTO, (g.D_AFUERA - g.D_BOCA) / 2,
               g.CAR_N_ALTO, "pieza2")
    v.linea((0, -10), (0, top + 12), "eje")
    for z in g.CAR_HUECOS:
        v.linea((-g.CAR_A_OD / 2 - 6, z), (g.CAR_A_OD / 2 + 6, z), "cruz")
    v.cota_v(0, top, r, r + 12, f(top))
    v.cota_v(0, g.H_BOCA, -r, -r - 10, f(g.H_BOCA))
    v.cota_v(g.H_BOCA, top, -r, -r - 22, f(top - g.H_BOCA))
    v.cota_h(-g.CAR_A_OD / 2, g.CAR_A_OD / 2, T + g.CAR_A_ALTO, T + g.CAR_A_ALTO + 26 + 10, f"Ø {f(g.CAR_A_OD)}")
    v.texto(r - 4, top + 6, "15 naranja", 0.8, "end", "etq")
    v.texto(r - 4, -12, "16 azul", 0.8, "end", "etq")
    return v


def dib_ahp(ancho):
    p, hs, cs = g.AHP
    minx, miny, maxx, maxy = p.bounds
    v = Vista(minx - 150, miny - 30, maxx + 50, maxy + 20, ancho)
    s_ = p
    for c in cs:
        s_ = s_.difference(c)
    v.forma(s_, "pieza2")
    for n, x, y, d in hs:
        v.circulo(x, y, d / 2)
        v.eje_cruz(x, y, d / 2)
    u = g.AHP_U / 2
    v.linea((-u - 30, g.AHP_PIN_Y), (u + 30, g.AHP_PIN_Y), "oculta")
    v.linea((0, -10), (0, maxy + 10), "eje")
    v.cota_h(minx, maxx, miny, miny - 16, f(maxx - minx))
    v.cota_v(miny, maxy, maxx, maxx + 26, f(maxy - miny))
    v.cota_h(-u, u, 150, 136, f(g.AHP_U))
    v.cota_v(miny, g.AHP_PIN_Y, -u - 30, -u - 44, f(g.AHP_PIN_Y - miny))
    v.cota_h(-27, 27, 380, 392, "54")
    v.cota_h(-66, 66, 214, 244, "132")
    v.cota_v(170, 214, 96, 108, "44")
    v.nota(-66 - 12.5, 214, minx - 10, 280, "4 × Ø 25 anclajes")
    v.nota(0, 350 - 8.25, 60, 330, "Ø 16,5 pasador del adaptador")
    v.nota(-u - 15, g.AHP_PIN_Y, minx - 6, 50, "Ø 9,9 de canto (pasador 3/8\")")
    v.nota(-(u + 30 + 16), 81, minx - 6, 110, "ranura 16 × 24 (maniota)")
    return v


# ------------------------------------------------------------------ hojas
def banner(html):
    return html.replace('<div class="marco"></div>', '<div class="marco"></div><div class="unidades">TODAS LAS MEDIDAS EN MILÍMETROS (mm)</div>', 1)


CSS8 = CSS + """
.unidades{position:absolute;right:14mm;top:1.2mm;font:700 10.5pt 'Barlow Condensed',sans-serif;letter-spacing:.06em;
  background:#101820;color:#fff;padding:1.2mm 3.5mm;border-radius:.6mm;z-index:3}
"""


def kg_cabeza():
    return sum(kg(p) for p in ("01", "02a", "02b", "03a", "03b", "03c", "03d", "04"))


def kg_gin():
    return sum(kg(p) for p in ("05", "06", "07a", "07b", "08", "09a", "09b"))


LISTA = [
    ("01", "Placa frontal (cara lisa)", "Al 6061-T6 10 mm · láser", 1, "01", AL),
    ("02", "Casquillo de la cabeza", "Tubo Al 6061-T6 2½\" × 1/4\" × 153", 2, "02a", AL),
    ("03", "Aleta de la cabeza", "Al 6061-T6 10 mm · láser", 4, "03a", AL),
    ("04", "Puente central (hueco C)", "Al 6061-T6 10 mm · láser", 1, "04", AL),
    ("05", "Ala de la gin pole", "Al 6061-T6 10 mm · láser", 1, "05", AL),
    ("06", "Tubo de la gin pole", "Tubo Al 6061-T6 2½\" × 1/4\"", 1, "06", AL),
    ("07", "Oreja de la gin pole", "Al 6061-T6 10 mm · láser", 2, "07a", AL),
    ("08", "Ojo central de la gin pole", "Al 6061-T6 10 mm · láser", 1, "08", AL),
    ("09", "Cartela de la gin pole", "Al 6061-T6 10 mm · láser", 2, "09a", AL),
    ("10", "Pata de afuera (cuerpo + espiga + tope)", "Tubo 2\" céd. 40 × 902 + tubo 2\" × 1/4\" × 272", 7, "10", AL),
    ("13", "Pata de adentro", "Tubo Al 6061-T6 2\" × 1/4\" × 965", 3, "13", AL),
    ("14", "Pie de flecha", "Casquillo Al Ø 60,3 × 140 + garra A36 12 mm", 3, "14", AL),
    ("15", "Carrete naranja (de adentro)", "Disco Al 10 mm + tubo Ø 60,3 × 100", 1, "15", AL),
    ("16", "Carrete azul (de afuera)", "Disco Al 10 mm + tubo Ø 73 × 107", 1, "16", AL),
    ("17", "AHP (poste de enganche del carro)", "Al 6061-T6 1\" (25,4) · chorro de agua", 1, "17", AL),
    ("18", "Adaptador de enganche 2\"", "Acero A36 · tubo cuadrado 2\" + placas", 1, "18", AC),
]


def hoja_portada():
    filas = "".join(f'<tr><td class="m" style="width:12mm">{i + 2:02d}</td><td>{escape(t)}</td></tr>' for i, t in enumerate(INDICE))
    h, lado, tau, phi = trip(2, 1)
    c = f"""<div class="cont" style="grid-template-columns:150mm 1fr">
      <div class="bloque" style="gap:5mm;align-content:space-between">
        <div class="bloque" style="gap:4mm">
          <div class="kick">Juego de planos de fabricación · Rev. D</div>
          <h1 style="font-size:54pt;font-weight:700;line-height:.9">VX-EC<br><span style="color:var(--azul)">Trípode</span><br>tipo Vortex</h1>
          <p class="lead">Copia del Arizona Vortex: cabeza A-frame (azul) y gin pole (naranja) con placas de aluminio 6061-T6 de 10 mm,
          láser y TIG; 7 patas de afuera, 3 de adentro y 3 pies; carrete de anclajes de 2 piezas y poste AHP para el carro.
          Todos los huecos siguen una sola regla para que cualquier combinación coincida.</p>
        </div>
        <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:5mm">
          <div class="cifra"><b>{m2(h / 1000)} m</b><span>altura al pasador de abajo · 2 patas de afuera (Vortex 2,41 m)</span></div>
          <div class="cifra"><b>417 × 165 mm</b><span>cabeza A-frame (igual al Vortex)</span></div>
          <div class="cifra"><b>{m2(kg_cabeza())} kg</b><span>cabeza A-frame soldada (Vortex 2,3 kg)</span></div>
          <div class="cifra"><b>63,5 · 139,7 mm</b><span>regla de huecos: desde cada boca · paso de la pata de adentro</span></div>
        </div>
        <div class="bloque"><h3>Contenido</h3><table><tbody>{filas}</tbody></table></div>
        <div class="ficha">
          <dt>Cliente</dt><dd>Aventuras con Janeric · Morona Santiago, Ecuador</dd>
          <dt>Referencia</dt><dd>Arizona Vortex, AZORP y AHP · Rock Exotica / CMC · manual y fotos</dd>
          <dt>Reemplaza</dt><dd>Rev. C: ya no se usa</dd>
        </div>
      </div>
      <div style="display:grid;grid-template-rows:1fr 1fr;gap:6mm">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:4mm;align-items:center">
          <img class="render" src="{img('v8_t')}" style="height:112mm;justify-self:center">
          <img class="render" src="{img('v8_tb')}" style="height:112mm;justify-self:center">
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:6mm;align-items:center">
          <img class="render" src="{img('v8_ciso')}" style="height:74mm">
          <img class="render" src="{img('v8_acc')}" style="height:74mm">
        </div>
      </div>
    </div>"""
    hoja("—", "Portada", "—", "", "S/E", c)


def hoja_lista():
    filas = ""
    for n, nom, mat, q, pid, dens in LISTA:
        filas += (f'<tr><td class="n">{n}</td><td><b>{escape(nom)}</b></td><td>{escape(mat)}</td><td class="m">{q}</td>'
                  f'<td class="m">{m2(kg(pid, dens))}</td><td class="m">{m2(kg(pid, dens) * q)}</td></tr>')
    alt = ""
    for ne in (1, 2, 3):
        for hu in (1, 3, 6):
            h, lado, tau, phi = trip(ne, hu)
            alt += (f'<tr{" class=dest" if (ne, hu) == (2, 1) else ""}><td class="m">{ne}</td><td class="m">{hu}</td>'
                    f'<td class="m">{f(h, 0)} mm</td><td class="m">{f(lado, 0)} mm</td></tr>')
    c = f"""<div class="cont" style="grid-template-columns:1fr 128mm">
      <div class="bloque" style="gap:4mm">
        <div class="bloque"><div class="kick">Todas las piezas, numeradas</div><h2>Lista de piezas</h2></div>
        <table><thead><tr><th>N.º</th><th>Pieza</th><th>Material</th><th>Cant.</th><th>kg c/u</th><th>kg total</th></tr></thead><tbody>{filas}</tbody></table>
        <div class="aviso"><b>Numeración</b>01–04 cabeza A-frame (azul) · 05–09 gin pole (naranja) · 10 pata de afuera (7: 6 en uso + 1 de repuesto) ·
        13 pata de adentro · 14 pie · 15–16 carrete de anclajes · 17–18 poste AHP para el carro. Grabar el número en cada pieza.</div>
      </div>
      <div class="bloque" style="gap:4mm">
        <h3>Alturas · trípode de patas iguales</h3>
        <table><thead><tr><th>Patas de afuera</th><th>Hueco pata de adentro</th><th>Altura al pasador</th><th>Lado entre pies</th></tr></thead><tbody>{alt}</tbody></table>
        <p style="font-size:8pt;color:var(--gris)">Hueco 1 = la pata de adentro metida lo menos posible en la pata de afuera. Vortex: 2410 mm con 2 patas de afuera.</p>
        <img class="render" src="{img('v8_t')}" style="height:70mm;justify-self:center">
      </div>
    </div>"""
    hoja("LISTA", "Lista de piezas y alturas", "Varios", "", "S/E", c)
    indice("Lista de piezas numeradas y tabla de alturas")


def hoja_regla():
    ia, pa_, pu_a = ARM_A
    ib, pb, pu_b, top_b = ARM_B
    ca = dib_cadena(ia, pa_, ancho=380)
    cb = dib_cadena(ib, pb, sale=(-top_b - g.CAS_L,), ancho=380)
    c = f"""<div class="cont" style="grid-template-rows:auto auto auto auto 1fr">
      <div style="display:grid;grid-template-columns:1fr 160mm;gap:8mm;align-items:end">
        <div class="bloque"><div class="kick">Por qué coinciden todos los huecos</div><h2>Regla de huecos y formas de armar</h2></div>
        <div class="aviso"><b>Una sola regla para todo</b><span>1) Todo hueco de pasador 3/8" queda a 63,5 mm (2½") de la boca de su pieza.
        2) Todo macho sale 152 mm, con su hueco a 88,5 mm de la punta. 3) La pata de adentro tiene 7 huecos cada 139,7 mm (5½"),
        el primero y el último a 63,5 mm de las puntas. 4) Casquillos y carretes llevan huecos extra cada 27,9 mm para ajuste fino.</span></div>
      </div>
      {guardar("cadena_A", ca.svg("A · Patas largas: macho arriba en el casquillo, 2 patas de afuera, pata de adentro, pie", esc(ca)))}
      {guardar("cadena_B", cb.svg("B · Tubo arriba: la pata de adentro atraviesa el casquillo y sale " + f(-top_b - g.CAS_L, 0) + " mm; las patas de afuera van dadas vuelta", esc(cb)))}
      <table><thead><tr><th>Forma</th><th>Orden desde la cabeza</th><th>Distancia boca → punta del pie</th><th>Pasadores (distancias desde la boca del casquillo)</th></tr></thead><tbody>
        <tr><td class="n">A</td><td>casquillo · afuera · afuera · adentro · pie</td><td class="m">{f(pu_a, 0)} mm</td><td class="m">{" · ".join(f(x) for x in pa_)} mm</td></tr>
        <tr><td class="n">B</td><td>adentro (sale arriba, carrete) · casquillo · afuera dada vuelta · afuera dada vuelta · pie</td><td class="m">{f(pu_b, 0)} mm</td><td class="m">{" · ".join(f(x) for x in pb)} mm</td></tr>
      </tbody></table>
    </div>"""
    hoja("REGLA", "Regla de huecos y formas de armar", "—", "", "S/E", c,
         "Los números negativos quedan dentro del casquillo o por encima de él.")
    indice("Regla de huecos y formas de armar (patas largas / tubo arriba)")


def hoja_armado_cabeza():
    fr, la, ar = conjunto_cabeza(215, 100, 215)
    c = f"""<div class="cont" style="grid-template-columns:1fr 112mm;grid-template-rows:auto auto 1fr;grid-template-areas:'t t' 'f l' 'a l'">
      <div class="bloque" style="grid-area:t"><div class="kick">Cabeza A-frame · 8 piezas soldadas con TIG</div><h2>Armado de la cabeza A-frame</h2></div>
      <div style="grid-area:f">{guardar("arm_cab_frente", fr.svg("Vista de frente (cara lisa) · aletas en línea oculta", esc(fr)))}</div>
      <div class="bloque" style="grid-area:l;gap:5mm">{guardar("arm_cab_lado", la.svg("Vista de lado", esc(la)))}
        <img class="render" src="{img('v8_ab')}" style="height:46mm">
        <div class="aviso"><b>Centro de atrás abierto</b>Como el Vortex: entre las 2 aletas de adentro no hay placa trasera; queda una U para pasar la cuerda y meter la mano.</div>
      </div>
      <div style="grid-area:a">{guardar("arm_cab_arriba", ar.svg("Vista de arriba · posición de cada placa", esc(ar)))}</div>
    </div>"""
    hoja("01–04", "Armado de la cabeza A-frame", "Al 6061-T6", "1 juego", "ver vistas", c,
         "Las 4 aletas son iguales. Soldar primero con puntos y medir antes del cordón completo.")
    indice("Armado de la cabeza A-frame (vistas con posiciones)")


def hoja_piezas_cabeza_1():
    v1 = dib_frontal(236)
    tub = tubo_cas(132)
    WEB["02"] = tub
    c = f"""<div class="cont" style="grid-template-columns:245mm 1fr;grid-template-rows:auto 1fr">
      <div class="bloque" style="grid-column:1/3"><div class="kick">Piezas 01 y 02</div><h2>Placa frontal y casquillos</h2></div>
      <div class="bloque">{guardar("01", v1.svg("01 · Placa frontal (cara lisa) · 1 pieza", esc(v1)))}
        <dl class="ficha">
          <dt>01</dt><dd>Al 6061-T6 10 mm, láser o chorro de agua. {m2(kg('01'))} kg. La cara lisa del Vortex: una sola pieza.</dd>
          <dt>Bordes</dt><dd>Los 2 bordes laterales tocan el tubo por atrás; adelante queda una V para soldar y luego se lija al ras. Redondear R 1 mm los bordes de las ventanas E, el corazón B y las muescas.</dd>
        </dl>
      </div>
      <div class="bloque" style="gap:4mm">{tub}
        <dl class="ficha">
          <dt>02</dt><dd>Tubo 6061-T6 2½" × 1/4" (Ø 63,5 × 6,35 mm), largo 153 mm, 2 piezas, ABIERTO en las 2 puntas. Tornear por dentro a Ø 51,4 mm. {m2(kg('02a'))} kg c/u.</dd>
          <dt>Huecos</dt><dd>De frente a atrás, Ø 9,9 mm a 35,6 · <b>63,5</b> · 91,4 · 119,4 mm de la boca de la pata. De lado (a 90°), Ø 9,9 mm a 63,5 y 91,4 mm. El de 63,5 mm es el principal; los otros ajustan la pata de adentro cada 27,9 mm.</dd>
          <dt>Ranuras F</dt><dd>3 ranuras de 10,5 × 11 mm en la boca de la pata, a 90°, 210° y 330° (el tope de la pata de afuera entra en una: 3 posiciones de giro).</dd>
          <dt>Posición</dt><dd>Eje a {f(g.ANG)}° de la vertical; boca de arriba centrada en x = ±{f(g.XC)} mm, z = {f(g.ZT)} mm.</dd>
        </dl>
      </div>
    </div>"""
    hoja("01–02", "Placa frontal y casquillos", "Al 6061-T6", "1 + 2", "ver vistas", c)
    indice("01 y 02 · Placa frontal y casquillos")


def hoja_piezas_cabeza_2():
    a = dib_aleta(118)
    pu = dib_puente(108)
    c = f"""<div class="cont" style="grid-template-columns:auto auto 1fr;grid-template-rows:auto 1fr auto;column-gap:14mm">
      <div class="bloque" style="grid-column:1/4"><div class="kick">Piezas 03 y 04 · Al 6061-T6 10 mm</div><h2>Aletas y puente central</h2></div>
      {guardar("03", a.svg("03 · Aleta · 4 piezas iguales", esc(a)))}
      {guardar("04", pu.svg("04 · Puente central · 1", esc(pu)))}
      <div></div>
      <table style="grid-column:1/4"><thead><tr><th>N.º</th><th>Pieza</th><th>Cant.</th><th>Dónde va</th><th>kg c/u</th></tr></thead><tbody>
        <tr><td class="n">03</td><td>Aleta</td><td class="m">4</td><td>Parada de canto contra la cara de atrás de la placa 01. Caras de adentro a x = ±36 mm y ±64 mm del centro. Entre cada par queda la ranura de 18 mm: ahí entra la oreja 07 de la gin pole y cuelgan las poleas y los mosquetones.</td><td class="m">{m2(kg('03a'))}</td></tr>
        <tr><td class="n">04</td><td>Puente central</td><td class="m">1</td><td>Acostado abajo (z = 0 … 10 mm) entre las aletas de adentro, desde la placa 01 hasta 70 mm hacia atrás. Hueco C Ø 22 mm vertical para mosquetón. Atrás queda abierto (sin placa trasera).</td><td class="m">{m2(kg('04'))}</td></tr>
      </tbody></table>
    </div>"""
    hoja("03–04", "Aletas y puente central", "Al 6061-T6 10 mm", "4 + 1", "ver vistas", c,
         "Huecos de pasador Ø 13,1 mm: cortar a Ø 12 mm con láser y escariar a 13,1 mm después de soldar, con las 4 aletas en línea.")
    indice("03 y 04 · Aletas y puente central")


def hoja_gin():
    arm = conjunto_gin(210)
    ala = dib_ala(118)
    c = f"""<div class="cont" style="grid-template-columns:132mm 1fr;grid-template-rows:auto 1fr">
      <div class="bloque" style="grid-column:1/3"><div class="kick">Gin pole (naranja) · piezas 05 a 09 · Al 6061-T6</div><h2>Gin pole · armado y ala</h2></div>
      <div class="bloque">{guardar("05", ala.svg("05 · Ala (escudo) · 1", esc(ala)))}</div>
      <div class="bloque" style="gap:5mm">
        {guardar("arm_gin", arm.svg("Armado · vista de lado (ala horizontal)", esc(arm)))}
        <div style="display:grid;grid-template-columns:1fr 80mm;gap:6mm;align-items:start">
        <dl class="ficha">
          <dt>05 Ala</dt><dd>Plancha 10 mm, {m2(kg('05'))} kg. 4 óvalos D de anclaje y hueco elíptico para el tubo inclinado.</dd>
          <dt>Bisagra</dt><dd>Las orejas 07 entran en las ranuras de la cabeza; el pasador de arriba de cada lado las atraviesa.</dd>
          <dt>Ángulo</dt><dd>Tubo a {f(ALFA)}° del ala: el ala queda horizontal con el trípode parado y las 3 patas iguales.</dd>
        </dl>
        <img class="render" src="{img('v8_ciso')}" style="height:52mm">
        </div>
      </div>
    </div>"""
    hoja("05", "Gin pole · armado y ala", "Al 6061-T6", "1 juego", "ver vistas", c)
    indice("05 · Gin pole: armado y ala")
    tub, largo, corto = tubo_gin(170)
    WEB["06"] = tub.svg("06 · Tubo de la gin pole · 1", esc(tub))
    o, oj, ca = dib_oreja(80), dib_ojo(76), dib_cartela(104)
    c = f"""<div class="cont" style="grid-template-columns:auto auto;grid-template-rows:auto auto auto 1fr;justify-content:start;column-gap:14mm">
      <div class="bloque" style="grid-column:1/3"><div class="kick">Gin pole · piezas 06 a 09</div><h2>Tubo, orejas, ojo y cartelas</h2></div>
      {WEB["06"]}
      {guardar("09", ca.svg("09 · Cartela · 2", esc(ca)))}
      {guardar("07", o.svg("07 · Oreja · 2", esc(o)))}
      {guardar("08", oj.svg("08 · Ojo · 1", esc(oj)))}
      <dl class="ficha" style="grid-column:1/3;max-width:330mm">
        <dt>06 Tubo</dt><dd>2½" × 1/4" torneado a Ø 51,4 mm, abierto arriba (la pata de adentro puede salir por arriba). Lado largo {f(largo)} mm, lado corto {f(corto)} mm; la boca de arriba se corta a {f(90 - ALFA)}° y queda 8 mm sobre el ala. Huecos Ø 9,9 mm a 63,5 y 91,4 mm de la boca, de frente a atrás. 3 ranuras F de 10,5 × 11 mm.</dd>
        <dt>07 Orejas</dt><dd>2 piezas, paradas bajo el ala a x = 50 … 60 mm del centro. Hueco C Ø 13,1 mm para el pasador de arriba de la cabeza.</dd>
        <dt>08 Ojo</dt><dd>1 pieza colgada al centro bajo el ala. Punto B de la gin pole, hueco Ø 25 mm.</dd>
        <dt>09 Cartelas</dt><dd>2 piezas paradas a x = 12 … 22 mm a cada lado del tubo; unen el ala con el tubo.</dd>
      </dl>
    </div>"""
    hoja("06–09", "Gin pole · tubo, orejas, ojo y cartelas", "Al 6061-T6", "1 + 2 + 1 + 2", "ver vistas", c)
    indice("06 a 09 · Gin pole: tubo, orejas, ojo y cartelas")
    return largo, corto


def recortar(svg):
    """Los detalles muestran solo su ventana (la pata sigue más allá)."""
    import re
    return re.sub(r'(<svg viewBox="[^"]*" style=")', r'\1overflow:hidden;', svg, count=1)


def hoja_patas():
    tot, mac, hem = pata_afuera_vistas()
    hu = [(p, g.D38, "") for p in g.PI_HUECOS]
    pi = vista_tubo(g.PI_L, g.D_PATA, 38.1, hu, "13 · Pata de adentro · 3", f"Escala 1:{f((g.PI_L + 90) / 232, 2)}", 232,
                    arriba_txt="grabar «ÚLTIMO HUECO» junto al hueco 1", abajo_txt="grabar «ÚLTIMO HUECO» junto al hueco 7")
    WEB["13"] = pi
    c = f"""<div class="cont" style="grid-template-columns:250mm 1fr;grid-template-rows:auto auto 1fr">
      <div class="bloque" style="grid-column:1/3"><div class="kick">Piezas 10 y 13 · sierra, torno, taladro de pedestal</div><h2>Patas de afuera y de adentro</h2></div>
      <div class="bloque" style="gap:4mm">
        {guardar("10", tot.svg("10 · Pata de afuera completa · 7 (6 + 1 de repuesto)", esc(tot)))}
        <div style="display:flex;gap:8mm;align-items:start">{guardar("10m", recortar(mac.svg("Detalle del macho", esc(mac))))}{guardar("10h", recortar(hem.svg("Detalle de la hembra", esc(hem))))}</div>
        {pi}
      </div>
      <dl class="ficha" style="grid-column:2;grid-row:2/4">
        <dt>10 Cuerpo</dt><dd>Tubo 6061-T6 2" cédula 40 (Ø 60,3 × 3,91 mm, interior 52,5 mm), largo 902 mm. Hueco Ø 9,9 mm a 63,5 mm de la boca hembra. Ranura 10,5 × 11 mm en la boca, del mismo lado del hueco.</dd>
        <dt>11 Espiga</dt><dd>Tubo 2" × 1/4" (Ø 50,8 × 6,35 mm), largo 272 mm: 120 mm adentro del cuerpo y 152 mm afuera (macho). Hueco Ø 9,9 mm a 88,5 mm de la punta. 2 pernos fijos 3/8" grado 8 a 34 y 94 mm del escalón, a 90° del hueco.</dd>
        <dt>12 Tope</dt><dd>Perno de acero Ø 9,5 × 16 mm prensado en la espiga a 5,5 mm del escalón, del lado del hueco; sale 6 mm. Entra en la ranura de la hembra, del casquillo o del pie.</dd>
        <dt>Peso</dt><dd>{m2(kg('10'))} kg por pata de afuera (Vortex 2,5 kg).</dd>
        <dt>13 Adentro</dt><dd>Tubo 6061-T6 2" × 1/4" (Ø 50,8 mm), largo 965,2 mm. 7 huecos Ø 9,9 mm a 63,5 mm de cada punta y cada 139,7 mm. Se puede usar en cualquier sentido. {m2(kg('13'))} kg (Vortex 978 mm: se acortó 13 mm para que todo coincida).</dd>
        <dt>Ajuste</dt><dd>Todo Ø 50,8 mm (pata de adentro y machos) entra con juego de 0,6 mm en las bocas de Ø 51,4 mm; todo Ø 60,3 mm entra en el carrete azul de Ø 61 mm.</dd>
      </dl>
    </div>"""
    hoja("10–13", "Patas de afuera y de adentro", "Al 6061-T6", "7 + 3", "ver vistas", c)
    indice("10 a 13 · Patas de afuera (macho y hembra) y patas de adentro")


def hoja_pie_carrete():
    pie = dib_pie(84)
    dn, da, lado = dib_disco(True, 98), dib_disco(False, 98), dib_carrete_lado(84)
    c = f"""<div class="cont" style="grid-template-columns:auto auto auto auto;grid-template-rows:auto auto 1fr;column-gap:8mm;justify-content:space-between">
      <div class="bloque" style="grid-column:1/5"><div class="kick">Piezas 14, 15 y 16</div><h2>Pie de flecha y carrete de anclajes</h2></div>
      {guardar("14", pie.svg("14 · Pie de flecha · 3", esc(pie)))}
      {guardar("15", dn.svg("15 · Disco del carrete naranja · 1", esc(dn)))}
      {guardar("16", da.svg("16 · Disco del carrete azul · 1", esc(da)))}
      {guardar("carrete", lado.svg("Carrete armado · corte", esc(lado)))}
      <dl class="ficha" style="grid-column:1/5">
        <dt>14 Pie</dt><dd>Casquillo de tubo 2½" × 1/4" torneado a Ø 60,3 mm por fuera y Ø 51,4 mm por dentro, largo 140 mm; hueco Ø 9,9 mm a 63,5 mm de la boca y 3 ranuras F. Garra de acero A36 12 mm de láser soldada con MIG. Recibe la pata de adentro o el macho de una pata de afuera. El carrete azul entra por encima del casquillo.</dd>
        <dt>15 Naranja</dt><dd>Disco Ø 165 mm de 10 mm (láser) + tubo Ø 60,3 / 51,4 mm × 100 mm soldado con TIG. Centro con llave (2 ranuras) para el tope de la pata de afuera. Huecos Ø 9,9 mm a 35,6 · 63,5 · 91,4 mm de la cara de arriba. Entra sobre Ø 50,8 mm (pata de adentro o macho).</dd>
        <dt>16 Azul</dt><dd>Disco Ø 165 mm de 10 mm + tubo Ø 73 / 61 mm × 107 mm (barra Ø 80 torneada o tubo 3" × 3/8"). Huecos Ø 9,9 mm a 35,6 · 63,5 · 91,4 mm de la cara de abajo, en 2 filas a 90°. Entra sobre Ø 60,3 mm (pata de afuera, tubo naranja o pie).</dd>
        <dt>Juntos</dt><dd>Azul abajo, naranja arriba con su tubo dentro del azul: alto total 127 mm; los huecos de los 2 coinciden. 9 anclajes Ø 24 mm por disco; hueco chico Ø 10 mm arriba alineado con la llave (marca de posición, no es anclaje).</dd>
      </dl>
    </div>"""
    hoja("14–16", "Pie de flecha y carrete de anclajes", "Al 6061-T6 · acero A36", "3 + 1 + 1", "ver vistas", c)
    indice("14 a 16 · Pie de flecha y carrete de anclajes (naranja y azul)")


def hoja_ahp():
    v = dib_ahp(170)
    c = f"""<div class="cont" style="grid-template-columns:auto 1fr;grid-template-rows:auto 1fr;column-gap:12mm">
      <div class="bloque" style="grid-column:1/3"><div class="kick">Accesorio aparte · piezas 17 y 18 · para el vehículo</div><h2>Poste de enganche AHP</h2></div>
      {guardar("17", v.svg("17 · AHP · 1", esc(v)))}
      <div class="bloque" style="gap:4mm">
        <img class="render" src="{img('v8_acc')}" style="height:70mm">
        <dl class="ficha">
          <dt>17 AHP</dt><dd>Plancha Al 6061-T6 de 1" (25,4 mm), chorro de agua. {m2(kg('17'))} kg. La U de 52 mm recibe la pata de adentro (Ø 50,8 mm); el pasador 3/8" cruza las 2 puntas de canto (hueco Ø 9,9 mm a 27 mm de la punta, taladrado de lado) y el hueco de 63,5 mm de la pata: la pata puede girar.</dd>
          <dt>Anclajes</dt><dd>4 huecos Ø 25 mm para mosquetón. 2 orejas con ranura 16 × 24 mm solo para la maniota (no para personas).</dd>
          <dt>18 Adaptador</dt><dd>Acero A36: caja de 90 × 80 × 44 mm con ranura de 55 × 26,2 mm donde entra la lengüeta, pasador Ø 16 mm (5/8"); espiga de tubo cuadrado 2" × 2" × 1/4" de 230 mm que entra en el enganche del carro, hueco Ø 16,5 mm a 60 mm de la punta. Medir el enganche del carro antes de taladrar.</dd>
        </dl>
        <div class="aviso"><b>Prueba antes de usar</b>El original era un prototipo. Probar con 10 kN (≈ 1000 kg) sin personas antes del primer uso.</div>
      </div>
    </div>"""
    hoja("17–18", "Poste de enganche AHP", "Al 6061-T6 · acero A36", "1 + 1", "ver vistas", c)
    indice("17 y 18 · Poste de enganche AHP para el carro")


COMPRAS = [
    ("P1", "Pasador de bola con anillo 1/2\" (12,7 mm) × 2\" de agarre", "4 (+1)", "Acero inox 17-4 · ≥ 140 kN doble corte", "Los 4 de la cabeza (los 2 de arriba son la bisagra de la gin pole)."),
    ("P2", "Pasador de bola con anillo 3/8\" (9,5 mm) × 3\" de agarre", "17", "Acero inox 17-4 · ≥ 80 kN doble corte", "Uniones de patas, pies, carrete y AHP (como el Vortex: 17)."),
    ("T1", "Perno 3/8\"-16 × 3\" grado 8 + tuerca de seguridad", "14", "Acero aleado", "2 por pata de afuera (fijan la espiga)."),
    ("T2", "Perno de acero Ø 9,5 × 16 mm (tope)", "7", "Acero 1045", "Tope de alineación de cada pata de afuera."),
    ("R1", "Polea de 1,5\" (38 mm) con rodamiento, ≥ 36 kN", "2", "Aluminio / acero", "Una en cada pasador de abajo, dentro de la ranura."),
    ("C1", "Cinta de maniota 25 mm con hebilla de leva, 20 kN", "3 × 3,5 m", "Poliéster", "Entre los pies."),
    ("M1", "Plancha Al 6061-T6 de 10 mm", "1 × (700 × 450)", "Con certificado", "01, 03, 04, 05, 07, 08, 09 y discos 15 y 16."),
    ("M2", "Tubo Al 6061-T6 2½\" × 1/4\" (Ø 63,5 × 6,35 mm)", "1,0 m", "Con certificado", "02 × 2, 06, pies 14 × 3, tubo del carrete naranja."),
    ("M3", "Tubo Al 6061-T6 2\" céd. 40 (Ø 60,3 × 3,91 mm)", "7 × 902 mm", "Con certificado", "Cuerpos de las patas de afuera."),
    ("M4", "Tubo Al 6061-T6 2\" × 1/4\" (Ø 50,8 × 6,35 mm)", "3 × 965 + 7 × 272 mm", "Con certificado", "Patas de adentro y espigas."),
    ("M5", "Plancha Al 6061-T6 de 1\" · barra Ø 80 · A36 12 mm", "según plano", "—", "AHP, tubo del carrete azul, garras."),
    ("S1", "Varilla TIG ER5356 Ø 2,4 mm + argón puro", "1 kg", "—", "Soldadura de aluminio."),
]


def hoja_compras_fab():
    tr = "".join(f'<tr><td class="n">{a}</td><td><b>{escape(b)}</b></td><td class="m">{c}</td><td>{escape(d)}</td><td>{escape(e)}</td></tr>'
                 for a, b, c, d, e in COMPRAS)
    ps = "".join(f'<div class="paso"><span class="k">{i + 1}</span><div><b>{escape(a)}</b><p>{escape(b)}</p></div></div>' for i, (a, b) in enumerate(PASOS_TALLER))
    c = f"""<div class="cont" style="grid-template-columns:1fr 1fr">
      <div class="bloque" style="gap:4mm">
        <div class="bloque"><div class="kick">Compras y material</div><h2>Material, pasadores y cuerdas</h2></div>
        <table><thead><tr><th>Cód.</th><th>Qué</th><th>Cant.</th><th>Material</th><th>Dónde va</th></tr></thead><tbody>{tr}</tbody></table>
        <div class="aviso"><b>Si no hay aluminio 6061-T6</b>Hacer las placas en acero 4130 de 6 mm con el mismo contorno y los mismos huecos (pesa 1,7 veces más; TIG con varilla ER80S-D2). No usar aluminio 6063 ni acero de construcción común.</div>
      </div>
      <div class="bloque" style="gap:2.6mm">
        <div class="bloque"><div class="kick">Taller</div><h2>Orden de fabricación y soldadura</h2></div>
        {ps}
      </div>
    </div>"""
    hoja("FAB", "Material, soldadura y prueba", "—", "", "S/E", c)
    indice("Material, pasadores, orden de fabricación, soldadura y prueba de carga")


PASOS_TALLER = [
    ("Corte", "DXF al taller (carpeta dxf): plancha Al 6061-T6 de 10 mm; AHP en plancha de 1\" con chorro de agua; garras en A36 12 mm. Huecos de pasador de la cabeza a Ø 12 mm para escariar después."),
    ("Tubos", "Cortar y tornear: 2 casquillos de 153 mm, tubo de la gin pole, 3 casquillos de pie de 140 mm, tubo naranja de 100 mm (Ø 60,3 / 51,4 mm), tubo azul de 107 mm (Ø 73 / 61 mm), 7 cuerpos de 902 mm, 7 espigas de 272 mm, 3 patas de adentro de 965,2 mm."),
    ("Huecos", "TODOS con plantilla: primero el de 63,5 mm desde la boca, luego los demás. Pata de adentro: 63,5 mm y cada 139,7 mm. Taladro de pedestal con prisma en V; broca de 6 y luego 9,9 mm."),
    ("Patas de afuera", "Meter la espiga 120 mm en el cuerpo, taladrar los 2 pernos juntos a 34 y 94 mm del escalón y apretar. Prensar el tope a 5,5 mm del escalón. Probar que 2 patas se unan y el pasador entre solo."),
    ("Cabeza", "Placa 01 boca abajo; 4 aletas paradas en x = ±36 y ±64 mm con un eje de Ø 12 mm por los huecos; puente 04; casquillos con gabarit a " + f(g.ANG) + "°. Puntear, medir, soldar TIG alternando lados."),
    ("Gin pole y carrete", "Ala 05 boca abajo; orejas 07 a 50 … 60 mm; ojo 08; tubo 06 a " + f(ALFA) + "°; cartelas 09. Discos 15 y 16 soldados a sus tubos a escuadra (la llave del naranja alineada con el hueco chico)."),
    ("TIG", "Corriente alterna, varilla ER5356 Ø 2,4 mm, argón puro, precalentar a 120 °C. Filete de 6 mm. Si se puede: tratamiento T6 después de soldar."),
    ("Escariar", "Con la gin pole puesta, escariar los huecos de la cabeza a Ø 13,1 mm de una pasada."),
    ("Prueba", "Armar a " + f(ARM["altura_I2"], 0) + " mm con maniotas. Colgar 18 kN (≈ 1800 kg) del pasador de abajo por 3 minutos, sin personas. Si nada se deforma y los pasadores salen con la mano, se aprueba."),
]

PASOS_CAMPO = [
    "Elegir la forma: A (patas largas) o B (tubo arriba con carrete). Ver la hoja «Regla de huecos».",
    "Armar cada pata en el suelo. Forma A: casquillo → pata de afuera → pata de afuera → pata de adentro → pie. Revisar que la bola de cada pasador salga del otro lado.",
    "Poner la gin pole: sus 2 orejas entran en las ranuras de las aletas y se meten los 2 pasadores de arriba.",
    "Poner los 2 pasadores de abajo con una polea en cada uno.",
    "Levantar, abrir las 3 patas a la misma distancia y poner las maniotas entre los pies.",
    "Vientos si la carga puede tirar de lado. Cargar poco a poco, con cuerda de seguridad aparte.",
]


def svgs_corte():
    ala, ovalos, tubo = g.perfil_ala(ALFA)
    svg_corte("01_placa_frontal_x1", g.placa_frontal(), (), g.cortes_frontal(), "01 Placa frontal · Al 6061-T6 10 mm · 1")
    svg_corte("03_aleta_x4", g.ALETA[0], g.ALETA[1], (), "03 Aleta · Al 6061-T6 10 mm · 4")
    svg_corte("04_puente_central_x1", g.PUENTE[0], g.PUENTE[1], (), "04 Puente central · 1")
    svg_corte("05_ala_gin_pole_x1", ala, (), ovalos + [tubo], "05 Ala de la gin pole · 1")
    svg_corte("07_oreja_gin_pole_x2", g.OREJA[0], g.OREJA[1], (), "07 Oreja · 2")
    svg_corte("08_ojo_gin_pole_x1", g.OJO[0], g.OJO[1], (), "08 Ojo · 1")
    svg_corte("09_cartela_gin_pole_x2", g.perfil_cartela(ALFA), (), (), "09 Cartela · 2")
    svg_corte("14_garra_pie_A36_12mm_x3", g4.contorno_garra(), [h[:4] for h in g4.HUECOS_GARRA], (), "14 Garra del pie · 3")
    svg_corte("15_disco_carrete_naranja_x1", g.CAR_N[0], g.CAR_N[1], g.CAR_N[2], "15 Disco naranja · 1")
    svg_corte("16_disco_carrete_azul_x1", g.CAR_A[0], g.CAR_A[1], g.CAR_A[2], "16 Disco azul · 1")
    svg_corte("17_AHP_25mm_x1", g.AHP[0], g.AHP[1], g.AHP[2], "17 AHP · Al 25,4 mm · 1")


def revisar_cruces(html):
    """Comprueba que cada cruz roja esté centrada: sus 2 líneas se cortan en su punto medio."""
    import re
    ls = re.findall(r'<line class="cruz" x1="([-\d.]+)" y1="([-\d.]+)" x2="([-\d.]+)" y2="([-\d.]+)"/>', html)
    malas = 0
    for i in range(0, len(ls) - 1, 2):
        h_, v_ = [tuple(map(float, x)) for x in ls[i:i + 2]]
        if h_[1] != h_[3] or v_[0] != v_[2]:
            continue
        cx, cy = (h_[0] + h_[2]) / 2, (v_[1] + v_[3]) / 2
        if abs(cx - v_[0]) > 0.01 or abs(cy - h_[1]) > 0.01:
            malas += 1
    return len(ls) // 2, malas


# ------------------------------------------------------------------ generar

if __name__ == "__main__":
    exec(open(os.path.join(AQUI, "v8_cadenas.py")).read())
    hoja_lista()
    hoja_regla()
    hoja_armado_cabeza()
    hoja_piezas_cabeza_1()
    hoja_piezas_cabeza_2()
    largo_gin, corto_gin = hoja_gin()
    hoja_patas()
    hoja_pie_carrete()
    hoja_ahp()
    hoja_compras_fab()
    hoja_portada()
    HOJAS.insert(0, HOJAS.pop())
    svgs_corte()
    total = len(HOJAS)
    html = (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>VX-EC Trípode v8 · planos</title>'
            f'<style>{CSS8}</style></head><body>' + "".join(banner(render_hoja(h, i + 1, total)) for i, h in enumerate(HOJAS)) + "</body></html>")
    n_cruces, malas = revisar_cruces(html)
    print("cruces", n_cruces, "descentradas", malas)
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(html)
    datos = dict(dibujos=WEB, compras=COMPRAS, taller=PASOS_TALLER, campo=PASOS_CAMPO,
                 lista=[dict(n=n, nombre=nom, material=mat, cant=q, kg=round(kg(pid, dens), 2)) for n, nom, mat, q, pid, dens in LISTA],
                 alturas=[dict(ext=ne, hueco=hu, h=round(trip(ne, hu)[0]), lado=round(trip(ne, hu)[1])) for ne in (1, 2, 3) for hu in (1, 3, 6)],
                 kg_cabeza=round(kg_cabeza(), 2), kg_gin=round(kg_gin(), 2), alfa=ALFA, gin_largo=round(largo_gin, 1), gin_corto=round(corto_gin, 1))
    json.dump(datos, open(os.path.join(BASE, "web", "dibujos.json"), "w"), ensure_ascii=False)
    print("hojas", total, "bytes", len(html), "dibujos", len(WEB))
