from sqlalchemy.orm import Session

from app.domain.models.next_step_result import NextStepResult
from app.infrastructure.repositories.regla_repository import ReglaRepository


class NextStepPolicy:

    def __init__(self, db: Session):

        self.db = db
        self.regla_repo = ReglaRepository(db)


    def determine_next_step(
        self,
        compania_id,
        tipo_caso: str,
        prioridad: str,
    ) -> NextStepResult:

        regla = self.regla_repo.get_regla_by_tipo_caso(
            compania_id,
            tipo_caso
        )

        if regla and regla.siguiente_paso:

            return NextStepResult(
                action=regla.siguiente_paso,
                reason="Definido por regla de negocio."
            )

        return NextStepResult(
            action="RESPUESTA_DIRECTA",
            reason="Caso manejable internamente."
        )
