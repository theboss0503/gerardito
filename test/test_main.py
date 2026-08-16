import uuid
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

SESSION_ID = str(uuid.uuid4())
HEADERS = {"X-Session-Id": SESSION_ID}


def test_health_check():
    """Prueba el endpoint de estado del sistema"""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "servicio": "Gerardito API"}

def test_get_metadata():
    """Prueba el endpoint de metadatos del sistema"""
    response = client.get("/api/v1/metadata")
    assert response.status_code == 200
    data = response.json()
    assert data["version"] == "1.0"
    assert data["modelo_ia_principal"] == "gemma4:31b"

def test_validar_texto_habilidad():
    """Prueba la Fase 1: Validar un texto con la IA (Requiere IA Real)"""
    payload = {
        "texto": "Tengo mucha facilidad para resolver problemas matemáticos.",
        "tipo": "habilidad"
    }
    response = client.post("/api/v1/validar-texto", json=payload, headers=HEADERS)
    
    assert response.status_code == 200
    data = response.json()
    assert "es_valido" in data
    assert "mensaje_ui" in data
    assert "clasificacion" in data

def test_diagnostico_matriz():
    """Prueba la Fase 2: Generar matriz diagnóstica (Requiere IA Real)"""
    payload = {
        "habilidades": ["programación en python", "lógica matemática"],
        "intereses": ["desarrollo de software", "inteligencia artificial"]
    }
    response = client.post("/api/v1/diagnostico", json=payload, headers=HEADERS)
    
    assert response.status_code == 200
    data = response.json()
    assert "resultado_markdown" in data
    assert len(data["resultado_markdown"]) > 0

def test_explorar_carrera():
    """Prueba la Fase 3: Exploración de carrera (Requiere IA Real)"""
    payload = {
        "carrera": "Ingeniería en Desarrollo de Software"
    }
    response = client.post("/api/v1/explorar", json=payload, headers=HEADERS)
    
    assert response.status_code == 200
    data = response.json()
    assert "respuesta_chat" in data

def test_analizar_resena():
    """Prueba la Fase 4: Analizar feedback del usuario (Requiere IA Real y spaCy)"""
    payload = {
        "comentario": "El sistema es excelente y muy rápido, me ayudó mucho."
    }
    response = client.post("/api/v1/resena", json=payload, headers=HEADERS)
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["mensaje"] == "¡Gracias por tu reseña! Ha sido procesada."
    assert "sentimiento" in data
    assert type(data["palabras_clave"]) == list

def test_pydantic_protege_resena_vacia():
    """Valida que los esquemas rechacen textos vacíos"""
    payload = {
        "comentario": "      "
    }
    response = client.post("/api/v1/resena", json=payload, headers=HEADERS)
    assert response.status_code == 422

def test_diagnostico_matriz_listas_vacias():
    """Valida que el sistema rechace un diagnóstico sin habilidades o intereses"""
    payload = {
        "habilidades": [],
        "intereses": []
    }
    response = client.post("/api/v1/diagnostico", json=payload, headers=HEADERS)
    assert response.status_code == 422

def test_validar_texto_basura():
    """Prueba que el LLM rechace texto que no tiene sentido"""
    payload = {
        "texto": "asdfghjkl zxcvbnm 12345",
        "tipo": "habilidad"
    }
    response = client.post("/api/v1/validar-texto", json=payload, headers=HEADERS)
    
    assert response.status_code == 200
    data = response.json()
    assert data["es_valido"] == False

def test_analizar_resena_negativa():
    """Prueba la Fase 4 con un comentario negativo para validar el NLP"""
    payload = {
        "comentario": "El sistema es muy confuso, me dio resultados que no tienen nada que ver conmigo."
    }
    response = client.post("/api/v1/resena", json=payload, headers=HEADERS)
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["sentimiento"].lower() in ["negativo", "malo"]
    assert len(data["palabras_clave"]) > 0

def test_explorar_carrera_sin_payload():
    """Verifica el manejo de error cuando falta el body de la petición"""
    response = client.post("/api/v1/explorar")
    assert response.status_code == 422

def test_get_metrics():
    """Prueba el endpoint de métricas de observabilidad"""
    response = client.get("/api/v1/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "resumen" in data
    assert "por_endpoint" in data
    assert "llm" in data
    assert "ultimas_metricas" in data
    assert isinstance(data["resumen"]["total_requests"], int)
    assert isinstance(data["resumen"]["tiempo_promedio_ms"], (int, float))
    assert isinstance(data["por_endpoint"], dict)
    assert isinstance(data["llm"], dict)
    assert isinstance(data["ultimas_metricas"], list)
