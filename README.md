# Gerardito: Sistema de Orientacion Vocacional Inteligente UGB

## 1. Informacion General

**Modulo:** Modulo 4 - Desarrollo de Aplicaciones con IA  
**Semana:** Semana 6 - Seguridad, Documentacion y Defensa  
**Nombre del equipo:** Equipo Gerardito  
**Integrantes:** 
- Integrante 1: Fatima del Carmen Ayala Santos
- Integrante 2: Fernando Ruben Chevez Sanchez
- Integrante 3: Meylin Nohely Reyes Medina

---

## 2. Descripcion del Problema

La eleccion de una carrera universitaria es un proceso critico; sin embargo, los test vocacionales tradicionales institucionales operan mediante reglas estaticas y formularios rigidos. Esto provoca que los estudiantes (especialmente de bachillerato) no se sientan comprendidos, ya que estos sistemas no logran procesar sus verdaderos intereses expresados en lenguaje natural, jerga local o con errores ortograficos comunes. Una mala orientacion deriva en desercion temprana o cambios recurrentes de carrera, afectando tanto al estudiante como a las metricas de retencion de la Universidad Gerardo Barrios (UGB). Una solucion con IA aporta un valor incalculable al permitir un perfilamiento semantico, dinamico y altamente empatico.

---

## 3. Usuarios o Beneficiarios

| **Usuario / Beneficiario**        | **Necesidad principal**                                                                                 | **Beneficio proporcionado por la aplicacion**                                                                                                     |
|-----------------------------------|---------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| Aspirantes de Bachillerato        | Encontrar una carrera universitaria afin a sus gustos y habilidades reales sin fricciones tecnologicas. | Permite expresarse libremente en su propio lenguaje, recibiendo un diagnostico comprensible, justificado y validado en tiempo real.               |
| Universidad Gerardo Barrios (UGB) | Reducir la tasa de desercion y optimizar el proceso de admision y orientacion.                          | Proporciona una herramienta automatizada, escalable y atractiva que genera recomendaciones precisas basadas estrictamente en su catalogo oficial. |

---

## 4. Descripcion de la Solucion

"Gerardito" es una aplicacion web interactiva que automatiza y humaniza el proceso de orientacion vocacional. La aplicacion permite al usuario seleccionar y escribir sus habilidades e intereses. Recibe como entrada datos categoricos y texto libre, los cuales son pasados por un filtro de seguridad semantico (que tolera errores ortograficos pero bloquea lenguaje basura o inapropiado). Como resultado, entrega una matriz de afinidad (3 carreras sugeridas con su porcentaje de compatibilidad y justificacion) y permite una exploracion detallada a traves de un chat controlado. Finalmente, procesa la retroalimentacion del usuario evaluando su sentimiento general (detectando ironias y sarcasmo).

---

## 5. Componente de Inteligencia Artificial

| **Elemento** | **Descripcion** |
|---|---|
| **Tipo de IA utilizada** | Inteligencia Artificial Generativa y Procesamiento de Lenguaje Natural (NLP). |
| **Modelo, algoritmo, servicio o tecnica** | Gemma 4 31B via Ollama Cloud y spaCy (`es_core_news_sm`). |
| **Datos de entrada** | Perfil en texto libre del estudiante y resenas de evaluacion validados mediante esquemas Pydantic. |
| **Resultado generado por la IA** | Validacion de seguridad (SI/NO/INVALIDO), Diagnostico cruzado (Markdown) y Clasificacion de Sentimientos. |
| **Metrica o forma de evaluacion, si aplica** | Nivel de precision en el emparejamiento con el catalogo institucional y contencion de Prompt Injections. |
| **Limitaciones actuales** | Dependencia de la conectividad con Ollama Cloud para la inferencia del LLM. |

**Explicacion breve:**
La IA actua como el motor central en tres fases operativas: primero como un "firewall cognitivo" que valida la coherencia de la entrada del estudiante; segundo, como un sistema experto que inyecta el catalogo de la UGB en su contexto para razonar la mejor opcion de carrera; y tercero, mediante un enfoque hibrido (LLM + spaCy) que analiza semantica y sintacticamente las resenas finales a traves de una API RESTful.

---

## 6. Estado Actual del Proyecto

### Funcionalidades completadas

