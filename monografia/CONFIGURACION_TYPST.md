# Configuración Typst — Monografía y Diapositivas

Referencia de configuración de los dos sistemas Typst del curso *IA Causal en
Producción* (ECO-490 / ECON-540, edición 2026):

| Artefacto | Archivo de configuración | Salida |
|---|---|---|
| Monografía (32 capítulos + apéndices) | `02_monografia/monografia-ml-causal-typst/template/template.typ` | `monografia.pdf` (~377 pp., A4) |
| Diapositivas (32 mazos) | `07_diapositivas/plantilla_monografia.typ` | `07_diapositivas/build/capNN_*.pdf` (16:9) |

Ambos sistemas comparten **paleta y lenguaje visual** (mismo accent teal, navy
profundo, grises pizarra) para que libro y diapositivas se lean como un único
sistema. Requieren Typst ≥ 0.15; las diapositivas además usan
`touying 0.5.5`, `cetz 0.3.4` y `fletcher 0.5.3` (cache en
`~/.cache/typst/packages`).

---

## 1. Monografía — `template/template.typ`

Plantilla consolidada (~660 líneas) organizada en 11 secciones numeradas con
comentarios `// ====`. No es un paquete externo: `main.typ` hace
`#import "template/template.typ": *` y aplica `#show: project`.

### 1.1 Paleta (`§1`)

```typst
#let navy    = rgb("#0D1B2E")   // navy profundo
#let crimson = rgb("#A61E2B")   // crimson sobrio
#let gray    = rgb("#475569")   // slate-600
#let light   = rgb("#F8FAFC")   // slate-50
#let accent  = rgb("#0E7490")   // teal técnico (cyan-700)
#let green   = rgb("#15803D")   // green-700
#let orange  = rgb("#B45309")   // amber-700 sobrio
```

Roles de color: `accent` (teal) para secciones, proposiciones/lemas/corolarios
y líneas de acento; `navy` para capítulos, teoremas y títulos; `green` para
definiciones y decisiones de referencia; `orange` para supuestos/ejemplos/notas
técnicas; `crimson` para riesgos y alertas; `gray` para observaciones.

### 1.2 Tipografía (`§2`)

```typst
#let serif-font = "New Computer Modern"   // cuerpo
#let sans-font  = "Inter"                  // display: títulos, kickers, headers
#let mono-font  = "DejaVu Sans Mono"       // código
```

Configuración global del cuerpo (`project`): serif **11 pt**, `lang: "es"`,
justificado, `leading: 0.72em`, sangría de primera línea `1.2em`
(solo párrafos, no listas), `spacing: 1em`. Si `Inter` no está instalada,
basta reemplazar el string de `sans-font` (se evitó la cadena de fallback por
el ruido de warnings que genera).

### 1.3 Página y header (`project`)

```typst
set page(
  paper: "a4",
  margin: (left: 2.6cm, right: 2.6cm, top: 3.5cm, bottom: 3.5cm),
  header: ... ,            // título del capítulo/parte al margen exterior,
  numbering: "1",          // folio al margen interior; regla sutil debajo
)
```

- El header lee `state("chapter-title")` / `state("part-title")` y alterna
  lado par/impar (título exterior, folio interior) con una línea de
  `0.3pt + gray.lighten(65%)`.
- `frontmatter-mode` decide numeración romana (`i`) vs. arábiga (`1`).

### 1.4 Apertura de capítulo (heading nivel 1)

Composición "cereza" para capítulos numerados y apéndices (nunca en
frontmatter):

1. **Numeral fantasma**: 96 pt, `navy.transparentize(89%)`, anclado arriba a la
   derecha con `place(top + right, dx: -0.5em, dy: -0.6em)` (no empuja el
   flujo).
2. **Kicker** `CAPÍTULO X` / `APÉNDICE X`: accent, 10.5 pt, `tracking: 0.24em`.
3. **Filete superior fino**: `0.5pt + navy` al 100 % del ancho.
4. **Título**: sans 26 pt navy, `tracking: -0.015em`, `hyphenate: false`.
5. **Línea corta de accent**: 32 % del ancho, `2.25pt + accent`.

La lógica de contadores se mantiene intacta en la rama numbered:
`counter("chapter").step()`, resets de sección/subsección, figuras, tablas,
listados, ecuaciones y teoremas, y los `state()` de `chapter-title` /
`part-title` / `chapter-kind`.

Frontmatter (prefacio, notación…): solo título navy 24 pt + línea corta de
accent al 45 %.

Niveles 2–5: sección = sans 16 pt navy con numeración `1.1` (apéndice `A.1`);
subsección = sans 13 pt accent `1.1.1`; nivel 4 = sans 11 pt gris itálica;
nivel 5 = sans 10 pt gris bold.

