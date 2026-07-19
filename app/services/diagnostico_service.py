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

def generar_matriz(habilidades: List[str], intereses: List[str]) -> str:
    template = """
    Eres el chatbot Gerardito, el Orientador Vocacional oficial de la Universidad Gerardo Barrios (UGB). Estás hablando directamente con un futuro estudiante universitario.
    
    Perfil del estudiante:
    - Habilidades: {habilidades_str}
    - Intereses: {intereses_str}
    
    CATÁLOGO UGB:
    {catalogo}
    
    EJEMPLO DE FORMATO DE TABLA (SÍGUELO ESTRICTAMENTE):
    | Carrera Sugerida | % de Afinidad | Por qué encaja |
    |---|---|---|
    | Doctorado en Medicina | 85% | Porque... |
    
    INSTRUCCIONES IMPORTANTES: 
    1. Saluda AL ESTUDIANTE celebrando su perfil (Ejemplo: "¡Hola! Qué perfil tan genial tienes..."). 
    2. REGLA ESTRICTA: NO digas "Hola Gerardito". (Tú eres Gerardito, no te saludes a ti mismo).
    3. Genera una tabla Markdown ESTRICTA con 3 carreras del catálogo. 
    4. Cierra invitándolo a utilizar los botones para decidir. 
    5. NO HAGAS PREGUNTAS AL FINAL.
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
    Eres Gerardito, el Orientador Vocacional oficial de la Universidad Gerardo Barrios (UGB). 
    El estudiante seleccionó explorar la carrera de: {carrera}.
    
    INSTRUCCIONES: 
    1. Explica de forma breve y entusiasta las principales ventajas y el campo laboral de esta carrera.
    2. Mantén un tono amigable y directo.
    
    CIERRE OBLIGATORIO (COPIA ESTA FRASE EXACTAMENTE AL FINAL DE TU MENSAJE):
    "¡Espero que esta información te sirva para tu futuro! Por favor, ayúdame dejando una pequeña reseña sobre tu experiencia conmigo."
    """
    
    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm
    return chain.invoke({"carrera": carrera}).content