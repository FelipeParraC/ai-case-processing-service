class SolicitudValidationService:

    MIN_LENGTH = 5
    MIN_CONFIDENCE = 0.5

    @classmethod
    def validate_message(cls, message: str) -> tuple[bool, str]:

        if not message:
            return False, "Mensaje vacío"

        message = message.strip()

        if len(message) < cls.MIN_LENGTH:
            return False, "Mensaje demasiado corto"

        # Detectar garbage patterns
        garbage_patterns = [
            "lorem ipsum",
            "asdf",
            "qwerty",
            "'; drop table"
        ]

        malicious_patterns = [
            "<script",
            "</script>",
            "javascript:",
            "drop table",
            "--",
        ]


        lower_msg = message.lower()

        for pattern in garbage_patterns:
            if pattern in lower_msg:
                return False, "Mensaje inválido o malicioso"
            
        for pattern in malicious_patterns:
            if pattern in lower_msg:
                return False, "Mensaje inválido o malicioso"

        return True, ""

    @classmethod
    def validate_classification(
        cls,
        confidence: float
    ) -> tuple[bool, str]:

        if confidence < cls.MIN_CONFIDENCE:
            return False, "Confidence demasiado bajo"

        return True, ""