### 1.5 Numeración de objetos

| Objeto | Contador | Formato |
|---|---|---|
| Ecuaciones | `equation-counter` (reset por capítulo) | `(1.1)` |
| Figuras (`kind: image`) | reset por capítulo | `Figura 1.1` |
| Tablas (`kind: table`) | reset por capítulo | `Tabla 1.1` |
| Listados (`kind: raw`) | reset por capítulo | `Listado 1.1` |
| Algoritmos (`kind: "algorithm"`) | global (no se resetea) | `Algoritmo 1.` |
| Teoremas/defs/etc. | `theorem-number` (reset por capítulo) | `Teorema 1.1` |

`set math.equation(numbering: ...)` antepone el capítulo; los suplementos de
figura se configuran con `show figure.where(kind: ...)`.

### 1.6 Estructura del documento

- `frontmatter(body)` — numeración romana, `chapter-kind = "frontmatter"`,
  headings sin numeración.
- `mainmatter(body)` — numeración arábiga, `chapter-kind = "chapter"`,
  resetea todos los contadores, `set heading(numbering: "1.1.1")`.
- `appendix-mode(body)` — `chapter-kind = "appendix"`, reinicia contador de
  headings para que el índice general use letras (`A.1.1`).
- `part(title)` — apertura de parte: kicker `PARTE I` accent con tracking
  `0.3em`, título 36 pt navy, línea de accent al 14 %.
- Helpers `chapter(title)`, `section(title)`, `subsection(title)`.

### 1.7 Bloques de teoremas

`_theorem-block(kind-name, kind-color, body, name: none)` usa una
`figure(kind: "theorem-block")` con contador compartido `theorem-number` y
`numbering: "1.1"` (capítulo.teorema). Internamente fuerza
`set align(left)` para que la figura no centre la cabecera. Composición:

- **Badge** del tipo (p. ej. "Definición 1.1"): `#box(fill: kind-color, ...)`
  con texto blanco sans 10.5 pt bold.
- **Nombre** `(name)`: sans 11.5 pt itálica bold, `navy.darken(20%)`.
- **Cuerpo** en `block(breakable: true)` (puede partirse entre páginas).

Macros públicas (firma `(body, name: none, ..rest)` que acepta también el
nombre como segundo argumento posicional):

| Macro | Color |
|---|---|
| `theorem` / `teorema` | navy |
| `proposition`, `lemma`, `corollary` | accent |
| `definition` / `definicion` | green |
| `assumption`, `example` | orange |
| `remark` | gray |

`proof(body, kind: "full" | "sketch")` agrega el cuadrado final
(`$sym.square.small$`).

> ⚠️ No referenciar teoremas con `@thm-...`: el template suprime el caption de
> esas figuras (`#show figure.where(kind: "theorem-block"): it => it.body`), así
> que Typst no puede resolver el número. Usar prosa o `@sec-...`.

### 1.8 Cajas `_tbox` y derivadas

`_tbox(title, frame-color, body, fill-color: light)` — borde izquierdo
`2.5pt + frame-color` como ancla cromática, resto de bordes
`0.3pt + frame-color.lighten(78%)`, `inset: (left: 12pt, right: 10pt, top:
8pt, bottom: 8pt)`, `radius: 3pt`, título sans 10.5 pt bold con
`tracking: 0.06em` y filete separador sutil (`0.3pt + frame-color.lighten(55%)`).

| Función | Título | Color |
|---|---|---|
| `cuadrosinoptico`, `cuadrodecision`, `opciones` | … | accent |
| `disenio` | El problema de diseño | navy |
| `decisionref`, `diagnosticos`, `intuicion` | … | green |
| `supuestos` | Supuestos del capítulo | gray |
| `riesgos` | Riesgos, límites y mitigación | crimson |
| `notatecnica`, `advertencia` | Nota técnica / Atención | orange |
| `monorepo` | Implementación en el monorepo… | accent |

Ninguna cambió de firma en las pasadas estéticas; los cambios fueron visuales.

### 1.9 Algoritmos, código y utilidades

- `algorithm(title, body)` — `figure(kind: "algorithm")`, estilo
  *algorithm2e ruled*: cabecera "Algoritmo" sans 11 pt bold, filetes superior
  e inferior negros, cuerpo 10 pt, `set align(left)` interno.
- `kwin`/`kwout`, `for-loop`, `if-then`, `return-stmt` — bloques de
  pseudocódigo con palabras clave en bold.
