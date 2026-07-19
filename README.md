# Gerardito: Sistema de Orientación Vocacional Inteligente UGB

## 1. Información General

**Módulo:** Módulo 4 - Desarrollo de Aplicaciones con IA  
**Semana:** Semana 2 - Desarrollo de API y validación de esquemas  
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
| **Modelo, algoritmo, servicio o técnica** | Llama 3.1 (8B) vía Ollama (Ejecución local en GPU) y spaCy (`es_core_news_sm`). |
| **Datos de entrada** | Perfil en texto libre del estudiante y reseñas de evaluación validados mediante esquemas Pydantic. |
| **Resultado generado por la IA** | Validación de seguridad (SI/NO/INVALIDO), Diagnóstico cruzado (Markdown) y Clasificación de Sentimientos. |
| **Métrica o forma de evaluación, si aplica** | Nivel de precisión en el emparejamiento con el catálogo institucional y contención de Prompt Injections. |
| **Limitaciones actuales** | Alta dependencia de recursos de hardware local (VRAM) para la ejecución rápida del LLM. |

**Explicación breve:**
La IA actúa como el motor central en tres fases operativas: primero como un "firewall cognitivo" que valida la coherencia de la entrada del estudiante; segundo, como un sistema experto que inyecta el catálogo de la UGB en su contexto para razonar la mejor opción de carrera; y tercero, mediante un enfoque híbrido (LLM + spaCy) que analiza semántica y sintácticamente las reseñas finales a través de una API RESTful.

---

## 6. Estado Actual del Proyecto

### Funcionalidades que ya funcionan
- **Backend API:** Separación exitosa de la lógica de negocio mediante una API RESTful con FastAPI.
- **Validación Estricta:** Implementación de esquemas Pydantic (`ResenaInput`, `ResenaResponse`) para sanear datos y manejar errores (HTTP 400 y 422).
- Filtro semántico de seguridad funcional (tolera ortografía, bloquea insultos y texto vacío/basura).
- Motor de emparejamiento de carreras y generador de matrices de afinidad conectado a Llama 3.1 local.
- Pipeline de análisis de sentimientos híbrido (detección de sarcasmo y extracción de palabras clave) operando vía endpoints.

### Funcionalidades incompletas o pendientes
- Integración completa del frontend (React.js/Streamlit) con los nuevos endpoints de FastAPI.
- Implementación de una base de datos persistente (transición de memoria a SQLite).
- Contenerización y estructuración de despliegue (Docker/MLOps) para aislar los entornos.

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
| Backend / API | API RESTful construida con FastAPI y validación Pydantic. | Desacoplado y Funcional |
| Lógica Principal | Orquestación de LangChain y pipeline NLP enrutados en endpoints HTTP. | Integrado en API |
| Interfaz | Cliente (React) que consume los endpoints. | En proceso de migración |
| Componente IA | Llama 3.1 orquestado por Ollama (Hardware GPU local) y spaCy (CPU). | Operativo |
| Datos | Manejo de sesión temporal, pendiente de migración a DB. | Volátil / Sin persistencia |
| Servicios externos | Ninguno. Arquitectura 100% On-Premise. | Cumple criterios de privacidad |

---

## 8. Arquitectura Objetivo

**Enlace a documento detallado:** `docs/arquitectura-objetivo.md`

Para el final del Módulo 4, el proyecto transicionará completamente hacia una arquitectura de 5 capas orientada a microservicios:

- **Interfaz:** Single Page Application (SPA) en **React.js** consumiendo la API.
- **API / Backend:** API RESTful robusta y documentada utilizando **FastAPI** (Ya implementado).
- **Servicio IA:** Orquestación de Llama 3.1 y spaCy protegida por validadores Pydantic (Ya implementado).
- **Datos:** Implementación de persistencia relacional robusta utilizando **PostgreSQL**, lo que permitirá soportar alta concurrencia de usuarios simultáneos durante las pruebas de carga y rendimiento, registrando sesiones, recomendaciones y reseñas sin cuellos de botella.
- **Operación:** Contenerización de los servicios (Frontend y Backend) utilizando **Docker**, aislando el entorno de ejecución.

---

## 9. Estructura del Repositorio

```text
gerardito-ugb/
  ├── app/                  # Código principal del backend y frontend
  │   ├── api/              # Endpoints de FastAPI (ej. main.py, routers)
  │   ├── schemas/          # Modelos de validación Pydantic
  │   ├── frontend/         # Componentes de UI (Streamlit/React)
  │   └── services/         # Lógica de LangChain y spaCy
  ├── data/                 # Base de datos local (próximamente SQLite)
  ├── docs/                 # Documentación técnica y diagramas
  ├── tests/                # Pruebas unitarias
  ├── README.md             # Este archivo
  ├── requirements.txt      # Dependencias de Python (incluye fastapi, uvicorn, pydantic)
  └── .env.example          # Plantilla de variables de entorno
```

## 10. Instalación y Ejecución

*(Instrucciones correspondientes al prototipo actual en Streamlit)*

### Requisitos previos
- Python 3.10+
- Ollama instalado localmente con el modelo `llama3.1:8b` descargado.

