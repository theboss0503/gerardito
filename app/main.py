from dotenv import load_dotenv
load_dotenv()

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from app.db.connection import init_db
from app.db.models import Sesion, Diagnostico, Exploracion, Resena, Metrica  # noqa: F401
from app.api.routes import router
from app.middleware.observabilidad import ObservabilidadMiddleware
from app.limiter import limiter

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

ALLOWED_ORIGINS = (
    ["https://gerarditougb.qd.je", "http://localhost:5173", "http://127.0.0.1:5173"]
    if ENVIRONMENT == "production"
    else ["*"]
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="Gerardito IA API",
    description="API RESTful para motor de emparejamiento vocacional hibrido",
    version="1.0.0",
    lifespan=lifespan,
)

app.state.limiter = limiter


def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": f"Demasiadas peticiones. Intenta mas tarde."},
    )


app.add_exception_handler(RateLimitExceeded, rate_limit_handler)
app.add_middleware(ObservabilidadMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Gerardito. Visita /docs para Swagger UI."}
