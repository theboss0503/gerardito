from dotenv import load_dotenv
load_dotenv()

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.connection import init_db
from app.api.routes import router
from app.middleware.observabilidad import ObservabilidadMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="Gerardito IA API",
    description="API RESTful para motor de emparejamiento vocacional híbrido",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(ObservabilidadMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Gerardito. Visita /docs para Swagger UI."}
