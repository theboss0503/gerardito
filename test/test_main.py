from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

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
    assert data["modelo_ia_principal"] == "llama3.1:8b"

def test_validar_texto_habilidad():
    """Prueba la Fase 1: Validar un texto con la IA (Requiere IA Real)"""
    payload = {
        "texto": "Tengo mucha facilidad para resolver problemas matemáticos.",
        "tipo": "habilidad"
    }
    response = client.post("/api/v1/validar-texto", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    # Verificamos la estructura exacta de ValidacionResponse
    assert "es_valido" in data
    assert "mensaje_ui" in data
    assert "clasificacion" in data

def test_diagnostico_matriz():
    """Prueba la Fase 2: Generar matriz diagnóstica (Requiere IA Real)"""
    payload = {
        "habilidades": ["programación en python", "lógica matemática"],
        "intereses": ["desarrollo de software", "inteligencia artificial"]
    }
    response = client.post("/api/v1/diagnostico", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    # Verificamos la estructura exacta de DiagnosticoResponse
    assert "resultado_markdown" in data
    assert len(data["resultado_markdown"]) > 0

def test_explorar_carrera():
    """Prueba la Fase 3: Exploración de carrera (Requiere IA Real)"""
    payload = {
        "carrera": "Ingeniería en Desarrollo de Software"
    }
    response = client.post("/api/v1/explorar", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    # Verificamos la estructura exacta de ExploracionResponse
    assert "respuesta_chat" in data

def test_analizar_resena():
    """Prueba la Fase 4: Analizar feedback del usuario (Requiere IA Real y spaCy)"""
    payload = {
        "comentario": "El sistema es excelente y muy rápido, me ayudó mucho."
    }
    response = client.post("/api/v1/resena", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    
    # Verificamos la estructura exacta de ResenaResponse
    assert data["mensaje"] == "¡Gracias por tu reseña! Ha sido procesada."
    assert "sentimiento" in data
    assert type(data["palabras_clave"]) == list

def test_pydantic_protege_resena_vacia():
    """Valida que los esquemas rechacen textos vacíos (No requiere IA, lo detiene FastAPI)"""
    # Tu esquema usa strip_whitespace=True y un validador personalizado
    payload = {
        "comentario": "       "
    }
    response = client.post("/api/v1/resena", json=payload)
    
    # Debe lanzar 422 Unprocessable Entity antes de llegar al modelo
    assert response.status_code == 422