"""Genera el documento de fabricación (HTML) con planos SVG sacados de geometria.py.

Uso:  python3 documento.py   ->  ../documento/index.html
"""
import math
import os
from html import escape

from shapely.geometry import Point, box

import geometria as g

OUT = os.path.join(os.path.dirname(__file__), "..", "documento")
os.makedirs(OUT, exist_ok=True)


def f1(v):
    return f"{v:.1f}".replace(".", ",").replace(",0", "") if abs(v - round(v)) < 0.05 else f"{v:.1f}".replace(".", ",")


# ------------------------------------------------------------------ dibujos SVG
def cota_h(x1, x2, y, texto, arriba=True, fs=11):
    """Cota horizontal en coordenadas SVG."""
    ty = y - fs * 0.5 if arriba else y + fs * 1.3
    return (f'<line class="dim" x1="{x1:.1f}" y1="{y:.1f}" x2="{x2:.1f}" y2="{y:.1f}" '
            f'marker-start="url(#fl)" marker-end="url(#fl)"/>'
            f'<text class="dt" x="{(x1 + x2) / 2:.1f}" y="{ty:.1f}" text-anchor="middle">{texto}</text>')


def cota_v(x, y1, y2, texto, fs=11):
    return (f'<line class="dim" x1="{x:.1f}" y1="{y1:.1f}" x2="{x:.1f}" y2="{y2:.1f}" '
            f'marker-start="url(#fl)" marker-end="url(#fl)"/>'
            f'<text class="dt" x="{x + fs * 0.6:.1f}" y="{(y1 + y2) / 2:.1f}" transform="rotate(90 {x + fs * 0.6:.1f} {(y1 + y2) / 2:.1f})" '
            f'text-anchor="middle">{texto}</text>')


DEFS = ('<defs><marker id="fl" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" '
        'orient="auto-start-reverse"><path d="M0 1L9 5L0 9z" class="ah"/></marker></defs>')


def svg_placa(contorno, huecos, titulo, ventana=None, hueco_central=None, extras=""):
    minx, miny, maxx, maxy = contorno.bounds
    m = 55
    W, H = maxx - minx + 2 * m, maxy - miny + 2 * m
    vb = f"{minx - m:.1f} {-maxy - m:.1f} {W:.1f} {H:.1f}"
    pts = " ".join(f"{x:.2f},{-y:.2f}" for x, y in contorno.exterior.coords)
    fs = max(W, H) / 42
    s = [f'<svg viewBox="{vb}" font-size="{fs:.1f}" role="img" aria-label="{escape(titulo)}">', DEFS,
         f'<polygon class="part" points="{pts}"/>']
    if ventana:
        cx, cy, L, Wv = ventana
        s.append(f'<rect class="hole" x="{cx - L / 2:.1f}" y="{-cy - Wv / 2:.1f}" width="{L}" height="{Wv}" rx="{Wv / 2}"/>')
        s.append(f'<text class="hl" x="{cx}" y="{-cy + 4:.1f}" text-anchor="middle">V</text>')
    if hueco_central:
        s.append(f'<circle class="hole" cx="0" cy="0" r="{hueco_central / 2}"/>')
    s.append(f'<line class="cl" x1="-12" y1="0" x2="12" y2="0"/><line class="cl" x1="0" y1="-12" x2="0" y2="12"/>')
    for n, x, y, d in huecos:
        s.append(f'<circle class="hole" cx="{x}" cy="{-y}" r="{d / 2}"/>')
        s.append(f'<text class="hl" x="{x}" y="{-y + fs * 0.3:.1f}" font-size="{min(fs * 0.75, d * 0.42):.1f}" text-anchor="middle">{n}</text>')
    s.append(extras)
    s.append(cota_h(minx, maxx, -miny + 25, f1(maxx - minx), arriba=False, fs=fs))
    s.append(cota_v(maxx + 22, -maxy, -miny, f1(maxy - miny), fs=fs))
    s.append("</svg>")
    return "".join(s)


