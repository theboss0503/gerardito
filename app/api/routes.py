from fastapi import APIRouter, HTTPException, Header
from sqlalchemy import select
from app.schemas.vocacional import (
    ValidacionInput, ValidacionResponse,
    PerfilEstudiante, DiagnosticoResponse,
    ExploracionInput, ExploracionResponse,
    ResenaInput, ResenaResponse
)
from app.services.validacion_service import validar_texto_individual
from app.services.diagnostico_service import generar_matriz, explorar_carrera
from app.services.resena_service import evaluar_resena_hibrida
from app.db.connection import async_session
from app.db.models import Sesion, Diagnostico, Exploracion, Resena, Metrica
import time
import uuid
import os
import logging
from ollama import Client

router = APIRouter()
logger = logging.getLogger(__name__)

OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
ollama_client = Client(
    host=os.getenv("OLLAMA_HOST", "https://ollama.com"),
    headers={"Authorization": f"Bearer {OLLAMA_API_KEY}"} if OLLAMA_API_KEY else {},
)


async def guardar_metrica(endpoint: str, method: str, status_code: int, elapsed_ms: float, llm_ms: float | None = None):
    try:
        async with async_session() as db:
            db.add(Metrica(
                endpoint=endpoint,
                method=method,
                status_code=status_code,
                tiempo_total_ms=round(elapsed_ms, 2),
                tiempo_llm_ms=round(llm_ms, 2) if llm_ms else None,
            ))
            await db.commit()
    except Exception as e:
        logger.debug(f"Metrica no guardada: {e}")


@router.get("/health", tags=["Sistema"])
def health_check():
    return {"status": "ok", "servicio": "Gerardito API"}


@router.get("/metadata", tags=["Sistema"])
def get_metadata():
    return {
        "version": "1.0",
        "proposito": "Sistema de Orientación Vocacional Inteligente UGB",
        "tecnologias": ["FastAPI", "Ollama Cloud (Gemma 4)", "LangChain", "spaCy", "PostgreSQL"],
        "modelo_ia_principal": os.getenv("MODEL_NAME", "gemma4:31b")
    }


@router.get("/prueba-llm", tags=["Sistema"])
def prueba_llm():
    try:
        response = ollama_client.chat(
            model=os.getenv("MODEL_NAME", "gemma4:31b"),
            messages=[{"role": "user", "content": "Explica brevemente qué es la orientación vocacional."}]
        )
        return {"respuesta": response.message.content}
    except Exception as e:
        logger.error(f"Error en prueba LLM: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de conexión con Ollama: {str(e)}")


@router.post("/validar-texto", response_model=ValidacionResponse, tags=["Fase 1: Recolección"])
async def validar_texto(
    input_data: ValidacionInput,
    x_session_id: str | None = Header(None, description="ID de sesión del usuario"),
):
    session_id = x_session_id or str(uuid.uuid4())
    start = time.perf_counter()
    try:
        llm_start = time.perf_counter()
        resultado = await validar_texto_individual(input_data.texto, input_data.tipo)
        llm_ms = (time.perf_counter() - llm_start) * 1000
        elapsed = (time.perf_counter() - start) * 1000
        await guardar_metrica("/validar-texto", "POST", 200, elapsed, llm_ms)
        return ValidacionResponse(**resultado)
    except Exception as e:
        elapsed = (time.perf_counter() - start) * 1000
        await guardar_metrica("/validar-texto", "POST", 500, elapsed)
        logger.error(f"Error en validación: {str(e)}")
        raise HTTPException(status_code=500, detail="Error evaluando el texto.")


