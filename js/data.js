/* Ganchan - catálogos propios (filtros, textos, stickers, fuentes, sonidos) */
const GC = window.GC = {};

GC.RATIOS = [
  { id: '16:9', w: 16, h: 9 }, { id: '9:16', w: 9, h: 16 }, { id: '1:1', w: 1, h: 1 },
  { id: '4:3', w: 4, h: 3 }, { id: '3:4', w: 3, h: 4 }, { id: '21:9', w: 21, h: 9 }, { id: '4:5', w: 4, h: 5 },
];
GC.sizeFor = (ratioId, short) => {
  const r = GC.RATIOS.find(x => x.id === ratioId) || GC.RATIOS[0];
  let w, h;
  if (r.w >= r.h) { h = short; w = Math.round(short * r.w / r.h); } else { w = short; h = Math.round(short * r.h / r.w); }
  return [w + (w % 2), h + (h % 2)];
};

/* Filtros: b=brillo c=contraste s=saturación sep=sepia hue=giro de tono gray=gris blur=desenfoque
   tint=[[r,g,b,alfa,modo]] */
GC.FILTER_CATS = ['Destacados', 'Vida', 'Cine', 'Paisaje', 'Retro', 'B/N', 'Noche'];
GC.FILTERS = [
  { id: 'none', name: 'Original', cat: 'Destacados' },
  { id: 'vivid', name: 'Vívido', cat: 'Destacados', b: 1.05, c: 1.15, s: 1.5 },
  { id: 'clear', name: 'Claro', cat: 'Destacados', b: 1.1, c: 1.05, s: 1.15 },
  { id: 'soft', name: 'Suave', cat: 'Destacados', b: 1.08, c: .9, s: 1.05, tint: [[255, 220, 230, .15, 'soft-light']] },
  { id: 'pop', name: 'Pop', cat: 'Destacados', c: 1.3, s: 1.7 },
  { id: 'fresh', name: 'Fresco', cat: 'Vida', b: 1.08, s: 1.2, tint: [[120, 220, 255, .14, 'soft-light']] },
  { id: 'cozy', name: 'Acogedor', cat: 'Vida', b: 1.02, c: 1.05, s: 1.1, tint: [[255, 170, 90, .2, 'soft-light']] },
  { id: 'sweet', name: 'Dulce', cat: 'Vida', b: 1.1, c: .92, s: 1.2, tint: [[255, 150, 190, .22, 'soft-light']] },
  { id: 'day', name: 'Día soleado', cat: 'Vida', b: 1.1, c: 1.1, s: 1.3, tint: [[255, 210, 120, .15, 'overlay']] },
  { id: 'cine', name: 'Cinemático', cat: 'Cine', b: .95, c: 1.25, s: .9, tint: [[0, 70, 100, .22, 'soft-light']] },
  { id: 'teal', name: 'Teal y naranja', cat: 'Cine', c: 1.15, s: 1.2, tint: [[255, 120, 40, .16, 'soft-light'], [0, 120, 160, .18, 'overlay']] },
  { id: 'drama', name: 'Dramático', cat: 'Cine', b: .9, c: 1.4, s: .8 },
  { id: 'matte', name: 'Mate', cat: 'Cine', b: 1.05, c: .85, s: .9, tint: [[40, 40, 60, .2, 'lighten']] },
  { id: 'thriller', name: 'Suspenso', cat: 'Cine', b: .85, c: 1.3, s: .6, tint: [[0, 90, 80, .2, 'soft-light']] },
  { id: 'green', name: 'Bosque', cat: 'Paisaje', c: 1.1, s: 1.3, hue: -8, tint: [[40, 160, 60, .15, 'soft-light']] },
  { id: 'ocean', name: 'Océano', cat: 'Paisaje', c: 1.1, s: 1.3, tint: [[0, 120, 220, .22, 'soft-light']] },
  { id: 'sunset', name: 'Atardecer', cat: 'Paisaje', c: 1.1, s: 1.3, tint: [[255, 100, 40, .3, 'soft-light']] },
  { id: 'golden', name: 'Hora dorada', cat: 'Paisaje', b: 1.05, c: 1.1, s: 1.2, tint: [[255, 190, 70, .3, 'soft-light']] },
  { id: 'autumn', name: 'Otoño', cat: 'Paisaje', c: 1.1, s: 1.2, hue: -12, tint: [[230, 120, 30, .22, 'overlay']] },
  { id: 'winter', name: 'Invierno', cat: 'Paisaje', b: 1.08, c: 1.05, s: .8, tint: [[170, 210, 255, .25, 'soft-light']] },
  { id: 'vintage', name: 'Vintage', cat: 'Retro', b: 1.02, c: .95, s: .8, sep: .4, tint: [[255, 200, 130, .12, 'soft-light']] },
  { id: 'film', name: 'Película', cat: 'Retro', c: 1.1, s: .9, sep: .15, tint: [[255, 180, 120, .12, 'overlay']] },
  { id: 'polaroid', name: 'Polaroid', cat: 'Retro', b: 1.1, c: .9, s: .85, sep: .25, tint: [[120, 200, 190, .12, 'soft-light']] },
  { id: 'r80', name: 'Años 80', cat: 'Retro', c: 1.15, s: 1.4, tint: [[255, 0, 160, .16, 'soft-light'], [0, 200, 255, .14, 'overlay']] },
  { id: 'faded', name: 'Desvaído', cat: 'Retro', b: 1.05, c: .8, s: .7, tint: [[200, 200, 200, .2, 'lighten']] },
  { id: 'bw', name: 'Blanco y negro', cat: 'B/N', gray: 1, c: 1.1 },
  { id: 'noir', name: 'Noir', cat: 'B/N', gray: 1, b: .9, c: 1.6 },
  { id: 'silver', name: 'Plata', cat: 'B/N', gray: 1, b: 1.1, c: .9 },
  { id: 'sepia', name: 'Sepia', cat: 'B/N', sep: 1, c: 1.05 },
  { id: 'night', name: 'Noche', cat: 'Noche', b: .85, c: 1.2, s: .9, tint: [[10, 20, 90, .3, 'soft-light']] },
  { id: 'neon', name: 'Neón', cat: 'Noche', b: .95, c: 1.3, s: 1.8, tint: [[255, 0, 200, .18, 'soft-light'], [0, 200, 255, .18, 'overlay']] },
  { id: 'cyber', name: 'Cyberpunk', cat: 'Noche', c: 1.25, s: 1.6, hue: 15, tint: [[120, 0, 255, .25, 'soft-light']] },
  { id: 'moody', name: 'Melancólico', cat: 'Noche', b: .88, c: 1.15, s: .7, tint: [[40, 60, 110, .25, 'soft-light']] },
];
GC.FBYID = Object.fromEntries(GC.FILTERS.map(f => [f.id, f]));

