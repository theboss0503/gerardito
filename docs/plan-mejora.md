# Plan de Mejora Continua (Semanas 2 a 6)

## 1. Introducción
Este documento detalla la hoja de ruta técnica para la evolución del sistema "Gerardito". El objetivo principal es refactorizar la arquitectura monolítica actual (Streamlit) hacia una solución distribuida, escalable y persistente. Cada semana abordará un pilar fundamental de la ingeniería de software y MLOps aplicado a Inteligencia Artificial.

---

## Semana 2: API inteligente y contratos de entrada/salida
**Objetivo:** Desacoplar la lógica de negocio y la inferencia de IA de la interfaz gráfica, garantizando la persistencia de los datos.
- **Backend Independiente:** Migrar la orquestación de LangChain, Llama 3.1 y spaCy hacia una API RESTful construida con **FastAPI**.
- **Contratos de Datos:** Definir esquemas estrictos de entrada y salida utilizando `Pydantic` para garantizar que la IA reciba los tipos de datos correctos (ej. validación del perfil del estudiante).
- **Documentación Automática:** Habilitar y configurar Swagger UI (`/docs`) nativo de FastAPI para facilitar la futura integración con React.js.
- **Persistencia:** Integrar **SQLite** mediante un ORM (como SQLAlchemy) para guardar el historial de sesiones y los resultados del análisis de sentimiento.

---

## Semana 3: Pruebas, automatización y CI/CD
**Objetivo:** Garantizar la fiabilidad del motor de Inteligencia Artificial y la estabilidad de la API mediante pruebas automatizadas.
- **Pruebas Unitarias y de Integración:** Escribir *scripts* utilizando el framework `pytest` para evaluar los *endpoints* críticos de la API.
- **Aserciones Semánticas:** Crear pruebas específicas para el "Filtro de Seguridad" de Llama 3.1, asegurando que retorne consistentemente la etiqueta "INVALIDO" frente a simulaciones de inyección de código o lenguaje inapropiado.
- **Automatización Básica:** Configurar un pipeline de ejecución local o integración continua simple (ej. GitHub Actions) que corra las pruebas sobre el código de Python antes de permitir una fusión (*merge*) en la rama principal.

---

## Semana 4: Contenedor o despliegue
**Objetivo:** Estandarizar el entorno de ejecución para evitar el problema de dependencias locales ("funciona en mi máquina").
- **Contenerización del Backend:** Crear un `Dockerfile` optimizado para empaquetar la aplicación de FastAPI, spaCy y sus dependencias (`requirements.txt`).
- **Orquestación Local:** Configurar un archivo `docker-compose.yml` para levantar la API de forma predecible.
- **Estrategia de Hardware (GPU):** Para mitigar la fricción de virtualizar la tarjeta gráfica (RTX 4060) en Docker para Windows, el contenedor de FastAPI se comunicará a través de la red de Docker con el servicio de Ollama, el cual se mantendrá en ejecución nativa en el sistema *Host*.

---

## Semana 5: Observabilidad, rendimiento y escalabilidad
**Objetivo:** Implementar herramientas de monitoreo para medir el comportamiento del modelo de lenguaje en un entorno real.
- **Trazabilidad (Logging):** Reemplazar los comandos `print()` por el módulo `logging` de Python. Registrar sistemáticamente las peticiones HTTP entrantes y las respuestas del LLM.
- **Métricas de Latencia:** Implementar *middleware* en FastAPI para medir y registrar el tiempo exacto que le toma a la GPU procesar cada inferencia de Llama 3.1.
- **Endpoints de Salud:** Crear un endpoint `/health` que reporte en tiempo real si la conexión con la base de datos (SQLite) y el motor de IA (Ollama) están activos y listos para recibir peticiones.

---

## Semana 6: Seguridad, documentación final y defensa técnica
**Objetivo:** Asegurar la aplicación y preparar los artefactos técnicos para la evaluación final del módulo.
- **Seguridad en la API:** Implementar políticas CORS (*Cross-Origin Resource Sharing*) estrictas para que solo el *Frontend* autorizado (React.js) pueda realizar peticiones a la API.
- **Gestión de Secretos:** Migrar cualquier configuración dura (*hardcoded*) hacia un archivo de variables de entorno (`.env`), excluyéndolo del control de versiones mediante `.gitignore`.
- **Cierre Documental:** Actualizar el diagrama de arquitectura final, pulir el README del repositorio y asegurar que el código esté comentado profesionalmente.
- **Preparación de la Defensa:** Ensayar la demostración en vivo del sistema completo (React.js -> FastAPI -> SQLite & Ollama) destacando las métricas de MLOps y los bloqueos de seguridad de la IA.