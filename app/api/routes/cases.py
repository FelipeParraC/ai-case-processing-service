import uuid
import time

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.infrastructure.database.dependencies import get_db
from app.infrastructure.repositories.company_repository import CompanyRepository
from app.infrastructure.repositories.request_log_repository import RequestLogRepository

from app.api.schemas.case_request import CaseProcessRequest
from app.api.schemas.case_response import CaseProcessResponse

from app.domain.validators.minimum_information_validator import MinimumInformationValidator

from app.application.services.classification_service import ClassificationService


router = APIRouter(prefix="/cases", tags=["Cases"])


@router.post("/process", response_model=CaseProcessResponse)
def process_case(
    request: CaseProcessRequest,
    db: Session = Depends(get_db),
):

    start_time = time.time()

    request_id = str(uuid.uuid4())

    company_repo = CompanyRepository(db)

    company = company_repo.get_by_code(request.company_code)

    if not company:

        RequestLogRepository(db).create(
            request_id=request_id,
            company_id=None,
            status="FAILED",
            error_code="COMPANY_NOT_FOUND",
        )

        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )
    
    validator = MinimumInformationValidator()
    validation = validator.validate(request.message)

    if not validation.is_valid:

        RequestLogRepository(db).create(
            request_id=request_id,
            company_id=company.id,
            status="INVALID",
            error_code="INVALID_MESSAGE",
            error_detail={
                "missing_fields": validation.missing_fields,
                "errors": validation.errors
            }
        )

        return CaseProcessResponse(
            request_id=request_id,
            status="INVALID",
            company_found=True,
            message="Message does not contain minimum required information",
            metadata={
                "missing_fields": validation.missing_fields,
                "errors": validation.errors
            }
        )
    
    classification_service = ClassificationService(db)
    classification = classification_service.classify(
        company.id,
        validation.cleaned_message
    )

    latency_ms = int((time.time() - start_time) * 1000)

    RequestLogRepository(db).create(
        request_id=request_id,
        company_id=company.id,
        status="SUCCESS",
        latency_ms=latency_ms,
    )

    return CaseProcessResponse(
        request_id=request_id,
        status="CLASSIFIED",
        company_found=True,
        message="Case classified successfully",
        metadata={
            "case_type": classification.case_type,
            "confidence": classification.confidence,
            "justification": classification.justification,
        }
    )