/* Ajustes manuales (panel Ajustar) */
GC.ADJ = [
  ['brightness', 'Brillo'], ['contrast', 'Contraste'], ['saturation', 'Saturación'],
  ['temp', 'Temperatura'], ['hue', 'Tono'], ['fade', 'Desvanecer'],
  ['vignette', 'Viñeta'], ['grain', 'Grano'], ['blur', 'Desenfoque'],
];

GC.FONTS = ['Arial', 'Impact', 'Georgia', 'Verdana', 'Trebuchet MS', 'Courier New', 'Times New Roman',
  'Comic Sans MS', 'Bebas Neue', 'Anton', 'Oswald', 'Montserrat', 'Pacifico', 'Lobster',
  'Permanent Marker', 'Playfair Display'];

GC.TEXT_PRESETS = [
  { name: 'Básico', t: { font: 'Arial', size: 90, bold: true, color: '#ffffff', stroke: '#000000', strokeW: 0, shadow: { c: 'rgba(0,0,0,.6)', b: 8, x: 0, y: 4 } } },
  { name: 'Contorno', t: { font: 'Impact', size: 100, bold: false, color: '#ffffff', stroke: '#000000', strokeW: 12 } },
  { name: 'Subtítulo', t: { font: 'Arial', size: 56, bold: false, color: '#ffffff', bg: 'rgba(0,0,0,.65)' }, y: .36 },
  { name: 'Neón', t: { font: 'Pacifico', size: 100, color: '#ffffff', shadow: { c: '#ff2bd6', b: 40, x: 0, y: 0 }, glow: true } },
  { name: 'Retro', t: { font: 'Bebas Neue', size: 120, color: '#ffe14d', stroke: '#ff3d6e', strokeW: 8, shadow: { c: '#ff3d6e', b: 0, x: 8, y: 8 } } },
  { name: 'Cómic', t: { font: 'Permanent Marker', size: 100, color: '#ffdf00', stroke: '#000000', strokeW: 10 } },
  { name: 'Elegante', t: { font: 'Playfair Display', size: 90, italic: true, color: '#f5e6c8' } },
  { name: 'Manuscrito', t: { font: 'Lobster', size: 100, color: '#ffffff', shadow: { c: 'rgba(0,0,0,.7)', b: 10, x: 2, y: 4 } } },
  { name: 'Caja amarilla', t: { font: 'Montserrat', size: 70, bold: true, color: '#111111', bg: '#ffe14d' } },
  { name: 'Terminal', t: { font: 'Courier New', size: 60, bold: true, color: '#39ff14', bg: 'rgba(0,0,0,.8)' } },
];

