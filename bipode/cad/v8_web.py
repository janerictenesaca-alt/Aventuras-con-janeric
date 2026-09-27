"""Página del trípode v8: visor 3D, juego de armado y planos.

Uso:  python3 v8_web.py <carpeta_salida>   (usa ../v8/armado.json y ../v8/web/dibujos.json)
"""
import base64
import json
import os
import sys
from html import escape

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(AQUI, "..", "v8")
OUT = sys.argv[1]
ARM = json.load(open(os.path.join(BASE, "armado.json")))
DOC = json.load(open(os.path.join(BASE, "web", "dibujos.json")))
POSTER = "data:image/png;base64," + base64.b64encode(open(os.path.join(OUT, "poster.png"), "rb").read()).decode()
REPO = "https://github.com/janerictenesaca-alt/aventuras-con-janeric/tree/claude/kind-wozniak-p89zyg/bipode/v8"


def f(v, dec=1):
    s = f"{v:.{dec}f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s.replace(".", ",")


NOMBRES = {p["id"]: p["nombre"] for p in ARM["piezas"] + ARM["piezas_B"] + ARM["acc"]}
PIEZAS_T = [dict(n=p["node"], id=p["id"], nom=p["nombre"], g=p["grupo"],
                 e=[p["explota"][0], p["explota"][2], -p["explota"][1]]) for p in ARM["piezas"]]

TARJETAS = [
    ("cadena_A", "Forma A · patas largas", "Regla de huecos", "Macho arriba en el casquillo, 2 patas de afuera, pata de adentro y pie. Los números son las distancias de cada pasador desde la boca del casquillo."),
    ("cadena_B", "Forma B · tubo arriba", "Regla de huecos", f"La pata de adentro atraviesa el casquillo y sale {f(ARM['sale_arriba'], 0)} mm por arriba para el carrete; las patas de afuera van dadas vuelta."),
    ("arm_cab_frente", "Cabeza A-frame · vista de frente", "Armado", "Las 8 piezas de la cabeza. Las aletas de atrás van en línea oculta."),
    ("arm_cab_arriba", "Cabeza A-frame · vista de arriba", "Armado", "Posición de cada placa desde el centro: 36, 46, 64 y 74 mm. Atrás queda abierto, como el Vortex."),
    ("arm_cab_lado", "Cabeza A-frame · vista de lado", "Armado", "Fondo 88 mm desde la cara lisa. Pasadores a 46 mm del eje del tubo."),
    ("01", "01 · Placa frontal (cara lisa)", "1 pieza · Al 6061-T6 10 mm", "Una sola pieza, como la cara lisa del Vortex. Ventanas E, corazón B y 2 muescas."),
    ("02", "02 · Casquillo", "2 piezas · tubo 2½\" × 1/4\" × 153 mm", "Abierto arriba y abajo. Hueco principal a 63,5 mm de la boca; ajuste fino cada 27,9 mm; 3 ranuras F."),
    ("03", "03 · Aleta", "4 piezas iguales · 10 mm", "Paradas atrás de la placa 01. Dos huecos de pasador 1/2\" (Ø 13,1 mm)."),
    ("04", "04 · Puente central", "1 pieza · 10 mm", "Chico, abajo, con el hueco C de Ø 22 mm. Reemplaza la placa trasera que sobraba."),
    ("arm_gin", "Gin pole · armado de lado", "Armado", f"El tubo va a {f(DOC['alfa'])}° del ala para que el ala quede horizontal."),
    ("05", "05 · Ala de la gin pole", "1 pieza · 10 mm", "Escudo con 4 óvalos D de anclaje y hueco elíptico del tubo."),
    ("06", "06 · Tubo de la gin pole", "1 pieza · tubo 2½\" × 1/4\"", f"Lado largo {f(DOC['gin_largo'])} mm, lado corto {f(DOC['gin_corto'])} mm. Huecos a 63,5 y 91,4 mm de la boca."),
    ("07", "07 · Oreja de la gin pole", "2 piezas · 10 mm", "Entran en las ranuras de la cabeza; el pasador de arriba hace de bisagra."),
    ("08", "08 · Ojo central", "1 pieza · 10 mm", "Punto B de la gin pole. Hueco Ø 25 mm."),
    ("09", "09 · Cartela", "2 piezas · 10 mm", "Unen el ala con el tubo, una a cada lado."),
    ("10", "10 · Pata de afuera", "7 piezas (6 + 1 de repuesto)", "Cuerpo 2\" céd. 40 de 902 mm + espiga macho de 152 mm afuera, con tope. Total 1054 mm, igual al Vortex."),
    ("10m", "10 · Detalle del macho", "Escala 1:2", "Hueco a 88,5 mm de la punta (63,5 mm del escalón). Tope a 5,5 mm del escalón. 2 pernos fijos."),
    ("10h", "10 · Detalle de la hembra", "Escala 1:2", "Hueco a 63,5 mm de la boca. Ranura de 10,5 × 11 mm para el tope."),
    ("13", "13 · Pata de adentro", "3 piezas · tubo 2\" × 1/4\" × 965,2 mm", "7 huecos: 63,5 mm de cada punta y cada 139,7 mm. Se usa en cualquier sentido."),
    ("14", "14 · Pie de flecha", "3 piezas · casquillo Al + garra A36", "Casquillo Ø 60,3 mm (el carrete azul entra encima). Hueco a 63,5 mm de la boca."),
    ("15", "15 · Carrete naranja", "1 pieza · disco 10 mm + tubo", "Entra en Ø 50,8 mm. Llave para el tope. 9 anclajes + hueco chico de marca."),
    ("16", "16 · Carrete azul", "1 pieza · disco 10 mm + tubo", "Entra en Ø 60,3 mm (pata de afuera, tubo naranja o pie). 9 anclajes + hueco chico."),
    ("carrete", "Carrete armado", "15 + 16", "Azul abajo, naranja arriba con su tubo dentro del azul. Alto 127 mm; los huecos coinciden."),
    ("17", "17 · Poste de enganche AHP", "1 pieza · Al 1\" (25,4 mm)", "Para el carro. La U recibe la pata de adentro y el pasador cruza de canto. 4 anclajes."),
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
    ("cabeza_v8.step · tripode_v8.step · accesorios_v8.step", "Conjuntos 3D (STEP)", "La cabeza con la gin pole, el trípode armado, y el carrete con el AHP."),
    ("stl/", "Mallas (STL)", "Para imprimir en 3D una maqueta y probar antes de cortar."),
    ("plano/VX-EC_Tripode_v8_planos_RevD.pdf", "Planos (PDF, A3)", "12 hojas: todas las medidas en milímetros, lista de piezas, regla de huecos, soldadura y prueba."),
]
archivos = "".join(f'<li><code>{escape(a)}</code><b>{escape(b)}</b><span>{escape(c)}</span></li>' for a, b, c in ARCHIVOS)

