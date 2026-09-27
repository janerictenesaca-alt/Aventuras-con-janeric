"""Página del trípode v7: visor 3D, juego de armado y planos.

Uso:  python3 v7_web.py <carpeta_salida>   (usa ../v7/armado.json y ../v7/web/dibujos.json)
"""
import base64
import json
import os
import sys
from html import escape

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(AQUI, "..", "v7")
OUT = sys.argv[1]
ARM = json.load(open(os.path.join(BASE, "armado.json")))
DOC = json.load(open(os.path.join(BASE, "web", "dibujos.json")))
POSTER = "data:image/png;base64," + base64.b64encode(open(os.path.join(OUT, "poster.png"), "rb").read()).decode()
REPO = "https://github.com/janerictenesaca-alt/aventuras-con-janeric/tree/claude/kind-wozniak-p89zyg/bipode/v7"


def f(v, dec=1):
    s = f"{v:.{dec}f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s.replace(".", ",")


NOMBRES = {p["id"]: p["nombre"] for p in ARM["piezas"]}
PIEZAS_T = [dict(n=p["node"], id=p["id"], nom=p["nombre"], g=p["grupo"],
                 e=[p["explota"][0], p["explota"][2], -p["explota"][1]]) for p in ARM["piezas"]]

TARJETAS = [
    ("arm_cab_frente", "Cabeza A-frame · vista de frente", "Armado", "Las 11 piezas de la cabeza. Las aletas de atrás van en línea oculta."),
    ("arm_cab_arriba", "Cabeza A-frame · vista de arriba", "Armado", "Posición de cada placa desde el centro: 36, 46, 64 y 74 mm."),
    ("arm_cab_lado", "Cabeza A-frame · vista de lado", "Armado", "Fondo 88 mm desde la cara lisa. Pasadores a 46 mm del tubo."),
    ("01", "01 · Placa frontal (cara lisa)", "1 pieza · Al 6061-T6 10 mm", "Una sola pieza, como la cara lisa del Vortex. Ventanas E, corazón B y 2 muescas."),
    ("02", "02 · Casquillo", "2 piezas · tubo 2½\" × 1/4\" × 153", "Tornear por dentro a Ø 51,4. 5 huecos G de frente, 2 de lado, 3 ranuras F."),
    ("03", "03 · Aleta", "4 piezas iguales · 10 mm", "Paradas atrás de la placa 01. Dos huecos de pasador 1/2\" (Ø 13,1)."),
    ("04", "04 · Placa trasera central", "1 pieza · 10 mm", "Entre las aletas de adentro. Silla D arriba, ventana y corazón."),
    ("05", "05 · Placa de fondo", "1 pieza · 10 mm", "Acostada abajo. Hueco C de Ø 22 para mosquetón vertical."),
    ("06", "06 · Escuadra lateral", "2 piezas · 10 mm", "Une la aleta de afuera con el tubo. Una se corta dada vuelta."),
    ("arm_gin", "Gin pole · armado de lado", "Armado", f"El tubo va a {f(DOC['alfa'])}° del ala para que el ala quede horizontal."),
    ("07", "07 · Ala de la gin pole", "1 pieza · 10 mm", "Escudo con 4 óvalos D de anclaje y hueco elíptico del tubo."),
    ("08", "08 · Tubo de la gin pole", "1 pieza · tubo 2½\" × 1/4\"", f"Lado largo {f(DOC['gin_largo'])}, lado corto {f(DOC['gin_corto'])}. 2 huecos G."),
    ("09", "09 · Oreja de la gin pole", "2 piezas · 10 mm", "Entran en las ranuras de la cabeza; el pasador de arriba hace de bisagra."),
    ("10", "10 · Ojo central", "1 pieza · 10 mm", "Punto B de la gin pole. Hueco Ø 25."),
    ("11", "11 · Cartela", "2 piezas · 10 mm", "Unen el ala con el tubo, una a cada lado."),
    ("21", "21 · Pata de afuera", "6 piezas · tubo 2\" céd. 40 + espigón", "Largo total 1050. 2 por pata."),
    ("22", "22 · Pata de adentro", "3 piezas · tubo 2\" × 1/4\" × 980", "6 huecos para la altura + 1 para el pie. Va siempre abajo."),
    ("23", "23 · Pie Raptor", "3 piezas · acero A36", "Garra de 12 mm de láser soldada con MIG a un casquillo."),
]

