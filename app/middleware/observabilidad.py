import time
import asyncio
import inspect
import logging
from contextvars import ContextVar
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("observabilidad")

_llm_time_var: ContextVar[float | None] = ContextVar("llm_time_ms", default=None)

EXCLUDED_PATHS = {"/health", "/metadata", "/prueba-llm", "/metrics", "/docs", "/openapi.json"}


def timer_llm(nombre: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = (time.perf_counter() - start) * 1000
            _llm_time_var.set(elapsed)
            logger.info(f"LLM [{nombre}] {elapsed:.0f}ms")
            return result
        async def async_wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = await func(*args, **kwargs)
            elapsed = (time.perf_counter() - start) * 1000
            _llm_time_var.set(elapsed)
            logger.info(f"LLM [{nombre}] {elapsed:.0f}ms")
            return result
        if inspect.iscoroutinefunction(func):
            return async_wrapper
        return wrapper
    return decorator


async def _guardar_metrica(
    path: str, method: str, status_code: int,
    elapsed_total: float, elapsed_llm: float | None,
    body_bytes: int, response_body_bytes: int,
    session_id: str | None,
):
    try:
        from app.db.connection import async_session
        from app.db.models import Metrica

        async with async_session() as db:
            metrica = Metrica(
                endpoint=path,
                method=method,
                status_code=status_code,
                tiempo_total_ms=round(elapsed_total, 2),
                tiempo_llm_ms=round(elapsed_llm, 2) if elapsed_llm else None,
                request_bytes=body_bytes,
                response_bytes=response_body_bytes,
                session_id=session_id,
            )
            db.add(metrica)
            await db.commit()
    except Exception as e:
        logger.warning(f"No se pudo guardar métrica: {e}")


class ObservabilidadMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if any(path.startswith(p) for p in EXCLUDED_PATHS):
            return await call_next(request)

        body_bytes = 0
        if request.method in ("POST", "PUT", "PATCH"):
            try:
                raw = await request.body()
                body_bytes = len(raw)
            except Exception:
                pass

        _llm_time_var.set(None)
        start = time.perf_counter()
        status_code = 500
        response_body_bytes = 0

        try:
            response = await call_next(request)
            status_code = response.status_code
            try:
                resp_body = b""
                async for chunk in response.body_iterator:
                    resp_body += chunk if isinstance(chunk, bytes) else chunk.encode()
                response_body_bytes = len(resp_body)
                response = Response(
                    content=resp_body,
                    status_code=response.status_code,
                    headers=dict(response.headers),
                    media_type=response.media_type,
                )
            except Exception:
                pass
        except Exception:
            status_code = 500
            raise
        finally:
            elapsed_total = (time.perf_counter() - start) * 1000
            elapsed_llm = _llm_time_var.get()
            session_id = request.headers.get("x-session-id")

            llm_log = f" (LLM: {elapsed_llm:.0f}ms)" if elapsed_llm else ""
            logger.info(
                f"{request.method} {path} {status_code} {elapsed_total:.0f}ms{llm_log}"
            )

            asyncio.create_task(
                _guardar_metrica(
                    path, request.method, status_code,
                    elapsed_total, elapsed_llm,
                    body_bytes, response_body_bytes, session_id,
                )
            )

        return response
