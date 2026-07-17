from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

app = FastAPI(
    title="Gerardito IA API",
    description="API RESTful para motor de emparejamiento vocacional híbrido",
    version="1.0.0"
)

# Configuración estricta de CORS para asegurar que solo la UI permitida la consuma
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción reemplazar con la URL de la app en React
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Registrar las rutas
app.include_router(router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Gerardito. Visita /docs para Swagger UI."}