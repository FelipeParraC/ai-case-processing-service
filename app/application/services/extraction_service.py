import json
import re

from groq import Groq
from app.core.config import settings


DOCUMENT_REGEX = re.compile(
    r"\b(CC|TI|CE|NIT|PASAPORTE)\s*[:\-]?\s*([0-9][0-9\.\-\s]{4,30}[0-9])\b",
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
            raw = match.group(2)
            numero = re.sub(r"\D", "", raw)  # quita puntos/espacios/guiones
            if 5 <= len(numero) <= 15:
                return {
                    "tipo_documento": match.group(1).upper(),
                    "numero_documento": numero,
                }

        return self._llm_extract(text)


    def _llm_extract(self, text: str):
        prompt = f"""
Tu tarea es extraer el tipo y número de documento de identidad desde el texto.

Reglas:
- Solo acepta tipos: CC, TI, CE, NIT, PASAPORTE
- El numero_documento debe contener SOLO dígitos (0-9)
- Si el texto no contiene un documento claro, devuelve ambos campos vacíos.
- NO inventes números. NO uses ejemplos. NO completes con valores por defecto.
- Responde SOLO un JSON válido, sin explicación, sin markdown.

Texto:
{text}

Salida JSON (única respuesta posible):
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
            return {"tipo_documento": "", "numero_documento": ""}

        # hard validation: evitar que el modelo invente basura
        tipo = (data.get("tipo_documento") or "").upper().strip()
        num = re.sub(r"\D", "", data.get("numero_documento") or "")

        if tipo not in {"CC", "TI", "CE", "NIT", "PASAPORTE"}:
            return {"tipo_documento": "", "numero_documento": ""}

        if not (5 <= len(num) <= 15):
            return {"tipo_documento": "", "numero_documento": ""}

        return {"tipo_documento": tipo, "numero_documento": num}