def tabla_huecos(huecos, funciones, extra_filas=""):
    filas = []
    for n, x, y, d in huecos:
        filas.append(f"<tr><td class='n'>{n}</td><td class='num'>{f1(x)}</td><td class='num'>{f1(y)}</td>"
                     f"<td class='num'>Ø {f1(d)}</td><td>{funciones(n)}</td></tr>")
    return ("<div class='tbl'><table><thead><tr><th>Hueco</th><th>X</th><th>Y</th><th>Diámetro</th>"
            "<th>Para qué sirve</th></tr></thead><tbody>" + "".join(filas) + extra_filas + "</tbody></table></div>")


def fn_placa(n):
    return {
        "A": "Punto de amarre para mosquetón (vientos, equipo)",
        "B": "Barra de carga Ø 25,4 (B1 = carga principal)",
        "D": "Perno 1/2\" con distanciador (une las placas; amarre de vientos)",
        "C": "Casquillo de pata: 1 = perno fijo 3/8\", 2 = pasador de pata 3/8\"",
    }[n[0]]


def svg_tubo(largo, od, huecos, titulo, extra=None, ranura=None, cotas_desde="arriba"):
    """Tubo horizontal: izquierda = punta de arriba. Escala real a lo largo."""
    m = 40
    h = od
    W = largo + 2 * m
    fs = max(W / 95, 5.0)
    larg = max(len(et) for _, _, et in huecos)
    top = h / 2 + fs * 4.2
    Hs = top + h / 2 + 18 + fs * 0.62 * larg + 10
    s = [f'<svg viewBox="{-m} {-top:.1f} {W} {Hs:.1f}" font-size="{fs:.1f}" role="img" aria-label="{escape(titulo)}">', DEFS,
         f'<rect class="part" x="0" y="{-h / 2}" width="{largo}" height="{h}"/>']
    if ranura:
        rl, rw = ranura
        s.append(f'<rect class="hole" x="{largo - rl}" y="{-rw / 2}" width="{rl}" height="{rw}"/>')
    for pos, d, et in huecos:
        s.append(f'<circle class="hole" cx="{pos}" cy="0" r="{d / 2}"/>')
        s.append(f'<line class="cl" x1="{pos}" y1="{-h / 2 - 8}" x2="{pos}" y2="{h / 2 + 8}"/>')
        yy = h / 2 + 14
        s.append(f'<text class="dt" x="{pos}" y="{yy + fs * 0.35:.1f}" text-anchor="end" '
                 f'transform="rotate(-90 {pos} {yy:.1f})">{et}</text>')
    s.append(cota_h(0, largo, -h / 2 - fs * 1.2, f"{f1(largo)}  (Ø {f1(od)})", fs=fs))
    if extra:
        s.append(extra)
    s.append(f'<text class="dt" x="0" y="{-h / 2 - fs * 3.2:.1f}">punta de arriba</text>')
    s.append(f'<text class="dt" x="{largo}" y="{-h / 2 - fs * 3.2:.1f}" text-anchor="end">punta de abajo</text>')
    s.append("</svg>")
    return "".join(s)


# ------------------------------------------------------------------ piezas
placa_svg = svg_placa(g.contorno_placa(), g.HUECOS_PLACA, "Placa de la cabeza con sus huecos",
                      ventana=g.VENTANA,
                      extras="".join(
                          f'<polygon class="ghost" points="' + " ".join(
                              f"{x:.1f},{-y:.1f}" for x, y in
                              __import__("shapely.geometry", fromlist=["LineString"]).LineString(
                                  [g.eje(l, -80), g.eje(l, 80)]).buffer(g.CAS_OD / 2, cap_style=2).exterior.coords) + '"/>'
                          for l in (-1, 1)))
placa_tabla = tabla_huecos(g.HUECOS_PLACA, fn_placa,
                           extra_filas=f"<tr><td class='n'>V</td><td class='num'>{f1(g.VENTANA[0])}</td>"
                                       f"<td class='num'>{f1(g.VENTANA[1])}</td><td class='num'>{f1(g.VENTANA[2])} × {f1(g.VENTANA[3])}</td>"
                                       "<td>Ventana ovalada para pasar una cinta o una gaza de cuerda</td></tr>")

anillo_svg = svg_placa(Point(0, 0).buffer(g.ANI_OD / 2, quad_segs=90), g.HUECOS_ANILLO, "Disco del anillo de amarre",
                       hueco_central=g.ANI_HUECO_C)
