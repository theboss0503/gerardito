# Gerardito: Sistema de Orientación Vocacional Inteligente UGB

## 1. Información General

**Módulo:** Módulo 4 - Desarrollo de Aplicaciones con IA  
**Semana:** Semana 6 - Seguridad, Documentación y Defensa  
**Nombre del equipo:** Equipo Gerardito  
**Integrantes:** 
- Integrante 1: Fátima del Carmen Ayala Santos
- Integrante 2: Fernando Rubén Chévez Sánchez
- Integrante 3: Meylin Nohely Reyes Medina

---

## 2. Descripción del Problema

La elección de una carrera universitaria es un proceso crítico; sin embargo, los test vocacionales tradicionales institucionales operan mediante reglas estáticas y formularios rígidos. Esto provoca que los estudiantes (especialmente de bachillerato) no se sientan comprendidos, ya que estos sistemas no logran procesar sus verdaderos intereses expresados en lenguaje natural, jerga local o con errores ortográficos comunes. Una mala orientación deriva en deserción temprana o cambios recurrentes de carrera, afectando tanto al estudiante como a las métricas de retención de la Universidad Gerardo Barrios (UGB). Una solución con IA aporta un valor incalculable al permitir un perfilamiento semántico, dinámico y altamente empático.

---

## 3. Usuarios o Beneficiarios

| **Usuario / Beneficiario**        | **Necesidad principal**                                                                                 | **Beneficio proporcionado por la aplicación**                                                                                                     |
|-----------------------------------|---------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| Aspirantes de Bachillerato        | Encontrar una carrera universitaria afín a sus gustos y habilidades reales sin fricciones tecnológicas. | Permite expresarse libremente en su propio lenguaje, recibiendo un diagnóstico comprensible, justificado y validado en tiempo real.               |
| Universidad Gerardo Barrios (UGB) | Reducir la tasa de deserción y optimizar el proceso de admisión y orientación.                          | Proporciona una herramienta automatizada, escalable y atractiva que genera recomendaciones precisas basadas estrictamente en su catálogo oficial. |

---

## 4. Descripción de la Solución

"Gerardito" es una aplicación web interactiva que automatiza y humaniza el proceso de orientación vocacional. La aplicación permite al usuario seleccionar y escribir sus habilidades e intereses. Recibe como entrada datos categóricos y texto libre, los cuales son pasados por un filtro de seguridad semántico (que tolera errores ortográficos pero bloquea lenguaje basura o inapropiado). Como resultado, entrega una matriz de afinidad (3 carreras sugeridas con su porcentaje de compatibilidad y justificación) y permite una exploración detallada a través de un chat controlado. Finalmente, procesa la retroalimentación del usuario evaluando su sentimiento general (detectando ironías y sarcasmo).

---

## 5. Componente de Inteligencia Artificial

| **Elemento** | **Descripción** |
|---|---|
| **Tipo de IA utilizada** | Inteligencia Artificial Generativa y Procesamiento de Lenguaje Natural (NLP). |
| **Modelo, algoritmo, servicio o técnica** | Gemma 4 31B vía Ollama Cloud y spaCy (`es_core_news_sm`). |
| **Datos de entrada** | Perfil en texto libre del estudiante y reseñas de evaluación validados mediante esquemas Pydantic. |
| **Resultado generado por la IA** | Validación de seguridad (SI/NO/INVALIDO), Diagnóstico cruzado (Markdown) y Clasificación de Sentimientos. |
| **Métrica o forma de evaluación, si aplica** | Nivel de precisión en el emparejamiento con el catálogo institucional y contención de Prompt Injections. |
| **Limitaciones actuales** | Dependencia de la conectividad con Ollama Cloud para la inferencia del LLM. |

**Explicación breve:**
La IA actúa como el motor central en tres fases operativas: primero como un "firewall cognitivo" que valida la coherencia de la entrada del estudiante; segundo, como un sistema experto que inyecta el catálogo de la UGB en su contexto para razonar la mejor opción de carrera; y tercero, mediante un enfoque híbrido (LLM + spaCy) que analiza semántica y sintácticamente las reseñas finales a través de una API RESTful.

---

## 6. Estado Actual del Proyecto

### Funcionalidades que ya funcionan
- **Backend API:** API RESTful completa con FastAPI, 5 endpoints funcionales y documentación Swagger automática.
- **Persistencia de Datos:** PostgreSQL con ORM SQLAlchemy (async), tablas: Sesion, Diagnostico, Exploracion, Resena.
- **Validación Estricta:** Esquemas Pydantic para sanear datos y manejar errores (HTTP 400 y 422).
- **Seguridad IA:** Filtro semántico de seguridad funcional (tolera ortografía, bloquea insultos y texto vacío/basura).
- **Frontend React:** SPA completa con React + TypeScript + Vite, 4 fases del wizard, conexión a todos los endpoints.
- **Docker Compose:** Orquestación de 3 servicios (PostgreSQL + API + Frontend) con un solo comando, compatible con ARM64.
- **Conexión Cloud:** Gemma 4 31B a través de Ollama Cloud (sin dependencia de hardware local).
- **Observabilidad:** Middleware de tiempos de respuesta + decorador de inferencia LLM + endpoint `/metrics` con métricas acumuladas.

