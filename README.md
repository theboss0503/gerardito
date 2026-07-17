# Gerardito: Sistema de Orientación Vocacional Inteligente UGB

## 1. Información General

**Módulo:** Módulo 4 - Desarrollo de Aplicaciones con IA  
**Semana:** Semana 1 - Diagnóstico y arquitectura inicial  
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
| **Datos de entrada** | Perfil en texto libre del estudiante y reseñas de evaluación. |
| **Resultado generado por la IA** | Validación de seguridad (SI/NO/INVALIDO), Diagnóstico cruzado (Markdown) y Clasificación de Sentimientos. |
| **Métrica o forma de evaluación, si aplica** | Nivel de precisión en el emparejamiento con el catálogo institucional y contención de Prompt Injections. |
| **Limitaciones actuales** | Fuerte acoplamiento entre la interfaz (Streamlit) y la lógica de inferencia del LLM en el mismo entorno. |

**Explicación breve:**
La IA actúa como el motor central en tres fases operativas: primero como un "firewall cognitivo" que valida la coherencia de la entrada del estudiante; segundo, como un sistema experto que inyecta el catálogo de la UGB en su contexto para razonar la mejor opción de carrera; y tercero, mediante un enfoque híbrido (LLM + spaCy) que analiza semántica y sintácticamente las reseñas finales.

---

## 6. Estado Actual del Proyecto

### Funcionalidades que ya funcionan
- Interfaz de usuario interactiva y bloqueos de estado síncrono (State Locking) implementados en Streamlit.
- Filtro semántico de seguridad funcional (tolera ortografía, bloquea insultos y texto basura).
- Motor de emparejamiento de carreras y generador de matrices de afinidad conectado a Llama 3.1 local.
- Pipeline de análisis de sentimientos híbrido (detección de sarcasmo y extracción de palabras clave).

### Funcionalidades incompletas o pendientes
- Separación de la interfaz gráfica y la lógica de negocio en una API REST independiente.
- Implementación de una base de datos persistente (actualmente se usa memoria volátil `session_state`).
- Contenerización y estructuración de despliegue (Docker/MLOps) para aislar los entornos.

### Evidencias actuales
Interfaz Inicial
![Interfaz Inicial](/images/imagen1.png)

Inicio en Consola
![Descripción de la imagen](/images/consola1.png)

Multiples Opciones
![Descripción de la imagen](/images/opcion.png)

---

## 7. Arquitectura Actual

**Enlace a documento detallado:** `docs/arquitectura-actual.md`

| Componente | Descripción | Estado actual |
|---|---|---|
| Interfaz | Construida en Python con Streamlit, altamente acoplada a la lógica. | Funcional monolítico |
| Backend / lógica principal | Scripts de orquestación (LangChain) dentro del mismo archivo de UI. | Funcional pero acoplado |
| Componente IA | Llama 3.1 orquestado por Ollama (Hardware GPU local) y spaCy (CPU). | Operativo |
| Datos | Manejo de historial temporal mediante variables de `session_state`. | Volátil / Sin persistencia |
| Servicios externos | Ninguno. Arquitectura 100% On-Premise. | Cumple criterios de privacidad |
| Configuración | Inicialización de procesos manual y scripts locales. | Pendiente de automatizar |

Diagrama de la Arquitectura Actual

![Diagrama Actual](/images/diagrama1.png)

---

## 8. Arquitectura Objetivo

**Enlace a documento detallado:** `docs/arquitectura-objetivo.md`

Para el final del Módulo 4, el proyecto transicionará hacia una arquitectura de 5 capas orientada a microservicios:

- **Interfaz:** Migración a una Single Page Application (SPA) en **React.js**.
- **API / Backend:** Construcción de una API RESTful rápida e independiente utilizando **FastAPI** en Python.
- **Servicio IA:** El backend orquestará a Llama 3.1 y spaCy para responder a las peticiones HTTP del frontend.
- **Datos:** Implementación de persistencia relacional ligera utilizando **SQLite**, permitiendo registrar las sesiones, recomendaciones y reseñas sin necesidad de configurar un servidor pesado.
- **Operación:** Contenerización de los servicios (Frontend y Backend) utilizando **Docker**, aislando el entorno de ejecución.

Diagrama de la Arquitectura Objetivo

![Diagrama Actual](/images/diagrama2.png)

---

## 9. Estructura del Repositorio

```text
gerardito-ugb/
  ├── app/                  # Código principal del backend y frontend
  │   ├── api/              # Endpoints de FastAPI
  │   ├── frontend/         # Componentes de React.js
  │   └── services/         # Lógica de LangChain y spaCy
  ├── data/                 # Base de datos local (ej. gerardito.db)
  ├── docs/                 # Documentación técnica y diagramas
  ├── tests/                # Pruebas unitarias
  ├── README.md             # Este archivo
  ├── requirements.txt      # Dependencias de Python
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
python -m streamlit run app_vocacional_streamlit.py
```
## 11. Datos Utilizados

Describan los datos que usa la aplicación.

