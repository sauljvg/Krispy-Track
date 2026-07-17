import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import scrape_jobs
from routes import router

app = FastAPI(title="Krispy Kreme Reseñas API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")


@app.on_event("startup")
def _start_daily_scraper():
    scrape_jobs.start_daily_scheduler()


@app.get("/api/health")
def health():
    return {"status": "ok"}


# Sirve el dashboard (HTML/CSS/JS) desde el mismo proceso y puerto que la API,
# para que un único comando de arranque baste tanto en local como en un
# despliegue (Replit, etc.) — antes hacían falta dos servidores (API +
# estático) en dos puertos distintos. Va DESPUÉS de include_router para que
# las rutas /api/* tengan prioridad sobre el catch-all de archivos estáticos.
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), reload=False)