### Funcionalidades pendientes
- Observabilidad y métricas de rendimiento (Semana 5).
- Despliegue en máquina virtual con Docker Compose.

### Evidencias actuales
*(Documentación de API y pruebas en Swagger UI / Consola)*

![Swagger](/images/swagger.jpeg)
![Descripción de la imagen](/images/consola.jpeg)

**Enlace a documentación de api:** `docs/api.md`

---

## 7. Arquitectura Actual

**Enlace a documento detallado:** `docs/arquitectura-actual.md`

| Componente | Descripción | Estado actual |
|---|---|---|
| Backend / API | API RESTful contenerizada con Docker y validación Pydantic. | Desacoplado y Funcional |
| Lógica Principal | Orquestación de LangChain y pipeline NLP enrutados en endpoints HTTP. | Integrado en API |
| Interfaz | SPA React.js + TypeScript + Vite consumiendo los endpoints. | Completo |
| Componente IA | Gemma 4 31B vía Ollama Cloud y spaCy (CPU). | Operativo (Cloud) |
| Datos | PostgreSQL con ORM SQLAlchemy (async), 4 tablas relacionales. | Persistente |
| Operación | Docker Compose: PostgreSQL + API + Frontend. Compatible ARM64. | Completo |
| Observabilidad | Middleware de tiempos + decorador LLM + tabla metricas + endpoint /metrics. | Completo |

---

## 8. Arquitectura Objetivo

**Enlace a documento detallado:** `docs/arquitectura-objetivo.md`

La arquitectura de 5 capas está completamente implementada:

- **Interfaz:** SPA en **React.js + TypeScript + Vite** consumiendo la API.
- **API / Backend:** API RESTful robusta y documentada utilizando **FastAPI**.
- **Servicio IA:** Orquestación de Gemma 4 31B y spaCy protegida por validadores Pydantic.
- **Datos:** **PostgreSQL** con ORM SQLAlchemy (async) y asyncpg, soportando concurrencia.
- **Operación:** **Docker Compose** con 3 servicios orquestados, compatible con ARM64.

---

## 9. Estructura del Repositorio

```text
gerardito/
  ├── .github/              # Configuración de GitHub Actions (CI/CD)
  ├── app/                  # Código principal del backend y frontend
  │   ├── api/              # Endpoints de FastAPI (routes.py)
  │   ├── db/               # Conexión y modelos ORM (SQLAlchemy)
  │   ├── models/           # LLM loader (Ollama Cloud)
  │   ├── schemas/          # Modelos de validación Pydantic
  │   ├── services/         # Lógica de LangChain y spaCy
  │   └── FrontEnd/         # React + TypeScript + Vite (SPA)
  ├── docs/                 # Documentación técnica y diagramas
  ├── test/                 # Pruebas unitarias y de integración (pytest)
  ├── docker-compose.yml    # Orquestación de servicios (ARM64 compatible)
  ├── Dockerfile            # Instrucciones de construcción de la imagen de la API
  ├── .dockerignore         # Exclusiones de archivos para la imagen Docker
  ├── .env.example          # Plantilla de variables de entorno seguras
  ├── README.md             # Este archivo
  ├── REGISTRO_PRUEBAS.md   # Registro de errores detectados y corregidos
  └── requirements.txt      # Dependencias de Python
```

---

## 10. Instalación y Ejecución

### Opción A: Docker Compose (Recomendado para producción)

1. **Configurar variables de entorno:**
   ```bash
   cp .env.example .env
   # Editar .env con tu OLLAMA_API_KEY
   ```

2. **Levantar todos los servicios:**
   ```bash
   docker compose up --build
   ```

3. **Acceder:**
   | Servicio | URL |
   |----------|-----|
   | Frontend | `http://localhost:5173` |
   | API + Swagger | `http://localhost:8000/docs` |
   | PostgreSQL | `localhost:5432` |

> **Nota para VM:** Cambia `localhost` por la IP de la VM en `VITE_API_URL` dentro de `.env` si accedes desde otro equipo.

### Opción B: Desarrollo Local

1. **PostgreSQL (solo la BD via Docker):**
   ```bash
   docker compose up postgres -d
   ```
   Esto levanta PostgreSQL en el puerto 5432. Las tablas se crean automáticamente al iniciar la API.

