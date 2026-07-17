"""Registro de tiendas a scrapear.

Añadir una tienda nueva es solo añadir una entrada aquí, con la clave que se
pasará como argumento al scraper (`python scraper_v2.py <clave>`).
"""

STORES = {
    "parquesur": {
        "nombre": "ParqueSur",
        "url": (
            "https://www.google.com/maps/place/Krispy+Kreme/@40.3394194,-3.7334062,17z/"
            "data=!3m1!5s0xd4227502054dd0b:0xff95595e535857dc!4m8!3m7!"
            "1s0xd422790a22b4cc9:0x50092f971214eb5e!8m2!3d40.3394194!4d-3.7308313!9m1!1b1!16s%2Fg%2F11x_z73fk9"
        ),
    },
    "caleido": {
        "nombre": "Caleido",
        # OJO: la URL anterior apuntaba al centro comercial "Caleido" en sí
        # (place id 0xd4229c52...), no a la tienda Krispy Kreme de dentro —
        # por eso acumulábamos reseñas del mall (4,5★, 1335 opiniones sobre
        # aparcamiento/tiendas) en vez de la panadería (4,9★, 509 opiniones).
        # Verificado en Google Maps el 17/07/2026: este es el place id correcto.
        "url": (
            "https://www.google.com/maps/place/Krispy+Kreme/@40.4767646,-3.688831,17z/"
            "data=!3m1!4b1!4m6!3m5!1s0xd4229b532fda521:0x789d19e4d74997fc!8m2!3d40.4767646!4d-3.688831!16s%2Fg%2F11z4stgk57"
        ),
    },
    "princesa": {
        "nombre": "Princesa",
        # El enlace directo con !9m1!1b1 se atascaba en 8 reseñas dentro de
        # Selenium (aunque abría bien la pestaña); el enlace corto sí funciona.
        "url": "https://maps.app.goo.gl/ayuCiW3DJkvszBNK9",
    },
    "lagavia": {
        "nombre": "La Gavia",
        "url": "https://maps.app.goo.gl/mtM1Ev7XNfpdpZHM7",
    },
    "granplaza2": {
        "nombre": "Gran Plaza 2",
        "url": "https://maps.app.goo.gl/AW4cfX2w8sXofQ9q6",
    },
    "plenilunio": {
        "nombre": "Plenilunio",
        "url": "https://maps.app.goo.gl/FBMzHzNo3BK3B8M99",
    },
}

DEFAULT_STORE = "parquesur"
