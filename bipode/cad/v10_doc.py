"""Planos del trípode tipo Vortex v10 (placas de corte láser soldadas con TIG), A3 horizontal.

Uso:  python3 v10_doc.py <carpeta_imagenes> <carpeta_fuentes>
Salida:  ../v10/plano/index.html (para imprimir a PDF), ../v10/svg/*.svg (piezas planas a escala 1:1)
         ../v10/web/dibujos.json (dibujos para la página)
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
import v10_geo as g
from v10_dibujo import Vista, f
ns["Vista"] = Vista

img, hoja, render_hoja, CSS, vista_tubo, pulg = (ns["img"], ns["hoja"], ns["render_hoja"], ns["CSS"],
                                                  ns["vista_tubo"], ns["pulg"])
HOJAS = ns["HOJAS"]
HOJAS.clear()
ns["TITULO"] = "Trípode tipo Vortex · placas soldadas"
ns["PROY"] = "VX-EC"
ns["REV"] = "F"
ns["FECHA"] = "26-09-2026"
INDICE = []

BASE = os.path.join(AQUI, "..", "v10")
OUT = os.path.join(BASE, "plano")
for d in ("plano", "svg", "web"):
    os.makedirs(os.path.join(BASE, d), exist_ok=True)
ARM = json.load(open(os.path.join(BASE, "armado.json")))
VOL = {p["id"]: p["vol"] for p in ARM["piezas"]}
VOL.update({a["id"]: a["vol"] for a in ARM["acc"]})
VOL.update(ARM["vol_sueltas"])
g.Z_DOBLE = ARM["z_doble"]                 # los 2 huecos quedan por encima del puente (calculado en v10_build)
PUENTE_Z0 = ARM["puente_z0"]
S_REF = (20.0, 128.0)                      # cartelitas 01r (igual que v10_build)               # cara de abajo del puente 04
AL, AC = 2.70e-6, 7.85e-6
ALFA = ARM["alfa"]
T = g.T
WEB = {}          # dibujos para la página: id -> svg


def fab(n):
    return f" · FABRICAR × {n}"


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
    s_ = fr
    for c in g.cortes_frontal():
        s_ = s_.difference(c)
    v.forma(s_, "pieza")
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
    r = g.D_DOBLE / 2
    for sx in (-1, 1):
        v.eje_cruz(sx * g.X_DOBLE, g.Z_DOBLE, r)
    v.diametro(g.X_DOBLE, g.Z_DOBLE, r, 35, "2 × Ø 25 (mosquetón)")
    v.cota_h(-g.X_DOBLE, g.X_DOBLE, g.Z_DOBLE + r, g.Z_DOBLE + r + 12, f(2 * g.X_DOBLE))
    v.cota_v(0, g.Z_DOBLE, -g.X_DOBLE - r, -g.X_DOBLE - r - 10, f(g.Z_DOBLE))
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
    v.nota(-18, g.C_HUECO[1] - 17, -50, -66, f"R {f(g.D_MOSQ / 2 + g.C_BORDE)} (centro en C): {f(g.C_BORDE)} mm de metal")
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
    v.nota(ovalos[1].centroid.x, ovalos[1].centroid.y, minx - 4, maxy - 22, "D: 21 × 33")
    yP = g.GP_PUNTA - g.GP_LARGO + g.D_PUNTA / 2 + 12.0
    v.eje_cruz(0, yP, g.D_PUNTA / 2)
    v.diametro(0, yP, g.D_PUNTA / 2, 300, "P · Ø 22 (punta)")
    for sx in (-1, 1):
        v.eje_cruz(sx * g.HUECOS_P2[0], g.HUECOS_P2[1], g.D_PUNTA / 2)
    v.diametro(g.HUECOS_P2[0], g.HUECOS_P2[1], g.D_PUNTA / 2, 330, "P2 · 2 × Ø 22")
    v.cota_h(-g.HUECOS_P2[0], g.HUECOS_P2[0], g.HUECOS_P2[1], miny - 4, f(2 * g.HUECOS_P2[0]))
    rb = ovalos[-1].bounds
    v.nota(rb[2], (rb[1] + rb[3]) / 2, maxx + 6, maxy - 40, "2 ranuras 13,1 × 20,4 (lengüeta de la oreja)")
    v.nota(maxx - 6, maxy - 7, maxx + 6, maxy + 12, "chaflán 13 × 45°")
    v.cota_h(-g.GP_OREJA_X[1], g.GP_OREJA_X[1], maxy, maxy + 12, f(2 * g.GP_OREJA_X[1]))
    v.texto(0, maxy - 6, "lado de la cabeza A-frame", 0.75)
    return v


def dib_oreja(ancho):
    p, hs = g.OREJA
    v = Vista(-128, -34, 34, 40, ancho)
    v.forma(p, "pieza2")
    v.circulo(0, 0, g.D12 / 2)
    v.eje_cruz(0, 0, g.D12 / 2)
    minx, miny, maxx, maxy = p.bounds
    v.cota_h(minx, maxx, miny, miny - 8, f(maxx - minx))
    v.cota_v(miny, g.GP_ALA_Z[0], minx, minx - 8, f(g.GP_ALA_Z[0] - miny))
    v.diametro(0, 0, g.D12 / 2, 40, "C · Ø 13,1 · R 16")
    zt = g.GP_ALA_Z[1]
    v.cota_h(g.RANURA_ALA[0], g.RANURA_ALA[1], zt, zt + 8, f(g.RANURA_ALA[1] - g.RANURA_ALA[0]))
    v.cota_v(g.GP_ALA_Z[0], zt, g.RANURA_ALA[0], g.RANURA_ALA[0] - 10, f(T))
    v.texto(-72, 26, "lengüeta: atraviesa el ala", 0.7)
    v.texto(-75, -2, "borde de abajo en diagonal", 0.7)
    return v


def dib_ojo(ancho):
    p, hs = g.OJO
    v = Vista(-40, -60, 56, 22, ancho)
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
    v = vista_tubo(g.CAS_L, g.CAS_OD, g.CAS_ID, hu, "02 · Casquillo · huecos desde la boca de la pata" + fab(2),
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
    s_ = fr
    for c in g.cortes_frontal():
        s_ = s_.difference(c)
    v.forma(s_, "pieza")
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
    s.rect(g.Y_FRENTE[0], 0, g.T_FR, g.alto_frontal(g.X_ALETA_INT), "pieza")
    s.rect(g.PUENTE_Y[0], PUENTE_Z0, g.Y_FRENTE[0] - g.PUENTE_Y[0], T, "oculta")
    s.cota_v(0, PUENTE_Z0, g.Y_ATRAS, g.Y_ATRAS - 12, f(PUENTE_Z0))
    s.cota_h(g.Y_ATRAS, g.Y_FRENTE[1], 0, -18, f(g.Y_FRENTE[1] - g.Y_ATRAS))
    s.cota_h(g.PIN_Y, 0, 110, 118, f(-g.PIN_Y))
    s.cota_h(0, g.Y_FRENTE[1], 156.9, 166, f(g.Y_FRENTE[1]))
    s.cota_h(-r, r, -8.4, -26, "63,5")
    s.texto(-44, 150, "tubo (casquillo)", 0.75, "end")
    s.texto(g.Y_FRENTE[1] + 2, 60, "01", 0.9, "start", "etq")
    s.texto(g.Y_ATRAS + 3, 58, "03", 0.9, "start", "etq")
    s.texto(g.PUENTE_Y[0] - 4, PUENTE_Z0 + 3, "04", 0.8, "end", "etq")
    lado = s

    # vista de arriba
    t = Vista(-230, -95, 230, 55, ancho_t)
    for lado_ in (-1, 1):
        xs = sorted([lado_ * 83.4, lado_ * 208.5])
        t.rect(xs[0], -r, xs[1] - xs[0], 2 * r, "pieza3")
    t.rect(-150, g.Y_FRENTE[0], 300, g.T_FR, "pieza")
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
    v = Vista(-150, -30, 150, 175, ancho)
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
    for z in g.CAR_HUECOS:
        v.linea((g.CAR_A_OD / 2 + 2, g.CAR_ALTO_A - z), (g.CAR_A_OD / 2 + 12, g.CAR_ALTO_A - z), "oculta")
    v.cota_v(0, top, r, r + 12, f(top))
    v.cota_v(top - g.CAR_ALTO_N, top, r, r + 26, f(g.CAR_ALTO_N))
    v.cota_v(0, g.CAR_ALTO_A, -r, -r - 10, f(g.CAR_ALTO_A))
    v.cota_v(T, g.CAR_ALTO_A, -r, -r - 24, f(g.CAR_ALTO_A - T))
    v.texto(-r - 30, (T + g.CAR_ALTO_A) / 2 - 18, "luz entre discos", 0.7, "end")
    v.cota_h(-g.CAR_A_OD / 2, g.CAR_A_OD / 2, T + g.CAR_A_ALTO, T + g.CAR_A_ALTO + 26 + 10, f"Ø {f(g.CAR_A_OD)}")
    v.texto(r - 4, top + 6, "15 naranja", 0.8, "end", "etq")
    v.texto(r - 4, -12, "16 azul", 0.8, "end", "etq")
    return v


def dib_plana(poly, hs, cs, ancho, cls="pieza2", notas=()):
    """Pieza plana genérica: contorno, huecos con cruz, medidas totales y posición de los huecos desde las esquinas."""
    minx, miny, maxx, maxy = poly.bounds
    v = Vista(minx - 34, miny - 34, maxx + 30, maxy + 24, ancho)
    s_ = poly
    for c in cs:
        s_ = s_.difference(c)
    for n, x, y, d in hs:
        s_ = s_.difference(Point(x, y).buffer(d / 2, quad_segs=48))
    v.forma(s_, cls)
    for n, x, y, d in hs:
        v.eje_cruz(x, y, d / 2)
    v.cota_h(minx, maxx, miny, miny - 16, f(maxx - minx))
    v.cota_v(miny, maxy, maxx, maxx + 16, f(maxy - miny))
    xs = sorted({round(x, 1) for n, x, y, d in hs})
    ys = sorted({round(y, 1) for n, x, y, d in hs})
    if xs:
        v.cota_h(minx, xs[0], miny, miny - 8, f(xs[0] - minx))
    if len(xs) > 1:
        v.cota_h(xs[-1], maxx, maxy, maxy + 8, f(maxx - xs[-1]))
    for k, y in enumerate(ys[:2]):
        v.cota_v(miny, y, minx, minx - 8 - 8 * k, f(y - miny))
    vistos = {}
    for n, x, y, d in hs:
        vistos.setdefault(d, []).append((x, y))
    for k, (d, pts) in enumerate(vistos.items()):
        v.diametro(*pts[-1], d / 2, 35 + 40 * k, f"{len(pts)} × Ø {f(d)}" if len(pts) > 1 else f"Ø {f(d)}")
    for x, y, xt, yt, t in notas:
        v.nota(x, y, xt, yt, t)
    return v


def dib_ahp_tubo(ancho):
    L, e, largo = g.AHP_TUBO
    return vista_tubo(largo, L, L - 2 * e, [(largo - 60.0, 16.5, "")], "17a · Tubo cuadrado 2\" × 2\" × 1/4\"" + fab(1),
                      f"Escala 1:{f((largo + 90) / ancho, 2)}", ancho, arriba_txt="contra la pared 17d, sobre la placa 17b", abajo_txt="entra en el enganche del carro",
                      cls="pieza3")


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
    ("01", "Placa frontal (cara lisa)", "Al 6061-T6 15,9 mm (5/8\") · chorro de agua", 1, "01", AL),
    ("01r", "Cartelita de refuerzo placa–tubo", "Al 6061-T6 8 mm · láser", 4, "01rda", AL),
    ("02", "Casquillo de la cabeza", "Tubo Al 6061-T6 2½\" × 1/4\" × 153", 2, "02a", AL),
    ("03", "Aleta de la cabeza", "Al 6061-T6 12,7 mm (1/2\") · láser", 4, "03a", AL),
    ("04", "Puente central (hueco C)", "Al 6061-T6 12,7 mm · láser", 1, "04", AL),
    ("05", "Ala de la gin pole", "Al 6061-T6 12,7 mm · láser", 1, "05", AL),
    ("06", "Tubo de la gin pole", "Tubo Al 6061-T6 2½\" × 1/4\"", 1, "06", AL),
    ("07", "Oreja de la gin pole (con lengüeta)", "Al 6061-T6 12,7 mm · láser", 2, "07a", AL),
    ("08", "Ojo central de la gin pole", "Al 6061-T6 12,7 mm · láser", 1, "08", AL),
    ("09", "Cartela de la gin pole", "Al 6061-T6 12,7 mm · láser", 2, "09a", AL),
    ("10", "Pata de afuera (cuerpo + espiga + tope)", "Tubo 2\" céd. 40 × 902 + tubo 2\" × 1/4\" × 272", 7, "10", AL),
    ("13", "Pata de adentro", "Tubo Al 6061-T6 2\" × 1/4\" × 965,2", 3, "13", AL),
    ("14", "Pie de flecha", f"Casquillo Al Ø 60,3 × {f(g.PIE_L)} + garra A36 12 mm", 3, "14", AL),
    ("15", "Carrete naranja (de adentro)", "Disco Al 12,7 + tubo Ø 60,3 × 114,3", 1, "15", AL),
    ("16", "Carrete azul (de afuera)", "Disco Al 12,7 + tubo Ø 73 × 129,5", 1, "16", AL),
    ("17a", "AHP · tubo cuadrado (punta al enganche)", "Tubo A36 2\" × 2\" × 1/4\" × 300", 1, "17a", AC),
    ("17b", "AHP · placa principal (centro + 2 patitas)", "Acero A36 25,4 mm (1\") · plasma o chorro de agua", 1, "17b", AC),
    ("17d", "AHP · pared de refuerzo cruzada", "Acero A36 12,7 mm · láser", 1, "17d", AC),
    ("17e", "AHP · cartela de atrás", "Acero A36 12,7 mm · láser", 2, "17ei", AC),
    ("17f", "AHP · orejita inclinada 10°", "Acero A36 12,7 mm · láser", 2, "17fi", AC),
    ("18a", "Pie con rótula · casquillo", f"Tubo Al 2½\" × 1/4\" × {f(g.PIE_L)} torneado", 3, "18a", AL),
    ("18b", "Pie con rótula · tapón con rosca 1\"", "Acero 1045 torneado", 3, "18b", AC),
    ("18d", "Pie con rótula · asiento de la bola", "Acero 1045 Ø 96 × 30 torneado", 3, "18d", AC),
    ("18e", "Pie con rótula · anillo de retención", "Acero 1045 12 mm (láser + torno)", 3, "18e", AC),
    ("18f", "Pie con rótula · base", "Acero A36 10 mm · láser", 3, "18f", AC),
]


def hoja_portada():
    filas = "".join(f'<tr><td class="m" style="width:12mm">{i + 2:02d}</td><td>{escape(t)}</td></tr>' for i, t in enumerate(INDICE))
    h, lado, tau, phi = trip(2, 1)
    c = f"""<div class="cont" style="grid-template-columns:150mm 1fr">
      <div class="bloque" style="gap:5mm;align-content:space-between">
        <div class="bloque" style="gap:4mm">
          <div class="kick">Juego de planos de fabricación · Rev. F</div>
          <h1 style="font-size:54pt;font-weight:700;line-height:.9">VX-EC<br><span style="color:var(--azul)">Trípode</span><br>tipo Vortex</h1>
          <p class="lead">Copia del Arizona Vortex: cabeza A-frame (azul) y gin pole (naranja) con placas de aluminio 6061-T6 de 12,7 mm
          (frontal de 15,9 mm), láser o chorro de agua y TIG; 7 patas de afuera, 3 de adentro y 3 pies; carrete de anclajes de 2 piezas,
          poste AHP de acero para el carro y pie plano con rótula. Todos los huecos siguen una sola regla para que cualquier combinación coincida.</p>
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
          <dt>Reemplaza</dt><dd>Rev. E: ya no se usa</dd>
        </div>
      </div>
      <div style="display:grid;grid-template-rows:1fr 1fr;gap:6mm">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:4mm;align-items:center">
          <img class="render" src="{img('v10_t')}" style="height:112mm;justify-self:center">
          <img class="render" src="{img('v10_tb')}" style="height:112mm;justify-self:center">
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:6mm;align-items:center">
          <img class="render" src="{img('v10_ciso')}" style="height:74mm">
          <img class="render" src="{img('v10_car')}" style="height:74mm">
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
        <div class="bloque"><div class="kick">Kit completo · cuántas de cada una</div><h2>Lista de piezas y cantidades a fabricar</h2></div>
        <table style="font-size:7.6pt"><thead><tr><th>N.º</th><th>Pieza</th><th>Material</th><th>FABRICAR</th><th>kg c/u</th><th>kg total</th></tr></thead><tbody>{filas}</tbody></table>
        <div class="aviso"><b>Numeración</b>01–04 cabeza A-frame (azul) · 05–09 gin pole (naranja) · 10 pata de afuera (7: 6 en uso + 1 de repuesto) ·
        13 pata de adentro · 14 pie · 15–16 carrete · 17a–f AHP del carro (igual al original) · 18a–h pie con rótula. Se compran: 16 pasadores 3/8" × 3", 1 pasador 3/8" × 4" (AHP), 4 (+1) pasadores 1/2",
        2 poleas, 3 maniotas, 3 bolas de enganche, 24 tornillos M8 (hoja de material). Grabar el número en cada pieza.
        Los 3 tubos naranja rectos con pasador del kit original: por ahora se toman como casquillos de pie de repuesto (confirmar).</div>
      </div>
      <div class="bloque" style="gap:4mm">
        <h3>Alturas · trípode de patas iguales</h3>
        <table><thead><tr><th>Patas de afuera</th><th>Hueco pata de adentro</th><th>Altura al pasador</th><th>Lado entre pies</th></tr></thead><tbody>{alt}</tbody></table>
        <p style="font-size:8pt;color:var(--gris)">Hueco 1 = la pata de adentro metida lo menos posible en la pata de afuera. Vortex: 2410 mm con 2 patas de afuera.</p>
        <img class="render" src="{img('v10_t')}" style="height:62mm;justify-self:center">
      </div>
    </div>"""
    hoja("LISTA", "Lista de piezas y alturas", "Varios", "", "S/E", c)
    indice("Lista de piezas numeradas y tabla de alturas")


def hoja_regla():
    ia, pa_, pu_a = ARM_A
    ib, pb, pu_b, top_b = ARM_B
    ia2, pa2, pu_a2 = ARM_A2
    ca = dib_cadena(ia, pa_, ancho=380)
    cb = dib_cadena(ib, pb, sale=(-top_b - g.CAS_L,), ancho=380)
    ca2 = dib_cadena(ia2, pa2, ancho=380)
    c = f"""<div class="cont" style="grid-template-rows:auto auto auto auto auto 1fr;row-gap:2mm">
      <div style="display:grid;grid-template-columns:1fr 180mm;gap:8mm;align-items:end">
        <div class="bloque"><div class="kick">Por qué coinciden todos los huecos</div><h2>Regla de huecos y formas de armar</h2></div>
        <div class="aviso"><b>Una sola regla para todo</b><span>1) Todo hueco de pasador 3/8" queda a 63,5 mm (2½") de la boca de su pieza.
        2) Todo macho sale 152 mm, con su hueco a 88,5 mm de la punta. 3) La pata de adentro tiene 7 huecos cada 139,7 mm (5½"),
        el primero y el último a 63,5 mm de las puntas. 4) Casquillos y carretes llevan huecos extra cada 27,9 mm para ajuste fino.
        5) Con carrete: SOLO esa pata va con el tubo arriba; las otras 2 van en A con la pata de adentro 2 huecos más adentro: las 3 quedan del mismo largo.
        Las 3 con tubo arriba a la vez: solo hasta que salgan 113,7 mm y sin carrete (más arriba se cruzan: las 3 patas apuntan al mismo punto, 250 mm sobre la cabeza).</span></div>
      </div>
      {guardar("cadena_A", ca.svg("A · Patas largas: macho arriba en el casquillo, 2 patas de afuera, pata de adentro, pie", esc(ca)))}
      {guardar("cadena_B", cb.svg("B · Tubo arriba con carrete (1 pata): la pata de adentro atraviesa el casquillo y sale " + f(-top_b - g.CAS_L, 1) + " mm; las patas de afuera van dadas vuelta", esc(cb)))}
      {guardar("cadena_A2", ca2.svg("B · Las otras 2 patas: forma A con la pata de adentro 2 huecos más adentro (mismo largo que la del carrete)", esc(ca2)))}
      <table><thead><tr><th>Forma</th><th>Orden desde la cabeza</th><th>Distancia boca → punta del pie</th><th>Pasadores (distancias desde la boca del casquillo)</th></tr></thead><tbody>
        <tr><td class="n">A</td><td>casquillo · afuera · afuera · adentro · pie</td><td class="m">{f(pu_a, 0)} mm</td><td class="m">{" · ".join(f(x) for x in pa_)} mm</td></tr>
        <tr><td class="n">B</td><td>adentro (sale arriba, carrete) · casquillo · afuera dada vuelta · afuera dada vuelta · pie</td><td class="m">{f(pu_b, 0)} mm</td><td class="m">{" · ".join(f(x) for x in pb)} mm</td></tr>
        <tr><td class="n">B′</td><td>las otras 2: casquillo · afuera · afuera · adentro (2 huecos más) · pie</td><td class="m">{f(pu_a2, 0)} mm</td><td class="m">{" · ".join(f(x) for x in pa2)} mm</td></tr>
      </tbody></table>
    </div>"""
    hoja("REGLA", "Regla de huecos y formas de armar", "—", "", "S/E", c,
         "Los números negativos quedan dentro del casquillo o por encima de él.")
    indice("Regla de huecos y formas de armar (patas largas / tubo arriba)")


def hoja_armado_cabeza():
    fr, la, ar = conjunto_cabeza(215, 100, 215)
    c = f"""<div class="cont" style="grid-template-columns:1fr 112mm;grid-template-rows:auto auto 1fr;grid-template-areas:'t t' 'f l' 'a l'">
      <div class="bloque" style="grid-area:t"><div class="kick">Cabeza A-frame · 8 piezas soldadas con TIG · FABRICAR × 1</div><h2>Armado de la cabeza A-frame</h2></div>
      <div style="grid-area:f">{guardar("arm_cab_frente", fr.svg("Vista de frente (cara lisa) · aletas en línea oculta", esc(fr)))}</div>
      <div class="bloque" style="grid-area:l;gap:5mm">{guardar("arm_cab_lado", la.svg("Vista de lado", esc(la)))}
        <img class="render" src="{img('v10_ab')}" style="height:46mm">
        <div class="aviso"><b>2 huecos, puente separado y refuerzos</b>Los 2 huecos Ø 25 de la placa 01 van abajo: {f(g.BORDE_DOBLE)} mm de metal al borde (centro a z = {f(g.Z_DOBLE)}). El puente 04 queda {f(g.LUZ_PUENTE)} mm atrás de la placa (no la toca): por ese espacio baja el mosquetón. La gin pole al juntarse baja hasta z = {f(ARM["zmin_gin"])}, lejos del puente. 4 cartelitas 01r de 8 mm refuerzan la unión placa–tubo arriba y abajo, por atrás.</div>
      </div>
      <div style="grid-area:a">{guardar("arm_cab_arriba", ar.svg("Vista de arriba · posición de cada placa", esc(ar)))}</div>
    </div>"""
    hoja("01–04", "Armado de la cabeza A-frame", "Al 6061-T6", "1 juego", "ver vistas", c,
         "Las 4 aletas son iguales. Soldar primero con puntos y medir antes del cordón completo.")
    indice("Armado de la cabeza A-frame (vistas con posiciones)")


def hoja_piezas_cabeza_1():
    v1 = dib_frontal(236)
    tub = tubo_cas(132)
    vr = dib_plana(g.REFUERZO, [], [], 60, cls="pieza")
    WEB["02"] = tub
    c = f"""<div class="cont" style="grid-template-columns:245mm 1fr;grid-template-rows:auto 1fr">
      <div class="bloque" style="grid-column:1/3"><div class="kick">Piezas 01 y 02</div><h2>Placa frontal y casquillos</h2></div>
      <div class="bloque">{guardar("01", v1.svg("01 · Placa frontal (cara lisa)" + fab(1), esc(v1)))}
        <dl class="ficha">
          <dt>01</dt><dd>Al 6061-T6 15,9 mm (5/8"), chorro de agua. {m2(kg('01'))} kg. La cara lisa del Vortex: una sola pieza, más gruesa para el tiro.</dd>
          <dt>Huecos</dt><dd>2 huecos Ø 25 mm para mosquetón grande (uno suelto en cada uno), en vez del corazón: centros a ±{f(g.X_DOBLE)} mm del centro y a {f(g.Z_DOBLE)} mm del borde de abajo ({f(g.BORDE_DOBLE)} mm de metal al borde); 13 mm de metal entre los dos. Las otras medidas no cambian.</dd>
          <dt>01r</dt><dd>4 cartelitas de refuerzo Al 6061-T6 8 mm (dibujo abajo), por la cara de atrás entre la placa y cada tubo: arriba a {f(S_REF[0], 0)} mm y abajo a {f(S_REF[1], 0)} mm de la boca de arriba del tubo. No tapan huecos ni ranuras. TIG todo alrededor.</dd>
          <dt>Bordes</dt><dd>Los 2 bordes laterales tocan el tubo por atrás; adelante queda una V para soldar y luego se lija al ras. Redondear R 1 mm los bordes de las ventanas E, los 2 huecos y las muescas.</dd>
        </dl>
      </div>
      <div class="bloque" style="gap:4mm">{tub}
        <dl class="ficha">
          <dt>02</dt><dd>Tubo 6061-T6 2½" × 1/4" (Ø 63,5 × 6,35 mm), largo 153 mm, 2 piezas, ABIERTO en las 2 puntas. Tornear por dentro a Ø 51,4 mm. {m2(kg('02a'))} kg c/u.</dd>
          <dt>Huecos</dt><dd>De frente a atrás, Ø 9,9 mm a 35,6 · <b>63,5</b> · 91,4 · 119,4 mm de la boca de la pata. De lado (a 90°), Ø 9,9 mm a 63,5 y 91,4 mm. El de 63,5 mm es el principal; los otros ajustan la pata de adentro cada 27,9 mm.</dd>
          <dt>Ranuras F</dt><dd>3 ranuras de 10,5 × 11 mm en la boca de la pata, a 90°, 210° y 330° (el tope de la pata de afuera entra en una: 3 posiciones de giro).</dd>
          <dt>Posición</dt><dd>Eje a {f(g.ANG)}° de la vertical; boca de arriba centrada en x = ±{f(g.XC)} mm, z = {f(g.ZT)} mm.</dd>
        </dl>
        {guardar("01r", vr.svg("01r · Cartelita placa–tubo (el lado curvo abraza el tubo)" + fab(4), esc(vr)))}
      </div>
    </div>"""
    hoja("01–02", "Placa frontal y casquillos", "Al 6061-T6", "FABRICAR 1 + 2", "ver vistas", c)
    indice("01 y 02 · Placa frontal y casquillos")


def hoja_piezas_cabeza_2():
    a = dib_aleta(118)
    pu = dib_puente(108)
    c = f"""<div class="cont" style="grid-template-columns:auto auto 1fr;grid-template-rows:auto 1fr auto;column-gap:14mm">
      <div class="bloque" style="grid-column:1/4"><div class="kick">Piezas 03 y 04 · Al 6061-T6 12,7 mm (1/2")</div><h2>Aletas y puente central</h2></div>
      {guardar("03", a.svg("03 · Aleta (4 iguales)" + fab(4), esc(a)))}
      {guardar("04", pu.svg("04 · Puente central" + fab(1), esc(pu)))}
      <div></div>
      <table style="grid-column:1/4"><thead><tr><th>N.º</th><th>Pieza</th><th>Cant.</th><th>Dónde va</th><th>kg c/u</th></tr></thead><tbody>
        <tr><td class="n">03</td><td>Aleta</td><td class="m">4</td><td>Parada de canto contra la cara de atrás de la placa 01. Caras de adentro a x = ±{f(g.X_ALETA_INT)} mm y ±{f(g.X_ALETA_EXT)} mm del centro. Entre cada par queda la ranura de 18 mm: ahí entra la oreja 07 de la gin pole y cuelgan las poleas y los mosquetones.</td><td class="m">{m2(kg('03a'))}</td></tr>
        <tr><td class="n">04</td><td>Puente central</td><td class="m">1</td><td>Acostado abajo (z = {f(PUENTE_Z0)} … {f(PUENTE_Z0 + T)} mm) entre las aletas de adentro, SEPARADO {f(g.LUZ_PUENTE)} mm de la placa 01 (de {f(g.Y_FRENTE[0] - g.PUENTE_Y[1])} a {f(g.Y_FRENTE[0] - g.PUENTE_Y[0])} mm hacia atrás): por ese espacio baja el mosquetón de los 2 huecos. Se suelda solo a las 2 aletas de adentro. Hueco C Ø 22 mm con 12 mm de metal adelante y {f(g.C_BORDE)} mm atrás.</td><td class="m">{m2(kg('04'))}</td></tr>
      </tbody></table>
    </div>"""
    hoja("03–04", "Aletas y puente central", "Al 6061-T6 12,7 mm", "FABRICAR 4 + 1", "ver vistas", c,
         "Huecos de pasador Ø 13,1 mm: cortar a Ø 12 mm con láser y escariar a 13,1 mm después de soldar, con las 4 aletas en línea.")
    indice("03 y 04 · Aletas y puente central")


def hoja_gin():
    arm = conjunto_gin(210)
    ala = dib_ala(118)
    c = f"""<div class="cont" style="grid-template-columns:132mm 1fr;grid-template-rows:auto 1fr">
      <div class="bloque" style="grid-column:1/3"><div class="kick">Gin pole (naranja) · piezas 05 a 09 · Al 6061-T6</div><h2>Gin pole · armado y ala</h2></div>
      <div class="bloque">{guardar("05", ala.svg("05 · Ala (escudo)" + fab(1), esc(ala)))}</div>
      <div class="bloque" style="gap:5mm">
        {guardar("arm_gin", arm.svg("Armado · vista de lado (ala horizontal)", esc(arm)))}
        <div style="display:grid;grid-template-columns:1fr 80mm;gap:6mm;align-items:start">
        <dl class="ficha">
          <dt>05 Ala</dt><dd>Plancha 12,7 mm, {m2(kg('05'))} kg. 7 huecos de anclaje: 4 óvalos D, hueco P Ø 22 en la punta y 2 huecos P2 Ø 22 a los lados (±{f(g.HUECOS_P2[0], 0)} mm). Hueco del tubo y 2 ranuras donde entran las lengüetas de las orejas. Todo hueco con ≥ 12 mm de metal.</dd>
          <dt>Bisagra</dt><dd>Las orejas 07 entran en las ranuras de la cabeza; el pasador de arriba de cada lado las atraviesa. Medidas de trabajo iguales al Vortex.</dd>
          <dt>Ángulo</dt><dd>Tubo a {f(ALFA)}° del ala: el ala queda horizontal con el trípode parado y las 3 patas iguales.</dd>
        </dl>
        <img class="render" src="{img('v10_ciso')}" style="height:52mm">
        </div>
      </div>
    </div>"""
    hoja("05", "Gin pole · armado y ala", "Al 6061-T6 12,7 mm", "FABRICAR 1", "ver vistas", c)
    indice("05 · Gin pole: armado y ala")
    tub, largo, corto = tubo_gin(170)
    WEB["06"] = tub.svg("06 · Tubo de la gin pole" + fab(1), esc(tub))
    o, oj, ca = dib_oreja(118), dib_ojo(70), dib_cartela(96)
    c = f"""<div class="cont" style="grid-template-columns:auto auto;grid-template-rows:auto auto auto 1fr;justify-content:start;column-gap:14mm">
      <div class="bloque" style="grid-column:1/3"><div class="kick">Gin pole · piezas 06 a 09</div><h2>Tubo, orejas, ojo y cartelas</h2></div>
      {WEB["06"]}
      {guardar("09", ca.svg("09 · Cartela" + fab(2), esc(ca)))}
      {guardar("07", o.svg("07 · Oreja reforzada" + fab(2), esc(o)))}
      {guardar("08", oj.svg("08 · Ojo" + fab(1), esc(oj)))}
      <dl class="ficha" style="grid-column:1/3;max-width:330mm">
        <dt>06 Tubo</dt><dd>2½" × 1/4" torneado a Ø 51,4 mm, abierto arriba (la pata de adentro puede salir por arriba). Lado largo {f(largo)} mm, lado corto {f(corto)} mm; la boca de arriba se corta a {f(90 - ALFA)}° y queda 8 mm sobre el ala. Huecos Ø 9,9 mm a 63,5 y 91,4 mm de la boca, de frente a atrás. 3 ranuras F de 10,5 × 11 mm.</dd>
        <dt>07 Orejas</dt><dd>2 piezas de 12,7 mm, paradas a x = {f(g.GP_OREJA_X[0])} … {f(g.GP_OREJA_X[1])} mm del centro. REFORZADAS: la lengüeta de arriba atraviesa el ala por su ranura y se suelda arriba y abajo; el cuerpo sigue {f(-g.OREJA_ATRAS)} mm bajo el ala con el borde de abajo en diagonal. Hueco C Ø 13,1 mm en el mismo lugar de antes.</dd>
        <dt>08 Ojo</dt><dd>1 pieza colgada al centro bajo el ala. Punto B de la gin pole, hueco Ø 25 mm con 12,5 mm de metal.</dd>
        <dt>09 Cartelas</dt><dd>2 piezas paradas a x = {f(g.CART_X[0])} … {f(g.CART_X[1])} mm a cada lado del tubo; unen el ala con el tubo.</dd>
      </dl>
    </div>"""
    hoja("06–09", "Gin pole · tubo, orejas, ojo y cartelas", "Al 6061-T6", "FABRICAR 1 + 2 + 1 + 2", "ver vistas", c)
    indice("06 a 09 · Gin pole: tubo, orejas, ojo y cartelas")
    return largo, corto


def recortar(svg):
    """Los detalles muestran solo su ventana (la pata sigue más allá)."""
    import re
    return re.sub(r'(<svg viewBox="[^"]*" style=")', r'\1overflow:hidden;', svg, count=1)


def hoja_patas():
    tot, mac, hem = pata_afuera_vistas()
    hu = [(p, g.D38, "") for p in g.PI_HUECOS]
    pi = vista_tubo(g.PI_L, g.D_PATA, 38.1, hu, "13 · Pata de adentro" + fab(3), f"Escala 1:{f((g.PI_L + 90) / 232, 2)}", 232,
                    arriba_txt="grabar «ÚLTIMO HUECO» junto al hueco 1", abajo_txt="grabar «ÚLTIMO HUECO» junto al hueco 7")
    WEB["13"] = pi
    c = f"""<div class="cont" style="grid-template-columns:250mm 1fr;grid-template-rows:auto auto 1fr">
      <div class="bloque" style="grid-column:1/3"><div class="kick">Piezas 10 y 13 · sierra, torno, taladro de pedestal</div><h2>Patas de afuera y de adentro</h2></div>
      <div class="bloque" style="gap:4mm">
        {guardar("10", tot.svg("10 · Pata de afuera completa (6 + 1 de repuesto)" + fab(7), esc(tot)))}
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
    hoja("10–13", "Patas de afuera y de adentro", "Al 6061-T6", "FABRICAR 7 + 3", "ver vistas", c)
    indice("10 a 13 · Patas de afuera (macho y hembra) y patas de adentro")


def hoja_pie_carrete():
    pie = dib_pie(84)
    dn, da, lado = dib_disco(True, 98), dib_disco(False, 98), dib_carrete_lado(84)
    c = f"""<div class="cont" style="grid-template-columns:auto auto auto auto;grid-template-rows:auto auto 1fr;column-gap:8mm;justify-content:space-between">
      <div class="bloque" style="grid-column:1/5"><div class="kick">Piezas 14, 15 y 16</div><h2>Pie de flecha y carrete de anclajes</h2></div>
      {guardar("14", pie.svg("14 · Pie de flecha" + fab(3), esc(pie)))}
      {guardar("15", dn.svg("15 · Disco del carrete naranja" + fab(1), esc(dn)))}
      {guardar("16", da.svg("16 · Disco del carrete azul" + fab(1), esc(da)))}
      {guardar("carrete", lado.svg("Carrete armado · corte", esc(lado)))}
      <dl class="ficha" style="grid-column:1/5">
        <dt>14 Pie</dt><dd>Casquillo de tubo 2½" × 1/4" torneado a Ø 60,3 mm por fuera y Ø 51,4 mm por dentro, largo {f(g.PIE_L)} mm (entra el macho completo de 152 mm sobre la garra); hueco Ø 9,9 mm a 63,5 mm de la boca y 3 ranuras F. Garra de acero A36 12 mm de láser soldada con MIG. Recibe la pata de adentro o el macho de una pata de afuera. El carrete azul entra por encima del casquillo.</dd>
        <dt>15 Naranja</dt><dd>Disco Ø {f(g.CAR_DISCO)} mm de 12,7 mm + tubo Ø 60,3 / 51,4 mm; alto total {f(g.CAR_ALTO_N)} mm, SIMÉTRICO: sirve derecho o de cabeza. Huecos Ø 9,9 mm a 35,6 · 63,5 · 91,4 mm de la cara del disco (= 91,4 · 63,5 · 35,6 desde la boca). Filete R 3 entre disco y tubo; bordes de los huecos redondeados R 1.</dd>
        <dt>16 Azul</dt><dd>Disco Ø {f(g.CAR_DISCO)} mm de 12,7 mm + tubo Ø 73 / 61 mm; alto total {f(g.CAR_ALTO_A)} mm. 2 filas de huecos Ø 9,9 a 90°: fila 1 a 35,6 · 63,5 · 91,4 mm de la cara del disco; fila 2 a 35,6 · 63,5 · 91,4 mm de la boca del tubo.</dd>
        <dt>Juntos</dt><dd>Luz entre discos {f(g.CAR_ALTO_A - T)} mm: cabe la cabeza de la gin pole DE LADO entre el azul (abajo) y el naranja (arriba), con 2 pasadores 1/2" verticales por los huecos de los discos y las orejas. 9 anclajes Ø 24 mm por disco en Ø {f(g.CAR_PCD)} (≥ 13 mm de metal).</dd>
      </dl>
    </div>"""
    hoja("14–16", "Pie de flecha y carrete de anclajes", "Al 6061-T6 · acero A36", "FABRICAR 3 + 1 + 1", "ver vistas", c)
    indice("14 a 16 · Pie de flecha y carrete de anclajes (naranja y azul)")


def hoja_ahp():
    b17, d17, e17, f17 = (g.AHP_PIEZAS[k] for k in ("17b", "17d", "17e", "17f"))
    vb = dib_plana(b17[0], b17[1], [], 104)
    vd = dib_plana(d17[0], [], [], 46)
    ve = dib_plana(e17[0], [], [], 66)
    vf = dib_plana(f17[0], [], f17[2], 40)
    ta = dib_ahp_tubo(150)
    WEB["17a"] = ta
    c = f"""<div class="cont" style="grid-template-columns:auto auto 1fr;grid-template-rows:auto auto auto 1fr;column-gap:8mm;row-gap:3mm">
      <div class="bloque" style="grid-column:1/4"><div class="kick">Accesorio aparte · para el vehículo · igual al original, reforzado atrás · acero A36 soldado con MIG</div><h2>Poste de enganche AHP (17a–17f)</h2></div>
      <div style="grid-row:2/4">{guardar("17b", vb.svg("17b · Placa principal: centro con 4 huecos + 2 patitas" + fab(1), esc(vb)))}</div>
      {guardar("17f", vf.svg("17f · Orejita" + fab(2), esc(vf)))}
      <div style="display:flex;gap:4mm;grid-row:2/4;grid-column:3;align-items:start"><img class="render" src="{img('v10_ahp')}" style="height:60mm"><img class="render" src="{img('v10_ahp2')}" style="height:60mm"></div>
      <div style="display:flex;gap:6mm">{guardar("17d", vd.svg("17d · Pared" + fab(1), esc(vd)))}{guardar("17e", ve.svg("17e · Cartela" + fab(2), esc(ve)))}</div>
      <div style="grid-column:1/3">{ta}</div>
      <dl class="ficha" style="grid-column:3;grid-row:3/5;align-self:start;font-size:8pt">
        <dt>Partes</dt><dd>Como el original: la PUNTA es el tubo cuadrado 17a que entra en el enganche de 2" del carro (pasador Ø 16 mm por el hueco de Ø 16,5 a 60 mm de la punta); el CENTRO es la placa 17b con 4 huecos Ø 25 (2 a cada lado, 13 mm de metal); abajo, las 2 PATITAS de la misma placa, con 52 mm de luz para la pata de adentro y el pasador 3/8" × 4" de canto a 24 mm de la punta.</dd>
        <dt>Refuerzo atrás</dt><dd>Como la gin pole: el tubo 17a va por atrás de la placa desde la pared cruzada 17d hasta el enganche, soldado a la placa; 2 cartelas 17e unen el tubo con la placa, una a cada lado.</dd>
        <dt>Orejitas</dt><dd>2 orejitas 17f con ventana de 26 × 36 mm (mosquetón o maniota), soldadas afuera de cada patita a {f(g.AHP_ARG_Y, 0)} mm de la punta, inclinadas {f(g.AHP_ARG_ANG, 0)}° hacia atrás (el lado del tubo). En total 6 anclajes: 4 huecos + 2 orejitas.</dd>
        <dt>Soldadura</dt><dd>MIG ER70S-6, filete de 8 mm todo alrededor (10 mm tubo–placa). Galvanizar o pintar. {m2(sum(kg(p, AC) for p in ("17a", "17b", "17d", "17ei", "17ed", "17fi", "17fd")))} kg el conjunto.</dd>
      </dl>
    </div>"""
    hoja("17", "Poste de enganche AHP (vehículo)", "Acero A36", "1 juego", "ver vistas", c,
         "Probar con 10 kN (≈ 1000 kg) sin personas antes del primer uso. Revisar la capacidad del enganche del carro.")
    indice("17a a 17f · Poste de enganche AHP para el carro (igual al original, reforzado)")


def hoja_rotula():
    pb, hb = g.rot_base()
    pa_, ha_, ca_ = g.rot_anillo()
    vb = dib_plana(pb, hb, [], 150)
    va = dib_plana(pa_, ha_, ca_, 74, cls="pieza")
    c = f"""<div class="cont" style="grid-template-columns:auto auto 1fr;grid-template-rows:auto auto 1fr;column-gap:10mm">
      <div class="bloque" style="grid-column:1/4"><div class="kick">Accesorio aparte · reto para el ingeniero</div><h2>Pie plano con rótula (18a–18h)</h2></div>
      {guardar("18f", vb.svg("18f · Base (4 pernos de anclaje + 2 mosquetones)" + fab(3), esc(vb)))}
      {guardar("18e", va.svg("18e · Anillo de retención (azul)" + fab(3), esc(va)))}
      <img class="render" src="{img('v10_rot')}" style="height:82mm;grid-row:2/4;grid-column:3;justify-self:center">
      <dl class="ficha" style="grid-column:1/3">
        <dt>Idea</dt><dd>La pata termina en una bola de enganche de 2" que gira dentro de un asiento: el pie queda plano sobre roca o losa aunque la pata vaya inclinada (hasta ±30°).</dd>
        <dt>18a</dt><dd>Casquillo igual al pie de flecha: tubo 2½" × 1/4" torneado Ø 60,3 / 51,4, largo {f(g.PIE_L)} mm, hueco Ø 9,9 a 63,5 mm de la boca y 3 ranuras F. Recibe la pata de adentro o el macho.</dd>
        <dt>18b</dt><dd>Tapón de acero 1045 soldado al fondo del casquillo, con hueco para la rosca 1" de la bola.</dd>
        <dt>18c</dt><dd>Bola de enganche 2" (50,8 mm), clase III, ≥ 3500 kg (≈ 34 kN), rosca 1": SE COMPRA. Se aprieta al tapón con su tuerca y arandela de presión.</dd>
        <dt>18d</dt><dd>Asiento: acero 1045 Ø 96 × 30 mm, copa esférica R 25,7 (bola + 0,3 mm de juego), 8 huecos con rosca M8 (broca 6,8) en Ø 90. Se suelda a la base 18f.</dd>
        <dt>18e</dt><dd>Anillo Ø 110 × 12 mm, hueco central Ø 44 (la bola no sale), 8 huecos Ø 8,6 en Ø 90; tornear la cara de abajo esférica igual al asiento.</dd>
        <dt>18f · 18g · 18h</dt><dd>Base A36 250 × 120 × 10 mm: 4 huecos Ø 14 para pernos de anclaje y 2 huecos Ø 25 para mosquetón (12,5 mm de metal). Suela de caucho 5 mm pegada abajo. 8 tornillos Allen M8 × 30 clase 8.8 con Loctite.</dd>
        <dt>Para el ingeniero</dt><dd>Comprobar el asiento y el anillo con la carga de la pata (≈ 9 kN por pata con 18 kN colgando) y probar 3 minutos con carga, sin personas.</dd>
      </dl>
    </div>"""
    hoja("18", "Pie plano con rótula", "Al 6061-T6 · acero 1045 · A36", "3 juegos", "ver vistas", c)
    indice("18a a 18h · Pie plano con rótula (bola de enganche 2\")")


COMPRAS = [
    ("P1", "Pasador de bola con anillo 1/2\" (12,7 mm) × 2\" de agarre", "4 (+1)", "Acero inox 17-4 · ≥ 140 kN doble corte", "Los 4 de la cabeza (los 2 de arriba son la bisagra de la gin pole). Sirven también de verticales en la gin pole de lado."),
    ("P2", "Pasador de bola con anillo 3/8\" (9,5 mm) × 3\" de agarre", "16", "Acero inox 17-4 · ≥ 80 kN doble corte", "Uniones de patas, pies y carrete."),
    ("P3", "Pasador de bola con anillo 3/8\" (9,5 mm) × 4\" de agarre", "1", "Acero inox 17-4 · ≥ 80 kN doble corte", "AHP: cruza las 2 patitas de 25,4 mm y la pata."),
    ("T1", "Perno 3/8\"-16 × 3\" grado 8 + tuerca de seguridad", "14", "Acero aleado", "2 por pata de afuera (fijan la espiga)."),
    ("T2", "Perno de acero Ø 9,5 × 16 mm (tope)", "7", "Acero 1045", "Tope de alineación de cada pata de afuera."),
    ("R1", "Polea de 1,5\" (38 mm) con rodamiento, ≥ 36 kN", "2", "Aluminio / acero", "Una en cada pasador de abajo, dentro de la ranura."),
    ("C1", "Cinta de maniota 25 mm con hebilla de leva, 20 kN", "3 × 3,5 m", "Poliéster", "Entre los pies."),
    ("M1", "Plancha Al 6061-T6 de 12,7 mm (1/2\")", "1 × (800 × 450)", "Con certificado", "03, 04, 05, 07, 08, 09 y discos 15 y 16."),
    ("M1b", "Plancha Al 6061-T6 de 15,9 mm (5/8\")", "1 × (450 × 150)", "Con certificado", "Placa frontal 01."),
    ("M2", "Tubo Al 6061-T6 2½\" × 1/4\" (Ø 63,5 × 6,35 mm)", "2,2 m", "Con certificado", "02 × 2, 06, pies 14 × 3, 18a × 3, tubo del carrete naranja."),
    ("M3", "Tubo Al 6061-T6 2\" céd. 40 (Ø 60,3 × 3,91 mm)", "7 × 902 mm", "Con certificado", "Cuerpos de las patas de afuera."),
    ("M4", "Tubo Al 6061-T6 2\" × 1/4\" (Ø 50,8 × 6,35 mm)", "3 × 965 + 7 × 272 mm", "Con certificado", "Patas de adentro y espigas."),
    ("M5", "Plancha A36 25,4 mm (1\") y 12,7 mm · tubo cuadrado A36 2\" × 1/4\" × 300 · A36 10 y 12 mm", "según plano", "—", "AHP 17, bases 18f, garras 14."),
    ("M7", "Plancha Al 6061-T6 de 8 mm", "1 × (100 × 50)", "Con certificado", "4 cartelitas 01r."),
    ("M6", "Barra Al 6061 Ø 80 · barra acero 1045 Ø 100 y Ø 115", "según plano", "—", "Tubo del carrete azul; asientos 18d, anillos 18e, tapones 18b."),
    ("B1", "Bola de enganche 2\" clase III, rosca 1\", ≥ 3500 kg", "3", "Acero forjado", "Pie con rótula 18c."),
    ("B2", "Tornillo Allen M8 × 30 clase 8.8 + Loctite", "24", "Acero", "Anillos 18e."),
    ("B3", "Caucho de 5 mm (neumático o SBR)", "3 × (250 × 120)", "—", "Suela 18g."),
    ("S1", "Varilla TIG ER5356 Ø 2,4 mm + argón puro · alambre MIG ER70S-6", "1 kg · 1 kg", "—", "Aluminio · acero."),
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
    ("Corte", "DXF al taller (carpeta dxf): Al 6061-T6 12,7 mm y la frontal en 15,9 mm (chorro de agua); AHP y bases en A36; garras en A36 12 mm. Huecos de pasador de la cabeza a Ø 12 mm para escariar después."),
    ("Tubos", "Cortar y tornear: 2 casquillos de 153 mm, tubo de la gin pole, 6 casquillos de pie de " + f(g.PIE_L) + " mm (3 flecha + 3 rótula), tubo naranja 114,3 mm (Ø 60,3 / 51,4), tubo azul 129,5 mm (Ø 73 / 61), 7 cuerpos de 902 mm, 7 espigas de 272 mm, 3 patas de adentro de 965,2 mm."),
    ("Huecos", "TODOS con plantilla: primero el de 63,5 mm desde la boca, luego los demás. Pata de adentro: 63,5 mm y cada 139,7 mm. Taladro de pedestal con prisma en V; broca de 6 y luego 9,9 mm. Redondear R 1 los bordes de todos los huecos de mosquetón."),
    ("Patas de afuera", "Meter la espiga 120 mm en el cuerpo, taladrar los 2 pernos juntos a 34 y 94 mm del escalón y apretar. Prensar el tope a 5,5 mm del escalón. Probar que 2 patas se unan y el pasador entre solo."),
    ("Cabeza", "Placa 01 boca abajo; 4 aletas paradas en x = ±" + f(g.X_ALETA_INT) + " y ±" + f(g.X_ALETA_EXT) + " mm con un eje de Ø 12 mm por los huecos; puente 04 abajo y separado " + f(g.LUZ_PUENTE) + " mm de la placa (soldado solo a las aletas de adentro); casquillos con gabarit a " + f(g.ANG) + "°; 4 cartelitas 01r atrás, arriba y abajo de cada tubo. Puntear, medir, soldar TIG alternando lados."),
    ("Gin pole y carrete", "Ala 05 boca abajo; las lengüetas de las orejas 07 entran en las ranuras del ala y se sueldan arriba y abajo; ojo 08; tubo 06 a " + f(ALFA) + "°; cartelas 09. Discos 15 y 16 soldados a sus tubos a escuadra, con filete R 3 entre disco y tubo."),
    ("TIG", "Corriente alterna, varilla ER5356 Ø 2,4 mm, argón puro, precalentar a 120 °C. Filete de 6 mm (8 mm en la frontal de 15,9). Si se puede: tratamiento T6 después de soldar."),
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
    A = "Al 6061-T6 12,7 mm"
    svg_corte("01_placa_frontal_x1", g.placa_frontal(), (), g.cortes_frontal(), "01 Placa frontal · Al 6061-T6 15,9 mm · FABRICAR × 1")
    svg_corte("03_aleta_x4", g.ALETA[0], g.ALETA[1], (), f"03 Aleta · {A} · FABRICAR × 4")
    svg_corte("04_puente_central_x1", g.PUENTE[0], g.PUENTE[1], (), f"04 Puente central · {A} · FABRICAR × 1")
    svg_corte("05_ala_gin_pole_x1", ala, (), ovalos + [tubo], f"05 Ala de la gin pole · {A} · FABRICAR × 1")
    svg_corte("07_oreja_gin_pole_x2", g.OREJA[0], g.OREJA[1], (), f"07 Oreja · {A} · FABRICAR × 2")
    svg_corte("08_ojo_gin_pole_x1", g.OJO[0], g.OJO[1], (), f"08 Ojo · {A} · FABRICAR × 1")
    svg_corte("09_cartela_gin_pole_x2", g.perfil_cartela(ALFA), (), (), f"09 Cartela · {A} · FABRICAR × 2")
    svg_corte("14_garra_pie_A36_12mm_x3", g4.contorno_garra(), [h[:4] for h in g4.HUECOS_GARRA], (), "14 Garra del pie · A36 12 mm · FABRICAR × 3")
    svg_corte("15_disco_carrete_naranja_x1", g.CAR_N[0], g.CAR_N[1], g.CAR_N[2], f"15 Disco naranja · {A} · FABRICAR × 1")
    svg_corte("16_disco_carrete_azul_x1", g.CAR_A[0], g.CAR_A[1], g.CAR_A[2], f"16 Disco azul · {A} · FABRICAR × 1")
    for k, n, q, e in (("17b", "placa_principal", 1, "25,4"), ("17d", "pared", 1, "12,7"), ("17e", "cartela", 2, "12,7"), ("17f", "orejita", 2, "12,7")):
        p, hs, cs = g.AHP_PIEZAS[k]
        svg_corte(f"{k}_AHP_{n}_A36_{e}mm_x{q}", p, hs, cs, f"{k} AHP {n} · A36 {e} mm · FABRICAR × {q}")
    svg_corte("01r_refuerzo_placa_tubo_Al_8mm_x4", g.REFUERZO, (), (), "01r Cartelita placa-tubo · Al 6061-T6 8 mm · FABRICAR × 4")
    svg_corte("18e_rotula_anillo_1045_12mm_x3", g.rot_anillo()[0], g.rot_anillo()[1], g.rot_anillo()[2], "18e Anillo · 1045 12 mm · FABRICAR × 3")
    svg_corte("18f_rotula_base_A36_10mm_x3", g.rot_base()[0], g.rot_base()[1], (), "18f Base · A36 10 mm · FABRICAR × 3")


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
    exec(open(os.path.join(AQUI, "v10_cadenas.py")).read())
    hoja_lista()
    hoja_regla()
    hoja_armado_cabeza()
    hoja_piezas_cabeza_1()
    hoja_piezas_cabeza_2()
    largo_gin, corto_gin = hoja_gin()
    hoja_patas()
    hoja_pie_carrete()
    hoja_ahp()
    hoja_rotula()
    hoja_compras_fab()
    hoja_portada()
    HOJAS.insert(0, HOJAS.pop())
    svgs_corte()
    total = len(HOJAS)
    html = (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>VX-EC Trípode v10 · planos</title>'
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
