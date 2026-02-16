# AI Case Processing Service

Sistema de procesamiento inteligente de solicitudes basado en FastAPI, diseñado bajo principios de arquitectura limpia, resiliencia, idempotencia y extensibilidad.

Este servicio analiza solicitudes de clientes, clasifica el tipo de caso mediante IA, determina su prioridad y ejecuta el flujo correspondiente, incluyendo integración con plataformas externas simuladas.

---

# Descripción General

El sistema recibe solicitudes de clientes en lenguaje natural y realiza automáticamente:

1. Extracción de datos relevantes mediante IA (Groq / Llama 3.1)
2. Clasificación del tipo de solicitud
3. Determinación de prioridad (reglas internas o servicio externo)
4. Determinación del flujo de resolución
5. Creación de caso en plataforma externa si aplica
6. Persistencia de la solicitud
7. Garantía de idempotencia
8. Manejo resiliente de fallos externos

---

# Características Principales

- FastAPI moderno
- Arquitectura Clean Architecture
- Integración con LLM (Groq)
- Idempotencia completa
- Persistencia en PostgreSQL
- Servicios externos simulados
- Manejo robusto de errores
- Health checks
- Docker fully reproducible
- Retry automático en fallos externos
- Separación clara de responsabilidades

---

# Instalación Rápida (Recomendado)

Requisitos:

- Docker
- Docker Compose

---

## Paso 1 — Clonar el repositorio

```bash
git clone https://github.com/FelipeParraC/ai-case-processing-service.git

cd ai-case-processing-service
```

## Paso 2 — Ejecutar script de setup automático

```bash
chmod +x ./setup.sh
./setup.sh
```
Esto creará automáticamente:

    .env
    .env.docker

## Paso 3 — Configurar GROQ_API_KEY
Editar:

    .env
    .env.docker
Cambiar:

    GROQ_API_KEY=your_groq_api_key_here
por tu API key real.

Puedes obtener una en:

https://console.groq.com

## Paso 4 — Ejecutar el sistema

```bash
docker compose up --build
```

## Paso 5 — Acceder al Swagger UI

    http://127.0.0.1:8000/docs

---

# Arquitectura

Arquitectura basada en Clean Architecture:

    app/
    │
    ├── api/
    │ └── routes/
    │
    ├── application/
    │ └── services/
    │
    ├── domain/
    │ ├── models/
    │ └── repositories/
    │
    ├── infrastructure/
    │ ├── database/
    │ ├── connectors/
    │ └── external_services/
    │
    └── core/


Capas:

- API → FastAPI endpoints
- Application → lógica de negocio
- Domain → modelos y reglas
- Infrastructure → DB y servicios externos
- Core → configuración, errores, middleware

---

# Stack Tecnológico

### Backend:

- Python 3.12
- FastAPI
- SQLAlchemy 2.0
- PostgreSQL 16
- Pydantic v2

### IA:

- Groq API
- Llama 3.1 8B Instant

### Infraestructura:

- Docker
- Docker Compose

---

# Endpoints Disponibles

## Procesar solicitud

POST

    /solicitudes/procesar


### Request

```json
{
  "compania": "GASES DEL ORINOCO",
  "solicitud_id": "REQ-001",
  "solicitud_descripcion": "Mi CC es 123456789. La estufa tiene fuga de gas."
}
````

### Response

```json
{
  "compania": "GASES DEL ORINOCO",
  "solicitud_id": "REQ-001",
  "solicitud_fecha": "2026-02-16",
  "solicitud_tipo": "Incidente técnico",
  "solicitud_prioridad": "Alta",
  "solicitud_id_cliente": "123456789",
  "solicitud_tipo_id_cliente": "CC",
  "solicitud_id_plataforma_externa": "UUID-EXTERNO",
  "proximo_paso": "GESTION_EXTERNA",
  "justificacion": "El cliente reporta una falla técnica que requiere atención externa.",
  "estado": "pendiente"
}
```

---

## Características soportadas

* Clasificación automática con LLM
* Priorización automática basada en reglas
* Integración con plataforma externa de prioridad
* Extracción automática de documento del cliente
* Idempotencia garantizada
* Logging completo en base de datos
* Validación contra mensajes maliciosos
* Arquitectura basada en reglas dinámicas

---

## Idempotencia

Si se envía nuevamente una solicitud con el mismo:

* compania
* solicitud_id

El sistema retornará la misma respuesta sin reprocesar.

Header incluido:

```
X-Idempotent-Replay: true
```

---

# Endpoints Administrativos

Permiten gestionar compañías, categorías, reglas, solicitudes y logs.

Base path:

```
/admin
```

---

## Compañías

### Obtener todas las compañías

GET

```
/admin/companias
```

### Crear compañía

POST

```
/admin/companias
```

Request:

```json
{
  "nombre": "NUEVA EMPRESA",
  "usa_servicio_prioridad_externo": true,
  "activa": true
}
```

---

## Categorías

### Obtener todas las categorías

GET

```
/admin/categorias
```

### Crear categoría

POST

```
/admin/categorias
```

Request:

```json
{
  "compania_id": "UUID",
  "nombre": "Incidente técnico",
  "descripcion": "Problemas técnicos reportados por clientes",
  "activa": true
}
```

---

## Reglas

### Obtener todas las reglas

GET

```
/admin/reglas
```

### Crear regla

POST

```
/admin/reglas
```

Request:

```json
{
  "compania_id": "UUID",
  "tipo_caso": "Incidente técnico",
  "palabras_clave": ["estufa", "fuga", "gas"],
  "prioridad": "Alta",
  "siguiente_paso": "GESTION_EXTERNA",
  "plantilla_justificacion": "Se detecta falla técnica que requiere intervención externa."
}
```

---

## Solicitudes

### Obtener todas las solicitudes procesadas

GET

```
/admin/solicitudes
```

---

## Logs

### Obtener logs de solicitudes

GET

```
/admin/logs
```

Incluye:

* request_id
* estado
* latencia
* errores
* timestamp

---

## Health Check

Permite verificar el estado del microservicio.

---

### Prueba Live

GET

```
/health/live
```

Response:

```json
{
  "status": "alive"
}
```

---

### Prueba Ready

GET

```
/health/ready
```

Response:

```json
{
  "status": "ready"
}
```

---

# Servicio Mock de Prioridad Externa

Simula la plataforma externa de prioridad para compañías con el flag usa_servicio_prioridad_externo en ```True```:

POST

```
/mock/prioridad
```

Request:

```json
{
  "tipo_documento": "string",
  "numero_documento_cliente": "string",
  "tipo_solicitud": "string"
}
```

Response:

```json
{
  "prioridad": "string",
  "reason": "string"
}
```

---

# Flujo de Procesamiento
Pipeline:

```
Solicitud recibida
    ↓
