import httpx
from app.core.config import settings

class ExternalPriorityConnector:
    def __init__(self):
        self.base_url = settings.EXTERNAL_PRIORITY_BASE_URL.rstrip("/")
        self.timeout = settings.EXTERNAL_PRIORITY_TIMEOUT_S

    def get_priority(self, tipo_documento: str, numero_documento: str, tipo_solicitud: str, descripcion: str) -> dict:
        url = f"{self.base_url}/mock/prioridad"

        payload = {
            "tipo_documento": tipo_documento,
            "numero_documento_cliente": numero_documento,
            "tipo_solicitud": tipo_solicitud,
            "descripcion": descripcion,
        }

        with httpx.Client(timeout=self.timeout) as client:
            resp = client.post(url, json=payload)
            resp.raise_for_status()
            return resp.json()
