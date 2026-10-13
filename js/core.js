/* Ganchan - utilidades de interfaz compartidas */
(function () {
  const $ = s => document.querySelector(s);
  const h = (tag, attrs, ...kids) => {
    const e = document.createElement(tag);
    for (const k in (attrs || {})) {
      const v = attrs[k]; if (v == null || v === false) continue;
      if (k === 'class') e.className = v; else if (k === 'style') e.style.cssText = v; else if (k.startsWith('on')) e.addEventListener(k.slice(2), v);
      else if (k === 'checked' || k === 'selected' || k === 'disabled' || k === 'value') e[k] = v; else e.setAttribute(k, v === true ? '' : v);
    }
    kids.flat().forEach(k => { if (k != null && k !== false) e.append(k.nodeType ? k : document.createTextNode(k)); });
    return e;
  };
  const ui = G.ui = { libTab: 'media', libCat: {}, libOpen: {}, libSearch: '', insTab: null, insSub: {}, animTab: 'in', hslColor: 'red', magnet: true, layout: 'media', clipboard: null };
  const fmt = t => { const fps = G.project.fps, f = Math.floor((t % 1) * fps + 1e-6), s = Math.floor(t) % 60, m = Math.floor(t / 60) % 60, hh = Math.floor(t / 3600), p = n => String(n).padStart(2, '0'); return `${p(hh)}:${p(m)}:${p(s)}:${p(f)}`; };
  const fmtS = t => { const m = Math.floor(t / 60), s = Math.floor(t % 60); return String(m).padStart(2, '0') + ':' + String(s).padStart(2, '0'); };
  const toast = msg => { const t = $('#toast'); t.textContent = msg; t.classList.remove('hidden'); clearTimeout(toast._t); toast._t = setTimeout(() => t.classList.add('hidden'), 2400); };
  Object.assign(ui, { $, h, fmt, fmtS, toast });

  /* menú desplegable anclado a un botón */
  let openPop = null;
  const closePop = () => { if (openPop) { openPop.remove(); openPop = null; } };
  document.addEventListener('pointerdown', e => { if (openPop && !openPop.contains(e.target) && !e.target.closest('[data-pop]')) closePop(); }, true);
  ui.closePop = closePop;
  ui.popMenu = (anchor, items, opts = {}) => {
    closePop(); const r = anchor.getBoundingClientRect();
    const m = h('div', { class: 'menu pop', style: `position:fixed;left:${r.left}px;${opts.up ? `bottom:${innerHeight - r.top + 4}px` : `top:${r.bottom + 4}px`};min-width:${Math.max(140, r.width)}px;z-index:90` });
    items.forEach(it => m.append(h('div', { class: 'it' + (it.on ? ' chk' : ''), onclick: () => { closePop(); it.fn && it.fn(); } }, (it.on ? '✓ ' : '') + it.label)));
    document.body.append(m); openPop = m; return m;
  };

  /* controles */
  ui.sl = (label, val, min, max, step, onIn, unit = '', opts = {}) => {
    const num = h('input', { class: 'num', type: 'number', min, max, step, value: +(+val).toFixed(2) }), rng = h('input', { type: 'range', min, max, step, value: val });
    const set = v => { v = G.clamp(+v, min, max); if (isNaN(v)) return; num.value = +v.toFixed(2); rng.value = v; onIn(v); G.touch(); G.save(); };
    rng.addEventListener('input', () => set(rng.value)); rng.addEventListener('change', () => { G.commit(); opts.after && opts.after(); });
    num.addEventListener('change', () => { set(num.value); G.commit(); opts.after && opts.after(); });
    return h('div', { class: 'f' }, h('div', { class: 'lab' }, h('span', null, label), h('span', null, num, unit)), rng);
  };
  ui.sel = (label, val, opts, onChange) => h('div', { class: 'f' }, label ? h('label', null, label) : null, h('select', { onchange: e => { onChange(e.target.value); G.touch(); G.commit(); } }, opts.map(([v, n]) => h('option', { value: v, selected: v === val }, n))));
  ui.sw = (label, on, fn, note) => h('div', { class: 'f swrow' }, h('div', null, h('span', null, label), note ? h('div', { class: 'hint', style: 'margin:2px 0 0' }, note) : null), h('label', { class: 'switch' }, h('input', { type: 'checkbox', checked: !!on, onchange: e => fn(e.target.checked) }), h('i')));
  ui.section = (title, reset, ...kids) => h('div', { class: 'psec' }, h('div', { class: 'ptitle' }, h('b', null, title), reset ? h('button', { class: 'icon', title: 'Restablecer', onclick: reset }, '↺') : null), ...kids);
  ui.seg = (items, cur, onPick) => h('div', { class: 'seg' }, items.map(n => h('button', { class: n === cur ? 'on' : '', onclick: () => onPick(n) }, n)));
  ui.modal = node => { $('#modalBox').innerHTML = ''; $('#modalBox').append(node); $('#modal').classList.remove('hidden'); };
  ui.closeModal = () => $('#modal').classList.add('hidden');
  ui.refreshAll = () => { ui.libBody(); ui.inspector(); };
})();