- `raw.where(block: true)` — fondo `#F4F7F9`, borde `0.3pt + gray.lighten(70%)`,
  mono 9 pt, `inset: (x: 9pt, y: 8pt)`, `radius: 3pt`, alineado a la izquierda.
- `checklist(body)` — lista con casillas `☐` navy.
- `code(body)` — texto mono 9.5 pt en accent.
- `portada()` — página independiente (`numbering: none`, márgenes 3.2/2.8 cm):
  kicker `MONOGRAFÍA DEL CURSO` accent con tracking, título sans 44 pt navy,
  línea de accent al 12 %, dos cajas con lenguaje de borde izquierdo
  (curso = accent, promesa = crimson), pie con stack del monorepo.

### 1.10 Compilar

```bash
cd 02_monografia/monografia-ml-causal-typst
typst compile main.typ monografia.pdf
```

Sin warnings en el entorno actual (fuentes instaladas: New Computer Modern,
Inter, DejaVu Sans Mono). ~377 páginas.

---

## 2. Diapositivas — `plantilla_monografia.typ`

Plantilla Touying (~840 líneas) que re-exporta el tema metropolis y define
~24 funciones `cap-*`, una por tipo de slide. Cada mazo (`capitulos/capNN_*.typ`)
es un `.typ` que importa la plantilla e invoca un subconjunto de funciones
(1 slide por llamada, en orden).

### 2.1 Motor y tema

```typst
#import "@preview/touying:0.5.5": *
#import "@preview/cetz:0.3.4": canvas, draw
#import "@preview/fletcher:0.5.3" as fletcher
```

`cap-theme(body)` configura `metropolis-theme.with(...)`:

- `aspect-ratio: "16-9"`, `align: top`, `footer-progress: true`.
- `config-colors(primary: navy, secondary: accent, neutral-lightest: #FAFAF8,
  neutral-darkest/foreground: texto, ...)` — la **banda de header** de cada
  slide usa `secondary` (teal) y la barra de progreso `primary` (navy).
- `config-page(margin: (left: 1.35cm, right: 1.35cm, top: 2.0cm, bottom:
  1.35cm), footer: "IA Causal en Producción · Cap. N ★/◇ · ECO-490/ECON-540 ·
  Ed. 2026")`.
- Texto base serif 12.5 pt (`("New Computer Modern", "Libertinus Serif",
  "Georgia")`), `par(leading: 0.42em, spacing: 0.5em)`, mono DejaVu Sans Mono.

### 2.2 Paleta y tipografía

Idéntica a la monografía (misma paleta refinada del §1.1) + colores
solo-diapositivas:

```typst
#let borde     = rgb("#CBD5E1")   // slate-300 (bordes de cajas/chips)
#let texto     = rgb("#0F172A")   // slate-900 (texto principal)
#let muted     = rgb("#64748B")   // slate-500 (secundario)
#let error     = rgb("#B4232E")   // rojo sobrio (errores críticos)
#let interact    = rgb("#7B3F8D")  // violeta (pausas interactivas)
#let interact-bg = rgb("#F3E8F9")
#let sans-font = "Inter"          // display (portada)
```

Escala tipográfica `sz-*`: body 12.5, title 18, h 12, small 10, tiny 9,
code 7.8, table 10 pt.

### 2.3 Estado del capítulo

`cap-state` guarda `num/titulo/parte/sesion/variant/critico`; `cap-init(...)`
lo actualiza al inicio de cada mazo (lo consume el footer y la portada).

### 2.4 Catálogo de funciones `cap-*` (1 slide cada una)

