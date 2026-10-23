#!/usr/bin/env node
// Clipper de investigación (solo lectura). Código propio; no depende de Nimbus ni de extensiones.
// Uso: node research/herramientas/clipper.mjs <url> [--sitio=capinita] [--captura] [--movil]
// Hace: abre la página pública en un Chrome aparte (perfil temporal), la observa SIN hacer clic ni enviar nada,
// y guarda un resumen estructurado en research/clips/. No guarda el texto completo ni descarga recursos.
import { spawn } from 'node:child_process';
import { mkdtempSync, mkdirSync, existsSync, readFileSync, writeFileSync, appendFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';

const AQUI = dirname(fileURLToPath(import.meta.url));
const RAIZ = resolve(AQUI, '..');              // carpeta research/
const CLIPS = join(RAIZ, 'clips');
const args = process.argv.slice(2);
const url = args.find(a => /^https?:\/\//i.test(a));
const opt = Object.fromEntries(args.filter(a => a.startsWith('--')).map(a => { const [k, v] = a.slice(2).split('='); return [k, v ?? true]; }));
if (!url) { console.error('Falta la URL (http/https).'); process.exit(2); }

// 1) Solo sitios autorizados por el usuario (lista en research/clips/sitios-autorizados.txt)
const autorizados = existsSync(join(CLIPS, 'sitios-autorizados.txt'))
  ? readFileSync(join(CLIPS, 'sitios-autorizados.txt'), 'utf8').split(/\r?\n/).map(l => l.trim().toLowerCase()).filter(l => l && !l.startsWith('#')) : [];
const host = new URL(url).hostname.toLowerCase().replace(/^www\./, '');
if (!autorizados.includes(host)) { console.error(`Sitio no autorizado: ${host}. Añádelo a research/clips/sitios-autorizados.txt solo si el usuario lo indicó.`); process.exit(3); }

const sitio = (opt.sitio || host.split('.')[0]).toLowerCase().replace(/[^a-z0-9-]/g, '');
const norm = u => { const x = new URL(u); x.hash = ''; x.searchParams.delete('utm_source'); return (x.origin.replace('://www.', '://') + x.pathname.replace(/\/$/, '') + x.search).toLowerCase(); };
const slug = (new URL(url).pathname.replace(/^\/|\/$/g, '').replace(/[^a-zA-Z0-9]+/g, '-') || 'inicio').toLowerCase().slice(0, 80) + (new URL(url).search ? '-' + createHash('sha1').update(new URL(url).search).digest('hex').slice(0, 6) : '');
const hoy = new Date().toISOString();
const dia = hoy.slice(0, 10);

// 2) Chrome aparte, perfil temporal
const chrome = process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const port = 9400 + Math.floor(Math.random() * 90);
const perfil = mkdtempSync(join(tmpdir(), 'clip-'));
const ancho = opt.movil ? 390 : 1366, alto = opt.movil ? 844 : 900;
const proc = spawn(chrome, ['--headless=new', '--disable-gpu', `--remote-debugging-port=${port}`, `--user-data-dir=${perfil}`, `--window-size=${Math.max(ancho, 500)},${alto}`, 'about:blank'], { stdio: 'ignore' });
const dormir = ms => new Promise(r => setTimeout(r, ms));
let ws, id = 0; const pend = new Map(); const ev = [];
const send = (method, params = {}) => new Promise(r => { const i = ++id; pend.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
const salir = c => { try { ws?.close(); } catch {} try { proc.kill(); } catch {} setTimeout(() => { try { rmSync(perfil, { recursive: true, force: true }); } catch {} process.exit(c); }, 300); };

try {
  for (let i = 0; i < 40; i++) { try { await fetch(`http://127.0.0.1:${port}/json/version`); break; } catch { await dormir(300); } }
  const tabs = await (await fetch(`http://127.0.0.1:${port}/json`)).json();
  ws = new WebSocket(tabs.find(t => t.type === 'page').webSocketDebuggerUrl);
  await new Promise(r => (ws.onopen = r));
  ws.onmessage = async m => {
    const d = JSON.parse(m.data);
    if (d.id && pend.has(d.id)) { pend.get(d.id)(d); pend.delete(d.id); return; }
    // Solo lectura: se bloquea cualquier petición que no sea GET/HEAD (p. ej. beacons de analítica)
    if (d.method === 'Fetch.requestPaused') {
      const ok = ['GET', 'HEAD', 'OPTIONS'].includes(d.params.request.method);
      send(ok ? 'Fetch.continueRequest' : 'Fetch.failRequest', ok ? { requestId: d.params.requestId } : { requestId: d.params.requestId, errorReason: 'BlockedByClient' });
      if (!ok) ev.push({ method: 'bloqueada', params: { m: d.params.request.method, u: d.params.request.url } });
      return;
    }
    ev.push(d);
  };
  for (const d of ['Network', 'Runtime', 'Log', 'Page']) await send(`${d}.enable`);
  await send('Network.setBlockedURLs', { urls: ['*google-analytics.com*', '*googletagmanager.com*', '*doubleclick.net*'] }); // no ensuciar su analítica
  await send('Fetch.enable', { patterns: [{ urlPattern: '*' }] });
  if (opt.movil) await send('Emulation.setDeviceMetricsOverride', { width: 390, height: 844, deviceScaleFactor: 2, mobile: true });
  await send('Page.navigate', { url });
  await dormir(7000);

  const r = await send('Runtime.evaluate', { returnByValue: true, expression: `(()=>{
    const cut=(s,n)=>(s||'').replace(/\\s+/g,' ').trim().slice(0,n);
    const meta=(n)=>document.querySelector('meta[name="'+n+'"],meta[property="'+n+'"]')?.content||'';
    const vis=e=>{const r=e.getBoundingClientRect();return r.width>0&&r.height>0};
    const uniq=(a,k)=>{const s=new Set();return a.filter(x=>{const key=k(x);if(s.has(key))return false;s.add(key);return true})};
    const outline=[...document.querySelectorAll('h1,h2,h3')].filter(vis).map(h=>({n:h.tagName,t:cut(h.innerText,90)})).filter(h=>h.t).slice(0,45);
    const links=[...document.querySelectorAll('nav a,aside a,header a,footer a')].map(a=>({t:cut(a.innerText||a.getAttribute('aria-label'),40),h:(()=>{try{const u=new URL(a.href);return u.origin===location.origin?u.pathname+u.search:u.origin}catch{return ''}})()})).filter(l=>l.h);
    const nav=uniq(links,l=>l.t+l.h).slice(0,50);
    const txt=document.body.innerText;
    const precios=uniq(txt.split('\\n').filter(l=>/\\$\\s?\\d/.test(l)).map(l=>cut(l,80)),x=>x).slice(0,20);
    const forms=[...document.querySelectorAll('form')].map(f=>({campos:[...f.querySelectorAll('input,select,textarea')].filter(i=>i.type!=='hidden').map(i=>({tipo:i.type||i.tagName.toLowerCase(),etiqueta:cut(i.labels?.[0]?.innerText||i.placeholder||i.name||i.id,50),requerido:!!i.required,autocomplete:i.autocomplete||''})),botones:[...f.querySelectorAll('button')].map(b=>cut(b.innerText,30)).filter(Boolean)}));
    const cta=uniq([...document.querySelectorAll('main a,main button')].filter(vis).map(e=>cut(e.innerText,40)).filter(t=>t&&t.length<40),x=>x).slice(0,30);
    const cs=(e,p)=>e?getComputedStyle(e)[p]:'';
    const btn=[...document.querySelectorAll('main button,main a')].find(e=>vis(e)&&cs(e,'backgroundColor')!=='rgba(0, 0, 0, 0)');
    const diseno={fuenteCuerpo:cs(document.body,'fontFamily').slice(0,80),fuenteTitulo:cs(document.querySelector('h1'),'fontFamily').slice(0,80),tamH1:cs(document.querySelector('h1'),'fontSize'),colorTexto:cs(document.body,'color'),fondo:cs(document.body,'backgroundColor'),boton:btn?{fondo:cs(btn,'backgroundColor'),texto:cs(btn,'color'),radio:cs(btn,'borderRadius')}:null,ancho:innerWidth,desbordeHorizontal:document.documentElement.scrollWidth>innerWidth+2};
    const imgs=[...document.images];
    const medios={imagenes:imgs.length,picture:document.querySelectorAll('picture').length,sinAlt:imgs.filter(i=>!i.alt).length,lazy:imgs.filter(i=>i.loading==='lazy').length,svg:document.querySelectorAll('svg').length};
    const sc=[...document.scripts].map(s=>s.src).filter(Boolean).map(s=>{try{return new URL(s).host}catch{return ''}});
    const tecnologia={generator:meta('generator'),next:!!window.__next_f||!!window.next,react:!!document.querySelector('[data-reactroot]')||!!window.__next_f,leaflet:!!window.L,hostsScripts:[...new Set(sc)].slice(0,10),cookiesJS:document.cookie?document.cookie.split(';').map(c=>c.split('=')[0].trim()):[]};
    const norm=(txt||'').replace(/\\d{1,2}:\\d{2}(:\\d{2})?/g,'').replace(/\\s+/g,' ').trim();
    return {finalUrl:location.href,canonica:document.querySelector('link[rel=canonical]')?.href||'',titulo:document.title,sitioMeta:meta('og:site_name'),descripcion:cut(meta('description'),300),idioma:document.documentElement.lang,outline,nav,precios,forms,cta,diseno,medios,tecnologia,palabras:norm.split(' ').length,huella:norm};
  })()` });
  const dat = r.result?.result?.value;
  if (!dat) throw new Error('No se pudo leer la página: ' + JSON.stringify(r.result?.exceptionDetails || r.result).slice(0, 200));
  const huella = createHash('sha256').update(dat.huella).digest('hex').slice(0, 16); delete dat.huella;

  // Red y errores
  const reqs = new Map(), resp = new Map();
  for (const e of ev) {
    if (e.method === 'Network.requestWillBeSent') reqs.set(e.params.requestId, { url: e.params.request.url, type: e.params.type });
    if (e.method === 'Network.responseReceived') resp.set(e.params.requestId, e.params.response.status);
  }
  const docId = [...reqs].find(([, v]) => v.type === 'Document')?.[0];
  const estado = docId ? resp.get(docId) : null;
  const porHost = {}; for (const [, v] of reqs) { const h = new URL(v.url).host; porHost[h] = (porHost[h] || 0) + 1; }
  const errores = {
    http: [...reqs].filter(([k]) => (resp.get(k) || 0) >= 400).map(([k, v]) => `${resp.get(k)} ${v.url.slice(0, 100)}`).slice(0, 10),
    consola: ev.filter(e => e.method === 'Runtime.consoleAPICalled' && e.params.type === 'error').map(e => (e.params.args || []).map(a => a.value ?? a.description ?? '').join(' ').slice(0, 160)).slice(0, 5),
    excepciones: ev.filter(e => e.method === 'Runtime.exceptionThrown').map(e => (e.params.exceptionDetails.exception?.description || e.params.exceptionDetails.text).split('\n')[0].slice(0, 160)).slice(0, 5),
    bloqueadasPorSerSoloLectura: ev.filter(e => e.method === 'bloqueada').length,
  };

  // Captura solo si se pide
  let captura = null;
  if (opt.captura) {
    const s = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: true, clip: { x: 0, y: 0, width: ancho, height: Math.min(2400, 2400), scale: 1 } });
    mkdirSync(join(RAIZ, 'capturas', sitio), { recursive: true });
    captura = `capturas/${sitio}/${slug}-${opt.movil ? 'movil' : 'escritorio'}-${dia}.png`;
    writeFileSync(join(RAIZ, captura), Buffer.from(s.result.data, 'base64'));
  }

  // 3) Registro acumulativo con deduplicación (clave = URL normalizada)
  mkdirSync(join(CLIPS, sitio), { recursive: true });
  const idxPath = join(CLIPS, 'indice.json');
  const idx = existsSync(idxPath) ? JSON.parse(readFileSync(idxPath, 'utf8')) : {};
  const clave = norm(url), previo = idx[clave];
  const archivo = `clips/${sitio}/${slug}.md`;
  const f = n => (n ?? '').toString();
  const tabla = (filas, cab) => filas.length ? `| ${cab.join(' | ')} |\n|${cab.map(() => '---').join('|')}|\n` + filas.map(x => `| ${x.map(c => f(c).replace(/\|/g, '/')).join(' | ')} |`).join('\n') + '\n' : '_ninguno_\n';
  const bloque = `
### Consulta ${hoy} · ${opt.movil ? 'móvil 390 px' : 'escritorio 1366 px'}${previo ? (previo.huella === huella ? ' · SIN CAMBIOS' : ' · CONTENIDO CAMBIÓ') : ' · primera consulta'}
- **URL exacta consultada:** ${url}
- **URL final:** ${dat.finalUrl}${dat.canonica ? ` · canónica: ${dat.canonica}` : ''}
- **Título:** ${dat.titulo} · **Sitio:** ${dat.sitioMeta || sitio} · **Idioma:** ${dat.idioma || '?'} · **Estado HTTP:** ${estado ?? 'no registrado'} · **Palabras visibles:** ~${dat.palabras} · **Huella de contenido:** \`${huella}\`
- **Descripción declarada (meta):** ${dat.descripcion || '_sin meta description_'}

**Observado directamente (automático)**
- Estructura (h1–h3):
${dat.outline.map(h => `  - ${h.n} ${h.t}`).join('\n') || '  - _ninguna_'}
- Navegación y enlaces (texto → ruta):
${tabla(dat.nav.map(l => [l.t, l.h]), ['Texto', 'Ruta/Origen'])}
- Precios publicados (líneas con "$", recortadas):
${dat.precios.map(p => `  - ${p}`).join('\n') || '  - _ninguno_'}
- Llamadas a la acción en el contenido principal: ${dat.cta.join(' · ') || '_ninguna_'}
- Formularios (solo campos, no se enviaron): ${dat.forms.length ? '\n' + dat.forms.map((fm, i) => `  - Formulario ${i + 1}: ` + fm.campos.map(c => `${c.etiqueta || c.tipo} (${c.tipo}${c.requerido ? ', requerido' : ''}${c.autocomplete ? ', autocomplete=' + c.autocomplete : ''})`).join('; ') + (fm.botones.length ? ` — botones: ${fm.botones.join(', ')}` : '')).join('\n') : '_ninguno_'}
- Diseño medido (estilos calculados): fuente cuerpo \`${dat.diseno.fuenteCuerpo}\`, títulos \`${dat.diseno.fuenteTitulo}\` (${dat.diseno.tamH1}); texto ${dat.diseno.colorTexto} sobre ${dat.diseno.fondo}; botón principal ${dat.diseno.boton ? `${dat.diseno.boton.fondo} / ${dat.diseno.boton.texto} / radio ${dat.diseno.boton.radio}` : 'n/d'}; desborde horizontal: ${dat.diseno.desbordeHorizontal ? 'SÍ' : 'no'} (ancho ${dat.diseno.ancho}px)
- Medios: ${dat.medios.imagenes} imágenes (${dat.medios.picture} \`picture\`, ${dat.medios.sinAlt} sin alt, ${dat.medios.lazy} lazy), ${dat.medios.svg} SVG
- Tecnología detectada: ${Object.entries(dat.tecnologia).map(([k, v]) => `${k}=${Array.isArray(v) ? v.join(',') || '-' : v || '-'}`).join('; ')}
- Peticiones por host: ${Object.entries(porHost).sort((a, b) => b[1] - a[1]).slice(0, 6).map(([h, n]) => `${h} (${n})`).join(', ')}
- Errores/límites: HTTP≥400: ${errores.http.join(' | ') || 'ninguno'}; consola: ${errores.consola.join(' | ') || 'ninguno'}; excepciones: ${errores.excepciones.join(' | ') || 'ninguna'}; peticiones no-GET bloqueadas por ser solo lectura: ${errores.bloqueadasPorSerSoloLectura}
- Captura: ${captura ? captura : 'no tomada (solo con --captura cuando documenta un elemento visual)'}

**Síntesis fiel:** _(pendiente: el agente la redacta en 3–6 líneas tras leer lo anterior, sin copiar texto del sitio)_
**Inferencias [I]:** _(pendiente: separar aquí lo que NO se comprobó)_
`;
  const cabecera = `# ${sitio} · ${new URL(url).pathname || '/'}\nRegistro acumulativo. No se sobrescribe: cada consulta añade una sección. Solo resúmenes y datos medidos; sin copiar páginas, imágenes ni código.\n`;
  if (previo && previo.huella === huella && !opt.forzar) {
    // Sin cambios: no se duplica el hallazgo; solo se anota la fecha de verificación
    appendFileSync(join(RAIZ, archivo), `\n> Verificado de nuevo el ${hoy}: sin cambios (huella \`${huella}\`).\n`);
  } else if (!existsSync(join(RAIZ, archivo))) {
    writeFileSync(join(RAIZ, archivo), cabecera + bloque);
  } else {
    appendFileSync(join(RAIZ, archivo), bloque);
  }
  idx[clave] = { sitio, titulo: dat.titulo, url, archivo, estado, huella, primeraConsulta: previo?.primeraConsulta || hoy, ultimaConsulta: hoy, consultas: (previo?.consultas || 0) + 1, capturas: [...(previo?.capturas || []), ...(captura ? [captura] : [])], errores: errores.http.length + errores.excepciones.length };
  writeFileSync(idxPath, JSON.stringify(idx, null, 1));
  // Vista legible del índice (derivada; se regenera, no contiene hallazgos)
  const filas = Object.values(idx).sort((a, b) => a.sitio.localeCompare(b.sitio) || a.url.localeCompare(b.url));
  writeFileSync(join(CLIPS, 'INDICE.md'), `# Índice de páginas guardadas (generado por clipper.mjs)\n\n| Sitio | Página | Estado | Consultas | Última | Archivo |\n|---|---|---|---|---|---|\n` + filas.map(x => `| ${x.sitio} | ${x.titulo.slice(0, 50)} | ${x.estado} | ${x.consultas} | ${x.ultimaConsulta.slice(0, 10)} | ${x.archivo} |`).join('\n') + '\n');
  console.log(JSON.stringify({ ok: true, archivo, estado, huella, cambio: previo ? previo.huella !== huella : 'nuevo', captura, errores }, null, 1));
  salir(0);
} catch (e) {
  // Registrar el fallo sin inventar contenido
  mkdirSync(join(CLIPS, sitio), { recursive: true });
  appendFileSync(join(CLIPS, sitio, 'errores.log'), `${hoy} ${url} → ${String(e.message).slice(0, 200)}\n`);
  console.error('FALLO:', e.message); salir(1);
}
