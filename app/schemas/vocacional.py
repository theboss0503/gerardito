from typing import Literal, List
from pydantic import BaseModel, Field

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
    mensaje: str = Field(..., description="Retroalimentación del LLM sobre la validación")
    clasificacion: str = Field(..., description="La habilidad o interés extraído y formateado")

# --- ESQUEMAS PARA DIAGNÓSTICO ---
class DiagnosticoInput(BaseModel):
    habilidades: List[str] = Field(..., description="Lista de habilidades validadas del usuario")
    intereses: List[str] = Field(..., description="Lista de intereses validados del usuario")

class DiagnosticoResponse(BaseModel):
    resultado: str = Field(..., description="La matriz de carreras sugeridas en formato Markdown")

# --- ESQUEMAS PARA EXPLORACIÓN ---
class ExploracionInput(BaseModel):
    carrera: str = Field(..., description="Nombre de la carrera que el usuario desea explorar")

class ExploracionResponse(BaseModel):
    resultado: str = Field(..., description="Explicación de la carrera seleccionada")

# --- ESQUEMAS PARA RESEÑAS ---
class ResenaInput(BaseModel):
    comentario: str = Field(..., description="Reseña final o retroalimentación del usuario")

class ResenaResponse(BaseModel):
    mensaje: str = Field(..., description="Confirmación de que la reseña fue guardada")