"""Juego de planos del bípode tipo Vortex (v4) en HTML A3 horizontal, para imprimir a PDF.

Uso:  python3 v4_doc.py <carpeta_imagenes> <carpeta_fuentes>  ->  ../v4/plano/index.html
"""
import base64
import datetime
import math
import os
import sys
from html import escape

from shapely.geometry import LineString, Point, box

import v4_geo as g
from v4_dibujo import Vista, f

IMG = sys.argv[1]
FONTS = sys.argv[2]
OUT = os.path.join(os.path.dirname(__file__), "..", "v4", "plano")
os.makedirs(OUT, exist_ok=True)

PROY = "VX-EC"
TITULO = "Bípode A-Frame de rescate"
CLIENTE = "Aventuras con Janeric · Morona Santiago, Ecuador"
FECHA = "24-09-2026"
REV = "A"

AL, AC = 2.70e-6, 7.85e-6
VOL = {"01": 503106, "02": 199340, "03": 14172, "04": 83159, "05": 58046, "06": 850253, "07": 858411,
       "08": 276395, "09": 434513, "10": 712062}
KG = {k: v * (AC if k in ("03", "05", "08", "09") else AL) for k, v in VOL.items()}


def pulg(mm):
    return f"{mm / 25.4:.3f}\"".replace(".", ",")


def img(nombre):
    from io import BytesIO
    from PIL import Image
    im = Image.open(os.path.join(IMG, f"out_{nombre}.png")).convert("RGBA")
    x0, y0, x1, y1 = im.getbbox()
    p = 12
    im = im.crop((max(0, x0 - p), max(0, y0 - p), min(im.width, x1 + p), min(im.height, y1 + p)))
    buf = BytesIO()
    im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def fuente(familia, peso, archivo):
    b = base64.b64encode(open(os.path.join(FONTS, archivo), "rb").read()).decode()
    return (f"@font-face{{font-family:'{familia}';font-weight:{peso};font-style:normal;"
            f"src:url(data:font/woff2;base64,{b}) format('woff2');}}")


FUENTES = "".join([
    fuente("Barlow", 400, "fontsource-barlow-5.3.0/files/barlow-latin-400-normal.woff2"),
    fuente("Barlow", 500, "fontsource-barlow-5.3.0/files/barlow-latin-500-normal.woff2"),
    fuente("Barlow", 600, "fontsource-barlow-5.3.0/files/barlow-latin-600-normal.woff2"),
    fuente("Barlow", 700, "fontsource-barlow-5.3.0/files/barlow-latin-700-normal.woff2"),
    fuente("Barlow Condensed", 500, "fontsource-barlow-condensed-5.3.0/files/barlow-condensed-latin-500-normal.woff2"),
    fuente("Barlow Condensed", 600, "fontsource-barlow-condensed-5.3.0/files/barlow-condensed-latin-600-normal.woff2"),
    fuente("Barlow Condensed", 700, "fontsource-barlow-condensed-5.3.0/files/barlow-condensed-latin-700-normal.woff2"),
    fuente("Plex Mono", 400, "fontsource-ibm-plex-mono-5.3.0/files/ibm-plex-mono-latin-400-normal.woff2"),
    fuente("Plex Mono", 500, "fontsource-ibm-plex-mono-5.3.0/files/ibm-plex-mono-latin-500-normal.woff2"),
])

CSS = FUENTES + """
@page{size:420mm 297mm;margin:0}
:root{--tinta:#101820;--gris:#5b6875;--linea:#c9d1d9;--suave:#eef2f6;--azul:#1646a8;--naranja:#e0621b;--papel:#ffffff}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:#dfe4ea}
body{font-family:'Barlow',Arial,sans-serif;color:var(--tinta);font-size:9.5pt;line-height:1.38;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.hoja{width:420mm;height:297mm;background:var(--papel);position:relative;overflow:hidden;page-break-after:always;margin:0 auto 8mm}
@media print{.hoja{margin:0}html,body{background:#fff}}
.marco{position:absolute;inset:8mm;border:0.5mm solid var(--tinta)}
.zona{position:absolute;font:500 6pt 'Plex Mono',monospace;color:var(--gris)}
.cont{position:absolute;left:14mm;top:14mm;right:14mm;bottom:50mm;display:grid;gap:7mm}
h1,h2,h3{font-family:'Barlow Condensed','Arial Narrow',sans-serif;margin:0;letter-spacing:.01em;line-height:1.05}
h2{font-size:22pt;font-weight:700;text-transform:uppercase}
h3{font-size:12.5pt;font-weight:700;text-transform:uppercase;letter-spacing:.04em}
.kick{font:500 7.5pt 'Plex Mono',monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--naranja)}
.lead{font-size:10.5pt;color:#26323d;max-width:150mm}
p{margin:0}
.bloque{display:grid;gap:2.2mm;align-content:start}
.num{font-family:'Plex Mono',monospace;font-variant-numeric:tabular-nums}
table{border-collapse:collapse;width:100%;font-size:8.2pt}
th{font:600 6.8pt 'Plex Mono',monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--gris);text-align:left;border-bottom:0.35mm solid var(--tinta);padding:1.4mm 1.6mm}
td{border-bottom:0.2mm solid var(--linea);padding:1.25mm 1.6mm;vertical-align:top}
td.n{font:500 8.2pt 'Plex Mono',monospace;color:var(--azul);white-space:nowrap}
td.m{font-family:'Plex Mono',monospace;font-size:7.8pt;white-space:nowrap;font-variant-numeric:tabular-nums}
tr.dest td{background:var(--suave)}
ul,ol{margin:0;padding-left:4.5mm;display:grid;gap:1.1mm}
li{padding-left:.5mm}
.vista{margin:0;display:grid;gap:1.2mm;justify-items:start}
.vista svg{display:block;overflow:visible}
.vista-tit{display:flex;gap:3mm;align-items:baseline;font:700 9pt 'Barlow Condensed',sans-serif;text-transform:uppercase;letter-spacing:.05em}
.vista-tit em{font:400 7pt 'Plex Mono',monospace;color:var(--gris);font-style:normal;letter-spacing:.04em}
svg .pieza{fill:#e6ecf4;stroke:var(--tinta)}
svg .pieza2{fill:#f6d9c6;stroke:var(--tinta)}
svg .pieza3{fill:#d9dee4;stroke:var(--tinta)}
svg .hueco{fill:#fff;stroke:var(--tinta)}
svg .obj{stroke:var(--tinta);fill:none}
svg .oculta{stroke:#4a5663;fill:none}
svg .fantasma{stroke:#8795a3;fill:none}
svg .eje{stroke:var(--naranja);fill:none}
svg .aux,svg .cota{stroke:#39434d;fill:none}
svg .flecha{fill:#39434d}
svg .t{font-family:'Plex Mono',monospace;fill:var(--tinta)}
svg .ct{font-family:'Plex Mono',monospace;fill:#1a2530;font-weight:500}
svg .etq{font-family:'Plex Mono',monospace;fill:var(--azul);font-weight:500}
.render{display:block;max-width:100%;object-fit:contain}
.ficha{display:grid;grid-template-columns:auto 1fr;gap:1mm 5mm;font-size:8.6pt;margin:0}
.ficha dt{font:500 6.8pt 'Plex Mono',monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--gris);padding-top:.6mm}
.ficha dd{margin:0}
.aviso{border-left:1.2mm solid var(--naranja);background:#fff4ec;padding:2.5mm 3.5mm;display:grid;gap:1mm;font-size:8.6pt}
.aviso b{font:700 10pt 'Barlow Condensed',sans-serif;text-transform:uppercase;letter-spacing:.04em;color:#9a3a07}
.chip{display:inline-block;font:500 6.8pt 'Plex Mono',monospace;border:0.25mm solid var(--tinta);padding:.4mm 1.6mm;border-radius:.6mm;letter-spacing:.06em}
.paso{display:grid;grid-template-columns:9mm 1fr;gap:3mm;align-items:start}
.paso .k{font:700 15pt 'Barlow Condensed',sans-serif;color:#fff;background:var(--azul);text-align:center;line-height:9mm;border-radius:.8mm}
.paso div{display:grid;gap:.8mm}
.cifra{display:grid;gap:.4mm;border-top:0.6mm solid var(--tinta);padding-top:1.8mm}
.cifra b{font:700 20pt 'Barlow Condensed',sans-serif;line-height:1}
.cifra span{font-size:8pt;color:var(--gris)}
/* rótulo */
.rotulo{position:absolute;right:8mm;bottom:8mm;width:196mm;height:36mm;border-left:0.5mm solid var(--tinta);border-top:0.5mm solid var(--tinta);display:grid;
  grid-template-columns:54mm 1fr 34mm;grid-template-rows:1fr 1fr 1fr}
.rotulo>div{border-right:0.25mm solid var(--tinta);border-bottom:0.25mm solid var(--tinta);padding:1.3mm 2mm;display:grid;align-content:start;gap:.3mm;overflow:hidden}
.rotulo>div:nth-child(3n){border-right:0}
.rotulo>div.ult{border-bottom:0}
.rotulo small{font:500 5.6pt 'Plex Mono',monospace;letter-spacing:.1em;text-transform:uppercase;color:var(--gris)}
.rotulo strong{font:700 11pt 'Barlow Condensed',sans-serif;letter-spacing:.02em;line-height:1.05}
.rotulo .grande{grid-row:1/3;background:var(--tinta);color:#fff}
.rotulo .grande small{color:#9fb0c1}
.rotulo .grande strong{font-size:22pt;line-height:.95}
.rotulo .tit{grid-column:2/3;grid-row:1/3}
.rotulo .tit strong{font-size:15pt}
.leyenda{position:absolute;left:14mm;bottom:12mm;width:196mm;font-size:7.2pt;color:var(--gris);display:grid;gap:.6mm}
"""