tarjetas = "".join(
    f'<article class="plano" id="p-{k}"><header><h3>{escape(t)}</h3><p class="meta">{escape(m)}</p></header>'
    f'<div class="papel">{DOC["dibujos"][k]}</div><p>{escape(d)}</p></article>' for k, t, m, d in TARJETAS)

lista = "".join(f'<tr><td class="n">{p["n"]}</td><td>{escape(p["nombre"])}</td><td>{escape(p["material"])}</td>'
                f'<td class="num">{p["cant"]}</td><td class="num">{f(p["kg"], 2)}</td></tr>' for p in DOC["lista"])
compras = "".join(f'<tr><td class="n">{a}</td><td>{escape(b)}</td><td class="num">{escape(c)}</td><td>{escape(d)}</td><td>{escape(e)}</td></tr>'
                  for a, b, c, d, e in DOC["compras"])
taller = "".join(f'<li><b>{escape(a)}.</b> {escape(b)}</li>' for a, b in DOC["taller"])
campo = "".join(f'<li>{escape(t)}</li>' for t in DOC["campo"])
alturas = "".join(f'<tr{" class=dest" if (a["ext"], a["hueco"]) == (2, 1) else ""}><td class="num">{a["ext"]}</td><td class="num">{a["hueco"]}</td>'
                  f'<td class="num">{f(a["h"] / 1000, 2)} m</td><td class="num">{f(a["lado"] / 1000, 2)} m</td></tr>' for a in DOC["alturas"])

ARCHIVOS = [
    ("dxf/", "Corte láser (DXF, mm)", "Una pieza por archivo, en milímetros, capa CORTE. Lo abre cualquier programa de láser, AutoCAD, LibreCAD, SolidWorks, Fusion 360."),
    ("svg/", "Corte láser (SVG 1:1)", "Mismo contorno en SVG a escala real, para LightBurn, Inkscape o Illustrator."),
    ("step/ · iges/", "Piezas 3D (STEP e IGES)", "Cada pieza sólida por separado, para SolidWorks, Inventor, Fusion 360, FreeCAD o el CNC."),
    ("cabeza_v7.step · tripode_v7.step", "Conjuntos 3D (STEP)", "La cabeza con la gin pole, y el trípode completo armado."),
    ("stl/", "Mallas (STL)", "Para imprimir en 3D una maqueta y probar antes de cortar."),
    ("plano/VX-EC_Tripode_v7_planos_RevC.pdf", "Planos (PDF, A3)", "9 hojas con medidas, lista de piezas, soldadura y prueba."),
]
archivos = "".join(f'<li><code>{escape(a)}</code><b>{escape(b)}</b><span>{escape(c)}</span></li>' for a, b, c in ARCHIVOS)

PASOS_SOLDAR = [
    dict(t="Placa frontal 01", d="Boca abajo sobre una mesa plana: la cara lisa contra la mesa.", p=["c_01"]),
    dict(t="4 aletas 03", d="Paradas con escuadra a 36, 46, 64 y 74 mm del centro. Un eje de Ø 12 por los huecos las deja en línea. Puntear.", p=["c_03a", "c_03b", "c_03c", "c_03d"]),
    dict(t="Fondo 05 y placa trasera 04", d="El fondo acostado abajo entre las aletas de adentro; la trasera al ras del borde de atrás.", p=["c_05", "c_04"]),
    dict(t="2 casquillos 02", d=f"Con un gabarit a 26,5°. El borde de la placa 01 toca el tubo por atrás; adelante queda una V para soldar.", p=["c_02a", "c_02b"]),
    dict(t="2 escuadras 06", d="Arriba, de la aleta de afuera al tubo. Luego soldar todo con TIG, alternando lados.", p=["c_06a", "c_06b"]),
    dict(t="Ala de la gin pole 07", d="Aparte, boca abajo sobre la mesa.", p=["g_07"]),
    dict(t="Orejas 09 y ojo 10", d="Las orejas paradas a 50 … 60 mm del centro; el ojo colgado al centro.", p=["g_09a", "g_09b", "g_10"]),
    dict(t="Tubo 08 y cartelas 11", d=f"El tubo pasa por el hueco elíptico a {f(DOC['alfa'])}°. Las cartelas lo unen al ala.", p=["g_08", "g_11a", "g_11b"]),
    dict(t="Pasadores y polea", d="Las orejas entran en las ranuras y los 2 pasadores de arriba hacen de bisagra. Abajo, 2 pasadores más y la polea.", p=["c_P-I1i", "c_P-I1d", "c_P-I2i", "c_P-I2d", "c_PL"]),
]