| Función | Slide |
|---|---|
| `cap-progreso-curso(cap-actual:)` | Grid 3×3 de las 9 partes, chips por capítulo (tarjetas con `height: 7.6em`, borde `0.5pt + borde`) |
| `cap-portada(...)` | Portada: numeral fantasma 104 pt translúcido arriba a la derecha, kicker `CAPÍTULO N`, filete, título, línea accent 30 % |
| `cap-roadmap(objetivos:, agenda:, lectura:, lab:, entrega:)` | Objetivos + agenda + bloque "Antes de clase" |
| `cap-motivacion(problema:, gancho:, caso:)` | Variante A: problema, gancho, caso del curso |
| `cap-problema-diseno(decision:, alternativas:, tradeoff:, stack:, riesgo:)` | Variante B: tabla de diseño |
| `cap-opciones-tradeoffs(opciones:)` | Variante B: opciones y trade-offs |
| `cap-decision-referencia(decision:, justificacion:)` | Variante B: decisión adoptada (box verde) |
| `cap-glosario(terminos:)` | Definiciones clave |
| `cap-definicion(titulo-def:, cuerpo:, eq:)` | Marco teórico I |
| `cap-supuestos(supuestos:)` | Marco teórico II (tabla) |
| `cap-teorema(titulo:, enunciado:, ref-apendice:)` | Caja de teorema (usa `caja-teorema`) |
| `cap-demostracion(pasos:)` | Pasos de demostración |
| `cap-interactivo(tipo:, pregunta:, duracion:)` | Pausa activa (box violeta) |
| `cap-codigo-parte(titulo:, snippet:, salida:, nota:, invariante:)` / `cap-codigo` | Código oscuro + salida + chequeo de sanidad |
| `cap-caso-resolucion(titulo:, contexto:, resultado:, interpretacion:)` / `cap-caso` | Caso aplicado |
| `cap-validacion(tipo:, descripcion:, conclusion:)` | Validación/robustez (sin uso actual) |
| `cap-mapeo-pch-activo(nivel:, metrica:, pregunta-activa:)` / `cap-mapeo-pch` | Jerarquía Causal de Pearl + pregunta activa |
| `cap-errores-transiciones(errores:, conexiones:)` / `cap-errores` | Errores comunes |
| `cap-checklist-alertas(items:)` | Checklist ☐ (variante B) |
| `cap-monorepo(texto-monorepo:)` | Callout del monorepo (Caps. 4, 9, 15, 19, 20, 30) |
| `cap-discusion-ejercicio(pregunta:, ejercicio:)` / `cap-discusion` | Discusión y ejercicio |
| `cap-cierre-narrativo(resumen:, refs:, transicion:, gancho:)` / `cap-cierre` | Cierre: resumen + refs + gancho |
| `cap-diagrama(titulo:, cuerpo-diagrama:)` | Envoltorio cetz/fletcher (sin uso actual) |

Cajas de contenido (`caja-generica` + 8 derivadas: teorema, proposición, lema,
corolario, definición, supuesto, ejemplo, observación, axioma) — mismos colores
que el libro: inset `1.0/0.8em`, título 15 pt, cuerpo 13 pt, borde izquierdo
`3.5pt + color`, ref-apéndice 10 pt.

### 2.5 Convenciones de contenido

- **Variantes por capítulo**: A (teoría: motivación→definición→supuestos→
  teorema→demostración) y B (ingeniería: problema de diseño→opciones→decisión
  de referencia→checklist). La portada muestra `Plantilla A/B`.
- **Capítulos ◇** (5, 16, 17, 18, 27, 28) usan esqueleto reducido, sin
  `cap-progreso-curso`.
- **Trampa de sintaxis**: los parámetros que son arreglos de bloques
  (`terminos:`, `supuestos:`, `pasos:`, `errores:`, `items:`, `opciones:`,
  `resumen:`, `refs:`, `agenda:`) re-parsean como markup: usar modo matemático
  (`$...$`) para subíndices/desigualdades, o escapar `\_`, `\<`, `\>`.
- **Mínimos de legibilidad** (acordados en auditoría): chip/tabla ≥ 9 pt,
  cuerpo de caja ≥ 12 pt, título de caja ≥ 14 pt.

### 2.6 Compilar

```bash
cd 07_diapositivas
./build.sh                     # los 32 mazos -> build/*.pdf (32/32 OK esperado)
./build.sh cap11               # solo los que matcheen "cap11"
./build.sh --watch cap11_dml   # recompilación al guardar
```

Siempre con `--root .` desde `07_diapositivas/` (los `#import
"../plantilla_monografia.typ"` fallan si se compila desde otra carpeta). Las
salidas y logs van a `build/` (gitignored). Herramienta de medición de
aprovechamiento de cada slide: `build/medir_aprovechamiento.py` (usa PIL +
numpy; en este tema usar `footer_px≈40` porque el footer de metropolis vive a
~25–37 px del borde inferior).

---

## 3. Tabla de correspondencia visual

| Elemento | Monografía | Diapositivas |
|---|---|---|
| Paleta | `template.typ` §1 | `plantilla_monografia.typ` §paleta (idéntica) |
| Sans display | `sans-font = "Inter"` | `sans-font = "Inter"` (portada) |
| Apertura de capítulo | numeral 96 pt top-right + kicker + filete + título + línea accent 32 % | `cap-portada` numeral 104 pt top-right + kicker + filete + título + línea accent 30 % |
| Cajas | `_tbox`: borde izq. 2.5 pt, radius 3 pt, título con tracking | `caja-generica`: borde izq. 3.5 pt, radius 3 pt, título 15 pt |
| Contadores | capítulo/sesión/teorema por capítulo | `cap-state` por mazo |
| Código | fondo `#F4F7F9` claro | fondo oscuro `#1e1e1e` (proyección) |