# ------------------------------------------------------------------ hoja base
HOJAS = []


def hoja(num_pieza, titulo, material, cantidad, escala, contenido, nota=""):
    zonas = "".join(f'<div class="zona" style="left:{8 + 4 + i * 50.5}mm;top:3mm">{i + 1}</div>' for i in range(8)) + \
        "".join(f'<div class="zona" style="left:3mm;top:{8 + 20 + i * 35}mm">{"ABCDEFG"[i]}</div>' for i in range(7))
    HOJAS.append(dict(num=num_pieza, titulo=titulo, material=material, cantidad=cantidad, escala=escala,
                      contenido=contenido, nota=nota, zonas=zonas))


def render_hoja(h, i, total):
    rot = f"""<div class="rotulo">
      <div class="grande"><small>Proyecto</small><strong>{PROY}</strong><small style="margin-top:1mm">{escape(TITULO)}</small></div>
      <div class="tit"><small>Plano</small><strong>{escape(h['titulo'])}</strong><small style="margin-top:.8mm">{escape(CLIENTE)}</small></div>
      <div><small>Hoja</small><strong class="num">{i:02d} / {total:02d}</strong></div>
      <div><small>Rev. · fecha</small><strong class="num" style="font-size:9pt">{REV} · {FECHA}</strong></div>
      <div class="ult"><small>Pieza</small><strong class="num">{escape(h['num'])}</strong></div>
      <div class="ult"><small>Material · cantidad</small><strong style="font-size:9pt">{escape(h['material'])}{(' · ' + escape(h['cantidad'])) if h['cantidad'] else ''}</strong></div>
      <div class="ult"><small>Escala · unidad</small><strong class="num" style="font-size:9pt">{escape(h['escala'])} · mm</strong></div>
    </div>"""
    ley = (f'<div class="leyenda"><div>Medidas en milímetros; entre paréntesis, en pulgadas. Tolerancia general ±0,5 mm; '
           f'huecos de pasador +0,1 / −0. Quitar filos vivos (chaflán 0,5 mm). {escape(h["nota"])}</div>'
           f'<div>Diseño propio inspirado en el Arizona Vortex (Rock Exotica). Uso con personas solo después de la revisión de un ingeniero '
           f'mecánico y de la prueba de carga de la hoja de fabricación.</div></div>')
    return f'<section class="hoja"><div class="marco"></div>{h["zonas"]}{h["contenido"]}{ley}{rot}</section>'


# ------------------------------------------------------------------ datos
def alturas_tabla():
    filas = []
    for n in (2, 3):
        for h in (1, 2, 3, 4, 5):
            alto = g.altura(n, h)
            dest = (n == 2 and h == 2) or (n == 3 and h == 3)
            wll = "9 kN (≈ 900 kg)" if n == 2 else "5,5 kN (≈ 550 kg)"
            mbs = "36 kN" if n == 2 else "22 kN"
            filas.append(f'<tr class="{"dest" if dest else ""}"><td class="m">{n}</td><td class="m">{h}</td>'
                         f'<td class="m">{g.expuestos(h)}</td><td class="m">{f(alto / 1000, 2)} m</td>'
                         f'<td class="m">{f(g.altura(n, h, 15) / 1000, 2)} m</td><td class="m">{f(g.abertura(n, h) / 1000, 2)} m</td>'
                         f'<td class="m">{mbs}</td><td class="m">{wll}</td></tr>')
    return "".join(filas)


def pandeo(n):
    E = 69000.0
    I_e = math.pi / 64 * (g.EXT_OD ** 4 - (g.EXT_OD - 2 * g.EXT_E) ** 4)
    I_i = math.pi / 64 * (g.MACHO_OD ** 4 - (g.MACHO_OD - 2 * g.MACHO_E) ** 4)
    L = g.largo_pata(n, 2 if n == 2 else 3) + 150
    Le, Li = n * g.PE_TUBO, L - n * g.PE_TUBO
    I = (I_e * Le + I_i * Li) / L
    P = math.pi ** 2 * E * I / L ** 2
    return L, P, 2 * P * g.CA