- **Backend API:** API RESTful completa con FastAPI, 8 endpoints funcionales y documentacion Swagger automatica.
- **Persistencia de Datos:** PostgreSQL con ORM SQLAlchemy (async), tablas: Sesion, Diagnostico, Exploracion, Resena, Metrica.
- **Validacion Estricta:** Esquemas Pydantic para sanear datos y manejar errores (HTTP 400, 422, 429).
- **Seguridad IA:** Filtro semantico de seguridad funcional (tolera ortografia, bloquea insultos y texto vacio/basura).
- **Frontend React:** SPA completa con React + TypeScript + Vite, 4 fases del wizard, conexion a todos los endpoints.
- **Docker Compose:** Orquestacion de 4 servicios (PostgreSQL + API + Frontend + Caddy) con un solo comando.
- **Conexión Cloud:** Gemma 4 31B a traves de Ollama Cloud (sin dependencia de hardware local).
- **Observabilidad:** Middleware de tiempos de respuesta + decorador de inferencia LLM + endpoint `/metrics` con metricas, p50, p95.
- **CI/CD:** GitHub Actions con 12 tests + smoke tests (health, metadata, validar-texto).
- **Despliegue:** Oracle Cloud via SSH con deploy automatico.
- **Seguridad:** CORS restringido, rate limiting (slowapi), UUID validation, API Key opcional, Docker non-root, errores sanitizados.
- **Documentacion:** README completo, api.md, arquitectura, escalabilidad, rollback, plan de contingencia, release-manifest.yml.

### Evidencias actuales

- **Tabla generada con recomendacion de carreras.**

![React](/images/tabla_carreras.png)

- **Contenedores corriendo en Maquina Virtual de Oracle.**

![Contenedores](/images/contenedores.png)    

**Enlace a documentacion de api:** `docs/api.md`

---

## 7. Arquitectura Actual

**Enlace a documento detallado:** `docs/arquitectura-actual.md`

| Componente | Descripcion | Estado actual |
|---|---|---|
| Backend / API | API RESTful contenerizada con Docker y validacion Pydantic. | Desacoplado y Funcional |
| Logica Principal | Orquestacion de LangChain y pipeline NLP enrutados en endpoints HTTP. | Integrado en API |
| Interfaz | SPA React.js + TypeScript + Vite consumiendo los endpoints. | Completo |
| Componente IA | Gemma 4 31B via Ollama Cloud y spaCy (CPU). | Operativo (Cloud) |
| Datos | PostgreSQL con ORM SQLAlchemy (async), 5 tablas relacionales. | Persistente |
| Operacion | Docker Compose: PostgreSQL + API + Frontend + Caddy. | Completo |
| Observabilidad | Middleware de tiempos + decorador LLM + tabla metricas + endpoint /metrics con p50/p95. | Completo |
| Seguridad | CORS, rate limiting, UUID validation, API Key, Docker non-root. | Completo |

---

## 8. Arquitectura Objetivo

**Enlace a documento detallado:** `docs/arquitectura-objetivo.md`

La arquitectura de 5 capas esta completamente implementada:

- **Interfaz:** SPA en **React.js + TypeScript + Vite** consumiendo la API.
- **API / Backend:** API RESTful robusta y documentada utilizando **FastAPI**.
- **Servicio IA:** Orquestacion de Gemma 4 31B y spaCy protegida por validadores Pydantic.
- **Datos:** **PostgreSQL** con ORM SQLAlchemy (async) y asyncpg, soportando concurrencia.
- **Operacion:** **Docker Compose** con 4 servicios orquestados (PostgreSQL, API, Frontend, Caddy).

---

## 9. Estructura del Repositorio

