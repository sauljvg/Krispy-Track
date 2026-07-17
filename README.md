# Krispy Kreme ParqueSur — Reseñas Analytics

Plataforma para extraer, analizar y visualizar las reseñas de Google Maps de
Krispy Kreme ParqueSur.

## Estructura

```
proyecto-krispy-analytics/
├── scraper/
│   ├── scraper_v2.py      # Extractor (Selenium)
│   ├── stores.py          # Registro de tiendas (nombre + URL de Google Maps)
│   └── config.py          # Parámetros de scroll
├── common.py               # Parseo de fechas relativas + sentimiento (compartido)
├── backend/
│   ├── main.py             # App FastAPI
│   ├── routes.py           # Endpoints /api/*
│   ├── db.py                # Conexión SQLite
│   ├── analytics.py         # Stats, timeline, keywords
│   └── utils.py              # Paginación, CSV
├── frontend/
│   ├── index.html
│   ├── css/styles.css
│   └── js/{filters,analytics,dashboard}.js
├── krispy_kreme.db          # Se genera al correr el scraper
└── krispy_kreme_todas_resenas.{json,csv}
```

## 1. Extraer las reseñas

```bash
cd scraper
python scraper_v2.py              # tienda por defecto (parquesur)
python scraper_v2.py <clave>       # otra tienda, ver stores.py
```

Abre una ventana real de Chrome (no headless) y hace scroll sobre el panel de
reseñas de Google Maps hasta cargarlas todas. Google las sirve en lotes con
latencia variable, así que el proceso puede tardar bastante y a veces se
queda "parado" varios minutos entre lotes — es normal, el script espera con
backoff adaptativo antes de darse por vencido. En la práctica, sesiones
automatizadas parecen tener un tope real de cuántas reseñas sirve Google (no
siempre se llega al 100% del total anunciado).

Guarda checkpoints cada ~100 reseñas nuevas en `krispy_kreme.db`, `.json` y
`.csv`, así que si el proceso se corta (conexión, cierre de la ventana) no se
pierde el progreso — solo hay que volver a lanzarlo (vuelve a extraer desde
cero, pero lo ya guardado en `krispy_kreme.db` queda como estaba hasta ese
punto).

### Añadir una tienda nueva

Añadir una entrada en `scraper/stores.py` con la clave, el nombre a mostrar y
la URL de Google Maps de esa tienda. Todas las reseñas quedan en la misma
`krispy_kreme.db`, distinguidas por la columna `tienda` — el dashboard y la
API ya filtran/agrupan por tienda automáticamente.

### Actualizar una tienda ya scrapeada (rápido)

```bash
python scraper_v2.py <clave> --update
```

En vez de recorrer todo el histórico otra vez, ordena por "Más recientes" y
para el scroll en cuanto encuentra 15 reseñas seguidas que ya están en la BD
(todo lo que viene después, en orden cronológico, ya lo tenemos). Para una
tienda con pocas reseñas nuevas desde la última vez, esto tarda segundos en
vez de los 15-60+ minutos de un scrape completo.

## 2. Levantar la API

```bash
cd backend
pip install fastapi uvicorn openpyxl
python main.py
```

Sirve en `http://127.0.0.1:8000`. La mayoría de endpoints aceptan los mismos
filtros `tienda`, `rating`, `sentiment`, `date_from`, `date_to`, `q` — así que
las estadísticas, gráficos y exportaciones siempre reflejan lo que esté
filtrado en el dashboard, no el total global:

- `GET /api/stores` — tiendas presentes en la BD con su nº de reseñas
- `GET /api/stats` — total, promedio, distribución por estrellas, % positivas
- `GET /api/timeline` — reseñas y promedio por mes
- `GET /api/keywords` — palabras más mencionadas
- `GET /api/staff-mentions` — ranking de personal mencionado (actuales/anteriores)
- `GET /api/reviews` — listado paginado, con filtros `tienda`, `rating`,
  `sentiment`, `date_from`, `date_to`, `q` (búsqueda en texto/autor), `staff`, `sort`
- `GET /api/reviews/export` — CSV con los mismos filtros
- `GET /api/reviews/export/xlsx` — Excel (.xlsx) con los mismos filtros

## 3. Abrir el dashboard

El frontend hace `fetch` a `http://127.0.0.1:8000`, así que necesita
servirse por HTTP (no `file://`, los navegadores bloquean el `fetch` desde
disco):

```bash
cd frontend
python -m http.server 8080
```

Y abrir `http://127.0.0.1:8080`.

## Notas sobre el análisis de sentimiento

La etiqueta positivo/neutral/negativo se basa principalmente en la
calificación en estrellas del propio usuario (4-5★ = positivo, 3★ = neutral,
1-2★ = negativo), reforzada con un score de texto (léxico simple en
español) usado solo para búsqueda/orden fino. Es más fiable que un análisis
de texto puro, porque la estrella es la señal que el propio usuario dio.
