/* Ganjan - interfaz (pestañas, línea de tiempo, inspector, interacción) */
(function () {
  const ui = G.ui, { $, h, fmt, fmtS, toast } = G.ui;
  const clamp = G.clamp;

  const libTabs = () => ui.libTabs(), libBody = () => ui.libBody(), inspector = () => ui.inspector();

  /* ============ Línea de tiempo ============ */
  const HW = 128;
  function toolbar() {
    const t = $('#tltools'); t.innerHTML = '';
    const tb = (ic, title, fn, id, on) => h('button', { class: 'tb' + (on ? ' on' : ''), title, id, onclick: fn }, ic);
    t.append(tb('＋', 'Añadir archivos', () => $('#fileIn').click()), h('span', { class: 'sep' }),
      tb('↶', 'Deshacer (Ctrl+Z)', G.undo, 'bUndo'), tb('↷', 'Rehacer (Ctrl+Shift+Z)', G.redo, 'bRedo'), h('span', { class: 'sep' }),
      tb('✂', 'Dividir (Ctrl+B)', () => { if (!G.splitAtPlayhead()) toast('Coloca el cursor sobre un clip'); }),
      tb('⇤', 'Recortar a la izquierda (Q)', trimL), tb('⇥', 'Recortar a la derecha (W)', trimR),
      tb('🗑', 'Eliminar (Supr)', delSel), tb('⧉', 'Duplicar (Ctrl+D)', () => G.sel && G.duplicate(G.sel)),
      h('span', { class: 'sep' }), tb('🎤', 'Grabar voz', () => ui.toggleRec(), 'bMic'),
      h('div', { class: 'spacer' }),
      tb('🧲', 'Imán (ajuste automático)', e => { ui.magnet = !ui.magnet; e.currentTarget.classList.toggle('on', ui.magnet); }, 'bMag', ui.magnet),
      tb('⤢', 'Ajustar al proyecto', fitZoom), tb('−', 'Alejar', () => setZoom(G.pps / 1.3)),
      h('input', { type: 'range', min: 0, max: 100, id: 'zoomR', oninput: e => setZoom(zoomFrom(+e.target.value)) }), tb('＋', 'Acercar', () => setZoom(G.pps * 1.3)));
    syncHist();
  }
  const zoomTo = p => 100 * Math.log(p / 6) / Math.log(400 / 6), zoomFrom = v => 6 * Math.pow(400 / 6, v / 100);
  function setZoom(p) { const sc = $('#tlscroll'), tc = G.time * G.pps - sc.scrollLeft; G.pps = clamp(p, 6, 400); renderTL(); sc.scrollLeft = G.time * G.pps - tc; $('#zoomR').value = zoomTo(G.pps); }
  function fitZoom() { const d = Math.max(G.duration(), 5); setZoom(($('#tlscroll').clientWidth - HW - 60) / d); }
  function syncHist() { const u = $('#bUndo'), r = $('#bRedo'); if (u) u.disabled = G.hi <= 0; if (r) r.disabled = G.hi >= G.hist.length - 1; }
  const delSel = () => { if (G.sel) G.deleteClip(G.sel); };
  const trimL = () => { const c = G.selClip(); if (!c || G.time <= c.start || G.time >= c.start + c.dur) return; const d = G.time - c.start; c.in += d * c.speed; c.start = G.time; c.dur -= d; c.transIn = null; G.touch(); G.emit('tl'); G.commit(); };
  const trimR = () => { const c = G.selClip(); if (!c || G.time <= c.start || G.time >= c.start + c.dur) return; c.dur = G.time - c.start; G.touch(); G.emit('tl'); G.commit(); };

  const rowH = t => t.kind === 'a' ? 46 : 64;
  const hitKinds = ['video', 'image', 'text', 'sticker'];
  function renderTL() {
    const inner = $('#tlinner'), P = G.project, pps = G.pps, vw = $('#tlscroll').clientWidth;
    const total = Math.max(G.duration() + 12, (vw - HW) / pps), lw = total * pps;
    inner.style.width = (HW + lw) + 'px'; inner.innerHTML = '';
    // regla
    const steps = [.5, 1, 2, 5, 10, 15, 30, 60, 120, 300, 600], step = steps.find(s => s * pps >= 90) || 600;
    const ruler = h('div', { class: 'row ruler', style: 'height:26px' }, h('div', { class: 'thead', style: 'height:26px' }), h('div', { class: 'lane', style: `width:${lw}px;height:26px` }));
    const rl = ruler.lastChild;
    for (let s = 0; s <= total; s += step) { rl.append(h('div', { class: 'tick', style: `left:${s * pps}px` }, fmtS(s))); const sub = step / 2; if (s + sub < total && sub * pps > 20) rl.append(h('div', { class: 'tick minor', style: `left:${(s + sub) * pps}px` })); }
    ruler.addEventListener('pointerdown', e => scrub(e, rl)); inner.append(ruler);
    // pistas
    P.tracks.forEach(tr => {
      const lane = h('div', { class: 'lane', 'data-tid': tr.id, style: `width:${lw}px;height:${rowH(tr)}px` });
      G.clipsOn(tr.id).forEach(c => lane.append(clipEl(c, tr)));
      const head = h('div', { class: 'thead', style: `height:${rowH(tr)}px` },
        h('button', { class: tr.lock ? 'on' : '', title: 'Bloquear pista', onclick: () => { tr.lock = !tr.lock; G.commit(); renderTL(); } }, '🔒'),
        tr.kind === 'v' ? h('button', { class: tr.hide ? '' : 'on', title: 'Mostrar/ocultar', onclick: () => { tr.hide = !tr.hide; G.touch(); G.commit(); renderTL(); } }, tr.hide ? '🚫' : '👁') : null,
        h('button', { class: tr.mute ? '' : 'on', title: 'Silenciar pista', onclick: () => { tr.mute = !tr.mute; G.touch(); G.commit(); renderTL(); } }, tr.mute ? '🔇' : '🔊'),
        h('button', { title: 'Más', 'data-pop': 1, onclick: e => ui.popMenu(e.currentTarget, [{ label: 'Eliminar pista', fn: () => { G.project.clips.filter(c => c.track === tr.id).forEach(c => G.deleteClip(c.id, true)); G.project.tracks = G.project.tracks.filter(t => t.id !== tr.id); G.touch(); G.emit('tl'); G.emit('insp'); G.commit(); } }]) }, '⋯'));
      const row = h('div', { class: 'row ' + tr.kind }, head, lane);
      lane.addEventListener('pointerdown', e => { if (e.target === lane) { G.sel = null; G.emit('insp'); renderTL(); scrub(e, lane); } });
      inner.append(row);
    });
    if (!P.tracks.length) inner.append(h('div', { class: 'empty', style: `padding-left:${HW + 40}px;text-align:left` }, 'Arrastra aquí tus archivos o pulsa + en los archivos multimedia para empezar a editar'));
    inner.append(h('div', { id: 'playhead' }));
    movePlayhead(); $('#tTot').textContent = fmt(G.duration());
  }
  function clipEl(c, tr) {
    const pps = G.pps, m = G.media.get(c.mediaId), kind = c.type === 'video' ? 'v' : c.type === 'audio' ? 'a' : c.type;
    const el = h('div', { class: `clip ${kind}${G.sel === c.id ? ' sel' : ''}${tr.mute && c.type === 'audio' ? ' muted' : ''}`, 'data-id': c.id, style: `left:${c.start * pps}px;width:${Math.max(4, c.dur * pps)}px` });
    if (c.type === 'video' && m && m.thumb) el.append(h('div', { class: 'strip', style: `background-image:url(${m.thumb})` }));
    if (c.type === 'image' && m && m.thumb) el.append(h('div', { class: 'strip', style: `background-image:url(${m.thumb})` }));
    if (c.type === 'audio' && m && m.peaks) { const cv = h('canvas', { width: Math.max(4, Math.floor(c.dur * pps)), height: 40 }); const x = cv.getContext('2d'); x.fillStyle = '#9bd7ff'; const n = cv.width, i0 = c.in * 50, span = c.dur * c.speed * 50; for (let i = 0; i < n; i += 2) { const p = m.peaks[Math.floor(i0 + (i / n) * span)] || 0, hh = Math.max(1, p / 255 * 38 * Math.min(1.5, c.vol)); x.fillRect(i, 20 - hh / 2, 1.5, hh); } el.append(cv); }
    const label = c.type === 'text' ? (c.text.s || '').split('\n')[0] : c.type === 'sticker' ? c.text.s : c.type === 'adjust' ? 'Ajuste' : (c.name || (m && m.name) || '');
    el.append(h('div', { class: 'lbl' }, (c.type === 'text' ? 'T ' : '') + label));
    if (c.speed !== 1) el.append(h('div', { class: 'badges' }, c.speed + 'x'));
    if (c.transIn) el.append(h('div', { class: 'tr', title: GC.TBYID[c.transIn.id].name }, '⋈'));
    el.append(h('div', { class: 'hd l', 'data-edge': 'l' }), h('div', { class: 'hd r', 'data-edge': 'r' }));
    el.addEventListener('pointerdown', e => clipDown(e, c, el));
    return el;
  }
  function movePlayhead() { const p = $('#playhead'); if (p) p.style.left = (HW + G.time * G.pps) + 'px'; }
  function scrub(e, lane) {
    const sc = $('#tlscroll'); const at = ev => { const r = lane.getBoundingClientRect(); G.seek(clamp((ev.clientX - r.left) / G.pps, 0, 1e5)); };
    at(e); const mv = ev => at(ev), up = () => { removeEventListener('pointermove', mv); removeEventListener('pointerup', up); };
    addEventListener('pointermove', mv); addEventListener('pointerup', up);
  }
  function snapPts(skipId) { const pts = [0, G.time]; G.project.clips.forEach(o => { if (o.id !== skipId) { pts.push(o.start, o.start + o.dur); } }); return pts; }
  function snapVal(v, pts, thr) { let best = v, bd = thr; pts.forEach(p => { const d = Math.abs(p - v); if (d < bd) { bd = d; best = p; } }); return best; }
  function clipDown(e, c, el) {
    if (e.button !== 0) return; e.stopPropagation();
    const tr = G.track(c.track); if (tr && tr.lock) { G.sel = c.id; G.emit('insp'); renderTL(); return; }
    const edge = e.target.dataset && e.target.dataset.edge, x0 = e.clientX, y0 = e.clientY, o = { start: c.start, dur: c.dur, in: c.in, track: c.track };
    const wasSel = G.sel === c.id; G.sel = c.id; G.emit('insp'); document.querySelectorAll('.clip.sel').forEach(n => n.classList.remove('sel')); el.classList.add('sel');
    const m = G.media.get(c.mediaId), maxSrc = (c.type === 'video' || c.type === 'audio') && m ? m.dur : Infinity, thr = 8 / G.pps; let moved = false, targetTid = c.track, tmpStart = c.start;
    const mv = ev => {
      const dx = (ev.clientX - x0) / G.pps; if (Math.abs(ev.clientX - x0) + Math.abs(ev.clientY - y0) > 3) moved = true; if (!moved) return;
      const pts = ui.magnet ? snapPts(c.id) : [];
      if (edge === 'l') {
        let ns = snapVal(o.start + dx, pts, thr); ns = Math.max(ns, 0); let d = ns - o.start;
        if (o.in + d * c.speed < 0) d = -o.in / c.speed; if (o.dur - d < .1) d = o.dur - .1;
        const prev = G.project.clips.filter(p => p.track === c.track && p.id !== c.id && p.start + p.dur <= o.start + 1e-6).reduce((mx, p) => Math.max(mx, p.start + p.dur), 0); if (o.start + d < prev) d = prev - o.start;
        c.start = o.start + d; c.dur = o.dur - d; c.in = o.in + d * c.speed;
      } else if (edge === 'r') {
        let ne = snapVal(o.start + o.dur + dx, pts, thr), nd = Math.max(.1, ne - o.start);
        if (isFinite(maxSrc)) nd = Math.min(nd, (maxSrc - c.in) / c.speed);
        const next = G.project.clips.filter(p => p.track === c.track && p.id !== c.id && p.start >= o.start + o.dur - 1e-6).reduce((mn, p) => Math.min(mn, p.start), Infinity); if (o.start + nd > next) nd = next - o.start;
        c.dur = nd;
      } else {
        let ns = o.start + dx; if (ui.magnet) { const a = snapVal(ns, pts, thr), b = snapVal(ns + c.dur, pts, thr) - c.dur; ns = Math.abs(a - ns) <= Math.abs(b - ns) ? a : b; }
        tmpStart = Math.max(0, ns);
        const under = document.elementsFromPoint(ev.clientX, ev.clientY).find(n => n.classList && n.classList.contains('lane') && n.dataset.tid);
        if (under) { const t2 = G.track(under.dataset.tid); if (t2 && t2.kind === G.track(o.track).kind && !t2.lock) targetTid = t2.id; }
        const rs = G.resolveStart(targetTid, c.id, tmpStart, c.dur); if (rs !== null) { tmpStart = rs; } else targetTid = o.track;
        el.style.left = tmpStart * G.pps + 'px'; el.style.opacity = .85;
        if (targetTid !== c.track) { const lane = document.querySelector(`.lane[data-tid="${targetTid}"]`); if (lane) lane.append(el); c.track = targetTid; }
        c.start = tmpStart; G.touch(); return;
      }
      el.style.left = c.start * G.pps + 'px'; el.style.width = Math.max(4, c.dur * G.pps) + 'px'; G.touch();
    };
    const up = () => {
      removeEventListener('pointermove', mv); removeEventListener('pointerup', up);
      if (moved) { if (!G.fits(c.track, c.id, c.start, c.dur)) { c.start = o.start; c.dur = o.dur; c.in = o.in; c.track = o.track; } G.emit('tl'); G.commit(); } else if (!wasSel) G.emit('tl');
      G.emit('insp'); libBodyRefreshIfNeeded();
    };
    addEventListener('pointermove', mv); addEventListener('pointerup', up);
  }
  const libBodyRefreshIfNeeded = () => { if (['effects', 'trans', 'filters', 'adjust'].includes(ui.libTab)) libBody(); };

  /* arrastrar desde la biblioteca a la línea de tiempo */
  function tlDrop() {
    const sc = $('#tlscroll');
    sc.addEventListener('dragover', e => { e.preventDefault(); });
    sc.addEventListener('drop', async e => {
      e.preventDefault();
      const r = $('#tlinner').getBoundingClientRect(), start = Math.max(0, (e.clientX - r.left - HW) / G.pps);
      const laneEl = document.elementsFromPoint(e.clientX, e.clientY).find(n => n.classList && n.classList.contains('lane') && n.dataset.tid), tid = laneEl && laneEl.dataset.tid;
      if (e.dataTransfer.files && e.dataTransfer.files.length) { const ms = await G.importFiles(e.dataTransfer.files); let t = start; ms.forEach(m => { G.addMediaClip(m, t, tid); t += m.type === 'image' ? 5 : m.dur; }); return; }
      const raw = e.dataTransfer.getData('application/x-ganchan'); if (!raw) return; const d = JSON.parse(raw);
      if (d.k === 'media') G.addMediaClip(G.media.get(d.id), start, tid); else if (d.k === 'sfx') G.addSfx(d.id, start);
      else if (d.k === 'text') G.addText(GC.TEXT_PRESETS.find(p => p.name === d.n), start); else if (d.k === 'sticker') G.addSticker(d.e, start);
    });
  }

  /* ============ Reproductor: selección en el lienzo ============ */
  function updateBox() {
    const b = $('#selbox'), c = G.selClip(), cv = G.canvas;
    if (!c || !c._box || !c._box.w || c.type === 'audio' || G.time < c.start || G.time >= c.start + c.dur) { b.classList.add('hidden'); return; }
    const f = cv.clientWidth / cv.width, B = c._box; b.classList.remove('hidden');
    b.style.cssText = `left:${(B.cx - B.w / 2) * f}px;top:${(B.cy - B.h / 2) * f}px;width:${B.w * f}px;height:${B.h * f}px;transform:rotate(${B.rot}rad)`;
  }
  function fitStage() {
    const st = $('#stage'), cv = G.canvas, pad = 20, aw = st.clientWidth - pad, ah = st.clientHeight - pad, r = cv.width / cv.height;
    let w = aw, hh = w / r; if (hh > ah) { hh = ah; w = hh * r; } cv.style.width = Math.max(50, w) + 'px'; cv.style.height = Math.max(30, hh) + 'px'; updateBox();
  }
  function stageEvents() {
    const cv = G.canvas, box = $('#selbox');
    const toCv = e => { const r = cv.getBoundingClientRect(), f = cv.width / r.width; return [(e.clientX - r.left) * f, (e.clientY - r.top) * f]; };
    const hit = (x, y) => {
      const vts = G.project.tracks.filter(t => t.kind === 'v');
      for (const tr of vts) { if (tr.hide || tr.lock) continue; for (const c of G.clipsOn(tr.id).reverse()) { if (G.time < c.start || G.time >= c.start + c.dur || !c._box || !c._box.w) continue; const B = c._box, dx = x - B.cx, dy = y - B.cy, cs = Math.cos(-B.rot), sn = Math.sin(-B.rot), lx = dx * cs - dy * sn, ly = dx * sn + dy * cs; if (Math.abs(lx) <= B.w / 2 && Math.abs(ly) <= B.h / 2) return c; } }
      return null;
    };
    cv.addEventListener('pointerdown', e => { const [x, y] = toCv(e), c = hit(x, y); G.sel = c ? c.id : null; G.emit('insp'); renderTL(); if (c) dragMove(e, c); });
    box.addEventListener('pointerdown', e => { const c = G.selClip(); if (!c) return; const hd = e.target.dataset && e.target.dataset.h; if (hd === 'scale') dragScale(e, c); else if (hd === 'rot') dragRot(e, c); else if (!e.target.classList.contains('h')) dragMove(e, c); e.preventDefault(); });
    box.style.pointerEvents = 'none'; box.querySelectorAll('.h').forEach(n => n.style.pointerEvents = 'auto');
    function drag(mv, e) { const up = () => { removeEventListener('pointermove', mv); removeEventListener('pointerup', up); G.commit(); G.emit('insp'); }; addEventListener('pointermove', mv); addEventListener('pointerup', up); }
    function dragMove(e, c) { const [x0, y0] = toCv(e), cx0 = c.x, cy0 = c.y; drag(ev => { const [x, y] = toCv(ev); c.x = cx0 + (x - x0) / cv.width; c.y = cy0 + (y - y0) / cv.height; if (Math.abs(c.x) < .008) c.x = 0; if (Math.abs(c.y) < .008) c.y = 0; G.touch(); G.save(); }, e); }
    function dragScale(e, c) { const B = c._box, d0 = Math.hypot(toCv(e)[0] - B.cx, toCv(e)[1] - B.cy), s0 = c.sc; drag(ev => { const [x, y] = toCv(ev); c.sc = clamp(s0 * Math.hypot(x - B.cx, y - B.cy) / d0, .05, 8); G.touch(); G.save(); }, e); }
    function dragRot(e, c) { const B = c._box, a0 = Math.atan2(toCv(e)[1] - B.cy, toCv(e)[0] - B.cx), r0 = c.rot; drag(ev => { const [x, y] = toCv(ev); let r = r0 + (Math.atan2(y - B.cy, x - B.cx) - a0) * 180 / Math.PI; r = ((r + 540) % 360) - 180; if (Math.abs(r) < 3) r = 0; c.rot = r; G.touch(); G.save(); }, e); }
  }

  /* ============ Menú, exportar, atajos ============ */
  const LAYOUTS = [['default', 'Predeterminado'], ['media', 'Archivos multimedia'], ['attr', 'Atributos'], ['vertical', 'Vertical']];
  function setLayout(l) { ui.layout = l; $('#work').className = 'lay-' + l; try { localStorage.setItem('ganchan.layout', l); } catch (e) { } setTimeout(() => { fitStage(); renderTL(); }, 30); }
  const copyClip = cut => { const c = G.selClip(); if (!c) return toast('Selecciona un clip'); ui.clipboard = JSON.parse(JSON.stringify(c)); if (cut) G.deleteClip(c.id); else toast('Copiado'); };
  const pasteClip = () => { if (!ui.clipboard) return; const n = JSON.parse(JSON.stringify(ui.clipboard)); n.id = G.uid(); n.transIn = null; G.placeClip(n, G.time); G.sel = n.id; G.touch(); G.emit('tl'); G.emit('insp'); G.commit(); };
  function menu() {
    const items = [
      ['Archivo', [['Nuevo proyecto', '', async () => { if (confirm('¿Empezar un proyecto nuevo? Se borra el actual.')) await G.reset(); }], ['Importar', '', () => $('#fileIn').click()], ['Exportar', 'Ctrl+E', openExport]]],
      ['Editar', [['Deshacer', 'Ctrl+Z', G.undo], ['Rehacer', 'Ctrl+Shift+Z', G.redo], ['Copiar', 'Ctrl+C', () => copyClip(false)], ['Cortar', 'Ctrl+X', () => copyClip(true)], ['Pegar', 'Ctrl+V', pasteClip, () => !ui.clipboard], ['Dividir', 'Ctrl+B', () => G.splitAtPlayhead()], ['Duplicar', 'Ctrl+D', () => G.sel && G.duplicate(G.sel)], ['Eliminar', 'Supr', () => delSel()]]],
      ['Diseño', [...LAYOUTS.map(([k, n]) => [n, '', () => setLayout(k), null, () => ui.layout === k]), ['Restablecer diseño actual', '', () => setLayout('media')]]],
      ['Más', [['Versión: Ganjan 0.2', '', () => { }, () => true]]],
      ['Ayuda', [['Atajos', '', shortcuts], ['Tutorial', '', tutorial], ['Acerca de', '', about]]],
      ['Configuración', [], settings],
    ];
    const m = $('#menu'); m.innerHTML = '';
    items.forEach(([name, sub, fn]) => {
      const row = h('div', { class: 'it sub' }, name, sub.length ? h('span', null, '›') : null);
      if (sub.length) { const pop = h('div', { class: 'menu subm hidden' }, sub.map(([n, k, f, dis, on]) => h('div', { class: 'it' + (dis && dis() ? ' dim' : ''), onclick: e => { e.stopPropagation(); if (dis && dis()) return; m.classList.add('hidden'); f(); } }, (on && on() ? '✓ ' : '') + n, h('kbd', null, k)))); row.append(pop); row.onmouseenter = () => { m.querySelectorAll('.subm').forEach(x => x.classList.add('hidden')); pop.classList.remove('hidden'); }; }
      else row.onclick = () => { m.classList.add('hidden'); fn(); };
      m.append(row);
    });
    m.append(h('div', { class: 'sep' }), h('div', { class: 'it', onclick: () => { m.classList.add('hidden'); location.reload(); } }, 'Volver a la página de inicio'));
  }
  const modal = n => ui.modal(n), closeModal = () => ui.closeModal();
  function about() { modal(h('div', null, h('h3', null, 'Ganjan'), h('div', { class: 'hint' }, 'Editor de video personal, hecho desde cero con la misma distribución que CapCut de escritorio. Funciona en el navegador y guarda tu trabajo automáticamente.'), h('div', { class: 'btnrow' }, h('button', { class: 'btn', onclick: closeModal }, 'Cerrar')))); }
  function tutorial() { modal(h('div', null, h('h3', null, 'Cómo empezar'), h('ol', { class: 'hint', style: 'padding-left:18px;line-height:1.7' }, [h('li', null, 'Importa tus videos en "Archivos multimedia".'), h('li', null, 'Haz clic en un archivo (o arrástralo a la línea de tiempo).'), h('li', null, 'Selecciona un clip y usa Filtros, Efectos, Transiciones y el panel derecho.'), h('li', null, 'Divide con Ctrl+B, elimina con Supr.'), h('li', null, 'Cuando termines pulsa Exportar.')]), h('div', { class: 'btnrow' }, h('button', { class: 'btn', onclick: closeModal }, 'Cerrar')))); }
  function settings() {
    modal(h('div', null, h('h3', null, 'Configuración'), h('div', { class: 'f' }, h('label', null, 'Calidad de la vista previa'), h('select', { onchange: e => { const q = { Baja: 640, Media: 960, Alta: 1280 }; G.quality = e.target.value; G.previewMax = q[G.quality]; $('#btnQuality').textContent = G.quality; G.applyCanvasSize(); } }, ['Baja', 'Media', 'Alta'].map(q => h('option', { selected: q === G.quality }, q)))),
      h('div', { class: 'f' }, h('label', null, 'Diseño de pantalla'), h('select', { onchange: e => setLayout(e.target.value) }, LAYOUTS.map(([k, n]) => h('option', { value: k, selected: k === ui.layout }, n)))), h('div', { class: 'btnrow' }, h('button', { class: 'btn', onclick: closeModal }, 'Cerrar'))));
  }
  function shortcuts() {
    modal(h('div', null, h('h3', null, 'Atajos de teclado'), ...[['Espacio', 'Reproducir / pausar'], ['Ctrl+B', 'Dividir en el cursor'], ['Q / W', 'Recortar izquierda / derecha'], ['Supr', 'Eliminar clip'], ['Ctrl+D', 'Duplicar'], ['Ctrl+Z / Ctrl+Shift+Z', 'Deshacer / Rehacer'], ['← →', 'Un fotograma (Shift = 1 s)'], ['Inicio / Fin', 'Ir al principio / final'], ['Ctrl + rueda', 'Zoom de la línea de tiempo']].map(([k, v]) => h('div', { class: 'f', style: 'display:flex;justify-content:space-between;margin-bottom:6px' }, h('b', null, k), v)), h('div', { class: 'btnrow' }, h('button', { class: 'btn', onclick: closeModal }, 'Cerrar'))));
  }
  function openExport() {
    if (!G.duration()) return toast('Añade algo a la línea de tiempo primero');
    const P = G.project; let res = Math.min(1080, P.res), fps = P.fps, br = 8;
    const nameIn = h('input', { type: 'text', value: P.name });
    const bar = h('i'), pct = h('div', { class: 'hint' }, ''), box = h('div', null);
    const opts = h('div', null, h('h3', null, 'Exportar'), h('div', { class: 'f' }, h('label', null, 'Nombre'), nameIn),
      h('div', { class: 'row2' }, h('div', { class: 'f' }, h('label', null, 'Resolución'), h('select', { onchange: e => res = +e.target.value }, [[480, '480p'], [720, '720p'], [1080, '1080p'], [1440, '2K'], [2160, '4K']].map(([v, n]) => h('option', { value: v, selected: v === res }, n)))),
        h('div', { class: 'f' }, h('label', null, 'Fotogramas'), h('select', { onchange: e => fps = +e.target.value }, [24, 25, 30, 50, 60].map(v => h('option', { value: v, selected: v === fps }, v + ' fps')))),
        h('div', { class: 'f' }, h('label', null, 'Calidad'), h('select', { onchange: e => br = +e.target.value }, [[4, 'Baja'], [8, 'Recomendada'], [16, 'Alta'], [30, 'Máxima']].map(([v, n]) => h('option', { value: v, selected: v === br }, n))))),
      h('div', { class: 'hint' }, 'La exportación se hace en tiempo real: dura lo mismo que tu video. Deja esta pestaña visible mientras exporta.'),
      h('div', { class: 'btnrow' }, h('button', { class: 'btn', onclick: closeModal }, 'Cancelar'), h('button', { class: 'btn-primary', onclick: go }, 'Exportar')));
    async function go() {
      P.name = nameIn.value || 'Ganjan'; $('#projName').value = P.name;
      box.append(h('h3', null, 'Exportando…'), h('div', { class: 'bar' }, bar), pct, h('div', { class: 'btnrow' }, h('button', { class: 'btn', onclick: () => G.exportCancel && G.exportCancel() }, 'Cancelar')));
      modal(box);
      try {
        const out = await G.exportVideo({ res, fps, bitrate: br * 1e6, onProgress: p => { bar.style.width = (p * 100).toFixed(1) + '%'; pct.textContent = Math.round(p * 100) + '%'; } });
        const url = URL.createObjectURL(out.blob), a = h('a', { href: url, download: `${P.name}.${out.ext}` }); document.body.append(a); a.click(); a.remove();
        modal(h('div', null, h('h3', null, '¡Listo!'), h('div', { class: 'hint' }, `Se descargó ${P.name}.${out.ext}`), h('div', { class: 'btnrow' }, h('button', { class: 'btn-primary', onclick: closeModal }, 'Cerrar'))));
      } catch (e) { closeModal(); if (e.message !== 'cancelado') toast('Error al exportar: ' + e.message); }
    }
    modal(opts);
  }
  $('#btnExport').onclick = openExport;
  $('#modal').addEventListener('pointerdown', e => { if (e.target.id === 'modal' && !G.exporting) closeModal(); });

  document.addEventListener('keydown', e => {
    const tg = e.target.tagName; if (tg === 'INPUT' && e.target.type !== 'range' && e.target.type !== 'checkbox' || tg === 'TEXTAREA' || tg === 'SELECT') return;
    const k = e.key.toLowerCase(), ctrl = e.ctrlKey || e.metaKey;
    if (k === ' ') { e.preventDefault(); G.toggle(); }
    else if (ctrl && k === 'z') { e.preventDefault(); e.shiftKey ? G.redo() : G.undo(); } else if (ctrl && k === 'y') { e.preventDefault(); G.redo(); }
    else if (ctrl && k === 'c') { e.preventDefault(); copyClip(false); } else if (ctrl && k === 'x') { e.preventDefault(); copyClip(true); } else if (ctrl && k === 'v') { e.preventDefault(); pasteClip(); } else if (ctrl && k === 'e') { e.preventDefault(); openExport(); }
    else if (ctrl && k === 'b') { e.preventDefault(); G.splitAtPlayhead(); } else if (ctrl && k === 'd') { e.preventDefault(); G.sel && G.duplicate(G.sel); }
    else if (k === 'delete' || k === 'backspace') { e.preventDefault(); delSel(); } else if (k === 'q') trimL(); else if (k === 'w') trimR();
    else if (k === 'arrowleft') { e.preventDefault(); G.seek(G.time - (e.shiftKey ? 1 : 1 / G.project.fps)); } else if (k === 'arrowright') { e.preventDefault(); G.seek(G.time + (e.shiftKey ? 1 : 1 / G.project.fps)); }
    else if (k === 'home') G.seek(0); else if (k === 'end') G.seek(G.duration());
  });

  /* ============ Arranque ============ */
  ui.magnet = true;
  const init = async () => {
    G.canvas = $('#cv'); toolbar(); libTabs(); stageEvents(); tlDrop(); menu(); try { setLayout(localStorage.getItem('ganchan.layout') || 'media'); } catch (e) { setLayout('media'); }
    $('#fileIn').onchange = async e => { const ms = await G.importFiles(e.target.files); e.target.value = ''; if (ms.length) toast(ms.length + ' archivo(s) importado(s)'); };
    $('#menuBtn').onclick = e => { e.stopPropagation(); $('#menu').classList.toggle('hidden'); }; document.addEventListener('click', () => $('#menu').classList.add('hidden'));
    $('#btnPlay').onclick = () => G.toggle();
    $('#btnFull').onclick = () => $('#stageInner').requestFullscreen && $('#stageInner').requestFullscreen();
    $('#btnQuality').onclick = e => ui.popMenu(e.currentTarget, [['Baja', 640], ['Media', 960], ['Alta', 1280]].map(([n, px]) => ({ label: n, on: G.quality === n, fn: () => { G.quality = n; G.previewMax = px; $('#btnQuality').textContent = n; G.applyCanvasSize(); } })), { up: true });
    $('#btnRatio').onclick = e => ui.popMenu(e.currentTarget, GC.RATIOS.map(r => ({ label: r.id, on: G.project.ratio === r.id, fn: () => { G.project.ratio = r.id; G.applyCanvasSize(); G.commit(); ui.inspector(); } })), { up: true });
    $('#projName').onchange = e => { G.project.name = e.target.value; G.commit(); };
    // arrastrar archivos a la biblioteca
    const lb = $('#libBody'); ['dragenter', 'dragover'].forEach(ev => lb.addEventListener(ev, e => { if ([...(e.dataTransfer.types || [])].includes('Files')) { e.preventDefault(); lb.classList.add('drop'); } }));
    ['dragleave', 'drop'].forEach(ev => lb.addEventListener(ev, e => { lb.classList.remove('drop'); if (ev === 'drop' && e.dataTransfer.files.length) { e.preventDefault(); G.importFiles(e.dataTransfer.files); } }));
    $('#tlscroll').addEventListener('wheel', e => { if (e.ctrlKey) { e.preventDefault(); setZoom(G.pps * (e.deltaY < 0 ? 1.15 : 1 / 1.15)); } }, { passive: false });
    G.on('tl', renderTL); G.on('insp', inspector); G.on('media', () => { if (['media', 'audio', 'stickers'].includes(ui.libTab)) libBody(); }); G.on('hist', syncHist);
    G.on('size', () => { fitStage(); $('#btnRatio').textContent = 'Relación'; });
    G.on('rendered', updateBox);
    G.on('saved', d => { $('#saved').innerHTML = '<i class="dotok">✓</i> Guardado automático: ' + d.toLocaleTimeString(); });
    G.on('play', () => { $('#btnPlay').textContent = G.playing ? '⏸' : '▶'; });
    G.on('time', () => { $('#tCur').textContent = fmt(G.time); movePlayhead(); if (G.playing) { const sc = $('#tlscroll'), x = HW + G.time * G.pps; if (x > sc.scrollLeft + sc.clientWidth - 40) sc.scrollLeft = x - HW - 40; } });
    addEventListener('resize', () => { fitStage(); renderTL(); });
    await G.init(G.canvas);
    $('#projName').value = G.project.name; $('#btnRatio').textContent = 'Relación'; $('#zoomR').value = zoomTo(G.pps);
    libBody(); fitStage(); renderTL(); inspector(); G.seek(0);
    window.addEventListener('beforeunload', () => { try { localStorage.getItem('x'); } catch (e) { } });
  };
  init();
})();
