@echo off
REM Script para ejecutar el NUEVO scraper mejorado
REM Solo haz doble clic en este archivo

color 0a
title Krispy Kreme - Extractor Mejorado (TODAS LAS RESENAS)

echo.
echo ============================================================
echo  EXTRACTOR MEJORADO - KRISPY KREME PARQUESUR
echo  Extrayendo TODAS las 2886 resenas (15-30 minutos)
echo ============================================================
echo.
echo Instalando dependencias...
pip install selenium --break-system-packages -q

echo.
echo Iniciando scraper mejorado...
echo.

python scraper_krispy_mejorado.py

echo.
echo ============================================================
echo Proceso completado!
echo Archivos generados:
echo   - krispy_kreme_todas_resenas.json (TODAS las resenas)
echo   - krispy_kreme_reviews_abril.json (FILTRADAS)
echo.
echo Abre app_visualizador.html en tu navegador
echo ============================================================
echo.
pause
