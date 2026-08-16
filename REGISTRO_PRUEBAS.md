# Registro de Errores y Correcciones (Testing y CI/CD)

1. **Bloqueo de Importación de Módulos (CI/CD y Local)**
   - **Error:** `ModuleNotFoundError: No module named 'app'` al ejecutar pytest.
   - **Causa:** El entorno aislado de GitHub Actions no reconocía el directorio raíz como parte del `PYTHONPATH`.
   - **Corrección:** Se modificó el comando de ejecución de pruebas en el pipeline a `python -m pytest -v test/` para forzar la inclusión del directorio actual en la ruta de búsqueda de módulos.

2. **Falta de Dependencias en el Pipeline**
   - **Error:** `ModuleNotFoundError: No module named 'langchain_openai'` durante el flujo de CI.
   - **Causa:** La dependencia necesaria para la conexión remota con la IA no estaba declarada en los pasos de instalación del contenedor virtual de GitHub.
   - **Corrección:** Se agregó la dependencia al comando de instalación en `ci.yml`.

3. **Error de Enrutamiento en Entorno de Pruebas**
   - **Error:** Todos los endpoints devolvían error `404 Not Found` durante la ejecución de los tests.
   - **Causa:** El cliente de pruebas (`TestClient`) estaba solicitando rutas absolutas (ej. `/diagnostico`), pero la aplicación principal enruta todo bajo un prefijo ( `/api/v1/diagnostico`).
   - **Corrección:** Se actualizaron las URLs en el archivo `test/test_main.py` para coincidir con el enrutador de la aplicación principal.

4. **Vulnerabilidad en Validación de Datos (Pydantic)**
   - **Error:** El sistema procesaba listas vacías `[]` retornando un código HTTP `200 OK`, lo cual es un comportamiento indeseado para el motor de diagnóstico.
   - **Causa:** El esquema de Pydantic `PerfilEstudiante` validaba el tipo de dato (lista), pero no su longitud mínima.
   - **Corrección:** Se modificó el esquema agregando `min_length=1` mediante `Field()` a las propiedades de habilidades e intereses, logrando que el sistema retorne el código de error `422 Unprocessable Entity` antes de ejecutar la lógica de negocio.

5. **Error 422 en Tests tras agregar `X-Session-Id` (Semana 6)**
   - **Error:** 6 de 11 tests fallaban con `422 Unprocessable Entity` tras agregar el header requerido `X-Session-Id`.
   - **Causa:** Los tests no enviaban el header `X-Session-Id` que ahora es obligatorio en todos los endpoints de datos.
   - **Corrección:** Se actualizó `test/test_main.py` para generar un `session_id` UUID y enviarlo como header `X-Session-Id` en todas las peticiones de prueba.

6. **Error de Importación en Frontend: `./types` (Semana 6)**
   - **Error:** `TS2307: Cannot find module './types'` al compilar el frontend con TypeScript.
   - **Causa:** El archivo `api/client.ts` importaba `../types` como `./types` (ruta incorrecta, resolvía a `src/api/types.ts` en lugar de `src/types.ts`).
   - **Corrección:** Se cambió la ruta de importación de `./types` a `../types` en `src/api/client.ts`.

7. **Migración de Llama 3.1 a Gemma 4 31B (Semana 6)**
   - **Cambio:** Se migró el modelo de IA de Llama 3.1 (local Ollama) a Gemma 4 31B (Ollama Cloud).
   - **Archivos afectados:** `app/models/llm_loader.py`, `app/api/routes.py`, `app/schemas/vocacional.py`, `test/test_main.py`, todos los documentos de arquitectura y API.
   - **Nuevo modelo:** `gemma4:31b` con autenticación `Authorization: Bearer` en el header.

8. **Migración de SQLite/Memoria a PostgreSQL (Semana 6)**
   - **Cambio:** Se implementó persistencia relacional con PostgreSQL, ORM SQLAlchemy (async) y driver asyncpg.
   - **Nuevos archivos:** `app/db/__init__.py`, `app/db/connection.py`, `app/db/models.py`.
   - **Tablas:** sesion, diagnostico, exploracion, resena.
   - **Dependencias nuevas:** `sqlalchemy[asyncio]`, `asyncpg`, `alembic` en `requirements.txt`.

9. **Implementación de Observabilidad (Semana 6)**
   - **Cambio:** Se agregó middleware de tiempos de respuesta y decorador de inferencia LLM.
   - **Nuevos archivos:** `app/middleware/__init__.py`, `app/middleware/observabilidad.py`.
   - **Nueva tabla:** `metricas` en PostgreSQL (endpoint, method, status_code, tiempo_total_ms, tiempo_llm_ms, request_bytes, response_bytes, session_id, created_at).
   - **Nuevo endpoint:** `GET /api/v1/metrics` que devuelve resumen global, métricas por endpoint, métricas del LLM y últimas 100 peticiones.
   - **Decoradores aplicados:** `@timer_llm("diagnostico")`, `@timer_llm("exploracion")`, `@timer_llm("resena")` en los servicios que llaman al LLM.
   - **Logs en consola:** Cada petición imprime `METHOD /path STATUS TIMEms (LLM: TIMEms)`.
   - **Excluidos de métricas:** `/health`, `/metadata`, `/prueba-llm`, `/metrics`.
