from app.models.llm_loader import get_llm
from langchain_core.prompts import PromptTemplate

llm = get_llm()

def validar_texto_individual(texto: str, contexto: str) -> dict:
    """
    Evalúa si el texto es válido, tolera mala ortografía y extrae el concepto limpio.
    """
    template = """
    Eres el evaluador de un test de orientación vocacional.
    El usuario ingresa un texto que representa un(a) '{contexto}'.

    REGLAS:
    1. TOLERANCIA FONÉTICA EXTREMA: Acepta habilidades o intereses reales, INCLUSO CON PÉSIMA ORTOGRAFÍA. Si al pronunciarlo en voz alta tiene sentido, acéptalo y corrígelo. 
       - Tolera el intercambio de letras que suenan igual (b/v, c/s/z, ll/y, g/j) y la omisión de la 'h'.
    2. SPANGLISH Y TECNOLOGÍA: Acepta anglicismos o términos de internet castellanizados (ej. jakear, stremear, mutear, farmear) y clasifícalos en su rama tecnológica o digital correspondiente.
    3. RECHAZO ESTRICTO: Rechaza ROTUNDAMENTE: insultos, quejas ('tengo sueño'), saludos ('hola') o texto al azar que no suene a nada real ('asdfg').

    FORMATO DE RESPUESTA ESTRICTO:
    Debes responder en una sola línea separada por un símbolo |.
    Si es válido: SI | [Concepto limpio y corregido en 1-3 palabras]
    Si no es válido: NO | N/A

    Ejemplos de cómo aplicar la tolerancia:
    Texto: "programar sitios web" -> SI | Desarrollo Web
    Texto: "ezcrivir" -> SI | Escribir
    Texto: "alludar a la jente" -> SI | Ayuda Social
    Texto: "divujar vien" -> SI | Dibujo
    Texto: "jakear cuentas" -> SI | Ciberseguridad
    Texto: "estremear juegos" -> SI | Creación de Contenido
    Texto: "jajaja" -> NO | N/A

    Texto a evaluar: "{texto}"
    """
    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm
    
    # Inferencia
    respuesta_llm = chain.invoke({"contexto": contexto, "texto": texto}).content.strip()
    
    # Procesamiento para separar la decisión de la clasificación
    # Ejemplo de respuesta_llm: "SI | Escribir"
    partes = respuesta_llm.split("|")
    decision = partes[0].strip().upper()
    
    # Si por alguna razón el LLM no usa el formato correcto, evitamos que la API colapse
    concepto_limpio = partes[1].strip() if len(partes) > 1 else None
    
    es_valido = "SI" in decision
    mensaje = "Válido" if es_valido else f"El texto ingresado no es válido para una {contexto}. Por favor, ingresa datos reales."
    
    # Si es inválido o el concepto es "N/A", mandamos null a la clasificación
    clasificacion_final = concepto_limpio if es_valido and concepto_limpio != "N/A" else None
    
    return {
        "es_valido": es_valido, 
        "mensaje_ui": mensaje, 
        "clasificacion": clasificacion_final
    }