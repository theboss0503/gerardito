from app.models.llm_loader import get_llm
from langchain_core.prompts import PromptTemplate

llm = get_llm()

def validar_texto_individual(texto: str, tipo: str) -> dict:
    """
    Evalúa el texto basándose estrictamente en si fue ingresado como habilidad o como interés.
    """
    template = """
    Eres el filtro de seguridad de un test de orientación vocacional. 
    El usuario afirma que el siguiente texto es su {tipo}.
    
    Tu tarea es evaluar si el texto ingresado tiene sentido específicamente como un(a) {tipo} personal para elegir una carrera universitaria.
    
    REGLA 1 (Tolerancia ortográfica): Perdona errores de tipeo o mala ortografía.
    REGLA 2 (Rechazo Estricto): Debes rechazar y responder 'NO' a:
    - Insultos, groserías o lenguaje inapropiado (Bloqueo inmediato).
    - Necesidades biológicas, estados de ánimo o quejas (ej. 'quiero comer', 'tengo sueño').
    - Peticiones al chatbot o charla general (ej. 'dame una receta', 'hola').
    - Teclas al azar o palabras absurdas (ej. 'asdfg').
    
    Responde ESTRICTAMENTE con 'SI' o 'NO'. Cero explicaciones.
    
    Texto ingresado como {tipo}: "{texto}"
    """
    
    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm
    
    # Inferencia (convertimos 'tipo' a mayúsculas en el prompt para darle más énfasis)
    respuesta_llm = chain.invoke({"tipo": tipo.upper(), "texto": texto}).content.strip().upper()
    
    es_valido = "SI" in respuesta_llm
    
    # Mensaje dinámico para el frontend de React
    if es_valido:
        mensaje = "Válido"
    else:
        articulo = "una" if tipo == "habilidad" else "un"
        mensaje = f"El texto ingresado no parece ser {articulo} {tipo} válido(a). Por favor, ingresa datos reales."
    
    return {"es_valido": es_valido, "mensaje_ui": mensaje}