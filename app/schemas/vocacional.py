from pydantic import BaseModel, Field
from typing import List, Optional, Literal

# --- Contratos de Entrada ---
class ValidacionInput(BaseModel):
    texto: str = Field(..., description="El texto a evaluar")
    tipo: Literal["habilidad", "interes"] = Field(..., description="Especifica qué se está evaluando")

class PerfilEstudiante(BaseModel):
    habilidades: List[str] = Field(...)
    intereses: List[str] = Field(...)

class ExploracionInput(BaseModel):
    carrera: str = Field(...)

class ResenaInput(BaseModel):
    texto: str = Field(...)


class ValidacionResponse(BaseModel):
    es_valido: bool
    mensaje_ui: str

class DiagnosticoResponse(BaseModel):
    resultado_markdown: str

class ExploracionResponse(BaseModel):
    respuesta_chat: str

class ResenaResponse(BaseModel):
    sentimiento: str
    palabras_clave: List[str]