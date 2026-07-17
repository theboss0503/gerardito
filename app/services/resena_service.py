from app.models.llm_loader import get_llm
from langchain_core.prompts import PromptTemplate
import spacy
import logging

logger = logging.getLogger(__name__)

try:
    nlp = spacy.load("es_core_news_sm")
except OSError:
    spacy.cli.download("es_core_news_sm")
    nlp = spacy.load("es_core_news_sm")

llm = get_llm()

def procesar_resena(texto: str) -> dict:
    # Extracción CPU
    doc = nlp(texto)
    palabras = [token.text for token in doc if token.pos_ in ["NOUN", "ADJ"]]
    
    # Inferencia GPU
    template = "Clasifica el sentimiento de este texto con una palabra (POSITIVO, NEGATIVO, NEUTRAL): {texto}"
    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm
    
    sentimiento_bruto = chain.invoke({"texto": texto}).content.strip().upper()
    sentimiento_final = sentimiento_bruto if sentimiento_bruto in ["POSITIVO", "NEGATIVO", "NEUTRAL"] else "NEUTRAL"
    
    return {
        "sentimiento": sentimiento_final,
        "palabras_clave": palabras
    }