import json
from groq import Groq

from app.core.config import settings
from app.domain.models.llm_classification_result import LLMClassificationResult


class GroqLLMClient:

    def __init__(self):

        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )

        self.model = settings.GROQ_MODEL


    def classify_case(
        self,
        message: str,
        categories: list[str]
    ) -> LLMClassificationResult:

        prompt = self._build_prompt(message, categories)

        response = self.client.chat.completions.create(

            model=self.model,

            messages=[
                {
                    "role": "system",
                    "content": (
                        "Eres un sistema de clasificación de casos de atención al cliente. "
                        "SIEMPRE responde en JSON válido. "
                        "TODOS los textos deben estar en español. "
                        "La 'justification' debe estar en español."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],

            temperature=0,

        )

        content = response.choices[0].message.content

        return self._parse_response(content)


    def _build_prompt(self, message, categories):

        categories_str = ", ".join(categories)

        return f"""
Clasifica el siguiente mensaje del cliente en una de estas categorías:

{categories_str}

Mensaje:
{message}

Responde SOLO en formato JSON válido:

{{
  "case_type": "categoria exacta de la lista",
  "confidence": número entre 0.0 y 1.0,
  "justification": "explicación corta en español"
}}

Si el mensaje no contiene suficiente información, responde:

{{
  "case_type": "INVALIDO",
  "confidence": 0.0,
  "justification": "Mensaje sin suficiente información para clasificación"
}}

"""



    def _parse_response(self, content: str) -> LLMClassificationResult:

        try:

            data = json.loads(content)

            return LLMClassificationResult(**data)

        except Exception as e:

            raise Exception(
                f"Invalid LLM response: {content}"
            ) from e
