"""Página del trípode v9: visor 3D, juego de armado y planos.

Uso:  python3 v9_web.py <carpeta_salida>   (usa ../v9/armado.json y ../v9/web/dibujos.json)
"""
import base64
import json
import os
import sys
from html import escape

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(AQUI, "..", "v9")
OUT = sys.argv[1]
ARM = json.load(open(os.path.join(BASE, "armado.json")))
DOC = json.load(open(os.path.join(BASE, "web", "dibujos.json")))
POSTER = "data:image/png;base64," + base64.b64encode(open(os.path.join(OUT, "poster.png"), "rb").read()).decode()
REPO = "https://github.com/janerictenesaca-alt/aventuras-con-janeric/tree/claude/kind-wozniak-p89zyg/bipode/v9"


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
    ("arm_cab_frente", "Cabeza A-frame · vista de frente", "Armado · FABRICAR × 1", "Las 8 piezas de la cabeza. Los 2 huecos Ø 25 mm reemplazan al corazón."),
    ("arm_cab_arriba", "Cabeza A-frame · vista de arriba", "Armado", "Posición de cada placa desde el centro. Atrás queda abierto, como el Vortex."),
    ("arm_cab_lado", "Cabeza A-frame · vista de lado", "Armado", f"El puente 04 sube a {f(ARM['puente_z0'])} mm: queda 5 mm por debajo de la gin pole cuando la pata se junta."),
    ("01", "01 · Placa frontal (cara lisa)", "FABRICAR × 1 · Al 6061-T6 15,9 mm (5/8\")", f"Una sola pieza, más gruesa. 2 huecos Ø 25 mm para mosquetón grande a {f(ARM['z_doble'])} mm del borde de abajo; las demás medidas no cambian."),
    ("02", "02 · Casquillo", "FABRICAR × 2 · tubo 2½\" × 1/4\" × 153 mm", "Abierto arriba y abajo. Hueco principal a 63,5 mm de la boca; ajuste fino cada 27,9 mm; 3 ranuras F."),
    ("03", "03 · Aleta", "FABRICAR × 4 · Al 12,7 mm", "Paradas atrás de la placa 01. Dos huecos de pasador 1/2\" (Ø 13,1 mm)."),
    ("04", "04 · Puente central", "FABRICAR × 1 · Al 12,7 mm", "Subido, con el hueco C de Ø 22 mm más cerca de la placa y 14 mm de metal atrás. No tapa los 2 huecos."),
    ("arm_gin", "Gin pole · armado de lado", "Armado · FABRICAR × 1", f"El tubo va a {f(DOC['alfa'])}° del ala para que el ala quede horizontal."),
    ("05", "05 · Ala de la gin pole", "FABRICAR × 1 · Al 12,7 mm", "4 óvalos D, hueco P Ø 22 mm nuevo en la punta, hueco del tubo y 2 ranuras para las lengüetas de las orejas."),
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
    ("17a", "17a · Espiga cuadrada del AHP", "FABRICAR × 1 · tubo A36 2\" × 2\" × 1/4\"", "Entra directo en el enganche de 2\" del carro. Hueco Ø 16,5 mm a 60 mm de la punta."),
    ("17b", "17b · Yugo (C) del AHP", "FABRICAR × 1 · A36 12,7 mm", "Une la espiga con los 2 brazos."),
    ("17c", "17c · Brazo largo del AHP", "FABRICAR × 2 · A36 12,7 mm", "Punta redonda con el hueco del pasador 3/8\". 52 mm de luz entre los dos."),
    ("17d", "17d · Placa de anclajes", "FABRICAR × 1 · A36 12,7 mm", "Abajo de los brazos. 4 huecos Ø 25 mm y un hueco en U para la punta de la pata."),
    ("17e", "17e · Alma de la T", "FABRICAR × 1 · A36 12,7 mm", "Parada bajo la espiga, por el centro, hasta los brazos."),
    ("17f", "17f · Argolla inclinada", "FABRICAR × 2 · A36 12,7 mm", "Una afuera de cada brazo, inclinada 35°. Hueco Ø 22 mm."),
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
    ("cabeza_v9.step · tripode_v9.step · accesorios_v9.step", "Conjuntos 3D (STEP)", "La cabeza con la gin pole, el trípode armado, y los accesorios: carretes, AHP y pie con rótula."),
    ("stl/", "Mallas (STL)", "Para imprimir en 3D una maqueta y probar antes de cortar."),
    ("plano/VX-EC_Tripode_v9_planos_RevE.pdf", "Planos (PDF, A3)", "13 hojas: todas las medidas en milímetros, «FABRICAR × N» en cada pieza, kit completo, regla de huecos, AHP, pie con rótula, soldadura y prueba."),
]
archivos = "".join(f'<li><code>{escape(a)}</code><b>{escape(b)}</b><span>{escape(c)}</span></li>' for a, b, c in ARCHIVOS)

