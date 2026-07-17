"""Nombres del personal mencionados en las reseñas, por tienda.

Cada tienda tiene su propia plantilla porque el mismo nombre de pila puede
pertenecer a personas distintas en tiendas distintas (p. ej. hay una "Andrea"
en ParqueSur y otra en La Gavia — son personas diferentes, no se deben sumar).

Cada clave dentro de "current"/"former" es el nombre canónico a mostrar; la
lista son las variantes de escritura (diminutivos, erratas típicas) que se
buscan como palabra completa dentro del TEXTO de la reseña (nunca del nombre
de quien la escribe). "former" = personas que ya no trabajan ahí pero siguen
apareciendo en reseñas antiguas; se muestran aparte en el dashboard
("Mostrar anteriores").

Las plantillas de ParqueSur están validadas contra reseñas reales (diminutivos
confirmados: Tony→Antonio, Ari→Ariadne, Carol→Carolina, etc.). Las de las
demás tiendas son un primer borrador a partir del listado de empleados —
conviene revisarlas en cuanto se scrapeen reseñas reales de cada una, igual
que se hizo con ParqueSur.
"""

STORE_STAFF = {
    "ParqueSur": {
        "current": {
            "Alvaro": ["alvaro", "álvaro"],
            "Andrea": ["andrea", "andre"],
            "Antonio": ["antonio", "toni", "tony", "tonny"],
            "Ariadne": ["ariadne", "ariadna", "ari"],
            "Blessing": ["blessing", "bless"],
            "Camila": ["camila", "cami"],
            "Carolina": ["carolina", "carol"],
            "Elisabeth": ["elisabeth"],
            "Jonatan": ["jonatan", "jonathan"],
            "Jose": ["jose", "josé"],
            "Natalia": ["natalia"],
            "Noelia": ["noelia"],
            "Sandy": ["sandy"],
            "Valentina": ["valentina"],
            "Valeria": ["valeria"],
            "Vanessa": ["vanessa", "vanesa"],
            "Carlos": ["carlos", "xialei"],  # Xialei Zhu, se presenta como Carlos
        },
        "former": {
            "Alma": ["alma"],
            "Max": ["max", "maxwell", "maxwel", "mawxell"],
            "Dafne": ["dafne"],
            "Lucero": ["lucero"],
            "Aurora": ["aurora"],
        },
    },
    "Caleido": {
        "current": {
            "Ángela": ["ángela", "angela"],
            "Aurelis": ["aurelis"],
            "Catalina": ["catalina"],
            "Dafne": ["dafne"],
            "Dania": ["dania"],
            "Fatima": ["fatima", "fátima"],
            "Jose Luis": ["jose luis", "joseluis", "jose"],
            "Katherin": ["katherin", "katheryn", "kathy"],
        },
        "former": {},
    },
    "Princesa": {
        "current": {
            "Alicia": ["alicia"],
            "Evlinlimar": ["evlinlimar", "margarita"],
            "Gadir": ["gadir"],
            "Natasha": ["natasha"],
            "Nicolas": ["nicolas", "nicolás"],
            "Ramon": ["ramon", "ramón"],
            "Raymar": ["raymar"],
            "Sofia": ["sofia", "sofía", "vanessa"],
        },
        "former": {},
    },
    "La Gavia": {
        "current": {
            "Ana": ["ana"],
            "Andrea": ["andrea"],
            "Elena": ["elena"],
            "Heber": ["heber"],
            "Jesus": ["jesus", "jesús"],
            "Maria Teresa": ["maria teresa", "maite"],
            "Micheilly": ["micheilly"],
            "Sergio": ["sergio"],
            "Slaiman": ["slaiman"],
        },
        "former": {},
    },
    "Gran Plaza 2": {
        "current": {
            "Alfonso": ["alfonso"],
            "Daniela": ["daniela"],
            "Diana": ["diana", "carolina"],
            "Luisa": ["luisa"],
            "Mariana": ["mariana"],
            "Nidia": ["nidia"],
        },
        "former": {},
    },
    "Plenilunio": {
        "current": {
            "Adhara": ["adhara"],
            "Aurora": ["aurora"],
            "Franchesca": ["franchesca", "francesca"],
            "Irun": ["irun", "irún", "estefany"],
            "Lisbeth": ["lisbeth"],
            "Pilar": ["pilar"],
            "Tatiana": ["tatiana"],
            "Veronica": ["veronica", "verónica"],
        },
        "former": {},
    },
}
