import json
from groq import Groq

from app.core.config import settings


class ExtractionService:

    def __init__(self):

        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )

        self.model = settings.GROQ_MODEL


    def extract_document(self, text: str):

        prompt = f"""
Extrae el documento del cliente del siguiente texto.

REGLAS:

- Si encuentras un documento, extrae:
  tipo_documento: CC, CE, NIT o PASAPORTE
  numero_documento: el número exacto

- Si NO hay documento en el texto, devuelve campos vacíos.

Responde SOLO en JSON válido.

Formato de respuesta:

{{
  "tipo_documento": "",
  "numero_documento": ""
}}

Texto:
{text}
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
            data = json.loads(content)

            return {
                "tipo_documento": data.get("tipo_documento", "") or "",
                "numero_documento": data.get("numero_documento", "") or "",
            }

        except Exception:

            # fallback seguro production-grade
            return {
                "tipo_documento": "",
                "numero_documento": ""
            }