anillo_tabla = tabla_huecos(g.HUECOS_ANILLO, lambda n: "Punto de amarre para mosquetón",
                            extra_filas=f"<tr><td class='n'>C</td><td class='num'>0</td><td class='num'>0</td>"
                                        f"<td class='num'>Ø {f1(g.ANI_HUECO_C)}</td><td>Hueco central: entra el manguito Ø 73</td></tr>")

tubo_svg = (f'<line class="cl" x1="-60" y1="0" x2="60" y2="0"/>'
            f'<rect class="ghost" x="{-g.INF_OD / 2}" y="0" width="{g.INF_OD}" height="{g.PIE_RANURA_L + 30}"/>')
pie_svg = svg_placa(g.contorno_pie_garra(), g.HUECOS_PIE_GARRA, "Pie de garra",
                    extras=tubo_svg + f'<text class="dt" x="{g.INF_OD / 2 + 4}" y="-90">tubo</text>')
pie_tabla = tabla_huecos(g.HUECOS_PIE_GARRA,
                         lambda n: "Perno 1/2\" que une el pie con la pata" if n == "P1" else "Amarre de la maniota o de un anclaje")

lengua_svg = svg_placa(g.contorno_pie_plano_lengua(), g.HUECOS_PIE_PLANO_LENGUA, "Lengua del pie plano")
base_svg = svg_placa(box(-80, -80, 80, 80).buffer(-10).buffer(10, quad_segs=16), g.HUECOS_BASE, "Base del pie plano",
                     extras=f'<rect class="ghost" x="-{g.OREJA[0] / 2}" y="-{(g.PLACA_AC + 0.5) / 2 + g.PLACA_AC_BASE}" '
                            f'width="{g.OREJA[0]}" height="{g.PLACA_AC_BASE}"/>'
                            f'<rect class="ghost" x="-{g.OREJA[0] / 2}" y="{(g.PLACA_AC + 0.5) / 2}" '
                            f'width="{g.OREJA[0]}" height="{g.PLACA_AC_BASE}"/>')
oreja_svg = svg_placa(g.contorno_oreja(), g.HUECOS_OREJA, "Oreja del pie plano")

sup_huecos = [(h, g.D_PATA, f"{f1(h)}" + (" ←último para unir" if h == g.ULTIMO_HUECO_UNION else "")) for h in g.HUECOS_SUP]
sup_svg = svg_tubo(g.SUP_L, g.SUP_OD, sup_huecos, "Pata de arriba")
inf_huecos = [(h, g.D_PATA, f1(h)) for h in g.HUECOS_INF] + \
             [(g.INF_L - g.PIE_PERNO_Y, g.D_PERNO12, f"{f1(g.INF_L - g.PIE_PERNO_Y)} (perno pie)")]
inf_svg = svg_tubo(g.INF_L, g.INF_OD, inf_huecos, "Pata de abajo", ranura=(g.PIE_RANURA_L, g.PIE_RANURA_A))
cas_huecos = [(g.S_PERNO_FIJO + 80, g.D_PATA, f"{f1(g.S_PERNO_FIJO + 80)} perno fijo"),
              (g.S_PASADOR + 80, g.D_PATA, f"{f1(g.S_PASADOR + 80)} pasador")]
cas_svg = svg_tubo(g.CAS_L, g.CAS_OD, cas_huecos, "Casquillo de la cabeza")
man_svg = svg_tubo(g.MAN_L, g.MAN_OD, [(g.MAN_L - g.MAN_PASADOR_Z, g.D_PATA, f"{f1(g.MAN_L - g.MAN_PASADOR_Z)}")],
                   "Manguito del anillo",
                   extra=f'<rect class="ghost" x="{g.MAN_L - g.MAN_DISCO_Z - g.PLACA_AL / 2}" y="-{g.ANI_OD / 2 * 0.35}" '
                         f'width="{g.PLACA_AL}" height="{g.ANI_OD * 0.35}"/>'
                         f'<text class="dt" x="{g.MAN_L - g.MAN_DISCO_Z}" y="{-g.ANI_OD * 0.175 - 3:.1f}" text-anchor="middle">disco</text>')

