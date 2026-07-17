from app.models.llm_loader import get_llm
from langchain_core.prompts import PromptTemplate

llm = get_llm()

def validar_texto_individual(texto: str, contexto: str) -> dict:
    """
    Utiliza el prompt restrictivo para evaluar un solo elemento (habilidad o interés).
    """
    template = """
    Eres el filtro de seguridad de un test de orientación vocacional. 
    Tu tarea es evaluar si el texto ingresado tiene sentido como una '{contexto}' para elegir una carrera universitaria.
    
    REGLA 1 (Tolerancia ortográfica): Perdona errores de tipeo o mala ortografía (ej. 'baialar', 'ezcrivir', 'aser cuentas' SON VÁLIDOS).
    REGLA 2 (Rechazo Estricto): Debes rechazar y responder 'NO' a:
    - Insultos, groserías, palabras obscenas o lenguaje inapropiado (Bloqueo inmediato).
    - Necesidades biológicas, estados de ánimo o quejas (ej. 'quiero comer', 'tengo hambre', 'me aburro', 'tengo sueño').
    - Peticiones al chatbot, instrucciones, o charla general (ej. 'dame una receta', 'cuéntame un chiste', 'hola', 'qué haces').
    - Teclas al azar o palabras absurdas (ej. 'asdfg', 'jajaja').
    
    Responde ESTRICTAMENTE con 'SI' o 'NO'. Cero explicaciones.
    Texto a evaluar: "{texto}"
    """
    
    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm
    
    # Inferencia
    respuesta_llm = chain.invoke({"contexto": contexto, "texto": texto}).content.strip().upper()
    
    # Procesamiento para React
    es_valido = "SI" in respuesta_llm
    mensaje = "Válido" if es_valido else f"El texto ingresado no es válido para una {contexto}. Por favor, ingresa datos reales."
    
    return {"es_valido": es_valido, "mensaje_ui": mensaje}