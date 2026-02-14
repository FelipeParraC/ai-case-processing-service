from datetime import date


PRIORITY_MAP = {
    "HIGH": "Alta",
    "MEDIUM": "Media",
    "LOW": "Baja"
}

NEXT_STEP_MAP = {
    "ESCALATE_IMMEDIATELY": "ESCALAMIENTO",
    "CREATE_EXTERNAL_CASE": "GESTIÓN EXTERNA",
    "QUEUE_FOR_REVIEW": "REVISIÓN INTERNA"
}


class SolicitudMapper:

    def map(
        self,
        compania,
        solicitud_id,
        classification,
        priority,
        extraction,
        external_case,
        next_step,
    ):

        return {

            "compania": compania,

            "solicitud_id": solicitud_id,

            "solicitud_fecha": date.today(),

            "solicitud_tipo": classification.case_type,

            "solicitud_prioridad": PRIORITY_MAP.get(
                priority.level,
                "Media"
            ),

            "solicitud_id_cliente": extraction["numero_documento"],

            "solicitud_tipo_id_cliente": extraction["tipo_documento"],

            "solicitud_id_plataforma_externa": (
                external_case.case_id
                if external_case else None
            ),

            "proximo_paso": NEXT_STEP_MAP.get(
                next_step.action,
                "REVISIÓN INTERNA"
            ),

            "justificacion": classification.justification,

            "estado": "pendiente"
        }