GC.STICKERS = {
  'Caras': '😀 😂 🤣 😍 🥰 😎 🤩 😭 😱 🥳 😴 🤔 😡 🤯 😇 😜',
  'Gestos': '👍 👎 👏 🙌 🙏 💪 ✌️ 🤞 👌 👋 🤝 ☝️ 👀 🫶 💅 🤙',
  'Corazones': '❤️ 🧡 💛 💚 💙 💜 🖤 🤍 💔 💖 💗 💘 💝 ❣️ 💕 💞',
  'Símbolos': '⭐ 🌟 ✨ 💥 🔥 💯 ✅ ❌ ❓ ❗ ➡️ ⬅️ ⬆️ ⬇️ 🔔 🎯',
  'Naturaleza': '🌞 🌙 ⭐ ☁️ 🌈 ⚡ ❄️ 🌊 🌸 🌹 🌴 🍀 🌵 🍁 🐶 🐱',
  'Comida': '🍕 🍔 🍟 🌮 🍣 🍩 🍦 🍰 🍎 🍌 🍓 🥑 ☕ 🍺 🍷 🥤',
  'Fiesta': '🎉 🎊 🎈 🎁 🎂 🥂 🎵 🎶 🎤 🎧 📸 🎬 🏆 👑 💎 🚀',
};

GC.SFX = [
  { id: 'whoosh', name: 'Whoosh', d: .9 }, { id: 'pop', name: 'Pop', d: .25 },
  { id: 'ding', name: 'Campanita', d: 1.4 }, { id: 'riser', name: 'Subida', d: 2.5 },
  { id: 'impact', name: 'Impacto', d: 1.6 }, { id: 'laser', name: 'Láser', d: .5 },
  { id: 'coin', name: 'Moneda', d: .6 }, { id: 'click', name: 'Clic', d: .12 },
];

GC.BLENDS = [['source-over', 'Normal'], ['multiply', 'Multiplicar'], ['screen', 'Trama'], ['overlay', 'Superponer'],
  ['lighten', 'Aclarar'], ['darken', 'Oscurecer'], ['soft-light', 'Luz suave'], ['difference', 'Diferencia']];
GC.MASKS = [['', 'Ninguna'], ['circle', 'Círculo'], ['rect', 'Rectángulo'], ['heart', 'Corazón'], ['star', 'Estrella']];
