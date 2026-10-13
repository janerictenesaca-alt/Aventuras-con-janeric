/* Ganjan - biblioteca (panel izquierdo): pestañas, barra lateral, búsqueda, favoritos */
(function () {
  const ui = G.ui, { $, h, fmtS, toast } = ui;
  const TABS = [['media', 'Archivos multimedia', '▶'], ['audio', 'Audio', '♫'], ['text', 'Texto', 'T'], ['stickers', 'Stickers', '☺'], ['effects', 'Efectos', '✦'],
    ['trans', 'Transiciones', '⋈'], ['subs', 'Subtítulos', '▤'], ['filters', 'Filtros', '◍'], ['adjust', 'Ajuste', '⚙'], ['tpl', 'Plantillas', '▦']];
  const dragData = d => e => { e.dataTransfer.setData('application/x-ganchan', JSON.stringify(d)); e.dataTransfer.effectAllowed = 'copy'; };
  const needTarget = () => { const c = G.targetClip(); if (!c) toast('Selecciona un clip en la línea de tiempo'); return c; };
  const applied = c => { G.touch(); G.emit('tl'); G.emit('insp'); G.commit(); return c; };
  const cur = tab => ui.libCat[tab];
  const isFav = k => G.favs.has(k);

  ui.libTabs = () => {
    const nav = $('#libTabs'); nav.innerHTML = '';
    TABS.forEach(([id, nm, ic]) => nav.append(h('button', { class: ui.libTab === id ? 'on' : '', title: nm, onclick: () => { ui.libTab = id; ui.libSearch = ''; ui.libTabs(); ui.libBody(); } }, h('span', { class: 'ic' }, ic), nm)));
  };

  /* barra lateral: [{id,label,action,group,children,note}] */
  function side(tab, spec, fallback) {
    const el = $('#libSide'); el.innerHTML = '';
    if (!ui.libCat[tab]) ui.libCat[tab] = fallback;
    spec.forEach(it => {
      if (it.children) {
        const open = ui.libOpen[tab + it.id] !== false;
        el.append(h('button', { class: 'grp' + (it.children.some(c => c.id === cur(tab)) ? ' on' : ''), onclick: () => { ui.libOpen[tab + it.id] = !open; ui.libBody(); } }, it.label, h('span', { class: 'chev' }, open ? '▴' : '▾')));
        if (open) it.children.forEach(ch => el.append(h('button', { class: 'leaf' + (cur(tab) === ch.id ? ' on' : ''), onclick: () => { ui.libCat[tab] = ch.id; ui.libBody(); } }, ch.label || ch.id)));
      } else el.append(h('button', { class: (cur(tab) === it.id && !it.action ? 'on' : '') + (it.disabled ? ' dis' : ''), title: it.note || '', onclick: () => { if (it.action) it.action(); else { ui.libCat[tab] = it.id; ui.libBody(); } } }, it.label));
    });
  }
  const leaves = arr => arr.map(x => typeof x === 'string' ? { id: x, label: x } : x);
  function header(ph) {
    const inp = h('input', { class: 'search', type: 'text', placeholder: ph, value: ui.libSearch, oninput: e => { ui.libSearch = e.target.value; clearTimeout(header._t); header._t = setTimeout(() => ui.libBody(true), 180); } });
    return h('div', { class: 'sbar' }, h('span', null, '⌕'), inp);
  }
  const match = n => !ui.libSearch || n.toLowerCase().includes(ui.libSearch.toLowerCase());
  const card = o => h('div', { class: 'card' + (o.on ? ' on' : ''), draggable: !!o.drag, ondragstart: o.drag && dragData(o.drag), onclick: o.click, title: o.name },
    o.thumb ? o.thumb : h('div', { class: 'th tcard', style: o.style || '' }, o.icon || ''),
    o.dur ? h('div', { class: 'dur' }, o.dur) : null,
    h('div', { class: 'nm' }, o.name),
    o.fav ? h('button', { class: 'star' + (isFav(o.fav) ? ' on' : ''), onclick: e => { e.stopPropagation(); G.toggleFav(o.fav); } }, isFav(o.fav) ? '★' : '☆') : null,
    o.add ? h('div', { class: 'add' }, '+') : null, o.del ? h('div', { class: 'del', onclick: e => { e.stopPropagation(); o.del(); } }, '✕') : null);

  ui.libBody = keepSide => {
    const body = $('#libBody'), scroll = body.scrollTop; body.innerHTML = '';
    const t = ui.libTab; $('#libFoot').innerHTML = '';
    const fn = BODY[t]; fn && fn(body, keepSide);
    body.scrollTop = scroll;
  };

  const sampleCache = {};
  function sampleCanvas(f) {
    if (!sampleCache.base) {
      const b = sampleCache.base = document.createElement('canvas'); b.width = 160; b.height = 100; const c = b.getContext('2d');
      let g = c.createLinearGradient(0, 0, 0, 100); g.addColorStop(0, '#5aa7ff'); g.addColorStop(.6, '#ffc78a'); g.addColorStop(1, '#2d5a2a'); c.fillStyle = g; c.fillRect(0, 0, 160, 100);
      c.fillStyle = '#ffe9a8'; c.beginPath(); c.arc(120, 28, 14, 0, 7); c.fill();
      c.fillStyle = '#2f7d3a'; c.beginPath(); c.moveTo(0, 100); c.lineTo(0, 70); c.quadraticCurveTo(50, 40, 100, 75); c.quadraticCurveTo(130, 60, 160, 72); c.lineTo(160, 100); c.fill();
      c.fillStyle = '#c0392b'; c.fillRect(40, 62, 22, 20); c.fillStyle = '#7d3c98'; c.fillRect(70, 66, 16, 16);
      c.fillStyle = '#f1c9a5'; c.beginPath(); c.arc(100, 56, 9, 0, 7); c.fill(); c.fillStyle = '#2c3e50'; c.fillRect(92, 64, 16, 22);
    }
    if (sampleCache[f.id]) return sampleCache[f.id];
    const cv = h('canvas', { width: 160, height: 100, style: 'width:100%;display:block' }), c = cv.getContext('2d');
    c.filter = GC.filterStr(f, 1, null, .15); c.drawImage(sampleCache.base, 0, 0); c.filter = 'none';
    GC.tintsOf(f, 1, null).forEach(t => GC.tintLayer(c, t[0], t[1], t[2], t[3], t[4]));
    return sampleCache[f.id] = cv;
  }

  const empty = (b, msg) => b.append(h('div', { class: 'empty' }, msg));
  function mediaCard(m) {
    return card({ name: m.name, thumb: h('div', { class: 'th', style: m.thumb ? `background-image:url(${m.thumb})` : '' }, m.thumb ? '' : '🎵'), dur: m.type !== 'image' ? fmtS(m.dur) : null, drag: { k: 'media', id: m.id }, click: () => G.addMediaClip(m), add: true,
      del: () => { if (confirm('¿Quitar este archivo y sus clips?')) G.removeMedia(m.id); } });
  }
  function audioRow(m) {
    const wave = h('div', { class: 'cover' }, '♫');
    return h('div', { class: 'arow', draggable: true, ondragstart: dragData({ k: 'media', id: m.id }), onclick: () => G.addMediaClip(m) }, wave, h('div', { class: 'meta' }, h('b', null, m.name), h('span', null, fmtS(m.dur))),
      h('button', { class: 'icon', title: 'Añadir', onclick: e => { e.stopPropagation(); G.addMediaClip(m); } }, '＋'),
      h('button', { class: 'icon', title: 'Quitar', onclick: e => { e.stopPropagation(); if (confirm('¿Quitar este audio?')) G.removeMedia(m.id); } }, '🗑'));
  }

  /* ---------- contenido de cada pestaña ---------- */
  const BODY = {
    media(b) {
      side('media', [{ id: 'imp', label: '⬆ Importar', action: () => $('#fileIn').click() }, { id: 'tuyos', label: 'Tuyos' }, { id: 'bib', label: 'Biblioteca', disabled: true, note: 'La biblioteca de CapCut tiene derechos de autor y no se copia' }], 'tuyos');
      b.append(header('Buscar en tus archivos'));
      const list = [...G.media.values()].filter(m => !m.sfx && match(m.name));
      if (!list.length) empty(b, ['Arrastra aquí tus videos, fotos o audios.', h('br'), h('br'), h('button', { class: 'btn', onclick: () => $('#fileIn').click() }, 'Importar archivos')]);
      else b.append(h('div', { class: 'grid' }, list.map(mediaCard)));
    },
    audio(b) {
      const sfxCats = ['Todos', ...new Set(Object.values(GC.SFX_CATS))];
      side('audio', [{ id: 'imp', label: '⬆ Importar', action: () => $('#fileIn').click() }, { id: 'tuyos', label: 'Tuyos' },
        { id: 'mus', label: 'Música', children: leaves(['Mi música']) }, { id: 'sfx', label: 'Efectos de sonido', children: leaves(sfxCats.map(c => ({ id: 'sfx:' + c, label: c }))) },
        { id: 'rec', label: '🎤 Grabar voz', action: () => ui.toggleRec() }], 'tuyos');
      b.append(header('Buscar audio'));
      const c = cur('audio');
      if (c && c.startsWith('sfx:')) {
        const cat = c.slice(4);
        b.append(h('div', { class: 'grid' }, GC.SFX.filter(s => (cat === 'Todos' || GC.SFX_CATS[s.id] === cat) && match(s.name)).map(s => card({ name: s.name, icon: '🔊', drag: { k: 'sfx', id: s.id }, click: () => G.addSfx(s.id), add: true }))));
      } else {
        if (c === 'Mi música') b.append(h('div', { class: 'hint' }, 'La música de CapCut tiene derechos de autor y no se puede copiar. Importa tus propias canciones: aparecen aquí.'));
        const list = [...G.media.values()].filter(m => m.type === 'audio' && !m.sfx && match(m.name));
        if (!list.length) empty(b, 'Aún no tienes audios. Pulsa Importar o grábate con 🎤.'); else list.forEach(m => b.append(audioRow(m)));
      }
    },
    text(b) {
      side('text', [{ id: 'add', label: 'Agregar texto', action: () => G.addText() },
        { id: 'pl', label: 'Plantilla de texto', children: leaves(GC.TEXT_CATS) }], GC.TEXT_CATS[0]);
      b.append(header('Buscar plantillas de texto'));
      const c = cur('text'), list = GC.TEXT_PRESETS.filter(p => (c === 'Tendencias' || p.cat === c || ui.libSearch) && match(p.name));
      b.append(h('div', { class: 'sec' }, c), h('div', { class: 'grid' }, list.map(p => card({ name: p.name, drag: { k: 'text', n: p.name }, click: () => G.addText(p), add: true, fav: 'text:' + p.name,
        style: `font-family:"${p.t.font}";font-weight:${p.t.bold ? 700 : 400};font-style:${p.t.italic ? 'italic' : 'normal'};color:${p.t.color};-webkit-text-stroke:${(p.t.strokeW || 0) / 5}px ${p.t.stroke || '#000'};${p.t.bg ? 'background:' + p.t.bg : ''};${p.t.shadow ? 'text-shadow:0 0 8px ' + p.t.shadow.c : ''}`, icon: 'Aa' }))));
    },
    stickers(b) {
      const cats = Object.keys(GC.STICKERS);
      side('stickers', [{ id: 'tuyos', label: 'Tuyos' }, { id: 'st', label: 'Stickers', children: leaves(['Tendencias', ...cats]) }], 'Tendencias');
      b.append(header('Buscar stickers'));
      const c = cur('stickers');
      if (c === 'tuyos') { const imgs = [...G.media.values()].filter(m => m.type === 'image' && match(m.name)); if (!imgs.length) empty(b, 'Importa imágenes y aparecerán aquí.'); else b.append(h('div', { class: 'grid' }, imgs.map(mediaCard))); return; }
      const all = c === 'Tendencias' || ui.libSearch ? cats : [c];
      all.forEach(cat => { b.append(h('div', { class: 'sec' }, cat), h('div', { class: 'emoji-grid' }, GC.STICKERS[cat].split(' ').map(e => h('button', { draggable: true, ondragstart: dragData({ k: 'sticker', e }), onclick: () => G.addSticker(e) }, e)))); });
    },
    effects(b) {
      side('effects', [{ id: 'fav', label: 'Favoritos' }, { id: 'fx', label: 'Efectos de video', children: leaves(['Tendencias', ...GC.FX_CATS]) },
        { id: 'body', label: 'Efectos corporales', disabled: true, note: 'Necesitan detectar personas con IA' }], 'Tendencias');
      b.append(header('Buscar efectos'), h('div', { class: 'hint' }, 'Clic para aplicar al clip seleccionado (o al de arriba bajo el cursor). Clic otra vez para quitarlo.'));
      const c = cur('effects'), c0 = G.targetClip();
      const list = GC.FX.filter(f => (c === 'fav' ? isFav('fx:' + f.id) : (c === 'Tendencias' || f.cat === c || ui.libSearch)) && match(f.name));
      if (!list.length) return empty(b, c === 'fav' ? 'Aún no hay favoritos. Marca ☆ en un efecto.' : 'Sin resultados');
      b.append(h('div', { class: 'grid' }, list.map(f => card({ name: f.name, icon: f.icon, fav: 'fx:' + f.id, on: c0 && c0.fx.some(x => x.id === f.id), click: () => { const cl = needTarget(); if (!cl) return; const i = cl.fx.findIndex(x => x.id === f.id); if (i >= 0) cl.fx.splice(i, 1); else cl.fx.push({ id: f.id, k: .6 }); applied(cl); ui.libBody(); } }))));
    },
    trans(b) {
      side('trans', [{ id: 'fav', label: 'Favoritos' }, { id: 'tr', label: 'Transiciones', children: leaves(['Tendencias', ...GC.TRANS_CATS]) }], 'Tendencias');
      b.append(header('Buscar transiciones'), h('div', { class: 'hint' }, 'Se aplica al inicio del clip, mezclándolo con el clip anterior de la misma pista.'));
      const c = cur('trans'), c0 = G.targetClip();
      const list = [{ id: '', name: 'Ninguna', icon: '🚫' }, ...GC.TRANS.filter(x => (c === 'fav' ? isFav('tr:' + x.id) : (c === 'Tendencias' || x.cat === c || ui.libSearch)))].filter(x => !x.id || match(x.name));
      b.append(h('div', { class: 'grid' }, list.map(x => card({ name: x.name, icon: x.icon, fav: x.id ? 'tr:' + x.id : null, on: c0 && ((c0.transIn && c0.transIn.id) || '') === x.id, click: () => { const cl = needTarget(); if (!cl) return; cl.transIn = x.id ? { id: x.id, dur: Math.min(ui.transDur || .6, cl.dur / 2) } : null; applied(cl); ui.libBody(); } }))));
      const foot = $('#libFoot'); foot.append(h('span', null, 'Duración'), h('input', { type: 'range', min: .1, max: 2, step: .05, value: ui.transDur || .6, oninput: e => { ui.transDur = +e.target.value; const cl = G.selClip(); if (cl && cl.transIn) { cl.transIn.dur = Math.min(ui.transDur, cl.dur); G.touch(); } } }));
    },
    subs(b) {
      side('subs', [{ id: 'auto', label: 'Subtítulos automáticos', disabled: true, note: 'Necesita reconocimiento de voz con IA', action: () => toast('Los subtítulos automáticos necesitan IA y no están disponibles') },
        { id: 'pl', label: 'Plantillas', children: leaves(GC.SUB_CATS) }, { id: 'add', label: 'Agregar subtítulos', action: subModal }], 'Tendencias');
      b.append(header('Buscar estilos de subtítulos'));
      const c = cur('subs'), list = GC.SUB_STYLES.filter(p => (c === 'Tendencias' || p.cat === c || ui.libSearch) && match(p.name));
      b.append(h('div', { class: 'sec' }, c), h('div', { class: 'grid' }, list.map(p => card({ name: p.name, icon: 'Hola', add: true, fav: 'sub:' + p.name, click: () => { const cl = G.addText({ t: p.t, y: .36 }); cl.sub = true; cl.text.s = 'Subtítulo de ejemplo'; G.emit('tl'); G.commit(); },
        style: `font-family:"${p.t.font}";font-weight:${p.t.bold ? 700 : 400};color:${p.t.color};-webkit-text-stroke:${(p.t.strokeW || 0) / 5}px ${p.t.stroke || '#000'};${p.t.bg ? 'background:' + p.t.bg : ''};font-size:20px` }))));
      $('#libFoot').append(h('button', { class: 'btn', onclick: () => { const subs = G.project.clips.filter(c => c.sub); if (!subs.length) return toast('No hay subtítulos'); subs.forEach(c => G.deleteClip(c.id, true)); G.touch(); G.emit('tl'); G.emit('insp'); G.commit(); } }, 'Eliminar los subtítulos actuales'),
        h('button', { class: 'btn dis', onclick: () => toast('Generar subtítulos necesita IA y no está disponible') }, 'Generar subtítulos'));
    },
    filters(b) {
      side('filters', [{ id: 'fav', label: 'Favoritos' }, { id: 'fl', label: 'Filtros', children: leaves(GC.FILTER_CATS) }], GC.FILTER_CATS[0]);
      b.append(header('Buscar filtros'));
      const c = cur('filters'), c0 = G.targetClip();
      const list = GC.FILTERS.filter(f => (c === 'fav' ? isFav('fl:' + f.id) : (f.cat === c || ui.libSearch)) && match(f.name));
      if (!list.length) return empty(b, c === 'fav' ? 'Aún no hay favoritos. Marca ☆ en un filtro.' : 'Sin resultados');
      b.append(h('div', { class: 'grid' }, list.map(f => card({ name: f.name, thumb: sampleCanvas(f).cloneNode ? cloneCanvas(sampleCanvas(f)) : null, fav: 'fl:' + f.id, on: c0 && ((c0.filter && c0.filter.id) || 'none') === f.id, click: () => { const cl = needTarget(); if (!cl) return; cl.filter = f.id === 'none' ? null : { id: f.id, k: 1 }; applied(cl); ui.libBody(true); } }))));
    },
    adjust(b) {
      side('adjust', [{ id: 'new', label: 'Agregar ajuste', action: () => G.addAdjust() }, { id: 'tuyos', label: 'Tuyos', children: leaves([{ id: 'pre', label: 'Valores predefinidos' }, { id: 'lut', label: 'LUT' }]) }], 'pre');
      const c = cur('adjust');
      if (c === 'lut') {
        b.append(h('div', { class: 'hint' }, 'LUT: archivos .cube (3D) con el color de un look. Impórtalos y aplícalos al clip seleccionado.'), h('button', { class: 'btn', onclick: pickLut }, '⬆ Importar LUT (.cube)'));
        const names = [...GC.LUTS.keys()];
        if (names.length) b.append(h('div', { class: 'sec' }, 'Tus LUT'), h('div', { class: 'grid' }, names.map(n => card({ name: n, icon: '🎞️', click: () => { const cl = needTarget(); if (!cl) return; cl.lut = { name: n, k: 1 }; applied(cl); } }))));
        return;
      }
      b.append(h('div', { class: 'hint' }, 'Un ajuste es una capa que cambia el color de todo lo que está debajo de ella.'),
        h('div', { class: 'grid' }, GC.ADJ_PRESETS.map(p => card({ name: p.name, icon: '🎚️', add: true, click: () => G.addAdjust(p) }))));
    },
    tpl(b) {
      side('tpl', [{ id: 'tuyos', label: 'Tuyos', children: leaves(['Favoritos', 'Comprado']) }, { id: 'pl', label: 'Plantillas', disabled: true, note: 'Las plantillas de CapCut no se copian' }], 'Favoritos');
      empty(b, 'Plantillas: pendiente. Aquí se podrán guardar tus propias plantillas de proyecto.');
    },
  };
  const cloneCanvas = c => { const n = h('canvas', { width: c.width, height: c.height, style: 'width:100%;display:block' }); n.getContext('2d').drawImage(c, 0, 0); return n; };

  function pickLut() { const i = h('input', { type: 'file', accept: '.cube' }); i.onchange = async () => { try { const n = await G.importLut(i.files[0]); toast('LUT importada: ' + n); ui.libBody(); } catch (e) { toast(e.message); } }; i.click(); }
  ui.pickLut = pickLut;

  function parseSrt(txt) {
    const out = [], ts = s => { const m = /(\d+):(\d+):(\d+)[,.](\d+)/.exec(s); return m ? +m[1] * 3600 + +m[2] * 60 + +m[3] + +m[4] / 1000 : 0; };
    txt.replace(/\r/g, '').split(/\n\n+/).forEach(bl => { const ln = bl.split('\n').filter(Boolean), i = ln.findIndex(l => l.includes('-->')); if (i < 0) return; const [a, b] = ln[i].split('-->'); const text = ln.slice(i + 1).join('\n'); if (text) out.push({ a: ts(a), b: ts(b), text }); });
    return out;
  }
  function subModal() {
    const ta = h('textarea', { placeholder: 'Escribe el subtítulo…' });
    ui.modal(h('div', null, h('h3', null, 'Agregar subtítulos'),
      h('div', { class: 'f' }, h('label', null, 'Subtítulo manual (se añade en la posición del cursor)'), ta, h('div', { class: 'btnrow' }, h('button', { class: 'btn', onclick: () => { if (!ta.value.trim()) return; const p = GC.SUB_STYLES[0], cl = G.addText({ t: p.t, y: .36 }); cl.sub = true; cl.text.s = ta.value; G.emit('tl'); G.commit(); ui.closeModal(); } }, 'Añadir'))),
      h('div', { class: 'f' }, h('label', null, 'Importar archivo .srt'), h('button', { class: 'btn', onclick: () => { const i = h('input', { type: 'file', accept: '.srt,.vtt' }); i.onchange = async () => { const cues = parseSrt(await i.files[0].text()); if (!cues.length) return toast('No se encontraron subtítulos'); const p = GC.SUB_STYLES[0]; cues.forEach(q => { const cl = G.mkClip('text', { dur: Math.max(.2, q.b - q.a), y: .36, sub: true, text: Object.assign({ s: q.text, font: 'Arial', size: 58, bold: false, italic: false, color: '#fff', stroke: '#000', strokeW: 0, shadow: null, bg: null, glow: false, spacing: 0 }, p.t, { s: q.text }) }); G.placeClip(cl, q.a); }); G.touch(); G.emit('tl'); G.commit(); ui.closeModal(); toast(cues.length + ' subtítulos importados'); }; i.click(); } }, '⬆ Elegir archivo')),
      h('div', { class: 'btnrow' }, h('button', { class: 'btn', onclick: ui.closeModal }, 'Cerrar'))));
  }

  let rec = null;
  ui.toggleRec = async () => {
    try {
      if (!rec) { rec = await G.recordVoice(); toast('Grabando… pulsa de nuevo 🎤 para detener'); $('#bMic') && $('#bMic').classList.add('on'); }
      else { const r = rec; rec = null; $('#bMic') && $('#bMic').classList.remove('on'); await r.stop(); toast('Grabación añadida'); }
    } catch (e) { rec = null; toast('No se pudo usar el micrófono'); }
  };
  G.on('favs', () => { if (['effects', 'trans', 'filters', 'text', 'subs'].includes(ui.libTab)) ui.libBody(); });
  G.on('luts', () => { if (ui.libTab === 'adjust') ui.libBody(); });
})();
