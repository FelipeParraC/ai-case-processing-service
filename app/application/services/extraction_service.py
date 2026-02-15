import json
import re

from groq import Groq
from app.core.config import settings


DOCUMENT_REGEX = re.compile(
    r"\b(CC|TI|CE|NIT|PASAPORTE)\s*[:\-]?\s*(\d{5,15})\b",
    re.IGNORECASE,
)


class ExtractionService:

    def __init__(self):

        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )

        self.model = settings.GROQ_MODEL


    def extract_document(self, text: str):

        match = DOCUMENT_REGEX.search(text)

        if match:

            return {
                "tipo_documento": match.group(1).upper(),
                "numero_documento": match.group(2),
            }

        return self._llm_extract(text)


    def _llm_extract(self, text: str):

        prompt = f"""
Extrae el documento del cliente del siguiente texto.

Texto:
{text}

Si NO hay documento, responde:

{{
  "tipo_documento": "",
  "numero_documento": ""
}}

Si hay documento, responde:

{{
  "tipo_documento": "CC",
  "numero_documento": "12345678"
}}

RESPONDE SOLO JSON.
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        content = response.choices[0].message.content.strip()

        try:
            return json.loads(content)
        except Exception:
            return {
                "tipo_documento": "",
                "numero_documento": ""
            }