# ------------------------------------------------------------------ HOJA 1: portada
def portada():
    L2, P2, T2 = pandeo(2)
    L3, P3, T3 = pandeo(3)
    c = f"""<div class="cont" style="grid-template-columns:150mm 1fr">
      <div class="bloque" style="gap:6mm;align-content:space-between">
        <div class="bloque" style="gap:4mm">
          <div class="kick">Juego de planos de fabricación · Rev. {REV}</div>
          <h1 style="font-size:58pt;font-weight:700;letter-spacing:-.01em;line-height:.9">{PROY}<br><span style="color:var(--azul)">Bípode</span><br>A-Frame</h1>
          <p class="lead">Anclaje portátil de aluminio para rápel, rescate y entrada a cuevas. Copia de la geometría del
          Arizona Vortex (Rock Exotica), adaptada para fabricarse en Ecuador con tubo 6061-T6, corte por láser o
          chorro de agua, torno y taladro.</p>
        </div>
        <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:5mm">
          <div class="cifra"><b>2,45 m</b><span>altura al punto de carga · 2 patas de afuera</span></div>
          <div class="cifra"><b>3,13 m</b><span>altura al punto de carga · 3 patas de afuera</span></div>
          <div class="cifra"><b>36 kN</b><span>rotura objetivo · carga de trabajo 9 kN</span></div>
          <div class="cifra"><b>14</b><span>puntos de amarre · 46 con las 2 placas de amarre</span></div>
        </div>
        <div class="bloque">
          <h3>Contenido</h3>
          <table><tbody>
            {''.join(f'<tr><td class="m" style="width:12mm">{i + 2:02d}</td><td>{escape(t)}</td></tr>' for i, t in enumerate(INDICE))}
          </tbody></table>
        </div>
        <div class="ficha" style="grid-template-columns:auto 1fr">
          <dt>Cliente</dt><dd>{escape(CLIENTE)}</dd>
          <dt>Referencia</dt><dd>Arizona Vortex · Rock Exotica · manual técnico, 80 págs.</dd>
          <dt>Fecha</dt><dd class="num">{FECHA}</dd>
        </div>
      </div>
      <div style="display:grid;grid-template-columns:118mm 1fr;gap:6mm;align-items:start">
        <div class="bloque" style="gap:3mm;padding-top:10mm">
          <img class="render" src="{img('h_cab')}" style="width:118mm">
          <div class="chip" style="justify-self:start">01 · CABEZA A-FRAME</div>
          <img class="render" src="{img('h_cabx')}" style="width:112mm;margin-top:10mm">
          <div class="chip" style="justify-self:start">CABEZA · VISTA EXPLOTADA</div>
        </div>
        <img class="render" src="{img('h_armf')}" style="height:228mm;justify-self:end">
      </div>
    </div>"""
    HOJAS.insert(0, dict(num="—", titulo="Portada", material="—", cantidad="", escala="—", contenido=c, nota="",
                         zonas=""))


INDICE = []


def indice(t):
    INDICE.append(t)


# ------------------------------------------------------------------ HOJA 2: conjunto y alturas
def hoja_conjunto():
    L2, P2, T2 = pandeo(2)
    L3, P3, T3 = pandeo(3)
    c = f"""<div class="cont" style="grid-template-columns:118mm 118mm 1fr">
      <div class="bloque">
        <div class="kick">Conjunto armado</div><h2>Vista 3D</h2>
        <img class="render" src="{img('h_arm')}" style="height:165mm;justify-self:center">
        <p class="num" style="font-size:7.5pt;color:var(--gris)">Armado de la tabla: 2 patas de afuera + pata de adentro en el hueco 2 (4 huecos a la vista). Maniota amarilla entre los pies. Vientos azules adelante y atrás.</p>
      </div>
      <div class="bloque">
        <div class="kick">Conjunto armado</div><h2>Vista lateral</h2>
        <img class="render" src="{img('h_arml')}" style="height:165mm;justify-self:center">
        <p class="num" style="font-size:7.5pt;color:var(--gris)">Los vientos van a 45° o más; nunca a menos de 30°. La fuerza de la cuerda tiene que caer dentro del plano de las patas.</p>
      </div>
      <div class="bloque" style="gap:4mm">
        <div class="bloque"><div class="kick">Tabla de alturas</div><h2>Alturas y cargas</h2></div>
        <table><thead><tr><th>Patas afuera</th><th>Hueco</th><th>A la vista</th><th>Altura a B</th><th>Inclinado 15°</th><th>Entre pies</th><th>Rotura</th><th>Trabajo</th></tr></thead>
        <tbody>{alturas_tabla()}</tbody></table>
        <p style="font-size:8pt">Las filas marcadas son las del manual del Vortex (pág. 31): 2 patas + 4 huecos → 2,41 m, 36 kN; 3 patas + 3 huecos → 3,05 m, 22 kN.
        Este diseño da 2,45 m y 3,13 m: 1,5 % y 2,6 % de diferencia.</p>
        <div class="bloque" style="gap:1.5mm">
          <h3>Comprobación: pandeo de las patas</h3>
          <p style="font-size:8pt">Fórmula de Euler, P = π²·E·I / L², aluminio E = 69 000 MPa, patas articuladas en los extremos. Fuerza en la cabeza que dobla las 2 patas: T = 2·P·cos 30°.</p>
          <table><thead><tr><th>Armado</th><th>Largo pata</th><th>P por pata</th><th>T en la cabeza</th><th>Vortex</th></tr></thead><tbody>
          <tr><td>2 patas afuera</td><td class="m">{f(L2 / 1000, 2)} m</td><td class="m">{f(P2 / 1000, 1)} kN</td><td class="m">{f(T2 / 1000, 1)} kN</td><td class="m">36 kN</td></tr>
          <tr><td>3 patas afuera</td><td class="m">{f(L3 / 1000, 2)} m</td><td class="m">{f(P3 / 1000, 1)} kN</td><td class="m">{f(T3 / 1000, 1)} kN</td><td class="m">22 kN</td></tr>
          </tbody></table>
          <p style="font-size:8pt">Los tubos elegidos llegan a la misma resistencia que el Vortex original. La carga de trabajo es la rotura dividida para 4, igual que en el manual.</p>
        </div>
        <div class="aviso"><b>Regla de uso</b>Máximo 3 patas de afuera por pata. Usar siempre la altura más baja que sirva: menos altura, más resistencia.</div>
      </div>
    </div>"""
    hoja("CONJ", "Conjunto, alturas y cargas", "—", "", "S/E", c)
    indice("Conjunto, alturas y cargas")


# ------------------------------------------------------------------ HOJA 3: lista de piezas
PIEZAS = [
    ("01", "Placa de cabeza", 2, "Aluminio 6061-T6, plancha 1/2\" (12,7)", "Corte por chorro de agua o láser de fibra", "h", "p01"),
    ("02", "Casquillo de cabeza", 2, "Tubo Al 6061-T6 2½\" × 1/4\" (Ø 63,5 × 6,35)", "Sierra, torno (interior Ø 51,4), taladro, fresa", "h", "p02"),
    ("03", "Separador del perno I", 4, "Tubo acero Ø 25,4 × 3,2 (1\" × 1/8\")", "Sierra y refrentado a 63,5", "c", "p03"),
    ("04", "Bloque central C", 1, "Barra Al 6061-T6 63,5 × 50 × 34", "Fresa y taladro", "h", "p04"),
    ("05", "Barra de carga B", 1, "Barra acero AISI 4140 Ø 25,4 (1\")", "Torno y taladro", "c", "p05"),
    ("06", "Pata de afuera", 4, "Tubo Al 6061-T6 2\" céd. 40 + espigón 2\" × 1/4\"", "Sierra, taladro, fresa, 2 pernos 3/8\"", "l", "p06"),
    ("07", "Pata de adentro", 2, "Tubo Al 6061-T6 2\" × 1/4\" (Ø 50,8 × 6,35)", "Sierra, taladro, fresa (muesca)", "l", "p07"),
    ("08", "Pie Raptor", 2, "Tubo acero Ø 63,5 × 6 + garra A36 12 mm", "Láser, soldadura MIG, recargue duro en la punta", "p", "p08"),
    ("09", "Pie plano (opcional)", 2, "Acero A36 10 mm + tubo acero Ø 63,5 × 6 + caucho 5 mm", "Láser, soldadura MIG", "p", "p09"),
    ("10", "Placa de amarre de 2 pisos (mejora)", 2, "Tubo Al 2½\" × 1/4\" + 2 discos Al 1/2\" + espigón", "Láser, torno, soldadura TIG AC", "a", "p10"),
]


