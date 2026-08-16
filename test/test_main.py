import uuid
import pytest
import httpx
from app.main import app
from app.db.connection import init_db

SESSION_ID = str(uuid.uuid4())
HEADERS = {"X-Session-Id": SESSION_ID}


@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    await init_db()


@pytest.fixture
async def client():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


async def test_health_check(client):
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "servicio": "Gerardito API"}

async def test_get_metadata(client):
    response = await client.get("/api/v1/metadata")
    assert response.status_code == 200
    data = response.json()
    assert data["version"] == "1.0"
    assert data["modelo_ia_principal"] == "gemma4:31b"

async def test_validar_texto_habilidad(client):
    payload = {
        "texto": "Tengo mucha facilidad para resolver problemas matemáticos.",
        "tipo": "habilidad"
    }
    response = await client.post("/api/v1/validar-texto", json=payload, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "es_valido" in data
    assert "mensaje_ui" in data
    assert "clasificacion" in data

async def test_diagnostico_matriz(client):
    payload = {
        "habilidades": ["programación en python", "lógica matemática"],
        "intereses": ["desarrollo de software", "inteligencia artificial"]
    }
    response = await client.post("/api/v1/diagnostico", json=payload, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "resultado_markdown" in data
    assert len(data["resultado_markdown"]) > 0

async def test_explorar_carrera(client):
    payload = {"carrera": "Ingeniería en Desarrollo de Software"}
    response = await client.post("/api/v1/explorar", json=payload, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "respuesta_chat" in data

async def test_analizar_resena(client):
    payload = {"comentario": "El sistema es excelente y muy rápido, me ayudó mucho."}
    response = await client.post("/api/v1/resena", json=payload, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["mensaje"] == "¡Gracias por tu reseña! Ha sido procesada."
    assert "sentimiento" in data
    assert type(data["palabras_clave"]) == list

async def test_pydantic_protege_resena_vacia(client):
    payload = {"comentario": "      "}
    response = await client.post("/api/v1/resena", json=payload, headers=HEADERS)
    assert response.status_code == 422

async def test_diagnostico_matriz_listas_vacias(client):
    payload = {"habilidades": [], "intereses": []}
    response = await client.post("/api/v1/diagnostico", json=payload, headers=HEADERS)
    assert response.status_code == 422

async def test_validar_texto_basura(client):
    payload = {"texto": "asdfghjkl zxcvbnm 12345", "tipo": "habilidad"}
    response = await client.post("/api/v1/validar-texto", json=payload, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["es_valido"] == False

async def test_analizar_resena_negativa(client):
    payload = {"comentario": "El sistema es muy confuso, me dio resultados que no tienen nada que ver conmigo."}
    response = await client.post("/api/v1/resena", json=payload, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["sentimiento"].lower() in ["negativo", "malo"]
    assert len(data["palabras_clave"]) > 0

async def test_explorar_carrera_sin_payload(client):
    response = await client.post("/api/v1/explorar")
    assert response.status_code == 422

async def test_get_metrics(client):
    response = await client.get("/api/v1/metrics")
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
