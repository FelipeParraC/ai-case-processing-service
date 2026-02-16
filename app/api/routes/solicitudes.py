from fastapi import APIRouter, Depends, Request, Response, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.application.services.extraction_service import ExtractionService
from app.application.services.platform_service import PlatformService
from app.core.json_utils import to_json_serializable
from app.infrastructure.database.dependencies import get_db

from app.infrastructure.repositories.compania_repository import CompaniaRepository
from app.infrastructure.repositories.solicitud_repository import SolicitudRepository
from app.infrastructure.repositories.log_solicitud_repository import LogSolicitudRepository

from app.application.services.classification_service import ClassificationService
from app.application.services.priority_service import PriorityService

from app.domain.policies.next_step_policy import NextStepPolicy

from app.api.schemas.solicitud_request import SolicitudRequest
from app.api.schemas.solicitud_response import SolicitudResponse

from app.domain.validators.minimum_information_validator import MinimumInformationValidator

from app.core.logger import get_logger


logger = get_logger("solicitudes")
router = APIRouter(prefix="/solicitudes", tags=["Solicitudes"])


@router.post("/procesar", response_model=SolicitudResponse)
def procesar_solicitud(
    payload: SolicitudRequest,
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):

    id_request = request.state.request_id

    log_repo = LogSolicitudRepository(db)

    start_time = datetime.utcnow()


    try:

        # =====================================
        # VALIDAR COMPAÑÍA
        # =====================================

        compania_repo = CompaniaRepository(db)

        compania = compania_repo.get_by_nombre(payload.compania)

        if not compania:

            raise HTTPException(
                status_code=404,
                detail="Compañía no encontrada"
            )


        # =====================================
        # IDEMPOTENCIA CHECK
        # =====================================

        solicitud_repo = SolicitudRepository(db)

        existing = solicitud_repo.get(
            compania.id,
            payload.solicitud_id
        )

        if existing:

            response.headers["X-Idempotent-Replay"] = "true"

            return existing.respuesta_json


        response.headers["X-Idempotent-Replay"] = "false"

        # =====================================
        # VALIDACIÓN MÍNIMA
        # =====================================

        validator = MinimumInformationValidator()

        validation_result = validator.validate(payload.solicitud_descripcion)

        if not validation_result.is_valid:

            estado = "cerrado"

            prioridad = "N/A"

            siguiente_paso = "CIERRE_POR_INFORMACION_INSUFICIENTE"

            external_case_id = None

        # =====================================
        # CLASIFICACIÓN
        # =====================================

        classification = ClassificationService(db).classify(
            compania.id,
            payload.solicitud_descripcion
        )

        extraction = None

        # =====================================
        # VALIDACIÓN RESULTADO CLASIFICACIÓN
        # =====================================

        if classification.case_type == "INVALIDO":

            estado = "cerrado"

            prioridad = "N/A"

            siguiente_paso = "RESPUESTA_DIRECTA"

            external_case_id = None


        else:

            # =====================================
            # PRIORIDAD
            # =====================================

            priority_result = PriorityService(db).determine_priority(
                compania.id,
                payload.solicitud_descripcion,
                classification.case_type,
                extracted=None
            )

            prioridad = priority_result.level

            # =====================================
            # NEXT STEP
            # =====================================

            next_step_result = NextStepPolicy(db).determine_next_step(
                compania.id,
                classification.case_type,
                prioridad
            )

            siguiente_paso = next_step_result.action

            estado = (
                "pendiente"
                if siguiente_paso == "GESTION_EXTERNA"
                else "cerrado"
            )

            external_case_id = None
            
            if compania.usa_servicio_prioridad_externo:

                external_case = PlatformService().create_case(
                    compania.id,
                    classification.case_type,
                    prioridad,
                    payload.solicitud_descripcion
                )

                external_case_id = external_case.case_id


            extraction = ExtractionService().extract_document(
                payload.solicitud_descripcion
            )


        # =====================================
        # CREAR RESPONSE
        # =====================================

        response_data = {

            "compania": compania.nombre,

            "solicitud_id": payload.solicitud_id,

            "solicitud_fecha": datetime.utcnow().date(),

            "solicitud_tipo": classification.case_type,

            "solicitud_prioridad": prioridad,

            "solicitud_id_cliente": extraction["numero_documento"] if extraction else "",

            "solicitud_tipo_id_cliente": extraction["tipo_documento"] if extraction else "",

            "solicitud_id_plataforma_externa": external_case_id,

            "proximo_paso": siguiente_paso,

            "justificacion": classification.justification,

            "estado": estado

        }


        # =====================================
        # PERSISTENCIA
        # =====================================

        solicitud_repo.create(

            compania_id=compania.id,

            solicitud_id=payload.solicitud_id,

            id_request=id_request,

            estado=estado,

            id_caso_externo=external_case_id,

            respuesta_json=to_json_serializable(response_data)

        )


        # =====================================
        # LOG SUCCESS
        # =====================================

        latency = int(
            (datetime.utcnow() - start_time).total_seconds() * 1000
        )

        log_repo.create(

            id_request=id_request,

            compania_id=compania.id,

            estado="success",

            latencia_ms=latency

        )


        return response_data


    except HTTPException as e:

        logger.warning(
            f"HTTPException | id_request={id_request} | detail={e.detail}"
        )

        log_repo.create(

            id_request=id_request,

            compania_id=None,

            estado="error",

            codigo_error=str(e.status_code),

            detalle_error={"detail": e.detail}

        )

        raise e


    except Exception as e:

        logger.error(
            f"Unhandled exception | id_request={id_request} | error={str(e)}"
        )

        log_repo.create(

            id_request=id_request,

            compania_id=None,

            estado="error",

            codigo_error="internal_error",

            detalle_error={"error": str(e)}

        )

        raise HTTPException(
            status_code=500,
            detail="Error interno"
        )
