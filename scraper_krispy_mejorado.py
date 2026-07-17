#!/usr/bin/env python3
"""
Script MEJORADO para extraer TODAS las reseñas de Krispy Kreme ParqueSur
Extrae todas las 2886 reseñas y luego las filtra
"""

import json
import csv
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

# Configuración
KRISPY_KREME_URL = "https://www.google.com/maps/place/Krispy+Kreme/@40.3394194,-3.7334062,17z/data=!3m1!5s0xd4227502054dd0b:0xff95595e535857dc!4m8!3m7!1s0xd422790a22b4cc9:0x50092f971214eb5e!8m2!3d40.3394194!4d-3.7308313!9m1!1b1!16s%2Fg%2F11x_z73fk9"

CURRENT_DATE = datetime.now()

def parse_date(date_str):
    """Parsea fechas en español e inglés"""
    date_str = date_str.lower().strip()

    # Patrones: "hace X meses/semanas/días"
    hace_match = re.search(r'hace\s+(\d+)\s+(meses|semanas|días|mes|semana|día)', date_str)
    if hace_match:
        cantidad = int(hace_match.group(1))
        unidad = hace_match.group(2)

        if 'mes' in unidad:
            fecha_estimada = CURRENT_DATE - timedelta(days=30*cantidad)
        elif 'semana' in unidad:
            fecha_estimada = CURRENT_DATE - timedelta(weeks=cantidad)
        else:
            fecha_estimada = CURRENT_DATE - timedelta(days=cantidad)

        return fecha_estimada, date_str

    # Patrones españoles: "5 de abril de 2026"
    meses_es = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4, 'mayo': 5, 'junio': 6,
        'julio': 7, 'agosto': 8, 'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
    }

    for mes_nombre, mes_num in meses_es.items():
        if mes_nombre in date_str:
            match = re.search(rf'(\d+)\s+de\s+{mes_nombre}(?:\s+de\s+(\d+))?', date_str)
            if match:
                día = int(match.group(1))
                año = int(match.group(2)) if match.group(2) else CURRENT_DATE.year
                try:
                    return datetime(año, mes_num, día), date_str
                except:
                    pass

    # Patrones ingleses: "April 5, 2026"
    meses_en = {
        'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6,
        'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12
    }

    for mes_nombre, mes_num in meses_en.items():
        if mes_nombre in date_str:
            match = re.search(rf'({mes_nombre})\s+(\d+),?\s+(\d+)?', date_str)
            if match:
                día = int(match.group(2))
                año = int(match.group(3)) if match.group(3) else CURRENT_DATE.year
                try:
                    return datetime(año, mes_num, día), date_str
                except:
                    pass

    return None, date_str

def is_april_or_recent(date_str):
    """Verifica si es de abril o últimos 3-4 meses"""
    fecha, _ = parse_date(date_str)

    if fecha is None:
        return False, "Desconocido"

    # Abril de cualquier año
    if fecha.month == 4:
        return True, f"Abril {fecha.year}"

    # Últimos 3-4 meses
    fecha_limite = CURRENT_DATE - timedelta(days=120)
    if fecha >= fecha_limite:
        months_ago = (CURRENT_DATE.year - fecha.year) * 12 + (CURRENT_DATE.month - fecha.month)
        mes_nombre = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                      'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'][fecha.month-1]
        return True, f"{mes_nombre} {fecha.year}"

    return False, fecha.strftime("%d/%m/%Y")

