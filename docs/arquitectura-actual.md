# Arquitectura Actual del Proyecto

## 1. Usuario o Actor Principal
- **Aspirantes de Bachillerato / Estudiantes:** Son los usuarios finales que interactúan con el sistema para recibir orientación vocacional. Introducen datos sobre sus habilidades e intereses y evalúan el resultado final.

## 2. Interfaz o Punto de Entrada (Cliente)
- **SPA React.js + TypeScript + Vite:** La interfaz es una Aplicación de Página Única (SPA) construida con React, TypeScript y Vite. Actúa exclusivamente como cliente: captura los datos del usuario, los envía mediante peticiones HTTP al servidor y renderiza las respuestas recibidas. No procesa lógica de negocio.

## 3. Backend, Script o Servicio Actual (API RESTful)
- **API Independiente con FastAPI:** La lógica de negocio está completamente separada del frontend. El backend opera como un servicio RESTful construido en Python con FastAPI.
- **Validación Estricta:** Se utiliza **Pydantic** para definir esquemas de entrada y salida (`ResenaInput`, `ResenaResponse`, `ValidacionInput`, `PerfilEstudiante`, `ExploracionInput`). Garantiza que los datos vengan limpios y con el formato correcto antes de tocar la inteligencia artificial.
- **Persistencia de Datos:** **PostgreSQL** con ORM **SQLAlchemy (async)** y driver **asyncpg**. Las tablas son: `sesion`, `diagnostico`, `exploracion` y `resena`. La conexión se inicializa al arrancar la aplicación mediante un async lifespan.
- **Sesión por Request:** Cada petición incluye un header `X-Session-Id` (UUID) que identifica la sesión del usuario. El diagnóstico, exploración y reseña se asocian a la misma sesión.
- **Orquestador:** El backend utiliza endpoints (rutas) para invocar las cadenas de LangChain, gestionando la comunicación con el modelo de lenguaje de forma estructurada.

## 4. Componente de IA
- **Motor Generativo (LLM):** Gemma 4 31B ejecutado a través de **Ollama Cloud** (servicio remoto). La autenticación se realiza mediante API key en el header `Authorization: Bearer`. No requiere hardware local (GPU).
- **Motor NLP Clásico:** spaCy (modelo `es_core_news_sm`) ejecutado en el procesador (CPU) para la extracción de entidades, adjetivos y sustantivos durante el análisis de las reseñas de los usuarios.

## 5. Datos Utilizados
- **PostgreSQL (Persistente):** La información se almacena de forma permanente en 4 tablas relacionales:
  - `sesion`: ID, habilidades, intereses y timestamps.
  - `diagnostico`: resultado markdown y carreras sugeridas, vinculado a sesión.
  - `exploracion`: carrera explorada y respuesta del LLM, vinculado a sesión y diagnóstico.
  - `resena`: comentario, sentimiento y palabras clave, vinculado a sesión.
- **Catálogo Institucional:** El catálogo de carreras de la universidad está integrado como texto estático dentro de los prompts del backend.

## 6. Servicios Externos
- **Ollama Cloud (Servicio remoto):** El motor de inferencia Gemma 4 31B se ejecuta en la nube de Ollama. La API se comunica con él mediante el cliente `ollama` de Python con autenticación por API key.

## 7. Flujo Básico de Información
1. El usuario ingresa sus preferencias en la SPA React (habilidades e intereses).
2. El frontend genera un `session_id` (UUID) y lo envía en el header `X-Session-Id` de cada petición.
3. El cliente envía un payload JSON mediante una petición HTTP POST al endpoint correspondiente.
4. **Capa de Seguridad (Pydantic):** FastAPI valida el payload. Si viene vacío o corrupto, rechaza la petición con error 422.
5. Si pasa la validación, FastAPI orquesta el pipeline híbrido: spaCy extrae palabras clave y Gemma 4 evalúa el contexto/sentimiento.
6. Los resultados se persisten en PostgreSQL asociados al `session_id`.
7. El backend empaqueta el resultado y lo devuelve al cliente en formato JSON.
8. La interfaz renderiza el resultado final al usuario.

## 8. Dependencias Manuales o Puntos Frágiles
- **Conectividad con Ollama Cloud:** La inferencia depende de la conectividad con el servicio remoto de Ollama. Sin internet, el sistema no puede generar diagnósticos ni exploraciones.
- **Migración de Esquema:** Aún no se ha implementado Alembic para gestionar migraciones de la base de datos. Los cambios en los modelos ORM requieren recrear las tablas manualmente.
