from langchain_ollama import ChatOllama
import os

from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI  # Importante: requiere 'pip install langchain-openai'
import os

def get_llm():
    """
    Inicializa y retorna la conexión con el LLM local o remoto (zgrok).
    """
    model_name = os.getenv("MODEL_NAME", "llama3.1:8b")
    
    # Intentamos leer las variables del túnel (inyectadas por GitHub Actions)
    zgrok_url = os.getenv("ZGROK_URL")
    zgrok_token = os.getenv("ZGROK_TOKEN")
    
    # Si existen las variables de zgrok, usamos el modo remoto (para CI/CD)
    if zgrok_url and zgrok_token:
        return ChatOpenAI(
            model=model_name,
            temperature=0.3,
            base_url=zgrok_url,
            api_key=zgrok_token
        )
    
    # Si no existen, usamos el modo estrictamente local
    else:
        host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        return ChatOllama(
            model=model_name,
            temperature=0.3,
            base_url=host,
            keep_alive="24h" # Retención en VRAM (solo soportado por ChatOllama)
        )