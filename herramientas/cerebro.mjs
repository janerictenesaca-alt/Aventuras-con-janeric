#!/usr/bin/env node
// Herramientas del cerebro de Nanturia. Sin dependencias (Node 18 o superior).
//
//   node cerebro.mjs validar  --vault <boveda>
//   node cerebro.mjs enlazar  --vault <boveda> --notas <carpeta> [--write] [--ids IH]
//   node cerebro.mjs fusionar --vault <boveda> --sitio <proyecto del sitio> [--write] [--sobrescribir]
//
// Sin --write solo SIMULA: no crea ni modifica ningun archivo.
// Nunca modifica las carpetas de origen del sitio: solo las lee.

import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

const IGNORAR = new Set(['.git', 'node_modules', '.obsidian', '.next', 'dist', 'build', '.venv', 'venv', '__pycache__']);
const ID_RE = /^[AIHDRVN]\d{2}$/;

// ---------------------------------------------------------------- utilidades
function parseArgs(argv) {
  const [cmd, ...rest] = argv;
  const opts = {};
  for (let i = 0; i < rest.length; i++) {
    const a = rest[i];
    if (!a.startsWith('--')) continue;
    const key = a.slice(2);
    const next = rest[i + 1];
    if (next === undefined || next.startsWith('--')) opts[key] = true;
    else {
      opts[key] = next;
      i++;
    }
  }
  return { cmd, opts };
}

function walk(dir, exts = null, out = []) {
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    if (IGNORAR.has(e.name)) continue;
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, exts, out);
    else if (!exts || exts.includes(path.extname(e.name).toLowerCase())) out.push(p);
  }
  return out;
}

// Lee un archivo detectando UTF-8 (con o sin BOM) y UTF-16 (lo que genera `>` en Windows PowerShell 5.1).
function leer(p) {
  const buf = fs.readFileSync(p);
  let enc = 'utf8';
  let bom = false;
  let text;
  if (buf.length >= 2 && buf[0] === 0xff && buf[1] === 0xfe) {
    enc = 'utf16le';
    text = buf.subarray(2).toString('utf16le');
  } else if (buf.length >= 2 && buf[0] === 0xfe && buf[1] === 0xff) {
    enc = 'utf16be';
    const sw = Buffer.from(buf.subarray(2));
    if (sw.length % 2 === 0) sw.swap16();
    text = sw.toString('utf16le');
  } else {
    if (buf.length >= 3 && buf[0] === 0xef && buf[1] === 0xbb && buf[2] === 0xbf) bom = true;
    text = buf.toString('utf8').replace(/^﻿/, '');
  }
  return { text, enc, bom };
}

function indexar(vault) {
  const todos = walk(vault);
  const mds = todos.filter((p) => path.extname(p).toLowerCase() === '.md');
  const porBase = new Map();
  const porRuta = new Map();
  const porArchivo = new Map();
  for (const p of mds) {
    const k = path.basename(p, '.md').toLowerCase();
    if (!porBase.has(k)) porBase.set(k, []);
    porBase.get(k).push(p);
    const rel = path.relative(vault, p).split(path.sep).join('/').replace(/\.md$/i, '').toLowerCase();
    porRuta.set(rel, p);
  }
  for (const p of todos) porArchivo.set(path.basename(p).toLowerCase(), p);
  return { mds, porBase, porRuta, porArchivo };
}

// Quita bloques de codigo (con respeto a longitud de la cerca) y codigo en linea. Devuelve el texto restante.
function quitarCodigo(text) {
  const out = [];
  let enFence = false;
  let fenceCh = '';
  let fenceLen = 0;
  for (const linea of text.split(/\r?\n/)) {
    const m = /^\s*(`{3,}|~{3,})(.*)$/.exec(linea);
    if (m) {
      if (!enFence) {
        enFence = true;
        fenceCh = m[1][0];
        fenceLen = m[1].length;
      } else if (m[1][0] === fenceCh && m[1].length >= fenceLen && m[2].trim() === '') {
        enFence = false;
      }
      continue;
    }
    if (!enFence) out.push(linea.replace(/`[^`\n]*`/g, ''));
  }
  return out.join('\n');
}

