from fastapi import APIRouter, Depends, HTTPException, logger
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi import Request

from app.infrastructure.database.dependencies import get_db
from app.infrastructure.repositories.company_repository import CompanyRepository
from app.infrastructure.repositories.solicitud_repository import SolicitudRepository

from app.api.schemas.solicitud_request import SolicitudRequest
from app.api.schemas.solicitud_response import SolicitudResponse

from app.domain.validators.minimum_information_validator import MinimumInformationValidator

from app.application.services.classification_service import ClassificationService
from app.application.services.priority_service import PriorityService
from app.application.services.platform_service import PlatformService
from app.application.services.extraction_service import ExtractionService
from app.application.services.solicitud_mapper import SolicitudMapper

from app.domain.policies.next_step_policy import NextStepPolicy


router = APIRouter(prefix="/solicitudes", tags=["Solicitudes"])


@router.post("/procesar", response_model=SolicitudResponse)
def procesar_solicitud(
    request: SolicitudRequest,
    http_request: Request,
    db: Session = Depends(get_db),
):

    company_repo = CompanyRepository(db)

    company = company_repo.get_by_name_or_code(request.compania)

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Compañía no encontrada"
        )

    solicitud_repo = SolicitudRepository(db)

    existing = solicitud_repo.get(
        company.id,
        request.solicitud_id
    )

    if existing:

        logger.info(
            "idempotent_replay",
            extra={
                "request_id": http_request.state.request_id,
                "company_id": str(company.id),
                "solicitud_id": request.solicitud_id,
            }
        )

        return JSONResponse(
            content=existing.response_json,
            headers={
                "X-Idempotent-Replay": "true"
            }
        )


    if not company:
        raise HTTPException(404, "Compañía no encontrada")

    validator = MinimumInformationValidator()

    validation = validator.validate(request.solicitud_descripcion)

    if not validation.is_valid:

        result = SolicitudMapper().map_insufficient_information(
            compania=request.compania,
            solicitud_id=request.solicitud_id,
        )

        solicitud_repo.create(
            company_id=company.id,
            solicitud_id=request.solicitud_id,
            request_id=http_request.state.request_id,
            status=result["estado"],
            external_case_id=None,
            response_json=result,
        )

        return result

    classification = ClassificationService(db).classify(
        company.id,
        validation.cleaned_message
    )

    priority = PriorityService().determine_priority(
        request.compania,
        validation.cleaned_message,
        classification.case_type
    )

    extraction = ExtractionService().extract_document(
        validation.cleaned_message
    )

    next_step = NextStepPolicy().determine_next_step(
        priority.level,
        classification.case_type
    )

    external_case = None

    if next_step.action == "CREATE_EXTERNAL_CASE":

        external_case = PlatformService().create_case(
            request.compania,
            classification.case_type,
            priority.level,
            validation.cleaned_message
        )

    result = SolicitudMapper().map_success(
        compania=request.compania,
        solicitud_id=request.solicitud_id,
        classification=classification,
        priority=priority,
        extraction=extraction,
        external_case=external_case,
        next_step=next_step,
    )


    solicitud_repo.create(
        company_id=company.id,
        solicitud_id=request.solicitud_id,
        request_id=http_request.state.request_id,
        status=result["estado"],
        external_case_id=result["solicitud_id_plataforma_externa"],
        response_json=result,
    )

    return JSONResponse(
        content=result,
        headers={"X-Idempotent-Replay": "false"}
)


