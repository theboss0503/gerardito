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
    Analiza el sentimiento de la siguiente reseña sobre Gerardito, un chatbot de orientación vocacional.
    
    REGLAS:
    1. TOLERANCIA ORTOGRÁFICA: Entiende el contexto aunque falten tildes o haya mala ortografía (ej. "no me gusto" significa "no me gustó").
    2. INVALIDO: Si es texto sin sentido ('asdfg', '...'), responde INVALIDO.
    3. CLASIFICACIÓN: Clasifica estrictamente en POSITIVO, NEGATIVO o NEUTRAL.
    
    EJEMPLOS DE CLASIFICACIÓN:
    Reseña: "me encanto muy bueno" -> POSITIVO
    Reseña: "no me gusto la respuesta" -> NEGATIVO
    Reseña: "esta horrible el bot 🤡" -> NEGATIVO
    Reseña: "esta bien" -> NEUTRAL
    Reseña: "ok" -> NEUTRAL
    Reseña: "asdfg" -> INVALIDO
    
    Responde ESTRICTAMENTE con una de estas cuatro palabras: POSITIVO, NEGATIVO, NEUTRAL o INVALIDO. Cero explicaciones.
    Reseña a evaluar: "{texto}"
    """
    
    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm
    
    sentimiento_bruto = chain.invoke({"texto": texto}).content.strip().upper()
    
    
    estados_validos = ["POSITIVO", "NEGATIVO", "NEUTRAL"]
    sentimiento_final = "INVALIDO" # Asumimos inválido por defecto
    
    for estado in estados_validos:
        if estado in sentimiento_bruto:
            sentimiento_final = estado
            break
            
    return {
        "sentimiento": sentimiento_final,
        "palabras_clave": palabras
    }
    
   