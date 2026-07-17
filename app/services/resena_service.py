from app.models.llm_loader import get_llm
from langchain_core.prompts import PromptTemplate
import spacy

try:
    nlp = spacy.load("es_core_news_sm")
except OSError:
    spacy.cli.download("es_core_news_sm")
    nlp = spacy.load("es_core_news_sm")

llm = get_llm()

def evaluar_resena_hibrida(texto: str) -> dict:
    # 1. Extracción Sintáctica (CPU)
    doc = nlp(texto)
    palabras = [token.text for token in doc if token.pos_ in ["NOUN", "ADJ"]]
    
    # 2. Análisis de Sentimiento (GPU) con tu prompt exacto
    template = """
    Analiza la siguiente reseña enviada por un usuario del sistema de orientación.
    Debes clasificar la opinión.
    
    REGLA CRÍTICA DE VALIDACIÓN: Si el texto consiste en letras al azar sin sentido (ej. 'asfajfwef', 'ghjk'), 
    puros puntos o signos repetidos (ej. '.......', '???'), o palabras sueltas que no forman un comentario u opinión real, 
    debes responder ESTRICTAMENTE con la palabra: INVALIDO.
    
    Si el comentario tiene sentido humano, clasifícalo detectando ironía, sarcasmo o emojis (ej. 🤡, 💩) en: 
    POSITIVO, NEGATIVO o NEUTRAL.
    
    Responde ESTRICTAMENTE con una de estas cuatro palabras: POSITIVO, NEGATIVO, NEUTRAL o INVALIDO. Cero explicaciones.
    Reseña a evaluar: "{texto}"
    """
    
    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm
    
    sentimiento_bruto = chain.invoke({"texto": texto}).content.strip().upper()
    
    # Limpieza de alucinaciones
    estados_validos = ["POSITIVO", "NEGATIVO", "NEUTRAL", "INVALIDO"]
    sentimiento_final = sentimiento_bruto if sentimiento_bruto in estados_validos else "INVALIDO"
    
    return {
        "sentimiento": sentimiento_final,
        "palabras_clave": palabras
    }