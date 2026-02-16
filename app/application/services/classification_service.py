from sqlalchemy.orm import Session

from app.infrastructure.repositories.categoria_repository import CategoriaRepository
from app.infrastructure.repositories.regla_repository import ReglaRepository

from app.infrastructure.llm.llm_adapter import GroqLLMClient

from app.domain.models.llm_classification_result import LLMClassificationResult

from app.application.services.solicitud_validation_service import SolicitudValidationService


class ClassificationService:

    def __init__(self, db: Session):

        self.db = db

        self.categoria_repo = CategoriaRepository(db)

        self.regla_repo = ReglaRepository(db)

        self.llm = GroqLLMClient()


    def classify(
        self,
        compania_id,
        message
    ) -> LLMClassificationResult:


        # =====================================
        # VALIDACIÓN
        # =====================================

        is_valid, reason = SolicitudValidationService.validate_message(message)

        if not is_valid:

            return LLMClassificationResult(

                case_type="INVALIDO",

                justification=f"Solicitud inválida: {reason}",

                confidence=0.0
            )


        # =====================================
        # OBTENER CATEGORIAS
        # =====================================

        categorias = self.categoria_repo.get_by_compania(compania_id)

        nombres_categorias = [c.nombre for c in categorias]


        # =====================================
        # LLM CLASIFICATION
        # =====================================

        llm_result = self.llm.classify_case(
            message,
            nombres_categorias
        )


        confidence = getattr(llm_result, "confidence", 0.0)


        is_valid_conf, conf_reason = SolicitudValidationService.validate_classification(
            confidence
        )

        if not is_valid_conf:

            return LLMClassificationResult(

                case_type="INVALIDO",

                justification=f"Solicitud inválida: {conf_reason}",

                confidence=confidence
            )


        tipo_caso = llm_result.case_type


        # =====================================
        # OBTENER REGLA
        # =====================================

        regla = self.regla_repo.get_regla_by_tipo_caso(
            compania_id,
            tipo_caso
        )


        # =====================================
        # GENERAR JUSTIFICACIÓN DINÁMICA
        # =====================================

        justificacion = self._generate_justification(

            message=message,

            tipo_caso=tipo_caso,

            regla=regla,

            fallback=llm_result.justification
        )


        return LLMClassificationResult(

            case_type=tipo_caso,

            justification=justificacion,

            confidence=confidence
        )


    def _generate_justification(
        self,
        message,
        tipo_caso,
        regla,
        fallback
    ):


        if not regla:

            return fallback


        prompt = f"""
Eres un analista de solicitudes.

Tipo de caso:
{tipo_caso}

Prioridad definida por reglas:
{regla.prioridad}

Palabras clave de la regla:
{regla.palabras_clave}

Mensaje del cliente:
{message}

Redacta una justificación corta en español explicando por qué este caso tiene esa prioridad.

No inventes información.
Usa el mensaje real.
Máximo 20 palabras.
"""


        response = self.llm.client.chat.completions.create(

            model=self.llm.model,

            messages=[
                {
                    "role": "system",
                    "content": "Eres un analista profesional. Responde solo en español."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0
        )


        return response.choices[0].message.content.strip()
