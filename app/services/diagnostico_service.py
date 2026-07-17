from app.models.llm_loader import get_llm
from langchain_core.prompts import PromptTemplate
from typing import List

llm = get_llm()

CATALOGO_CARRERAS = """
### ÁREA DE SALUD Y HUMANIDADES
- Doctorado en Medicina
- Licenciatura y Técnico en Enfermería
- Licenciatura en Psicología
- Licenciatura, Profesorado o Técnico en Idioma Inglés
- Licenciatura en Comunicaciones
- Licenciatura en Ciencias Jurídicas
- Licenciatura en Relaciones y Negocios Internacionales
- Licenciatura y Profesorado en Educación Inicial y Parvularia
- Profesorado en Lenguaje y Literatura

### ÁREA DE NEGOCIOS Y MARKETING
- Licenciatura en Administración de Empresas
- Técnico en Mercadeo y Ventas
- Licenciatura en Administración de Empresas y Desarrollo Turístico
- Técnico en Marketing y Publicidad Digital
- Licenciatura en Marketing y Negocios Digitales

### ÁREA DE TECNOLOGÍA E INGENIERÍA
- Ingeniería o Técnico en Sistemas y Redes Informáticas
- Licenciatura en Computación
- Ingeniería Industrial
- Ingeniería o Técnico Electricista
- Ingeniería o Técnico en Hardware
- Ingeniería en Desarrollo de Software
- Ingeniería en Inteligencia de Negocios

### ÁREA DE DISEÑO Y CIENCIAS EXACTAS
- Licenciatura o Técnico en Contaduría Pública
- Ingeniería Civil
- Técnico en Ingeniería Civil y Construcción
- Arquitectura
- Licenciatura o Profesorado en Matemáticas
- Técnico en Diseño Gráfico
"""

# AQUÍ ESTÁ EL CAMBIO CLAVE: El nombre correcto de la función
def generar_matriz(habilidades: List[str], intereses: List[str]) -> str:
    template = """
    Eres Gerardito, Orientador Vocacional de la UGB. Perfil del usuario:
    - Habilidades: {habilidades_str}
    - Intereses: {intereses_str}
    
    CATÁLOGO UGB:
    {catalogo}
    
    EJEMPLO DE FORMATO DE TABLA (SÍGUELO ESTRICTAMENTE):
    | Carrera Sugerida | % de Afinidad | Por qué encaja |
    |---|---|---|
    | Doctorado en Medicina | 85% | Porque... |
    
    INSTRUCCIONES: Saluda celebrando su perfil. Genera una tabla Markdown ESTRICTA con 3 carreras del catálogo. Cierra invitándolo a utilizar los botones para decidir. NO HAGAS PREGUNTAS AL FINAL.
    """
    
    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm
    
    habilidades_str = ", ".join(habilidades)
    intereses_str = ", ".join(intereses)
    
    return chain.invoke({
        "habilidades_str": habilidades_str, 
        "intereses_str": intereses_str, 
        "catalogo": CATALOGO_CARRERAS
    }).content

def explorar_carrera(carrera: str) -> str:
    template = """
    Eres Gerardito, Orientador de la UGB. El usuario seleccionó explorar: {carrera}.
    REGLAS: Explica ventajas o campo laboral. ¡ÚLTIMA INTERVENCIÓN! PROHIBIDO hacer preguntas de seguimiento. Tu mensaje DEBE FINALIZAR EXACTAMENTE pidiendo la reseña.
    """
    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm
    return chain.invoke({"carrera": carrera}).content