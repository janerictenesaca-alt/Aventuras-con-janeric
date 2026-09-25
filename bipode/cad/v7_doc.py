"""Planos del trípode tipo Vortex v7 (placas de corte láser soldadas con TIG), A3 horizontal.

Uso:  python3 v7_doc.py <carpeta_imagenes> <carpeta_fuentes>
Salida:  ../v7/plano/index.html (para imprimir a PDF), ../v7/svg/*.svg (piezas planas a escala 1:1)
         ../v7/web/dibujos.json (dibujos para la página)
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
import v7_geo as g
from v4_dibujo import Vista, f

img, hoja, render_hoja, CSS, vista_tubo, pulg = (ns["img"], ns["hoja"], ns["render_hoja"], ns["CSS"],
                                                  ns["vista_tubo"], ns["pulg"])
HOJAS = ns["HOJAS"]
HOJAS.clear()
ns["TITULO"] = "Trípode tipo Vortex · placas soldadas"
ns["PROY"] = "VX-EC"
ns["REV"] = "C"
ns["FECHA"] = "25-09-2026"
INDICE = []

BASE = os.path.join(AQUI, "..", "v7")
OUT = os.path.join(BASE, "plano")
for d in ("plano", "svg", "web"):
    os.makedirs(os.path.join(BASE, d), exist_ok=True)
ARM = json.load(open(os.path.join(BASE, "armado.json")))
VOL = {p["id"]: p["vol"] for p in ARM["piezas"]}
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
    boca = -g4.ESPIGA_DENTRO + (g4.PE_ESPIGA - g4.PE_ESPIGA_DENTRO) + n_ext * g4.PE_TUBO
    s_pi = boca - g4.PE_HUECO_BOCA - g4.PI_HUECOS[hueco - 1]
    s_pie = s_pi + g4.PI_L - g4.ESPIGA_DENTRO
    return s_pie + g4.PIE_CAS_L - g4.GARRA_PUNTA


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
    v = Vista(minx - 78, miny - 42, maxx + 40, maxy + 30, ancho)
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


def dib_trasera(ancho):
    p, cs = g.TRASERA
    v = Vista(-58, -26, 62, 126, ancho)
    v.forma(p.difference(cs[0]).difference(cs[1]), "pieza")
    v.linea((0, -6), (0, 118), "eje")
    v.cota_h(-g.X_ALETA_INT, g.X_ALETA_INT, 0, -14, f(2 * g.X_ALETA_INT))
    v.cota_v(0, g.TRASERA_TOPE, g.X_ALETA_INT, g.X_ALETA_INT + 12, f(g.TRASERA_TOPE))
    v.cota_v(0, g.SILLA_Z, 0, -48, f(g.SILLA_Z))
    b = cs[0].bounds
    v.cota_h(b[0], b[2], b[3], 116, f(b[2] - b[0]))
    v.cota_v(b[1], b[3], b[2], b[2] + 22, f"{f(b[1])}–{f(b[3])}")
    v.nota(-12, 60, -40, 70, "R 9")
    v.nota(-6, 30, -40, 40, "corazón B (igual a la 01)")
    v.nota(-24, 102, -44, 118, "silla D (paso de cuerda)")
    return v


def dib_fondo(ancho):
    p, hs = g.FONDO
    v = Vista(-52, -80, 58, 26, ancho)
    v.forma(p, "pieza")
    for n, x, y, d in hs:
        v.circulo(x, y, d / 2)
        v.eje_cruz(x, y, d / 2)
    v.cota_h(-g.X_ALETA_INT, g.X_ALETA_INT, g.Y_TRASERA[1], -70, f(2 * g.X_ALETA_INT))
    v.cota_v(g.Y_TRASERA[1], g.Y_FRENTE[0], g.X_ALETA_INT, g.X_ALETA_INT + 12, f(g.Y_FRENTE[0] - g.Y_TRASERA[1]))
    v.cota_v(g.C_HUECO[1], g.Y_FRENTE[0], -g.X_ALETA_INT, -g.X_ALETA_INT - 10, f(g.Y_FRENTE[0] - g.C_HUECO[1]))
    v.diametro(*g.C_HUECO, g.D_MOSQ / 2, 40, "C · Ø 22")
    v.texto(0, 16, "adelante (placa 01)", 0.75)
    return v


def dib_escuadra(ancho):
    p = g.ESCUADRA
    minx, miny, maxx, maxy = p.bounds
    v = Vista(minx - 20, miny - 20, maxx + 30, maxy + 16, ancho)
    v.forma(p, "pieza")
    v.cota_h(minx, maxx, miny, miny - 10, f(maxx - minx))
    v.cota_v(miny, maxy, minx, minx - 10, f(maxy - miny))
    v.nota(maxx - 6, 0, maxx - 2, maxy + 8, "= tubo")
    v.texto(minx + 3, maxy - 5, "aleta de afuera", 0.7, "start")
    return v


def dib_ala(ancho):
    ala, ovalos, tubo = g.perfil_ala(ALFA)
    minx, miny, maxx, maxy = ala.bounds
    v = Vista(minx - 62, miny - 22, maxx + 30, maxy + 26, ancho)
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
def tubo_cas(ancho):
    hu = [(p, g.D38, "") for p in g.__dict__.get("G1", [38.0, 59.7, 81.4, 103.0, 124.8])]
    return vista_tubo(g.CAS_L, g.CAS_OD, g.CAS_ID, hu, "02 · Casquillo · 5 huecos G de frente", f"Escala 1:{f((g.CAS_L + 90) / ancho, 2)}", ancho,
                      ranuras=[(g.CAS_L - 14.0, 11.0, 14.0)], arriba_txt="boca de arriba (abierta)", abajo_txt="boca (pata)")


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
    v.rect(0, -5.5, 14, 11, "hueco")
    for p in (50.0, 80.0):
        v.circulo(p, 0, g.D38 / 2)
        v.linea((p, -r - 5), (p, r + 5), "eje")
    v.cota_h(0, 50, r, r + 10, "50")
    v.cota_h(0, 80, r, r + 20, "80")
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
    v.cota_v(0, g.ZT, -g.XC, -g.XC - 16 if False else -175, f(g.ZT))
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
    s.rect(g.Y_TRASERA[0], 0, T, g.TRASERA_TOPE, "oculta")
    s.rect(g.Y_TRASERA[1], 0, g.Y_FRENTE[0] - g.Y_TRASERA[1], T, "oculta")
    s.rect(-30, g.ESC_Z[0], 42, T, "oculta")
    s.cota_h(g.Y_ATRAS, g.Y_FRENTE[1], 0, -18, f(g.Y_FRENTE[1] - g.Y_ATRAS))
    s.cota_h(g.PIN_Y, 0, 110, 128 if False else 118, f(-g.PIN_Y))
    s.cota_h(0, g.Y_FRENTE[1], 156.9, 166, f(g.Y_FRENTE[1]))
    s.cota_h(-r, r, -8.4, -26, "63,5")
    s.texto(-44, 150, "tubo (casquillo)", 0.75, "end")
    s.texto(g.Y_FRENTE[1] + 2, 60, "01", 0.9, "start", "etq")
    s.texto(g.Y_ATRAS + 3, 58, "03", 0.9, "start", "etq")
    s.texto(g.Y_TRASERA[0] - 4, 12, "04", 0.9, "end", "etq")
    s.texto(-25, 4, "05", 0.8, "middle", "etq")
    s.texto(-8, g.ESC_Z[1] + 3, "06", 0.8, "middle", "etq")
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
    t.rect(-g.X_ALETA_INT, g.Y_TRASERA[0], 2 * g.X_ALETA_INT, T, "pieza")
    t.rect(-g.X_ALETA_INT, g.Y_TRASERA[1], 2 * g.X_ALETA_INT, g.Y_FRENTE[0] - g.Y_TRASERA[1], "pieza3")
    t.circulo(*g.C_HUECO, g.D_MOSQ / 2)
    from shapely.affinity import scale as sc
    for poly in (g.ESCUADRA, sc(g.ESCUADRA, -1, 1, origin=(0, 0))):
        t.forma(poly, "pieza")
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
    v.texto(-180, 26, "07 ala", 0.8, "middle", "etq")
    v.texto(-100, -8, "11 cartela", 0.8, "middle", "etq")
    v.texto(10, -24, "09 oreja", 0.8, "start", "etq")
    v.texto(-35, -52, "10 ojo", 0.8, "middle", "etq")
    v.texto(-200, -60, "08 tubo", 0.8, "middle", "etq")
    v.texto(0, 16, "pasador de arriba", 0.7, "middle")
    return v


# ------------------------------------------------------------------ hojas
def hoja_portada():
    filas = "".join(f'<tr><td class="m" style="width:12mm">{i + 2:02d}</td><td>{escape(t)}</td></tr>' for i, t in enumerate(INDICE))
    h, lado, tau, phi = trip(2, 1)
    c = f"""<div class="cont" style="grid-template-columns:150mm 1fr">
      <div class="bloque" style="gap:6mm;align-content:space-between">
        <div class="bloque" style="gap:4mm">
          <div class="kick">Juego de planos de fabricación · Rev. C</div>
          <h1 style="font-size:54pt;font-weight:700;line-height:.9">VX-EC<br><span style="color:var(--azul)">Trípode</span><br>tipo Vortex</h1>
          <p class="lead">Copia del Arizona Vortex armado como trípode. La cabeza A-frame (azul) y la gin pole (naranja) se hacen con
          placas de aluminio 6061-T6 de 10 mm cortadas con láser y soldadas con TIG, más tubo 2½" × 1/4".</p>
        </div>
        <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:5mm">
          <div class="cifra"><b>{m2(h / 1000)} m</b><span>altura al pasador de abajo · 2 patas de afuera (Vortex 2,41 m)</span></div>
          <div class="cifra"><b>417 × 165</b><span>cabeza A-frame, mm (igual al Vortex)</span></div>
          <div class="cifra"><b>{m2(kg_cabeza())} kg</b><span>cabeza A-frame soldada (Vortex 2,3 kg)</span></div>
          <div class="cifra"><b>{m2(kg_gin())} kg</b><span>gin pole soldada (Vortex 1,0 kg)</span></div>
        </div>
        <div class="bloque"><h3>Contenido</h3><table><tbody>{filas}</tbody></table></div>
        <div class="ficha">
          <dt>Cliente</dt><dd>Aventuras con Janeric · Morona Santiago, Ecuador</dd>
          <dt>Referencia</dt><dd>Arizona Vortex · Rock Exotica · manual y 164 fotos</dd>
          <dt>Reemplaza</dt><dd>Rev. B (cabeza maquinada): ya no se usa</dd>
        </div>
      </div>
      <div style="display:grid;grid-template-rows:1fr 1fr;gap:6mm">
        <img class="render" src="{img('v7_t')}" style="height:118mm;justify-self:center">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:6mm;align-items:center">
          <img class="render" src="{img('v7_ciso')}" style="height:80mm">
          <img class="render" src="{img('v7_af')}" style="height:60mm">
        </div>
      </div>
    </div>"""
    hoja("—", "Portada", "—", "", "S/E", c)


def kg_cabeza():
    return sum(kg(p) for p in ("01", "02a", "02b", "03a", "03b", "03c", "03d", "04", "05", "06a", "06b"))


def kg_gin():
    return sum(kg(p) for p in ("07", "08", "09a", "09b", "10", "11a", "11b"))


LISTA = [
    ("01", "Placa frontal (cara lisa)", "Al 6061-T6 10 mm · láser", 1, "01"),
    ("02", "Casquillo", "Tubo Al 6061-T6 2½\" × 1/4\" × 153", 2, "02a"),
    ("03", "Aleta (oreja de la cabeza)", "Al 6061-T6 10 mm · láser", 4, "03a"),
    ("04", "Placa trasera central", "Al 6061-T6 10 mm · láser", 1, "04"),
    ("05", "Placa de fondo (hueco C)", "Al 6061-T6 10 mm · láser", 1, "05"),
    ("06", "Escuadra lateral", "Al 6061-T6 10 mm · láser", 2, "06a"),
    ("07", "Ala de la gin pole", "Al 6061-T6 10 mm · láser", 1, "07"),
    ("08", "Tubo de la gin pole", "Tubo Al 6061-T6 2½\" × 1/4\"", 1, "08"),
    ("09", "Oreja de la gin pole", "Al 6061-T6 10 mm · láser", 2, "09a"),
    ("10", "Ojo central de la gin pole", "Al 6061-T6 10 mm · láser", 1, "10"),
    ("11", "Cartela de la gin pole", "Al 6061-T6 10 mm · láser", 2, "11a"),
    ("21", "Pata de afuera", "Tubo Al 6061-T6 2\" céd. 40 + espigón 2\" × 1/4\"", 6, "21I1"),
    ("22", "Pata de adentro", "Tubo Al 6061-T6 2\" × 1/4\" × 980", 3, "22I"),
    ("23", "Pie Raptor", "Acero A36 · garra 12 mm láser + tubo", 3, "23I"),
]


def hoja_lista():
    filas = ""
    for n, nom, mat, q, pid in LISTA:
        dens = AC if n == "23" else AL
        filas += (f'<tr><td class="n">{n}</td><td><b>{escape(nom)}</b></td><td>{escape(mat)}</td><td class="m">{q}</td>'
                  f'<td class="m">{m2(kg(pid, dens))}</td><td class="m">{m2(kg(pid, dens) * q)}</td></tr>')
    alt = ""
    for ne in (1, 2, 3):
        for hu in (1, 3, 6):
            h, lado, tau, phi = trip(ne, hu)
            alt += f'<tr{" class=dest" if (ne, hu) == (2, 1) else ""}><td class="m">{ne}</td><td class="m">{hu}</td><td class="m">{m2(h / 1000)} m</td><td class="m">{m2(lado / 1000)} m</td></tr>'
    c = f"""<div class="cont" style="grid-template-columns:1fr 120mm">
      <div class="bloque" style="gap:4mm">
        <div class="bloque"><div class="kick">Todas las piezas, numeradas</div><h2>Lista de piezas</h2></div>
        <table><thead><tr><th>N.º</th><th>Pieza</th><th>Material</th><th>Cant.</th><th>kg c/u</th><th>kg total</th></tr></thead><tbody>{filas}</tbody></table>
        <div class="aviso"><b>Numeración</b>01 a 06 = cabeza A-frame (azul) · 07 a 11 = gin pole (naranja) · 21 a 23 = patas y pies. Grabar el número en cada pieza con marcador de metal antes de soldar.</div>
      </div>
      <div class="bloque" style="gap:4mm">
        <img class="render" src="{img('v7_t')}" style="height:92mm;justify-self:center">
        <h3>Alturas (trípode de patas iguales)</h3>
        <table><thead><tr><th>Patas de afuera</th><th>Hueco pata de adentro</th><th>Altura al pasador</th><th>Lado del triángulo</th></tr></thead><tbody>{alt}</tbody></table>
        <p style="font-size:8pt;color:var(--gris)">Hueco 1 = pata de adentro metida lo menos posible. Vortex: 2,41 m con 2 patas de afuera · 3,20 m con 3.</p>
      </div>
    </div>"""
    hoja("LISTA", "Lista de piezas y alturas", "Varios", "", "S/E", c)
    indice("Lista de piezas numeradas y tabla de alturas")


def hoja_armado_cabeza():
    fr, la, ar = conjunto_cabeza(215, 100, 215)
    c = f"""<div class="cont" style="grid-template-columns:1fr 112mm;grid-template-rows:auto auto 1fr;grid-template-areas:'t t' 'f l' 'a l'">
      <div class="bloque" style="grid-area:t"><div class="kick">Cabeza A-frame · 11 piezas soldadas con TIG</div><h2>Armado de la cabeza A-frame</h2></div>
      <div style="grid-area:f">{guardar("arm_cab_frente", fr.svg("Vista de frente (cara lisa) · aletas en línea oculta", esc(fr)))}</div>
      <div class="bloque" style="grid-area:l;gap:5mm">{guardar("arm_cab_lado", la.svg("Vista de lado", esc(la)))}
        <img class="render" src="{img('v7_ab')}" style="height:46mm">
      </div>
      <div style="grid-area:a">{guardar("arm_cab_arriba", ar.svg("Vista de arriba · posición de cada placa", esc(ar)))}</div>
    </div>"""
    hoja("01–06", "Armado de la cabeza A-frame", "Al 6061-T6", "1 juego", "ver vistas", c,
         "Las 4 aletas son iguales. Soldar primero con puntos y medir antes de cordón completo.")
    indice("Armado de la cabeza A-frame (vistas con posiciones)")


def hoja_piezas_cabeza_1():
    v1 = dib_frontal(236)
    tub = tubo_cas(132)
    WEB["02"] = tub
    c = f"""<div class="cont" style="grid-template-columns:245mm 1fr;grid-template-rows:auto 1fr">
      <div class="bloque" style="grid-column:1/3"><div class="kick">Piezas 01 y 02</div><h2>Placa frontal y casquillos</h2></div>
      <div class="bloque">{guardar("01", v1.svg("01 · Placa frontal (cara lisa) · 1 pieza", esc(v1)))}
        <dl class="ficha">
          <dt>01</dt><dd>Al 6061-T6 10 mm, láser o chorro de agua. {m2(kg('01'))} kg. Es la cara lisa del Vortex: una sola pieza. Grabado opcional: "AVENTURAS CON JANERIC", serie y "Prueba __ kN".</dd>
          <dt>Bordes</dt><dd>Los 2 bordes laterales tocan el tubo por atrás; adelante queda una V para soldar y luego se lija al ras. Redondear R 1 los bordes de las ventanas E, el corazón B y las muescas (no dañan cuerdas ni cintas).</dd>
        </dl>
      </div>
      <div class="bloque" style="gap:4mm">{tub}
        <dl class="ficha">
          <dt>02</dt><dd>Tubo 6061-T6 2½" × 1/4" (Ø 63,5 × 6,35), largo 153, 2 piezas. Tornear por dentro a Ø 51,4 H8. {m2(kg('02a'))} kg c/u.</dd>
          <dt>Huecos G</dt><dd>5 × Ø 9,9 pasantes de frente a atrás a 38 · 59,7 · 81,4 · 103 · 124,8 de la boca de arriba. 2 × Ø 9,9 pasantes de lado (a 90°) a 85 y 106. Hueco Ø 5 a 22 de la boca de abajo para el cordón del pasador.</dd>
          <dt>Ranuras F</dt><dd>3 ranuras de 11 × 14 en la boca de abajo, a 0°, 120° y 240°.</dd>
          <dt>Posición</dt><dd>Eje a {f(g.ANG)}° de la vertical, boca de arriba centrada en x = ±{f(g.XC)}, z = {f(g.ZT)}. Eje del tubo a 17 mm detrás de la cara de atrás de la placa 01 (y = 0).</dd>
        </dl>
      </div>
    </div>"""
    hoja("01–02", "Placa frontal y casquillos", "Al 6061-T6", "1 + 2", "ver vistas", c)
    indice("01 y 02 · Placa frontal y casquillos")


def hoja_piezas_cabeza_2():
    a = dib_aleta(106)
    t = dib_trasera(104)
    fo = dib_fondo(96)
    e = dib_escuadra((g.ESCUADRA.bounds[2] - g.ESCUADRA.bounds[0] + 50) / 1.15)
    c = f"""<div class="cont" style="grid-template-columns:repeat(4,auto);grid-template-rows:auto 1fr auto;justify-content:space-between">
      <div class="bloque" style="grid-column:1/5"><div class="kick">Piezas 03 a 06 · Al 6061-T6 10 mm · escala 1:1,15</div><h2>Aletas y placas de atrás</h2></div>
      {guardar("03", a.svg("03 · Aleta · 4 piezas iguales", "2 × Ø 13,1"))}
      {guardar("04", t.svg("04 · Placa trasera · 1", "ventana + corazón"))}
      {guardar("05", fo.svg("05 · Placa de fondo · 1", "hueco C"))}
      {guardar("06", e.svg("06 · Escuadra · 2", "1 normal + 1 dada vuelta"))}
      <table style="grid-column:1/5"><thead><tr><th>N.º</th><th>Pieza</th><th>Cant.</th><th>Dónde va</th><th>kg c/u</th></tr></thead><tbody>
        <tr><td class="n">03</td><td>Aleta</td><td class="m">4</td><td>Soldada de canto contra la cara de atrás de la placa 01, parada (vertical). Caras de adentro a x = ±36 y ±64 del centro. Entre cada par queda la ranura de 18 donde entra la oreja 09 de la gin pole y cuelgan la polea y los mosquetones.</td><td class="m">{m2(kg('03a'))}</td></tr>
        <tr><td class="n">04</td><td>Placa trasera</td><td class="m">1</td><td>Entre las 2 aletas de adentro, al ras del borde de atrás (y = −66 … −56). Su corazón queda en línea con el de la 01.</td><td class="m">{m2(kg('04'))}</td></tr>
        <tr><td class="n">05</td><td>Placa de fondo</td><td class="m">1</td><td>Acostada abajo (z = 0 … 10) entre las aletas de adentro, de la placa 01 a la 04. Hueco C vertical para mosquetón.</td><td class="m">{m2(kg('05'))}</td></tr>
        <tr><td class="n">06</td><td>Escuadra</td><td class="m">2</td><td>Acostada arriba (z = 100 … 110) de la aleta de afuera al tubo. El corte curvo abraza el tubo.</td><td class="m">{m2(kg('06a'))}</td></tr>
      </tbody></table>
    </div>"""
    hoja("03–06", "Aletas, placa trasera, fondo y escuadras", "Al 6061-T6 10 mm", "4 + 1 + 1 + 2", "1:1,15", c,
         "Huecos de pasador Ø 13,1: cortar a Ø 12 con láser y escariar a 13,1 después de soldar, con las 4 aletas en línea.")
    indice("03 a 06 · Aletas, placa trasera, placa de fondo y escuadras")


def hoja_gin():
    arm = conjunto_gin(210)
    ala = dib_ala(118)
    c = f"""<div class="cont" style="grid-template-columns:132mm 1fr;grid-template-rows:auto 1fr">
      <div class="bloque" style="grid-column:1/3"><div class="kick">Gin pole (naranja) · piezas 07 a 11 · Al 6061-T6</div><h2>Gin pole · armado y ala</h2></div>
      <div class="bloque">{guardar("07", ala.svg("07 · Ala (escudo) · 1", esc(ala)))}</div>
      <div class="bloque" style="gap:5mm">
        {guardar("arm_gin", arm.svg("Armado · vista de lado (ala horizontal)", esc(arm)))}
        <div style="display:grid;grid-template-columns:1fr 80mm;gap:6mm;align-items:start">
        <dl class="ficha">
          <dt>07 Ala</dt><dd>Plancha 10 mm, {m2(kg('07'))} kg. 4 óvalos D para anclajes radiales y hueco elíptico por donde pasa el tubo inclinado.</dd>
          <dt>Bisagra</dt><dd>Las orejas 09 entran en las ranuras de la cabeza y el pasador de arriba de cada lado las atraviesa: la gin pole gira como en el Vortex.</dd>
          <dt>Ángulo</dt><dd>El tubo va a {f(ALFA)}° del ala. Así el ala queda horizontal con el trípode parado y las 3 patas iguales.</dd>
        </dl>
        <img class="render" src="{img('v7_ciso')}" style="height:52mm">
        </div>
      </div>
    </div>"""
    hoja("07", "Gin pole · armado y ala", "Al 6061-T6", "1 juego", "ver vistas", c)
    indice("07 · Gin pole: armado y ala")
    tub, largo, corto = tubo_gin(170)
    WEB["08"] = tub.svg("08 · Tubo de la gin pole · 1", esc(tub))
    o, oj, ca = dib_oreja(80), dib_ojo(76), dib_cartela(104)
    c = f"""<div class="cont" style="grid-template-columns:auto auto;grid-template-rows:auto auto auto 1fr;justify-content:start;column-gap:14mm">
      <div class="bloque" style="grid-column:1/3"><div class="kick">Gin pole · piezas 08 a 11</div><h2>Tubo, orejas, ojo y cartelas</h2></div>
      {WEB["08"]}
      {guardar("11", ca.svg("11 · Cartela · 2", esc(ca)))}
      {guardar("09", o.svg("09 · Oreja · 2", esc(o)))}
      {guardar("10", oj.svg("10 · Ojo · 1", esc(oj)))}
      <dl class="ficha" style="grid-column:1/3;max-width:330mm">
        <dt>08 Tubo</dt><dd>2½" × 1/4" torneado a Ø 51,4. Lado largo {f(largo)}, lado corto {f(corto)}: la boca de arriba se corta a {f(90 - ALFA)}° y queda 8 mm sobre el ala. 2 huecos Ø 9,9 a 50 y 80 de la boca, de frente a atrás. 3 ranuras F de 11 × 14. {m2(kg('08'))} kg.</dd>
        <dt>09 Orejas</dt><dd>2 piezas, paradas bajo el ala a x = 50 … 60 del centro (dentro de las ranuras de la cabeza). Hueco C Ø 13,1: ahí pasa el pasador de arriba de la cabeza.</dd>
        <dt>10 Ojo</dt><dd>1 pieza colgada al centro bajo el ala (y = −40 … −30 desde el pasador). Punto B de la gin pole, hueco Ø 25 para mosquetón.</dd>
        <dt>11 Cartelas</dt><dd>2 piezas paradas a x = 12 … 22 a cada lado del tubo; el borde inclinado se apoya en el tubo. Unen el ala con el tubo.</dd>
      </dl>
    </div>"""
    hoja("08–11", "Gin pole · tubo, orejas, ojo y cartelas", "Al 6061-T6", "1 + 2 + 1 + 2", "ver vistas", c)
    indice("08 a 11 · Gin pole: tubo, orejas, ojo y cartelas")
    return largo, corto


def hoja_patas():
    fuera = g4.PE_ESPIGA - g4.PE_ESPIGA_DENTRO
    L = g4.PE_TOTAL
    hu = [(g4.PE_HUECO_ESPIGA, g4.D38, ""), (fuera + g4.PE_PERNOS[0], g4.D38, ""), (fuera + g4.PE_PERNOS[1], g4.D38, ""),
          (L - g4.PE_HUECO_BOCA, g4.D38, "")]
    pe = vista_tubo(L, g4.EXT_OD, g4.EXT_OD - 2 * g4.EXT_E, hu, "21 · Pata de afuera · 6", "Escala 1:5", 245,
                    ranuras=[(L - g4.RANURA_P, g4.RANURA_A, g4.RANURA_P)], arriba_txt="espigón (va a la cabeza o a otra pata)",
                    abajo_txt="boca con 3 ranuras")
    hu = [(p, g4.D38, "") for p in g4.PI_HUECOS] + [(g4.PI_HUECO_PIE, g4.D38, "")]
    pi = vista_tubo(g4.PI_L, g4.MACHO_OD, g4.MACHO_OD - 2 * g4.MACHO_E, hu, "22 · Pata de adentro · 3", "Escala 1:5", 228,
                    arriba_txt="muesca 11 × 22", abajo_txt="va al pie")
    WEB["21"], WEB["22"] = pe, pi
    G = g4.contorno_garra()
    minx, miny, maxx, maxy = G.bounds
    v = Vista(minx - 35, miny - 28, maxx + 40, g4.PIE_CAS_L + 30, 100)
    v.rect(-g4.HEMBRA_OD / 2, 0, g4.HEMBRA_OD, g4.PIE_CAS_L, "pieza3")
    v.forma(G.difference(box(-g4.HEMBRA_OD / 2, 0, g4.HEMBRA_OD / 2, 200)), "pieza2")
    for n, x, y, d, _ in g4.HUECOS_GARRA:
        v.circulo(x, y, d / 2)
        v.eje_cruz(x, y, d / 2)
    v.circulo(0, g4.PIE_CAS_L - g4.PIE_HUECO, g4.D38 / 2)
    v.linea((0, miny - 8), (0, g4.PIE_CAS_L + 8), "eje")
    v.cota_h(minx, maxx, miny, miny - 14)
    v.cota_v(g4.GARRA_PUNTA, g4.PIE_CAS_L, maxx, maxx + 24, f(g4.PIE_CAS_L - g4.GARRA_PUNTA))
    v.cota_v(g4.PIE_CAS_L - g4.PIE_HUECO, g4.PIE_CAS_L, -g4.HEMBRA_OD / 2, -g4.HEMBRA_OD / 2 - 12, "50")
    pie = guardar("23", v.svg("23 · Pie Raptor · 3", "Escala 1:2,5 · garra A36 12 mm"))
    c = f"""<div class="cont" style="grid-template-columns:250mm 1fr">
      <div class="bloque" style="gap:6mm">
        <div class="bloque"><div class="kick">Piezas 21 y 22 · sierra, taladro de pedestal y fresa</div><h2>Patas y pies</h2></div>
        {pe}{pi}
        <dl class="ficha">
          <dt>21 Afuera</dt><dd>Tubo 6061-T6 2" cédula 40 (Ø 60,3 × 3,91) de {f(g4.PE_TUBO)} + espigón 2" × 1/4" de {f(g4.PE_ESPIGA)} metido {f(g4.PE_ESPIGA_DENTRO)}, fijado con 2 pernos 3/8" grado 8. Largo total {f(L)} (Vortex 1054). {m2(kg('21I1'))} kg.</dd>
          <dt>22 Adentro</dt><dd>Tubo 6061-T6 2" × 1/4" (Ø 50,8) de {f(g4.PI_L)} (Vortex 978). 6 huecos cada 150 desde 60 + 1 a 50 de abajo para el pie. {m2(kg('22I'))} kg.</dd>
        </dl>
      </div>
      <div class="bloque" style="gap:4mm">{pie}
        <dl class="ficha">
          <dt>23 Raptor</dt><dd>Casquillo de acero Ø 63,5 × 6 de 120 + garra A36 12 mm de láser, soldada con MIG por los 2 lados. Punta con recargue duro. {m2(kg('23I', AC))} kg.</dd>
        </dl>
        <div class="aviso"><b>Orden de una pata</b>Cabeza → pata de afuera → pata de afuera → pata de adentro → pie. La pata de adentro va siempre abajo (manual del Vortex).</div>
      </div>
    </div>"""
    hoja("21–23", "Patas y pies", "Al 6061-T6 · acero A36", "6 + 3 + 3", "1:5", c)
    indice("21 a 23 · Patas de afuera, patas de adentro y pies Raptor")


COMPRAS = [
    ("P1", "Pasador de bola con anillo 1/2\" (12,7) × 2\" de agarre", "4 (+1)", "Acero inox 17-4 · ≥ 140 kN doble corte", "Los 4 de la cabeza. Los 2 de arriba también son la bisagra de la gin pole."),
    ("P2", "Pasador de bola con anillo 3/8\" (9,5) × 3\" de agarre", "12 (+2)", "Acero inox 17-4 · ≥ 80 kN doble corte", "Pata en cabeza/gin pole, uniones de patas y pies."),
    ("T1", "Perno hexagonal 3/8\"-16 × 3\" grado 8 + tuerca de seguridad", "12", "Acero aleado", "Espigón de cada pata de afuera (2 por pata)."),
    ("R1", "Polea de 1,5\" (38 mm) para cuerda de 11 mm, ≥ 36 kN", "1", "Aluminio / acero", "En el pasador de abajo izquierdo, dentro de la ranura."),
    ("C1", "Cinta de maniota 25 mm con hebilla de leva, 20 kN", "3 × 3,5 m", "Poliéster", "Entre los pies."),
    ("C2", "Cuerda estática 11 mm para vientos", "4 × 15 m", "Poliamida", "A los anclajes, a 45°."),
    ("M1", "Plancha Al 6061-T6 de 10 mm", "1 × (600 × 400)", "Con certificado", "Todas las placas láser (01, 03–07, 09–11)."),
    ("M2", "Tubo Al 6061-T6 2½\" × 1/4\" (Ø 63,5 × 6,35)", "600 mm", "Con certificado", "02 × 2 (153) + 08 × 1 (≈ 160) + sobrante."),
    ("S1", "Varilla TIG ER5356 Ø 2,4 + argón puro", "1 kg", "—", "Soldadura de la cabeza y la gin pole."),
]


def hoja_compras_fab(largo_gin):
    tr = "".join(f'<tr><td class="n">{a}</td><td><b>{escape(b)}</b></td><td class="m">{c}</td><td>{escape(d)}</td><td>{escape(e)}</td></tr>'
                 for a, b, c, d, e in COMPRAS)
    pasos = PASOS_TALLER
    ps = "".join(f'<div class="paso"><span class="k">{i + 1}</span><div><b>{escape(a)}</b><p>{escape(b)}</p></div></div>' for i, (a, b) in enumerate(pasos))
    c = f"""<div class="cont" style="grid-template-columns:1fr 1fr">
      <div class="bloque" style="gap:4mm">
        <div class="bloque"><div class="kick">Compras y material</div><h2>Material, pasadores y cuerdas</h2></div>
        <table><thead><tr><th>Cód.</th><th>Qué</th><th>Cant.</th><th>Material</th><th>Dónde va</th></tr></thead><tbody>{tr}</tbody></table>
        <div class="aviso"><b>Si no hay aluminio 6061-T6</b>Hacer las mismas piezas en acero 4130 (cromo-molibdeno) de 6 mm en vez de 10 mm, con las mismas medidas de contorno y huecos. Pesa 1,7 veces más y se suelda con TIG y varilla ER80S-D2. No usar aluminio 6063 ni acero de construcción común para la cabeza.</div>
      </div>
      <div class="bloque" style="gap:3mm">
        <div class="bloque"><div class="kick">Taller</div><h2>Orden de fabricación y soldadura</h2></div>
        {ps}
      </div>
    </div>"""
    hoja("FAB", "Material, soldadura y prueba", "—", "", "S/E", c)
    indice("Material, pasadores, orden de fabricación, soldadura y prueba de carga")


PASOS_TALLER = [
    ("Corte láser", "Mandar los DXF (carpeta dxf) al taller: plancha Al 6061-T6 de 10 mm. Chorro de agua también sirve. Pedir los huecos de pasador a Ø 12 para escariar después."),
    ("Tubos", "Cortar 2 casquillos de 153 y el tubo de la gin pole (corte a " + f(90 - ALFA) + "° arriba). Tornear por dentro a Ø 51,4. Huecos G y ranuras F en fresa o taladro con prisma en V."),
    ("Punteado de la cabeza", "Sobre una mesa plana: placa 01 boca abajo (cara lisa contra la mesa). Poner las 4 aletas 03 paradas con escuadra en x = ±36 y ±64 y un eje de Ø 12 por los huecos de las 4 para que queden en línea. Puntear. Luego 05, 04 y los 2 casquillos con un gabarit a " + f(g.ANG) + "°. Al final las escuadras 06."),
    ("Soldadura TIG", "Corriente alterna, varilla ER5356 Ø 2,4, argón puro, precalentar a 120 °C. Soldar alternando lados para que no se tuerza. Cordón de filete de 6 mm en todas las uniones; en la V de la placa 01 con el tubo, cordón lleno y luego lijar al ras."),
    ("Gin pole", "Ala 07 boca abajo. Puntear las orejas 09 (x = 50 … 60) y el ojo 10. Pasar el tubo 08 por el hueco elíptico a " + f(ALFA) + "° con un gabarit, puntear, poner las cartelas 11 y soldar igual que la cabeza."),
    ("Escariar", "Con la gin pole puesta en la cabeza, escariar los 4 huecos de cada lado a Ø 13,1 de una sola pasada, para que los pasadores entren suave."),
    ("Tratamiento", "Si el taller puede: tratamiento térmico T6 después de soldar (recupera la fuerza del aluminio en la soldadura). Si no, tomar la carga de trabajo como la mitad."),
    ("Acabado", "Quitar filos y redondear R 1 los bordes donde van cuerdas. Anodizado azul (cabeza) y naranja (gin pole), o pintura en polvo."),
    ("Prueba de carga", "Armar a 2,46 m con maniotas. Colgar 18 kN (≈ 1.800 kg) del pasador de abajo por 3 minutos, sin personas, con tecle y dinamómetro. Si nada se deforma y los pasadores salen con la mano, se aprueba. Anotar fecha."),
]

PASOS_CAMPO = [
    "Armar cada pata en el suelo: cabeza → pata de afuera → pata de afuera → pata de adentro → pie. Revisar que la bola de cada pasador salga del otro lado.",
    "Poner la gin pole en la cabeza: sus 2 orejas entran en las ranuras de las aletas y se meten los 2 pasadores de arriba.",
    "Poner los 2 pasadores de abajo y la polea en el de la izquierda.",
    "Meter las 2 patas de la cabeza A-frame en los casquillos y la pata de atrás en el tubo de la gin pole, con su pasador 3/8\".",
    "Levantar, abrir las 3 patas hasta que queden a la misma distancia y poner las maniotas entre los pies.",
    "Poner vientos si la carga puede tirar de lado. Cargar poco a poco y con una cuerda de seguridad aparte.",
]


# ------------------------------------------------------------------ SVG 1:1 de corte
def svgs_corte():
    ala, ovalos, tubo = g.perfil_ala(ALFA)
    from shapely.affinity import scale as sc
    svg_corte("01_placa_frontal_x1", g.placa_frontal(), (), g.cortes_frontal(), "01 Placa frontal · Al 6061-T6 10 mm · 1")
    svg_corte("03_aleta_x4", g.ALETA[0], g.ALETA[1], (), "03 Aleta · Al 6061-T6 10 mm · 4")
    svg_corte("04_placa_trasera_x1", g.TRASERA[0], (), g.TRASERA[1], "04 Placa trasera · 1")
    svg_corte("05_placa_fondo_x1", g.FONDO[0], g.FONDO[1], (), "05 Placa de fondo · 1")
    svg_corte("06_escuadra_x2", g.ESCUADRA, (), (), "06 Escuadra · 2 (1 dada vuelta)")
    svg_corte("07_ala_gin_pole_x1", ala, (), ovalos + [tubo], "07 Ala de la gin pole · 1")
    svg_corte("09_oreja_gin_pole_x2", g.OREJA[0], g.OREJA[1], (), "09 Oreja · 2")
    svg_corte("10_ojo_gin_pole_x1", g.OJO[0], g.OJO[1], (), "10 Ojo · 1")
    svg_corte("11_cartela_gin_pole_x2", g.perfil_cartela(ALFA), (), (), "11 Cartela · 2")


# ------------------------------------------------------------------ generar
if __name__ == "__main__":
    hoja_lista()
    hoja_armado_cabeza()
    hoja_piezas_cabeza_1()
    hoja_piezas_cabeza_2()
    largo_gin, corto_gin = hoja_gin()
    hoja_patas()
    hoja_compras_fab(largo_gin)
    hoja_portada()
    HOJAS.insert(0, HOJAS.pop())
    svgs_corte()
    total = len(HOJAS)
    html = (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>VX-EC Trípode v7 · planos</title>'
            f'<style>{CSS}</style></head><body>' + "".join(render_hoja(h, i + 1, total) for i, h in enumerate(HOJAS)) + "</body></html>")
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(html)
    datos = dict(dibujos=WEB, compras=COMPRAS, taller=PASOS_TALLER, campo=PASOS_CAMPO,
                 lista=[dict(n=n, nombre=nom, material=mat, cant=q, kg=round(kg(pid, AC if n == "23" else AL), 2)) for n, nom, mat, q, pid in LISTA],
                 alturas=[dict(ext=ne, hueco=hu, h=round(trip(ne, hu)[0]), lado=round(trip(ne, hu)[1])) for ne in (1, 2, 3) for hu in (1, 3, 6)],
                 kg_cabeza=round(kg_cabeza(), 2), kg_gin=round(kg_gin(), 2), alfa=ALFA, gin_largo=round(largo_gin, 1), gin_corto=round(corto_gin, 1))
    json.dump(datos, open(os.path.join(BASE, "web", "dibujos.json"), "w"), ensure_ascii=False)
    print("hojas", total, "bytes", len(html), "dibujos", len(WEB))
