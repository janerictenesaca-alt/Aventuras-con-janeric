/* Ganchan - motor: proyecto, medios, reproducción, render, historial, exportación */
(function () {
  const G = window.G = {
    project: null, media: new Map(), els: new Map(), sel: null, time: 0, playing: false,
    pps: 80, dirty: true, hist: [], hi: -1, listeners: {}, waitFrames: 0, exporting: false,
    quality: 'Alta', previewMax: 1280,
  };
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const uid = () => Math.random().toString(36).slice(2, 9);
  G.uid = uid; G.clamp = clamp;
  G.on = (e, f) => { (G.listeners[e] = G.listeners[e] || []).push(f); };
  G.emit = (e, a) => (G.listeners[e] || []).forEach(f => f(a));
  G.P = () => G.project;

  /* ---------- Proyecto ---------- */
  G.newProject = () => ({ name: 'Proyecto sin título', ratio: '16:9', res: 1080, fps: 30, bg: '#000000', tracks: [], clips: [] });
  G.clip = id => G.project.clips.find(c => c.id === id);
  G.track = id => G.project.tracks.find(t => t.id === id);
  G.selClip = () => G.sel ? G.clip(G.sel) : null;
  G.duration = () => G.project.clips.reduce((m, c) => Math.max(m, c.start + c.dur), 0);
  G.clipsOn = tid => G.project.clips.filter(c => c.track === tid).sort((a, b) => a.start - b.start);

  G.mkClip = (type, o) => Object.assign({
    id: uid(), type, track: null, start: 0, dur: 3, in: 0, speed: 1, vol: 1, fadeIn: 0, fadeOut: 0,
    x: 0, y: 0, sc: 1, rot: 0, op: 1, flipH: false, flipV: false, blend: 'source-over', mask: null,
    filter: null, adj: {}, fx: [], transIn: null, animIn: null, animOut: null, animLoop: null, mediaId: null, text: null,
  }, o);

  G.fits = (tid, id, s, d) => !G.project.clips.some(o => o.track === tid && o.id !== id && s < o.start + o.dur - 1e-6 && s + d > o.start + 1e-6);
  G.resolveStart = (tid, id, s, d) => {
    s = Math.max(0, s); if (G.fits(tid, id, s, d)) return s;
    const cands = [];
    G.project.clips.forEach(o => { if (o.track === tid && o.id !== id) { cands.push(o.start - d, o.start + o.dur); } });
    const ok = cands.filter(c => c >= 0 && G.fits(tid, id, c, d)).sort((a, b) => Math.abs(a - s) - Math.abs(b - s));
    return ok.length ? ok[0] : null;
  };
  G.newTrack = (kind) => {
    const t = { id: uid(), kind, mute: false, hide: false, lock: false }, P = G.project;
    if (kind === 'v') P.tracks.unshift(t); else P.tracks.push(t);
    return t;
  };
  /* coloca el clip en la primera pista compatible con hueco; si no, crea una pista */
  G.placeClip = (clip, start, preferTid) => {
    const kind = clip.type === 'audio' ? 'a' : 'v', P = G.project;
    clip.start = Math.max(0, start);
    const list = P.tracks.filter(t => t.kind === kind);
    const order = (clip.type === 'video' || clip.type === 'image' || clip.type === 'audio') ? list.slice().reverse() : list;
    if (preferTid) { const pt = G.track(preferTid); if (pt && pt.kind === kind && !pt.lock) { const s = G.resolveStart(pt.id, clip.id, clip.start, clip.dur); if (s !== null) { clip.track = pt.id; clip.start = s; P.clips.push(clip); return clip; } } }
    for (const t of order) { if (t.lock) continue; if (G.fits(t.id, clip.id, clip.start, clip.dur)) { clip.track = t.id; P.clips.push(clip); return clip; } }
    clip.track = G.newTrack(kind).id; P.clips.push(clip); return clip;
  };

  /* ---------- Historial ---------- */
  const snapshot = () => JSON.stringify(G.project);
  G.resetHistory = () => { G.hist = [snapshot()]; G.hi = 0; };
  G.commit = () => {
    const s = snapshot(); if (s === G.hist[G.hi]) return;
    G.hist = G.hist.slice(0, G.hi + 1); G.hist.push(s); if (G.hist.length > 120) G.hist.shift(); G.hi = G.hist.length - 1;
    G.save(); G.emit('hist');
  };
  const restore = () => {
    G.project = JSON.parse(G.hist[G.hi]);
    if (G.sel && !G.clip(G.sel)) G.sel = null;
    G.applyCanvasSize(); G.touch(); G.emit('tl'); G.emit('insp'); G.emit('hist'); G.save();
  };
  G.undo = () => { if (G.hi > 0) { G.hi--; restore(); } };
  G.redo = () => { if (G.hi < G.hist.length - 1) { G.hi++; restore(); } };
  G.touch = () => { G.dirty = true; };
  let saveT = 0;
  G.save = () => {
    clearTimeout(saveT);
    saveT = setTimeout(() => {
      try {
        const media = [...G.media.values()].map(m => ({ id: m.id, name: m.name, type: m.type, sfx: m.sfx }));
        localStorage.setItem('ganchan.project', JSON.stringify({ p: G.project, media }));
        G.emit('saved', new Date());
      } catch (e) { console.warn('autosave', e); }
    }, 400);
  };

  /* ---------- IndexedDB (medios) ---------- */
  let dbp = null;
  const db = () => dbp || (dbp = new Promise((res, rej) => {
    const r = indexedDB.open('ganchan', 1);
    r.onupgradeneeded = () => r.result.createObjectStore('media');
    r.onsuccess = () => res(r.result); r.onerror = () => rej(r.error);
  }));
  const dbPut = async (id, blob) => { try { const d = await db(); d.transaction('media', 'readwrite').objectStore('media').put(blob, id); } catch (e) { } };
  const dbGet = async id => { try { const d = await db(); return await new Promise(r => { const q = d.transaction('media').objectStore('media').get(id); q.onsuccess = () => r(q.result); q.onerror = () => r(null); }); } catch (e) { return null; } };
  const dbClear = async () => { try { const d = await db(); d.transaction('media', 'readwrite').objectStore('media').clear(); } catch (e) { } };

  /* ---------- Audio ---------- */
  G.ensureAudio = () => {
    if (G.actx) return G.actx;
    try {
      G.actx = new (window.AudioContext || window.webkitAudioContext)();
      G.master = G.actx.createGain(); G.dest = G.actx.createMediaStreamDestination();
      G.master.connect(G.actx.destination); G.master.connect(G.dest);
    } catch (e) { console.warn('audio', e); }
    return G.actx;
  };

  /* ---------- Medios ---------- */
  const fmtThumb = (src, w, h) => { const c = document.createElement('canvas'); c.width = 160; c.height = Math.round(160 * h / w) || 90; c.getContext('2d').drawImage(src, 0, 0, c.width, c.height); return c.toDataURL('image/jpeg', .7); };
  const peaksOf = async (blob) => {
    try {
      const ac = G.ensureAudio(); if (!ac || blob.size > 150e6) return null;
      const buf = await ac.decodeAudioData(await blob.arrayBuffer()), d = buf.getChannelData(0), n = Math.ceil(buf.duration * 50), out = new Uint8Array(n), step = d.length / n;
      for (let i = 0; i < n; i++) { let m = 0; const a = Math.floor(i * step), b = Math.min(d.length, Math.floor((i + 1) * step)); for (let j = a; j < b; j += 8) m = Math.max(m, Math.abs(d[j])); out[i] = Math.min(255, m * 255 * 1.4); }
      return out;
    } catch (e) { return null; }
  };
  G.loadMedia = async (id, name, blob, extra) => {
    const type = blob.type.startsWith('video') ? 'video' : blob.type.startsWith('audio') ? 'audio' : 'image';
    const m = Object.assign({ id, name, type, blob, url: URL.createObjectURL(blob), dur: 0, w: 0, h: 0, thumb: null, peaks: null }, extra || {});
    if (type === 'image') {
      const img = new Image(); img.src = m.url; await img.decode().catch(() => { });
      m.img = img; m.w = img.naturalWidth; m.h = img.naturalHeight; m.thumb = fmtThumb(img, m.w, m.h);
    } else {
      const el = document.createElement(type); el.preload = 'metadata'; el.muted = true; el.src = m.url;
      await new Promise(r => { el.onloadedmetadata = r; el.onerror = r; });
      m.dur = isFinite(el.duration) ? el.duration : 0;
      if (type === 'video') {
        m.w = el.videoWidth; m.h = el.videoHeight;
        try { el.currentTime = Math.min(.1, m.dur / 2); await new Promise(r => { el.onseeked = r; setTimeout(r, 1500); }); m.thumb = fmtThumb(el, m.w, m.h); } catch (e) { }
      }
      peaksOf(blob).then(p => { m.peaks = p; G.emit('tl'); });
    }
    G.media.set(id, m); G.emit('media'); G.save();
    return m;
  };
  G.importFiles = async files => {
    const out = [];
    for (const f of files) {
      if (!/^(video|audio|image)\//.test(f.type)) continue;
      const id = uid(); await dbPut(id, f); out.push(await G.loadMedia(id, f.name, f));
    }
    return out;
  };
  G.removeMedia = id => {
    G.project.clips.filter(c => c.mediaId === id).forEach(c => G.deleteClip(c.id, true));
    G.media.delete(id); G.emit('media'); G.emit('tl'); G.commit();
  };
  G.addMediaClip = (m, start, tid) => {
    const type = m.type, dur = type === 'image' ? 5 : (m.dur || 5);
    const c = G.mkClip(type, { mediaId: m.id, dur, name: m.name });
    G.placeClip(c, start ?? G.time, tid); G.sel = c.id; G.touch(); G.emit('tl'); G.emit('insp'); G.commit(); return c;
  };
  G.addText = (preset, start) => {
    const base = { s: 'Texto', font: 'Arial', size: 90, bold: false, italic: false, color: '#ffffff', stroke: '#000000', strokeW: 0, shadow: null, bg: null, glow: false, spacing: 0 };
    const c = G.mkClip('text', { dur: 3, text: Object.assign(base, preset ? preset.t : {}), y: preset && preset.y || 0 });
    G.placeClip(c, start ?? G.time); G.sel = c.id; G.touch(); G.emit('tl'); G.emit('insp'); G.commit(); return c;
  };
  G.addSticker = (emoji, start) => {
    const c = G.mkClip('sticker', { dur: 3, text: { s: emoji, size: 260 } });
    G.placeClip(c, start ?? G.time); G.sel = c.id; G.touch(); G.emit('tl'); G.emit('insp'); G.commit(); return c;
  };
  G.addSfx = async (id, start) => {
    let m = [...G.media.values()].find(x => x.sfx === id);
    if (!m) { const blob = await synthSfx(id); const mid = uid(); await dbPut(mid, blob); m = await G.loadMedia(mid, GC.SFX.find(s => s.id === id).name, blob, { sfx: id }); }
    return G.addMediaClip(m, start);
  };

  /* ---------- Edición ---------- */
  G.deleteClip = (id, silent) => {
    const P = G.project; P.clips = P.clips.filter(c => c.id !== id);
    disposeEl(id); if (G.sel === id) G.sel = null;
    if (!silent) { G.touch(); G.emit('tl'); G.emit('insp'); G.commit(); }
  };
  G.duplicate = id => {
    const c = G.clip(id); if (!c) return;
    const n = JSON.parse(JSON.stringify(c)); n.id = uid();
    G.placeClip(n, c.start + c.dur); G.sel = n.id; G.touch(); G.emit('tl'); G.emit('insp'); G.commit();
  };
  G.split = (id, t) => {
    const a = G.clip(id); t = t ?? G.time;
    if (!a || t <= a.start + .05 || t >= a.start + a.dur - .05) return false;
    const b = JSON.parse(JSON.stringify(a)); b.id = uid();
    b.start = t; b.dur = a.start + a.dur - t; b.in = a.in + (t - a.start) * a.speed; b.transIn = null; b.animIn = null; b.fadeIn = 0;
    a.dur = t - a.start; a.animOut = null; a.fadeOut = 0;
    G.project.clips.push(b); G.sel = b.id; G.touch(); G.emit('tl'); G.emit('insp'); G.commit(); return true;
  };
  G.splitAtPlayhead = () => {
    const s = G.selClip();
    if (s && G.time > s.start && G.time < s.start + s.dur) return G.split(s.id);
    const hit = G.project.clips.filter(c => G.time > c.start + .05 && G.time < c.start + c.dur - .05);
    hit.forEach(c => G.split(c.id)); return hit.length > 0;
  };
  G.targetClip = () => {
    const s = G.selClip(); if (s) return s;
    for (const t of G.project.tracks.filter(t => t.kind === 'v')) { const c = G.clipsOn(t.id).find(c => G.time >= c.start && G.time < c.start + c.dur); if (c) return c; }
    return null;
  };
  G.setSpeed = (c, sp) => {
    const span = c.dur * c.speed; c.speed = sp; const nd = span / sp;
    if (G.fits(c.track, c.id, c.start, nd)) c.dur = nd; else { c.speed = span / c.dur; return false; }
    return true;
  };

  /* ---------- Elementos multimedia ---------- */
  function disposeEl(id) { const e = G.els.get(id); if (!e) return; try { e.pause(); } catch (x) { } if (e._gain) try { e._gain.disconnect(); } catch (x) { } G.els.delete(id); }
  const getEl = clip => {
    let e = G.els.get(clip.id); if (e) return e;
    const m = G.media.get(clip.mediaId); if (!m) return null;
    if (clip.type === 'image') return m.img;
    e = document.createElement(clip.type === 'video' ? 'video' : 'audio'); e.preload = 'auto'; e.playsInline = true; e.src = m.url;
    e.addEventListener('seeked', G.touch); e.addEventListener('loadeddata', G.touch);
    const ac = G.ensureAudio();
    if (ac) { try { const s = ac.createMediaElementSource(e), g = ac.createGain(); s.connect(g); g.connect(G.master); e._gain = g; } catch (x) { } }
    else e.muted = true;
    G.els.set(clip.id, e); return e;
  };
  G.srcTime = (c, lt) => c.in + lt * c.speed;
  const holding = (clip, t) => { // clip saliente durante una transición del siguiente
    const nx = G.project.clips.find(o => o.track === clip.track && o.transIn && Math.abs(o.start - (clip.start + clip.dur)) < .05);
    return nx && t >= clip.start + clip.dur && t < nx.start + nx.transIn.dur;
  };
  const fadeVol = (c, lt) => {
    let f = 1; if (c.fadeIn > 0 && lt < c.fadeIn) f = lt / c.fadeIn; if (c.fadeOut > 0 && lt > c.dur - c.fadeOut) f = Math.min(f, (c.dur - lt) / c.fadeOut);
    return clamp(f, 0, 1);
  };
  function syncMedia(t) {
    const P = G.project, ids = new Set(P.clips.map(c => c.id));
    for (const id of [...G.els.keys()]) if (!ids.has(id)) disposeEl(id);
    for (const c of P.clips) {
      if (c.type !== 'video' && c.type !== 'audio') continue;
      const end = c.start + c.dur, near = t >= c.start - 2.5 && t < end + .1, active = t >= c.start && t < end, hold = holding(c, t);
      let e = G.els.get(c.id);
      if (!near && !hold) { if (e && !e.paused) e.pause(); continue; }
      e = e || getEl(c); if (!e) continue;
      const tr = G.track(c.track);
      if (e._gain) e._gain.gain.value = (tr && tr.mute) || !active ? 0 : c.vol * fadeVol(c, t - c.start);
      const lt = clamp(t - c.start, 0, c.dur), want = clamp(G.srcTime(c, lt), 0, Math.max(0, (G.media.get(c.mediaId).dur || 1e9) - .02));
      if (G.playing && active) {
        e.playbackRate = clamp(c.speed, .0625, 16);
        if (e.paused) { e.currentTime = want; e._target = want; const p = e.play(); if (p) p.catch(() => { }); }
        else if (Math.abs(e.currentTime - want) > .3) { e.currentTime = want; e._target = want; }
      } else {
        if (!e.paused) e.pause();
        if (e._target === undefined || Math.abs(e._target - want) > .02) { e._target = want; try { e.currentTime = want; } catch (x) { } }
      }
    }
  }

  /* ---------- Render ---------- */
  G.applyCanvasSize = () => {
    const P = G.project, [fw, fh] = GC.sizeFor(P.ratio, P.res), k = Math.min(1, G.previewMax / Math.max(fw, fh));
    const w = G.exporting ? fw : Math.round(fw * k / 2) * 2, h = G.exporting ? fh : Math.round(fh * k / 2) * 2;
    if (G.canvas && (G.canvas.width !== w || G.canvas.height !== h)) { G.canvas.width = w; G.canvas.height = h; }
    G.emit('size'); G.touch();
  };
  const layer = (name, W, H) => { const c = GC.scratch(name, W, H); return c; };

  function drawText(c, clip, S, lt) {
    const T = clip.text; let s = T.s || '';
    const ai = clip.animIn; if (ai && ai.id === 'typewriter' && lt < ai.dur) s = Array.from(s).slice(0, Math.ceil(Array.from(s).length * lt / ai.dur)).join('');
    const size = T.size * S, lines = s.split('\n');
    c.font = `${T.italic ? 'italic ' : ''}${T.bold ? 'bold ' : ''}${size}px "${T.font}", sans-serif`;
    c.textAlign = 'center'; c.textBaseline = 'middle'; c.lineJoin = 'round';
    if ('letterSpacing' in c) c.letterSpacing = ((T.spacing || 0) * S) + 'px';
    const lh = size * 1.2, pad = T.bg ? size * .3 : 0;
    const full = (clip.text.s || '').split('\n'); let wMax = 0;
    full.forEach(l => { wMax = Math.max(wMax, c.measureText(l).width); });
    const bw = wMax + pad * 2, bh = full.length * lh + pad * 2, y0 = -((lines.length - 1) * lh) / 2 - (full.length - lines.length) * 0;
    const top = -((full.length - 1) * lh) / 2;
    if (T.bg) { c.fillStyle = T.bg; c.beginPath(); (c.roundRect ? c.roundRect(-bw / 2, -bh / 2, bw, bh, size * .2) : c.rect(-bw / 2, -bh / 2, bw, bh)); c.fill(); }
    lines.forEach((l, i) => {
      const y = top + i * lh;
      if (T.shadow) { c.shadowColor = T.shadow.c; c.shadowBlur = T.shadow.b * S; c.shadowOffsetX = T.shadow.x * S; c.shadowOffsetY = T.shadow.y * S; }
      if (T.strokeW > 0) { c.strokeStyle = T.stroke; c.lineWidth = T.strokeW * S; c.strokeText(l, 0, y); }
      c.fillStyle = T.color; c.fillText(l, 0, y);
      if (T.glow && T.shadow) { c.fillText(l, 0, y); c.fillText(l, 0, y); }
      c.shadowColor = 'transparent'; c.shadowBlur = 0; c.shadowOffsetX = c.shadowOffsetY = 0;
    });
    return [bw, bh];
  }
  function maskPath(c, type, bw, bh, k) {
    const r = Math.min(bw, bh) / 2 * k; c.beginPath();
    if (type === 'circle') c.arc(0, 0, r, 0, 7);
    else if (type === 'rect') { const w = bw * k * .8, h = bh * k * .8; c.rect(-w / 2, -h / 2, w, h); }
    else if (type === 'heart') { c.moveTo(0, r * .9); c.bezierCurveTo(-r * 1.6, -r * .1, -r * .8, -r * 1.2, 0, -r * .4); c.bezierCurveTo(r * .8, -r * 1.2, r * 1.6, -r * .1, 0, r * .9); c.closePath(); }
    else if (type === 'star') { for (let i = 0; i < 10; i++) { const a = -Math.PI / 2 + i * Math.PI / 5, rr = i % 2 ? r * .45 : r; c[i ? 'lineTo' : 'moveTo'](Math.cos(a) * rr, Math.sin(a) * rr); } c.closePath(); }
  }
  function drawClipLayer(clip, lt, cv, opts) {
    opts = opts || {};
    const W = cv.width, H = cv.height, S = Math.min(W, H) / 1080, c = cv.getContext('2d');
    c.setTransform(1, 0, 0, 1, 0, 0); c.globalAlpha = 1; c.globalCompositeOperation = 'source-over'; c.filter = 'none'; c.clearRect(0, 0, W, H);
    const a = { alpha: 1, dx: 0, dy: 0, sc: 1, rot: 0, sx: 1 };
    const mix = r => { if (!r) return; if (r.alpha !== undefined) a.alpha *= r.alpha; if (r.dx) a.dx += r.dx; if (r.dy) a.dy += r.dy; if (r.sc) a.sc *= r.sc; if (r.rot) a.rot += r.rot; if (r.sx !== undefined) a.sx *= r.sx; };
    const ai = clip.animIn && GC.ABYID[clip.animIn.id];
    if (ai && lt < clip.animIn.dur) { const p = clamp(lt / clip.animIn.dur, 0, 1), e = 1 - p * p * (3 - 2 * p); mix(ai.f(e, p, false)); }
    const ao = clip.animOut && GC.ABYID[clip.animOut.id];
    if (ao && !opts.noOut && lt > clip.dur - clip.animOut.dur) { const p = clamp((lt - (clip.dur - clip.animOut.dur)) / clip.animOut.dur, 0, 1), e = p * p * (3 - 2 * p); mix(ao.f(e, p, true)); }
    const al = clip.animLoop && GC.ABYID[clip.animLoop.id]; if (al) mix(al.f(lt * (clip.animLoop.speed || 1)));
    (clip.fx || []).forEach(f => { const d = GC.FXBYID[f.id]; if (d && d.xf) mix(d.xf(lt, f.k)); });
    const cx = W / 2 + (clip.x + a.dx) * W, cy = H / 2 + (clip.y + a.dy) * H, rot = clip.rot * Math.PI / 180 + a.rot, sc = clip.sc * a.sc;
    c.translate(cx, cy); c.rotate(rot); c.scale(sc * (clip.flipH ? -1 : 1) * a.sx, sc * (clip.flipV ? -1 : 1));
    const def = clip.filter ? GC.FBYID[clip.filter.id] : null, k = clip.filter ? clip.filter.k : 1;
    c.filter = GC.filterStr(def, k, clip.adj, S);
    let bw = 0, bh = 0;
    if (clip.type === 'video' || clip.type === 'image') {
      const m = G.media.get(clip.mediaId), e = getEl(clip);
      if (m && e && m.w) { const base = Math.min(W / m.w, H / m.h); bw = m.w * base; bh = m.h * base; c.save(); if (clip.mask) { maskPath(c, clip.mask.t, bw, bh, clip.mask.s); c.clip(); } try { c.drawImage(e, -bw / 2, -bh / 2, bw, bh); } catch (x) { } c.restore(); }
    } else if (clip.type === 'text') { [bw, bh] = drawText(c, clip, S, lt); }
    else if (clip.type === 'sticker') { const sz = clip.text.size * S; c.font = `${sz}px "Apple Color Emoji","Segoe UI Emoji","Noto Color Emoji",sans-serif`; c.textAlign = 'center'; c.textBaseline = 'middle'; c.fillText(clip.text.s, 0, 0); bw = bh = sz * 1.15; }
    c.setTransform(1, 0, 0, 1, 0, 0); c.filter = 'none';
    clip._box = { cx, cy, w: bw * sc, h: bh * sc, rot };
    GC.tintsOf(def, k, clip.adj).forEach(t => GC.tintLayer(c, t[0], t[1], t[2], t[3], t[4]));
    if (clip.adj && clip.adj.vignette) GC.vignette(c, clip.adj.vignette / 100);
    if (clip.adj && clip.adj.grain) GC.grain(c, clip.adj.grain / 100, lt);
    (clip.fx || []).forEach(f => { const d = GC.FXBYID[f.id]; if (d && d.post) { c.save(); d.post(c, W, H, lt, f.k); c.restore(); } });
    return a.alpha;
  }
  G.drawClipLayer = drawClipLayer;

  G.render = (force) => {
    const P = G.project, cv = G.canvas; if (!cv) return;
    const W = cv.width, H = cv.height, t = G.time, ctx = cv.getContext('2d');
    const vts = P.tracks.filter(x => x.kind === 'v').slice().reverse();
    if (!force) {
      for (const tr of vts) { if (tr.hide) continue; for (const c of G.clipsOn(tr.id)) if (c.type === 'video' && (t >= c.start && t < c.start + c.dur || holding(c, t))) { const e = G.els.get(c.id); if (e && e.readyState < 2 && G.waitFrames < 20) { G.waitFrames++; return; } } }
    }
    G.waitFrames = 0;
    ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over'; ctx.filter = 'none';
    ctx.fillStyle = P.bg; ctx.fillRect(0, 0, W, H);
    const LA = layer('LA', W, H), LB = layer('LB', W, H), LT = layer('LT', W, H);
    const put = (cv2, clip, al) => { ctx.globalAlpha = clamp(clip.op * al, 0, 1); ctx.globalCompositeOperation = clip.blend; ctx.drawImage(cv2, 0, 0); ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over'; };
    for (const tr of vts) {
      if (tr.hide) continue;
      for (const clip of G.clipsOn(tr.id)) {
        if (t < clip.start || t >= clip.start + clip.dur || clip.type === 'audio') continue;
        const lt = t - clip.start;
        if (clip.transIn && lt < clip.transIn.dur && GC.TBYID[clip.transIn.id]) {
          const prev = G.clipsOn(tr.id).find(o => o !== clip && Math.abs(o.start + o.dur - clip.start) < .05 && o.type !== 'audio');
          const p = clamp(lt / clip.transIn.dur, 0, 1);
          const aB = drawClipLayer(clip, lt, LB), aA = prev ? drawClipLayer(prev, prev.dur, LA, { noOut: true }) : 0;
          const tc = LT.getContext('2d'); tc.setTransform(1, 0, 0, 1, 0, 0); tc.globalAlpha = 1; tc.globalCompositeOperation = 'source-over'; tc.filter = 'none'; tc.clearRect(0, 0, W, H);
          GC.TBYID[clip.transIn.id].draw(tc, p, prev ? LA : null, LB, W, H);
          put(LT, clip, aB);
        } else { const al = drawClipLayer(clip, lt, LB); put(LB, clip, al); }
      }
    }
    G.emit('rendered');
  };

  /* ---------- Reproducción ---------- */
  G.seek = t => { G.time = clamp(t, 0, Math.max(G.duration(), 0)); if (G.playing) { G.playT0 = G.time; G.playWall = performance.now(); } syncMedia(G.time); G.touch(); G.emit('time'); };
  G.play = () => {
    const d = G.duration(); if (!d) return;
    const ac = G.ensureAudio(); if (ac && ac.state === 'suspended') ac.resume();
    if (G.time >= d - .03) G.time = 0;
    G.playing = true; G.playT0 = G.time; G.playWall = performance.now(); G.emit('play');
  };
  G.pause = () => { G.playing = false; G.els.forEach(e => { try { e.pause(); } catch (x) { } }); G.emit('play'); };
  G.toggle = () => G.playing ? G.pause() : G.play();
  function tick() {
    if (G.project) {
      if (G.playing) {
        G.time = G.playT0 + (performance.now() - G.playWall) / 1000;
        const d = G.duration();
        if (G.time >= d) { G.time = d; syncMedia(d); G.render(true); G.pause(); G.emit('time'); G.emit('end'); }
        else G.emit('time');
        syncMedia(G.time); G.dirty = true;
      } else if (G.dirty) syncMedia(G.time);
      if (G.dirty) { G.dirty = false; G.render(); if (G.waitFrames > 0) G.dirty = true; }
    }
    requestAnimationFrame(tick);
  }

  /* ---------- Sonidos sintetizados ---------- */
  const wav = (buf) => {
    const d = buf.getChannelData(0), n = d.length, ab = new ArrayBuffer(44 + n * 2), v = new DataView(ab), w = (o, s) => [...s].forEach((ch, i) => v.setUint8(o + i, ch.charCodeAt(0)));
    w(0, 'RIFF'); v.setUint32(4, 36 + n * 2, true); w(8, 'WAVEfmt '); v.setUint32(16, 16, true); v.setUint16(20, 1, true); v.setUint16(22, 1, true);
    v.setUint32(24, buf.sampleRate, true); v.setUint32(28, buf.sampleRate * 2, true); v.setUint16(32, 2, true); v.setUint16(34, 16, true); w(36, 'data'); v.setUint32(40, n * 2, true);
    for (let i = 0; i < n; i++) v.setInt16(44 + i * 2, clamp(d[i], -1, 1) * 32767, true);
    return new Blob([ab], { type: 'audio/wav' });
  };
  async function synthSfx(id) {
    const sr = 44100, spec = GC.SFX.find(s => s.id === id), oc = new OfflineAudioContext(1, Math.ceil(sr * spec.d), sr);
    const g = oc.createGain(); g.connect(oc.destination);
    const noise = () => { const b = oc.createBuffer(1, oc.length, sr), a = b.getChannelData(0); for (let i = 0; i < a.length; i++) a[i] = Math.random() * 2 - 1; const s = oc.createBufferSource(); s.buffer = b; return s; };
    const osc = (type, f0, f1, d) => { const o = oc.createOscillator(); o.type = type; o.frequency.setValueAtTime(f0, 0); o.frequency.exponentialRampToValueAtTime(f1, d); o.connect(g); o.start(); o.stop(d + .05); return o; };
    const d = spec.d;
    if (id === 'whoosh') { const n = noise(), f = oc.createBiquadFilter(); f.type = 'bandpass'; f.Q.value = 1.5; f.frequency.setValueAtTime(300, 0); f.frequency.exponentialRampToValueAtTime(4000, d * .5); f.frequency.exponentialRampToValueAtTime(500, d); g.gain.setValueAtTime(0, 0); g.gain.linearRampToValueAtTime(.9, d * .45); g.gain.linearRampToValueAtTime(0, d); n.connect(f); f.connect(g); n.start(); }
    else if (id === 'pop') { g.gain.setValueAtTime(.9, 0); g.gain.exponentialRampToValueAtTime(.001, d); osc('sine', 700, 150, d); }
    else if (id === 'ding') { g.gain.setValueAtTime(.6, 0); g.gain.exponentialRampToValueAtTime(.001, d); osc('sine', 1320, 1319, d); osc('sine', 1980, 1979, d); }
    else if (id === 'riser') { const n = noise(), f = oc.createBiquadFilter(); f.type = 'bandpass'; f.frequency.setValueAtTime(200, 0); f.frequency.exponentialRampToValueAtTime(6000, d); g.gain.setValueAtTime(0, 0); g.gain.linearRampToValueAtTime(.8, d); n.connect(f); f.connect(g); n.start(); osc('sawtooth', 100, 800, d); }
    else if (id === 'impact') { g.gain.setValueAtTime(1, 0); g.gain.exponentialRampToValueAtTime(.001, d); osc('sine', 90, 30, d); const n = noise(), f = oc.createBiquadFilter(); f.type = 'lowpass'; f.frequency.value = 600; n.connect(f); f.connect(g); n.start(); }
    else if (id === 'laser') { g.gain.setValueAtTime(.5, 0); g.gain.exponentialRampToValueAtTime(.001, d); osc('sawtooth', 1800, 200, d); }
    else if (id === 'coin') { g.gain.setValueAtTime(.4, 0); g.gain.setValueAtTime(.4, .08); g.gain.exponentialRampToValueAtTime(.001, d); const o = oc.createOscillator(); o.type = 'square'; o.frequency.setValueAtTime(988, 0); o.frequency.setValueAtTime(1319, .08); o.connect(g); o.start(); o.stop(d); }
    else { g.gain.setValueAtTime(.8, 0); g.gain.exponentialRampToValueAtTime(.001, d); const n = noise(), f = oc.createBiquadFilter(); f.type = 'highpass'; f.frequency.value = 2000; n.connect(f); f.connect(g); n.start(); }
    return wav(await oc.startRendering());
  }

  /* ---------- Grabar voz ---------- */
  G.recordVoice = async () => {
    const st = await navigator.mediaDevices.getUserMedia({ audio: true }), rec = new MediaRecorder(st), chunks = [], start = G.time;
    rec.ondataavailable = e => chunks.push(e.data);
    const done = new Promise(r => rec.onstop = r);
    rec.start();
    return { stop: async () => { rec.stop(); await done; st.getTracks().forEach(t => t.stop()); const blob = new Blob(chunks, { type: rec.mimeType || 'audio/webm' }); const id = uid(); await dbPut(id, blob); const m = await G.loadMedia(id, 'Grabación de voz', blob); G.addMediaClip(m, start); } };
  };

  /* ---------- Exportar ---------- */
  G.exportVideo = ({ res, fps, bitrate, onProgress }) => new Promise(async (resolve, reject) => {
    const P = G.project, d = G.duration(); if (!d) return reject(new Error('No hay nada que exportar'));
    G.pause(); const oldRes = P.res; P.res = res; G.exporting = true; G.applyCanvasSize();
    G.ensureAudio(); if (G.actx.state === 'suspended') await G.actx.resume();
    G.seek(0); await new Promise(r => setTimeout(r, 600)); G.render(true);
    const mimes = ['video/mp4;codecs=avc1.42E01E,mp4a.40.2', 'video/webm;codecs=vp9,opus', 'video/webm;codecs=vp8,opus', 'video/webm'];
    const mime = mimes.find(m => window.MediaRecorder && MediaRecorder.isTypeSupported(m)) || '';
    const stream = new MediaStream([...G.canvas.captureStream(fps).getVideoTracks(), ...G.dest.stream.getAudioTracks()]);
    const rec = new MediaRecorder(stream, { mimeType: mime, videoBitsPerSecond: bitrate }), chunks = []; let cancelled = false;
    const off = () => { onProgress && onProgress(G.time / d); };
    const endH = () => { setTimeout(() => { if (rec.state !== 'inactive') rec.stop(); }, 400); };
    const finish = () => { G.listeners.time = G.listeners.time.filter(f => f !== off); G.listeners.end = (G.listeners.end || []).filter(f => f !== endH); G.exporting = false; P.res = oldRes; G.applyCanvasSize(); G.seek(0); };
    rec.ondataavailable = e => { if (e.data.size) chunks.push(e.data); };
    rec.onstop = () => { finish(); if (cancelled) return reject(new Error('cancelado')); resolve({ blob: new Blob(chunks, { type: mime.split(';')[0] || 'video/webm' }), ext: mime.startsWith('video/mp4') ? 'mp4' : 'webm' }); };
    G.exportCancel = () => { cancelled = true; G.pause(); rec.stop(); };
    G.on('time', off); G.on('end', endH);
    rec.start(250); G.play();
  });

  /* ---------- Arranque ---------- */
  G.init = async (canvas) => {
    G.canvas = canvas;
    let loaded = false;
    try {
      const raw = localStorage.getItem('ganchan.project');
      if (raw) {
        const j = JSON.parse(raw); G.project = j.p;
        for (const m of j.media || []) { const b = await dbGet(m.id); if (b) await G.loadMedia(m.id, m.name, b, m.sfx ? { sfx: m.sfx } : null); }
        const ids = new Set(G.media.keys()); G.project.clips = G.project.clips.filter(c => !c.mediaId || ids.has(c.mediaId)); loaded = true;
      }
    } catch (e) { console.warn('load', e); }
    if (!loaded) G.project = G.newProject();
    G.resetHistory(); G.applyCanvasSize(); G.emit('tl'); G.emit('insp'); G.emit('media');
    requestAnimationFrame(tick);
  };
  G.reset = async () => {
    G.pause(); G.els.forEach((e, id) => disposeEl(id)); G.media.forEach(m => URL.revokeObjectURL(m.url)); G.media.clear();
    await dbClear(); G.project = G.newProject(); G.sel = null; G.time = 0; G.resetHistory(); G.applyCanvasSize(); G.save();
    G.emit('tl'); G.emit('insp'); G.emit('media'); G.emit('time'); G.emit('hist');
  };
})();
