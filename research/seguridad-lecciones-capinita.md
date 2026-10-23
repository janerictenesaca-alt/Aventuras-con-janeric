# Lecciones de seguridad a partir de Capinita (revisión pasiva, 2026-10-23)

**Alcance y ética.** Solo se revisó lo que el sitio entrega públicamente a cualquier visitante (cabeceras, HTML, JS, `robots.txt`). **No** se probó ninguna vulnerabilidad: no se envió ningún formulario, no se llamó a APIs, no se intentó acceder a `/perfil` ni `/administrador`, no se probó fuerza bruta, inyección ni control de acceso. Por eso **esto no es una auditoría**: del servidor, la base de datos, la autenticación real y los permisos no sabemos nada. Los hallazgos son mejoras generales y de bajo riesgo; el propósito es **qué hacer bien en nuestro proyecto**, no explotar el sitio. Si se quisiera avisar al dueño, se haría de forma responsable y privada (contacto público del sitio), sin detalles de ataque.
**[M]** medido en cabeceras/código público · **[I]** inferido.

## Qué hace bien (copiar la idea)
- **HTTPS siempre** con HSTS (`max-age` de 2 años) [M].
- **Sin source maps públicos** (0 de 15 bundles) [M] y **sin claves ni secretos** en el JS público (se buscaron patrones de claves de API, tokens, URLs de bases de datos y claves privadas: ninguno) [M].
- **Sin scripts de terceros** en el HTML aparte de Google Analytics [M]: poca superficie de ataque por cadena de suministro.
- **Rutas privadas separadas** (`/perfil`, `/administrador`) y excluidas de buscadores [M].
- **Consulta de datos viales hecha en el servidor** (no desde el navegador), así no se expone la integración [M].

## Debilidades observadas y cómo evitarlas en nuestro proyecto
| # | Hallazgo en Capinita | Riesgo | Qué haremos nosotros |
|---|---|---|---|
| 1 | **Sin Content-Security-Policy** [M] | Si entrara un XSS, nada limita qué scripts se ejecutan | Definir CSP estricta (nonce/hash, sin `unsafe-inline` donde sea posible) y probarla en modo "report-only" primero |
| 2 | **Sin `X-Frame-Options` ni `frame-ancestors`** [M] | Otra web podría incrustar el login/registro (clickjacking) | `frame-ancestors 'none'` y `X-Frame-Options: DENY` |
| 3 | Sin `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy` ni COOP [M] | Endurecimiento básico ausente | Añadirlas todas por defecto (middleware o `next.config` `headers()`) |
| 4 | HSTS sin `includeSubDomains`/`preload` [M] | Subdominios (`app.`, `img.`) quedan fuera de la protección | HSTS con `includeSubDomains; preload` tras verificar todos los subdominios |
| 5 | `Access-Control-Allow-Origin: *` en las páginas [M] | Bajo en HTML público, pero mala costumbre si llega a las APIs | CORS con lista de orígenes permitidos; nunca `*` con credenciales |
| 6 | **161 de 163 enlaces `target="_blank"` sin `rel`** (solo 18 con `noopener`) [M] | Los navegadores modernos ya aplican `noopener`, pero se filtra el `Referer` y se depende del navegador | `rel="noopener noreferrer"` en todos los enlaces externos (regla de lint) |
| 7 | **Campos de contraseña con `autocomplete="current-password"` también en el registro** [M] | Los gestores de contraseñas confunden "nueva" y "actual" y empujan a reutilizar claves | `autocomplete="new-password"` en registro y repetir; `current-password` solo en login |
| 8 | Se pide **fecha de nacimiento** sin explicar para qué [O] | Exceso de datos personales (minimización) | Pedir solo lo necesario; justificar cada dato en pantalla |
| 9 | **Sin señal visible de anti-bot** (ni CAPTCHA ni límite de intentos en el HTML) en login/registro [I] | Abuso: registros masivos, fuerza bruta de claves | Limitar intentos por IP y por cuenta, verificación de correo, CAPTCHA/Turnstile solo cuando haya abuso, bloqueo progresivo |
| 10 | **`robots.txt` revela `/administrador`** [M] | Anuncia dónde está el panel (la oscuridad no es seguridad) | No listar rutas sensibles; protegerlas con autenticación fuerte + MFA y, si se quiere, no enlazarlas |
| 11 | `robots.txt` apunta a otro dominio (`acme.com`) y el sitemap duplica URLs [M] | Plantilla sin revisar: señala descuido de configuración | Revisar `robots.txt`/sitemap en la lista de verificación de despliegue |
| 12 | **Google Analytics sin aviso de cookies visible** y política de privacidad sin derechos de acceso/eliminación ni contacto [O] | Incumplimiento de protección de datos (Ecuador: LOPDP) | Banner de consentimiento, política completa (derechos ARCO, plazos, contacto del responsable) |
| 13 | **Datos de contacto personales del equipo y teléfonos de cooperativas en claro** [O] | Spam, suplantación (smishing/phishing), scraping | Usar canales de la empresa, formularios con protección anti-spam, y ofuscar o limitar datos personales |
| 14 | Datos viales y de horarios mostrados **sin fecha de verificación** [O] | Desinformación (riesgo para el usuario) | Mostrar siempre la fecha del dato y su fuente |
| 15 | **Subdominios activos** (`app.`, `img.`) [M] | Más superficie que vigilar (un subdominio olvidado puede ser tomado) | Inventario de subdominios, quitar DNS huérfanos, mismas cabeceras en todos |
| 16 | Imágenes con `must-revalidate` y sin límites de tamaño de subida visibles [M/I] | Rendimiento y, si hay subida de archivos, riesgo de abuso | Validar tipo/tamaño en servidor, re-procesar imágenes, almacenar fuera del dominio principal con cabeceras seguras |

