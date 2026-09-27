"""Página del trípode v10: visor 3D, juego de armado y planos.

Uso:  python3 v10_web.py <carpeta_salida>   (usa ../v10/armado.json y ../v10/web/dibujos.json)
"""
import base64
import json
import os
import sys
from html import escape

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(AQUI, "..", "v10")
OUT = sys.argv[1]
ARM = json.load(open(os.path.join(BASE, "armado.json")))
DOC = json.load(open(os.path.join(BASE, "web", "dibujos.json")))
POSTER = "data:image/png;base64," + base64.b64encode(open(os.path.join(OUT, "poster.png"), "rb").read()).decode()
REPO = "https://github.com/janerictenesaca-alt/aventuras-con-janeric/tree/claude/kind-wozniak-p89zyg/bipode/v10"


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
    ("cadena_B", "Forma B · tubo arriba con carrete", "Regla de huecos", f"Solo la pata del carrete: la pata de adentro atraviesa el casquillo y sale {f(ARM['sale_arriba'], 1)} mm por arriba; las patas de afuera van dadas vuelta."),
    ("cadena_A2", "Forma B · las otras 2 patas", "Regla de huecos", "Forma A con la pata de adentro 2 huecos más adentro: quedan del mismo largo que la pata del carrete. (Las 3 patas apuntan al mismo punto: si las 3 salen mucho por arriba, se cruzan.)"),
    ("arm_cab_frente", "Cabeza A-frame · vista de frente", "Armado · FABRICAR × 1", "Las piezas de la cabeza. Los 2 huecos Ø 25 mm (en vez del corazón) van abajo, con 12 mm de metal al borde."),
    ("arm_cab_arriba", "Cabeza A-frame · vista de arriba", "Armado", "Posición de cada placa desde el centro. Atrás queda abierto, como el Vortex."),
    ("arm_cab_lado", "Cabeza A-frame · vista de lado", "Armado", "El puente 04 va abajo y separado 20 mm de la placa: por ese espacio baja el mosquetón."),
    ("01", "01 · Placa frontal (cara lisa)", "FABRICAR × 1 · Al 6061-T6 15,9 mm (5/8\")", f"Una sola pieza, más gruesa. 2 huecos Ø 25 mm para mosquetón grande, centro a {f(ARM['z_doble'])} mm del borde de abajo (12 mm de metal); las demás medidas no cambian."),
    ("01r", "01r · Cartelita de refuerzo placa–tubo", "FABRICAR × 4 · Al 6061-T6 8 mm", "Sutil, por atrás: arriba y abajo de cada tubo. El lado curvo abraza el tubo. No tapa huecos ni ranuras."),
    ("02", "02 · Casquillo", "FABRICAR × 2 · tubo 2½\" × 1/4\" × 153 mm", "Abierto arriba y abajo. Hueco principal a 63,5 mm de la boca; ajuste fino cada 27,9 mm; 3 ranuras F."),
    ("03", "03 · Aleta", "FABRICAR × 4 · Al 12,7 mm", "Paradas atrás de la placa 01. Dos huecos de pasador 1/2\" (Ø 13,1 mm)."),
    ("04", "04 · Puente central", "FABRICAR × 1 · Al 12,7 mm", "Separado 20 mm de la placa, soldado solo a las 2 aletas de adentro. Hueco C Ø 22 mm con 12 mm de metal adelante y 14 atrás."),
    ("arm_gin", "Gin pole · armado de lado", "Armado · FABRICAR × 1", f"El tubo va a {f(DOC['alfa'])}° del ala para que el ala quede horizontal."),
    ("05", "05 · Ala de la gin pole", "FABRICAR × 1 · Al 12,7 mm", "7 anclajes: 4 óvalos D, hueco P Ø 22 mm en la punta y 2 huecos P2 Ø 22 mm a los lados. Hueco del tubo y 2 ranuras para las lengüetas de las orejas."),
    ("06", "06 · Tubo de la gin pole", "FABRICAR × 1 · tubo 2½\" × 1/4\"", f"Lado largo {f(DOC['gin_largo'])} mm, lado corto {f(DOC['gin_corto'])} mm. Huecos a 63,5 y 91,4 mm de la boca."),
    ("07", "07 · Oreja reforzada", "FABRICAR × 2 · Al 12,7 mm", "La lengüeta atraviesa el ala y se suelda arriba y abajo; el cuerpo sigue 110 mm bajo el ala con el borde en diagonal. El hueco del pasador no cambia de lugar."),
    ("08", "08 · Ojo central", "FABRICAR × 1 · Al 12,7 mm", "Punto B de la gin pole. Hueco Ø 25 mm con 12,5 mm de metal."),
    ("09", "09 · Cartela", "FABRICAR × 2 · Al 12,7 mm", "Unen el ala con el tubo, una a cada lado."),
    ("10", "10 · Pata de afuera", "FABRICAR × 7 (6 + 1 de repuesto)", "Cuerpo 2\" céd. 40 de 902 mm + espiga macho de 152 mm afuera, con tope. Total 1054 mm, igual al Vortex."),
    ("10m", "10 · Detalle del macho", "Escala 1:2", "Hueco a 88,5 mm de la punta (63,5 mm del escalón). Tope a 5,5 mm del escalón. 2 pernos fijos."),
    ("10h", "10 · Detalle de la hembra", "Escala 1:2", "Hueco a 63,5 mm de la boca. Ranura de 10,5 × 11 mm para el tope."),
    ("13", "13 · Pata de adentro", "FABRICAR × 3 · tubo 2\" × 1/4\" × 965,2 mm", "7 huecos: 63,5 mm de cada punta y cada 139,7 mm. Se usa en cualquier sentido."),
    ("14", "14 · Pie de flecha", "FABRICAR × 3 · casquillo Al + garra A36", "Casquillo de 215 mm: entra el macho completo sobre la garra. Hueco a 63,5 mm de la boca."),
    ("15", "15 · Carrete naranja", "FABRICAR × 1 · disco 12,7 mm + tubo", "Simétrico, 127 mm: sirve derecho o de cabeza. 9 anclajes Ø 24 mm."),
    ("16", "16 · Carrete azul", "FABRICAR × 1 · disco 12,7 mm + tubo", "142,2 mm. 2 filas de huecos a 90°: una desde el disco y otra desde la boca."),
    ("carrete", "Carrete armado", "15 + 16", "Luz de 129,5 mm entre discos: cabe la cabeza de la gin pole de lado, con 2 pasadores 1/2\" verticales."),
    ("17b", "17b · Placa principal del AHP", "FABRICAR × 1 · A36 25,4 mm (1\")", "Igual al original: centro con 4 huecos Ø 25 mm (2 a cada lado) y 2 patitas con 52 mm de luz. Pasador 3/8\" de canto a 24 mm de la punta."),
    ("17a", "17a · Tubo cuadrado (punta)", "FABRICAR × 1 · tubo A36 2\" × 2\" × 1/4\"", "Va por atrás de la placa y entra directo en el enganche del carro. Hueco Ø 16,5 mm a 60 mm de la punta."),
    ("17d", "17d · Pared de refuerzo", "FABRICAR × 1 · A36 12,7 mm", "Cruzada atrás, donde empieza el tubo."),
    ("17e", "17e · Cartela de atrás", "FABRICAR × 2 · A36 12,7 mm", "Una a cada lado del tubo, lo une con la placa (como la gin pole)."),
    ("17f", "17f · Orejita", "FABRICAR × 2 · A36 12,7 mm", "Afuera de cada patita, inclinada 10° hacia atrás. Ventana de 26 × 36 mm para mosquetón o maniota."),
    ("18f", "18f · Base del pie con rótula", "FABRICAR × 3 · A36 10 mm", "4 huecos Ø 14 mm para pernos de anclaje y 2 huecos Ø 25 mm para mosquetón. Suela de caucho de 5 mm abajo."),
    ("18e", "18e · Anillo de retención", "FABRICAR × 3 · acero 1045 12 mm", "Aprieta la bola de enganche de 2\" contra el asiento con 8 tornillos M8."),
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
    ("cabeza_v10.step · tripode_v10.step · accesorios_v10.step", "Conjuntos 3D (STEP)", "La cabeza con la gin pole, el trípode armado, y los accesorios: carretes, AHP y pie con rótula."),
    ("stl/", "Mallas (STL)", "Para imprimir en 3D una maqueta y probar antes de cortar."),
    ("plano/VX-EC_Tripode_v10_planos_RevF.pdf", "Planos (PDF, A3)", "13 hojas: todas las medidas en milímetros, «FABRICAR × N» en cada pieza, kit completo, regla de huecos, AHP, pie con rótula, soldadura y prueba."),
]
archivos = "".join(f'<li><code>{escape(a)}</code><b>{escape(b)}</b><span>{escape(c)}</span></li>' for a, b, c in ARCHIVOS)