PASOS_SOLDAR = [
    dict(t="Placa frontal 01", d="Boca abajo sobre una mesa plana: la cara lisa contra la mesa.", p=["c_01"]),
    dict(t="4 aletas 03", d="Paradas con escuadra a ±33,3 y ±64 mm del centro (cara de adentro). Un eje de Ø 12 mm por los huecos las deja en línea. Puntear.", p=["c_03a", "c_03b", "c_03c", "c_03d"]),
    dict(t="Puente central 04", d=f"Acostado entre las aletas de adentro, subido a {f(ARM['puente_z0'])} mm del borde de abajo, con el hueco C. Atrás queda abierto.", p=["c_04"]),
    dict(t="2 casquillos 02", d="Con un gabarit a 26,5°. El borde de la placa 01 toca el tubo por atrás; adelante queda una V para soldar. Luego TIG alternando lados.", p=["c_02a", "c_02b"]),
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
    dict(t="Espiga cuadrada 17a", d="Tubo de acero 2\" × 2\" × 1/4\": entra directo en el enganche del carro.", p=a("17a")),
    dict(t="Yugo 17b", d="Placa en C soldada en la punta de la espiga.", p=a("17b")),
    dict(t="2 brazos largos 17c", d="Salen del yugo con 52 mm de luz entre ellos.", p=a("17ci", "17cd")),
    dict(t="Alma de la T 17e", d="Parada bajo la espiga, por el centro.", p=a("17e")),
    dict(t="Placa de anclajes 17d", d="Acostada bajo los brazos: con el alma forma la T de abajo. 4 huecos para mosquetón.", p=a("17d")),
    dict(t="2 argollas inclinadas 17f", d="Una afuera de cada brazo, a 35°.", p=a("17fi", "17fd")),
    dict(t="Pata y pasador", d="La pata de adentro entra entre los brazos y el pasador 3/8\" la deja girar.", p=a("17x", "17p")),
]
PASOS_ROTULA = [
    dict(t="Base 18f y suela 18g", d="Base A36 de 10 mm con 4 huecos de anclaje y 2 de mosquetón; caucho de 5 mm abajo.", p=a("18f", "18g")),
    dict(t="Asiento 18d", d="Copa esférica soldada a la base.", p=a("18d")),
    dict(t="Bola de enganche 18c", d="Bola de 2\" que se compra; se aprieta al tapón con su tuerca.", p=a("18c")),
    dict(t="Anillo 18e y 8 tornillos M8", d="El anillo encierra la bola: gira pero no sale.", p=a("18e", "18h")),
    dict(t="Tapón 18b y casquillo 18a", d="El casquillo recibe la pata como el pie de flecha (hueco a 63,5 mm).", p=a("18b", "18a")),
]

DATA = dict(tri=PIEZAS_T, nombres=NOMBRES, soldar=PASOS_SOLDAR, armar=PASOS_ARMAR, carrete=PASOS_CARRETE, ahp=PASOS_AHP, rotula=PASOS_ROTULA)

html = open(os.path.join(AQUI, "v9_web_plantilla.html"), encoding="utf-8").read()
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