2. **Backend:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate        # Windows
   pip install -r requirements.txt
   python -m spacy download es_core_news_sm
   cp .env.example .env         # Configurar OLLAMA_API_KEY y DATABASE_URL
   uvicorn app.main:app --reload
   ```

3. **Frontend (otra terminal):**
   ```bash
   cd app/FrontEnd
   npm install
   npm run dev
   ```

4. **Acceder:** Frontend en `http://localhost:5173`, API en `http://localhost:8000/docs`.

### Requisitos previos
- Docker (para PostgreSQL en desarrollo local, o para todo en Docker Compose).
- Python 3.11+ (para desarrollo local).
- Node.js 18+ (para desarrollo local).
- Cuenta en Ollama Cloud con API key.

---

## 11. Pruebas Automatizadas y CI/CD

### Ejecución Local

```bash
python -m pytest -v test/
```

> **Nota:** Los endpoints que requieren inferencia del LLM (`/diagnostico`, `/explorar`, `/resena`) necesitan conectividad con Ollama Cloud.

### Integración Continua (CI/CD)

GitHub Actions ejecuta en cada push o pull request:

1. Levantar el entorno de ejecución con Python.
2. Instalar las dependencias requeridas.
3. Establecer conexión con Ollama Cloud.
4. Ejecutar la suite completa de pruebas.

---

## 12. Datos Utilizados

| Fuente de datos | Tipo de datos | Uso dentro del proyecto | Observaciones |
|---|---|---|---|
| Catálogo UGB | Texto estático | Cruce de variables de afinidad para recomendar la carrera. | Integrado en los prompts del backend. |
| Sesión de Usuario | Texto libre y categórico | Habilidades e intereses ingresados por el aspirante. | Saneados mediante esquemas Pydantic. |
| Historial | PostgreSQL | Sesiones, diagnósticos, exploraciones y reseñas. | Persistente y preparado para concurrencia. |

**Consideraciones:**

- El catálogo de la UGB es público. Los datos ingresados por los usuarios se tratan como privados.
- El texto libre del usuario se somete a validación semántica y filtros de longitud.
- PostgreSQL soporta escrituras concurrentes para pruebas de carga.

---

## 13. Riesgos Técnicos y Deuda Técnica

| Riesgo | Categoría | Probabilidad | Impacto | Mitigación propuesta |
|---|---|---|---|---|
| *Resuelto:* Acoplamiento | Código | Baja | N/A | *Mitigado:* API REST con FastAPI. |
| *Resuelto:* Dependencias | Entorno | Baja | N/A | *Mitigado:* Docker y Docker Compose. |
| *Resuelto:* Pérdida de Historial | Datos | Baja | N/A | *Mitigado:* PostgreSQL con ORM SQLAlchemy. |
| Dependencia de Ollama Cloud | Despliegue | Baja | Medio | La inferencia depende de la conectividad con Ollama Cloud. |

---

## 14. Plan de Mejora por Semana

| Semana | Mejora esperada | Estado |
|---|---|---|
| **Semana 2** | **API inteligente y contratos de entrada/salida (FastAPI)** | **Completado** |
| **Semana 3** | **Pruebas y CI/CD (Validación de filtros de seguridad de IA)** | **Completado** |
| **Semana 4** | **Contenerización y Aislamiento (Docker)** | **Completado** |
| **Semana 5** | **Observabilidad y rendimiento** | Completado |
| **Semana 6** | **Frontend React + PostgreSQL + Docker Compose + Documentación** | **Completado** |

---

## 15. Limitaciones Actuales

- El rendimiento del sistema depende de la conectividad con Ollama Cloud.
- No hay autenticación de usuarios (el `session_id` es un UUID auto-generado).
- Falta migración de esquema con Alembic para cambios futuros en la BD.

---

## 16. Evidencias

| Evidencia | Enlace o ubicación | Descripción |
|---|---|---|
| Documentación API | `docs/api.md` | Uso de Swagger UI para pruebas |
| Arquitectura Actual | `docs/arquitectura-actual.md` | Flujo de componentes del sistema |
| Arquitectura Objetivo | `docs/arquitectura-objetivo.md` | Arquitectura de 5 capas implementada |

---

## 17. Créditos y Referencias

- **LangChain & Ollama Cloud:** Orquestación de inferencia con Gemma 4 31B (Cloud).
- **spaCy:** Framework de Procesamiento de Lenguaje Natural para extracción sintáctica (modelo `es_core_news_sm`).
- **FastAPI & Pydantic:** Framework web y validación estricta de datos para la construcción de la API.
- **SQLAlchemy:** ORM para persistencia de datos con PostgreSQL.
- **React + TypeScript + Vite:** Frontend moderno y tipado.
- **Docker:** Plataforma de contenerización para aislamiento de servicios.
- **Universidad Gerardo Barrios (UGB):** Catálogo oficial de la oferta académica.
