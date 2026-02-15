import json
import re

from groq import Groq
from app.core.config import settings


DOCUMENT_PATTERNS = [
    # CC explícito
    (re.compile(r"\bCC\s*[:\-]?\s*([0-9][0-9\.\-\s]{4,30}[0-9])\b", re.IGNORECASE), "CC"),

    # Cedula con palabra explícita
    (re.compile(r"\bC[EÉ]DULA(?:\s+DE\s+CIUDADAN[IÍ]A)?\s*(?:ES|:)?\s*([0-9][0-9\.\-\s]{4,30}[0-9])", re.IGNORECASE), "CC"),

    # Numero de cedula
    (re.compile(r"\bNUMERO\s+DE\s+C[EÉ]DULA\s*(?:ES|:)?\s*([0-9][0-9\.\-\s]{4,30}[0-9])", re.IGNORECASE), "CC"),

    # Documento
    (re.compile(r"\bDOCUMENTO\s*(?:ES|:)?\s*([0-9][0-9\.\-\s]{4,30}[0-9])", re.IGNORECASE), "CC"),

    # TI
    (re.compile(r"\bTI\s*[:\-]?\s*([0-9][0-9\.\-\s]{4,30}[0-9])\b", re.IGNORECASE), "TI"),

    # CE
    (re.compile(r"\bCE\s*[:\-]?\s*([0-9][0-9\.\-\s]{4,30}[0-9])\b", re.IGNORECASE), "CE"),

    # NIT
    (re.compile(r"\bNIT\s*[:\-]?\s*([0-9][0-9\.\-\s]{4,30}[0-9])\b", re.IGNORECASE), "NIT"),

    # PASAPORTE
    (re.compile(r"\bPASAPORTE\s*[:\-]?\s*([0-9][0-9\.\-\s]{4,30}[0-9])\b", re.IGNORECASE), "PASAPORTE"),
]


class ExtractionService:

    def __init__(self):

        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )

        self.model = settings.GROQ_MODEL


    def extract_document(self, text: str):

        # 1. Intentar extracción regex robusta
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

        # 2. fallback LLM
        return self._llm_extract(text)



    def _llm_extract(self, text: str):
        prompt = f"""
Tu tarea es extraer el tipo y número de documento de identidad desde el texto.

Reglas:
- Relaciona CC con cédula de ciudadanía o solo cédula, TI con tarjeta de identidad, CE con cédula de extranjería, NIT con número de identificación tributaria, PASAPORTE con pasaporte
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

