import json
import re

from groq import Groq
from app.core.config import settings


DOCUMENT_PATTERNS = [
    (re.compile(r"\bCC\s*[:\-]?\s*([0-9][0-9\.\-\s]{4,30}[0-9])", re.IGNORECASE), "CC"),
    (re.compile(r"\bC[EÉ]DULA\s*(?:ES|:)?\s*([0-9][0-9\.\-\s]{4,30}[0-9])", re.IGNORECASE), "CC"),
    (re.compile(r"\bDOCUMENTO\s*(?:ES|:)?\s*([0-9][0-9\.\-\s]{4,30}[0-9])", re.IGNORECASE), "CC"),
    (re.compile(r"\bIDENTIFICACI[OÓ]N\s*(?:ES|:)?\s*([0-9][0-9\.\-\s]{4,30}[0-9])", re.IGNORECASE), "CC"),
    (re.compile(r"\bTI\s*[:\-]?\s*([0-9][0-9\.\-\s]{4,30}[0-9])", re.IGNORECASE), "TI"),
    (re.compile(r"\bCE\s*[:\-]?\s*([0-9][0-9\.\-\s]{4,30}[0-9])", re.IGNORECASE), "CE"),
    (re.compile(r"\bNIT\s*[:\-]?\s*([0-9][0-9\.\-\s]{4,30}[0-9])", re.IGNORECASE), "NIT"),
    (re.compile(r"\bPASAPORTE\s*[:\-]?\s*([0-9][0-9\.\-\s]{4,30}[0-9])", re.IGNORECASE), "PASAPORTE"),
]


VALID_TYPES = {"CC", "TI", "CE", "NIT", "PASAPORTE"}


class ExtractionService:

    def __init__(self):

        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL


    def extract_document(self, text: str):

        # regex fast path
        result = self._regex_extract(text)

        if result:
            return result

        # LLM fallback
        result = self._llm_extract(text)

        if result:
            return result

        return {
            "tipo_documento": "",
            "numero_documento": ""
        }


    def _regex_extract(self, text: str):

        for pattern, tipo in DOCUMENT_PATTERNS:

            match = pattern.search(text)

            if match:

                raw = match.group(1)

                numero = re.sub(r"\D", "", raw)

                if 5 <= len(numero) <= 15:

                    return {
                        "tipo_documento": tipo,
                        "numero_documento": numero,
                    }

        return None


    def _llm_extract(self, text: str):

        prompt = f"""
Extrae el documento de identidad del cliente desde el siguiente texto.

Reglas importantes:

- tipos válidos: CC, TI, CE, NIT, PASAPORTE
- si el texto menciona "cédula", "cedula", "identificación", "documento", asume CC
- el numero_documento debe contener SOLO dígitos
- NO inventes números
- NO uses ejemplos
- responde SOLO JSON válido

Texto:
{text}

Formato de respuesta:

{{
  "tipo_documento": "CC",
  "numero_documento": "12345678"
}}

Si no hay documento:

{{
  "tipo_documento": "",
  "numero_documento": ""
}}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        content = response.choices[0].message.content.strip()

        try:
            data = json.loads(content)
        except Exception:
            return None

        tipo = (data.get("tipo_documento") or "").upper().strip()

        numero = re.sub(r"\D", "", data.get("numero_documento") or "")

        if tipo not in VALID_TYPES:
            return None

        if not (5 <= len(numero) <= 15):
            return None

        return {
            "tipo_documento": tipo,
            "numero_documento": numero,
        }