```text
gerardito/
  ├── .github/              # Configuracion de GitHub Actions (CI/CD)
  │   └── workflows/
  │       ├── ci.yml        # Tests + smoke tests
  │       └── deploy.yml    # Deploy automatico a Oracle Cloud
  ├── app/                  # Codigo principal del backend y frontend
  │   ├── api/              # Endpoints de FastAPI (routes.py)
  │   ├── auth.py           # Autenticacion API Key (opcional)
  │   ├── db/               # Conexion y modelos ORM (SQLAlchemy)
  │   ├── limiter.py        # Rate limiting compartido (slowapi)
  │   ├── middleware/        # Observabilidad (logging + timing)
  │   ├── models/           # LLM loader (Ollama Cloud)
  │   ├── schemas/          # Modelos de validacion Pydantic
  │   ├── services/         # Logica de LangChain y spaCy
  │   └── FrontEnd/         # React + TypeScript + Vite (SPA)
  │       ├── Dockerfile    # Multi-stage build (Node → Caddy)
  │       ├── src/          # Codigo fuente del frontend
  │       └── dist/         # Build de produccion
  ├── docs/                 # Documentacion tecnica y evidencias
  │   ├── api.md            # Documentacion completa de la API
  │   ├── arquitectura-actual.md
  │   ├── arquitectura-objetivo.md
  │   ├── diagnostico-semana-1.md
  │   ├── escalabilidad.md  # Plan de escalabilidad
  │   ├── plan-mejora.md
  │   ├── plan-contingencia-demo.md  # Riesgos para la demo
  │   ├── riesgos-tecnicos.md
  │   ├── rollback.md       # Procedimiento de rollback
  │   ├── Modulo 4 - Informe final .pdf
  │   ├── Observabilidad, Rendimiento y Escalabilidad.pdf
  │   ├── Evidencia de implementacion de docker.pdf
  │   └── Prueba de la API con Swagger.pdf
  ├── test/                 # Pruebas automatizadas (pytest)
  ├── release-manifest.yml  # Manifiesto del release v1.0.0
  ├── docker-compose.yml    # Orquestacion de 4 servicios
  ├── Dockerfile            # Imagen del backend (Python + spaCy)
  ├── Caddyfile             # Configuracion del reverse proxy
  ├── deploy.sh             # Script de despliegue a Oracle Cloud
  ├── .dockerignore         # Exclusiones para imagen Docker
  ├── .env.example          # Plantilla de variables de entorno
  ├── .gitignore            # Exclusiones de git
  ├── README.md             # Este archivo
  ├── REGISTRO_PRUEBAS.md   # Registro de errores detectados y corregidos
  └── requirements.txt      # Dependencias de Python
```

---

## 10. Instalacion y Ejecucion

### Opcion A: Docker Compose (Recomendado para produccion)

1. **Configurar variables de entorno:**
   ```bash
   cp .env.example .env
   # Editar .env con tu OLLAMA_API_KEY y DB_PASSWORD
   ```

2. **Levantar todos los servicios:**
   ```bash
   docker compose up --build
   ```

3. **Acceder:**
   | Servicio | URL |
   |----------|-----|
   | Frontend | `http://localhost` (via Caddy) |
   | API + Swagger | `http://localhost:8000/docs` |
   | PostgreSQL | `localhost:5432` |

### Opcion B: Desarrollo Local

1. **PostgreSQL (solo la BD via Docker):**
   ```bash
   docker compose up postgres -d
   ```

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

### Ejecucion Local

```bash
python -m pytest -v test/
```

> **Nota:** Los endpoints que requieren inferencia del LLM (`/diagnostico`, `/explorar`, `/resena`) necesitan conectividad con Ollama Cloud.

### Integracion Continua (CI/CD)

GitHub Actions ejecuta en cada push o pull request:

1. Levantar PostgreSQL 16 como servicio.
2. Instalar dependencias (Python 3.12 + pytest + httpx + pytest-asyncio).
3. Descargar modelo spaCy.
4. Ejecutar suite completa de 12 tests.
5. Ejecutar smoke tests (health, metadata, validar-texto).

### Deploy Automatico

Al hacer push a `main`, GitHub Actions:
1. Se conecta via SSH a Oracle Cloud.
2. Ejecuta `deploy.sh` que hace pull del código más reciente.
3. Reconstruye y levanta los containers con Docker Compose.

---

## 12. Datos Utilizados

| Fuente de datos | Tipo de datos | Uso dentro del proyecto | Observaciones |
|---|---|---|---|
| Catalogo UGB | Texto estatico | Cruce de variables de afinidad para recomendar la carrera. | Integrado en los prompts del backend. |
| Sesion de Usuario | Texto libre y categorico | Habilidades e intereses ingresados por el aspirante. | Saneados mediante esquemas Pydantic. |
| Historial | PostgreSQL | Sesiones, diagnosticos, exploraciones y resenas. | Persistente y preparado para concurrencia. |

---

## 13. Riesgos Tecnicos y Deuda Tecnica

| Riesgo | Categoria | Probabilidad | Impacto | Mitigacion propuesta |
|---|---|---|---|---|
| *Resuelto:* Acoplamiento | Codigo | Baja | N/A | *Mitigado:* API REST con FastAPI. |
| *Resuelto:* Dependencias | Entorno | Baja | N/A | *Mitigado:* Docker y Docker Compose. |
| *Resuelto:* Perdida de Historial | Datos | Baja | N/A | *Mitigado:* PostgreSQL con ORM SQLAlchemy. |
| *Resuelto:* Sin rate limiting | Seguridad | Media | Alto | *Mitigado:* slowapi con limites por endpoint. |
| *Resuelto:* CORS abierto | Seguridad | Media | Alto | *Mitigado:* Origenes restringidos a produccion. |
| *Resuelto:* Docker como root | Seguridad | Media | Alto | *Mitigado:* Usuario appuser no-root. |
| Dependencia de Ollama Cloud | Despliegue | Aceptada | Medio | La inferencia depende de la conectividad con Ollama Cloud. |

