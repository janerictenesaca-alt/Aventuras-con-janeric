/* Ganjan - inspector (panel derecho) */
(function () {
  const ui = G.ui, { $, h, toast, sl, sel, sw, section, seg } = ui, clamp = G.clamp;
  const commit = () => { G.touch(); G.commit(); };
  const redo = () => { commit(); ui.inspector(); };
  const dims = () => GC.sizeFor(G.project.ratio, G.project.res);

  const SPEC = {
    video: [['Video', ['Básico', 'Eliminar fondo', 'Máscara']], ['Audio', ['Básico', 'Modificador de voz']], ['Velocidad', ['Estándar', 'Curva']], ['Animación', null], ['Ajustar', ['Básico', 'HSL', 'Curvas', 'Círculo cromático']]],
    image: [['Video', ['Básico', 'Eliminar fondo', 'Máscara']], ['Animación', null], ['Ajustar', ['Básico', 'HSL', 'Curvas', 'Círculo cromático']]],
    text: [['Texto', null], ['Animación', null], ['Ajustar', ['Básico', 'HSL', 'Curvas', 'Círculo cromático']]],
    sticker: [['Video', ['Básico']], ['Animación', null], ['Ajustar', ['Básico', 'HSL', 'Curvas', 'Círculo cromático']]],
    audio: [['Audio', ['Básico', 'Modificador de voz']], ['Velocidad', ['Estándar']]],
    adjust: [['Ajustar', ['Básico', 'HSL', 'Curvas', 'Círculo cromático']]],
  };

  ui.inspector = () => {
    const c = G.selClip(), tabs = $('#inspTabs'), body = $('#inspBody'); tabs.innerHTML = ''; body.innerHTML = '';
    if (!c) return details(tabs, body);
    const spec = SPEC[c.type]; if (!spec.some(s => s[0] === ui.insTab)) ui.insTab = spec[0][0];
    spec.forEach(([n]) => tabs.append(h('button', { class: n === ui.insTab ? 'on' : '', onclick: () => { ui.insTab = n; ui.inspector(); } }, n)));
    const subs = spec.find(s => s[0] === ui.insTab)[1]; let sub = null;
    if (subs) { sub = ui.insSub[ui.insTab]; if (!subs.includes(sub)) sub = ui.insSub[ui.insTab] = subs[0]; body.append(seg(subs, sub, n => { ui.insSub[ui.insTab] = n; ui.inspector(); })); }
    const P = PANELS[ui.insTab + (sub ? '/' + sub : '')]; P && P(body, c);
  };

  function details(tabs, body) {
    tabs.append(h('button', { class: 'on' }, 'Detalles')); const P = G.project, [w, hh] = dims();
    body.append(section('Proyecto', null,
      h('div', { class: 'f' }, h('label', null, 'Nombre'), h('input', { type: 'text', value: P.name, onchange: e => { P.name = e.target.value; $('#projName').value = P.name; commit(); } })),
      h('div', { class: 'f' }, h('label', null, 'Relación de aspecto'), h('select', { onchange: e => { P.ratio = e.target.value; G.applyCanvasSize(); G.commit(); ui.inspector(); } }, GC.RATIOS.map(r => h('option', { value: r.id, selected: r.id === P.ratio }, r.id)))),
      h('div', { class: 'hint' }, `Lienzo: ${w} × ${hh} px`),
      h('div', { class: 'f' }, h('label', null, 'Fotogramas por segundo'), h('select', { onchange: e => { P.fps = +e.target.value; G.commit(); } }, [24, 25, 30, 50, 60].map(f => h('option', { value: f, selected: f === P.fps }, f + ' fps'))))),
      lienzo(),
      h('div', { class: 'hint' }, 'Selecciona un clip en la línea de tiempo para editar sus propiedades.'));
  }
  function lienzo() {
    const P = G.project;
    return section('Lienzo', null,
      h('div', { class: 'btnrow f' }, h('button', { class: 'btn' + (P.bgMode !== 'blur' ? ' on' : ''), onclick: () => { P.bgMode = 'color'; redo(); } }, 'Color'), h('button', { class: 'btn' + (P.bgMode === 'blur' ? ' on' : ''), onclick: () => { P.bgMode = 'blur'; redo(); } }, 'Desenfoque')),
      P.bgMode !== 'blur' ? h('div', { class: 'f' }, h('label', null, 'Color de fondo'), h('input', { type: 'color', value: P.bg, oninput: e => { P.bg = e.target.value; G.touch(); }, onchange: () => G.commit() })) : h('div', { class: 'hint' }, 'El fondo usa el video de abajo, desenfocado.'));
  }

  /* ---------- Video ---------- */
  function align(c, how) {
    const B = c._box; if (!B || !B.w) return toast('Primero reproduce hasta el clip'); const W = G.canvas.width, H = G.canvas.height;
    if (how === 'l') c.x = -.5 + B.w / 2 / W; if (how === 'c') c.x = 0; if (how === 'r') c.x = .5 - B.w / 2 / W;
    if (how === 't') c.y = -.5 + B.h / 2 / H; if (how === 'm') c.y = 0; if (how === 'b') c.y = .5 - B.h / 2 / H;
    redo();
  }
  function transform(c) {
    const [W, H] = dims(), uni = c.scy == null;
    const items = [section('Transformación', () => { Object.assign(c, { x: 0, y: 0, sc: 1, scy: null, rot: 0 }); redo(); },
      uni ? sl('Escala', Math.round(c.sc * 100), 5, 500, 1, v => c.sc = v / 100, '%') : [sl('Escala X', Math.round(c.sc * 100), 5, 500, 1, v => c.sc = v / 100, '%'), sl('Escala Y', Math.round(c.scy * 100), 5, 500, 1, v => c.scy = v / 100, '%')],
      sw('Escala uniforme', uni, on => { c.scy = on ? null : c.sc; redo(); }),
      h('div', { class: 'row2' }, sl('Posición X', Math.round(c.x * W), -W, W, 1, v => c.x = v / W, ' px'), sl('Posición Y', Math.round(c.y * H), -H, H, 1, v => c.y = v / H, ' px')),
      sl('Girar', +c.rot.toFixed(1), -360, 360, .5, v => c.rot = v, '°'),
      h('div', { class: 'alignrow' }, [['l', '⇤'], ['c', '↔'], ['r', '⇥'], ['t', '⤒'], ['m', '↕'], ['b', '⤓']].map(([k, ic]) => h('button', { class: 'icon', title: 'Alinear', onclick: () => align(c, k) }, ic))),
      h('div', { class: 'f btnrow' }, h('button', { class: 'btn' + (c.flipH ? ' on' : ''), onclick: () => { c.flipH = !c.flipH; redo(); } }, '⇋ Voltear H'), h('button', { class: 'btn' + (c.flipV ? ' on' : ''), onclick: () => { c.flipV = !c.flipV; redo(); } }, '⇅ Voltear V')))];
    return items;
  }
  function applied(c) {
    const sets = [];
    c.fx.forEach((f, i) => sets.push(h('div', { class: 'f' }, h('div', { class: 'tag' }, h('b', null, '✨ ' + GC.FXBYID[f.id].name), h('button', { class: 'btn danger', onclick: () => { c.fx.splice(i, 1); G.emit('tl'); redo(); ui.libBody(); } }, '✕')), sl('Intensidad', Math.round(f.k * 100), 0, 100, 1, v => f.k = v / 100, '%'))));
    if (c.filter) sets.push(h('div', { class: 'f' }, h('div', { class: 'tag' }, h('b', null, '🎨 ' + GC.FBYID[c.filter.id].name), h('button', { class: 'btn danger', onclick: () => { c.filter = null; redo(); ui.libBody(); } }, '✕')), sl('Intensidad del filtro', Math.round(c.filter.k * 100), 0, 100, 1, v => c.filter.k = v / 100, '%')));
    if (c.transIn) sets.push(h('div', { class: 'f' }, h('div', { class: 'tag' }, h('b', null, '⋈ ' + GC.TBYID[c.transIn.id].name), h('button', { class: 'btn danger', onclick: () => { c.transIn = null; redo(); ui.libBody(); } }, '✕')), sl('Duración de la transición', +c.transIn.dur.toFixed(2), .1, Math.max(.2, +c.dur.toFixed(2)), .05, v => c.transIn.dur = v, ' s')));
    return sets.length ? section('Aplicado', null, sets) : null;
  }
  const PANELS = {
    'Video/Básico': (b, c) => {
      b.append(...transform(c), section('Mezcla', () => { c.blend = 'source-over'; c.op = 1; redo(); }, sel('Modo', c.blend, GC.BLENDS, v => c.blend = v), sl('Opacidad', Math.round(c.op * 100), 0, 100, 1, v => c.op = v / 100, '%')), lienzo());
      const a = applied(c); a && b.append(a);
      b.append(h('div', { class: 'hint' }, 'No incluido (IA o Pro en CapCut): estabilización, mejorar calidad, reducir ruido, flujo óptico, eliminación/ampliación de IA, retoque.'));
    },
    'Video/Eliminar fondo': (b, c) => {
      const k = c.chroma = c.chroma || { on: false, color: '#00ff00', tol: .35, soft: .15 };
      b.append(sw('Eliminación automática', false, () => { toast('La eliminación automática necesita IA y no está disponible'); ui.inspector(); }, 'Necesita IA'),
        section('Chroma key', () => { c.chroma = null; redo(); },
          sw('Activar chroma key', k.on, on => { k.on = on; redo(); }),
          h('div', { class: 'f' }, h('label', null, 'Color a quitar'), h('div', { class: 'btnrow' }, h('input', { type: 'color', value: k.color, style: 'flex:1', oninput: e => { k.color = e.target.value; k.on = true; G.touch(); }, onchange: () => G.commit() }),
            window.EyeDropper ? h('button', { class: 'btn', onclick: async () => { try { const r = await new EyeDropper().open(); k.color = r.sRGBHex; k.on = true; redo(); } catch (e) { } } }, '💧 Cuentagotas') : null)),
          sl('Tolerancia', Math.round(k.tol * 100), 0, 100, 1, v => { k.tol = v / 100; k.on = true; }), sl('Suavizado', Math.round(k.soft * 100), 0, 100, 1, v => { k.soft = v / 100; k.on = true; })));
    },
    'Video/Máscara': (b, c) => {
      b.append(section('Máscara', () => { c.mask = null; redo(); }, h('div', { class: 'grid' }, GC.MASKS.map(([v, n]) => h('div', { class: 'card' + (((c.mask && c.mask.t) || '') === v ? ' on' : ''), onclick: () => { c.mask = v ? { t: v, s: c.mask ? c.mask.s : 1 } : null; redo(); } }, h('div', { class: 'th tcard' }, { '': '🚫', circle: '⚫', rect: '▬', heart: '♥', star: '★' }[v]), h('div', { class: 'nm' }, n)))),
        c.mask ? sl('Tamaño', Math.round(c.mask.s * 100), 10, 200, 1, v => c.mask.s = v / 100, '%') : null));
    },
    'Texto': (b, c) => textPanel(b, c),
    'Audio/Básico': (b, c) => {
      const db = c.vol > 0 ? 20 * Math.log10(c.vol) : -60;
      b.append(section('Básico', () => { c.vol = 1; c.fadeIn = 0; c.fadeOut = 0; c.norm = false; redo(); },
        sl('Volumen', +db.toFixed(1), -60, 12, .1, v => c.vol = v <= -60 ? 0 : Math.pow(10, v / 20), ' dB'),
        sl('Aparición progresiva', +c.fadeIn.toFixed(1), 0, Math.min(10, c.dur), .1, v => c.fadeIn = v, ' s'), sl('Desaparición progresiva', +c.fadeOut.toFixed(1), 0, Math.min(10, c.dur), .1, v => c.fadeOut = v, ' s'),
        sw('Normalizar la intensidad', c.norm, on => { c.norm = on; redo(); }, 'Aproxima el volumen a −23 LUFS'),
        sw('Reducir el ruido', false, () => { toast('Reducir el ruido con IA no está disponible'); ui.inspector(); }, 'Necesita IA')));
    },
    'Audio/Modificador de voz': (b, c) => {
      b.append(h('div', { class: 'chips' }, h('button', { class: 'on' }, 'Filtros de voz'), h('button', { class: 'dis', onclick: () => toast('Los personajes de voz necesitan IA') }, 'Personajes de voz'), h('button', { class: 'dis', onclick: () => toast('Voz a canción necesita IA') }, 'Voz a canción')),
        h('div', { class: 'grid' }, GC.VOICES.map(v => h('div', { class: 'card' + ((c.voice || '') === v.id ? ' on' : ''), onclick: () => { c.voice = v.id; redo(); } }, h('div', { class: 'th tcard', style: 'font-size:12px;min-height:50px' }, v.name)))),
        sw('Aplicar a todos los clips', false, on => { if (on) { G.project.clips.filter(x => x.type === 'video' || x.type === 'audio').forEach(x => x.voice = c.voice); commit(); } }));
    },
    'Velocidad/Estándar': (b, c) => {
      const base = c.dur * c.speed;
      b.append(sl('Velocidad', c.speed, .1, 10, .1, v => { G.setSpeed(c, v); G.emit('tl'); }, 'x'),
        h('div', { class: 'f btnrow' }, [.5, 1, 1.5, 2, 4].map(v => h('button', { class: 'btn' + (c.speed === v ? ' on' : ''), onclick: () => { if (!G.setSpeed(c, v)) toast('No hay espacio libre en la pista'); G.touch(); G.emit('tl'); redo(); } }, v + 'x'))),
        sl('Duración', +c.dur.toFixed(2), +(base / 10).toFixed(2), +(base / .1).toFixed(2), .05, v => { G.setSpeed(c, base / v); G.emit('tl'); }, ' s'),
        c.type === 'video' || c.type === 'audio' ? sw('Cambiar tono del audio', c.pitch, on => { c.pitch = on; commit(); }, 'Apagado: el tono se conserva al acelerar') : null);
    },
    'Velocidad/Curva': (b, c) => {
      b.append(h('div', { class: 'grid' }, GC.SPEED_CURVES.map(cu => h('div', { class: 'card' + ((c.curve || '') === cu.id ? ' on' : ''), onclick: () => { c.curve = cu.id; G.touch(); G.emit('tl'); redo(); } }, curveThumb(cu), h('div', { class: 'nm' }, cu.name)))),
        h('div', { class: 'hint' }, 'La curva cambia la velocidad dentro del clip sin cambiar su duración total.'));
    },
    'Animación': (b, c) => animPanel(b, c),
    'Ajustar/Básico': (b, c) => adjBasic(b, c),
    'Ajustar/HSL': (b, c) => hslPanel(b, c),
    'Ajustar/Curvas': (b, c) => curvesPanel(b, c),
    'Ajustar/Círculo cromático': (b, c) => wheelsPanel(b, c),
  };

  function curveThumb(cu) {
    const cv = h('canvas', { width: 120, height: 70, style: 'width:100%;display:block;background:#1d1d21' }), x = cv.getContext('2d'); x.strokeStyle = '#ffd24a'; x.lineWidth = 2; x.beginPath();
    for (let i = 0; i <= 60; i++) { const u = i / 60, m = cu.m ? cu.m(u) / cu.mean : 1, y = 60 - Math.min(1, m / 3) * 52; i ? x.lineTo(5 + u * 110, y) : x.moveTo(5 + u * 110, y); } x.stroke(); return cv;
  }

  /* ---------- Texto ---------- */
  function textPanel(b, c) {
    const T = c.text;
    b.append(section('Texto', null,
      h('div', { class: 'f' }, h('textarea', { oninput: e => { T.s = e.target.value; G.touch(); G.save(); G.emit('tl'); }, onchange: () => G.commit() }, T.s)),
      h('div', { class: 'f' }, h('label', null, 'Fuente'), h('select', { onchange: e => { T.font = e.target.value; document.fonts && document.fonts.load(`20px "${T.font}"`).then(G.touch); commit(); } }, GC.FONTS.map(f => h('option', { value: f, selected: f === T.font, style: `font-family:"${f}"` }, f)))),
      sl('Tamaño', T.size, 10, 400, 1, v => T.size = v),
      h('div', { class: 'f btnrow' }, h('button', { class: 'btn' + (T.bold ? ' on' : ''), onclick: () => { T.bold = !T.bold; redo(); } }, 'N'), h('button', { class: 'btn' + (T.italic ? ' on' : ''), onclick: () => { T.italic = !T.italic; redo(); } }, 'K')),
      h('div', { class: 'row2' }, h('div', { class: 'f' }, h('label', null, 'Color'), h('input', { type: 'color', value: T.color, oninput: e => { T.color = e.target.value; G.touch(); }, onchange: () => G.commit() })), h('div', { class: 'f' }, h('label', null, 'Contorno'), h('input', { type: 'color', value: T.stroke || '#000000', oninput: e => { T.stroke = e.target.value; G.touch(); }, onchange: () => G.commit() }))),
      sl('Grosor del contorno', T.strokeW || 0, 0, 40, 1, v => T.strokeW = v), sl('Espaciado de letras', T.spacing || 0, -5, 40, 1, v => T.spacing = v),
      sw('Sombra', !!T.shadow, on => { T.shadow = on ? { c: 'rgba(0,0,0,.7)', b: 10, x: 0, y: 4 } : null; redo(); }), sw('Fondo', !!T.bg, on => { T.bg = on ? 'rgba(0,0,0,.65)' : null; redo(); })),
      ...transform(c), section('Mezcla', null, sl('Opacidad', Math.round(c.op * 100), 0, 100, 1, v => c.op = v / 100, '%')));
  }

  /* ---------- Animación ---------- */
  function animPanel(b, c) {
    const tabs = [['in', 'Entrada'], ['out', 'Salida'], ['loop', 'Combinado']], at = ui.animTab, key = { in: 'animIn', out: 'animOut', loop: 'animLoop' }[at];
    b.append(seg(tabs.map(t => t[1]), tabs.find(t => t[0] === at)[1], n => { ui.animTab = tabs.find(t => t[1] === n)[0]; ui.animSearch = ''; ui.inspector(); }));
    b.append(h('div', { class: 'sbar' }, h('span', null, '⌕'), h('input', { class: 'search', placeholder: 'Buscar animaciones', value: ui.animSearch || '', oninput: e => { ui.animSearch = e.target.value; clearTimeout(animPanel._t); animPanel._t = setTimeout(() => { const f = document.activeElement; ui.inspector(); const i = $('#inspBody .search'); if (i) { i.focus(); i.setSelectionRange(i.value.length, i.value.length); } }, 250); } })));
    const cat = ui.animCat || GC.ANIM_CATS[0];
    b.append(h('div', { class: 'chips' }, [['★', '★'], ...GC.ANIM_CATS.map(x => [x, x])].map(([k, n]) => h('button', { class: cat === k ? 'on' : '', onclick: () => { ui.animCat = k; ui.inspector(); } }, n))));
    const all = at === 'loop' ? GC.ANIM_COMBO : GC.ANIM_IO.filter(a => !a.text || c.type === 'text'), q = (ui.animSearch || '').toLowerCase();
    const list = all.filter(a => (q ? a.name.toLowerCase().includes(q) : cat === '★' ? G.favs.has('an:' + a.id) : cat === 'En tendencia' ? a.trend : a.cat === cat));
    b.append(h('div', { class: 'grid' }, [{ id: '', name: 'Ninguno' }, ...list].map(a => h('div', { class: 'card' + (((c[key] && c[key].id) || '') === a.id ? ' on' : ''), onclick: () => { c[key] = a.id ? (at === 'loop' ? { id: a.id, speed: 1 } : { id: a.id, dur: Math.min(1, c.dur / 2) }) : null; redo(); } },
      h('div', { class: 'th tcard', style: 'font-size:13px;min-height:50px' }, a.name), a.id ? h('button', { class: 'star' + (G.favs.has('an:' + a.id) ? ' on' : ''), onclick: e => { e.stopPropagation(); G.toggleFav('an:' + a.id); ui.inspector(); } }, G.favs.has('an:' + a.id) ? '★' : '☆') : null))));
    if (c[key]) b.append(h('div', { style: 'margin-top:14px' }), at === 'loop' ? sl('Velocidad', c[key].speed || 1, .2, 4, .1, v => c[key].speed = v, 'x') : sl('Duración', +c[key].dur.toFixed(2), .1, Math.max(.2, c.dur), .05, v => c[key].dur = v, ' s'));
  }

  /* ---------- Ajustar ---------- */
  function adjBasic(b, c) {
    const A = c.adj = c.adj || {}, S = (k, n, mn = -100) => sl(n, A[k] || 0, mn, 100, 1, v => A[k] = v);
    const lutNames = [...GC.LUTS.keys()];
    b.append(section('LUT', () => { c.lut = null; redo(); },
      h('div', { class: 'f' }, h('label', null, 'Nombre'), h('div', { class: 'btnrow' }, h('select', { style: 'flex:1', onchange: e => { c.lut = e.target.value ? { name: e.target.value, k: 1 } : null; redo(); } }, [h('option', { value: '' }, 'Ninguno'), ...lutNames.map(n => h('option', { value: n, selected: c.lut && c.lut.name === n }, n))]), h('button', { class: 'btn', onclick: ui.pickLut }, '⬆ .cube'))),
      c.lut ? sl('Intensidad', Math.round((c.lut.k ?? 1) * 100), 0, 100, 1, v => c.lut.k = v / 100) : null),
      section('Ajustar', () => { c.adj = {}; redo(); }, h('div', { class: 'sub' }, 'Color'), S('temp', 'Temp'), S('tint', 'Tinte'), S('sat', 'Saturación'),
        h('div', { class: 'sub' }, 'Luz'), S('exposure', 'Exposición'), S('contrast', 'Contraste'), S('hl', 'Iluminar'), S('shadow', 'Sombra'), S('white', 'Blancos'), S('black', 'Negros'), S('lum', 'Luminosidad'),
        h('div', { class: 'sub' }, 'Efectos'), S('sharpen', 'Enfocar', 0), S('clarity', 'Claridad'), S('grain', 'Partículas', 0), S('fade', 'Desvanecer', 0), S('vignette', 'Viñeta', 0)));
    if (c.filter) b.append(section('Filtro: ' + GC.FBYID[c.filter.id].name, null, sl('Intensidad', Math.round(c.filter.k * 100), 0, 100, 1, v => c.filter.k = v / 100, '%')));
  }
  const COLORS = { red: '#ff3b3b', orange: '#ff9a2e', yellow: '#ffe135', green: '#35d44a', cyan: '#2ee6e6', blue: '#3b6bff', purple: '#9b4dff', magenta: '#ff3bd0' };
  function hslPanel(b, c) {
    c.hsl = c.hsl || {}; const k = ui.hslColor, v = c.hsl[k] = c.hsl[k] || { h: 0, s: 0, l: 0 };
    b.append(section('Básico', () => { c.hsl = {}; redo(); },
      h('div', { class: 'dots' }, GC.HSL_COLORS.map(n => h('button', { class: 'dot' + (n === k ? ' on' : ''), style: `border-color:${COLORS[n]};background:${n === k ? COLORS[n] : 'transparent'}`, onclick: () => { ui.hslColor = n; ui.inspector(); } }))),
      sl('Matiz', v.h, -100, 100, 1, x => v.h = x), sl('Saturación', v.s, -100, 100, 1, x => v.s = x), sl('Brillo', v.l, -100, 100, 1, x => v.l = x)));
  }
  function curvesPanel(b, c) {
    c.curves = c.curves || {};
    [['luma', 'Luma', '#ffffff'], ['r', 'Rojo (R)', '#ff5252'], ['g', 'Verde (V)', '#4cd964'], ['b', 'Azul (A)', '#5a8dff']].forEach(([k, n, col]) => b.append(h('div', { class: 'f' }, h('div', { class: 'lab' }, h('span', null, n), h('button', { class: 'icon', onclick: () => { delete c.curves[k]; redo(); } }, '↺')), curveEditor(c, k, col))));
  }
  function curveEditor(c, key, color) {
    const cv = h('canvas', { width: 480, height: 300, class: 'curvecv' }), x = cv.getContext('2d'); c.curves[key] = c.curves[key] || [[0, 0], [1, 1]]; const pts = () => c.curves[key];
    const W = 480, H = 300, pad = 8, px = p => pad + p * (W - 2 * pad), py = p => H - pad - p * (H - 2 * pad);
    function draw() {
      x.clearRect(0, 0, W, H); x.strokeStyle = '#333'; x.lineWidth = 1; for (let i = 0; i <= 4; i++) { x.beginPath(); x.moveTo(px(i / 4), pad); x.lineTo(px(i / 4), H - pad); x.moveTo(pad, py(i / 4)); x.lineTo(W - pad, py(i / 4)); x.stroke(); }
      const L = GC.curveLUT(pts()); x.strokeStyle = color; x.lineWidth = 2.5; x.beginPath(); for (let i = 0; i < 256; i++) { const X = px(i / 255), Y = py(L[i]); i ? x.lineTo(X, Y) : x.moveTo(X, Y); } x.stroke();
      pts().forEach(p => { x.fillStyle = '#fff'; x.beginPath(); x.arc(px(p[0]), py(p[1]), 7, 0, 7); x.fill(); x.strokeStyle = color; x.lineWidth = 2; x.stroke(); });
    }
    const pos = e => { const r = cv.getBoundingClientRect(); return [clamp(((e.clientX - r.left) / r.width * W - pad) / (W - 2 * pad), 0, 1), clamp(1 - ((e.clientY - r.top) / r.height * H - pad) / (H - 2 * pad), 0, 1)]; };
    let drag = -1;
    cv.addEventListener('pointerdown', e => {
      const [u, v] = pos(e), P = pts(); let best = -1, bd = 1e9; P.forEach((p, i) => { const d = Math.hypot(p[0] - u, p[1] - v); if (d < bd) { bd = d; best = i; } });
      if (bd < .06) drag = best; else { P.push([u, v]); P.sort((a, b) => a[0] - b[0]); drag = P.findIndex(p => p[0] === u && p[1] === v); }
      cv.setPointerCapture(e.pointerId); draw(); G.touch();
    });
    cv.addEventListener('pointermove', e => { if (drag < 0) return; const P = pts(), [u, v] = pos(e), last = P.length - 1; const lo = drag === 0 ? 0 : P[drag - 1][0] + .01, hi = drag === last ? 1 : P[drag + 1][0] - .01; P[drag] = [drag === 0 ? 0 : drag === last ? 1 : clamp(u, lo, hi), v]; draw(); G.touch(); });
    cv.addEventListener('pointerup', () => { if (drag >= 0) { drag = -1; G.commit(); } });
    cv.addEventListener('dblclick', e => { const [u, v] = pos(e), P = pts(); const i = P.findIndex(p => Math.hypot(p[0] - u, p[1] - v) < .06); if (i > 0 && i < P.length - 1) { P.splice(i, 1); draw(); G.touch(); G.commit(); } });
    draw(); return cv;
  }
  function hsv(hh, s, v) { const c = v * s, x = c * (1 - Math.abs((hh / 60) % 2 - 1)), m = v - c; let r, g, b; if (hh < 60) [r, g, b] = [c, x, 0]; else if (hh < 120) [r, g, b] = [x, c, 0]; else if (hh < 180) [r, g, b] = [0, c, x]; else if (hh < 240) [r, g, b] = [0, x, c]; else if (hh < 300) [r, g, b] = [x, 0, c]; else [r, g, b] = [c, 0, x]; return [r + m, g + m, b + m]; }
  function wheelsPanel(b, c) {
    c.wheels = c.wheels || {}; c.wheelPos = c.wheelPos || {};
    b.append(section('Círculo cromático', () => { c.wheels = {}; c.wheelPos = {}; c.wheelInt = 100; redo(); }, sl('Intensidad', c.wheelInt ?? 100, 0, 100, 1, v => c.wheelInt = v),
      h('div', { class: 'wheels' }, [['shadows', 'Sombras'], ['mid', 'Gris intermedio'], ['high', 'Tinte'], ['offset', 'Desplazamiento']].map(([k, n]) => wheel(c, k, n)))));
  }
  function wheel(c, key, name) {
    const S = 120, cv = h('canvas', { width: S * 2, height: S * 2, class: 'wheelcv' }), x = cv.getContext('2d'), R = S - 6, nums = h('div', { class: 'wn' });
    const ring = document.createElement('canvas'); ring.width = ring.height = S * 2; const rc = ring.getContext('2d'); const id = rc.createImageData(S * 2, S * 2);
    for (let j = 0; j < S * 2; j++) for (let i = 0; i < S * 2; i++) { const dx = (i - S) / (R * 2 / 2), dy = (j - S) / R, d = Math.hypot(dx, dy); if (d > 1.0 || d < 0) continue; const rgb = hsv((Math.atan2(dy, dx) * 180 / Math.PI + 360) % 360, d, 1), o = (j * S * 2 + i) * 4; id.data[o] = rgb[0] * 255; id.data[o + 1] = rgb[1] * 255; id.data[o + 2] = rgb[2] * 255; id.data[o + 3] = 255; }
    rc.putImageData(id, 0, 0);
    const pos = () => c.wheelPos[key] || [0, 0];
    const draw = () => { x.clearRect(0, 0, S * 2, S * 2); x.globalAlpha = .85; x.drawImage(ring, 0, 0); x.globalAlpha = 1; const p = pos(); x.fillStyle = '#fff'; x.strokeStyle = '#000'; x.lineWidth = 2; x.beginPath(); x.arc(S + p[0] * R, S + p[1] * R, 8, 0, 7); x.fill(); x.stroke(); const v = c.wheels[key] || [0, 0, 0]; nums.innerHTML = ''; ['#ff5252', '#4cd964', '#5a8dff'].forEach((col, i) => nums.append(h('span', { style: `border-top:2px solid ${col}` }, v[i].toFixed(2)))); };
    const set = (u, v) => { const d = Math.hypot(u, v); if (d > 1) { u /= d; v /= d; } c.wheelPos[key] = [u, v]; const r = Math.hypot(u, v), ang = (Math.atan2(v, u) * 180 / Math.PI + 360) % 360, col = hsv(ang, 1, 1), mean = (col[0] + col[1] + col[2]) / 3; c.wheels[key] = col.map(q => +((q - mean) * r * 1.5).toFixed(2)); draw(); G.touch(); };
    let down = false; const pt = e => { const r = cv.getBoundingClientRect(); return [((e.clientX - r.left) / r.width * S * 2 - S) / R, ((e.clientY - r.top) / r.height * S * 2 - S) / R]; };
    cv.addEventListener('pointerdown', e => { down = true; cv.setPointerCapture(e.pointerId); set(...pt(e)); }); cv.addEventListener('pointermove', e => down && set(...pt(e))); cv.addEventListener('pointerup', () => { if (down) { down = false; G.commit(); } });
    cv.addEventListener('dblclick', () => { delete c.wheels[key]; delete c.wheelPos[key]; draw(); G.touch(); G.commit(); });
    draw(); return h('div', { class: 'wheel' }, h('div', { class: 'lab' }, h('span', null, name), h('button', { class: 'icon', onclick: () => { delete c.wheels[key]; delete c.wheelPos[key]; draw(); G.touch(); G.commit(); } }, '↺')), cv, nums);
  }
})();