function encabezados(p) {
  const hs = new Set();
  for (const linea of quitarCodigo(leer(p).text).split('\n')) {
    const m = /^#{1,6}\s+(.*)$/.exec(linea);
    if (m) hs.add(m[1].trim());
  }
  return hs;
}

// ---------------------------------------------------------------- mapa de identificadores
function mapaIds(idx) {
  const ids = new Map();
  for (const p of idx.mds) {
    const base = path.basename(p, '.md');
    const m = /^([AIN]\d{2}) /.exec(base);
    if (m && !ids.has(m[1])) ids.set(m[1], { archivo: base, heading: null, ruta: p });
  }
  const hubs = { H: 'N03', D: 'N04', R: 'N08', V: 'N09' };
  for (const [letra, hub] of Object.entries(hubs)) {
    const info = ids.get(hub);
    if (!info) continue;
    for (const linea of leer(info.ruta).text.split(/\r?\n/)) {
      const m = /^## ([HDRV]\d\d) (.+)$/.exec(linea.trim());
      if (m && m[1][0] === letra) ids.set(m[1], { archivo: info.archivo, heading: `${m[1]} ${m[2].trim()}`, ruta: info.ruta });
    }
  }
  return ids;
}

function enlace(id, info, tabla, alias = null) {
  const barra = tabla ? '\\|' : '|';
  const texto = alias !== null && alias !== '' ? alias : id;
  return info.heading ? `[[${info.archivo}#${info.heading}${barra}${texto}]]` : `[[${info.archivo}${barra}${texto}]]`;
}

// ---------------------------------------------------------------- enlazar
const PROTEGIDOS = /(`[^`\n]*`)|(\[\[[^\]\n]*\]\])|(\[[^\]\n]*\]\([^)\n]*\))|(https?:\/\/[^\s)>\]]+)|(\b[AIHDRVN]\d{2}\b)/g;

function normalizarWiki(m, ids, idx, tabla, stats, letras) {
  const inner = m.slice(2, -2);
  let sep = null;
  if (inner.includes('\\|')) sep = '\\|';
  else if (inner.includes('|')) sep = '|';
  const pos = sep ? inner.indexOf(sep) : -1;
  const destinoRaw = sep ? inner.slice(0, pos) : inner;
  const alias = sep ? inner.slice(pos + sep.length) : null;
  const hashPos = destinoRaw.indexOf('#');
  const destino = (hashPos >= 0 ? destinoRaw.slice(0, hashPos) : destinoRaw).trim();
  const heading = hashPos >= 0 ? destinoRaw.slice(hashPos + 1) : null;

  // 1) identificador suelto: [[I07]] o [[I07|texto]]
  if (ID_RE.test(destino) && letras.has(destino[0]) && ids.has(destino) && heading === null) {
    stats.ids++;
    return enlace(destino, ids.get(destino), tabla, alias);
  }
  // 2) ruta con carpeta que ya no existe: usar el nombre del archivo si es unico en la boveda
  if (destino.includes('/') && !idx.porRuta.has(destino.toLowerCase().replace(/\.md$/, ''))) {
    const base = path.posix.basename(destino).replace(/\.md$/i, '').toLowerCase();
    const c = idx.porBase.get(base);
    if (c && c.length === 1) {
      stats.rutas++;
      const barra = tabla ? '\\|' : '|';
      return `[[${path.basename(c[0], '.md')}${heading !== null ? '#' + heading : ''}${alias !== null ? barra + alias : ''}]]`;
    }
  }
  return m;
}

function enlazarLinea(linea, ids, idx, stats, letras) {
  const tabla = linea.trimStart().startsWith('|');
  return linea.replace(PROTEGIDOS, (m, code, wiki, md, url, id) => {
    if (code || md || url) return m;
    if (wiki) return normalizarWiki(m, ids, idx, tabla, stats, letras);
    if (id && letras.has(id[0]) && ids.has(id)) {
      stats.ids++;
      return enlace(id, ids.get(id), tabla);
    }
    return m;
  });
}

function enlazarTexto(text, ids, idx, stats, letras) {
  const partes = text.split(/(\r?\n)/); // linea, separador, linea, ...
  let enFM = false;
  let enFence = false;
  let fenceCh = '';
  let fenceLen = 0;
  for (let i = 0; i < partes.length; i += 2) {
    const linea = partes[i];
    const t = linea.trim();
    if (i === 0 && t === '---') {
      enFM = true;
      continue;
    }
    if (enFM) {
      if (t === '---') enFM = false;
      continue;
    }
    const m = /^\s*(`{3,}|~{3,})(.*)$/.exec(linea);
    if (m) {
      if (!enFence) {
        enFence = true;
        fenceCh = m[1][0];
        fenceLen = m[1].length;
      } else if (m[1][0] === fenceCh && m[1].length >= fenceLen && m[2].trim() === '') {
        enFence = false;
      }
      continue;
    }
    if (enFence) continue;
    if (/^#{1,6}\s/.test(linea)) continue; // no tocar encabezados
    partes[i] = enlazarLinea(linea, ids, idx, stats, letras);
  }
  return partes.join('');
}