PASOS_SOLDAR = [
    dict(t="Placa frontal 01", d="Boca abajo sobre una mesa plana: la cara lisa contra la mesa.", p=["c_01"]),
    dict(t="4 aletas 03", d="Paradas con escuadra a 36, 46, 64 y 74 mm del centro. Un eje de Ø 12 mm por los huecos las deja en línea. Puntear.", p=["c_03a", "c_03b", "c_03c", "c_03d"]),
    dict(t="Puente central 04", d="Acostado abajo entre las aletas de adentro, con el hueco C. Atrás queda abierto.", p=["c_04"]),
    dict(t="2 casquillos 02", d="Con un gabarit a 26,5°. El borde de la placa 01 toca el tubo por atrás; adelante queda una V para soldar. Luego TIG alternando lados.", p=["c_02a", "c_02b"]),
    dict(t="Ala de la gin pole 05", d="Aparte, boca abajo sobre la mesa.", p=["g_05"]),
    dict(t="Orejas 07 y ojo 08", d="Las orejas paradas a 50 … 60 mm del centro; el ojo colgado al centro.", p=["g_07a", "g_07b", "g_08"]),
    dict(t="Tubo 06 y cartelas 09", d=f"El tubo pasa por el hueco elíptico a {f(DOC['alfa'])}°. Las cartelas lo unen al ala.", p=["g_06", "g_09a", "g_09b"]),
    dict(t="Pasadores y 2 poleas", d="Las orejas entran en las ranuras y los 2 pasadores de arriba hacen de bisagra. Abajo, 2 pasadores con una polea cada uno.", p=["c_P-I1i", "c_P-I1d", "c_P-I2i", "c_P-I2d", "c_PLi", "c_PLd"]),
]


def nodos(pref):
    return [p["node"] for p in ARM["piezas"] if any(p["id"].startswith(x) for x in pref)]


def nodos_exact(ids):
    return [p["node"] for p in ARM["piezas"] if p["id"] in ids]


PASOS_ARMAR = [
    dict(t="Cabeza A-frame", d="Ya viene soldada: 8 piezas azules en una sola.", p=[p["node"] for p in ARM["piezas"] if p["grupo"] == "cabeza"]),
    dict(t="Gin pole", d="Sus 2 orejas entran en las ranuras de atrás de la cabeza.", p=[p["node"] for p in ARM["piezas"] if p["grupo"] == "gin"]),
    dict(t="4 pasadores de cabeza y 2 poleas", d="Los 2 de arriba son la bisagra de la gin pole. Una polea en cada pasador de abajo.", p=nodos_exact(["P-I1i", "P-I1d", "P-I2i", "P-I2d", "PLi", "PLd"])),
    dict(t="Primera pata de afuera", d="El macho entra en el casquillo, el tope en una ranura F, y el pasador a 63,5 mm de la boca.", p=nodos_exact(["10I1", "10D1", "10G1", "PP-I1", "PP-D1", "PP-G1"])),
    dict(t="Segunda pata de afuera", d="Su macho entra en la hembra de la primera; los huecos coinciden solos.", p=nodos_exact(["10I2", "10D2", "10G2", "PP-I2", "PP-D2", "PP-G2"])),
    dict(t="Patas de adentro", d="Entran en la hembra de la segunda. Cada hueco (cada 139,7 mm) da otra altura.", p=nodos_exact(["13I1", "13D1", "13G1", "PP-I3", "PP-D3", "PP-G3"])),
    dict(t="Pies de flecha", d="La punta de la pata de adentro entra en el pie; pasador a 63,5 mm.", p=nodos_exact(["14I1", "14D1", "14G1", "PP-I4", "PP-D4", "PP-G4"])),
    dict(t="Maniotas", d="Cinta entre los 3 pies para que no se abran. Tensar al final.", p=nodos_exact(["M1", "M2", "M3"])),
]

DATA = dict(tri=PIEZAS_T, nombres=NOMBRES, soldar=PASOS_SOLDAR, armar=PASOS_ARMAR)

html = open(os.path.join(AQUI, "v8_web_plantilla.html"), encoding="utf-8").read()
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
    "%%ALTURAB%%": f(ARM["altura_B"] / 1000, 2),
    "%%SALE%%": f(ARM["sale_arriba"], 0),
}
for k, v in rep.items():
    html = html.replace(k, v)
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(html)
print("bytes", len(html))
