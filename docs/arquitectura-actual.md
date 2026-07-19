# Arquitectura Actual del Proyecto

## 1. Usuario o Actor Principal
- **Aspirantes de Bachillerato / Estudiantes:** Son los usuarios finales que interactúan con el sistema para recibir orientación vocacional. Introducen datos sobre sus habilidades e intereses y evalúan el resultado final.

## 2. Interfaz o Punto de Entrada (Cliente)
- **Aplicación Web Desacoplada:** El punto de entrada es una interfaz gráfica (actualmente migrando de Streamlit a React) que actúa **exclusivamente como cliente**. Ya no procesa lógica de negocio; su única función es capturar los datos del usuario, enviarlos mediante peticiones HTTP al servidor y renderizar las respuestas recibidas.

## 3. Backend, Script o Servicio Actual (API RESTful)
- **API Independiente con FastAPI:** La lógica de negocio está completamente separada del frontend. El backend opera como un servicio RESTful construido en Python con FastAPI.
- **Validación Estricta:** Se utiliza **Pydantic** para definir esquemas de entrada y salida (`ResenaInput`, `ResenaResponse`). Esto garantiza que los datos vengan limpios y con el formato correcto antes de tocar la inteligencia artificial, devolviendo errores HTTP 422 automáticos si la entrada es inválida.
- **Orquestador:** El backend utiliza endpoints (rutas) para invocar las cadenas de `LangChain`, gestionando la comunicación con el modelo de lenguaje de forma estructurada.

## 4. Componente de IA
- **Motor Generativo (LLM):** Llama 3.1 (8B parámetros) ejecutado de forma 100% local a través del servidor Ollama. Responde a las peticiones de la API para aplicar filtros de seguridad semánticos, generar diagnósticos y detectar sarcasmo/ironía.
- **Motor NLP Clásico:** spaCy (modelo `es_core_news_sm`) ejecutado en el procesador (CPU) para la extracción de entidades, adjetivos y sustantivos durante el análisis de las reseñas de los usuarios.

## 5. Datos Utilizados
- **Memoria Volátil:** Aunque los datos viajan de forma segura a través de JSON, el almacenamiento a largo plazo sigue pendiente. El historial se maneja temporalmente en memoria, por lo que la información se pierde al reiniciar los servicios.
- **Catálogo Institucional:** El catálogo de carreras de la universidad sigue integrado como texto estático dentro de los prompts del backend.

## 6. Servicios Externos
- **Ninguno (Arquitectura On-Premise):** El sistema no consume APIs en la nube (como OpenAI o Google Cloud). Todos los procesos de inferencia matemática se resuelven en el hardware local de la máquina anfitriona (ej. GPU dedicada RTX 4060), garantizando privacidad de datos.

## 7. Flujo Básico de Información
1. El usuario ingresa sus preferencias o reseñas en la interfaz gráfica.
2. El cliente envía un payload JSON mediante una petición HTTP POST al endpoint correspondiente (ej. `/resena`).
3. **Capa de Seguridad (Pydantic):** FastAPI valida el payload. Si viene vacío o corrupto, rechaza la petición inmediatamente con un error 422.
4. Si pasa la validación, FastAPI orquesta el pipeline híbrido: spaCy extrae palabras clave y Llama 3.1 evalúa el contexto/sentimiento. Si el LLM detecta texto sin sentido, el backend lanza un error controlado 400.
5. El backend empaqueta el resultado y lo devuelve al cliente en formato JSON.
6. La interfaz renderiza el resultado final al usuario.

## 8. Dependencias Manuales o Puntos Frágiles
- **Arranque de Múltiples Servicios:** Al estar desacoplado, ahora se requiere levantar dos servicios en consolas separadas: el servidor de Ollama (`ollama run llama3.1:8b`) y el servidor de la API (`uvicorn app.api.main:app`). Si uno falla, el sistema no opera.
- **Pérdida de Datos y Cuellos de Botella:** La ausencia de una base de datos relacional cliente-servidor (como PostgreSQL o SQL Server) impide persistir el registro histórico. Si se somete el sistema actual a pruebas de rendimiento con usuarios simultáneos, la memoria volátil colapsará rápidamente.