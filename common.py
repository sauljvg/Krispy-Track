"""Utilidades compartidas entre el scraper y el backend."""
import re
from datetime import datetime, timedelta

MESES_ES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]

_UNIDADES = {
    "minuto": "minutes", "minutos": "minutes",
    "hora": "hours", "horas": "hours",
    "día": "days", "días": "days",
    "semana": "weeks", "semanas": "weeks",
    "mes": "months", "meses": "months",
    "año": "years", "años": "years",
}

_NUMEROS_TEXTO = {"un": 1, "una": 1}


def parse_relative_date(fecha_relativa: str, ahora: datetime):
    """Convierte 'Hace 5 meses' / 'Hace un año' / 'Hace 17 horas' en una
    fecha aproximada. Las reseñas de hace pocas horas/minutos son de HOY —
    si no se reconocen, fecha_datetime queda NULL y esa reseña desaparece
    de cualquier desglose por mes (aunque sí cuenta en el total)."""
    texto = fecha_relativa.lower().strip()
    if "momento" in texto or "ahora mismo" in texto:
        return ahora
    match = re.search(
        r"hace\s+(un|una|\d+)\s+(minuto|minutos|hora|horas|día|días|semana|semanas|mes|meses|año|años)",
        texto,
    )
    if not match:
        return None

    cantidad_str, unidad = match.groups()
    cantidad = _NUMEROS_TEXTO.get(cantidad_str, None)
    if cantidad is None:
        cantidad = int(cantidad_str)

    unidad_en = _UNIDADES[unidad]
    if unidad_en == "minutes":
        return ahora - timedelta(minutes=cantidad)
    if unidad_en == "hours":
        return ahora - timedelta(hours=cantidad)
    if unidad_en == "days":
        return ahora - timedelta(days=cantidad)
    if unidad_en == "weeks":
        return ahora - timedelta(weeks=cantidad)
    if unidad_en == "months":
        return ahora - timedelta(days=30 * cantidad)
    return ahora - timedelta(days=365 * cantidad)


def fecha_categoria(fecha: datetime | None) -> str:
    if fecha is None:
        return "Desconocido"
    return f"{MESES_ES[fecha.month - 1]} {fecha.year}"


# Léxico simple de sentimiento en español, usado solo como refuerzo secundario.
_PALABRAS_POSITIVAS = {
    "excelente", "genial", "increíble", "recomendado", "recomendable", "buenísimo",
    "delicioso", "rico", "amable", "rápido", "limpio", "perfecto", "encantador",
    "fantástico", "estupendo", "maravilloso", "agradable", "bueno", "buena",
    "encanta", "gustó", "mejor", "cómodo", "atento", "atenta", "sonrisa",
}
_PALABRAS_NEGATIVAS = {
    "malo", "mala", "pésimo", "horrible", "asqueroso", "caro", "carísimo",
    "lento", "sucio", "grosero", "desagradable", "decepcionante", "frío",
    "tarde", "nunca", "peor", "queja", "reclamo", "estafa", "maleducado",
    "esperando", "espera", "mal",
}


def calcular_sentimiento(texto: str, calificacion: int | None):
    """Etiqueta positivo/neutral/negativo.

    La calificación en estrellas es la señal principal (es la que el propio
    usuario dio); el texto solo aporta un score numérico de refuerzo para
    búsquedas y ordenación, no cambia la etiqueta.
    """
    palabras = set(re.findall(r"[a-záéíóúñ]+", (texto or "").lower()))
    positivas = len(palabras & _PALABRAS_POSITIVAS)
    negativas = len(palabras & _PALABRAS_NEGATIVAS)
    texto_score = 0.0
    if positivas or negativas:
        texto_score = (positivas - negativas) / (positivas + negativas)

    if calificacion is not None:
        rating_score = (calificacion - 3) / 2  # -1 .. 1
        if calificacion >= 4:
            etiqueta = "positivo"
        elif calificacion == 3:
            etiqueta = "neutral"
        else:
            etiqueta = "negativo"
        score = round(0.8 * rating_score + 0.2 * texto_score, 3)
    else:
        score = round(texto_score, 3)
        etiqueta = "positivo" if score > 0.15 else "negativo" if score < -0.15 else "neutral"

    return etiqueta, score
