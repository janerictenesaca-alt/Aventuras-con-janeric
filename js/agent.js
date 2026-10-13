/* Ganjan - Asistente de IA: chat por voz o texto que edita el proyecto con las mismas funciones del programa */
(function () {
  const { h, $, toast } = G.ui;
  const LS = k => { try { return localStorage.getItem(k) || ''; } catch (e) { return ''; } };
  const LSset = (k, v) => { try { localStorage.setItem(k, v); } catch (e) { } };
  const MODELS = [['claude-haiku-5-5', 'Haiku 5.5 (rápido y barato)'], ['claude-sonnet-5-5', 'Sonnet 5.5 (más listo)'], ['claude-opus-5-5', 'Opus 5.5 (el más potente)']];
  const r2 = n => Math.round(n * 100) / 100;
  const commitAll = () => { G.touch(); G.emit('tl'); G.emit('insp'); G.commit(); };

  /* ---------- Resumen del proyecto para la IA ---------- */
  const brief = c => {
    const o = { id: c.id, tipo: c.type, pista: c.track, inicio: r2(c.start), dur: r2(c.dur), fin: r2(c.start + c.dur) };
    const m = c.mediaId && G.media.get(c.mediaId); if (m) o.nombre = m.name;
    if (c.type === 'text' || c.type === 'sticker') o.texto = c.text && c.text.s;
    if (c.in) o.recorte_inicio_fuente = r2(c.in);
    if (c.speed !== 1) o.velocidad = c.speed;
    if (c.vol !== 1) o.volumen = c.vol;
    if (c.filter) o.filtro = c.filter.id + '@' + c.filter.k;
    if (c.fx && c.fx.length) o.efectos = c.fx.map(f => f.id);
    if (c.transIn) o.transicion_entrada = c.transIn.id;
    if (c.animIn) o.anim_entrada = c.animIn.id || c.animIn;
    if (c.op !== 1) o.opacidad = c.op;
    if (c.sc !== 1) o.escala = c.sc;
    const adj = Object.keys(c.adj || {}).filter(k => c.adj[k]); if (adj.length) o.ajustes = Object.fromEntries(adj.map(k => [k, c.adj[k]]));
    return o;
  };
  const state = () => {
    const P = G.project;
    return {
      proyecto: { nombre: P.name, relacion: P.ratio, resolucion: P.res, fps: P.fps, duracion_total: r2(G.duration()) },
      posicion_cursor: r2(G.time), clip_seleccionado: G.sel,
      pistas: P.tracks.map(t => ({ id: t.id, tipo: t.kind === 'v' ? 'video/imagen/texto' : 'audio', silenciada: !!t.mute, oculta: !!t.hide, bloqueada: !!t.lock })),
      clips: P.clips.slice().sort((a, b) => a.start - b.start).map(brief),
      biblioteca: [...G.media.values()].filter(m => !m.sfx).map(m => ({ id: m.id, nombre: m.name, tipo: m.type, duracion: r2(m.dur || 0), ancho: m.w, alto: m.h })),
    };
  };
  const catalog = () => ({
    filtros: GC.FILTERS.map(f => f.id + ' = ' + f.name),
    efectos: GC.FX.map(f => f.id + ' = ' + f.name),
    transiciones: GC.TRANS.map(t => t.id + ' = ' + t.name),
    sonidos_sfx: GC.SFX.map(s => s.id + ' = ' + s.name),
    estilos_texto: GC.TEXT_PRESETS.map(p => p.name),
    ajustes_validos: Object.keys(Object.assign({}, ...GC.ADJ_PRESETS.map(p => p.adj))),
    relaciones: Object.keys(GC.RATIOS || {}),
  });

  /* ---------- Herramientas (lo que la IA puede "apretar") ---------- */
  const need = id => { const c = G.clip(id); if (!c) throw new Error('No existe el clip ' + id); return c; };
  const many = ids => (ids && ids.length ? ids : [G.sel]).filter(Boolean).map(need);
  const IDS = { type: 'array', items: { type: 'string' }, description: 'IDs de clips. Si se omite, se usa el clip seleccionado.' };
  const TOOLS = [
    { name: 'ver_proyecto', description: 'Devuelve el estado actual: pistas, clips (con ids, tiempos en segundos), biblioteca de medios y cursor. Llámalo siempre antes de editar si no sabes qué hay.', input_schema: { type: 'object', properties: {} }, run: () => state() },
    { name: 'ver_catalogo', description: 'Lista los ids válidos de filtros, efectos, transiciones, sonidos, estilos de texto y ajustes.', input_schema: { type: 'object', properties: {} }, run: () => catalog() },
    {
      name: 'dividir_clip', description: 'Corta un clip en dos en el segundo indicado (tiempo de la línea de tiempo).', input_schema: { type: 'object', properties: { clip_id: { type: 'string' }, tiempo: { type: 'number' } }, required: ['clip_id', 'tiempo'] },
      run: a => { need(a.clip_id); return G.split(a.clip_id, a.tiempo) ? 'ok' : 'No se pudo: el tiempo está fuera del clip o muy cerca del borde'; }
    },
    {
      name: 'dividir_en_cursor', description: 'Divide los clips que cruzan el cursor.', input_schema: { type: 'object', properties: {} }, run: () => G.splitAtPlayhead() ? 'ok' : 'No hay clip bajo el cursor'
    },
    {
      name: 'eliminar_clips', description: 'Elimina clips. Si hay que cerrar el hueco, usa mover_clip después.', input_schema: { type: 'object', properties: { clip_ids: IDS }, required: ['clip_ids'] },
      run: a => { const cs = many(a.clip_ids); cs.forEach(c => G.deleteClip(c.id, true)); commitAll(); return 'eliminados ' + cs.length; }
    },
    {
      name: 'mover_clip', description: 'Mueve un clip a un nuevo segundo de inicio. Si choca con otro, se acomoda al hueco más cercano.', input_schema: { type: 'object', properties: { clip_id: { type: 'string' }, inicio: { type: 'number' } }, required: ['clip_id', 'inicio'] },
      run: a => { const c = need(a.clip_id); const s = G.resolveStart(c.track, c.id, Math.max(0, a.inicio), c.dur); c.start = s; c.transIn = c.transIn; commitAll(); return 'inicio=' + r2(s); }
    },
    {
      name: 'recortar_clip', description: 'Cambia el tramo visible de un clip. "desde" y "hasta" son segundos DENTRO del clip original (de la fuente), no de la línea de tiempo. Mantiene el inicio en la línea de tiempo.', input_schema: { type: 'object', properties: { clip_id: { type: 'string' }, desde: { type: 'number' }, hasta: { type: 'number' } }, required: ['clip_id'] },
      run: a => {
        const c = need(a.clip_id), m = c.mediaId && G.media.get(c.mediaId), end0 = c.in + c.dur * c.speed;
        const from = Math.max(0, a.desde ?? c.in), to = Math.min(m && m.dur ? m.dur : 1e9, a.hasta ?? end0); if (to <= from + .05) throw new Error('Rango inválido');
        c.in = from; c.dur = (to - from) / c.speed; commitAll(); return 'nuevo dur=' + r2(c.dur);
      }
    },
    {
      name: 'cerrar_huecos', description: 'Junta los clips de una pista uno tras otro sin huecos (útil tras cortar/eliminar). Si no se da pista, usa la primera pista de video.', input_schema: { type: 'object', properties: { pista: { type: 'string' } } },
      run: a => {
        const tid = a.pista || (G.project.tracks.find(t => t.kind === 'v') || {}).id; if (!tid) throw new Error('No hay pistas');
        let t = 0; G.clipsOn(tid).slice().sort((x, y) => x.start - y.start).forEach(c => { c.start = t; t += c.dur; }); commitAll(); return 'ok, total ' + r2(t);
      }
    },
    {
      name: 'ajustar_clip', description: 'Cambia propiedades de uno o varios clips: velocidad (0.1-100), volumen (0-4, 1=normal), opacidad (0-1), escala (1=normal), posicion_x, posicion_y, rotacion (grados), voltear_h, voltear_v, aparecer (s fundido de audio entrada), desaparecer (s fundido salida).', input_schema: { type: 'object', properties: { clip_ids: IDS, velocidad: { type: 'number' }, volumen: { type: 'number' }, opacidad: { type: 'number' }, escala: { type: 'number' }, posicion_x: { type: 'number' }, posicion_y: { type: 'number' }, rotacion: { type: 'number' }, voltear_h: { type: 'boolean' }, voltear_v: { type: 'boolean' }, aparecer: { type: 'number' }, desaparecer: { type: 'number' } } },
      run: a => {
        const out = []; many(a.clip_ids).forEach(c => {
          if (a.velocidad != null && !G.setSpeed(c, G.clamp(a.velocidad, .1, 100))) out.push(c.id + ': no cabe con esa velocidad');
          if (a.volumen != null) c.vol = G.clamp(a.volumen, 0, 4); if (a.opacidad != null) c.op = G.clamp(a.opacidad, 0, 1); if (a.escala != null) { c.sc = a.escala; } if (a.rotacion != null) c.rot = a.rotacion;
          if (a.posicion_x != null) c.x = a.posicion_x; if (a.posicion_y != null) c.y = a.posicion_y; if (a.voltear_h != null) c.flipH = a.voltear_h; if (a.voltear_v != null) c.flipV = a.voltear_v;
          if (a.aparecer != null) c.fadeIn = Math.max(0, a.aparecer); if (a.desaparecer != null) c.fadeOut = Math.max(0, a.desaparecer);
        }); commitAll(); return out.length ? out.join('; ') : 'ok';
      }
    },
    {
      name: 'poner_filtro', description: 'Aplica un filtro (id del catálogo) a clips. Usa "ninguno" para quitarlo. intensidad de 0 a 1.', input_schema: { type: 'object', properties: { clip_ids: IDS, filtro: { type: 'string' }, intensidad: { type: 'number' } }, required: ['filtro'] },
      run: a => { if (a.filtro !== 'ninguno' && a.filtro !== 'none' && !GC.FBYID[a.filtro]) throw new Error('Filtro desconocido; usa ver_catalogo'); many(a.clip_ids).forEach(c => { c.filter = (a.filtro === 'ninguno' || a.filtro === 'none') ? null : { id: a.filtro, k: G.clamp(a.intensidad ?? 1, 0, 1) }; }); commitAll(); return 'ok'; }
    },
    {
      name: 'poner_efecto', description: 'Añade o quita (quitar=true) un efecto visual (id del catálogo) en clips.', input_schema: { type: 'object', properties: { clip_ids: IDS, efecto: { type: 'string' }, quitar: { type: 'boolean' } }, required: ['efecto'] },
      run: a => { if (!GC.FXBYID[a.efecto]) throw new Error('Efecto desconocido; usa ver_catalogo'); many(a.clip_ids).forEach(c => { c.fx = c.fx.filter(x => x.id !== a.efecto); if (!a.quitar) c.fx.push({ id: a.efecto, k: .6 }); }); commitAll(); return 'ok'; }
    },
    {
      name: 'poner_transicion', description: 'Pone una transición (id del catálogo) al INICIO de los clips (une con el clip anterior de la misma pista, deben tocarse). Usa "ninguna" para quitar. dur en segundos (por defecto .6).', input_schema: { type: 'object', properties: { clip_ids: IDS, transicion: { type: 'string' }, dur: { type: 'number' } }, required: ['transicion'] },
      run: a => { const none = a.transicion === 'ninguna' || a.transicion === 'none'; if (!none && !GC.TBYID[a.transicion]) throw new Error('Transición desconocida; usa ver_catalogo'); many(a.clip_ids).forEach(c => { c.transIn = none ? null : { id: a.transicion, dur: Math.min(a.dur || .6, c.dur / 2) }; }); commitAll(); return 'ok'; }
    },
    {
      name: 'transiciones_a_todos', description: 'Pone la misma transición entre todos los clips consecutivos de la pista de video (todos menos el primero).', input_schema: { type: 'object', properties: { transicion: { type: 'string' }, dur: { type: 'number' } }, required: ['transicion'] },
      run: a => { if (!GC.TBYID[a.transicion]) throw new Error('Transición desconocida'); const tid = (G.project.tracks.find(t => t.kind === 'v') || {}).id; const cs = G.clipsOn(tid).slice().sort((x, y) => x.start - y.start); cs.forEach((c, i) => { c.transIn = i ? { id: a.transicion, dur: Math.min(a.dur || .6, c.dur / 2) } : null; }); commitAll(); return 'ok ' + Math.max(0, cs.length - 1); }
    },
    {
      name: 'ajustar_color', description: 'Cambia ajustes de color de clips (ver ajustes_validos en ver_catalogo). Valores típicos de -100 a 100. Ej: {"temp":20,"contrast":10}.', input_schema: { type: 'object', properties: { clip_ids: IDS, ajustes: { type: 'object' } }, required: ['ajustes'] },
      run: a => { many(a.clip_ids).forEach(c => { c.adj = Object.assign({}, c.adj, a.ajustes); }); commitAll(); return 'ok'; }
    },
    {
      name: 'agregar_medio', description: 'Pone un medio de la biblioteca (media_id de ver_proyecto) en la línea de tiempo en el segundo "inicio".', input_schema: { type: 'object', properties: { media_id: { type: 'string' }, inicio: { type: 'number' } }, required: ['media_id'] },
      run: a => { const m = G.media.get(a.media_id); if (!m) throw new Error('No existe ese medio'); return brief(G.addMediaClip(m, a.inicio ?? G.time)); }
    },
    {
      name: 'agregar_texto', description: 'Añade un texto en pantalla. estilo = nombre de un estilo de ver_catalogo (opcional).', input_schema: { type: 'object', properties: { texto: { type: 'string' }, inicio: { type: 'number' }, duracion: { type: 'number' }, estilo: { type: 'string' }, posicion_y: { type: 'number', description: 'Desplazamiento vertical en px del lienzo; negativo = arriba' } }, required: ['texto'] },
      run: a => { const p = GC.TEXT_PRESETS.find(p => p.name === a.estilo); const c = G.addText(p, a.inicio ?? G.time); c.text.s = a.texto; if (a.duracion) c.dur = a.duracion; if (a.posicion_y != null) c.y = a.posicion_y; commitAll(); return brief(c); }
    },
    {
      name: 'agregar_sticker', description: 'Añade un sticker (emoji).', input_schema: { type: 'object', properties: { emoji: { type: 'string' }, inicio: { type: 'number' }, duracion: { type: 'number' } }, required: ['emoji'] },
      run: a => { const c = G.addSticker(a.emoji, a.inicio ?? G.time); if (a.duracion) { c.dur = a.duracion; commitAll(); } return brief(c); }
    },
    {
      name: 'agregar_sonido', description: 'Añade un efecto de sonido (id del catálogo) en un segundo.', input_schema: { type: 'object', properties: { sonido: { type: 'string' }, inicio: { type: 'number' } }, required: ['sonido'] },
      run: async a => { if (!GC.SFX.find(s => s.id === a.sonido)) throw new Error('Sonido desconocido'); return brief(await G.addSfx(a.sonido, a.inicio ?? G.time)); }
    },
    {
      name: 'detectar_silencios', description: 'Busca silencios (tramos con volumen bajo) en un clip de audio/video. Devuelve tramos en segundos de la LÍNEA DE TIEMPO. umbral 0-1 (0.08 por defecto), min_dur segundos (0.5 por defecto). Después puedes dividir y eliminar esos tramos.', input_schema: { type: 'object', properties: { clip_id: { type: 'string' }, umbral: { type: 'number' }, min_dur: { type: 'number' } }, required: ['clip_id'] },
      run: a => {
        const c = need(a.clip_id), m = G.media.get(c.mediaId); if (!m || !m.peaks) throw new Error('Este clip no tiene audio analizado todavía (espera unos segundos o es muy pesado)');
        const th = (a.umbral ?? .08) * 255, minD = a.min_dur ?? .5, res = []; let s = null;
        const n = Math.floor(c.dur * c.speed * 50);
        for (let i = 0; i <= n; i++) {
          const p = i < n ? (m.peaks[Math.floor(c.in * 50) + i] ?? 0) : 1e9, q = p < th;
          if (q && s === null) s = i; else if (!q && s !== null) { const d = (i - s) / 50 / c.speed; if (d >= minD) res.push({ desde: r2(c.start + s / 50 / c.speed), hasta: r2(c.start + i / 50 / c.speed) }); s = null; }
        }
        return { silencios: res, nota: 'Para quitarlos: dividir en los extremos de cada tramo (de atrás hacia adelante), eliminar los trozos y luego cerrar_huecos.' };
      }
    },
    { name: 'mover_cursor', description: 'Pone el cursor de reproducción en un segundo.', input_schema: { type: 'object', properties: { tiempo: { type: 'number' } }, required: ['tiempo'] }, run: a => { G.seek(a.tiempo); return 'ok'; } },
    { name: 'seleccionar_clip', description: 'Selecciona un clip.', input_schema: { type: 'object', properties: { clip_id: { type: 'string' } }, required: ['clip_id'] }, run: a => { need(a.clip_id); G.sel = a.clip_id; G.emit('tl'); G.emit('insp'); return 'ok'; } },
    {
      name: 'proyecto', description: 'Cambia el proyecto: nombre, relacion (ej "9:16", "16:9"), resolucion (720,1080,1440,2160), fps.', input_schema: { type: 'object', properties: { nombre: { type: 'string' }, relacion: { type: 'string' }, resolucion: { type: 'number' }, fps: { type: 'number' } } },
      run: a => { const P = G.project; if (a.nombre) { P.name = a.nombre; const pn = $('#projName'); if (pn) pn.value = a.nombre; } if (a.relacion) { if (GC.RATIOS && !GC.RATIOS[a.relacion]) throw new Error('Relación no válida'); P.ratio = a.relacion; } if (a.resolucion) P.res = a.resolucion; if (a.fps) P.fps = a.fps; G.applyCanvasSize(); commitAll(); return 'ok'; }
    },
    { name: 'reproducir', description: 'Reproduce o pausa la vista previa.', input_schema: { type: 'object', properties: {} }, run: () => { G.toggle(); return G.playing ? 'reproduciendo' : 'pausado'; } },
    { name: 'abrir_exportar', description: 'Abre el diálogo de exportar para que la persona elija y confirme (la IA no exporta sola).', input_schema: { type: 'object', properties: {} }, run: () => { $('#btnExport').click(); return 'abierto'; } },
  ];
  const TOOL_DEFS = TOOLS.map(t => ({ name: t.name, description: t.description, input_schema: t.input_schema }));

  const SYSTEM = `Eres el asistente de edición dentro de Ganjan, un editor de video estilo CapCut. La persona te habla en español (a veces por voz, así que puede haber errores de transcripción: interpreta la intención con sentido común) y tú editas el proyecto usando las herramientas.
Reglas:
- Todos los tiempos son segundos. Antes de editar, mira el proyecto con ver_proyecto (los ids cambian después de dividir: vuelve a mirar cuando haga falta). Usa ver_catalogo para ids válidos de filtros/efectos/transiciones; elige el más parecido a lo pedido.
- Ejecuta lo pedido sin pedir permiso; solo pregunta si falta un dato imprescindible. Si dudas entre opciones razonables, elige una y dilo.
- Al quitar tramos de un clip: divide de atrás hacia adelante para que los tiempos no se muevan, elimina los trozos y usa cerrar_huecos si la persona quiere que quede continuo.
- No puedes ver ni oír el contenido de los videos, solo sus datos y el volumen (detectar_silencios). No inventes lo que hay en ellos; si piden algo que depende del contenido (quitar errores al hablar, subtítulos de lo que dicen), explica brevemente que aún no puedes y ofrece alternativas.
- No exportas solo: usa abrir_exportar para que la persona confirme.
- Todo se puede deshacer con Ctrl+Z; igual, no borres cosas que no te pidieron.
- Responde corto, claro y en español, diciendo qué hiciste.`;

  /* ---------- Llamada a la API ---------- */
  let history = [], busy = false, startHi = null;
  const call = async (messages) => {
    const r = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: { 'content-type': 'application/json', 'x-api-key': LS('ganjan.apikey'), 'anthropic-version': '2023-06-01', 'anthropic-dangerous-direct-browser-access': 'true' },
      body: JSON.stringify({ model: LS('ganjan.model') || MODELS[0][0], max_tokens: 2048, system: SYSTEM, tools: TOOL_DEFS, messages }),
    });
    const j = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error((j.error && j.error.message) || ('Error ' + r.status));
    return j;
  };
  const runAgent = async (userText) => {
    if (!LS('ganjan.apikey')) { addMsg('bot', 'Primero pon tu clave de la API en ⚙ (arriba a la derecha de este panel).'); openSettings(); return; }
    busy = true; setBusy(true); if (startHi === null) startHi = G.hi;
    history.push({ role: 'user', content: userText });
    try {
      for (let i = 0; i < 14; i++) {
        const resp = await call(history);
        history.push({ role: 'assistant', content: resp.content });
        resp.content.filter(b => b.type === 'text' && b.text.trim()).forEach(b => addMsg('bot', b.text));
        const uses = resp.content.filter(b => b.type === 'tool_use');
        if (!uses.length) break;
        const results = [];
        for (const u of uses) {
          const t = TOOLS.find(t => t.name === u.name); let out, err = false;
          try { out = await t.run(u.input || {}); } catch (e) { out = String(e.message || e); err = true; }
          addStep(u.name, u.input, err ? out : null);
          results.push({ type: 'tool_result', tool_use_id: u.id, content: typeof out === 'string' ? out : JSON.stringify(out), is_error: err });
        }
        history.push({ role: 'user', content: results });
        if (resp.stop_reason !== 'tool_use') break;
      }
    } catch (e) { addMsg('bot', '⚠ ' + e.message); }
    if (history.length > 40) { history = history.slice(-24); while (history.length && !(history[0].role === 'user' && typeof history[0].content === 'string')) history.shift(); }
    busy = false; setBusy(false); G.rev++; G.render(true);
  };

  /* ---------- Interfaz ---------- */
  const NICE = { dividir_clip: '✂ Dividir', dividir_en_cursor: '✂ Dividir en el cursor', eliminar_clips: '🗑 Eliminar', mover_clip: '↔ Mover', recortar_clip: '✂ Recortar', cerrar_huecos: '⇥ Cerrar huecos', ajustar_clip: '⚙ Ajustar clip', poner_filtro: '🎨 Filtro', poner_efecto: '✨ Efecto', poner_transicion: '⋈ Transición', transiciones_a_todos: '⋈ Transiciones', ajustar_color: '🎚 Color', agregar_medio: '＋ Medio', agregar_texto: '＋ Texto', agregar_sticker: '＋ Sticker', agregar_sonido: '＋ Sonido', detectar_silencios: '🔎 Buscar silencios', mover_cursor: '⌖ Cursor', seleccionar_clip: '▣ Seleccionar', proyecto: '⚙ Proyecto', reproducir: '▶ Reproducir', abrir_exportar: '⬆ Exportar', ver_proyecto: '👁 Mirando el proyecto', ver_catalogo: '📖 Catálogo' };
  let panel, log, input, micBtn, sendBtn, undoBtn, statusEl;
  const addMsg = (who, text) => { const d = h('div', { class: 'ag-msg ' + who }, text); log.append(d); log.scrollTop = 1e9; return d; };
  const addStep = (name, args, err) => {
    const short = Object.entries(args || {}).filter(([k]) => k !== 'clip_ids' && k !== 'clip_id').map(([k, v]) => k + '=' + (typeof v === 'object' ? JSON.stringify(v) : v)).join(' ').slice(0, 70);
    log.append(h('div', { class: 'ag-step' + (err ? ' err' : '') }, (NICE[name] || name) + (short ? ' · ' + short : '') + (err ? ' → ' + err : ''))); log.scrollTop = 1e9;
  };
  const setBusy = b => { statusEl.textContent = b ? '⏳ Pensando…' : ''; sendBtn.disabled = b; undoBtn.classList.toggle('hidden', startHi === null || G.hi <= startHi); };
  const send = text => { text = (text || input.value).trim(); if (!text || busy) return; input.value = ''; addMsg('me', text); runAgent(text); };

  /* voz */
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  let rec = null, listening = false, held = false, pendingStop = false, autoSend = LS('ganjan.autosend') !== '0';
  const stopRec = () => { try { rec && rec.stop(); } catch (e) { } };
  const toggleMic = () => {
    if (!SR) { toast('Este navegador no tiene dictado por voz. Usa Chrome o Edge.'); return; }
    if (listening) { stopRec(); return; }
    rec = new SR(); const nl = (navigator.language || 'es-ES'); rec.lang = /^es/i.test(nl) ? nl : 'es-ES'; rec.interimResults = true; rec.continuous = true; rec.maxAlternatives = 1;
    let finalT = '';
    rec.onstart = () => { listening = true; if (!held) { stopRec(); return; } micBtn.classList.add('rec'); statusEl.textContent = '🎙 Te escucho…'; };
    rec.onresult = e => { let it = ''; finalT = ''; for (let i = 0; i < e.results.length; i++) { const r = e.results[i]; if (r.isFinal) finalT += r[0].transcript; else it += r[0].transcript; } input.value = (finalT + it).trim(); };
    rec.onerror = e => { statusEl.textContent = e.error === 'not-allowed' ? '🎙 Permite el micrófono en el navegador' : e.error === 'no-speech' ? '' : '🎙 ' + e.error; };
    rec.onend = () => { listening = false; micBtn.classList.remove('rec'); if (!busy && statusEl.textContent.startsWith('🎙 Te')) statusEl.textContent = ''; const t = input.value.trim(); if (t && autoSend) send(t); };
    try { rec.start(); } catch (e) { }
  };

  const openSettings = () => {
    const key = h('input', { type: 'password', placeholder: 'sk-ant-…', value: LS('ganjan.apikey'), style: 'width:100%' });
    const mod = h('select', { onchange: e => LSset('ganjan.model', e.target.value) }, MODELS.map(([v, n]) => h('option', { value: v, selected: v === (LS('ganjan.model') || MODELS[0][0]) }, n)));
    const auto = h('input', { type: 'checkbox', checked: autoSend, onchange: e => { autoSend = e.target.checked; LSset('ganjan.autosend', autoSend ? '1' : '0'); } });
    ui_modal(h('div', { class: 'ag-set' },
      h('h3', null, 'Asistente de Ganjan'),
      h('p', { class: 'hint' }, 'Necesitas una clave de la API de Anthropic (se saca en console.anthropic.com, se paga por uso). Se guarda solo en este navegador de tu computadora. No la compartas ni la pongas en el instalador.'),
      h('div', { class: 'f' }, h('label', null, 'Clave de la API'), key),
      h('div', { class: 'f' }, h('label', null, 'Modelo'), mod),
      h('label', { class: 'swrow', style: 'display:flex;gap:8px;align-items:center;margin:10px 0' }, auto, 'Enviar automáticamente cuando termine de hablar'),
      h('div', { style: 'display:flex;gap:8px;justify-content:flex-end' },
        h('button', { class: 'btn', onclick: () => { history = []; startHi = null; log.textContent = ''; hello(); G.ui.closeModal(); } }, 'Borrar conversación'),
        h('button', { class: 'btn-primary', onclick: () => { LSset('ganjan.apikey', key.value.trim()); G.ui.closeModal(); toast('Guardado'); } }, 'Guardar'))));
  };
  const ui_modal = n => G.ui.modal(n);
  const hello = () => addMsg('bot', 'Hola, soy tu asistente. Mantén apretado 🎙 mientras hablas y suéltalo al terminar, por ejemplo: por ejemplo: «corta el clip en el segundo 10 y ponle un filtro cálido». También puedes escribirme.');

  const build = () => {
    log = h('div', { class: 'ag-log' });
    input = h('textarea', { rows: 1, placeholder: 'Habla con 🎙 o escribe aquí…', onkeydown: e => { e.stopPropagation(); if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); } } });
    input.addEventListener('keyup', e => e.stopPropagation());
    micBtn = h('button', { class: 'ag-mic', title: 'Mantén apretado para hablar, suelta para terminar' }, '🎙');
    const down = e => { e.preventDefault(); try { micBtn.setPointerCapture(e.pointerId); } catch (x) { } held = true; if (!listening) toggleMic(); };
    const up = () => { if (!held) return; held = false; if (listening) stopRec(); else pendingStop = true; };
    micBtn.addEventListener('pointerdown', down); micBtn.addEventListener('pointerup', up); micBtn.addEventListener('pointercancel', up); micBtn.addEventListener('lostpointercapture', up);
    sendBtn = h('button', { class: 'ag-send', title: 'Enviar', onclick: () => send() }, '➤');
    undoBtn = h('button', { class: 'btn hidden', onclick: () => { while (G.hi > startHi) G.undo(); startHi = null; undoBtn.classList.add('hidden'); addMsg('bot', 'Listo, deshice todo lo que hice en esta conversación.'); } }, '↶ Deshacer lo del asistente');
    statusEl = h('span', { class: 'ag-status' });
    panel = h('div', { id: 'agent', class: 'ag hidden' },
      h('div', { class: 'ag-head' }, h('b', null, '✨ Asistente'), h('span', { class: 'spacer' }), h('button', { class: 'icon', title: 'Configuración', onclick: openSettings }, '⚙'), h('button', { class: 'icon', title: 'Cerrar', onclick: () => panel.classList.add('hidden') }, '✕')),
      log, h('div', { class: 'ag-bar' }, statusEl, undoBtn),
      h('div', { class: 'ag-in' }, micBtn, input, sendBtn));
    document.body.append(panel); hello();
    const btn = h('button', { class: 'btn-menu ag-open', title: 'Asistente de IA (voz o texto)', onclick: () => { panel.classList.toggle('hidden'); if (!panel.classList.contains('hidden')) input.focus(); } }, '✨ Asistente');
    $('#top').insertBefore(btn, $('#btnExport'));
  };
  window.addEventListener('DOMContentLoaded', build);
  if (document.readyState !== 'loading') build();
  G.agent = { state, TOOLS, send };
})();