def nodos(pref):
    return [p["node"] for p in ARM["piezas"] if any(p["id"].startswith(x) for x in pref)]


def nodos_exact(ids):
    return [p["node"] for p in ARM["piezas"] if p["id"] in ids]


PASOS_ARMAR = [
    dict(t="Cabeza A-frame", d="Ya viene soldada: 11 piezas azules en una sola.", p=[p["node"] for p in ARM["piezas"] if p["grupo"] == "cabeza"]),
    dict(t="Gin pole", d="Sus 2 orejas entran en las ranuras de atrás de la cabeza.", p=[p["node"] for p in ARM["piezas"] if p["grupo"] == "gin"]),
    dict(t="4 pasadores de cabeza y polea", d="Los 2 de arriba son la bisagra de la gin pole. La polea cuelga del de abajo a la izquierda.", p=nodos_exact(["P-I1i", "P-I1d", "P-I2i", "P-I2d", "PL"])),
    dict(t="Primera pata de afuera", d="Una en cada casquillo y en el tubo de la gin pole, con su pasador 3/8\".", p=nodos_exact(["21I1", "21D1", "21G1", "PP-I1", "PP-D1", "PP-G1"])),
    dict(t="Segunda pata de afuera", d="Se enchufa en la primera con su pasador.", p=nodos_exact(["21I2", "21D2", "21G2", "PP-I2", "PP-D2", "PP-G2"])),
    dict(t="Patas de adentro", d="Van siempre abajo. El hueco elegido da la altura.", p=nodos_exact(["22I", "22D", "22G", "PP-Ii", "PP-Di", "PP-Gi"])),
    dict(t="Pies Raptor", d="La garra se clava en tierra, grieta o raíz.", p=nodos_exact(["23I", "23D", "23G", "PP-Ip", "PP-Dp", "PP-Gp"])),
    dict(t="Maniotas", d="Cinta entre los 3 pies para que no se abran. Tensar al final.", p=nodos_exact(["M1", "M2", "M3"])),
]

DATA = dict(tri=PIEZAS_T, nombres=NOMBRES, soldar=PASOS_SOLDAR, armar=PASOS_ARMAR)

html = open(os.path.join(AQUI, "v7_web_plantilla.html"), encoding="utf-8").read()
rep = {
    "%%DATA%%": json.dumps(DATA, ensure_ascii=False),
    "%%POSTER%%": POSTER,
    "%%TARJETAS%%": tarjetas,
    "%%LISTA%%": lista,
    "%%COMPRAS%%": compras,
    "%%TALLER%%": taller,
    "%%CAMPO%%": campo,
    "%%ALTURAS%%": alturas,
    "%%ARCHIVOS%%": archivos,
    "%%REPO%%": REPO,
    "%%KGC%%": f(DOC["kg_cabeza"], 2),
    "%%KGG%%": f(DOC["kg_gin"], 2),
    "%%ALTURA%%": f(ARM["altura_I2"] / 1000, 2),
    "%%ALFA%%": f(DOC["alfa"]),
}
for k, v in rep.items():
    html = html.replace(k, v)
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(html)
print("bytes", len(html))
