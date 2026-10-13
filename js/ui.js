/* Ganchan - interfaz (pestañas, línea de tiempo, inspector, interacción) */
(function () {
  const $ = s => document.querySelector(s);
  const clamp = G.clamp;
  const h = (tag, attrs, ...kids) => {
    const e = document.createElement(tag);
    for (const k in (attrs || {})) {
      const v = attrs[k]; if (v == null || v === false) continue;
      if (k === 'class') e.className = v; else if (k === 'style') e.style.cssText = v; else if (k.startsWith('on')) e.addEventListener(k.slice(2), v);
      else if (k === 'html') e.innerHTML = v; else e.setAttribute(k, v === true ? '' : v);
    }
    kids.flat().forEach(k => { if (k != null && k !== false) e.append(k.nodeType ? k : document.createTextNode(k)); });
    return e;
  };
  const ui = G.ui = { libTab: 'media', libCat: {}, insTab: null, animTab: 'in', mediaView: 'tuyos' };
  const fmt = t => { const fps = G.project.fps, f = Math.floor((t % 1) * fps + 1e-6), s = Math.floor(t) % 60, m = Math.floor(t / 60) % 60, hh = Math.floor(t / 3600), p = n => String(n).padStart(2, '0'); return `${p(hh)}:${p(m)}:${p(s)}:${p(f)}`; };
  const fmtS = t => { const m = Math.floor(t / 60), s = Math.floor(t % 60); return String(m).padStart(2, '0') + ':' + String(s).padStart(2, '0'); };
  const toast = (msg) => { const t = $('#toast'); t.textContent = msg; t.classList.remove('hidden'); clearTimeout(toast._t); toast._t = setTimeout(() => t.classList.add('hidden'), 2200); };
  ui.toast = toast;

  /* ============ Biblioteca (izquierda) ============ */
  const LIB = [
    ['media', '🎞️', 'Archivos multimedia'], ['audio', '🎵', 'Audio'], ['text', '🅣', 'Texto'], ['stickers', '😊', 'Stickers'],
    ['effects', '✨', 'Efectos'], ['trans', '⋈', 'Transiciones'], ['subs', '💬', 'Subtítulos'], ['filters', '🎨', 'Filtros'],
    ['adjust', '🎚️', 'Ajuste'], ['tpl', '🗂️', 'Plantillas'],
  ];
  function libTabs() {
    const nav = $('#libTabs'); nav.innerHTML = '';
    LIB.forEach(([id, ic, nm]) => nav.append(h('button', { class: ui.libTab === id ? 'on' : '', onclick: () => { ui.libTab = id; libTabs(); libBody(); } }, h('span', { class: 'ic' }, ic), nm)));
  }
  const needTarget = () => { const c = G.targetClip(); if (!c) toast('Selecciona un clip en la línea de tiempo'); return c; };
  const applied = c => { G.touch(); G.emit('tl'); G.emit('insp'); G.commit(); return c; };
  const dragData = d => e => { e.dataTransfer.setData('application/x-ganchan', JSON.stringify(d)); e.dataTransfer.effectAllowed = 'copy'; };
  const chipsFor = (cats, key) => { const cur = ui.libCat[key] || cats[0]; return h('div', { class: 'chips' }, cats.map(c => h('button', { class: c === cur ? 'on' : '', onclick: () => { ui.libCat[key] = c; libBody(); } }, c))); };

  function libBody() {
    const side = $('#libSide'), body = $('#libBody'); side.innerHTML = ''; body.innerHTML = '';
    const t = ui.libTab;
    if (t === 'media') {
      side.append(h('button', { class: 'on', onclick: () => $('#fileIn').click() }, '⬆ Importar'), h('button', { class: ui.mediaView === 'tuyos' ? 'on' : '' }, 'Tuyos'));
      const list = [...G.media.values()].filter(m => !m.sfx);
      if (!list.length) body.append(h('div', { class: 'empty' }, 'Arrastra aquí tus videos, fotos o audios', h('br'), h('br'), h('button', { class: 'btn', onclick: () => $('#fileIn').click() }, 'Importar archivos')));
      else body.append(h('div', { class: 'grid' }, list.map(m => mediaCard(m))));
    } else if (t === 'audio') {
      side.append(h('button', { class: 'on' }, 'Efectos de sonido'), h('button', { onclick: () => $('#fileIn').click() }, '⬆ Importar audio'), h('button', { onclick: toggleRec, id: 'recBtn' }, '🎤 Grabar voz'));
      body.append(h('div', { class: 'hint' }, 'Sonidos creados dentro de Ganchan. Clic para añadirlos en la posición del cursor.'),
        h('div', { class: 'grid' }, GC.SFX.map(s => h('div', { class: 'card', draggable: true, ondragstart: dragData({ k: 'sfx', id: s.id }), onclick: () => G.addSfx(s.id) }, h('div', { class: 'th tcard' }, '🔊'), h('div', { class: 'nm' }, s.name), h('div', { class: 'add' }, '+')))),
        h('div', { class: 'sec' }, 'Tus audios'), h('div', { class: 'grid' }, [...G.media.values()].filter(m => m.type === 'audio' && !m.sfx).map(m => mediaCard(m))));
    } else if (t === 'text') {
      side.append(h('button', { class: 'on', onclick: () => G.addText() }, '+ Añadir texto'));
      body.append(h('div', { class: 'grid' }, GC.TEXT_PRESETS.map(p => h('div', { class: 'card', draggable: true, ondragstart: dragData({ k: 'text', n: p.name }), onclick: () => G.addText(p) },
        h('div', { class: 'th tcard', style: `font-family:"${p.t.font}";font-weight:${p.t.bold ? 700 : 400};font-style:${p.t.italic ? 'italic' : 'normal'};color:${p.t.color};-webkit-text-stroke:${(p.t.strokeW || 0) / 5}px ${p.t.stroke};${p.t.bg ? 'background:' + p.t.bg : ''};${p.t.shadow ? 'text-shadow:0 0 8px ' + p.t.shadow.c : ''}` }, 'Aa'),
        h('div', { class: 'nm' }, p.name), h('div', { class: 'add' }, '+')))));
    } else if (t === 'stickers') {
      side.append(h('button', { class: 'on' }, 'Emoji'));
      Object.entries(GC.STICKERS).forEach(([cat, list]) => body.append(h('div', { class: 'sec' }, cat), h('div', { class: 'emoji-grid' }, list.split(' ').map(e => h('button', { draggable: true, ondragstart: dragData({ k: 'sticker', e }), onclick: () => G.addSticker(e) }, e)))));
    } else if (t === 'effects') {
      body.append(chipsFor(GC.FX_CATS, 'fx'), h('div', { class: 'hint' }, 'Clic para aplicar al clip seleccionado (o al que está bajo el cursor). Clic otra vez para quitarlo.'));
      const cur = ui.libCat.fx || GC.FX_CATS[0], c0 = G.targetClip();
      body.append(h('div', { class: 'grid' }, GC.FX.filter(f => f.cat === cur).map(f => h('div', { class: 'card' + (c0 && c0.fx.some(x => x.id === f.id) ? ' on' : ''), onclick: () => { const c = needTarget(); if (!c) return; const i = c.fx.findIndex(x => x.id === f.id); if (i >= 0) c.fx.splice(i, 1); else c.fx.push({ id: f.id, k: .6 }); applied(c); libBody(); } }, h('div', { class: 'th tcard' }, f.icon), h('div', { class: 'nm' }, f.name)))));
    } else if (t === 'trans') {
      body.append(chipsFor(['Todas', ...GC.TRANS_CATS], 'tr'), h('div', { class: 'hint' }, 'Se aplica al inicio del clip, mezclándolo con el clip anterior de la misma pista.'));
      const cur = ui.libCat.tr || 'Todas', c0 = G.targetClip();
      body.append(h('div', { class: 'grid' }, [{ id: '', name: 'Ninguna', icon: '🚫' }, ...GC.TRANS.filter(x => cur === 'Todas' || x.cat === cur)].map(x => h('div', { class: 'card' + (c0 && ((c0.transIn && c0.transIn.id) || '') === x.id ? ' on' : ''), onclick: () => { const c = needTarget(); if (!c) return; c.transIn = x.id ? { id: x.id, dur: Math.min(.8, c.dur / 2) } : null; applied(c); libBody(); } }, h('div', { class: 'th tcard' }, x.icon), h('div', { class: 'nm' }, x.name)))));
    } else if (t === 'subs') {
      side.append(h('button', { class: 'on' }, 'Manual'));
      body.append(h('div', { class: 'hint' }, 'Añade un subtítulo en la posición del cursor. (Los subtítulos automáticos con IA no están disponibles.)'), h('button', { class: 'btn', onclick: () => G.addText(GC.TEXT_PRESETS.find(p => p.name === 'Subtítulo')) }, '+ Nuevo subtítulo'));
    } else if (t === 'filters') {
      body.append(chipsFor(GC.FILTER_CATS, 'fl'));
      const cur = ui.libCat.fl || GC.FILTER_CATS[0], c0 = G.targetClip();
      body.append(h('div', { class: 'grid' }, GC.FILTERS.filter(f => f.cat === cur).map(f => {
        const cv = h('canvas', { width: 160, height: 100, style: 'width:100%;display:block' }); drawSample(cv, f);
        return h('div', { class: 'card' + (c0 && ((c0.filter && c0.filter.id) || 'none') === f.id ? ' on' : ''), onclick: () => { const c = needTarget(); if (!c) return; c.filter = f.id === 'none' ? null : { id: f.id, k: 1 }; applied(c); libBody(); } }, cv, h('div', { class: 'nm' }, f.name));
      })));
    } else if (t === 'adjust') {
      const c = G.targetClip(); body.append(h('div', { class: 'hint' }, 'Ajustes manuales del clip seleccionado.'));
      if (c) adjustPanel(body, c); else body.append(h('div', { class: 'empty' }, 'Selecciona un clip'));
    } else if (t === 'tpl') body.append(h('div', { class: 'empty' }, 'Plantillas: pendiente.', h('br'), 'Cuando me pases capturas las armamos.'));
  }
  function mediaCard(m) {
    return h('div', { class: 'card', draggable: true, ondragstart: dragData({ k: 'media', id: m.id }), onclick: () => G.addMediaClip(m) },
      h('div', { class: 'th', style: m.thumb ? `background-image:url(${m.thumb})` : '' }, m.thumb ? '' : '🎵'),
      m.type !== 'image' ? h('div', { class: 'dur' }, fmtS(m.dur)) : null, h('div', { class: 'nm' }, m.name), h('div', { class: 'add' }, '+'),
      h('div', { class: 'del', title: 'Quitar de la biblioteca', onclick: e => { e.stopPropagation(); if (confirm('¿Quitar este archivo y sus clips?')) G.removeMedia(m.id); } }, '✕'));
  }
  let sampleImg = null;
  function drawSample(cv, f) {
    if (!sampleImg) {
      sampleImg = document.createElement('canvas'); sampleImg.width = 160; sampleImg.height = 100; const c = sampleImg.getContext('2d');
      let g = c.createLinearGradient(0, 0, 0, 100); g.addColorStop(0, '#5aa7ff'); g.addColorStop(.6, '#ffc78a'); g.addColorStop(1, '#2d5a2a'); c.fillStyle = g; c.fillRect(0, 0, 160, 100);
      c.fillStyle = '#ffe9a8'; c.beginPath(); c.arc(120, 28, 14, 0, 7); c.fill();
      c.fillStyle = '#2f7d3a'; c.beginPath(); c.moveTo(0, 100); c.lineTo(0, 70); c.quadraticCurveTo(50, 40, 100, 75); c.quadraticCurveTo(130, 60, 160, 72); c.lineTo(160, 100); c.fill();
      c.fillStyle = '#c0392b'; c.fillRect(40, 62, 22, 20); c.fillStyle = '#7d3c98'; c.fillRect(70, 66, 16, 16);
    }
    const c = cv.getContext('2d'); c.filter = GC.filterStr(f, 1, null, .15); c.drawImage(sampleImg, 0, 0); c.filter = 'none';
    GC.tintsOf(f, 1, null).forEach(t => GC.tintLayer(c, t[0], t[1], t[2], t[3], t[4]));
  }
  let rec = null;
  async function toggleRec() {
    const b = $('#recBtn');
    try {
      if (!rec) { rec = await G.recordVoice(); b.textContent = '⏹ Detener grabación'; b.classList.add('on'); }
      else { const r = rec; rec = null; b.textContent = '🎤 Grabar voz'; b.classList.remove('on'); await r.stop(); toast('Grabación añadida'); }
    } catch (e) { rec = null; toast('No se pudo usar el micrófono'); }
  }

  /* ============ Inspector (derecha) ============ */
  function sl(label, val, min, max, step, onIn, unit = '', opts = {}) {
    const num = h('input', { class: 'num', type: 'number', min, max, step, value: +(+val).toFixed(2) }), rng = h('input', { type: 'range', min, max, step, value: val });
    const set = v => { v = clamp(+v, min, max); num.value = +v.toFixed(2); rng.value = v; onIn(v); G.touch(); G.save(); };
    rng.addEventListener('input', () => set(rng.value)); rng.addEventListener('change', () => { G.commit(); opts.after && opts.after(); });
    num.addEventListener('change', () => { set(num.value); G.commit(); opts.after && opts.after(); });
    return h('div', { class: 'f' }, h('div', { class: 'lab' }, h('span', null, label), h('span', null, num, unit)), rng);
  }
  const sel = (label, val, opts, onChange) => h('div', { class: 'f' }, h('label', null, label), h('select', { onchange: e => { onChange(e.target.value); G.touch(); G.commit(); } }, opts.map(([v, n]) => h('option', { value: v, selected: v === val }, n))));

  function adjustPanel(host, c) {
    GC.ADJ.forEach(([k, n]) => { const pos = ['vignette', 'grain', 'blur'].includes(k); host.append(sl(n, c.adj[k] || 0, pos ? 0 : -100, 100, 1, v => { c.adj[k] = v; })); });
    if (c.filter) host.append(sl('Intensidad del filtro (' + GC.FBYID[c.filter.id].name + ')', Math.round(c.filter.k * 100), 0, 100, 1, v => { c.filter.k = v / 100; }, '%'));
    host.append(h('button', { class: 'btn', onclick: () => { c.adj = {}; G.touch(); G.commit(); G.emit('insp'); libBody(); } }, 'Restablecer'));
  }

  function inspector() {
    const c = G.selClip(), tabs = $('#inspTabs'), body = $('#inspBody'); tabs.innerHTML = ''; body.innerHTML = '';
    $('#playerTitle').textContent = 'Reproductor';
    if (!c) {
      tabs.append(h('button', { class: 'on' }, 'Detalles')); const P = G.project;
      body.append(h('div', { class: 'f' }, h('label', null, 'Relación de aspecto'), h('select', { onchange: e => { P.ratio = e.target.value; G.applyCanvasSize(); G.commit(); G.emit('size'); } }, GC.RATIOS.map(r => h('option', { value: r.id, selected: r.id === P.ratio }, r.id)))),
        h('div', { class: 'f' }, h('label', null, 'Color de fondo'), h('input', { type: 'color', value: P.bg, oninput: e => { P.bg = e.target.value; G.touch(); }, onchange: () => G.commit() })),
        h('div', { class: 'f' }, h('label', null, 'Fotogramas por segundo'), h('select', { onchange: e => { P.fps = +e.target.value; G.commit(); } }, [24, 25, 30, 50, 60].map(f => h('option', { value: f, selected: f === P.fps }, f + ' fps')))),
        h('div', { class: 'hint' }, 'Selecciona un clip en la línea de tiempo para editar sus propiedades.'));
      return;
    }
    const map = { video: ['Video', 'Audio', 'Velocidad', 'Animación', 'Ajustar'], image: ['Video', 'Animación', 'Ajustar'], text: ['Texto', 'Animación', 'Ajustar'], sticker: ['Video', 'Animación', 'Ajustar'], audio: ['Audio', 'Velocidad'] };
    const list = map[c.type]; if (!list.includes(ui.insTab)) ui.insTab = list[0];
    list.forEach(n => tabs.append(h('button', { class: n === ui.insTab ? 'on' : '', onclick: () => { ui.insTab = n; inspector(); } }, n)));
    const T = ui.insTab;
    if (T === 'Video') basicTab(body, c);
    else if (T === 'Texto') textTab(body, c);
    else if (T === 'Audio') audioTab(body, c);
    else if (T === 'Velocidad') speedTab(body, c);
    else if (T === 'Animación') animTab(body, c);
    else if (T === 'Ajustar') adjustPanel(body, c);
  }
  function basicTab(b, c) {
    b.append(h('div', { class: 'sec' }, 'Transformar'),
      h('div', { class: 'row2' }, sl('Posición X', +(c.x * 100).toFixed(1), -100, 100, .5, v => c.x = v / 100, '%'), sl('Posición Y', +(c.y * 100).toFixed(1), -100, 100, .5, v => c.y = v / 100, '%')),
      sl('Escala', Math.round(c.sc * 100), 5, 500, 1, v => c.sc = v / 100, '%'), sl('Rotación', Math.round(c.rot), -180, 180, 1, v => c.rot = v, '°'),
      sl('Opacidad', Math.round(c.op * 100), 0, 100, 1, v => c.op = v / 100, '%'),
      h('div', { class: 'f btnrow' }, h('button', { class: 'btn' + (c.flipH ? ' on' : ''), onclick: () => { c.flipH = !c.flipH; G.touch(); G.commit(); inspector(); } }, '⇋ Voltear H'), h('button', { class: 'btn' + (c.flipV ? ' on' : ''), onclick: () => { c.flipV = !c.flipV; G.touch(); G.commit(); inspector(); } }, '⇅ Voltear V'), h('button', { class: 'btn', onclick: () => { Object.assign(c, { x: 0, y: 0, sc: 1, rot: 0, op: 1 }); G.touch(); G.commit(); inspector(); } }, 'Restablecer')),
      sel('Mezcla', c.blend, GC.BLENDS, v => c.blend = v));
    if (c.type === 'video' || c.type === 'image') {
      b.append(sel('Máscara', c.mask ? c.mask.t : '', GC.MASKS, v => { c.mask = v ? { t: v, s: c.mask ? c.mask.s : 1 } : null; inspector(); }));
      if (c.mask) b.append(sl('Tamaño de máscara', Math.round(c.mask.s * 100), 10, 200, 1, v => c.mask.s = v / 100, '%'));
    }
    const sets = [];
    c.fx.forEach((f, i) => sets.push(h('div', { class: 'f' }, h('div', { class: 'tag' }, h('b', null, '✨ ' + GC.FXBYID[f.id].name), h('button', { class: 'btn danger', onclick: () => { c.fx.splice(i, 1); applied(c); libBody(); } }, '✕')), sl('Intensidad', Math.round(f.k * 100), 0, 100, 1, v => f.k = v / 100, '%'))));
    if (c.filter) sets.push(h('div', { class: 'tag' }, h('b', null, '🎨 ' + GC.FBYID[c.filter.id].name), h('button', { class: 'btn danger', onclick: () => { c.filter = null; applied(c); libBody(); } }, '✕')));
    if (c.transIn) sets.push(h('div', { class: 'f' }, h('div', { class: 'tag' }, h('b', null, '⋈ ' + GC.TBYID[c.transIn.id].name), h('button', { class: 'btn danger', onclick: () => { c.transIn = null; applied(c); libBody(); } }, '✕')), sl('Duración de la transición', +c.transIn.dur.toFixed(2), .1, Math.max(.2, +c.dur.toFixed(2)), .05, v => c.transIn.dur = v, ' s')));
    if (sets.length) b.append(h('div', { class: 'sec' }, 'Aplicado'), sets);
  }
  function textTab(b, c) {
    const T = c.text;
    b.append(h('div', { class: 'f' }, h('label', null, 'Texto'), h('textarea', { oninput: e => { T.s = e.target.value; G.touch(); G.save(); }, onchange: () => G.commit() }, T.s)),
      h('div', { class: 'f' }, h('label', null, 'Fuente'), h('select', { onchange: e => { T.font = e.target.value; document.fonts && document.fonts.load(`20px "${T.font}"`).then(G.touch); G.touch(); G.commit(); } }, GC.FONTS.map(f => h('option', { value: f, selected: f === T.font, style: `font-family:"${f}"` }, f)))),
      sl('Tamaño', T.size, 10, 400, 1, v => T.size = v),
      h('div', { class: 'f btnrow' }, h('button', { class: 'btn' + (T.bold ? ' on' : ''), onclick: () => { T.bold = !T.bold; G.touch(); G.commit(); inspector(); } }, 'N'), h('button', { class: 'btn' + (T.italic ? ' on' : ''), onclick: () => { T.italic = !T.italic; G.touch(); G.commit(); inspector(); } }, 'K')),
      h('div', { class: 'row2' }, h('div', { class: 'f' }, h('label', null, 'Color'), h('input', { type: 'color', value: T.color, oninput: e => { T.color = e.target.value; G.touch(); }, onchange: () => G.commit() })),
        h('div', { class: 'f' }, h('label', null, 'Contorno'), h('input', { type: 'color', value: T.stroke || '#000000', oninput: e => { T.stroke = e.target.value; G.touch(); }, onchange: () => G.commit() }))),
      sl('Grosor del contorno', T.strokeW || 0, 0, 40, 1, v => T.strokeW = v), sl('Espaciado de letras', T.spacing || 0, -5, 40, 1, v => T.spacing = v),
      h('div', { class: 'f ck' }, h('input', { type: 'checkbox', checked: !!T.shadow, onchange: e => { T.shadow = e.target.checked ? { c: 'rgba(0,0,0,.7)', b: 10, x: 0, y: 4 } : null; G.touch(); G.commit(); } }), 'Sombra'),
      h('div', { class: 'f ck' }, h('input', { type: 'checkbox', checked: !!T.bg, onchange: e => { T.bg = e.target.checked ? 'rgba(0,0,0,.65)' : null; G.touch(); G.commit(); inspector(); } }), 'Fondo'));
    b.append(h('div', { class: 'sec' }, 'Posición'), h('div', { class: 'row2' }, sl('X', +(c.x * 100).toFixed(1), -100, 100, .5, v => c.x = v / 100, '%'), sl('Y', +(c.y * 100).toFixed(1), -100, 100, .5, v => c.y = v / 100, '%')), sl('Escala', Math.round(c.sc * 100), 5, 500, 1, v => c.sc = v / 100, '%'), sl('Rotación', Math.round(c.rot), -180, 180, 1, v => c.rot = v, '°'), sl('Opacidad', Math.round(c.op * 100), 0, 100, 1, v => c.op = v / 100, '%'));
  }
  function audioTab(b, c) {
    b.append(sl('Volumen', Math.round(c.vol * 100), 0, 200, 1, v => c.vol = v / 100, '%'),
      sl('Fundido de entrada', c.fadeIn, 0, Math.min(10, c.dur), .1, v => c.fadeIn = v, ' s'), sl('Fundido de salida', c.fadeOut, 0, Math.min(10, c.dur), .1, v => c.fadeOut = v, ' s'));
  }
  function speedTab(b, c) {
    b.append(sl('Velocidad', c.speed, .1, 10, .1, v => { G.setSpeed(c, v); G.emit('tl'); }, 'x'),
      h('div', { class: 'f btnrow' }, [.5, 1, 1.5, 2, 4].map(v => h('button', { class: 'btn' + (c.speed === v ? ' on' : ''), onclick: () => { if (!G.setSpeed(c, v)) toast('No hay espacio libre en la pista'); G.touch(); G.emit('tl'); G.commit(); inspector(); } }, v + 'x'))),
      h('div', { class: 'hint' }, 'Duración: ' + c.dur.toFixed(2) + ' s'));
  }
  function animTab(b, c) {
    const tabs = [['in', 'Entrada'], ['out', 'Salida'], ['loop', 'Combo']];
    b.append(h('div', { class: 'chips' }, tabs.map(([k, n]) => h('button', { class: ui.animTab === k ? 'on' : '', onclick: () => { ui.animTab = k; inspector(); } }, n))));
    const key = { in: 'animIn', out: 'animOut', loop: 'animLoop' }[ui.animTab], list = ui.animTab === 'loop' ? GC.ANIM_COMBO : GC.ANIM_IO.filter(a => !a.text || c.type === 'text');
    b.append(h('div', { class: 'grid' }, [{ id: '', name: 'Ninguna' }, ...list].map(a => h('div', { class: 'card' + (((c[key] && c[key].id) || '') === a.id ? ' on' : ''), onclick: () => { c[key] = a.id ? (ui.animTab === 'loop' ? { id: a.id, speed: 1 } : { id: a.id, dur: Math.min(1, c.dur / 2) }) : null; G.touch(); G.commit(); inspector(); } }, h('div', { class: 'th tcard', style: 'font-size:15px;min-height:46px' }, a.name)))));
    if (c[key]) b.append(h('div', { style: 'margin-top:14px' }), ui.animTab === 'loop' ? sl('Velocidad', c[key].speed || 1, .2, 4, .1, v => c[key].speed = v, 'x') : sl('Duración', +c[key].dur.toFixed(2), .1, Math.max(.2, c.dur), .05, v => c[key].dur = v, ' s'));
  }

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
      h('span', { class: 'sep' }), tb('🎤', 'Grabar voz', () => { ui.libTab = 'audio'; libTabs(); libBody(); toggleRec(); }),
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
        h('button', { class: tr.mute ? '' : 'on', title: 'Silenciar pista', onclick: () => { tr.mute = !tr.mute; G.touch(); G.commit(); renderTL(); } }, tr.mute ? '🔇' : '🔊'));
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
    const label = c.type === 'text' ? (c.text.s || '').split('\n')[0] : c.type === 'sticker' ? c.text.s : (c.name || (m && m.name) || '');
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
  function menu() {
    const items = [['Nuevo proyecto', '', async () => { if (confirm('¿Empezar un proyecto nuevo? Se borra el actual.')) await G.reset(); }], ['Importar archivos…', '', () => $('#fileIn').click()], ['Exportar…', '', openExport], '-',
      ['Deshacer', 'Ctrl+Z', G.undo], ['Rehacer', 'Ctrl+Shift+Z', G.redo], ['Dividir', 'Ctrl+B', () => G.splitAtPlayhead()], ['Duplicar', 'Ctrl+D', () => G.sel && G.duplicate(G.sel)], ['Eliminar', 'Supr', delSel], '-',
      ['Atajos de teclado', '', shortcuts]];
    const m = $('#menu'); m.innerHTML = '';
    items.forEach(it => it === '-' ? m.append(h('div', { class: 'sep' })) : m.append(h('div', { class: 'it', onclick: () => { m.classList.add('hidden'); it[2](); } }, it[0], h('kbd', null, it[1]))));
  }
  const modal = (node) => { const m = $('#modal'); $('#modalBox').innerHTML = ''; $('#modalBox').append(node); m.classList.remove('hidden'); };
  const closeModal = () => $('#modal').classList.add('hidden');
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
      P.name = nameIn.value || 'Ganchan'; $('#projName').value = P.name;
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
    else if (ctrl && k === 'b') { e.preventDefault(); G.splitAtPlayhead(); } else if (ctrl && k === 'd') { e.preventDefault(); G.sel && G.duplicate(G.sel); }
    else if (k === 'delete' || k === 'backspace') { e.preventDefault(); delSel(); } else if (k === 'q') trimL(); else if (k === 'w') trimR();
    else if (k === 'arrowleft') { e.preventDefault(); G.seek(G.time - (e.shiftKey ? 1 : 1 / G.project.fps)); } else if (k === 'arrowright') { e.preventDefault(); G.seek(G.time + (e.shiftKey ? 1 : 1 / G.project.fps)); }
    else if (k === 'home') G.seek(0); else if (k === 'end') G.seek(G.duration());
  });

  /* ============ Arranque ============ */
  ui.magnet = true;
  const init = async () => {
    G.canvas = $('#cv'); toolbar(); libTabs(); stageEvents(); tlDrop(); menu();
    $('#fileIn').onchange = async e => { const ms = await G.importFiles(e.target.files); e.target.value = ''; if (ms.length) toast(ms.length + ' archivo(s) importado(s)'); };
    $('#menuBtn').onclick = e => { e.stopPropagation(); $('#menu').classList.toggle('hidden'); }; document.addEventListener('click', () => $('#menu').classList.add('hidden'));
    $('#btnPlay').onclick = () => G.toggle();
    $('#btnFull').onclick = () => $('#stageInner').requestFullscreen && $('#stageInner').requestFullscreen();
    $('#btnQuality').onclick = () => { const q = [['Baja', 640], ['Media', 960], ['Alta', 1280]]; const i = (q.findIndex(x => x[0] === G.quality) + 1) % q.length; G.quality = q[i][0]; G.previewMax = q[i][1]; $('#btnQuality').textContent = G.quality; G.applyCanvasSize(); };
    $('#btnRatio').onclick = () => { const P = G.project, i = (GC.RATIOS.findIndex(r => r.id === P.ratio) + 1) % GC.RATIOS.length; P.ratio = GC.RATIOS[i].id; G.applyCanvasSize(); G.commit(); };
    $('#projName').onchange = e => { G.project.name = e.target.value; G.commit(); };
    // arrastrar archivos a la biblioteca
    const lb = $('#libBody'); ['dragenter', 'dragover'].forEach(ev => lb.addEventListener(ev, e => { if ([...(e.dataTransfer.types || [])].includes('Files')) { e.preventDefault(); lb.classList.add('drop'); } }));
    ['dragleave', 'drop'].forEach(ev => lb.addEventListener(ev, e => { lb.classList.remove('drop'); if (ev === 'drop' && e.dataTransfer.files.length) { e.preventDefault(); G.importFiles(e.dataTransfer.files); } }));
    $('#tlscroll').addEventListener('wheel', e => { if (e.ctrlKey) { e.preventDefault(); setZoom(G.pps * (e.deltaY < 0 ? 1.15 : 1 / 1.15)); } }, { passive: false });
    G.on('tl', renderTL); G.on('insp', inspector); G.on('media', libBody); G.on('hist', syncHist);
    G.on('size', () => { fitStage(); $('#btnRatio').textContent = G.project.ratio; });
    G.on('rendered', updateBox);
    G.on('saved', d => { $('#saved').textContent = '● Guardado ' + d.toLocaleTimeString(); });
    G.on('play', () => { $('#btnPlay').textContent = G.playing ? '⏸' : '▶'; });
    G.on('time', () => { $('#tCur').textContent = fmt(G.time); movePlayhead(); if (G.playing) { const sc = $('#tlscroll'), x = HW + G.time * G.pps; if (x > sc.scrollLeft + sc.clientWidth - 40) sc.scrollLeft = x - HW - 40; } });
    addEventListener('resize', () => { fitStage(); renderTL(); });
    await G.init(G.canvas);
    $('#projName').value = G.project.name; $('#btnRatio').textContent = G.project.ratio; $('#zoomR').value = zoomTo(G.pps);
    libBody(); fitStage(); renderTL(); inspector(); G.seek(0);
    window.addEventListener('beforeunload', () => { try { localStorage.getItem('x'); } catch (e) { } });
  };
  init();
})();