function cmdEnlazar(opts, silencioso = false) {
  const vault = path.resolve(opts.vault ?? '.');
  if (!opts.notas) fallar('Falta --notas <carpeta con las notas a enlazar>.');
  const notas = path.resolve(opts.notas);
  if (!fs.existsSync(notas)) fallar(`No existe la carpeta de notas: ${notas}`);
  const escribir = !!opts.write;
  const letras = new Set(typeof opts.ids === 'string' ? opts.ids.toUpperCase().split('') : ['I', 'H']);
  const idx = indexar(vault);
  const ids = mapaIds(idx);
  if (!ids.has('N03')) fallar('No encuentro "N03 Hallazgos criticos" en la boveda. ¿--vault apunta a Aventuras-con-janeric?');

  let totalIds = 0;
  let totalRutas = 0;
  let archivosCambiados = 0;
  let reparados = 0;
  const lineas = [];
  for (const p of walk(notas, ['.md'])) {
    const info = leer(p);
    const stats = { ids: 0, rutas: 0 };
    const nuevo = enlazarTexto(info.text, ids, idx, stats, letras);
    const cambiado = nuevo !== info.text;
    const reparar = info.enc !== 'utf8' || info.bom;
    if (cambiado) archivosCambiados++;
    if (reparar) reparados++;
    totalIds += stats.ids;
    totalRutas += stats.rutas;
    if (cambiado || reparar) {
      lineas.push(`  ${path.relative(vault, p)}  (ids: ${stats.ids}, rutas corregidas: ${stats.rutas}${reparar ? ', reparado a UTF-8' : ''})`);
      if (escribir) fs.writeFileSync(p, nuevo, 'utf8');
    }
  }
  if (!silencioso || escribir) {
    console.log(`${escribir ? 'ENLAZAR (aplicado)' : 'ENLAZAR (simulacion, usa --write para aplicar)'} · ${path.relative(vault, notas) || '.'} · identificadores: ${letras.size ? [...letras].join('') : 'ninguno (solo rutas)'}`);
    for (const l of lineas) console.log(l);
    console.log(`Archivos con cambios: ${archivosCambiados} · identificadores enlazados: ${totalIds} · rutas corregidas: ${totalRutas} · archivos reparados a UTF-8: ${reparados}`);
  }
  return { archivosCambiados, totalIds, totalRutas, reparados };
}

