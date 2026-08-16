import os
from functools import lru_cache


@lru_cache(maxsize=1)
def get_llm():
    from langchain_ollama import ChatOllama

    model_name = os.getenv("MODEL_NAME", "gemma4:31b")
    api_key = os.getenv("OLLAMA_API_KEY")
    base_url = os.getenv("OLLAMA_HOST", "https://ollama.com")

    client_kwargs = {}
    if api_key:
        client_kwargs["headers"] = {"Authorization": f"Bearer {api_key}"}

    return ChatOllama(
        model=model_name,
        temperature=0.3,
        base_url=base_url,
        client_kwargs=client_kwargs,
    )