def hoja_piezas():
    filas = []
    for n, nom, q, mat, proc, _, r in PIEZAS:
        filas.append(f'<tr><td class="n">{n}</td><td><b>{escape(nom)}</b></td><td class="m">{q}</td><td>{escape(mat)}</td>'
                     f'<td>{escape(proc)}</td><td class="m">{f(KG[n], 2)} kg</td></tr>')
    total = 2 * KG["01"] + 2 * KG["02"] + 4 * KG["03"] + KG["04"] + KG["05"] + 4 * KG["06"] + 2 * KG["07"] + 2 * KG["08"]
    tiles = "".join(f'<div style="display:grid;gap:1mm;justify-items:center;border:0.2mm solid var(--linea);padding:2mm">'
                    f'<img class="render" src="{img(r)}" style="height:38mm;width:100%"><div style="display:flex;gap:2mm;align-items:baseline">'
                    f'<span class="num" style="color:var(--azul);font-weight:500">{n}</span><span style="font-size:8pt;font-weight:600">{escape(nom)}</span></div></div>'
                    for n, nom, q, mat, proc, _, r in PIEZAS)
    c = f"""<div class="cont" style="grid-template-rows:auto 1fr">
      <div style="display:grid;grid-template-columns:1fr 130mm;gap:10mm;align-items:end">
        <div class="bloque"><div class="kick">Lista de piezas</div><h2>Piezas a fabricar para un bípode</h2></div>
        <div class="ficha"><dt>Peso</dt><dd class="num">{f(total, 1)} kg sin pasadores ni cuerdas (Vortex: ≈ 20 kg en A-frame)</dd>
        <dt>Colores</dt><dd>Cabeza y placas de amarre anodizado azul · pies pintura en polvo naranja · patas anodizado natural</dd></div>
      </div>
      <div style="display:grid;grid-template-columns:1fr 150mm;gap:10mm">
        <table><thead><tr><th>N.º</th><th>Pieza</th><th>Cant.</th><th>Material</th><th>Proceso</th><th>Peso c/u</th></tr></thead><tbody>{''.join(filas)}</tbody></table>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:2mm;align-content:start">{tiles}</div>
      </div>
    </div>"""
    hoja("LISTA", "Lista de piezas", "Varios", "", "S/E", c)
    indice("Lista de piezas")


# ------------------------------------------------------------------ HOJA: placa de cabeza
def hoja_placa():
    P = g.contorno_placa()
    for cc in g.cortes_placa():
        P = P.difference(cc)
    minx, miny, maxx, maxy = P.bounds
    v = Vista(minx - 60, miny - 70, maxx + 60, maxy + 40, 245)
    for lado in (-1, 1):
        s = LineString([g.eje(lado, 0), g.eje(lado, g.CAS_L)]).buffer(g.HEMBRA_OD / 2, cap_style=2)
        v.poli(list(s.exterior.coords), "fantasma")
        v.linea(g.eje(lado, -15), g.eje(lado, g.CAS_L + 15), "eje")
    v.forma(P)
    for n, x, y, d, _ in g.HUECOS_PLACA:
        v.circulo(x, y, d / 2)
        v.eje_cruz(x, y, d / 2)
        v.texto(x + d / 2 + 2.2 * v.k, y + d / 2 + 0.6 * v.k, n, 0.8, "start", "etq")
    for i, cc in enumerate(g.cortes_placa()):
        cx, cy = cc.centroid.x, cc.centroid.y
        v.texto(cx, cy - 1 * v.k, "E", 0.8, cls="etq")
    v.texto(0, 88, "D", 0.8, cls="etq")
    v.cota_h(minx, maxx, miny, miny - 18)
    v.cota_v(miny, maxy, maxx, maxx + 22)
    v.cota_h(-g.XC, g.XC, g.YT, maxy + 14, f"{f(2 * g.XC)} ejes casquillos")
    x1, y1 = g.eje(1, g.CAS_L)
    v.cota((g.eje(1, 0)), g.eje(1, g.CAS_L), -44, f"{f(g.CAS_L)} casquillo")
    v.nota(g.eje(-1, 150)[0], g.eje(-1, 150)[1], -60, miny - 42, "30° cada casquillo · 60° entre patas")
    v.cota_v(0, g.YT, -g.XC, -g.XC - 30, f(g.YT))
    placa_svg = v.svg("Vista de frente · 1 placa", "Escala 1:1,6 · origen = centro del hueco B")

    pares = {}
    for n, x, y, d, t in g.HUECOS_PLACA:
        clave = (n[0] if n[0] != "I" else ("I-arr" if y > 0 else "I-abj")) + (n[2:] if n[0] == "S" else "")
        pares.setdefault(clave, []).append((n, x, y, d, t))
    filas = ""
    for lst in pares.values():
        nombres = " · ".join(e[0] for e in lst)
        x = f"±{f(abs(lst[0][1]))}" if len(lst) > 1 else f(lst[0][1])
        filas += (f'<tr><td class="n">{nombres}</td><td class="m">{x}</td><td class="m">{f(lst[0][2])}</td>'
                  f'<td class="m">Ø {f(lst[0][3])}</td><td style="font-size:7.6pt">{escape(lst[0][4])}</td></tr>')
    vent = ('<tr><td class="n">E1 · E2</td><td class="m" colspan="3">triángulo (±50; −2) (±74; −4) (±58; −22), R 6</td>'
            '<td style="font-size:7.6pt">Ventana: paso del mosquetón a I3 / I4</td></tr>'
            '<tr><td class="n">D</td><td class="m" colspan="3">canal R 26, centro (0; 110)</td>'
            '<td style="font-size:7.6pt">Canal para que pase la cuerda</td></tr>')
    c = f"""<div class="cont" style="grid-template-columns:250mm 1fr">
      <div class="bloque">
        <div class="kick">Pieza 01 · corte por láser o chorro de agua</div><h2>Placa de cabeza</h2>
        {placa_svg}
      </div>
      <div class="bloque" style="gap:3.5mm">
        <img class="render" src="{img('h_cabf')}" style="height:46mm">
        <dl class="ficha">
          <dt>Material</dt><dd>Aluminio 6061-T6, plancha 1/2" (12,7 mm), con certificado</dd>
          <dt>Cantidad</dt><dd>2 iguales (delantera y trasera) por bípode</dd>
          <dt>Tamaño</dt><dd class="num">{f(maxx - minx)} × {f(maxy - miny)} × 12,7 mm · {f(KG['01'], 2)} kg</dd>
          <dt>Archivo</dt><dd class="num">01_placa_cabeza_Al6061-T6_12.7mm_x2.dxf</dd>
          <dt>Corte</dt><dd>Huecos A, I, S y C: cortar a Ø 11 y terminar con broca junto con los casquillos (hoja de fabricación). B, H y E a medida final.</dd>
        </dl>
        <table><thead><tr><th>Hueco</th><th>X</th><th>Y</th><th>Ø</th><th>Uso</th></tr></thead><tbody>{filas}{vent}</tbody></table>
      </div>
    </div>"""
    hoja("01", "Placa de cabeza", "Al 6061-T6 1/2\"", "2", "1:1,6", c, "Redondear aristas de los huecos A, B, H y E (R 1) para no dañar cuerdas.")
    indice("01 · Placa de cabeza")


