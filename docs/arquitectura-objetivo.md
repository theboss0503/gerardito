# Arquitectura Objetivo (Módulo 4)

## 1. Visión General
El objetivo para el final del Módulo 4 era refactorizar el prototipo monolítico actual de "Gerardito" hacia una arquitectura distribuida de 5 capas. Esta arquitectura está completamente implementada.

---

## 2. Separación de Componentes (Arquitectura de 5 Capas)

### 2.1. Interfaz (Frontend)
- **Tecnología:** React.js + TypeScript + Vite.
- **Estado:** ✅ Completado.
- **Función:** SPA responsable exclusivamente de la presentación visual y la interacción fluida con el estudiante.
- **Comunicación:** Consume los servicios del backend mediante peticiones HTTP (Fetch API).

### 2.2. API / Backend (Capa Lógica)
- **Tecnología:** Python con **FastAPI**.
- **Estado:** ✅ Completado.
- **Función:** Servidor que recibe las solicitudes de React.js, valida la estructura de los datos de entrada (mediante Pydantic) y orquesta la comunicación entre la base de datos y los modelos de IA.
- **Endpoints:** `/validar-texto`, `/diagnostico`, `/explorar`, `/resena`, `/health`, `/metadata`.

### 2.3. Servicio IA (Capa Cognitiva)
- **Tecnología:** LangChain, **Gemma 4 31B** vía Ollama Cloud y spaCy (`es_core_news_sm`).
- **Estado:** ✅ Completado.
- **Función:** LangChain estructura los prompts. La inferencia se ejecuta en Ollama Cloud (sin dependencia de GPU local). spaCy procesa la extracción de palabras clave en la CPU.

### 2.4. Datos (Capa de Persistencia)
- **Tecnología:** **PostgreSQL** con ORM **SQLAlchemy (async)** y driver **asyncpg**.
- **Estado:** ✅ Completado.
- **Función:** Persistencia relacional de sesiones, diagnósticos, exploraciones y reseñas. Preparado para concurrencia de múltiples usuarios.

### 2.5. Operación y Configuración
- **Tecnología:** Docker, Docker Compose, variables de entorno (`.env`).
- **Estado:** ✅ Completado.
- **Función:** Orquestación de 3 servicios (PostgreSQL + API + Frontend) con un solo comando. Compatible con ARM64.

---

## 3. Estado de Implementación por Semana

| Semana | Objetivo | Estado |
|---|---|---|
| Semana 2 | API inteligente y contratos de entrada/salida | ✅ Completado |
| Semana 3 | Pruebas automatizadas y CI/CD | ✅ Completado |
| Semana 4 | Contenerización y aislamiento con Docker | ✅ Completado |
| Semana 5 | Observabilidad y rendimiento | ✅ Completado |
| Semana 6 | Frontend React + PostgreSQL + Docker Compose + Documentación | ✅ Completado |
