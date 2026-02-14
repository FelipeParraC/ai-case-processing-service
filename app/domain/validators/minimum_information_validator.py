import re

from app.domain.models.validation_result import ValidationResult


class MinimumInformationValidator:

    MIN_LENGTH = 10

    NOISE_PATTERNS = [
        r"^\s*$",
        r"^[\W_]+$",
    ]


    def validate(self, message: str) -> ValidationResult:

        missing_fields = []
        errors = []

        if not message:
            return ValidationResult(
                is_valid=False,
                missing_fields=["message"],
                errors=["Message is empty"],
                cleaned_message=""
            )

        cleaned = message.strip()

        # Validar longitud mínima

        if len(cleaned) < self.MIN_LENGTH:
            missing_fields.append("message_detail")
            errors.append("Message too short")

        # Detectar ruido

        for pattern in self.NOISE_PATTERNS:

            if re.match(pattern, cleaned):
                errors.append("Message contains only noise")
                break

        is_valid = len(errors) == 0

        return ValidationResult(
            is_valid=is_valid,
            missing_fields=missing_fields,
            errors=errors,
            cleaned_message=cleaned
        )