# ------------------------------------------------------------------ HOJA: casquillo + pequeñas
def vista_tubo(largo, od, idi, huecos, titulo, escala_txt, ancho_mm, ranuras=None, extras=None, arriba_txt="arriba",
               abajo_txt="boca", cls="pieza"):
    """Tubo horizontal. x = 0 punta izquierda (arriba), x = largo a la derecha."""
    k = (largo + 90) / ancho_mm
    v = Vista(-45, -od / 2 - 60, largo + 45, od / 2 + 9 * k * (len(huecos) + 1) + 4 * k, ancho_mm)
    v.rect(0, -od / 2, largo, od, cls)
    v.linea((0, idi / 2), (largo, idi / 2), "oculta")
    v.linea((0, -idi / 2), (largo, -idi / 2), "oculta")
    v.linea((-12, 0), (largo + 12, 0), "eje")
    if ranuras:
        for (x0, w, h) in ranuras:
            v.rect(x0, -w / 2, h, w, "hueco")
    niveles = [od / 2 + 9 * v.k * (i + 1) for i in range(len(huecos))]
    for (pos, d, et), yn in zip(sorted(huecos), niveles):
        v.circulo(pos, 0, d / 2)
        v.linea((pos, -od / 2 - 5), (pos, od / 2 + 5), "eje")
        v.cota_h(0, pos, od / 2, yn, f(pos))
    v.cota_h(0, largo, -od / 2, -od / 2 - 16, f"{f(largo)} ({pulg(largo)})")
    v.cota_v(-od / 2, od / 2, largo, largo + 22, f"Ø {f(od)}")
    v.texto(0, -od / 2 - 30, arriba_txt, 0.8, "start")
    v.texto(largo, -od / 2 - 30, abajo_txt, 0.8, "end")
    if extras:
        extras(v)
    return v.svg(titulo, escala_txt)


def hoja_casquillo():
    hu = [(s, g.D12, "") for s in g.S_PERNOS] + [(g.CAS_L - gb, g.D38, "") for gb in g.G_DESDE_BOCA]
    sv = vista_tubo(g.CAS_L, g.HEMBRA_OD, g.HEMBRA_ID, hu, "02 · Casquillo · vista de lado", "Escala 1:1", 150,
                    ranuras=[(g.CAS_L - g.RANURA_P, g.RANURA_A, g.RANURA_P)], abajo_txt="boca (abajo)")
    e = Vista(-55, -55, 55, 55, 60)
    e.circulo(0, 0, g.HEMBRA_OD / 2, "pieza")
    e.circulo(0, 0, g.HEMBRA_ID / 2, "hueco")
    for a in g.RANURAS_ANG:
        ca, sa = math.cos(math.radians(a + 90)), math.sin(math.radians(a + 90))
        e.linea((ca * g.HEMBRA_ID / 2, sa * g.HEMBRA_ID / 2), (ca * (g.HEMBRA_OD / 2 + 6), sa * (g.HEMBRA_OD / 2 + 6)), "eje")
    e.eje_cruz(0, 0, g.HEMBRA_OD / 2)
    e.diametro(0, 0, g.HEMBRA_ID / 2, 225, f"Ø {f(g.HEMBRA_ID)} H8")
    e.diametro(0, 0, g.HEMBRA_OD / 2, 30, f"Ø {f(g.HEMBRA_OD)}")
    ev = e.svg("Vista desde la boca", "3 ranuras F a 120°")

    # separador, bloque, barra
    s = Vista(-25, -30, 90, 28, 58)
    s.rect(0, -12.7, g.GAP, 25.4, "pieza3")
    s.linea((0, 9.5), (g.GAP, 9.5), "oculta")
    s.linea((0, -9.5), (g.GAP, -9.5), "oculta")
    s.cota_h(0, g.GAP, -12.7, -22, f(g.GAP))
    s.cota_v(-12.7, 12.7, g.GAP, g.GAP + 12, "Ø 25,4")
    sep = s.svg("03 · Separador", "Escala 1:1 · pared 3,2")

    w, h, y0 = g.BLOQUE_C
    b = Vista(-45, y0 - 18, 45, y0 + h + 22, 58)
    b.rect(-w / 2, y0, w, h, "pieza")
    b.linea((-g.D_C_VERT / 2, y0), (-g.D_C_VERT / 2, y0 + h), "oculta")
    b.linea((g.D_C_VERT / 2, y0), (g.D_C_VERT / 2, y0 + h), "oculta")
    for x in (-16, 16):
        b.circulo(x, 31, g.D_M10 / 2)
        b.eje_cruz(x, 31, g.D_M10 / 2)
    b.linea((0, y0 - 5), (0, y0 + h + 5), "eje")
    b.cota_h(-w / 2, w / 2, y0, y0 - 10, f(w))
    b.cota_v(y0, y0 + h, w / 2, w / 2 + 10, f(h))
    b.cota_h(-16, 16, 31, y0 + h + 12, "32")
    blo = b.svg("04 · Bloque C · frente", "Escala 1:1 · fondo 63,5 · Ø 22 vertical")

    L = g.GAP + 2 * g.PL_T + 28
    r = Vista(-20, -30, L + 20, 28, 66)
    r.rect(0, -12.7, L, 25.4, "pieza3")
    for xx in (7, L - 7):
        r.circulo(xx, 0, 2.6)
        r.linea((xx, -16), (xx, 16), "eje")
    r.linea((-6, 0), (L + 6, 0), "eje")
    r.cota_h(0, L, -12.7, -22, f(L))
    r.cota_h(0, 7, 12.7, 20, "7")
    r.cota_v(-12.7, 12.7, L, L + 10, "Ø 25,4")
    bar = r.svg("05 · Barra de carga B", "Escala 1:1 · 2 huecos Ø 5,2 para pasador R")

    c = f"""<div class="cont" style="grid-template-columns:1fr 1fr;grid-template-rows:auto 1fr">
      <div class="bloque" style="grid-column:1/3"><div class="kick">Piezas 02 a 05 · torno, fresa y taladro</div><h2>Casquillo y piezas de la cabeza</h2></div>
      <div class="bloque" style="gap:5mm">
        <div style="display:flex;gap:10mm;align-items:start">{sv}{ev}</div>
        <dl class="ficha">
          <dt>02 Casquillo</dt><dd>Tubo 6061-T6 2½" × 1/4" (Ø 63,5 × 6,35, interior 50,8). Tornear el interior a Ø 51,4 en todo el largo para que entren el espigón y la pata de adentro (Ø 50,8) con 0,6 mm de juego.</dd>
          <dt>Huecos</dt><dd>2 × Ø 13,1 a 25 y 70 de arriba (pernos que lo sujetan a las placas). 2 × Ø 9,9 (huecos G) a 50 y 80 de la boca, para el pasador de pata.</dd>
          <dt>Ranuras F</dt><dd>3 ranuras de 11 × 14 en la boca, a 0°, 120° y 240°. Ahí entra el tope de la pata de afuera y la deja girada en 1 de 3 posiciones, como el Vortex.</dd>
          <dt>Cantidad</dt><dd class="num">2 · {f(KG['02'], 2)} kg c/u</dd>
        </dl>
        <img class="render" src="{img('p02')}" style="height:40mm;justify-self:start">
      </div>
      <div class="bloque" style="gap:6mm">
        <div style="display:flex;gap:8mm;align-items:start;flex-wrap:wrap">{sep}{blo}</div>
        {bar}
        <table><thead><tr><th>N.º</th><th>Pieza</th><th>Material</th><th>Detalle</th></tr></thead><tbody>
          <tr><td class="n">03</td><td>Separador ×4</td><td>Tubo acero 1" × 1/8"</td><td>Largo exacto 63,5: de esto depende que las placas queden paralelas. Refrentar en torno.</td></tr>
          <tr><td class="n">04</td><td>Bloque C ×1</td><td>Al 6061-T6</td><td>Hueco vertical Ø 22 (punto C del Vortex) y 2 huecos Ø 10,5 para pernos M10. Aristas R 4.</td></tr>
          <tr><td class="n">05</td><td>Barra B ×1</td><td>Acero 4140 bonificado</td><td>Ø 25,4 × {f(L)}. Chaflán 1 mm. Se traba con 2 pasadores R de Ø 5 mm. Aquí se cuelga la polea.</td></tr>
        </tbody></table>
      </div>
    </div>"""
    hoja("02–05", "Casquillo y piezas de la cabeza", "Al 6061-T6 · acero", "ver tabla", "1:1", c)
    indice("02 a 05 · Casquillo, separador, bloque C y barra de carga")