## Lista de verificación para nuestro proyecto
**Antes de publicar**
- Cabeceras: CSP, `frame-ancestors`, `nosniff`, `Referrer-Policy`, `Permissions-Policy`, HSTS con subdominios. Comprobar con un escáner de cabeceras.
- Cookies de sesión: `HttpOnly`, `Secure`, `SameSite=Lax/Strict`, caducidad corta con renovación.
- Autenticación (Auth.js u otra): contraseñas con Argon2/bcrypt, política de longitud (no solo reglas de símbolos), verificación de correo, recuperación segura, límite de intentos, MFA para administradores y negocios.
- Autorización **en el servidor** para cada acción (un negocio solo edita lo suyo): probar a mano y con pruebas automáticas que un usuario no pueda ver o cambiar datos de otro (IDOR).
- Validación de entrada con zod en cliente **y servidor**; consultas parametrizadas o ORM; escapar la salida; sanear cualquier HTML (blog, descripciones).
- Subidas de imágenes: lista blanca de tipos, tamaño máximo, re-codificación, nombres aleatorios.
- CORS cerrado, sin `*` en APIs; CSRF protegido en formularios.
- Secretos solo en variables de entorno del servidor, nunca en el bundle; revisar que no haya claves en el JS publicado; sin source maps públicos.
- Dependencias: `npm audit`/Dependabot, fijar versiones, revisar paquetes nuevos.
- Privacidad: política completa, consentimiento de cookies, minimización de datos, plazos de conservación.
**Después de publicar**
- Registro de accesos y alertas de intentos fallidos; copias de seguridad probadas; plan de respuesta ante incidentes; revisión periódica de cabeceras, dependencias y subdominios.

## Límites
Sin pruebas dinámicas ni acceso autenticado: no se evaluó fuerza bruta, inyección, control de acceso entre usuarios, subida de archivos ni la configuración del servidor. Para una auditoría real haría falta autorización escrita del propietario del sitio. En nuestro propio proyecto sí podremos hacer pruebas de seguridad completas (propias, en un entorno de pruebas).
