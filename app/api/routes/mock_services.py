from fastapi import APIRouter

router = APIRouter(prefix="/mock", tags=["Mock Services"])

@router.post("/mensajeria-del-valle/prioridad")
def prioridad_mensajeria_del_valle(payload: dict):
    """
    Simula un servicio externo real que retorna prioridad.
    Recibe (por ejemplo):
      - tipo_documento
      - numero_documento_cliente
      - tipo_solicitud
      - descripcion
    """

    descripcion = (payload.get("descripcion") or "").lower()
    tipo_solicitud = (payload.get("tipo_solicitud") or "").lower()

    # regla mock sencilla (puedes sofisticarla)
    if any(k in descripcion for k in ["robo", "perdido", "urgente", "nunca llegó", "nunca llego", "fuga", "peligroso"]):
        return {"prioridad": "Alta", "reason": "Palabras clave críticas detectadas por servicio externo."}

    if "retraso" in descripcion or "demora" in descripcion or "tarde" in descripcion:
        return {"prioridad": "Media", "reason": "Retraso detectado por servicio externo."}

    if "consulta" in tipo_solicitud or "información" in descripcion or "informacion" in descripcion:
        return {"prioridad": "Baja", "reason": "Caso informativo detectado por servicio externo."}

    return {"prioridad": "Media", "reason": "Prioridad por defecto del servicio externo."}