# ------------------------------------------------------------------ HOJA: patas
def hoja_patas():
    fuera = g.PE_ESPIGA - g.PE_ESPIGA_DENTRO
    L = g.PE_TOTAL

    def extras_pe(v):
        v.rect(0, -g.MACHO_OD / 2, fuera, g.MACHO_OD, "pieza3")
        v.linea((fuera, -g.MACHO_OD / 2 + g.MACHO_E), (fuera + g.PE_ESPIGA_DENTRO, -g.MACHO_OD / 2 + g.MACHO_E), "oculta")
        v.circulo(g.TOPE_DESDE_PUNTA, g.MACHO_OD / 2 + 3, 4.75, "pieza2")
        v.nota(g.TOPE_DESDE_PUNTA, g.MACHO_OD / 2 + 7, g.TOPE_DESDE_PUNTA + 60, g.EXT_OD / 2 + 70, "tope Ø 9,5 · sale 6")
        v.nota(fuera + 60, 0, fuera + 150, -g.EXT_OD / 2 - 45, "pernos fijos 3/8\" (a 90° de los huecos)")
    hu = [(g.PE_HUECO_ESPIGA, g.D38, ""), (fuera + g.PE_PERNOS[0], g.D38, ""), (fuera + g.PE_PERNOS[1], g.D38, ""),
          (L - g.PE_HUECO_BOCA, g.D38, "")]
    pe_svg = vista_tubo(L, g.EXT_OD, g.EXT_OD - 2 * g.EXT_E, hu, "06 · Pata de afuera", "Escala 1:5", 245,
                        ranuras=[(L - g.RANURA_P, g.RANURA_A, g.RANURA_P)], extras=extras_pe,
                        arriba_txt="espigón (va a la cabeza o a otra pata)", abajo_txt="boca con 3 ranuras")

    def extras_pi(v):
        v.rect(0, -g.MUESCA_A / 2, g.MUESCA_P, g.MUESCA_A, "hueco")
        v.nota(g.PI_HUECOS[0], 0, g.PI_HUECOS[0] + 90, g.MACHO_OD / 2 + 70, "ÚLTIMO HUECO: grabar")
    hu = [(p, g.D38, "") for p in g.PI_HUECOS] + [(g.PI_HUECO_PIE, g.D38, "")]
    pi_svg = vista_tubo(g.PI_L, g.MACHO_OD, g.MACHO_OD - 2 * g.MACHO_E, hu, "07 · Pata de adentro", "Escala 1:5", 228,
                        extras=extras_pi, arriba_txt="muesca 11 × 22", abajo_txt="va al pie")
    c = f"""<div class="cont" style="grid-template-columns:250mm 1fr">
      <div class="bloque" style="gap:6mm">
        <div class="bloque"><div class="kick">Piezas 06 y 07 · sierra, taladro de pedestal y fresa</div><h2>Patas</h2></div>
        {pe_svg}
        {pi_svg}
      </div>
      <div class="bloque" style="gap:3.5mm">
        <img class="render" src="{img('h_patx')}" style="height:70mm;justify-self:center">
        <dl class="ficha">
          <dt>06 Afuera</dt><dd>Tubo 6061-T6 2" cédula 40 (Ø 60,3 × 3,91, interior 52,5) de {f(g.PE_TUBO)} + espigón de tubo 2" × 1/4" de {f(g.PE_ESPIGA)}, metido {f(g.PE_ESPIGA_DENTRO)} y fijado con 2 pernos 3/8" grado 8 con tuerca de seguridad. Largo total {f(L)} (Vortex 1054). {f(KG['06'], 2)} kg.</dd>
          <dt>Tope</dt><dd>Pasador de acero Ø 9,5 × 20 prensado en un hueco radial del espigón, a {f(g.TOPE_DESDE_PUNTA)} de la punta; sobresale 6 mm. Entra en las ranuras F de la cabeza, de otra pata o de la placa de amarre.</dd>
          <dt>07 Adentro</dt><dd>Tubo 6061-T6 2" × 1/4" (Ø 50,8 × 6,35) de {f(g.PI_L)} (Vortex 978). 6 huecos cada 150 desde 60 + 1 hueco a 50 de abajo para el pie. {f(KG['07'], 2)} kg.</dd>
          <dt>Huecos</dt><dd>Todos Ø 9,9 (25/64"), pasantes y en línea. Taladro de pedestal con el tubo en un prisma en V; primero broca de 6, luego 9,9.</dd>
          <dt>Ajuste</dt><dd>La pata de adentro y los espigones (Ø 50,8) tienen que correr suave dentro de la pata de afuera (52,5) y del casquillo (51,4).</dd>
        </dl>
        <div class="aviso"><b>Armado de una pata</b>Cabeza → pata de afuera → pata de afuera → pata de adentro → pie. La pata de adentro va siempre abajo, junto al pie (manual del Vortex, pág. 31 y 37).</div>
      </div>
    </div>"""
    hoja("06–07", "Patas de afuera y de adentro", "Al 6061-T6", "4 + 2", "1:5", c)
    indice("06 y 07 · Patas de afuera y de adentro")