def scrape_all_reviews():
    """Extrae TODAS las reseñas de Google Maps"""
    print("Iniciando Chrome...")
    print(f"Objetivo: Extraer todas las 2886 reseñas\n")

    driver = None
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-extensions")
        driver = webdriver.Chrome(options=options)

        print(f"Accediendo a Google Maps...")
        driver.get(KRISPY_KREME_URL)
        time.sleep(5)

        print("Buscando panel de reseñas...")

        # Scroll dentro del panel de reseñas
        reviews_data = []
        seen_reviews = set()  # Para evitar duplicados
        no_new_reviews_count = 0
        scroll_count = 0
        max_scrolls_without_new = 50  # Si no hay nuevas reseñas en 50 scrolls, termina

        print("Iniciando extracción (esto puede tomar 15-30 minutos)...\n")

        while no_new_reviews_count < max_scrolls_without_new and scroll_count < 1000:
            # Encontrar el contenedor de reseñas (buscar en múltiples selectores)
            try:
                review_elements = driver.find_elements(By.CSS_SELECTOR,
                    "div[data-review-id], div.section-review, div[jsname='jKTz3c'], div[role='article']")
            except:
                review_elements = []

            # Si no hay reseñas, intentar scroll
            if not review_elements:
                driver.execute_script("window.scrollBy(0, 1000)")
                time.sleep(1)
                scroll_count += 1
                continue

            print(f"Reseñas visibles: {len(review_elements)} | Scrolls: {scroll_count} | Únicos extraídos: {len(reviews_data)}", end='\r')

            # Extraer información de cada reseña
            previous_count = len(reviews_data)

            for element in review_elements:
                try:
                    text = element.text
                    if not text or len(text) < 5:
                        continue

                    # Clave única para evitar duplicados
                    review_hash = hash(text[:50])
                    if review_hash in seen_reviews:
                        continue

                    seen_reviews.add(review_hash)

                    lines = text.split('\n')
                    author = ""
                    date_str = ""
                    rating = ""
                    review_text = ""

                    # Parsear líneas
                    for i, line in enumerate(lines):
                        if any(x in line.lower() for x in ['hace', 'de', 'ago', 'month', 'week', 'day']):
                            date_str = line
                        elif '★' in line or 'estrella' in line.lower():
                            rating = line
                        elif i == 0:
                            author = line
                        else:
                            review_text += line + " "

                    if date_str and author:
                        es_valido, categoria = is_april_or_recent(date_str)
                        reviews_data.append({
                            'autor': author.strip(),
                            'fecha': date_str.strip(),
                            'calificación': rating.strip() or "No especificada",
                            'texto': review_text.strip()[:500],
                            'es_abril_o_reciente': es_valido,
                            'fecha_categoria': categoria
                        })
                except:
                    continue

            # Verificar si se añadieron nuevas reseñas
            if len(reviews_data) > previous_count:
                no_new_reviews_count = 0
            else:
                no_new_reviews_count += 1

            # Scroll dentro del panel
            driver.execute_script("""
                var reviewPanel = document.querySelector('[role="presentation"]') ||
                                 document.querySelector('div[style*="overflow"]');
                if (reviewPanel) {
                    reviewPanel.scrollTop += 1000;
                }
                window.scrollBy(0, 500);
            """)

            time.sleep(0.5)
            scroll_count += 1

        print(f"\n✓ Extracción completada!")
        print(f"Total de reseñas únicas: {len(reviews_data)}")

        return reviews_data

    except Exception as e:
        print(f"Error: {e}")
        return []

    finally:
        if driver:
            driver.quit()
            print("Chrome cerrado")

def save_reviews(all_reviews):
    """Guarda TODAS las reseñas y las filtradas"""
    if not all_reviews:
        print("\n✗ No se extrajeron reseñas")
        return

    # Eliminar duplicados finales
    unique_reviews = []
    seen = set()
    for r in all_reviews:
        key = (r['autor'], r['fecha'], r['texto'][:100])
        if key not in seen:
            unique_reviews.append(r)
            seen.add(key)

    all_reviews = unique_reviews

    # Filtrar abril y últimos 3-4 meses
    filtered_reviews = [r for r in all_reviews if r['es_abril_o_reciente']]
    filtered_reviews = sorted(filtered_reviews, key=lambda x: x['fecha'], reverse=True)

    print(f"\n{'='*60}")
    print(f"ESTADÍSTICAS")
    print(f"{'='*60}")
    print(f"Total de reseñas extraídas: {len(all_reviews)}")
    print(f"Reseñas de abril/últimos 3-4 meses: {len(filtered_reviews)}")
    print(f"Porcentaje: {len(filtered_reviews)*100//len(all_reviews) if all_reviews else 0}%")

    # Guardar TODAS las reseñas
    with open("krispy_kreme_todas_resenas.json", 'w', encoding='utf-8') as f:
        json.dump(all_reviews, f, ensure_ascii=False, indent=2)
    print(f"\n✓ Todas las reseñas guardadas en: krispy_kreme_todas_resenas.json")

    # Guardar reseñas filtradas
    with open("krispy_kreme_reviews_abril.json", 'w', encoding='utf-8') as f:
        json.dump(filtered_reviews, f, ensure_ascii=False, indent=2)
    print(f"✓ Reseñas filtradas guardadas en: krispy_kreme_reviews_abril.json")

    # Guardar CSV filtrado
    if filtered_reviews:
        with open("krispy_kreme_reviews_abril.csv", 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['autor', 'fecha', 'fecha_categoria', 'calificación', 'texto'])
            writer.writeheader()
            writer.writerows(filtered_reviews)
        print(f"✓ CSV guardado en: krispy_kreme_reviews_abril.csv")

    # Vista previa
    print(f"\n{'='*60}")
    print(f"VISTA PREVIA (primeras 5 reseñas de abril/recientes)")
    print(f"{'='*60}\n")

    for i, review in enumerate(filtered_reviews[:5], 1):
        print(f"{i}. {review['autor']}")
        print(f"   Fecha: {review['fecha']} ({review['fecha_categoria']})")
        print(f"   Calificación: {review['calificación']}")
        print(f"   Texto: {review['texto'][:150]}...")
        print()

if __name__ == "__main__":
    print("="*60)
    print("EXTRACTOR MEJORADO - KRISPY KREME PARQUESUR")
    print("="*60)
    print(f"Fecha: {CURRENT_DATE.strftime('%d/%m/%Y %H:%M')}")
    print(f"Objetivo: Extraer TODAS las 2886 reseñas")
    print("="*60)
    print()

    reviews = scrape_all_reviews()
    save_reviews(reviews)

    print("\n✓ ¡Proceso completado!")
    print("Archivos generados:")
    print("  - krispy_kreme_todas_resenas.json (TODAS las reseñas)")
    print("  - krispy_kreme_reviews_abril.json (FILTRADAS)")
    print("  - app_visualizador.html (para visualizar)")
