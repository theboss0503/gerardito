from typing import Literal, List
from pydantic import BaseModel, Field, field_validator

# --- ESQUEMA PRINCIPAL ---
class PerfilEstudiante(BaseModel):
    habilidades: List[str] = Field(default_factory=list, description="Lista de habilidades validadas")
    intereses: List[str] = Field(default_factory=list, description="Lista de intereses validados")

# --- ESQUEMAS PARA VALIDACIÓN ---
class ValidacionInput(BaseModel):
    texto: str = Field(..., description="El texto ingresado por el usuario para validar")
    tipo: Literal["habilidad", "interes"] = Field(..., description="Especifica qué se está evaluando")

class ValidacionResponse(BaseModel):
    es_valido: bool = Field(..., description="Indica si el texto pasó la validación")
    mensaje_ui: str = Field(..., description="Retroalimentación para la interfaz de usuario")
    clasificacion: str | None = Field(default=None, description="La habilidad o interés extraído (opcional)")

# --- ESQUEMAS PARA DIAGNÓSTICO ---
class DiagnosticoInput(BaseModel): 
    habilidades: list[str] = Field(
        ..., 
        min_length=1, 
        description="Lista de habilidades del usuario (mínimo 1)"
    )
    intereses: list[str] = Field(
        ..., 
        min_length=1, 
        description="Lista de intereses del usuario (mínimo 1)"
    )

class DiagnosticoResponse(BaseModel):
    
    resultado_markdown: str

# --- ESQUEMAS PARA EXPLORACIÓN ---
class ExploracionInput(BaseModel):
    carrera: str = Field(..., description="Nombre de la carrera que el usuario desea explorar")

class ExploracionResponse(BaseModel):
   
    respuesta_chat: str

# --- ESQUEMAS PARA RESEÑAS ---
class ResenaInput(BaseModel):
    # Quitamos strip_whitespace=True de aquí
    comentario: str = Field(..., min_length=1, description="El feedback del usuario")

    @field_validator("comentario")
    @classmethod
    def validar_no_vacio(cls, v: str) -> str:
        # Hacemos la limpieza de espacios en blanco manualmente
        v_limpio = v.strip()
        if not v_limpio:
            raise ValueError("El comentario no puede estar vacío o contener solo espacios.")
        return v_limpio

class ResenaResponse(BaseModel):
    mensaje: str = Field(..., description="Confirmación de que la reseña fue guardada")
    sentimiento: str = Field(..., description="Sentimiento detectado por el LLM")
    palabras_clave: List[str] = Field(..., description="Sustantivos y adjetivos extraídos por spaCy")