| Fuente de datos | Tipo de datos | Uso dentro del proyecto | Observaciones |
|---|---|---|---|
| Catálogo UGB | Texto estático | Cruce de variables de afinidad para recomendar la carrera. | Es la fuente oficial de la institución. |
| Sesión de Usuario | Texto libre y categórico | Habilidades e intereses ingresados por el aspirante. | Se utiliza como contexto de entrada para el LLM. |
| Historial (Objetivo) | Tablas SQLite | Almacenamiento de recomendaciones y análisis de sentimientos. | Permitirá auditorías y analíticas en el futuro. |

**Consideraciones:**

- ¿Los datos son públicos, privados o simulados? El catálogo de la UGB es público. Los datos ingresados por los usuarios serán tratados como privados.
- ¿Contienen información sensible? No contienen información médica o financiera, pero la preferencia vocacional y los perfiles de los aspirantes se tratarán con confidencialidad.
- ¿Requieren limpieza o validación? Sí, el texto libre del usuario requiere validación semántica (se aplica tolerancia ortográfica y un filtro de lenguaje inapropiado previo a la inferencia).
- ¿Existen limitaciones de calidad? Actualmente, la calidad del diagnóstico depende de la claridad con la que el estudiante exprese sus habilidades en el formulario.

---

## 12. Riesgos Técnicos y Deuda Técnica

Identifiquen riesgos reales del proyecto.

| Riesgo | Categoría | Probabilidad | Impacto | Mitigación propuesta |
|---|---|---|---|---|
| Limitación de Hardware | Despliegue | Alta | Alto | Mantener el modelo cuantizado a 8B e implementar el parámetro `keep_alive` en Ollama para fijarlo en VRAM. |
| Acoplamiento Fuerte | Código | Alta | Medio | Desacoplar urgentemente la UI (Streamlit) creando una API con FastAPI (Semana 2). |
| Pérdida de Historial | Datos | Media | Bajo | Transicionar del `session_state` volátil hacia una base de datos local SQLite (Semana 2). |

---

## 13. Plan de Mejora por Semana

Indiquen cómo evolucionará el proyecto durante el módulo.

| Semana | Mejora esperada | Evidencia esperada |
|---|---|---|
| Semana 2 | API inteligente y contratos de entrada/salida (FastAPI y SQLite) | Endpoint, Swagger, prueba manual o automatizada |
| Semana 3 | Pruebas y CI/CD (Validación de filtros de seguridad de IA) | Tests (pytest), pipeline, evidencia de ejecución |
| Semana 4 | Contenedor o despliegue (Aislamiento de API y UI) | Dockerfile, servicio desplegado o entorno simulado |
| Semana 5 | Observabilidad y rendimiento (Medición de latencia de Ollama) | Logs, métricas, prueba de carga |
| Semana 6 | Seguridad, documentación y defensa final (React conectado y .env) | README final, demo, presentación |

---

## 14. Limitaciones Actuales

Describan con honestidad las limitaciones del prototipo.

- La interfaz gráfica (Streamlit) y la lógica de inferencia de la IA están fuertemente acopladas en un solo archivo, impidiendo la escalabilidad.
- El historial de interacciones se guarda temporalmente en la memoria volátil del navegador y se pierde al recargar la página; no hay conexión a base de datos.
- El rendimiento del sistema depende 100% de los recursos gráficos (VRAM) de la máquina anfitriona que ejecuta Ollama, lo que puede causar bloqueos si no hay suficiente memoria disponible.

---

## 15. Evidencias

Agreguen enlaces o referencias a evidencias del proyecto.

Bloqueo de texto inapropiado o basura
![Texto Inapropiado](/images/texto.png)

Tabla con resultados
![Resultados](/images/resultado.png)

Evaluacion de reseña
![Resultados](/images/eva.png)

| Evidencia | Enlace o ubicación | Descripción |
|---|---|---|
| Notebook / Script | `app_vocacional_streamlit.py` | Archivo principal actual con la orquestación funcional. |
| Endpoint probado | N/A (Semana 2) | Se documentarán los endpoints de FastAPI en la siguiente etapa. |
| Diagrama | `docs/arquitectura-actual.md` | Flujo de componentes y lógica actual del sistema. |

---

## 16. Créditos y Referencias

Incluyan librerías, modelos, datasets, documentación o servicios utilizados.

- **LangChain & Ollama:** Orquestación de inferencia local con Llama 3.1 (8B).
- **spaCy:** Framework de Procesamiento de Lenguaje Natural para extracción sintáctica (modelo `es_core_news_sm`).
- **Streamlit:** Framework utilizado para la construcción rápida del prototipo actual.
- **Universidad Gerardo Barrios (UGB):** Catálogo oficial de la oferta académica.

---

## 17. Checklist de Revisión

Antes de entregar, verifiquen:

- [x] El problema está claramente descrito.
- [x] Se explica quién usará o se beneficiará de la aplicación.
- [x] Se identifica dónde está la IA.
- [x] Se describen entradas y salidas.
- [x] Se documenta el estado actual del proyecto.
- [x] Se incluye arquitectura actual.
- [x] Se incluye arquitectura objetivo.
- [x] Se explica cómo ejecutar el proyecto.
- [x] Se identifican riesgos técnicos.
- [x] Se presenta plan de mejora por semana.
- [x] No se incluyen claves, contraseñas ni tokens privados.