---

## 14. Plan de Mejora por Semana

| Semana | Mejora esperada | Estado |
|---|---|---|
| **Semana 2** | **API inteligente y contratos de entrada/salida (FastAPI)** | **Completado** |
| **Semana 3** | **Pruebas y CI/CD (Validacion de filtros de seguridad de IA)** | **Completado** |
| **Semana 4** | **Contenerizacion y Aislamiento (Docker)** | **Completado** |
| **Semana 5** | **Observabilidad y rendimiento** | **Completado** |
| **Semana 6** | **Frontend React + PostgreSQL + Docker Compose + Documentacion** | **Completado** |

---

## 15. Limitaciones Actuales

- El rendimiento del sistema depende de la conectividad con Ollama Cloud.
- No hay backup automatizado de PostgreSQL.
- No hay automatizacion de rollback (procedimiento manual documentado en `docs/rollback.md`).
- Las sesiones no se persisten en el frontend. Si el usuario cierra el navegador, el flujo se reinicia.
- Sin módulo de cache para resultados frecuentes del LLM.

---

## 16. Cuotas y Costos

| Concepto | Detalle |
|----------|---------|
| **Proveedor** | Ollama Cloud (https://ollama.com) |
| **Modelo** | gemma4:31b |
| **Autenticacion** | API Key via header `Authorization: Bearer` |
| **Costo por request** | Plan Gratis de Ollama Cloud|
| **Manejo de cuota agotada** | La API retorna HTTP 429 con mensaje: "Cuota de API agotada. Verifica el plan en Ollama Cloud e intenta mas tarde." |
| **Proveedor** | Oracle |
| **Servicio** | Maquina Virtual: VM.Standard.E5.Flex|
| **Costo** | $1.55 promedio diario|


**Nota:** Quedarse sin creditos o cuota es una contingencia controlable. La aplicacion maneja el error de forma segura y no bloquea el sistema completo.


---

## 17. Seguridad

| Capa | Implementacion | Estado |
|------|----------------|--------|
| CORS | Origenes restringidos a `gerarditougb.qd.je` + `localhost:5173` | Activo |
| Rate Limiting | slowapi: 10/min validar-texto, 5/min diagnostico/explorar/resena, 20/min metrics | Activo |
| UUID Validation | Session ID debe ser UUID valido (HTTP 400 si no) | Activo |
| Docker Non-Root | Container corre como `appuser`, no `root` | Activo |
| Errores Sanitizados | Mensajes genericos, sin `str(e)` en respuestas | Activo |
| API Key | Header `X-Api-Key` opcional (no activado para app publica) | Configurado |
| SQL Injection | SQLAlchemy ORM (sin queries raw) | Seguro |
| Input Validation | Pydantic con min_length, max_length, Literal, field_validator | Activo |

---

## 18. Evidencias

| Evidencia | Enlace o ubicacion | Descripcion |
|---|---|---|
| Documentacion API | `docs/api.md` | Uso de Swagger UI para pruebas |
| Arquitectura Actual | `docs/arquitectura-actual.md` | Flujo de componentes del sistema |
| Arquitectura Objetivo | `docs/arquitectura-objetivo.md` | Arquitectura de 5 capas implementada |
| Escalabilidad | `docs/escalabilidad.md` | Plan de escalabilidad a corto, mediano y largo plazo |
| Rollback | `docs/rollback.md` | Procedimiento de rollback manual |
| Plan de Contingencia | `docs/plan-contingencia-demo.md` | Riesgos y verificaciones para la demostracion |
| Release Manifest | `release-manifest.yml` | Manifiesto del release v1.0.0 |

---

## 19. Creditos y Referencias

- **LangChain & Ollama Cloud:** Orquestacion de inferencia con Gemma 4 31B (Cloud).
- **spaCy:** Framework de Procesamiento de Lenguaje Natural para extraccion sintactica (modelo `es_core_news_sm`).
- **FastAPI & Pydantic:** Framework web y validacion estricta de datos para la construccion de la API.
- **SQLAlchemy:** ORM para persistencia de datos con PostgreSQL.
- **React + TypeScript + Vite:** Frontend moderno y tipado.
- **Docker:** Plataforma de contenerizacion para aislamiento de servicios.
- **slowapi:** Rate limiting para FastAPI.
- **Caddy:** Reverse proxy con HTTPS automatico.
- **Universidad Gerardo Barrios (UGB):** Catalogo oficial de la oferta academica.
