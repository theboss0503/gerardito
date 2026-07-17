# Arquitectura Actual del Proyecto

## 1. Usuario o Actor Principal
- **Aspirantes de Bachillerato / Estudiantes:** Son los usuarios finales que interactúan con el sistema para recibir orientación vocacional. Introducen datos sobre sus habilidades e intereses y evalúan el resultado final.

## 2. Interfaz o Punto de Entrada
- **Aplicación Web (Streamlit):** El punto de entrada actual es una interfaz gráfica web generada íntegramente mediante el framework Streamlit en Python. Los usuarios interactúan a través de formularios dinámicos (multiselect, cajas de texto libre) y un entorno de chat simulado (`st.chat_message`).

## 3. Backend, Script o Servicio Actual
- **Script Monolítico en Python:** No existe una separación real entre el frontend y el backend. Toda la lógica de negocio, validaciones, control de estado y orquestación de la inteligencia artificial residen en un único script principal (`app_vocacional_streamlit.py`). 
- **Orquestador:** Se utiliza la librería `LangChain` para estructurar la comunicación con el modelo de lenguaje (roles de System, Human y AI).

## 4. Componente de IA
- **Motor Generativo (LLM):** Llama 3.1 (8B parámetros) ejecutado de forma 100% local a través del servidor Ollama. Se encarga del filtro de seguridad semántico, la generación del diagnóstico vocacional cruzado y la detección de sarcasmo/ironía.
- **Motor NLP Clásico:** spaCy (modelo `es_core_news_sm`) ejecutado en el procesador (CPU) para la extracción de entidades, adjetivos y sustantivos durante el análisis de las reseñas de los usuarios.

## 5. Datos Utilizados
- **Memoria Volátil:** El historial de la conversación y las selecciones temporales del usuario se almacenan en el `session_state` de Streamlit. Al recargar la página, la información se destruye.
- **Catálogo Institucional:** El catálogo de carreras de la universidad está integrado como texto estático (hardcoded) dentro del script de Python, no se consulta desde una base de datos.

## 6. Servicios Externos
- **Ninguno (Arquitectura On-Premise):** El prototipo actual no consume APIs en la nube (como OpenAI o Google Cloud). Todos los procesos de inferencia matemática se resuelven en el hardware local de la máquina anfitriona (GPU dedicada RTX 4060).

## 7. Flujo Básico de Información
1. El usuario ingresa sus preferencias a través de los componentes visuales de Streamlit.
2. Streamlit bloquea la interfaz (State Locking) y envía el texto de entrada al LLM (Llama 3.1) para una validación de seguridad (Zero-Shot Classification).
3. Si la entrada es válida, el script en Python ensambla un prompt combinando el perfil del usuario con el catálogo estático de carreras.
4. Ollama procesa la inferencia en la VRAM de la GPU y retorna una tabla Markdown.
5. El usuario explora una opción específica en un chat guiado y proporciona una reseña textual.
6. La reseña pasa por un pipeline híbrido: spaCy extrae componentes sintácticos (CPU) y Llama evalúa el sentimiento (GPU), mostrando el resultado en los logs internos.

## 8. Dependencias Manuales o Puntos Frágiles
- **Acoplamiento Fuerte:** Al estar la UI y la lógica de inferencia en el mismo archivo, cualquier cambio en la interfaz puede romper el flujo de datos hacia el modelo.
- **Inicialización Manual:** Se requiere encender el servidor de Ollama manualmente (`ollama run llama3.1:8b`) antes de levantar la aplicación de Streamlit. Si el servicio no está corriendo, la aplicación colapsa sin un manejo de errores robusto.
- **Pérdida de Datos:** La ausencia de una base de datos relacional impide guardar el registro histórico de los aspirantes y las métricas de rendimiento del orientador vocacional.