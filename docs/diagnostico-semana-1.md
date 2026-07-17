# Diagnóstico Técnico Inicial (Semana 1)

## 1. Estado actual del proyecto
El proyecto "Gerardito" se encuentra en una fase de prototipo funcional avanzado (*Proof of Concept*). Actualmente opera bajo una arquitectura monolítica donde la capa de presentación, el manejo de estado y la lógica de inferencia de Inteligencia Artificial conviven en un único script de Python (basado en Streamlit). Aunque es completamente operativo y cumple con los objetivos de negocio (orientación vocacional segura y semántica), carece de la estructuración en capas, persistencia de datos y automatización necesarias para un entorno de producción escalable.

## 2. Partes que funcionan actualmente
- **Interfaz Reactiva:** La captura de datos estructurados (opciones predefinidas) y texto libre a través del frontend funciona correctamente, implementando bloqueos asíncronos (*State Locking*) para evitar condiciones de carrera durante la inferencia.
- **Filtro Semántico (Firewall):** La validación inicial procesa exitosamente la tolerancia ortográfica y bloquea de manera determinista intentos de inyección (*prompt injection*) o lenguaje soez.
- **Motor de Emparejamiento:** El LLM (Llama 3.1) es capaz de recibir el contexto del estudiante junto con el catálogo de la UGB y generar una matriz de afinidad coherente en formato Markdown.
- **Pipeline NLP Híbrido:** El sistema analiza correctamente la reseña final del usuario, combinando la extracción de entidades de `spaCy` con la clasificación de sentimientos (ironía/sarcasmo) del modelo generativo.

## 3. Partes manuales, incompletas o frágiles
- **Acoplamiento UI/Backend (Frágil):** Al depender del ciclo de renderizado de Streamlit (`st.rerun()`), cualquier modificación menor en la interfaz corre el riesgo de reiniciar el estado de la aplicación de forma imprevista, rompiendo la lógica de negocio.
- **Volatilidad de la Información (Incompleto):** No existe integración con motores de bases de datos. El historial de interacción reside en memoria RAM (`session_state`), lo que significa que todos los datos de los aspirantes y métricas de reseñas se pierden irremediablemente al finalizar la sesión del navegador.
- **Catálogo Estático (Incompleto):** La oferta académica de la UGB está incrustada directamente como una variable de cadena de texto (*hardcoded*) en el código fuente, impidiendo actualizaciones dinámicas sin modificar el script.
- **Inicialización (Manual):** La orquestación no está contenerizada. Requiere que un operador inicie los servicios subyacentes por separado.

## 4. Dependencias técnicas principales
- **Lenguaje Base:** Python 3.x
- **Framework Web:** `streamlit`
- **Orquestación IA:** `langchain`, `langchain-ollama`, `langchain-core`
- **Procesamiento de Lenguaje (CPU):** `spacy` (con el corpus lingüístico `es_core_news_sm`).
- **Motor de Inferencia (GPU):** `ollama` instalado en el sistema operativo anfitrión.
- **Hardware Crítico:** Aceleración gráfica dedicada (Ej. NVIDIA RTX 4060 con 8GB VRAM) para soportar el despliegue del modelo con baja latencia y mantener la fluidez conversacional.

## 5. Datos, archivos, servicios o credenciales necesarios
- **Archivos fuente:** `app_vocacional_streamlit.py`.
- **Modelos Locales Requeridos:** - Llama 3.1 (8B parámetros) descargado en el servicio local de Ollama.
  - Modelo `es_core_news_sm` instalado en el entorno de Python.
- **Servicios Externos / Credenciales:** **Ninguno.** Por diseño arquitectónico enfocado en la privacidad de datos (On-Premise), el sistema no requiere claves API (API Keys), tokens de acceso web ni conexión a servicios en la nube (como OpenAI o AWS).

## 6. Cómo se ejecuta actualmente
Para levantar el sistema, se deben ejecutar secuencialmente los siguientes comandos de manera manual:
1. Iniciar el motor de inferencia local en segundo plano (consola independiente): 
   `ollama run llama3.1:8b`
2. Activar el entorno virtual de Python correspondiente:
   `venv\Scripts\activate` (Windows)
3. Levantar la aplicación monolítica:
   `python -m streamlit run app_vocacional_streamlit.py`

## 7. Evidencia de que el prototipo funciona
Las evidencias de operatividad de este diagnóstico inicial residen en:
- **Capturas de Interfaz:** Pantallas del flujo conversacional completo, desde el Paso 1 (recolección) hasta la emisión de la tabla de afinidad y captura de la reseña.

Interfaz de Inicio
![Resultados](/images/imagen1.png)

Diferentes opciones para seleccionar
![Resultados](/images/opcion.png)

Pasatiempos
![Pasatiempo](/images/pasatiempo.png)

Tabla con las carreras recomendadas
![Resultados](/images/resultado.png)

Investigacion a fondo sobre una opcion
![Profundidad en la carrera](/images/profundo.png)

Reseñas
![Reseñas](/images/resene.png)

- **Logs de Consola de Backend:** Registros impresos en la terminal de ejecución de Python durante el Paso 3, donde se evidencia la respuesta del sentimiento validado ("POSITIVO", "NEGATIVO", "NEUTRAL" o "INVALIDO") y el arreglo de palabras clave extraídas sintácticamente por spaCy.

Sentimientos Obtenidos
![Resultados de sentimientos](/images/sentimiento.png)

- **Bloqueos Exitosos:** Pruebas documentadas de rechazo frente a la inserción de texto aleatorio (ej. "asfajfwef").

Bloqueo de Palabras
![Bloqueo](/images/bloqueo.png)