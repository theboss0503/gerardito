# Plan de Escalabilidad - Gerardito IA

## Estado Actual

- **Arquitectura:** Monolito FastAPI + PostgreSQL + React
- **Modelo IA:** Gemma 4 31B via Ollama Cloud (externo)
- **Base de datos:** PostgreSQL 16 (sin partitioning, sin read replicas)
- **Cuello de botella principal:** Latencia del modelo LLM (~5-8s por request)
- **Cache:** No implementado
- **Rate limiting:** No implementado

## Metricas de Referencia (endpoint /metrics)

| Metrica | Valor estimado | Descripcion |
|---------|---------------|-------------|
| Latencia total promedio | ~700ms | Incluye LLM + DB + overhead |
| Latencia LLM promedio | ~5000ms | Dependiente de Ollama Cloud |
| p95 total | ~800ms | 95% de requests completan en este tiempo |
| Tasa de error | <5% | Principalmente 422 de validacion |

## Plan de Escalabilidad

### Corto Plazo (ya implementable)

1. **Cache de resultados frecuentes**
   - Redis para cache de diagnosticos y exploraciones similares
   - TTL: 24 horas
   - Impacto: Reduce llamadas LLM un ~30% en uso repetido

2. **Rate limiting**
   - FastAPI middleware con limite por IP/sesion
   - Limite recomendado: 10 requests/minuto por sesion
   - Impacto: Protege contra abuso y reduce costos de API

3. **Connection pooling optimizado**
   - SQLAlchemy ya usa pool, pero puede optimizarse con `pool_size` y `max_overflow`
   - Impacto: Mejor manejo de concurrencia

### Mediano Plazo

4. **Worker asincrono para LLM**
   - Celery o ARQ con Redis como broker
   - Las llamadas LLM se ejecutan en workers separados
   - Frontend usa polling o WebSocket para recibir resultado
   - Impacto: Desacopla el API de la latencia del LLM

5. **Read replicas de PostgreSQL**
   - Para separar lecturas (metrics, historial) de escrituras
   - Impacto: Mejora rendimiento en consultas de metrics

6. **CDN para frontend**
   - Cloudflare o similar para assets estaticos
   - Impacto: Reduce carga del servidor y mejora tiempo de carga

### Largo Plazo

7. **Microservicios**
   - Separar servicio de LLM del servicio de datos
   - API Gateway para routing
   - Impacto: Escalabilidad independiente por componente

8. **Auto-scaling**
   - Oracle Cloud auto-scaling para el servicio API
   - Impacto: Manejo automatico de picos de demanda

## Riesgos de Escalabilidad

| Riesgo | Probabilidad | Impacto | Mitigacion |
|--------|-------------|---------|------------|
| Ollama Cloud con downtime | Baja | Alto | Documentar fallback, plan de contingencia |
| PostgreSQL sin backup | Media | Alto | Implementar backups automaticos |
| Sin rate limiting | Media | Medio | Implementar antes de produccion pesada |
| Cache sin invalidacion | Baja | Medio | TTL corto + invalidacion manual |

## Criterios de Exito

- Latencia p95 < 1s (sin contar LLM)
- Tasa de error < 1%
- Disponibilidad > 99.5%
- Tiempo de respuesta LLM < 10s (promedio)
