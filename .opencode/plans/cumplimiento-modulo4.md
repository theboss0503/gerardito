# Plan: Cumplimiento de Requisitos - Evaluación Final Módulo 4

## Resumen de brechas identificadas

| # | Brecha | Prioridad |
|---|--------|-----------|
| 1 | Falta `release-manifest.yml` | Alta |
| 2 | Falta `docs/final/plan-contingencia-demo.md` | Alta |
| 3 | Métricas sin p50/p95 | Alta |
| 4 | Falta `docs/escalabilidad.md` | Media |
| 5 | `requirements.txt` incompleto | Alta |
| 6 | Sin smoke tests en CI | Media |
| 7 | Sin documentar cuotas/costos Ollama | Media |
| 8 | Sin manejo de cuota agotada | Media |
| 9 | Sin procedimiento de rollback | Media |

---

## Acción 1: Crear `release-manifest.yml`

**Archivo:** `release-manifest.yml` (raíz del repo)

Contenido:
- `release.version`, `release.tag`, `release.commit` (4a4896a7e547b36e7374bfdf40439858ad09b211)
- `producto` (nombre, tipo, url, stack)
- `api` (8 endpoints documentados)
- `modelo` (gemma4:31b, Ollama Cloud, timeout, reintentos)
- `prompt` (4 prompts: diagnóstico, explorar, validar, reseña)
- `datos` (ficticios, PostgreSQL, retención)
- `imagen` (python:3.11-slim, Dockerfile, spaCy)
- `ambiente` (Docker Compose 4 servicios, Oracle Cloud, dominio)
- `pruebas` (pytest, 12 tests, CI, smoke tests)
- `limitaciones_conocidas` (7 items documentados)

---

## Acción 2: Crear `docs/final/plan-contingencia-demo.md`

**Archivo:** `docs/final/plan-contingencia-demo.md`

Tabla con 7 riesgos, prevención y respuesta:
1. Servicio dormido → calentar 15 min + /health + reintento
2. Tokens/cuota agotada → revisar panel + mensaje controlado
3. DNS/SSL/release → probar desde otra red + evidencia
4. Datos/almacenamiento → sembrar datos + verificar conexión
5. Sesión vencida → validar cuenta + reingreso rápido
6. CORS/migración → probar producción + rollback
7. API externa lenta → timeout + error controlado

Verificaciones programadas:
- 24h antes: congelar release, probar recorrido, revisar secretos
- 2h antes: confirmar URL, datos, proveedor, cuotas
- 15 min antes: calentar servicios, iniciar sesión
- Al finalizar: no exponer credenciales, registrar incidentes

---

## Acción 3: Métricas p50/p95 en endpoint `/metrics`

**Archivo:** `app/api/routes.py` (modificar `get_metrics`)

Cambios:
- Agregar cálculo de percentiles p50 y p95 a partir de la lista de `tiempos`
- Usar `statistics.median()` para p50
- Usar fórmula de percentil para p95 (o `numpy` si está disponible, pero sin agregar dependencia)
- Agregar `p50_ms` y `p95_ms` al diccionario `resumen`
- Agregar `p50_ms` y `p95_ms` a `por_endpoint` también

```python
import statistics

# En get_metrics():
tiempos_sorted = sorted(tiempos)
p50 = statistics.median(tiempos_sorted)
p95_index = int(len(tiempos_sorted) * 0.95)
p95 = tiempos_sorted[min(p95_index, len(tiempos_sorted) - 1)]
```

---

## Acción 4: Crear `docs/escalabilidad.md`

**Archivo:** `docs/escalabilidad.md`

Contenido:
- Estado actual: monolito FastAPI, PostgreSQL, Ollama Cloud
- Cuello de botella identificado: latencia LLM (~5-8s), sin cache
- Plan de escalabilidad:
  - Corto plazo: Redis cache para diagnósticos similares, rate limiting
  - Mediano plazo: Worker asíncrono para llamadas LLM (Celery/RQ)
  - Largo plazo: Separación en microservicios, CDN para frontend
- Métricas de soporte: p50, p95, max, tasa error del endpoint `/metrics`

---

## Acción 5: Actualizar `requirements.txt`

**Archivo:** `requirements.txt`

Agregar:
```
pytest-asyncio==1.0.0
ollama==0.4.0
```

(Verificar versiones exactas con pip list)

---

## Acción 6: Smoke tests en CI

**Archivo:** `.github/workflows/ci.yml`

Agregar paso después de pytest:
```yaml
- name: Smoke tests
  run: |
    # Iniciar el servidor
    python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
    sleep 5
    # Health check
    curl -f http://localhost:8000/api/v1/health
    # Metadata
    curl -f http://localhost:8000/api/v1/metadata
    # Validar texto
    curl -f -X POST http://localhost:8000/api/v1/validar-texto \
      -H "Content-Type: application/json" \
      -d '{"texto": "programación", "tipo": "habilidad"}'
  env:
    DATABASE_URL: postgresql+asyncpg://postgres:postgres@localhost:5432/test_db
    OLLAMA_API_KEY: ${{ secrets.OLLAMA_API_KEY }}
    OLLAMA_HOST: https://ollama.com
    MODEL_NAME: gemma4:31b
```

---

## Acción 7: Documentar cuotas/costos Ollama en README

**Archivo:** `README.md` (sección nueva o modificar "Limitaciones Actuales")

Agregar subsección "Cuotas y Costos":
- Proveedor: Ollama Cloud (plan gratuito/pago)
- Modelo: gemma4:31b
- Límites por minuto/concurrencia: (documentar si se conocen)
- Manejo de cuota agotada: mensaje controlado, error registrado, no bloquea
- Recomendación: verificar panel de Ollama antes de demostración

---

## Acción 8: Manejo de cuota agotada

**Archivo:** `app/api/routes.py` (en cada endpoint con LLM)

Agregar try/except específico para errores de Ollama:
```python
except Exception as e:
    error_msg = str(e).lower()
    if "quota" in error_msg or "credit" in error_msg or "rate" in error_msg:
        raise HTTPException(
            status_code=429,
            detail="Cuota de API agotada. Intenta más tarde o verifica tu plan en Ollama Cloud."
        )
    # ... manejo de error existente
```

---

## Acción 9: Procedimiento de rollback

**Archivo:** `docs/rollback.md`

Contenido:
1. Identificar versión estable anterior (tag v1.0.0)
2. `git checkout v1.0.0`
3. Re-deploy: `docker compose down && docker compose up -d --build`
4. Verificar: `curl https://gerarditougb.qd.je/api/v1/health`
5. Si hay problemas de DB: `alembic downgrade` (si aplica)
6. Notificar al equipo

---

## Orden de ejecución

1. `release-manifest.yml` (Archivos críticos)
2. `docs/final/plan-contingencia-demo.md` (Archivos críticos)
3. `requirements.txt` (Archivos críticos)
4. Métricas p50/p95 en `/metrics`
5. `docs/escalabilidad.md`
6. Smoke tests en CI
7. Cuotas/costos en README
8. Manejo de cuota agotada
9. `docs/rollback.md`

## Verificación

- Ejecutar `pytest` para confirmar que nada se rompe
- Verificar que el endpoint `/metrics` retorna p50/p95
- Verificar que `release-manifest.yml` tiene el commit correcto
- Verificar que `docs/final/` existe con los archivos
