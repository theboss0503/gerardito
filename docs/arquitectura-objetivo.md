# Arquitectura Objetivo (Módulo 4)

## 1. Visión General
El objetivo para el final del Módulo 4 es refactorizar el prototipo monolítico actual de "Gerardito" hacia una arquitectura distribuida de 5 capas, orientada a microservicios. Se desacoplará completamente la interfaz gráfica del motor de Inteligencia Artificial mediante una API RESTful, implementando persistencia de datos relacional robusta (SQL Server) y contenerización, garantizando un despliegue estructurado, escalable y seguro.

---

## 2. Separación de Componentes (Arquitectura de 5 Capas)

### 2.1. Interfaz (Frontend)
- **Tecnología:** React.js.
- **Función:** Aplicación de Página Única (SPA) responsable exclusivamente de la presentación visual y la interacción fluida con el estudiante. 
- **Comunicación:** Consumirá los servicios del backend a través de peticiones HTTP (Axios/Fetch), manejando estados locales sin procesar lógica de negocio pesada.

### 2.2. API / Backend (Capa Lógica)
- **Tecnología:** Python con **FastAPI**.
- **Función:** Servidor ágil que recibe las solicitudes de React.js, valida la estructura de los datos de entrada (mediante Pydantic) y orquesta la comunicación entre la base de datos y los modelos de IA.
- **Endpoints Clave:** `/api/diagnostico` (cruce de afinidad), `/api/chat` (exploración), `/api/resena` (análisis de sentimientos).

### 2.3. Servicio IA (Capa Cognitiva)
- **Tecnología:** LangChain, Ollama (Llama 3.1 de 8B parámetros) y spaCy (`es_core_news_sm`).
- **Función:** Aislado detrás de la API, LangChain estructurará los *prompts*. La inferencia pesada (Llama 3.1) se ejecutará en la VRAM de la GPU local para garantizar baja latencia, mientras spaCy procesará la extracción de palabras clave en la CPU.

### 2.4. Datos (Capa de Persistencia)
- **Tecnología:** **SQL Server**.
- **Función:** Implementación de un motor de base de datos relacional cliente-servidor de alto rendimiento. Almacenará el historial de sesiones, los perfiles vocacionales ingresados y los resultados del análisis NLP de las reseñas. Esta arquitectura garantiza el soporte para múltiples conexiones concurrentes durante las pruebas de carga y estrés, evitando los bloqueos de escritura característicos de las bases de datos locales.

### 2.5. Operación y Configuración
- **Tecnología:** Docker, Docker Compose, variables de entorno (`.env`) y librerías de *logging*.
- **Función:** Estandarizar el entorno de desarrollo y producción, registrar la actividad del sistema (errores y tiempos de inferencia) y facilitar un despliegue reproducible.

---

## 3. Plan de Evolución y Mejora Continua

El desarrollo de esta arquitectura se ejecutará de forma iterativa cumpliendo con los hitos del módulo:

### Semana 2: API Inteligente y Base de Datos
- **Acción:** Desarrollar el núcleo del backend migrando la lógica actual a una API REST con FastAPI. Integración del motor relacional SQL Server utilizando un ORM (ej. SQLAlchemy con `pyodbc`) configurado con un *pool* de conexiones para manejar múltiples peticiones simultáneas.
- **Entregable:** Endpoints funcionales documentados automáticamente a través de Swagger UI (`/docs`), capaces de recibir y guardar interacciones JSON de manera persistente.

### Semana 3: Pruebas y Automatización
- **Acción:** Implementar pruebas unitarias y de integración utilizando el framework `pytest`.
- **Entregable:** Batería de pruebas automatizadas validando que los endpoints de la IA respondan con los esquemas correctos y que el filtro de seguridad retorne explícitamente la etiqueta "INVALIDO" frente a inyecciones de *prompts*.

### Semana 4: Contenedor y Despliegue
- **Acción:** Escribir un `Dockerfile` optimizado para el backend (FastAPI) y otro para el frontend (React.js), orquestados mediante `docker-compose.yml`.
- **Entregable:** Entorno de red interno de Docker que comunique la API con la instancia nativa de Ollama en el *host* (aprovechando la GPU dedicada sin fricciones de virtualización).

### Semana 5: Logs, Métricas y Monitoreo
- **Acción:** Configurar el módulo nativo `logging` de Python para auditar el comportamiento de la aplicación en tiempo real.
- **Entregable:** Archivos de *log* que registren peticiones HTTP entrantes, tiempos exactos de latencia del modelo Llama 3.1, y un endpoint de estado (`/health`) para verificar la conectividad con SQL Server y Ollama.

### Semana 6: Seguridad, Documentación Final y Defensa
- **Acción:** Blindar la comunicación de la API.
- **Entregable:** Implementación de políticas CORS restrictivas y variables de configuración externalizadas en un archivo `.env`. Código depurado, repositorios actualizados y demostración en vivo del sistema híbrido funcionando de extremo a extremo.