# ------------------------------------------------------------------ HOJA: pies y placa de amarre
def hoja_pies():
    G = g.contorno_garra()
    minx, miny, maxx, maxy = G.bounds
    v = Vista(minx - 35, miny - 28, maxx + 40, g.PIE_CAS_L + 30, 110)
    v.rect(-g.HEMBRA_OD / 2, 0, g.HEMBRA_OD, g.PIE_CAS_L, "pieza3")
    v.linea((-51.5 / 2, 0), (-51.5 / 2, g.PIE_CAS_L), "oculta")
    v.linea((51.5 / 2, 0), (51.5 / 2, g.PIE_CAS_L), "oculta")
    v.forma(G.difference(box(-g.HEMBRA_OD / 2, 0, g.HEMBRA_OD / 2, 200)), "pieza2")
    v.poli([(-38, 0), (-38, 60), (38, 60), (38, 0)], "oculta", cerrado=False)
    for n, x, y, d, _ in g.HUECOS_GARRA:
        v.circulo(x, y, d / 2)
        v.eje_cruz(x, y, d / 2)
        v.texto(x, y - d / 2 - 3.5 * v.k, n, 0.8, cls="etq")
    v.circulo(0, g.PIE_CAS_L - g.PIE_HUECO, g.D38 / 2)
    v.linea((0, miny - 8), (0, g.PIE_CAS_L + 8), "eje")
    v.cota_h(minx, maxx, miny, miny - 14)
    v.cota_v(g.GARRA_PUNTA, g.PIE_CAS_L, maxx, maxx + 24, f(g.PIE_CAS_L - g.GARRA_PUNTA))
    v.cota_v(g.PIE_CAS_L - g.PIE_HUECO, g.PIE_CAS_L, -g.HEMBRA_OD / 2, -g.HEMBRA_OD / 2 - 12, "50")
    v.cota_v(0, 60, 38, 50, "60")
    v.nota(0, g.GARRA_PUNTA + 4, -60, g.GARRA_PUNTA + 20, "recargue duro")
    garra_svg = v.svg("08 · Pie Raptor", "Escala 1:2,5 · garra 12 mm")

    d = Vista(-95, -95, 95, 95, 80)
    d.circulo(0, 0, g.AM_DISCO_D / 2, "pieza")
    d.circulo(0, 0, (g.HEMBRA_OD + 0.4) / 2)
    for n, x, y, dd, _ in g.huecos_circulo(g.AM_HUECOS, g.AM_PCD, g.AM_D):
        d.circulo(x, y, dd / 2)
        d.eje_cruz(x, y, dd / 2)
    d.circulo(0, 0, g.AM_PCD / 2, "eje")
    d.diametro(0, 0, g.AM_DISCO_D / 2, 35, f"Ø {f(g.AM_DISCO_D)}")
    d.diametro(0, 0, g.AM_PCD / 2, 200, f"8 × Ø 22 en Ø {f(g.AM_PCD)}")
    d.diametro(0, 0, (g.HEMBRA_OD + 0.4) / 2, 290, "Ø 63,9")
    disco_svg = d.svg("10 · Disco de amarre", "Escala 1:2 · 1/2\"")

    c = f"""<div class="cont" style="grid-template-columns:118mm 120mm 1fr">
      <div class="bloque" style="gap:4mm">
        <div class="bloque"><div class="kick">Piezas 08 y 09 · acero</div><h2>Pies</h2></div>
        {garra_svg}
        <dl class="ficha">
          <dt>08 Raptor</dt><dd>Casquillo de tubo de acero Ø 63,5 × 6 (interior 51,5) de 120, con 2 ranuras de 12,4 × 60 abajo. La garra de A36 12 mm entra en las ranuras y se suelda con MIG por los dos lados. Punta con recargue duro (electrodo de alta dureza). {f(KG['08'], 2)} kg.</dd>
          <dt>Uso</dt><dd>Garra en tierra, grietas o raíces. Los huecos L1 y L2 son para la maniota o para amarrar el pie a un anclaje.</dd>
        </dl>
      </div>
      <div class="bloque" style="gap:4mm">
        <img class="render" src="{img('p08')}" style="height:52mm">
        <img class="render" src="{img('p09')}" style="height:52mm">
        <dl class="ficha">
          <dt>09 Plano</dt><dd>Base A36 10 mm de 150 × 150 con 4 huecos Ø 14 a 110 × 110 para anclarlo con tus pernos de 1/2". 2 orejas de 8 mm soldadas y una lengüeta que gira en un perno 1/2". Caucho de 5 mm pegado abajo. Opcional.</dd>
        </dl>
      </div>
      <div class="bloque" style="gap:4mm">
        <div class="bloque"><div class="kick">Pieza 10 · mejora sobre el Vortex</div><h2>Placa de amarre de 2 pisos</h2></div>
        <div style="display:flex;gap:6mm;align-items:start">{disco_svg}<img class="render" src="{img('p10')}" style="height:62mm"></div>
        <dl class="ficha">
          <dt>Idea</dt><dd>Del Vortex (placa AZORP) y de la Space Station de SMC. Se pone entre dos patas de afuera, o entre la pata de afuera y la de adentro. Da 16 huecos de mosquetón en medio de la pata, justo en la unión, donde el tubo es más fuerte.</dd>
          <dt>Piezas</dt><dd>Cuerpo de tubo 2½" × 1/4" de 150 (interior 51,4) + espigón 2" × 1/4" de 230 con tope, igual que la pata de afuera. 2 discos de 160 × 12,7 soldados con TIG a 22 y 128 de arriba.</dd>
          <dt>Carga</dt><dd>Máximo 20 kN por disco, tirando en línea con la pata. Para más fuerza, amarrar a la cabeza.</dd>
        </dl>
        <div class="aviso"><b>Soldadura</b>TIG con corriente alterna, varilla ER5356, argón puro. Si el taller puede, tratamiento térmico T6 después de soldar.</div>
      </div>
    </div>"""
    hoja("08–10", "Pies y placa de amarre", "Acero A36 · Al 6061-T6", "2 + 2 + 2", "1:2,5", c)
    indice("08 a 10 · Pies Raptor y plano, placa de amarre de 2 pisos")


# ------------------------------------------------------------------ HOJA: tornillería y compras
def hoja_compras():
    L = g.GAP + 2 * g.PL_T
    filas = [
        ("P1", "Pasador de bola con anillo, 1/2\" (12,7) × 4\" de agarre (101,6)", "6", "Acero inox 17-4 · ≥ 140 kN doble corte",
         "Cabeza: I1 a I4 y orejas A1 y A2"),
        ("P2", "Pasador de bola con anillo, 3/8\" (9,5) × 3\" de agarre (76,2)", "10", "Acero inox 17-4 · ≥ 80 kN doble corte",
         "Pata en la cabeza, uniones de patas, pie; 2 de repuesto"),
        ("T1", "Perno Allen 1/2\"-13 × 4\" grado 8 + tuerca de seguridad (nylon) + 2 arandelas", "4", "Acero aleado",
         "Casquillos a las placas (S1 y S2 de cada lado) · llave Allen 3/8\" · apriete 100 N·m"),
        ("T2", "Perno Allen M10 × 100 clase 12.9 + tuerca de seguridad", "2", "Acero aleado", "Bloque C (C1 y C2) · apriete 45 N·m"),
        ("T3", "Perno hexagonal 3/8\"-16 × 3\" grado 8 + tuerca de seguridad", "8", "Acero aleado",
         "Espigón de cada pata de afuera (2 por pata) · llave 9/16\" (14 mm)"),
        ("T4", "Perno hexagonal 1/2\" × 3\" grado 8 + tuerca de seguridad", "2", "Acero aleado", "Bisagra del pie plano (si se hace)"),
        ("R1", "Pasador R (clip) de Ø 5 mm", "2", "Acero galvanizado", "Seguro de la barra de carga B"),
        ("P3", "Pasador de acero Ø 9,5 × 20 (tope)", "6", "Acero 1045", "Tope de alineación de cada espigón"),
        ("C1", "Cinta de maniota 25 mm con hebilla de leva, 20 kN", "1", "Poliéster", "Entre los huecos L de los pies · 3,5 m"),
        ("C2", "Cuerda estática 11 mm (EN 1891 tipo A) para vientos", "4 × 15 m", "Poliamida", "Orejas A y puntos H a los anclajes, a 45°"),
        ("C3", "Polea de 1,5\" (38 mm) para cuerda de 11 mm, ≥ 36 kN", "1", "Aluminio / acero", "Colgada de la barra B con un mosquetón de acero"),
    ]
    tr = "".join(f'<tr><td class="n">{a}</td><td><b>{escape(b)}</b></td><td class="m">{c}</td><td>{escape(d)}</td><td>{escape(e)}</td></tr>'
                 for a, b, c, d, e in filas)
    c = f"""<div class="cont" style="grid-template-rows:auto 1fr">
      <div style="display:grid;grid-template-columns:1fr 150mm;gap:10mm;align-items:end">
        <div class="bloque"><div class="kick">Piezas que se compran</div><h2>Pasadores, tornillería y cuerdas</h2></div>
        <div class="aviso"><b>No reemplazar por piezas de ferretería</b>Los pasadores y pernos tienen que ser del grado indicado. El manual del Vortex y el del TerrAdaptor lo advierten.</div>
      </div>
      <div style="display:grid;grid-template-columns:1fr 150mm;gap:10mm">
        <table><thead><tr><th>Cód.</th><th>Qué</th><th>Cant.</th><th>Material</th><th>Dónde va</th></tr></thead><tbody>{tr}</tbody></table>
        <div class="bloque" style="gap:4mm">
          <img class="render" src="{img('h_cabx')}" style="height:70mm">
          <dl class="ficha">
            <dt>Pasadores</dt><dd>Se consiguen como "ball lock pin" o "quick release pin" (McMaster-Carr, Amazon). La bola tiene que salir por completo del otro lado (manual TerrAdaptor, pág. 24).</dd>
            <dt>Si no llegan</dt><dd>Un tornero puede hacer pasadores de acero 4140 Ø 12,7 y Ø 9,5 con un hueco de 3 mm en la punta para un pasador R. Pierden rapidez pero no fuerza.</dd>
          </dl>
        </div>
      </div>
    </div>"""
    hoja("COMPRAS", "Pasadores, tornillería y cuerdas", "Varios", "", "S/E", c)
    indice("Pasadores, tornillería, cuerdas y polea")