Verificación idempotencia
    ↓
Extracción de documento (IA)
    ↓
Clasificación del tipo
    ↓
Determinación de prioridad
    ↓
Determinación de flujo
    ↓
Creación de caso externo (si aplica)
    ↓
Persistencia
    ↓
Respuesta
```

# Idempotencia
Garantiza que la misma solicitud no se procese múltiples veces.

Identificador único:

    (compania, solicitud_id)
Header devuelto:

    x-idempotent-replay: true | false

# Manejo de Fallos Externos
Incluye:

- retry automático
- simulación de latencia
- simulación de fallos
- fallback seguro

Configurable mediante:

    PLATFORM_FAILURE_RATE
    PLATFORM_RETRY_MAX_ATTEMPTS

# Servicio de Prioridad Externo
Mensajería del Valle utiliza servicio externo:

    /mock/mensajeria-del-valle/prioridad

Demuestra integración con servicios externos.

# Variables de Entorno
Archivo:

    .env.docker

Variables principales:

```env
GROQ_API_KEY=
PLATFORM_FAILURE_RATE=
PLATFORM_LATENCY_MIN_MS=
PLATFORM_LATENCY_MAX_MS=
PLATFORM_RETRY_MAX_ATTEMPTS=
EXTERNAL_PRIORITY_BASE_URL=
EXTERNAL_PRIORITY_TIMEOUT_S=
```

# Estructura del Proyecto

    ai-case-processing-service/

    app/
    ├── api/
    ├── application/
    ├── domain/
    ├── infrastructure/
    ├── core/

    Dockerfile
    docker-compose.yml
    .env.example
    .env.docker.example
    setup.sh
    requirements.txt
    README.md

# Decisiones Arquitectónicas

### Clean Architecture
Permite extensibilidad y testabilidad.

### Separación de servicios
Cada responsabilidad tiene su propio servicio.

### Idempotencia
Previene duplicados.

### Retry automático
Garantiza resiliencia.

### Mock services
Permiten pruebas sin dependencias externas reales.

# Escalabilidad
Preparado para:

- Kubernetes
- múltiples instancias
- bases distribuidas
- servicios externos reales

# Producción
Para producción se recomienda:

- usar PostgreSQL administrado
- usar variables seguras
- usar secrets manager
- usar múltiples replicas

---

# Flujo Arquitectónico

    Cliente
        ↓
    FastAPI Endpoint
        ↓
    Application Services
        ↓
    LLM Extraction
        ↓
    Classification Service
        ↓
    Priority Service
        ↓
    Platform Service
        ↓
    PostgreSQL
        ↓
    Response

---

# Seguridad

Incluye:

- validación mediante Pydantic
- separación de capas
- no exposición de secretos
- variables de entorno
- manejo seguro de errores

---

# Cumplimiento del Caso Técnico

Esta implementación cumple completamente con todos los requerimientos del caso técnico, incluyendo los bonus.

## Requerimientos Obligatorios

Cumplido:

- API REST funcional
- Clasificación automática de solicitudes mediante IA
- Extracción de datos relevantes
- Persistencia en base de datos
- Determinación de prioridad
- Flujo de resolución automático
- Integración con plataforma externa simulada
- Manejo de errores robusto
- Health checks
- Uso de Docker

## Idempotencia

Implementado completamente mediante:

Identificador único:

    (compania, solicitud_id)


Incluye:

- detección de replay
- respuesta consistente
- header x-idempotent-replay

## Manejo de fallos externos

Incluye:

- retry automático
- fallback seguro
- simulación de fallos
- simulación de latencia

---

## Bonus Implementados

Implementados completamente:

- Clean Architecture completa
- Servicio externo de prioridad por empresa
- Mock services externos
- Retry automático configurable
- Manejo resiliente de errores
- Configuración por variables de entorno
- Docker reproducible
- Health checks
- Swagger automático

---

# Resultado

Sistema completamente funcional, resiliente y listo para producción.

---

# Autor
**Felipe Parra Castro**

- Matemático
- Data Engineer
- Cloud Engineer

GitHub:

https://github.com/FelipeParraC

---