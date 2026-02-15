import requests
import uuid
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"


# ==========================================
# UTILIDADES
# ==========================================

def print_header(title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def print_test(name, request_body, response):
    print(f"\nTEST: {name}")
    print("-" * 40)

    if request_body:
        print("REQUEST:")
        print(json.dumps(request_body, indent=2, ensure_ascii=False))

    print("\nSTATUS:", response.status_code)

    try:
        print("\nRESPONSE:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except:
        print(response.text)

    print("\nHEADERS:")
    for k, v in response.headers.items():
        if k.lower().startswith("x-"):
            print(f"{k}: {v}")


def post(path, body):
    return requests.post(
        BASE_URL + path,
        json=body,
        timeout=30
    )


def get(path):
    return requests.get(BASE_URL + path, timeout=30)


def generate_id(prefix):
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


# ==========================================
# TESTS
# ==========================================

def test_health():
    print_header("HEALTH TESTS")

    r1 = get("/health/live")
    print_test("Health Live", None, r1)

    r2 = get("/health/ready")
    print_test("Health Ready", None, r2)


def test_company_not_found():
    print_header("COMPANY NOT FOUND")

    body = {
        "compania": "EMPRESA_INEXISTENTE",
        "solicitud_id": generate_id("REQ"),
        "solicitud_descripcion": "Texto cualquiera"
    }

    r = post("/solicitudes/procesar", body)
    print_test("Company Not Found", body, r)


def test_insufficient_information():
    print_header("INSUFFICIENT INFORMATION")

    body = {
        "compania": "GASES DEL ORINOCO",
        "solicitud_id": generate_id("REQ"),
        "solicitud_descripcion": "Hola"
    }

    r = post("/solicitudes/procesar", body)
    print_test("Insufficient Info", body, r)


def test_direct_response():
    print_header("DIRECT RESPONSE")

    body = {
        "compania": "GASES DEL ORINOCO",
        "solicitud_id": generate_id("REQ"),
        "solicitud_descripcion":
            "Mi CC es 123456789. ¿Cuál es el horario de atención?"
    }

    r = post("/solicitudes/procesar", body)
    print_test("Direct Response", body, r)


def test_external_management():
    print_header("EXTERNAL MANAGEMENT")

    body = {
        "compania": "GASES DEL ORINOCO",
        "solicitud_id": generate_id("REQ"),
        "solicitud_descripcion":
            "Mi CC es 123456789. La estufa tiene fuga de gas peligrosa."
    }

    r = post("/solicitudes/procesar", body)
    print_test("External Management", body, r)


def test_idempotency():
    print_header("IDEMPOTENCY")

    solicitud_id = generate_id("REQ-IDEMP")

    body = {
        "compania": "GASES DEL ORINOCO",
        "solicitud_id": solicitud_id,
        "solicitud_descripcion":
            "Mi CC es 123456789. La estufa presenta falla grave."
    }

    r1 = post("/solicitudes/procesar", body)
    print_test("Idempotency First Call", body, r1)

    r2 = post("/solicitudes/procesar", body)
    print_test("Idempotency Second Call", body, r2)


def test_external_priority_service():
    print_header("EXTERNAL PRIORITY SERVICE")

    body = {
        "compania": "MENSAJERIA DEL VALLE",
        "solicitud_id": generate_id("REQ"),
        "solicitud_descripcion":
            "Mi CC es 777888999. El paquete nunca llegó."
    }

    r = post("/solicitudes/procesar", body)
    print_test("External Priority Service", body, r)


def test_priority_mock_endpoint():
    print_header("PRIORITY MOCK SERVICE")

    body = {
        "tipo_documento": "CC",
        "numero_documento_cliente": "123456789",
        "tipo_solicitud": "Problema de entrega"
    }

    r = post(
        "/mock/mensajeria-del-valle/prioridad",
        body
    )

    print_test("Mock Priority Service", body, r)


def test_external_platform_failure():
    print_header("EXTERNAL PLATFORM FAILURE")

    body = {
        "compania": "GASES DEL ORINOCO",
        "solicitud_id": generate_id("REQ"),
        "solicitud_descripcion":
            "Mi CC es 999888777. Hay fuga de gas."
    }

    r = post("/solicitudes/procesar", body)
    print_test("External Platform Failure Handling", body, r)


def test_missing_fields():
    print_header("VALIDATION ERROR")

    body = {
        "compania": "GASES DEL ORINOCO"
    }

    r = post("/solicitudes/procesar", body)
    print_test("Missing Fields", body, r)


def test_bulk_requests():
    print_header("BULK TEST (Scalability Simulation)")

    for i in range(5):

        body = {
            "compania": "GASES DEL ORINOCO",
            "solicitud_id": generate_id("REQ-BULK"),
            "solicitud_descripcion":
                f"Mi CC es 123456789. Problema técnico #{i}"
        }

        r = post("/solicitudes/procesar", body)
        print_test(f"Bulk Request {i+1}", body, r)

        time.sleep(0.5)


# ==========================================
# MAIN
# ==========================================

def run_all_tests():

    start = datetime.now()

    test_health()

    test_company_not_found()

    test_insufficient_information()

    test_direct_response()

    test_external_management()

    test_idempotency()

    test_external_priority_service()

    test_priority_mock_endpoint()

    test_external_platform_failure()

    test_missing_fields()

    test_bulk_requests()

    end = datetime.now()

    print_header("TEST EXECUTION FINISHED")
    print("Started:", start)
    print("Finished:", end)
    print("Duration:", end - start)


if __name__ == "__main__":
    run_all_tests()
