from fastapi import APIRouter, HTTPException
from app.schemas.vocacional import (
    ValidacionInput, ValidacionResponse, 
    PerfilEstudiante, DiagnosticoResponse, 
    ExploracionInput, ExploracionResponse,
    ResenaInput, ResenaResponse
)
from app.services.validacion_service import validar_texto_individual
from app.services.diagnostico_service import generar_matriz, explorar_carrera
from app.services.resena_service import evaluar_resena_hibrida
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/health", tags=["Sistema"])
def health_check():
    """Verifica que la API de Gerardito esté en línea."""
    return {"status": "ok", "servicio": "Gerardito API"}

@router.get("/metadata", tags=["Sistema"])
def get_metadata():
    """Devuelve la información de la versión de la API."""
    return {
        "version": "1.0",
        "proposito": "Sistema de Orientación Vocacional Inteligente UGB",
        "tecnologias": ["FastAPI", "Ollama", "LangChain", "spaCy"],
        "modelo_ia_principal": "llama3.1:8b"
    }

@router.post("/validar-texto", response_model=ValidacionResponse, tags=["Fase 1: Recolección"])
def validar_texto(input_data: ValidacionInput):
    """Evalúa si el texto ingresado tiene sentido como habilidad o interés."""
    try:
        # Ahora pasamos input_data.tipo en lugar de contexto
        resultado = validar_texto_individual(input_data.texto, input_data.tipo)
        return ValidacionResponse(**resultado)
    except Exception as e:
        logger.error(f"Error en validación: {str(e)}")
        raise HTTPException(status_code=500, detail="Error evaluando el texto.")

@router.post("/diagnostico", response_model=DiagnosticoResponse, tags=["Fase 2: Afinidad"])
def diagnostico(perfil: PerfilEstudiante):
    """Recibe las listas validadas y cruza la información con el catálogo UGB."""
    try:
        resultado = generar_matriz(perfil.habilidades, perfil.intereses)
        return DiagnosticoResponse(resultado_markdown=resultado)
    except Exception as e:
        logger.error(f"Error en diagnóstico: {str(e)}")
        raise HTTPException(status_code=500, detail="Error generando la matriz.")

@router.post("/explorar", response_model=ExploracionResponse, tags=["Fase 3: Exploración"])
def explorar(input_data: ExploracionInput):
    """Genera la respuesta final detallando la carrera elegida."""
    try:
        resultado = explorar_carrera(input_data.carrera)
        return ExploracionResponse(respuesta_chat=resultado)
    except Exception as e:
        logger.error(f"Error en exploración: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al explorar la carrera.")

@router.post("/resena", response_model=ResenaResponse, tags=["Fase 4: Feedback"])
def analizar_resena(resena: ResenaInput):
    """Procesa el feedback utilizando el pipeline NLP híbrido."""
    try:
        resultado = evaluar_resena_hibrida(resena.texto)
        return ResenaResponse(**resultado)
    except Exception as e:
        logger.error(f"Error en NLP: {str(e)}")
        raise HTTPException(status_code=500, detail="Error procesando la reseña.")