# ------------------------------------------------------------------ HOJA: fabricación y armado
def hoja_fabricacion():
    pasos = [
        ("Material", "Comprar los tubos 2\" × 1/4\", 2\" cédula 40 y 2½\" × 1/4\" en 6061-T6 con certificado. Probar que el 2\" × 1/4\" corra dentro del 2\" cédula 40. No usar 6063 de ventanería: tiene la mitad de la fuerza."),
        ("Corte láser", "Mandar los DXF al taller: 2 placas de cabeza y 4 discos en Al 1/2\"; 2 garras en A36 12 mm; base del pie plano en A36 10 mm. Chorro de agua es lo mejor para aluminio de 1/2\"."),
        ("Torno", "Tornear el interior de los casquillos, cuerpos de amarre y casquillos de pie a Ø 51,4. Refrentar los 4 separadores a 63,5 exactos. Barra B de 4140."),
        ("Tubos", "Cortar patas: 4 × 940 (afuera), 4 espigones × 230, 2 × 980 (adentro). Huecos en taladro de pedestal con prisma en V, todo medido desde la punta de arriba. Ranuras F con fresa."),
        ("Espigones", "Meter cada espigón 120 mm en su pata de afuera, taladrar los 2 pernos 3/8\" juntos y apretar. Prensar el tope Ø 9,5."),
        ("Cabeza", "Armar placas + separadores + bloque C con los pernos flojos. Meter los casquillos entre las placas, alinear a 30° con el plano y apretar con prensas. Taladrar S1 y S2 atravesando placa, casquillo y placa. Apretar todo."),
        ("Soldadura", "Pies de acero con MIG. Placas de amarre con TIG AC, varilla ER5356. Recargue duro en la punta de la garra."),
        ("Acabado", "Quitar filos. Anodizado azul (cabeza y placas de amarre), natural (patas). Pintura en polvo naranja (pies). Grabar en cada placa: VX-EC, número de serie, fecha, «Trabajo 9 kN / Rotura 36 kN»."),
        ("Prueba", "Armar a 2,45 m con maniota y 4 vientos. Colgar 18 kN (≈ 1.800 kg, 2 veces la carga de trabajo) de la barra B por 3 minutos, sin personas, con tecle y dinamómetro. Repetir con 3 patas de afuera a 11 kN."),
        ("Revisión", "Que ningún tubo quede doblado (regla de 1 m), que ningún hueco se ovale, que los pasadores salgan con la mano. Si algo se deforma, no se usa. Anotar fecha y resultado."),
    ]
    tr = "".join(f'<div class="paso"><span class="k">{i + 1}</span><div><b>{escape(a)}</b><p>{escape(b)}</p></div></div>' for i, (a, b) in enumerate(pasos))
    campo = [
        "Armar todo en el suelo: altura de las patas, pies y cabeza. Revisar que la bola de cada pasador salga del otro lado.",
        "Colgar la polea de la barra B antes de levantar. Pasar la maniota por los huecos L de los pies.",
        "Levantar y poner los vientos: 2 adelante (hacia el borde) y 2 atrás, desde las orejas A. Ángulo 45° o más, nunca menos de 30°.",
        "Si la carga se puede mover de lado, poner también vientos a los lados desde los puntos H.",
        "Tensar la maniota al final, hasta que las patas se flexionen apenas. Inclinación máxima hacia el borde: 15°.",
        "La fuerza de la cuerda tiene que caer dentro del plano de las patas. Cargar poco a poco, con una cuerda de seguridad aparte.",
    ]
    c = f"""<div class="cont" style="grid-template-columns:1fr 1fr">
      <div class="bloque" style="gap:3.2mm">
        <div class="bloque"><div class="kick">Taller</div><h2>Orden de fabricación</h2></div>
        {tr}
      </div>
      <div class="bloque" style="gap:4mm">
        <div class="bloque"><div class="kick">En el lugar</div><h2>Armado para un descenso</h2></div>
        <ol>{''.join(f'<li>{escape(t)}</li>' for t in campo)}</ol>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:4mm">
          <table><thead><tr><th colspan="2">Dónde amarrar</th></tr></thead><tbody>
            <tr><td class="n">B</td><td>Carga principal: polea o carga</td></tr>
            <tr><td class="n">A1 A2</td><td>Vientos adelante y atrás; cabeza gin pole</td></tr>
            <tr><td class="n">I1–I4</td><td>Anclajes de la cabeza, por las ventanas E</td></tr>
            <tr><td class="n">H</td><td>Vientos laterales, hacia afuera</td></tr>
            <tr><td class="n">C</td><td>Mosquetón vertical, cuerda por el canal D</td></tr>
            <tr><td class="n">L1 L2</td><td>Maniota y anclaje de los pies</td></tr>
          </tbody></table>
          <table><thead><tr><th colspan="2">Nunca</th></tr></thead><tbody>
            <tr><td>✕</td><td>Amarrar en medio de un tubo sin placa de amarre</td></tr>
            <tr><td>✕</td><td>Pasar una cuerda en movimiento sobre un pasador</td></tr>
            <tr><td>✕</td><td>Más de 3 patas de afuera por pata</td></tr>
            <tr><td>✕</td><td>Unir la pata de adentro por encima del hueco 1</td></tr>
            <tr><td>✕</td><td>Usarlo sin maniota ni vientos</td></tr>
          </tbody></table>
        </div>
        <div class="aviso"><b>Antes de usar con personas</b>Un ingeniero mecánico revisa y firma estos planos. Se hace la prueba de carga del paso 9. Vida útil máxima: 12 años o hasta la primera deformación.</div>
      </div>
    </div>"""
    hoja("FAB", "Fabricación, prueba y armado", "—", "", "S/E", c)
    indice("Orden de fabricación, prueba de carga y armado en el lugar")


# ------------------------------------------------------------------ generar
hoja_conjunto()
hoja_piezas()
hoja_placa()
hoja_casquillo()
hoja_patas()
hoja_pies()
hoja_compras()
hoja_fabricacion()
portada()
total = len(HOJAS)
html = (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{PROY} Bípode · planos</title>'
        f'<style>{CSS}</style></head><body>' + "".join(render_hoja(h, i + 1, total) for i, h in enumerate(HOJAS)) + "</body></html>")
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(html)
print("hojas", total, "bytes", len(html))
