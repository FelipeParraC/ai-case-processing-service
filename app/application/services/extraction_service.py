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

Texto:
{text}

Responde SOLO en JSON:

{{
  "tipo_documento": "CC",
  "numero_documento": "string"
}}
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

        content = response.choices[0].message.content

        return json.loads(content)