@router.post("/diagnostico", response_model=DiagnosticoResponse, tags=["Fase 2: Afinidad"])
async def diagnostico(
    perfil: PerfilEstudiante,
    x_session_id: str | None = Header(None, description="ID de sesión del usuario"),
):
    session_id = x_session_id or str(uuid.uuid4())
    start = time.perf_counter()
    try:
        llm_start = time.perf_counter()
        resultado = await generar_matriz(perfil.habilidades, perfil.intereses)
        llm_ms = (time.perf_counter() - llm_start) * 1000

        async with async_session() as db:
            existing = await db.get(Sesion, session_id)
            if not existing:
                sesion = Sesion(
                    id=session_id,
                    habilidades=perfil.habilidades,
                    habilidad_personalizada=perfil.habilidades[-1] if len(perfil.habilidades) > 0 else None,
                    intereses=perfil.intereses,
                    interes_personalizado=perfil.intereses[-1] if len(perfil.intereses) > 0 else None,
                )
                db.add(sesion)
                await db.flush()

            carreras_extraidas = []
            for linea in resultado.split("\n"):
                l = linea.strip()
                if l.startswith("|") and "Carrera Sugerida" not in l and "---" not in l:
                    partes = l.split("|")
                    if len(partes) >= 2:
                        carrera = partes[1].replace("*", "").strip()
                        if carrera:
                            carreras_extraidas.append(carrera)

            existing_diag = await db.execute(
                select(Diagnostico).where(Diagnostico.sesion_id == session_id)
            )
            if not existing_diag.scalar_one_or_none():
                diagnostico = Diagnostico(
                    sesion_id=session_id,
                    resultado_markdown=resultado,
                    carreras_sugeridas=carreras_extraidas[:3],
                )
                db.add(diagnostico)
            await db.commit()

        elapsed = (time.perf_counter() - start) * 1000
        await guardar_metrica("/diagnostico", "POST", 200, elapsed, llm_ms)
        return DiagnosticoResponse(resultado_markdown=resultado)
    except HTTPException:
        raise
    except Exception as e:
        elapsed = (time.perf_counter() - start) * 1000
        await guardar_metrica("/diagnostico", "POST", 500, elapsed)
        logger.error(f"Error en diagnóstico: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generando la matriz.")


@router.post("/explorar", response_model=ExploracionResponse, tags=["Fase 3: Exploración"])
async def explorar(
    input_data: ExploracionInput,
    x_session_id: str | None = Header(None, description="ID de sesión del usuario"),
):
    session_id = x_session_id or str(uuid.uuid4())
    start = time.perf_counter()
    try:
        llm_start = time.perf_counter()
        resultado = await explorar_carrera(input_data.carrera)
        llm_ms = (time.perf_counter() - llm_start) * 1000

        async with async_session() as db:
            result = await db.execute(
                select(Diagnostico).where(Diagnostico.sesion_id == session_id)
            )
            diag = result.scalars().first()
            if not diag:
                raise HTTPException(status_code=404, detail="No hay diagnóstico para esta sesión.")

            exploracion = Exploracion(
                sesion_id=session_id,
                diagnostico_id=diag.id,
                carrera=input_data.carrera,
                respuesta_llm=resultado,
            )
            db.add(exploracion)
            await db.commit()

        elapsed = (time.perf_counter() - start) * 1000
        await guardar_metrica("/explorar", "POST", 200, elapsed, llm_ms)
        return ExploracionResponse(respuesta_chat=resultado)
    except HTTPException:
        raise
    except Exception as e:
        elapsed = (time.perf_counter() - start) * 1000
        await guardar_metrica("/explorar", "POST", 500, elapsed)
        logger.error(f"Error en exploración: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al explorar la carrera.")


@router.post("/resena", response_model=ResenaResponse, tags=["Fase 4: Feedback"])
async def analizar_resena(
    resena: ResenaInput,
    x_session_id: str | None = Header(None, description="ID de sesión del usuario"),
):
    session_id = x_session_id or str(uuid.uuid4())
    start = time.perf_counter()
    try:
        llm_start = time.perf_counter()
        resultado = await evaluar_resena_hibrida(resena.comentario)
        llm_ms = (time.perf_counter() - llm_start) * 1000

        if resultado["sentimiento"] == "INVALIDO":
            elapsed = (time.perf_counter() - start) * 1000
            await guardar_metrica("/resena", "POST", 400, elapsed, llm_ms)
            raise HTTPException(
                status_code=400,
                detail="El comentario no parece válido o no tiene sentido. Intenta de nuevo."
            )

        async with async_session() as db:
            resena_db = Resena(
                sesion_id=session_id,
                comentario=resena.comentario,
                sentimiento=resultado["sentimiento"],
                palabras_clave=resultado["palabras_clave"],
            )
            db.add(resena_db)
            await db.commit()

        elapsed = (time.perf_counter() - start) * 1000
        await guardar_metrica("/resena", "POST", 200, elapsed, llm_ms)
        resultado["mensaje"] = "¡Gracias por tu reseña! Ha sido procesada."
        return ResenaResponse(**resultado)

    except HTTPException:
        raise
    except Exception as e:
        elapsed = (time.perf_counter() - start) * 1000
        await guardar_metrica("/resena", "POST", 500, elapsed)
        logger.error(f"Error en NLP: {str(e)}")
        raise HTTPException(status_code=500, detail="Error procesando la reseña.")


