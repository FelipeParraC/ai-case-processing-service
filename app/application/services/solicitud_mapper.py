from datetime import date


PRIORITY_MAP = {

    "HIGH": "Alta",
    "MEDIUM": "Media",
    "LOW": "Baja",

    "Alta": "Alta",
    "Media": "Media",
    "Baja": "Baja",
}


NEXT_STEP_MAP = {

    "ESCALATE_IMMEDIATELY": "GESTION_EXTERNA",
    "CREATE_EXTERNAL_CASE": "GESTION_EXTERNA",

    "RESPOND_DIRECTLY": "RESPUESTA_DIRECTA",
    "QUEUE_FOR_REVIEW": "RESPUESTA_DIRECTA",

    "INSUFFICIENT_INFORMATION": "CIERRE_POR_INFORMACION_INSUFICIENTE",
    "CLOSE_INSUFFICIENT_INFO": "CIERRE_POR_INFORMACION_INSUFICIENTE",

    "GESTION_EXTERNA": "GESTION_EXTERNA",
    "RESPUESTA_DIRECTA": "RESPUESTA_DIRECTA",
    "CIERRE_POR_INFORMACION_INSUFICIENTE": "CIERRE_POR_INFORMACION_INSUFICIENTE",
}


class SolicitudMapper:

    def map_success(
        self,
        compania: str,
        solicitud_id: str,
        classification,
        priority,
        extraction,
        external_case,
        next_step,
    ):

        prioridad = PRIORITY_MAP.get(
            priority.level,
            "Media"
        )

        proximo_paso = NEXT_STEP_MAP.get(
            next_step.action,
            "RESPUESTA_DIRECTA"
        )

        solicitud_id_plataforma = (
            external_case.case_id
            if external_case and proximo_paso == "GESTION_EXTERNA"
            else None
        )

        estado = (
            "pendiente"
            if proximo_paso == "GESTION_EXTERNA"
            else "cerrado"
        )

        tipo = (
            classification.case_type
            if classification.case_type
            else "No clasificada"
        )

        justificacion = (
            classification.justification
            if classification.justification
            else "Clasificación automática basada en reglas del sistema."
        )

        return {

            "compania": compania,

            "solicitud_id": solicitud_id,

            "solicitud_fecha": date.today().isoformat(),

            "solicitud_tipo": tipo,

            "solicitud_prioridad": prioridad,

            "solicitud_id_cliente": extraction.get(
                "numero_documento",
                ""
            ),

            "solicitud_tipo_id_cliente": extraction.get(
                "tipo_documento",
                ""
            ),

            "solicitud_id_plataforma_externa": solicitud_id_plataforma,

            "proximo_paso": proximo_paso,

            "justificacion": justificacion,

            "estado": estado,
        }


    def map_insufficient_information(
        self,
        compania: str,
        solicitud_id: str,
    ):

        return {

            "compania": compania,

            "solicitud_id": solicitud_id,

            "solicitud_fecha": date.today().isoformat(),

            "solicitud_tipo": "No clasificada",

            "solicitud_prioridad": "Baja",

            "solicitud_id_cliente": "",

            "solicitud_tipo_id_cliente": "",

            "solicitud_id_plataforma_externa": None,

            "proximo_paso": "CIERRE_POR_INFORMACION_INSUFICIENTE",

            "justificacion": "Información incompleta o faltante.",

            "estado": "cerrado",
        }
