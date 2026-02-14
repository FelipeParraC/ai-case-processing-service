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
                        "You are an insurance case classification system. "
                        "Always respond in valid JSON."
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
Classify the following customer message into one of these categories:

{categories_str}

Message:
{message}

Respond ONLY in JSON format:

{{
  "case_type": "category",
  "confidence": 0.0 to 1.0,
  "justification": "short explanation"
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
