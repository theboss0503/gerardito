from app.models.llm_loader import get_llm
from langchain_core.prompts import PromptTemplate

llm = get_llm()

def generar_diagnostico_vocacional(habilidades: str, intereses: str) -> str:
    template = """
    Eres Gerardito, orientador vocacional de la Universidad Gerardo Barrios (UGB).
    Evalúa este perfil:
    Habilidades: {habilidades}
    Intereses: {intereses}
    
    Genera una tabla en formato Markdown con las 3 carreras más afines de la UGB, su porcentaje de afinidad y justificación.
    """
    
    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm
    
    return chain.invoke({"habilidades": habilidades, "intereses": intereses}).content