@router.get("/metrics", tags=["Observabilidad"])
async def get_metrics():
    """Devuelve métricas de rendimiento de la API."""
    try:
        async with async_session() as db:
            result = await db.execute(select(Metrica))
            metricas = result.scalars().all()

        if not metricas:
            return {
                "resumen": {"total_requests": 0, "tiempo_promedio_ms": 0, "tiempo_max_ms": 0, "tiempo_min_ms": 0, "tasa_error_pct": 0},
                "por_endpoint": {},
                "llm": {"promedio_ms": 0, "max_ms": 0, "min_ms": 0, "total_llm_ms": 0},
                "ultimas_metricas": [],
            }

        total = len(metricas)
        tiempos = [m.tiempo_total_ms for m in metricas]
        errores = [m for m in metricas if m.status_code >= 400]
        llm_tiempos = [m.tiempo_llm_ms for m in metricas if m.tiempo_llm_ms is not None]

        promedio_total = sum(tiempos) / total
        max_total = max(tiempos)
        min_total = min(tiempos)
        tasa_error = (len(errores) / total) * 100

        por_endpoint = {}
        for m in metricas:
            ep = m.endpoint
            if ep not in por_endpoint:
                por_endpoint[ep] = {"calls": 0, "total_ms": 0, "errors": 0, "max_ms": 0}
            por_endpoint[ep]["calls"] += 1
            por_endpoint[ep]["total_ms"] += m.tiempo_total_ms
            por_endpoint[ep]["max_ms"] = max(por_endpoint[ep]["max_ms"], m.tiempo_total_ms)
            if m.status_code >= 400:
                por_endpoint[ep]["errors"] += 1

        for ep in por_endpoint:
            calls = por_endpoint[ep]["calls"]
            por_endpoint[ep]["avg_ms"] = round(por_endpoint[ep]["total_ms"] / calls, 2)
            del por_endpoint[ep]["total_ms"]

        llm_stats = {"promedio_ms": 0, "max_ms": 0, "min_ms": 0, "total_llm_ms": 0}
        if llm_tiempos:
            llm_stats = {
                "promedio_ms": round(sum(llm_tiempos) / len(llm_tiempos), 2),
                "max_ms": round(max(llm_tiempos), 2),
                "min_ms": round(min(llm_tiempos), 2),
                "total_llm_ms": round(sum(llm_tiempos), 2),
            }

        ultimas = sorted(metricas, key=lambda m: m.created_at, reverse=True)[:100]
        ultimas_metricas = [
            {
                "endpoint": m.endpoint,
                "method": m.method,
                "status_code": m.status_code,
                "tiempo_total_ms": m.tiempo_total_ms,
                "tiempo_llm_ms": m.tiempo_llm_ms,
                "created_at": m.created_at.isoformat() if m.created_at else None,
            }
            for m in ultimas
        ]

        return {
            "resumen": {
                "total_requests": total,
                "tiempo_promedio_ms": round(promedio_total, 2),
                "tiempo_max_ms": round(max_total, 2),
                "tiempo_min_ms": round(min_total, 2),
                "tasa_error_pct": round(tasa_error, 2),
            },
            "por_endpoint": por_endpoint,
            "llm": llm_stats,
            "ultimas_metricas": ultimas_metricas,
        }
    except Exception as e:
        logger.error(f"Error en métricas: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al obtener métricas.")
