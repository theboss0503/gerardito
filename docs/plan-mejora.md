# Plan de Mejora Continua (Semanas 2 a 6)

## 1. Introducción
Este documento detalla la hoja de ruta técnica para la evolución del sistema "Gerardito". El objetivo principal era refactorizar la arquitectura monolítica actual (Streamlit) hacia una solución distribuida, escalable y persistente. **Todos los hitos han sido completados.**

---

## Semana 2: API inteligente y contratos de entrada/salida ✅
**Objetivo:** Desacoplar la lógica de negocio y la inferencia de IA de la interfaz gráfica.
- **Backend Independiente:** Migración de LangChain y spaCy a una API RESTful con **FastAPI**.
- **Contratos de Datos:** Esquemas Pydantic para validación estricta de entrada/salida.
- **Documentación:** Swagger UI (`/docs`) habilitado nativamente por FastAPI.
- **Persistencia:** Integración de SQLAlchemy con PostgreSQL (ORM async + asyncpg).

---

## Semana 3: Pruebas, automatización y CI/CD ✅
**Objetivo:** Garantizar la fiabilidad del motor de IA y la estabilidad de la API.
- **Pruebas:** Suite de `pytest` con 11 pruebas (happy paths y sad paths).
- **CI/CD:** Pipeline de GitHub Actions ejecutando pruebas en cada push/PR.
- **Seguridad IA:** Filtro semántico validado con pruebas automatizadas.

---

## Semana 4: Contenerización y Aislamiento ✅
**Objetivo:** Estandarizar el entorno de ejecución con Docker.
- **Dockerfile:** Imagen optimizada de Python con spaCy descargado en tiempo de construcción.
- **Protección de Entorno:** `.dockerignore` y variables de entorno via `.env`.
- **Conexión Cloud:** API contenerizada conectada exitosamente con Ollama Cloud.

---

## Semana 5: Observabilidad y Rendimiento ✅
**Objetivo:** Medir el comportamiento del sistema.
- **Logging:** Módulo `logging` de Python integrado en los endpoints.
- **Endpoint de Salud:** `/health` funcional para verificación de estado.
- **Pruebas de Conexión:** Endpoint `/prueba-llm` para verificar conectividad con Ollama Cloud.

---

## Semana 6: Frontend React + PostgreSQL + Docker Compose ✅
**Objetivo:** Completar la arquitectura de 5 capas.
- **Frontend React:** SPA completa con React + TypeScript + Vite, 4 fases del wizard.
- **PostgreSQL:** 4 tablas (sesion, diagnostico, exploracion, resena) con ORM SQLAlchemy async.
- **Session ID:** Header `X-Session-Id` requerido en todos los endpoints de datos.
- **Docker Compose:** 3 servicios orquestados (PostgreSQL + API + Frontend).
- **ARM64:** Compatible con arquitectura ARM (todas las imágenes son multi-arch).
- **Configuración:** `VITE_API_URL` configurable para acceso remoto.
- **Observabilidad:** Middleware de tiempos de respuesta + decorador `@timer_llm` para inferencia + tabla `metricas` en PostgreSQL + endpoint `GET /metrics`.
- **Documentación:** README, arquitectura, API y planes actualizados.
