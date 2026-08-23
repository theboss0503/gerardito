import time
import inspect
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("observabilidad")

EXCLUDED_PATHS = {"/health", "/metadata", "/prueba-llm", "/docs", "/openapi.json"}


def timer_llm(nombre: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = (time.perf_counter() - start) * 1000
            logger.info(f"LLM [{nombre}] {elapsed:.0f}ms")
            return result
        async def async_wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = await func(*args, **kwargs)
            elapsed = (time.perf_counter() - start) * 1000
            logger.info(f"LLM [{nombre}] {elapsed:.0f}ms")
            return result
        if inspect.iscoroutinefunction(func):
            return async_wrapper
        return wrapper
    return decorator


class ObservabilidadMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if any(path.endswith(p) for p in EXCLUDED_PATHS):
            return await call_next(request)

        body_bytes = 0
        if request.method in ("POST", "PUT", "PATCH"):
            try:
                raw = await request.body()
                body_bytes = len(raw)
            except Exception:
                pass

        start = time.perf_counter()

        response = await call_next(request)
        status_code = response.status_code

        elapsed_total = (time.perf_counter() - start) * 1000
        logger.info(
            f"{request.method} {path} {status_code} {elapsed_total:.0f}ms"
        )

        return response