// ---------------------------------------------------------------- validar
function cmdValidar(opts, silencioso = false) {
  const vault = path.resolve(opts.vault ?? '.');
  const idx = indexar(vault);
  let total = 0;
  const rotos = [];
  const ambiguos = new Set();
  const inseguros = [];
  const utf16 = [];
  const conBom = [];
  const cacheHeads = new Map();
  const linkRe = /\[\[([^\]|#]+)(?:#([^\]|]+))?(?:\|([^\]]+))?\]\]/g;

  for (const p of idx.mds) {
    const rel = path.relative(vault, p);
    const info = leer(p);
    if (info.enc !== 'utf8') utf16.push(rel);
    else if (info.bom) conBom.push(rel);
    const nombre = path.basename(p);
    if (/[:?*"<>|]/.test(nombre) || /[. ]$/.test(path.basename(p, '.md'))) inseguros.push(rel);

    const texto = quitarCodigo(info.text).replace(/\\\|/g, '|');
    for (const m of texto.matchAll(linkRe)) {
      total++;
      const destino = m[1].trim();
      const head = m[2];
      const clave = destino.toLowerCase().replace(/\.md$/, '');
      let dest = null;
      if (/\.[a-z0-9]{2,5}$/i.test(destino) && !/\.md$/i.test(destino)) {
        dest = idx.porArchivo.get(path.basename(destino).toLowerCase()) ?? null; // adjunto
      } else if (clave.includes('/')) {
        dest = idx.porRuta.get(clave) ?? null;
      } else {
        const c = idx.porBase.get(clave) ?? [];
        if (c.length === 1) dest = c[0];
        else if (c.length > 1) {
          ambiguos.add(`${path.basename(p)} -> ${destino}`);
          dest = c[0];
        }
      }
      if (!dest) {
        rotos.push([rel, m[0], 'archivo inexistente']);
        continue;
      }
      if (head && path.extname(dest).toLowerCase() === '.md') {
        if (!cacheHeads.has(dest)) cacheHeads.set(dest, encabezados(dest));
        if (!cacheHeads.get(dest).has(head.trim())) rotos.push([rel, m[0], 'encabezado inexistente']);
      }
    }
  }

  // nombres de archivo repetidos entre carpetas (pueden volver ambiguos los enlaces)
  const repetidos = [];
  for (const [k, v] of idx.porBase) if (v.length > 1) repetidos.push(`${k}: ${v.map((x) => path.relative(vault, x)).join(' | ')}`);

  const ok = rotos.length === 0 && utf16.length === 0 && inseguros.length === 0;
  if (!silencioso || !ok) {
    console.log(`VALIDAR ${vault}`);
    console.log(`Archivos .md: ${idx.mds.length} · enlaces revisados: ${total}`);
    console.log(`Enlaces rotos: ${rotos.length}`);
    for (const r of rotos.slice(0, 80)) console.log(`  - ${r[0]}  ${r[1]}  (${r[2]})`);
    if (rotos.length > 80) console.log(`  ... y ${rotos.length - 80} mas`);
    console.log(`Enlaces ambiguos (mismo nombre en varias carpetas): ${ambiguos.size}`);
    for (const a of [...ambiguos].slice(0, 20)) console.log(`  - ${a}`);
    console.log(`Nombres repetidos entre carpetas: ${repetidos.length}`);
    for (const r of repetidos.slice(0, 20)) console.log(`  - ${r}`);
    console.log(`Nombres inseguros para Windows: ${inseguros.length}${inseguros.length ? '\n  - ' + inseguros.join('\n  - ') : ''}`);
    console.log(`Archivos en UTF-16 (se reparan con "enlazar --write"): ${utf16.length}${utf16.length ? '\n  - ' + utf16.join('\n  - ') : ''}`);
    console.log(`Archivos UTF-8 con BOM: ${conBom.length}`);
    console.log(ok ? 'RESULTADO: OK' : 'RESULTADO: HAY PROBLEMAS');
  }
  return { ok, rotos: rotos.length, utf16: utf16.length, inseguros: inseguros.length, repetidos: repetidos.length };
}

// ---------------------------------------------------------------- fusionar
function copiar(src, dst, sobrescribir) {
  const archivos = walk(src);
  let n = 0;
  for (const f of archivos) {
    const destino = path.join(dst, path.relative(src, f));
    fs.mkdirSync(path.dirname(destino), { recursive: true });
    fs.copyFileSync(f, destino, sobrescribir ? 0 : fs.constants.COPYFILE_EXCL);
    n++;
  }
  return n;
}

function cmdFusionar(opts) {
  if (!opts.vault) fallar('Falta --vault <carpeta Aventuras-con-janeric>.');
  const vault = path.resolve(opts.vault);
  const sitio = path.resolve(opts.sitio ?? '.');
  const escribir = !!opts.write;
  const sobre = !!opts.sobrescribir;
  if (!fs.existsSync(path.join(vault, 'cerebro nanturia'))) fallar(`No veo "cerebro nanturia" dentro de ${vault}. ¿Clonaste la rama correcta?`);
  if (!fs.existsSync(sitio)) fallar(`No existe la carpeta del sitio: ${sitio}`);

  const raiz = path.join(vault, 'cerebro nanturia', 'sitio web');
  const fuentes = [
    ['cerebro-sitio-web', 'auditoria'],
    ['cerebro', 'proyecto'],
  ];
  const plan = [];
  for (const [carpeta, destino] of fuentes) {
    const src = path.join(sitio, carpeta);
    if (!fs.existsSync(src) || !fs.statSync(src).isDirectory()) {
      console.log(`- No encontre ${src} (se omite)`);
      continue;
    }
    const dst = path.join(raiz, destino);
    plan.push({ src, dst, n: walk(src).length, existe: fs.existsSync(dst) });
  }
  if (!plan.length) fallar('No encontre ninguna carpeta de origen (cerebro-sitio-web, cerebro). Usa --sitio para indicar la raiz del proyecto del sitio.');

  console.log(escribir ? 'FUSIONAR (aplicado)' : 'FUSIONAR (simulacion, usa --write para aplicar)');
  for (const p of plan) console.log(`- ${p.src}  ->  ${p.dst}   (${p.n} archivos${p.existe ? ', YA EXISTE el destino' : ''})`);
  const bloqueados = plan.filter((p) => p.existe && !sobre);
  if (bloqueados.length) fallar('El destino ya existe. No se sobrescribe nada. Usa --sobrescribir si de verdad quieres reemplazarlo.');
  if (!escribir) {
    console.log('Simulacion terminada: no se copio ni se modifico nada.');
    return;
  }

  for (const p of plan) {
    const n = copiar(p.src, p.dst, sobre);
    console.log(`  copiados ${n} archivos a ${path.relative(vault, p.dst)}`);
  }
  console.log('');
  const aud = path.join(raiz, 'auditoria');
  const pro = path.join(raiz, 'proyecto');
  const ide = typeof opts.ids === 'string' ? opts.ids : 'IH';
  if (fs.existsSync(aud)) cmdEnlazar({ vault, notas: aud, write: true, ids: ide });
  if (fs.existsSync(pro)) cmdEnlazar({ vault, notas: pro, write: true, ids: '' }); // el cerebro del proyecto tiene su propia numeracion: solo se corrigen rutas
  console.log('');
  const r = cmdValidar({ vault });
  console.log('');
  console.log('Siguiente paso: abre la carpeta de la boveda en Obsidian ("Open folder as vault").');
  console.log('Las carpetas originales del sitio no se tocaron.');
  if (!r.ok) process.exitCode = 1;
}

// ---------------------------------------------------------------- main
function fallar(msg) {
  console.error(`ERROR: ${msg}`);
  process.exit(2);
}

const AYUDA = `Uso:
  node cerebro.mjs validar  --vault <boveda>
  node cerebro.mjs enlazar  --vault <boveda> --notas <carpeta> [--write] [--ids IH]
  node cerebro.mjs fusionar --vault <boveda> --sitio <proyecto del sitio> [--write] [--sobrescribir]

Sin --write solo simula. La boveda es la carpeta Aventuras-con-janeric (la que contiene "cerebro nanturia").`;

const { cmd, opts } = parseArgs(process.argv.slice(2));
if (cmd === 'validar') {
  const r = cmdValidar(opts);
  process.exitCode = r.ok ? 0 : 1;
} else if (cmd === 'enlazar') cmdEnlazar(opts);
else if (cmd === 'fusionar') cmdFusionar(opts);
else {
  console.log(AYUDA);
  process.exitCode = cmd ? 2 : 0;
}
