from sqlalchemy.orm import Session

from app.infrastructure.database.models import (
    Compania,
    Categoria,
    Regla,
)


def seed_database(db: Session):

    companias_data = [

        {
            "nombre": "GASES DEL ORINOCO",

            "usa_servicio_prioridad_externo": False,

            "categorias": [
                "Incidente técnico",
                "Consulta",
                "Queja",
                "Solicitud administrativa",
            ],

            "reglas": [

                {
                    "tipo_caso": "Incidente técnico",

                    "palabras_clave": [
                        "estufa"
                    ],

                    "prioridad": "Alta",

                    "siguiente_paso": "GESTION_EXTERNA",

                    "plantilla_justificacion":
                        "Se detecta falla técnica en estufa de gas que requiere intervención externa."
                },

                {
                    "tipo_caso": "Consulta",

                    "palabras_clave": [
                        "consulta",
                        "información",
                        "pregunta"
                    ],

                    "prioridad": "Baja",

                    "siguiente_paso": "RESPUESTA_DIRECTA",

                    "plantilla_justificacion":
                        "Solicitud informativa que puede resolverse internamente."
                }

            ]
        },

        {
            "nombre": "MENSAJERIA DEL VALLE",

            "usa_servicio_prioridad_externo": True,

            "categorias": [
                "Problema de entrega",
                "Consulta",
                "Queja",
            ],

            "reglas": [

                {
                    "tipo_caso": "Problema de entrega",

                    "palabras_clave": [
                        "entrega",
                        "paquete",
                        "no llegó",
                        "retraso"
                    ],

                    "prioridad": "Media",

                    "siguiente_paso": "GESTION_EXTERNA",

                    "plantilla_justificacion":
                        "Incidente relacionado con logística de entrega."
                }

            ]
        }

    ]


    for compania_data in companias_data:

        compania = (
            db.query(Compania)
            .filter_by(nombre=compania_data["nombre"])
            .first()
        )

        if not compania:

            compania = Compania(
                nombre=compania_data["nombre"],
                usa_servicio_prioridad_externo=compania_data.get(
                    "usa_servicio_prioridad_externo",
                    False
                )
            )

            db.add(compania)

            db.flush()

        else:

            # actualizar flag si cambió
            compania.usa_servicio_prioridad_externo = compania_data.get(
                "usa_servicio_prioridad_externo",
                False
            )


        # ============================================
        # Categorías
        # ============================================

        for categoria_nombre in compania_data["categorias"]:

            existe = (
                db.query(Categoria)
                .filter_by(
                    compania_id=compania.id,
                    nombre=categoria_nombre
                )
                .first()
            )

            if not existe:

                db.add(
                    Categoria(
                        compania_id=compania.id,
                        nombre=categoria_nombre,
                        activa=True
                    )
                )


        # ============================================
        # Reglas
        # ============================================

        for regla_data in compania_data["reglas"]:

            existe = (
                db.query(Regla)
                .filter_by(
                    compania_id=compania.id,
                    tipo_caso=regla_data["tipo_caso"]
                )
                .first()
            )

            if existe:
                continue

            db.add(
                Regla(
                    compania_id=compania.id,

                    tipo_caso=regla_data["tipo_caso"],

                    palabras_clave=regla_data["palabras_clave"],

                    prioridad=regla_data["prioridad"],

                    siguiente_paso=regla_data["siguiente_paso"],

                    plantilla_justificacion=regla_data["plantilla_justificacion"],
                )
            )


    db.commit()

    print("Database seeded successfully")
