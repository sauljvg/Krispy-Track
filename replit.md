# Krispy Track

Analytics dashboard for Google Maps reviews of Krispy Kreme stores in Colombia.

## Stack

- **Backend**: FastAPI + SQLite (`krispy_kreme.db`)
- **Frontend**: Static HTML/CSS/JS served by FastAPI at `/`
- **Scraper**: Selenium + Chrome (runs locally only — Replit cannot run Chrome)

## How to run

The app is configured to start automatically via the **"Start application"** workflow:

```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 5000
```

This serves both the API (`/api/*`) and the frontend dashboard at the same port.

## Project structure

```
backend/        FastAPI app, routes, analytics, DB connection
frontend/       Static HTML + CSS + JS dashboard
scraper/        Selenium scraper (local use only)
common.py       Shared date parsing + sentiment logic
krispy_kreme.db SQLite database with scraped reviews
requirements.txt
```

## Updating data

The scraper runs locally (requires Chrome). To refresh data on Replit, run the scraper locally and commit/upload the updated `krispy_kreme.db`.

A nightly scheduler inside the app also triggers incremental updates at 02:00 via `POST /api/scrape` (update mode), but this only works if you have a working scraper environment.

## User preferences
