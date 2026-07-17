from langchain_ollama import ChatOllama
import os

def get_llm():
    """
    Inicializa y retorna la conexión con el LLM local configurado.
    """
    host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    model_name = os.getenv("MODEL_NAME", "llama3.1:8b")
    
    return ChatOllama(
        model=model_name,
        temperature=0.3, # Baja temperatura para respuestas institucionales consistentes
        base_url=host,
        keep_alive="24h" # Retención en VRAM para optimizar inferencias
    )