### Instalación
```bash
pip install -r requirements.txt
python -m spacy download es_core_news_sm

# Iniciar el motor de IA en una consola:
ollama run llama3.1:8b

# En otra consola, levantar la aplicación:
uvicorn app.api.main:app --reload
```
## 11. Datos Utilizados

Describan los datos que usa la aplicación.

| Fuente de datos | Tipo de datos | Uso dentro del proyecto | Observaciones |
|---|---|---|---|
| Catálogo UGB | Texto estático | Cruce de variables de afinidad para recomendar la carrera. | Es la fuente oficial de la institución. |
| Sesión de Usuario | Texto libre y categórico | Habilidades e intereses ingresados por el aspirante. | Saneados mediante esquemas estrictos de Pydantic. |
| Historial (Objetivo) | Tablas relacionales | Almacenamiento de recomendaciones y análisis de sentimientos. | Se utilizará PostgreSQL para soportar escrituras concurrentes en pruebas de estrés. |

**Consideraciones:**

- ¿Los datos son públicos, privados o simulados? El catálogo de la UGB es público. Los datos ingresados por los usuarios serán tratados como privados.
- ¿Contienen información sensible? No contienen información médica o financiera, pero la preferencia vocacional y los perfiles de los aspirantes se tratarán con confidencialidad.
- ¿Requieren limpieza o validación? Sí, el texto libre del usuario requiere validación semántica (se aplica tolerancia ortográfica y un filtro de lenguaje inapropiado previo a la inferencia).
- ¿Existen limitaciones de calidad? Actualmente, la calidad del diagnóstico depende de la claridad con la que el estudiante exprese sus habilidades en el formulario.
- El texto libre del usuario se somete a validación de tipos, limpieza de espacios y filtros de longitud mediante FastAPI antes de llegar al motor de IA, previniendo errores de procesamiento y ataques básicos.
---

## 12. Riesgos Técnicos y Deuda Técnica

Identifiquen riesgos reales del proyecto.

| Riesgo | Categoría | Probabilidad | Impacto | Mitigación propuesta |
|---|---|---|---|---|
| Limitación de Hardware | Despliegue | Alta | Alto | Mantener el modelo cuantizado a 8B e implementar el parámetro `keep_alive` en Ollama para fijarlo en VRAM. |
| *Resuelto:* Acoplamiento | Código | Baja | N/A | *Mitigado:* La lógica ya fue extraída a una API REST con FastAPI. |
| Pérdida de Historial | Datos | Media | Bajo | Transicionar hacia una base de datos cliente-servidor (PostgreSQL) preparada para alta concurrencia. |
---

## 13. Plan de Mejora por Semana

Indiquen cómo evolucionará el proyecto durante el módulo.

| Semana | Mejora esperada | Evidencia esperada |
|---|---|---|
| **Semana 2** | **API inteligente y contratos de entrada/salida (FastAPI)** | **Endpoint funcional, Swagger UI, validación Pydantic (Completado)** |
| Semana 3 | Pruebas y CI/CD (Validación de filtros de seguridad de IA) | Tests (pytest), pipeline, evidencia de ejecución |
| Semana 4 | Contenedor o despliegue (Aislamiento de API y UI) | Dockerfile, servicio desplegado o entorno simulado |
| Semana 5 | Observabilidad y rendimiento (Medición de latencia de Ollama) | Logs, métricas, prueba de carga |
| Semana 6 | Seguridad, documentación y defensa final (React conectado y .env) | README final, demo, presentación |

---

## 14. Limitaciones Actuales

Describan con honestidad las limitaciones del prototipo.

- El historial de interacciones y las reseñas procesadas aún no persisten permanentemente, a la espera de la integración del módulo de base de datos relacional.
- La comunicación entre el frontend actualizado y la nueva API aún está en fase de acoplamiento.
- El rendimiento del sistema depende 100% de los recursos gráficos (VRAM) de la máquina anfitriona que ejecuta Ollama.

---

## 15. Evidencias

Agreguen enlaces o referencias a evidencias del proyecto.

Validacion de texto para habilidades e intereses.

![Validacion](/images/validacion.png)

Respuesta de la API con el diagnostico

![Resultados](/images/diagnostico.png)

Evaluacion de reseña

![Resultados](/images/resenia.png)

| Evidencia | Enlace o ubicación | Descripción |
|---|---|---|
| Documentación API | `docs/api.md` | Uso de Interfaz Swagger para pruebas |
| Diagrama | `docs/arquitectura-actual.md` | Flujo de componentes y lógica actual del sistema. |

---

## 16. Créditos y Referencias

Incluyan librerías, modelos, datasets, documentación o servicios utilizados.

- **LangChain & Ollama:** Orquestación de inferencia local con Llama 3.1 (8B).
- **spaCy:** Framework de Procesamiento de Lenguaje Natural para extracción sintáctica (modelo `es_core_news_sm`).
- **FastAPI & Pydantic:** Framework web y validación estricta de datos para la construcción de la API.
- **Universidad Gerardo Barrios (UGB):** Catálogo oficial de la oferta académica.

---