PASOS_SOLDAR = [
    dict(t="Placa frontal 01", d="Boca abajo sobre una mesa plana: la cara lisa contra la mesa.", p=["c_01"]),
    dict(t="4 aletas 03", d="Paradas con escuadra a ±33,3 y ±64 mm del centro (cara de adentro). Un eje de Ø 12 mm por los huecos las deja en línea. Puntear.", p=["c_03a", "c_03b", "c_03c", "c_03d"]),
    dict(t="Puente central 04", d="Acostado abajo entre las aletas de adentro, separado 20 mm de la placa (por ahí baja el mosquetón), con el hueco C.", p=["c_04"]),
    dict(t="2 casquillos 02", d="Con un gabarit a 26,5°. El borde de la placa 01 toca el tubo por atrás; adelante queda una V para soldar. Luego TIG alternando lados.", p=["c_02a", "c_02b"]),
    dict(t="4 cartelitas 01r", d="Refuerzo sutil por atrás, arriba y abajo de cada tubo, entre la placa y el tubo.", p=["c_01ria", "c_01rib", "c_01rda", "c_01rdb"]),
    dict(t="Ala de la gin pole 05", d="Aparte, boca abajo sobre la mesa.", p=["g_05"]),
    dict(t="Orejas 07 y ojo 08", d="La lengüeta de cada oreja entra en su ranura del ala y se suelda arriba y abajo; el ojo colgado al centro.", p=["g_07a", "g_07b", "g_08"]),
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


def a(*ids):
    return ["a_" + i for i in ids]


PASOS_CARRETE = [
    dict(t="Pata de adentro parada", d="Cualquier tubo de Ø 50,8 mm: la pata de adentro o el macho de una pata de afuera.", p=a("c13")),
    dict(t="Carrete azul abajo", d="Disco abajo. Su tubo sube 129,5 mm: esa es la luz entre los 2 discos.", p=a("c16")),
    dict(t="Gin pole de lado", d="La cabeza naranja entra de lado entre los discos; las orejas quedan sobre los huecos del disco.", p=a("cG05", "cG06", "cG07a", "cG07b", "cG08", "cG09a", "cG09b")),
    dict(t="Carrete naranja de cabeza", d="Disco arriba, su tubo baja dentro del azul. Como es simétrico, sirve derecho o de cabeza.", p=a("c15")),
    dict(t="Pasador 3/8\" del carrete", d="Atraviesa el azul, el naranja y la pata: los huecos coinciden (91,4 del azul = 63,5 del naranja).", p=a("cP1")),
    dict(t="2 pasadores 1/2\" verticales", d="Bajan por los huecos de los discos y por las orejas de la gin pole: la gin pole queda sujeta de lado.", p=a("cP2", "cP3")),
]
PASOS_AHP = [
    dict(t="Placa principal 17b", d="Una sola placa de 1\": el centro con 4 huecos y las 2 patitas, como el original.", p=a("17b")),
    dict(t="Pared 17d", d="Cruzada por atrás, donde empieza el tubo.", p=a("17d")),
    dict(t="Tubo cuadrado 17a", d="Va por atrás de la placa y sale hacia el enganche del carro.", p=a("17a")),
    dict(t="2 cartelas 17e", d="Una a cada lado del tubo: refuerzo como en la gin pole.", p=a("17ei", "17ed")),
    dict(t="2 orejitas 17f", d="Afuera de cada patita, inclinadas 10° hacia atrás.", p=a("17fi", "17fd")),
    dict(t="Pata y pasador", d="La pata de adentro entra entre las patitas y el pasador 3/8\" × 4\" la deja girar.", p=a("17x", "17p")),
]
PASOS_ROTULA = [
    dict(t="Base 18f y suela 18g", d="Base A36 de 10 mm con 4 huecos de anclaje y 2 de mosquetón; caucho de 5 mm abajo.", p=a("18f", "18g")),
    dict(t="Asiento 18d", d="Copa esférica soldada a la base.", p=a("18d")),
    dict(t="Bola de enganche 18c", d="Bola de 2\" que se compra; se aprieta al tapón con su tuerca.", p=a("18c")),
    dict(t="Anillo 18e y 8 tornillos M8", d="El anillo encierra la bola: gira pero no sale.", p=a("18e", "18h")),
    dict(t="Tapón 18b y casquillo 18a", d="El casquillo recibe la pata como el pie de flecha (hueco a 63,5 mm).", p=a("18b", "18a")),
]

DATA = dict(tri=PIEZAS_T, nombres=NOMBRES, soldar=PASOS_SOLDAR, armar=PASOS_ARMAR, carrete=PASOS_CARRETE, ahp=PASOS_AHP, rotula=PASOS_ROTULA)

html = open(os.path.join(AQUI, "v10_web_plantilla.html"), encoding="utf-8").read()
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
