"""Dibujo técnico en SVG (v8): cotas siempre con «mm», cruces de centro sólidas y centradas, texto más grande."""
import re
import math
from html import escape


def mm(t):
    """Agrega « mm» a todo texto de cota que termina en número y no tiene unidad."""
    t = str(t)
    if re.search(r"\d$", t) and "mm" not in t and "°" not in t and "\"" not in t:
        return t + " mm"
    return t


def f(v, dec=1):
    """Número con coma decimal y sin decimales sobrantes."""
    s = f"{v:.{dec}f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s.replace(".", ",")


class Vista:
    """Una vista a escala. Coordenadas del modelo en mm (y hacia arriba)."""

    def __init__(self, x0, y0, x1, y1, ancho_mm, margen=None):
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1
        self.ancho_mm = ancho_mm
        self.k = (x1 - x0) / ancho_mm            # mm de modelo por mm de papel
        self.alto_mm = (y1 - y0) / self.k
        self.el = []
        self.cruces = []
        self.txt = 2.9 * self.k                  # texto de 2,9 mm en papel
        self.lw = 0.25 * self.k

    # -------------------------------------------------------------- básicos
    def P(self, x, y):
        return x, -y

    def linea(self, a, b, cls="obj"):
        (x1, y1), (x2, y2) = self.P(*a), self.P(*b)
        self.el.append(f'<line class="{cls}" x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}"/>')

    def poli(self, pts, cls="pieza", cerrado=True):
        d = " ".join(f"{x:.2f},{-y:.2f}" for x, y in pts)
        tag = "polygon" if cerrado else "polyline"
        self.el.append(f'<{tag} class="{cls}" points="{d}"/>')

    def forma(self, geom, cls="pieza"):
        """Polígono de shapely con agujeros interiores (evenodd)."""
        partes = getattr(geom, "geoms", [geom])
        for g in partes:
            d = "M" + " L".join(f"{x:.2f},{-y:.2f}" for x, y in g.exterior.coords) + "Z"
            for i in g.interiors:
                d += " M" + " L".join(f"{x:.2f},{-y:.2f}" for x, y in i.coords) + "Z"
            self.el.append(f'<path class="{cls}" fill-rule="evenodd" d="{d}"/>')

    def rect(self, x, y, w, h, cls="pieza"):
        self.el.append(f'<rect class="{cls}" x="{x:.2f}" y="{-(y + h):.2f}" width="{w:.2f}" height="{h:.2f}"/>')

    def circulo(self, x, y, r, cls="hueco"):
        self.el.append(f'<circle class="{cls}" cx="{x:.2f}" cy="{-y:.2f}" r="{r:.2f}"/>')

    def texto(self, x, y, t, tam=1.0, anc="middle", cls="t", rot=0):
        X, Y = self.P(x, y)
        tr = f' transform="rotate({rot} {X:.2f} {Y:.2f})"' if rot else ""
        self.el.append(f'<text class="{cls}" x="{X:.2f}" y="{Y:.2f}" font-size="{self.txt * tam:.2f}" '
                       f'text-anchor="{anc}"{tr}>{escape(str(t))}</text>')

    def eje_cruz(self, x, y, r):
        """Cruz de centro: línea continua, simétrica respecto al centro exacto del hueco."""
        e = r * 1.35
        self.linea((x - e, y), (x + e, y), "cruz")
        self.linea((x, y - e), (x, y + e), "cruz")
        self.cruces.append((x, y))

    def etiqueta(self, x, y, t):
        """Burbuja de rótulo para un hueco."""
        self.el.append(f'<text class="etq" x="{x:.2f}" y="{-y + self.txt * 0.35:.2f}" font-size="{self.txt * 0.82:.2f}" '
                       f'text-anchor="middle">{escape(t)}</text>')

    # -------------------------------------------------------------- cotas
    def _flecha(self, x, y, ang):
        L, W = 2.2 * self.k, 0.7 * self.k
        ca, sa = math.cos(ang), math.sin(ang)
        p1 = (x, y)
        p2 = (x - L * ca + W * sa, y - L * sa - W * ca)
        p3 = (x - L * ca - W * sa, y - L * sa + W * ca)
        self.el.append(f'<polygon class="flecha" points="{p1[0]:.2f},{p1[1]:.2f} {p2[0]:.2f},{p2[1]:.2f} {p3[0]:.2f},{p3[1]:.2f}"/>')

    def cota(self, a, b, desp, texto=None, tam=1.0):
        """Cota alineada entre a y b, desplazada 'desp' mm de modelo hacia la izquierda del vector a→b."""
        (ax, ay), (bx, by) = a, b
        L = math.hypot(bx - ax, by - ay)
        if L < 1e-6:
            return
        ux, uy = (bx - ax) / L, (by - ay) / L
        nx, ny = -uy, ux
        a2 = (ax + nx * desp, ay + ny * desp)
        b2 = (bx + nx * desp, by + ny * desp)
        ext = 1.5 * self.k * (1 if desp >= 0 else -1)
        gap = 1.0 * self.k * (1 if desp >= 0 else -1)
        self.linea((ax + nx * gap, ay + ny * gap), (a2[0] + nx * ext, a2[1] + ny * ext), "aux")
        self.linea((bx + nx * gap, by + ny * gap), (b2[0] + nx * ext, b2[1] + ny * ext), "aux")
        self.linea(a2, b2, "cota")
        A, B = self.P(*a2), self.P(*b2)
        ang = math.atan2(B[1] - A[1], B[0] - A[0])
        self._flecha(B[0], B[1], ang)
        self._flecha(A[0], A[1], ang + math.pi)
        t = mm(texto if texto is not None else f(L))
        mx, my = (a2[0] + b2[0]) / 2 + nx * 1.2 * self.k, (a2[1] + b2[1]) / 2 + ny * 1.2 * self.k
        rot = -math.degrees(math.atan2(uy, ux))
        if rot > 90.1:
            rot -= 180
        if rot < -90.1:
            rot += 180
        X, Y = self.P(mx, my)
        self.el.append(f'<text class="ct" x="{X:.2f}" y="{Y:.2f}" font-size="{self.txt * tam:.2f}" text-anchor="middle" '
                       f'transform="rotate({rot:.2f} {X:.2f} {Y:.2f})">{escape(t)}</text>')

    def cota_h(self, x1, x2, y, ynivel, texto=None):
        self._cota_hv(x1, x2, y, ynivel, texto, True)

    def _cota_hv(self, a1, a2, base, nivel, texto, horiz):
        if horiz:
            a, b = (a1, base), (a2, base)
            desp = nivel - base
            self.cota(a, b, desp, texto)
        else:
            a, b = (base, a1), (base, a2)
            desp = -(nivel - base)
            self.cota(a, b, desp, texto)

    def cota_v(self, y1, y2, x, xnivel, texto=None):
        self._cota_hv(y1, y2, x, xnivel, texto, False)

    def diametro(self, x, y, r, ang, texto, largo=None):
        """Cota de diámetro con línea de referencia."""
        largo = largo or 12 * self.k
        ca, sa = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        p1 = (x + r * ca, y + r * sa)
        p2 = (x + (r + largo) * ca, y + (r + largo) * sa)
        self.linea(p1, p2, "cota")
        A, B = self.P(*p1), self.P(*p2)
        self._flecha(A[0], A[1], math.atan2(A[1] - B[1], A[0] - B[0]))
        derecha = ca >= 0
        p3 = (p2[0] + (8 if derecha else -8) * self.k, p2[1])
        self.linea(p2, p3, "cota")
        self.texto(p3[0] + (1 if derecha else -1) * self.k, p3[1] + 0.6 * self.k, mm(texto), anc="start" if derecha else "end", cls="ct")

    def nota(self, x, y, xt, yt, texto):
        self.linea((x, y), (xt, yt), "cota")
        A, B = self.P(x, y), self.P(xt, yt)
        self._flecha(A[0], A[1], math.atan2(A[1] - B[1], A[0] - B[0]))
        derecha = xt >= x
        self.linea((xt, yt), (xt + (6 if derecha else -6) * self.k, yt), "cota")
        self.texto(xt + (7 if derecha else -7) * self.k, yt + 0.6 * self.k, texto, anc="start" if derecha else "end", cls="ct")

    # -------------------------------------------------------------- salida
    def svg(self, titulo="", escala_txt=""):
        vb = f"{self.x0:.2f} {-self.y1:.2f} {self.x1 - self.x0:.2f} {self.y1 - self.y0:.2f}"
        k = self.k
        estilo = (f"<style>.pieza{{stroke-width:{0.35 * k:.3f}}}.obj{{stroke-width:{0.35 * k:.3f}}}"
                  f".hueco{{stroke-width:{0.3 * k:.3f}}}.oculta{{stroke-width:{0.22 * k:.3f};stroke-dasharray:{2 * k:.2f} {1 * k:.2f}}}"
                  f".eje{{stroke-width:{0.18 * k:.3f};stroke-dasharray:{6 * k:.2f} {1.2 * k:.2f} {1 * k:.2f} {1.2 * k:.2f}}}"
                  f".cruz{{stroke-width:{0.22 * k:.3f};stroke:#d9571a;fill:none}}"
                  f".aux,.cota{{stroke-width:{0.15 * k:.3f}}}.fantasma{{stroke-width:{0.22 * k:.3f};stroke-dasharray:{3 * k:.2f} {1.5 * k:.2f}}}</style>")
        cab = ""
        if titulo:
            cab = (f'<div class="vista-tit"><span>{escape(titulo)}</span><em>{escape(escala_txt)}</em></div>')
        return (f'<figure class="vista" style="width:{self.ancho_mm:.1f}mm">{cab}'
                f'<svg viewBox="{vb}" style="width:{self.ancho_mm:.1f}mm;height:{self.alto_mm:.1f}mm">{estilo}'
                + "".join(self.el) + "</svg></figure>")
