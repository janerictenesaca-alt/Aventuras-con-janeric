/* Ganjan - corrección de color por píxel: luz, color, HSL, curvas, ruedas, LUT .cube, nitidez y croma */
(function () {
  const clamp = (v, a = 0, b = 1) => v < a ? a : v > b ? b : v;
  const lerp = (a, b, k) => a + (b - a) * k;
  const ADJ_KEYS = ['temp', 'tint', 'sat', 'exposure', 'contrast', 'hl', 'shadow', 'white', 'black', 'lum', 'fade'];
  const HSL_COLORS = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple', 'magenta'];
  const HUES = [0, 30, 60, 120, 180, 240, 280, 320];
  GC.HSL_COLORS = HSL_COLORS;

  /* curva monótona cúbica -> tabla de 256 valores */
  const cache = new Map();
  function curveLUT(pts) {
    const key = JSON.stringify(pts); if (cache.has(key)) return cache.get(key);
    const p = pts.slice().sort((a, b) => a[0] - b[0]), n = p.length, L = new Float32Array(256);
    if (n < 2) { for (let i = 0; i < 256; i++) L[i] = i / 255; return L; }
    const dx = [], d = [], m = [];
    for (let i = 0; i < n - 1; i++) { dx[i] = (p[i + 1][0] - p[i][0]) || 1e-6; d[i] = (p[i + 1][1] - p[i][1]) / dx[i]; }
    m[0] = d[0]; m[n - 1] = d[n - 2];
    for (let i = 1; i < n - 1; i++) m[i] = d[i - 1] * d[i] <= 0 ? 0 : (d[i - 1] + d[i]) / 2;
    for (let i = 0; i < n - 1; i++) { if (d[i] === 0) { m[i] = m[i + 1] = 0; } else { const a = m[i] / d[i], b = m[i + 1] / d[i], s = a * a + b * b; if (s > 9) { const t = 3 / Math.sqrt(s); m[i] = t * a * d[i]; m[i + 1] = t * b * d[i]; } } }
    for (let k = 0; k < 256; k++) {
      const x = k / 255; let y, j = 0; while (j < n - 2 && x > p[j + 1][0]) j++;
      if (x <= p[0][0]) y = p[0][1]; else if (x >= p[n - 1][0]) y = p[n - 1][1];
      else { const h = dx[j], t = (x - p[j][0]) / h, t2 = t * t, t3 = t2 * t; y = (2 * t3 - 3 * t2 + 1) * p[j][1] + (t3 - 2 * t2 + t) * h * m[j] + (-2 * t3 + 3 * t2) * p[j + 1][1] + (t3 - t2) * h * m[j + 1]; }
      L[k] = clamp(y);
    }
    if (cache.size > 40) cache.clear(); cache.set(key, L); return L;
  }
  GC.curveLUT = curveLUT;
  const isIdentity = pts => !pts || pts.length < 2 || pts.every(([x, y]) => Math.abs(x - y) < 1e-4);
  const curvesActive = c => c && ['luma', 'r', 'g', 'b'].some(k => !isIdentity(c[k]));
  const hslActive = h => h && Object.values(h).some(v => v && (v.h || v.s || v.l));
  const wheelsActive = w => w && Object.values(w).some(v => v && (v[0] || v[1] || v[2]));

  GC.needsGrade = clip => {
    const a = clip.adj || {};
    return ADJ_KEYS.some(k => a[k]) || !!a.sharpen || !!a.clarity || hslActive(clip.hsl) || curvesActive(clip.curves) || wheelsActive(clip.wheels) || !!(clip.lut && clip.lut.name && GC.LUTS && GC.LUTS.get(clip.lut.name)) || !!(clip.chroma && clip.chroma.on);
  };

  /* ---------- LUT .cube ---------- */
  GC.LUTS = new Map();
  GC.parseCube = (text, name) => {
    let n = 0; const vals = [];
    for (const line of text.split(/\r?\n/)) {
      const t = line.trim(); if (!t || t[0] === '#') continue;
      if (t.startsWith('LUT_3D_SIZE')) { n = parseInt(t.split(/\s+/)[1]); continue; }
      if (/^[A-Z_]+/.test(t) && !/^[-\d.]/.test(t)) continue;
      const p = t.split(/\s+/).map(Number); if (p.length === 3 && p.every(isFinite)) vals.push(p[0], p[1], p[2]);
    }
    if (!n || vals.length !== n * n * n * 3) throw new Error('LUT .cube no válida (solo 3D)');
    const lut = { n, data: Float32Array.from(vals), name }; GC.LUTS.set(name, lut); return lut;
  };
  function lutSample(lut, r, g, b, out) {
    const N = lut.n, s = N - 1, D = lut.data, x = r * s, y = g * s, z = b * s;
    const x0 = x | 0, y0 = y | 0, z0 = z | 0, x1 = Math.min(x0 + 1, s), y1 = Math.min(y0 + 1, s), z1 = Math.min(z0 + 1, s), fx = x - x0, fy = y - y0, fz = z - z0;
    const idx = (a, b2, c) => ((c * N + b2) * N + a) * 3;
    for (let k = 0; k < 3; k++) {
      const c000 = D[idx(x0, y0, z0) + k], c100 = D[idx(x1, y0, z0) + k], c010 = D[idx(x0, y1, z0) + k], c110 = D[idx(x1, y1, z0) + k];
      const c001 = D[idx(x0, y0, z1) + k], c101 = D[idx(x1, y0, z1) + k], c011 = D[idx(x0, y1, z1) + k], c111 = D[idx(x1, y1, z1) + k];
      const c00 = c000 + (c100 - c000) * fx, c10 = c010 + (c110 - c010) * fx, c01 = c001 + (c101 - c001) * fx, c11 = c011 + (c111 - c011) * fx;
      const c0 = c00 + (c10 - c00) * fy, c1 = c01 + (c11 - c01) * fy; out[k] = c0 + (c1 - c0) * fz;
    }
  }

  function unsharp(c, amount, radius) {
    const W = c.canvas.width, H = c.canvas.height, s = GC.scratch('us', W, H), sc = s.getContext('2d', { willReadFrequently: true });
    sc.setTransform(1, 0, 0, 1, 0, 0); sc.clearRect(0, 0, W, H); sc.filter = `blur(${radius}px)`; sc.drawImage(c.canvas, 0, 0); sc.filter = 'none';
    const bl = sc.getImageData(0, 0, W, H).data, id = c.getImageData(0, 0, W, H), d = id.data;
    for (let i = 0; i < d.length; i += 4) { if (!d[i + 3]) continue; d[i] += (d[i] - bl[i]) * amount; d[i + 1] += (d[i + 1] - bl[i + 1]) * amount; d[i + 2] += (d[i + 2] - bl[i + 2]) * amount; }
    c.putImageData(id, 0, 0);
  }

  GC.grade = (c, clip, S) => {
    const W = c.canvas.width, H = c.canvas.height, a = clip.adj || {};
    const gs = GC.scratch('gr', W, H), g2 = gs._c || (gs._c = gs.getContext('2d', { willReadFrequently: true }));
    g2.setTransform(1, 0, 0, 1, 0, 0); g2.globalCompositeOperation = 'source-over'; g2.globalAlpha = 1; g2.filter = 'none'; g2.clearRect(0, 0, W, H); g2.drawImage(c.canvas, 0, 0);
    const id = g2.getImageData(0, 0, W, H), d = id.data, N = d.length;
    const ch = clip.chroma && clip.chroma.on ? clip.chroma : null;
    // ----- tablas de tono -----
    const ex = Math.pow(2, (a.exposure || 0) / 100 * 1.5), ct = 1 + (a.contrast || 0) / 100, bl = (a.black || 0) / 100 * .15, wh = 1 + (a.white || 0) / 100 * .2;
    const sh = (a.shadow || 0) / 100 * .25, hl = (a.hl || 0) / 100 * .25, lm = (a.lum || 0) / 100 * .2, fd = (a.fade || 0) / 100;
    const tone = v => {
      v *= ex; v = (v - .5) * ct + .5; v = v * (1 - bl) + bl; v *= wh;
      v += sh * Math.pow(1 - clamp(v), 2) + hl * Math.pow(clamp(v), 2); v += lm; v = v * (1 - fd * .4) + fd * .4 * .5;
      return clamp(v);
    };
    const tp = (a.temp || 0) / 100, ti = (a.tint || 0) / 100, gR = 1 + tp * .25 + ti * .08, gG = 1 - ti * .18, gB = 1 - tp * .25 + ti * .08;
    const cv = clip.curves, LL = cv && !isIdentity(cv.luma) ? curveLUT(cv.luma) : null, RL = cv && !isIdentity(cv.r) ? curveLUT(cv.r) : null, GL = cv && !isIdentity(cv.g) ? curveLUT(cv.g) : null, BL = cv && !isIdentity(cv.b) ? curveLUT(cv.b) : null;
    const lutR = new Uint8ClampedArray(256), lutG = new Uint8ClampedArray(256), lutB = new Uint8ClampedArray(256);
    for (let i = 0; i < 256; i++) {
      let v = tone(i / 255); if (LL) v = LL[Math.round(v * 255)];
      const r = clamp(v * gR), g = clamp(v * gG), b = clamp(v * gB);
      lutR[i] = (RL ? RL[Math.round(r * 255)] : r) * 255; lutG[i] = (GL ? GL[Math.round(g * 255)] : g) * 255; lutB[i] = (BL ? BL[Math.round(b * 255)] : b) * 255;
    }
    const sat = 1 + (a.sat || 0) / 100, doSat = !!a.sat;
    const hs = hslActive(clip.hsl) ? HSL_COLORS.map(k => (clip.hsl[k] || { h: 0, s: 0, l: 0 })) : null;
    const wh3 = wheelsActive(clip.wheels) ? clip.wheels : null, wI = ((clip.wheelInt ?? 100) / 100) * .3;
    const lut = clip.lut && clip.lut.name ? GC.LUTS.get(clip.lut.name) : null, lk = lut ? (clip.lut.k ?? 1) : 0, tmp = [0, 0, 0];
    const needPix = doSat || hs || wh3 || lut;
    let kr = 0, kcb = 0, tol = 0, soft = 0;
    if (ch) { const m = /^#?([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})$/i.exec(ch.color || '#00ff00'), R = parseInt(m[1], 16), G2 = parseInt(m[2], 16), B = parseInt(m[3], 16); kcb = -.169 * R - .331 * G2 + .5 * B; kr = .5 * R - .419 * G2 - .081 * B; tol = (ch.tol ?? .35) * .6; soft = (ch.soft ?? .15) * .4 + .01; }
    for (let i = 0; i < N; i += 4) {
      const al = d[i + 3]; if (!al) continue;
      let R0 = d[i], G0 = d[i + 1], B0 = d[i + 2];
      if (ch) {
        const cb = -.169 * R0 - .331 * G0 + .5 * B0, cr = .5 * R0 - .419 * G0 - .081 * B0, dist = Math.hypot(cb - kcb, cr - kr) / 181;
        const f = clamp((dist - tol) / soft); if (f < 1) { d[i + 3] = al * f * f * (3 - 2 * f); if (f < .02) { d[i + 3] = 0; continue; } }
      }
      let r = lutR[R0], g = lutG[G0], b = lutB[B0];
      if (needPix) {
        let rf = r / 255, gf = g / 255, bf = b / 255;
        if (doSat) { const gy = .299 * rf + .587 * gf + .114 * bf; rf = gy + (rf - gy) * sat; gf = gy + (gf - gy) * sat; bf = gy + (bf - gy) * sat; }
        if (hs) {
          const mx = Math.max(rf, gf, bf), mn = Math.min(rf, gf, bf), dl = mx - mn;
          if (dl > 1e-4) {
            let hh; if (mx === rf) hh = ((gf - bf) / dl) % 6; else if (mx === gf) hh = (bf - rf) / dl + 2; else hh = (rf - gf) / dl + 4; hh *= 60; if (hh < 0) hh += 360;
            let sv = dl / mx, vv = mx, dh = 0, ds = 0, dv = 0; const sw = Math.min(1, sv * 3);
            for (let k = 0; k < 8; k++) { let dd = Math.abs(hh - HUES[k]); if (dd > 180) dd = 360 - dd; const w = Math.max(0, 1 - dd / 45) * sw; if (w) { dh += w * hs[k].h * .3; ds += w * hs[k].s / 100; dv += w * hs[k].l / 100 * .4; } }
            if (dh || ds || dv) {
              hh = (hh + dh + 360) % 360; sv = clamp(sv * (1 + ds)); vv = clamp(vv + dv * vv + dv * .1);
              const cc = vv * sv, x = cc * (1 - Math.abs((hh / 60) % 2 - 1)), m2 = vv - cc; let r1, g1, b1;
              if (hh < 60) { r1 = cc; g1 = x; b1 = 0; } else if (hh < 120) { r1 = x; g1 = cc; b1 = 0; } else if (hh < 180) { r1 = 0; g1 = cc; b1 = x; } else if (hh < 240) { r1 = 0; g1 = x; b1 = cc; } else if (hh < 300) { r1 = x; g1 = 0; b1 = cc; } else { r1 = cc; g1 = 0; b1 = x; }
              rf = r1 + m2; gf = g1 + m2; bf = b1 + m2;
            }
          }
        }
        if (wh3) {
          const lu = .299 * rf + .587 * gf + .114 * bf, wS = (1 - lu) * (1 - lu), wH = lu * lu, wM = Math.max(0, 1 - wS - wH), S3 = wh3.shadows || [0, 0, 0], M3 = wh3.mid || [0, 0, 0], H3 = wh3.high || [0, 0, 0], O3 = wh3.offset || [0, 0, 0];
          rf += (S3[0] * wS + M3[0] * wM + H3[0] * wH + O3[0]) * wI; gf += (S3[1] * wS + M3[1] * wM + H3[1] * wH + O3[1]) * wI; bf += (S3[2] * wS + M3[2] * wM + H3[2] * wH + O3[2]) * wI;
        }
        if (lut) { lutSample(lut, clamp(rf), clamp(gf), clamp(bf), tmp); rf = lerp(rf, tmp[0], lk); gf = lerp(gf, tmp[1], lk); bf = lerp(bf, tmp[2], lk); }
        r = clamp(rf) * 255; g = clamp(gf) * 255; b = clamp(bf) * 255;
      }
      d[i] = r; d[i + 1] = g; d[i + 2] = b;
    }
    g2.putImageData(id, 0, 0);
    if (a.sharpen) unsharp(g2, a.sharpen / 100 * 1.2, Math.max(.6, 1 * S));
    if (a.clarity) unsharp(g2, a.clarity / 100 * .8, Math.max(4, 12 * S));
    c.save(); c.setTransform(1, 0, 0, 1, 0, 0); c.globalCompositeOperation = 'copy'; c.globalAlpha = 1; c.filter = 'none'; c.drawImage(gs, 0, 0); c.restore();
  };
})();