# ------------------------------------------------------------------ tabla de alturas
filas_alt = []
for i, f in enumerate(g.alturas(), 1):
    wll = "9 kN (≈ 900 kg)" if f["altura_barra"] <= 2030 else "5,5 kN (≈ 550 kg)"
    wllp = "360 kg" if f["altura_barra"] <= 2030 else "220 kg"
    filas_alt.append(
        f"<tr><td class='n'>{i}</td><td class='num'>{f1(f['hueco'])}</td><td class='num'>{f['altura_barra'] / 1000:.2f} m".replace(".", ",")
        + f"</td><td class='num'>{f['altura_total'] / 1000:.2f} m".replace(".", ",")
        + f"</td><td class='num'>{f['abertura'] / 1000:.2f} m".replace(".", ",")
        + f"</td><td class='num'>{f1(f['traslape'])}</td><td class='num'>{wll}</td><td class='num'>{wllp}</td></tr>")
tabla_alturas = "".join(filas_alt)

# ------------------------------------------------------------------ pesos
def area_placa(contorno, huecos, extra=0.0):
    return contorno.area - sum(math.pi * d * d / 4 for *_, d in huecos) - extra


def tubo_kg(od, esp, L):
    return math.pi / 4 * (od ** 2 - (od - 2 * esp) ** 2) * L * 2.7e-6


kg_placa = area_placa(g.contorno_placa(), g.HUECOS_PLACA, g.VENTANA[2] * g.VENTANA[3]) * g.PLACA_AL * 2.7e-6
kg_sup = tubo_kg(g.SUP_OD, g.SUP_ESP, g.SUP_L)
kg_inf = tubo_kg(g.INF_OD, g.INF_ESP, g.INF_L)
kg_cas = tubo_kg(g.CAS_OD, g.CAS_ESP, g.CAS_L)
kg_disco = area_placa(Point(0, 0).buffer(g.ANI_OD / 2, 64), g.HUECOS_ANILLO,
                      math.pi * g.ANI_HUECO_C ** 2 / 4) * g.PLACA_AL * 2.7e-6
kg_anillo = kg_disco + tubo_kg(g.MAN_OD, g.MAN_ESP, g.MAN_L)
kg_pie = area_placa(g.contorno_pie_garra(), g.HUECOS_PIE_GARRA) * g.PLACA_AC * 7.85e-6
kg_barra = math.pi / 4 * 25.4 ** 2 * (g.GAP + 2 * g.PLACA_AL + 28) * 7.85e-6
kg_cabeza = 2 * kg_placa + 2 * kg_cas + 3 * kg_barra + 2 * 0.25 + 0.3
kg_total = kg_cabeza + 2 * (kg_sup + kg_inf + kg_pie) + 2 * kg_anillo + 0.6


def kg(v):
    return f"{v:.1f}".replace(".", ",")


VALORES = {
    "KG_PLACA": kg(kg_placa), "KG_SUP": kg(kg_sup), "KG_INF": kg(kg_inf), "KG_CAS": kg(kg_cas),
    "KG_ANILLO": kg(kg_anillo), "KG_PIE": kg(kg_pie), "KG_BARRA": kg(kg_barra),
    "KG_CABEZA": kg(kg_cabeza), "KG_TOTAL": kg(kg_total),
    "PLACA_W": f1(g.contorno_placa().bounds[2] - g.contorno_placa().bounds[0]),
    "PLACA_H": f1(g.contorno_placa().bounds[3] - g.contorno_placa().bounds[1]),
    "SVG_PLACA": placa_svg, "TABLA_PLACA": placa_tabla,
    "SVG_ANILLO": anillo_svg, "TABLA_ANILLO": anillo_tabla,
    "SVG_PIE": pie_svg, "TABLA_PIE": pie_tabla,
    "SVG_LENGUA": lengua_svg, "SVG_BASE": base_svg, "SVG_OREJA": oreja_svg,
    "SVG_SUP": sup_svg, "SVG_INF": inf_svg, "SVG_CAS": cas_svg, "SVG_MAN": man_svg,
    "TABLA_ALTURAS": tabla_alturas,
}

tpl = open(os.path.join(os.path.dirname(__file__), "plantilla.html"), encoding="utf-8").read()
for k, v in VALORES.items():
    tpl = tpl.replace("{{" + k + "}}", v)
assert "{{" not in tpl, tpl[tpl.index("{{"):tpl.index("{{") + 40]
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(tpl)
print({k: v for k, v in VALORES.items() if k.startswith("KG") or k.startswith("PLACA")})
