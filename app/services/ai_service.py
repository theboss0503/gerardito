from app.models.llm_loader import get_llm
from langchain_core.prompts import PromptTemplate
import spacy
import logging

logger = logging.getLogger(__name__)

# Se carga el modelo de spaCy al iniciar el servicio
try:
    nlp = spacy.load("es_core_news_sm")
except OSError:
    logger.warning("Modelo spaCy no encontrado. Descargando automáticamente...")
    spacy.cli.download("es_core_news_sm")
    nlp = spacy.load("es_core_news_sm")

llm = get_llm()

def generar_diagnostico_vocacional(habilidades: str, intereses: str) -> str:
    """
    Inyecta el perfil del estudiante en el prompt y realiza la inferencia con Llama 3.1.
    """
    template = """
    Eres Gerardito, orientador vocacional de la Universidad Gerardo Barrios (UGB).
    Evalúa el siguiente perfil del estudiante:
    - Habilidades: {habilidades}
    - Intereses: {intereses}
    
    Proporciona una tabla en formato Markdown con las 3 carreras más afines de la UGB, 
    su porcentaje de afinidad y una breve justificación.
    """
    
    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm
    
    respuesta = chain.invoke({"habilidades": habilidades, "intereses": intereses})
    return respuesta.content

def procesar_resena(texto: str) -> dict:
    """
    Pipeline Híbrido: spaCy extrae palabras clave y Llama 3.1 clasifica el sentimiento.
    """
    # 1. Extracción con spaCy (CPU)
    doc = nlp(texto)
    palabras = [token.text for token in doc if token.pos_ in ["NOUN", "ADJ"]]
    
    # 2. Análisis semántico con LLM (GPU)
    template_sentimiento = "Analiza el siguiente texto y responde ÚNICAMENTE con una de estas tres palabras (POSITIVO, NEGATIVO, NEUTRAL): {texto}"
    prompt = PromptTemplate.from_template(template_sentimiento)
    chain = prompt | llm
    
    sentimiento_bruto = chain.invoke({"texto": texto}).content.strip().upper()
    
    # Limpieza de alucinaciones
    sentimiento_final = sentimiento_bruto if sentimiento_bruto in ["POSITIVO", "NEGATIVO", "NEUTRAL"] else "NEUTRAL"
    
    return {
        "sentimiento": sentimiento_final,
        "palabras_clave": palabras
    }