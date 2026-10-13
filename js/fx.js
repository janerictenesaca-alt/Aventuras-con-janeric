/* Ganchan - efectos, transiciones, animaciones y utilidades de dibujo (propios) */
(function () {
  const pool = {};
  GC.scratch = (name, w, h) => {
    let c = pool[name];
    if (!c) { c = pool[name] = document.createElement('canvas'); }
    if (c.width !== w || c.height !== h) { c.width = w; c.height = h; }
    return c;
  };
  GC.snap = (c, name = 'snap') => {
    const s = GC.scratch(name, c.canvas.width, c.canvas.height);
    const sc = s.getContext('2d');
    sc.setTransform(1, 0, 0, 1, 0, 0);
    sc.globalCompositeOperation = 'source-over'; sc.globalAlpha = 1; sc.filter = 'none';
    sc.clearRect(0, 0, s.width, s.height);
    sc.drawImage(c.canvas, 0, 0);
    return s;
  };
  const rnd = n => { const x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
  GC.rnd = rnd;
  const lerp = (a, b, k) => a + (b - a) * k;
  GC.lerp = lerp;
  const clear = c => { c.save(); c.setTransform(1, 0, 0, 1, 0, 0); c.clearRect(0, 0, c.canvas.width, c.canvas.height); c.restore(); };

  /* ---------- Filtros ---------- */
  GC.filterStr = (def, k, adj, S) => {
    let b = 1, c = 1, s = 1, sep = 0, hue = 0, gray = 0, blur = 0;
    if (def && def.id !== 'none') {
      b = lerp(1, def.b ?? 1, k); c = lerp(1, def.c ?? 1, k); s = lerp(1, def.s ?? 1, k);
      sep = (def.sep || 0) * k; hue = (def.hue || 0) * k; gray = (def.gray || 0) * k;
    }
    adj = adj || {};
    b *= 1 + (adj.brightness || 0) / 100; c *= 1 + (adj.contrast || 0) / 100; s *= 1 + (adj.saturation || 0) / 100;
    hue += (adj.hue || 0) * 1.8; blur += (adj.blur || 0) / 100 * 20 * S;
    const parts = [];
    if (b !== 1) parts.push(`brightness(${b.toFixed(3)})`);
    if (c !== 1) parts.push(`contrast(${c.toFixed(3)})`);
    if (s !== 1) parts.push(`saturate(${Math.max(0, s).toFixed(3)})`);
    if (sep) parts.push(`sepia(${sep.toFixed(3)})`);
    if (gray) parts.push(`grayscale(${gray.toFixed(3)})`);
    if (hue) parts.push(`hue-rotate(${hue.toFixed(1)}deg)`);
    if (blur > .1) parts.push(`blur(${blur.toFixed(1)}px)`);
    return parts.length ? parts.join(' ') : 'none';
  };
  GC.tintsOf = (def, k, adj) => {
    const out = [];
    if (def && def.tint) def.tint.forEach(t => out.push([t[0], t[1], t[2], t[3] * k, t[4]]));
    adj = adj || {};
    if (adj.temp) out.push(adj.temp > 0 ? [255, 150, 40, adj.temp / 100 * .35, 'soft-light'] : [40, 140, 255, -adj.temp / 100 * .35, 'soft-light']);
    if (adj.fade) out.push([210, 210, 210, adj.fade / 100 * .5, 'lighten']);
    return out;
  };
  GC.tintLayer = (c, r, g, b, a, mode) => {
    const s = GC.snap(c, 'tint');
    c.save(); c.setTransform(1, 0, 0, 1, 0, 0);
    c.globalCompositeOperation = mode; c.globalAlpha = Math.min(1, a);
    c.fillStyle = `rgb(${r},${g},${b})`; c.fillRect(0, 0, c.canvas.width, c.canvas.height);
    c.globalAlpha = 1; c.globalCompositeOperation = 'destination-in'; c.drawImage(s, 0, 0);
    c.restore();
  };

  /* ---------- Efectos de video ---------- */
  let noiseCv = null;
  const getNoise = () => {
    if (noiseCv) return noiseCv;
    noiseCv = document.createElement('canvas'); noiseCv.width = noiseCv.height = 256;
    const x = noiseCv.getContext('2d'), d = x.createImageData(256, 256);
    for (let i = 0; i < d.data.length; i += 4) { const v = Math.random() * 255; d.data[i] = d.data[i + 1] = d.data[i + 2] = v; d.data[i + 3] = Math.random() * 200; }
    x.putImageData(d, 0, 0); return noiseCv;
  };
  const overlay = (c, fn) => { c.save(); c.setTransform(1, 0, 0, 1, 0, 0); c.globalCompositeOperation = 'source-atop'; fn(c, c.canvas.width, c.canvas.height); c.restore(); };
  const vignette = (c, k) => overlay(c, (c, W, H) => {
    const g = c.createRadialGradient(W / 2, H / 2, Math.min(W, H) * .25, W / 2, H / 2, Math.hypot(W, H) * .55);
    g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(1, `rgba(0,0,0,${.9 * k})`);
    c.fillStyle = g; c.fillRect(0, 0, W, H);
  });
  const grain = (c, k, t) => overlay(c, (c, W, H) => {
    const p = c.createPattern(getNoise(), 'repeat'); c.globalAlpha = .35 * k;
    c.translate(Math.floor(rnd(Math.floor(t * 24)) * 256), Math.floor(rnd(Math.floor(t * 24) + 5) * 256));
    c.fillStyle = p; c.fillRect(-256, -256, W + 512, H + 512);
  });
  GC.vignette = vignette; GC.grain = grain;
  const rgbsplit = (c, W, H, t, k) => {
    const s = GC.snap(c, 'snap'), ch = GC.scratch('ch', W, H), cc = ch.getContext('2d');
    const d = W * .008 * k * (1 + Math.sin(t * 8) * .3);
    c.save(); c.setTransform(1, 0, 0, 1, 0, 0); c.clearRect(0, 0, W, H); c.globalCompositeOperation = 'lighter';
    [['#f00', -d], ['#0f0', 0], ['#00f', d]].forEach(([col, off]) => {
      cc.globalCompositeOperation = 'source-over'; cc.clearRect(0, 0, W, H); cc.drawImage(s, 0, 0);
      cc.globalCompositeOperation = 'multiply'; cc.fillStyle = col; cc.fillRect(0, 0, W, H);
      cc.globalCompositeOperation = 'destination-in'; cc.drawImage(s, 0, 0);
      c.drawImage(ch, off, 0);
    });
    c.restore();
  };

  GC.FX_CATS = ['Básicos', 'Estilizar', 'Distorsión', 'Desenfoque', 'Color', 'Luz'];
  GC.FX = [
    { id: 'blur', name: 'Desenfoque', cat: 'Desenfoque', icon: '🌫️', post(c, W, H, t, k) { const s = GC.snap(c); c.save(); c.setTransform(1, 0, 0, 1, 0, 0); c.clearRect(0, 0, W, H); c.filter = `blur(${(k * 16 * H / 1080).toFixed(1)}px)`; c.drawImage(s, 0, 0); c.restore(); } },
    { id: 'glow', name: 'Resplandor', cat: 'Luz', icon: '✨', post(c, W, H, t, k) { const s = GC.snap(c); c.save(); c.setTransform(1, 0, 0, 1, 0, 0); c.globalCompositeOperation = 'lighter'; c.filter = `blur(${(14 * H / 1080).toFixed(1)}px)`; c.globalAlpha = .7 * k; c.drawImage(s, 0, 0); c.restore(); } },
    { id: 'vignette', name: 'Viñeta', cat: 'Básicos', icon: '⚫', post(c, W, H, t, k) { vignette(c, k); } },
    { id: 'grain', name: 'Grano de película', cat: 'Básicos', icon: '🎞️', post(c, W, H, t, k) { grain(c, k, t); } },
    { id: 'cinebars', name: 'Barras de cine', cat: 'Básicos', icon: '🎬', post(c, W, H) { c.save(); c.setTransform(1, 0, 0, 1, 0, 0); c.fillStyle = '#000'; c.fillRect(0, 0, W, H * .12); c.fillRect(0, H * .88, W, H * .12); c.restore(); } },
    { id: 'flicker', name: 'Parpadeo', cat: 'Básicos', icon: '💡', post(c, W, H, t, k) { overlay(c, (c, W, H) => { c.fillStyle = `rgba(0,0,0,${rnd(Math.floor(t * 24)) * .55 * k})`; c.fillRect(0, 0, W, H); }); } },
    { id: 'flash', name: 'Destello', cat: 'Luz', icon: '⚡', post(c, W, H, t, k) { overlay(c, (c, W, H) => { c.fillStyle = `rgba(255,255,255,${Math.pow(Math.max(0, Math.sin(t * 6)), 6) * k * .9})`; c.fillRect(0, 0, W, H); }); } },
    { id: 'leak', name: 'Fuga de luz', cat: 'Luz', icon: '🌅', post(c, W, H, t, k) { overlay(c, (c, W, H) => { const x = ((t * .25) % 1.6 - .3) * W; const g = c.createLinearGradient(x - W * .4, 0, x + W * .4, H); g.addColorStop(0, 'rgba(255,120,40,0)'); g.addColorStop(.5, `rgba(255,170,70,${.5 * k})`); g.addColorStop(1, 'rgba(255,60,120,0)'); c.fillStyle = g; c.fillRect(0, 0, W, H); }); } },
    { id: 'glitch', name: 'Glitch', cat: 'Distorsión', icon: '📺', post(c, W, H, t, k) {
      const seed = Math.floor(t * 10); if (rnd(seed * 13) < .35) return;
      const s = GC.snap(c); const n = 3 + Math.floor(k * 6);
      c.save(); c.setTransform(1, 0, 0, 1, 0, 0);
      for (let i = 0; i < n; i++) { const y = rnd(seed + i) * H, h = rnd(seed + i * 7) * H * .08 + H * .01, dx = (rnd(seed + i * 3) - .5) * W * .15 * k; c.clearRect(0, y, W, h); c.drawImage(s, 0, y, W, h, dx, y, W, h); }
      c.restore(); rgbsplit(c, W, H, t, k * .6);
    } },
    { id: 'rgb', name: 'Separar RGB', cat: 'Distorsión', icon: '🌈', post(c, W, H, t, k) { rgbsplit(c, W, H, t, k); } },
    { id: 'vhs', name: 'VHS', cat: 'Estilizar', icon: '📼', post(c, W, H, t, k) {
      rgbsplit(c, W, H, t, k * .5);
      overlay(c, (c, W, H) => { c.fillStyle = `rgba(0,0,0,${.28 * k})`; const st = Math.max(3, Math.round(4 * H / 1080)); for (let y = 0; y < H; y += st * 2) c.fillRect(0, y, W, st); });
      grain(c, k * .6, t);
    } },
    { id: 'wave', name: 'Ondas', cat: 'Distorsión', icon: '🌊', post(c, W, H, t, k) {
      const s = GC.snap(c), st = Math.max(4, Math.round(6 * H / 1080));
      c.save(); c.setTransform(1, 0, 0, 1, 0, 0); c.clearRect(0, 0, W, H);
      for (let y = 0; y < H; y += st) c.drawImage(s, 0, y, W, st, Math.sin(y / H * 20 + t * 6) * W * .012 * k, y, W, st);
      c.restore();
    } },
    { id: 'pixel', name: 'Pixelar', cat: 'Estilizar', icon: '🟦', post(c, W, H, t, k) {
      const sz = Math.max(3, Math.round((6 + k * 40) * H / 1080)), s = GC.scratch('px', Math.ceil(W / sz), Math.ceil(H / sz)), sc = s.getContext('2d');
      sc.clearRect(0, 0, s.width, s.height); sc.drawImage(c.canvas, 0, 0, s.width, s.height);
      c.save(); c.setTransform(1, 0, 0, 1, 0, 0); c.clearRect(0, 0, W, H); c.imageSmoothingEnabled = false; c.drawImage(s, 0, 0, s.width * sz, s.height * sz); c.restore();
    } },
    { id: 'mirror', name: 'Espejo', cat: 'Distorsión', icon: '🪞', post(c, W, H) {
      const s = GC.snap(c); c.save(); c.setTransform(1, 0, 0, 1, 0, 0); c.clearRect(0, 0, W, H);
      c.drawImage(s, 0, 0, W / 2, H, 0, 0, W / 2, H); c.translate(W, 0); c.scale(-1, 1); c.drawImage(s, 0, 0, W / 2, H, 0, 0, W / 2, H); c.restore();
    } },
    { id: 'kaleido', name: 'Caleidoscopio', cat: 'Distorsión', icon: '🔮', post(c, W, H) {
      const s = GC.snap(c); c.save(); c.setTransform(1, 0, 0, 1, 0, 0); c.clearRect(0, 0, W, H);
      [[1, 1], [-1, 1], [1, -1], [-1, -1]].forEach(([sx, sy]) => { c.save(); c.translate(sx < 0 ? W : 0, sy < 0 ? H : 0); c.scale(sx, sy); c.drawImage(s, 0, 0, W / 2, H / 2, 0, 0, W / 2, H / 2); c.restore(); });
      c.restore();
    } },
    { id: 'invert', name: 'Invertir', cat: 'Color', icon: '🔄', post(c, W, H, t, k) { const s = GC.snap(c); c.save(); c.setTransform(1, 0, 0, 1, 0, 0); c.clearRect(0, 0, W, H); c.filter = `invert(${k})`; c.drawImage(s, 0, 0); c.restore(); } },
    { id: 'shake', name: 'Temblor', cat: 'Distorsión', icon: '📳', xf(t, k) { const n = Math.floor(t * 30); return { dx: (rnd(n) - .5) * .02 * k, dy: (rnd(n + 99) - .5) * .02 * k, sc: 1 + .03 * k }; } },
    { id: 'pulse', name: 'Latido', cat: 'Estilizar', icon: '💓', xf(t, k) { return { sc: 1 + .12 * k * Math.pow(Math.max(0, Math.sin(t * Math.PI * 3)), 3) }; } },
  ];
  GC.FXBYID = Object.fromEntries(GC.FX.map(f => [f.id, f]));

  /* ---------- Transiciones ---------- */
  const dA = (c, A, a = 1) => { if (A) { c.globalAlpha = a; c.drawImage(A, 0, 0); c.globalAlpha = 1; } };
  const clipRect = (c, B, x, y, w, h) => { c.save(); c.beginPath(); c.rect(x, y, w, h); c.clip(); c.drawImage(B, 0, 0); c.restore(); };
  const around = (c, W, H, fn) => { c.save(); c.translate(W / 2, H / 2); fn(); c.translate(-W / 2, -H / 2); };
  const glitchSlices = (c, S, W, H, k, seed) => { c.drawImage(S, 0, 0); for (let i = 0; i < 8; i++) { const y = rnd(seed + i) * H, h = rnd(seed + i * 7) * H * .1 + 4; c.clearRect(0, y, W, h); c.drawImage(S, 0, y, W, h, (rnd(seed + i * 3) - .5) * W * .25 * k, y, W, h); } };
  const slide = (dx, dy) => (c, p, A, B, W, H) => { dA(c, A); c.drawImage(B, dx * (1 - p) * W, dy * (1 - p) * H); };
  const push = (dx, dy) => (c, p, A, B, W, H) => { if (A) c.drawImage(A, -dx * p * W, -dy * p * H); c.drawImage(B, dx * (1 - p) * W, dy * (1 - p) * H); };
  const wipe = d => (c, p, A, B, W, H) => { dA(c, A); if (d === 'l') clipRect(c, B, 0, 0, W * p, H); if (d === 'r') clipRect(c, B, W * (1 - p), 0, W * p, H); if (d === 'u') clipRect(c, B, 0, 0, W, H * p); if (d === 'd') clipRect(c, B, 0, H * (1 - p), W, H * p); };
  GC.TRANS_CATS = ['Básicas', 'Deslizar', 'Cámara', 'Efectos'];
  GC.TRANS = [
    { id: 'dissolve', name: 'Disolver', cat: 'Básicas', icon: '◐', draw(c, p, A, B) { dA(c, A); c.globalAlpha = p; c.drawImage(B, 0, 0); c.globalAlpha = 1; } },
    { id: 'fadeblack', name: 'Fundido a negro', cat: 'Básicas', icon: '⬛', draw(c, p, A, B, W, H) { if (p < .5) { dA(c, A); c.fillStyle = `rgba(0,0,0,${p * 2})`; } else { c.drawImage(B, 0, 0); c.fillStyle = `rgba(0,0,0,${(1 - p) * 2})`; } c.fillRect(0, 0, W, H); } },
    { id: 'fadewhite', name: 'Fundido a blanco', cat: 'Básicas', icon: '⬜', draw(c, p, A, B, W, H) { if (p < .5) { dA(c, A); c.fillStyle = `rgba(255,255,255,${p * 2})`; } else { c.drawImage(B, 0, 0); c.fillStyle = `rgba(255,255,255,${(1 - p) * 2})`; } c.fillRect(0, 0, W, H); } },
    { id: 'slidel', name: 'Cubrir ←', cat: 'Deslizar', icon: '⬅', draw: slide(1, 0) },
    { id: 'slider', name: 'Cubrir →', cat: 'Deslizar', icon: '➡', draw: slide(-1, 0) },
    { id: 'slideu', name: 'Cubrir ↑', cat: 'Deslizar', icon: '⬆', draw: slide(0, 1) },
    { id: 'slided', name: 'Cubrir ↓', cat: 'Deslizar', icon: '⬇', draw: slide(0, -1) },
    { id: 'pushl', name: 'Empujar ←', cat: 'Deslizar', icon: '⏪', draw: push(1, 0) },
    { id: 'pushr', name: 'Empujar →', cat: 'Deslizar', icon: '⏩', draw: push(-1, 0) },
    { id: 'wipel', name: 'Cortina →', cat: 'Básicas', icon: '▶', draw: wipe('l') },
    { id: 'wiper', name: 'Cortina ←', cat: 'Básicas', icon: '◀', draw: wipe('r') },
    { id: 'wipeu', name: 'Cortina ↓', cat: 'Básicas', icon: '🔽', draw: wipe('u') },
    { id: 'wiped', name: 'Cortina ↑', cat: 'Básicas', icon: '🔼', draw: wipe('d') },
    { id: 'circle', name: 'Círculo', cat: 'Efectos', icon: '⭕', draw(c, p, A, B, W, H) { dA(c, A); c.save(); c.beginPath(); c.arc(W / 2, H / 2, p * Math.hypot(W, H) / 2, 0, 7); c.clip(); c.drawImage(B, 0, 0); c.restore(); } },
    { id: 'circleclose', name: 'Iris', cat: 'Efectos', icon: '🔘', draw(c, p, A, B, W, H) { c.drawImage(B, 0, 0); if (A) { c.save(); c.beginPath(); c.arc(W / 2, H / 2, (1 - p) * Math.hypot(W, H) / 2, 0, 7); c.clip(); c.drawImage(A, 0, 0); c.restore(); } } },
    { id: 'clock', name: 'Reloj', cat: 'Efectos', icon: '🕐', draw(c, p, A, B, W, H) { dA(c, A); c.save(); c.beginPath(); c.moveTo(W / 2, H / 2); c.arc(W / 2, H / 2, Math.hypot(W, H), -Math.PI / 2, -Math.PI / 2 + p * Math.PI * 2); c.closePath(); c.clip(); c.drawImage(B, 0, 0); c.restore(); } },
    { id: 'blinds', name: 'Persianas', cat: 'Efectos', icon: '☰', draw(c, p, A, B, W, H) { dA(c, A); c.save(); c.beginPath(); const n = 8, w = W / n; for (let i = 0; i < n; i++) c.rect(i * w, 0, w * p, H); c.clip(); c.drawImage(B, 0, 0); c.restore(); } },
    { id: 'mosaic', name: 'Mosaico', cat: 'Efectos', icon: '▦', draw(c, p, A, B, W, H) { dA(c, A); c.save(); c.beginPath(); const nx = 16, ny = 9; for (let i = 0; i < nx; i++) for (let j = 0; j < ny; j++) if (rnd(i * 31 + j * 7) < p) c.rect(i * W / nx, j * H / ny, W / nx + 1, H / ny + 1); c.clip(); c.drawImage(B, 0, 0); c.restore(); } },
    { id: 'zoomin', name: 'Zoom +', cat: 'Cámara', icon: '🔍', draw(c, p, A, B, W, H) { if (A) around(c, W, H, () => { c.globalAlpha = 1 - p; c.scale(1 + p * .8, 1 + p * .8); c.translate(-W / 2, -H / 2); c.drawImage(A, 0, 0); c.setTransform(1, 0, 0, 1, 0, 0); }); c.globalAlpha = p; const s = 1.3 - .3 * p; around(c, W, H, () => { c.scale(s, s); c.translate(-W / 2, -H / 2); c.drawImage(B, 0, 0); c.setTransform(1, 0, 0, 1, 0, 0); }); c.globalAlpha = 1; } },
    { id: 'zoomout', name: 'Zoom −', cat: 'Cámara', icon: '🔎', draw(c, p, A, B, W, H) { dA(c, A); c.globalAlpha = p; const s = .5 + .5 * p; around(c, W, H, () => { c.scale(s, s); c.translate(-W / 2, -H / 2); c.drawImage(B, 0, 0); c.setTransform(1, 0, 0, 1, 0, 0); }); c.globalAlpha = 1; } },
    { id: 'spin', name: 'Giro', cat: 'Cámara', icon: '🌀', draw(c, p, A, B, W, H) { dA(c, A, 1 - p); c.globalAlpha = p; around(c, W, H, () => { c.rotate((1 - p) * Math.PI / 2); c.scale(p, p); c.translate(-W / 2, -H / 2); c.drawImage(B, 0, 0); c.setTransform(1, 0, 0, 1, 0, 0); }); c.globalAlpha = 1; } },
    { id: 'flip', name: 'Voltear', cat: 'Cámara', icon: '🔃', draw(c, p, A, B, W, H) { const src = p < .5 ? A : B; if (!src) return; const sx = Math.max(.02, Math.abs(Math.cos(p * Math.PI))); around(c, W, H, () => { c.scale(sx, 1); c.translate(-W / 2, -H / 2); c.drawImage(src, 0, 0); c.setTransform(1, 0, 0, 1, 0, 0); }); } },
    { id: 'blurmix', name: 'Desenfoque', cat: 'Cámara', icon: '💨', draw(c, p, A, B, W, H) { const m = H / 1080; if (A) { c.filter = `blur(${p * 40 * m}px)`; c.globalAlpha = 1 - p; c.drawImage(A, 0, 0); } c.filter = `blur(${(1 - p) * 40 * m}px)`; c.globalAlpha = p; c.drawImage(B, 0, 0); c.filter = 'none'; c.globalAlpha = 1; } },
    { id: 'whipl', name: 'Barrido de cámara ←', cat: 'Cámara', icon: '💨', draw(c, p, A, B, W, H) { const m = H / 1080, e = p * p * (3 - 2 * p), bl = Math.sin(p * Math.PI) * 60 * m; c.filter = `blur(${bl}px)`; if (A) c.drawImage(A, -e * W * 1.2, 0); c.drawImage(B, (1 - e) * W * 1.2, 0); c.filter = 'none'; } },
    { id: 'whipr', name: 'Barrido de cámara →', cat: 'Cámara', icon: '💨', draw(c, p, A, B, W, H) { const m = H / 1080, e = p * p * (3 - 2 * p), bl = Math.sin(p * Math.PI) * 60 * m; c.filter = `blur(${bl}px)`; if (A) c.drawImage(A, e * W * 1.2, 0); c.drawImage(B, -(1 - e) * W * 1.2, 0); c.filter = 'none'; } },
    { id: 'lens', name: 'Lente', cat: 'Cámara', icon: '🔭', draw(c, p, A, B, W, H) { const m = H / 1080, bl = Math.sin(p * Math.PI) * 30 * m; c.filter = `blur(${bl}px)`; if (p < .5) { const s = 1 + p * p * 4; if (A) around(c, W, H, () => { c.scale(s, s); c.translate(-W / 2, -H / 2); c.drawImage(A, 0, 0); c.setTransform(1, 0, 0, 1, 0, 0); }); } else { const s = 1 + (1 - p) * (1 - p) * 4; around(c, W, H, () => { c.scale(s, s); c.translate(-W / 2, -H / 2); c.drawImage(B, 0, 0); c.setTransform(1, 0, 0, 1, 0, 0); }); } c.filter = 'none'; } },
    { id: 'spinblur', name: 'Giro con desenfoque', cat: 'Cámara', icon: '🌪️', draw(c, p, A, B, W, H) { const m = H / 1080, bl = Math.sin(p * Math.PI) * 25 * m; c.filter = `blur(${bl}px)`; const src = p < .5 ? A : B, a = p < .5 ? p * 2 : (1 - p) * 2; if (src) around(c, W, H, () => { c.rotate((p < .5 ? a : -a) * 1.1); c.scale(1 + a * .6, 1 + a * .6); c.translate(-W / 2, -H / 2); c.drawImage(src, 0, 0); c.setTransform(1, 0, 0, 1, 0, 0); }); c.filter = 'none'; } },
    { id: 'shutter', name: 'Obturador', cat: 'Efectos', icon: '📷', draw(c, p, A, B, W, H) { const src = p < .5 ? A : B; if (src) c.drawImage(src, 0, 0); const k = p < .5 ? p * 2 : (1 - p) * 2; c.fillStyle = '#000'; c.fillRect(0, 0, W, H / 2 * k); c.fillRect(0, H - H / 2 * k, W, H / 2 * k); } },
    { id: 'strips', name: 'Tiras', cat: 'Efectos', icon: '▥', draw(c, p, A, B, W, H) { const n = 10, w = W / n, e = p * p * (3 - 2 * p); if (A) c.drawImage(A, 0, 0); for (let i = 0; i < n; i++) { const dir = i % 2 ? 1 : -1, d = (1 - e) * H * dir; c.save(); c.beginPath(); c.rect(i * w, 0, w + 1, H); c.clip(); c.drawImage(B, 0, d); c.restore(); } } },
    { id: 'lightleak', name: 'Fuga de luz', cat: 'Luz', icon: '🌅', draw(c, p, A, B, W, H) { dA(c, A); c.globalAlpha = p; c.drawImage(B, 0, 0); c.globalAlpha = 1; const k = Math.sin(p * Math.PI), x = (p * 1.6 - .3) * W; const g = c.createLinearGradient(x - W * .5, 0, x + W * .5, H); g.addColorStop(0, 'rgba(255,110,40,0)'); g.addColorStop(.5, `rgba(255,190,90,${.85 * k})`); g.addColorStop(1, 'rgba(255,60,120,0)'); c.save(); c.globalCompositeOperation = 'screen'; c.fillStyle = g; c.fillRect(0, 0, W, H); c.restore(); } },
    { id: 'flashcut', name: 'Destello blanco', cat: 'Luz', icon: '⚡', draw(c, p, A, B, W, H) { c.drawImage(p < .5 ? (A || B) : B, 0, 0); const k = Math.pow(Math.sin(p * Math.PI), 3); c.fillStyle = `rgba(255,255,255,${k})`; c.fillRect(0, 0, W, H); } },
    { id: 'filmburn', name: 'Quemadura de película', cat: 'Luz', icon: '🔥', draw(c, p, A, B, W, H) { dA(c, A); c.globalAlpha = p; c.drawImage(B, 0, 0); c.globalAlpha = 1; const k = Math.sin(p * Math.PI); const g = c.createRadialGradient(W * (.2 + .6 * p), H * .4, 0, W * (.2 + .6 * p), H * .4, Math.max(W, H) * .8); g.addColorStop(0, `rgba(255,220,120,${k})`); g.addColorStop(.4, `rgba(255,120,30,${.7 * k})`); g.addColorStop(1, 'rgba(120,10,0,0)'); c.save(); c.globalCompositeOperation = 'screen'; c.fillStyle = g; c.fillRect(0, 0, W, H); c.restore(); } },
    { id: 'shaketr', name: 'Sacudida', cat: 'Cámara', icon: '📳', draw(c, p, A, B, W, H) { const n = Math.floor(p * 24), k = Math.sin(p * Math.PI), dx = (rnd(n) - .5) * W * .08 * k, dy = (rnd(n + 5) - .5) * H * .08 * k; c.globalAlpha = 1; if (A) c.drawImage(A, dx, dy); c.globalAlpha = p; c.drawImage(B, -dx, -dy); c.globalAlpha = 1; } },
    { id: 'glitch', name: 'Glitch', cat: 'Efectos', icon: '📺', draw(c, p, A, B, W, H) { const src = p < .5 ? A : B; if (src) glitchSlices(c, src, W, H, Math.sin(p * Math.PI), Math.floor(p * 20)); } },
  ];
  GC.TBYID = Object.fromEntries(GC.TRANS.map(t => [t.id, t]));

  /* ---------- Animaciones (entrada / salida / combinado) ----------
     f(e,p,out): e = 1 → oculto, 0 → reposo ; devuelve {alpha,dx,dy,sc,rot,sx,sy} */
  const bounceOut = x => { const n = 7.5625, d = 2.75; if (x < 1 / d) return n * x * x; if (x < 2 / d) return n * (x -= 1.5 / d) * x + .75; if (x < 2.5 / d) return n * (x -= 2.25 / d) * x + .9375; return n * (x -= 2.625 / d) * x + .984375; };
  const backOut = x => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };
  GC.ANIM_CATS = ['En tendencia', 'Básicos', 'Movimiento', '3D', 'Luz', 'Fallos'];
  GC.ANIM_IO = [
    { id: 'fade', name: 'Fundido', cat: 'Básicos', trend: 1, f: e => ({ alpha: 1 - e }) },
    { id: 'zoomin', name: 'Zoom +', cat: 'Básicos', trend: 1, f: e => ({ sc: 1 - .7 * e, alpha: 1 - e }) },
    { id: 'zoomout', name: 'Zoom −', cat: 'Básicos', f: e => ({ sc: 1 + e, alpha: 1 - e }) },
    { id: 'slidel', name: 'Deslizar ←', cat: 'Básicos', f: e => ({ dx: e * .5, alpha: 1 - e }) },
    { id: 'slider', name: 'Deslizar →', cat: 'Básicos', f: e => ({ dx: -e * .5, alpha: 1 - e }) },
    { id: 'slideu', name: 'Deslizar ↑', cat: 'Básicos', f: e => ({ dy: e * .5, alpha: 1 - e }) },
    { id: 'slided', name: 'Deslizar ↓', cat: 'Básicos', f: e => ({ dy: -e * .5, alpha: 1 - e }) },
    { id: 'pop', name: 'Rebote', cat: 'Básicos', trend: 1, f: (e, p, out) => { const q = out ? 1 - p : p; return { sc: Math.max(0, backOut(q)), alpha: Math.min(1, q * 3) }; } },
    { id: 'drop', name: 'Caída', cat: 'Movimiento', trend: 1, f: (e, p, out) => { const q = out ? 1 - p : p; return { dy: -(1 - bounceOut(q)) * .5, alpha: Math.min(1, q * 4) }; } },
    { id: 'spin', name: 'Giro', cat: 'Movimiento', f: e => ({ rot: e * Math.PI * 2, sc: 1 - .8 * e, alpha: 1 - e }) },
    { id: 'whirl', name: 'Remolino', cat: 'Movimiento', f: e => ({ rot: e * Math.PI, sc: 1 - .5 * e, alpha: 1 - e }) },
    { id: 'rise', name: 'Ascenso suave', cat: 'Movimiento', f: e => ({ dy: e * .15, alpha: 1 - e }) },
    { id: 'slidebig', name: 'Barrido', cat: 'Movimiento', f: e => ({ dx: e * 1.0 }) },
    { id: 'tilt', name: 'Inclinación', cat: 'Movimiento', f: e => ({ rot: e * .5, dx: e * .15, alpha: 1 - e }) },
    { id: 'flip', name: 'Voltear', cat: '3D', f: e => ({ sx: Math.max(.02, 1 - e), alpha: 1 - e * .5 }) },
    { id: 'flipv', name: 'Voltear vertical', cat: '3D', f: e => ({ sy: Math.max(.02, 1 - e), alpha: 1 - e * .5 }) },
    { id: 'tumble', name: 'Voltereta', cat: '3D', f: e => ({ sx: Math.max(.05, 1 - e), rot: e * 1.2, alpha: 1 - e }) },
    { id: 'flashin', name: 'Destello', cat: 'Luz', f: e => ({ alpha: (1 - e) + e * .6 * (Math.floor(e * 14) % 2) }) },
    { id: 'glow', name: 'Aparición lenta', cat: 'Luz', f: e => ({ alpha: Math.pow(1 - e, 2), sc: 1 + e * .05 }) },
    { id: 'glitchin', name: 'Falla', cat: 'Fallos', trend: 1, f: e => ({ dx: (GC.rnd(Math.floor(e * 24)) - .5) * .12 * e, alpha: 1 - e * (.5 + .5 * GC.rnd(Math.floor(e * 30))) }) },
    { id: 'jitter', name: 'Temblor de entrada', cat: 'Fallos', f: e => ({ dx: (GC.rnd(Math.floor(e * 40)) - .5) * .06 * e, dy: (GC.rnd(Math.floor(e * 40) + 7) - .5) * .06 * e, alpha: 1 - e }) },
    { id: 'typewriter', name: 'Máquina de escribir', cat: 'Básicos', text: true, f: () => ({}) },
  ];
  GC.ANIM_COMBO = [
    { id: 'zoom1', name: 'Zoom 1', cat: 'Básicos', trend: 1, f: t => ({ sc: 1 + .08 * Math.sin(t * 2) }) },
    { id: 'zoom2', name: 'Zoom 2', cat: 'Básicos', f: t => ({ sc: 1 + .15 * Math.abs(Math.sin(t * 2)) }) },
    { id: 'heart', name: 'Latido', cat: 'Básicos', trend: 1, f: t => ({ sc: 1 + .08 * Math.pow(Math.max(0, Math.sin(t * 6)), 2) }) },
    { id: 'breathe', name: 'Respirar', cat: 'Básicos', f: t => ({ sc: 1 + Math.sin(t * 2) * .05 }) },
    { id: 'blink', name: 'Parpadeo', cat: 'Luz', f: t => ({ alpha: .55 + .45 * Math.abs(Math.sin(t * 5)) }) },
    { id: 'strobe', name: 'Estroboscopio', cat: 'Luz', f: t => ({ alpha: Math.floor(t * 8) % 2 ? .35 : 1 }) },
    { id: 'swing', name: 'Balanceo', cat: 'Movimiento', trend: 1, f: t => ({ rot: Math.sin(t * 3) * .15 }) },
    { id: 'pendulum', name: 'Péndulo', cat: 'Movimiento', f: t => ({ rot: Math.sin(t * 2.2) * .4 }) },
    { id: 'bounce1', name: 'Rebote 1', cat: 'Movimiento', f: t => ({ dy: -Math.abs(Math.sin(t * 3)) * .05 }) },
    { id: 'osc', name: 'Oscilación', cat: 'Movimiento', f: t => ({ dx: Math.sin(t * 2) * .04 }) },
    { id: 'float', name: 'Flotar', cat: 'Movimiento', f: t => ({ dy: Math.sin(t * 2) * .02 }) },
    { id: 'slowspin', name: 'Giro lento', cat: 'Movimiento', f: t => ({ rot: t * .5 }) },
    { id: 'wiggle', name: 'Vibrar', cat: 'Fallos', f: t => ({ rot: Math.sin(t * 25) * .04 }) },
    { id: 'shake', name: 'Temblor', cat: 'Fallos', trend: 1, f: t => { const n = Math.floor(t * 24); return { dx: (GC.rnd(n) - .5) * .015, dy: (GC.rnd(n + 9) - .5) * .015 }; } },
    { id: 'flip3d', name: 'Giro 3D', cat: '3D', f: t => ({ sx: Math.max(.05, Math.abs(Math.cos(t * 1.5))) }) },
    { id: 'wobble3d', name: 'Vaivén 3D', cat: '3D', f: t => ({ sx: 1 - .25 * Math.abs(Math.sin(t * 2)) }) },
  ];
  GC.ABYID = Object.fromEntries([...GC.ANIM_IO, ...GC.ANIM_COMBO].map(a => [a.id, a]));
})();
