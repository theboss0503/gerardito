# Documentación de la API - Gerardito

Este documento detalla los contratos de comunicación (endpoints), validaciones y respuestas del backend construido con FastAPI para el sistema de orientación vocacional de la UGB.

---
## 1. Endpoint: Validación de Texto (Fase 1: Recolección)

**Método HTTP:** `POST`  
**Ruta:** `/validar-texto`  
**Descripción:** Evalúa el texto ingresado por el usuario aplicando tolerancia fonética extrema y comprensión de jerga tecnológica (Spanglish). Bloquea texto "basura" y, si es válido, extrae el concepto limpio.

### Payload de Entrada (`ValidacionInput`)
El endpoint recibe el texto y el tipo de dato que se está evaluando (ej. "habilidad" o "interés").

```json
{
  "texto": "estremear juegos y jakear",
  "tipo": "habilidad"
}
```

### Respuesta Exitosa (`ValidacionResponse` - 200 OK)
Devuelve el estado de validación positivo, un mensaje para la UI y el concepto limpio (clasificación).

```json
{
  "es_valido": true,
  "mensaje_ui": "Válido",
  "clasificacion": "Creación de Contenido y Ciberseguridad"
}
```

### Respuesta Rechazada (200 OK)
Si el texto es inválido o incomprensible, devuelve `es_valido: false` y un mensaje de error para que el frontend lo muestre sin romper la aplicación.

```json
{
  "es_valido": false,
  "mensaje_ui": "El texto ingresado no es válido para una habilidad. Por favor, ingresa datos reales.",
  "clasificacion": null
}
```

---

## 2. Endpoint: Diagnóstico Vocacional (Fase 2: Afinidad)

**Método HTTP:** `POST`  
**Ruta:** `/diagnostico`  
**Descripción:** Motor principal del sistema. Recibe las listas de habilidades e intereses ya validadas y limpiezas (provenientes de la Fase 1) y cruza la información con el catálogo oficial de la UGB para generar la matriz de afinidad.

### Payload de Entrada (`PerfilEstudiante`)
El endpoint espera un JSON con las listas de conceptos limpios del estudiante.

```json
{
  "habilidades": ["Creación de Contenido", "Ciberseguridad", "Lógica Matemática"],
  "intereses": ["Desarrollo Web", "Hardware"]
}
```

### Respuesta Exitosa (`DiagnosticoResponse` - 200 OK)
Devuelve el análisis generado por el LLM formateado en Markdown, listo para ser renderizado por React.

```json
{
  "resultado_markdown": "### 1. Ingeniería en Sistemas y Redes Informáticas (95%)\n\nTu afinidad por la ciberseguridad y el hardware hace que esta sea tu mejor opción..."
}
```

---

## 3. Endpoint: Exploración de Carrera (Fase 3: Exploración)

**Método HTTP:** `POST`  
**Ruta:** `/explorar`  
**Descripción:** Genera la respuesta final detallando la carrera elegida. Permite que el sistema actúe como un orientador enfocado en una carrera en específico.

### Payload de Entrada (`ExploracionInput`)
Recibe únicamente el nombre de la carrera que el usuario desea explorar a fondo.

```json
{
  "carrera": "Ingeniería en Sistemas y Redes Informáticas"
}
```

### Respuesta Exitosa (`ExploracionResponse` - 200 OK)
Devuelve la información detallada de la carrera en formato de texto o Markdown.

```json
{
  "respuesta_chat": "¡Excelente elección! La Ingeniería en Sistemas y Redes Informáticas en la UGB te preparará en áreas de ciberseguridad, redes y desarrollo de software..."
}
```
---

## 4. Endpoint: Evaluación de Reseñas

**Método HTTP:** `POST`  
**Ruta:** `/resena`  
**Descripción:** Procesa el feedback del estudiante utilizando un pipeline NLP híbrido. Extrae palabras clave utilizando spaCy y clasifica el sentimiento del comentario (POSITIVO, NEGATIVO, NEUTRAL o INVALIDO) utilizando Llama 3.1. 

### Payload de Entrada (Request Body)
El endpoint espera un objeto JSON validado por el esquema `ResenaInput`.

```json
{
  "comentario": "no me gusto la respuesta"
}
```

### Respuesta Exitosa (200 OK)
Devuelve un objeto JSON validado por el esquema `ResenaResponse` cuando el comentario tiene sentido y fue procesado correctamente.

```json
{
  "mensaje": "¡Gracias por tu reseña! Ha sido procesada.",
  "sentimiento": "NEGATIVO",
  "palabras_clave": [
    "respuesta"
  ]
}
```

### Respuestas de Error Controlado

**Error 400 - Bad Request (Contenido sin sentido):**
Se dispara cuando el modelo de IA clasifica el texto como `INVALIDO` (ej. "asdfg" o caracteres al azar).

```json
{
  "detail": "El comentario no parece válido o no tiene sentido. Intenta de nuevo."
}
```

**Error 422 - Unprocessable Entity (Fallo de Validación):**
Se dispara automáticamente por Pydantic antes de tocar el modelo de IA, cuando el usuario envía un texto vacío o puros espacios en blanco.

```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": [
        "body",
        "comentario"
      ],
      "msg": "Value error, El comentario no puede estar vacío o contener solo espacios.",
      "input": "           ",
      "ctx": {
        "error": {}
      }
    }
  ]
}
```
---

## 5. Endpoint: Health Check (Estado del Sistema)

**Método HTTP:** `GET`  
**Ruta:** `/health`  
**Descripción:** Verifica que la API de Gerardito esté en línea y respondiendo. Este endpoint es fundamental para la infraestructura operativa, ya que permite que Docker o cualquier orquestador (balanceador de carga) compruebe periódicamente si el contenedor está saludable.

### Respuesta Exitosa (200 OK)
Devuelve un JSON estático confirmando que el servicio está activo.

```json
{
  "status": "ok",
  "servicio": "Gerardito API"
}
```

---

## 6. Endpoint: Metadatos del Sistema

**Método HTTP:** `GET`  
**Ruta:** `/metadata`  
**Descripción:** Devuelve la información técnica de la versión actual de la API, el propósito del sistema y la pila tecnológica subyacente. Útil para auditorías rápidas y verificación del entorno desplegado.

### Respuesta Exitosa (200 OK)
Devuelve un objeto JSON con los detalles de la versión y las herramientas en uso.

```json
{
  "version": "1.0",
  "proposito": "Sistema de Orientación Vocacional Inteligente UGB",
  "tecnologias": [
    "FastAPI",
    "Ollama",
    "LangChain",
    "spaCy"
  ],
  "modelo_ia_principal": "llama3.1:8b"
}
```

### Validaciones Aplicadas y Procesamiento
1. **Limpieza de Pydantic (`strip_whitespace=True`):** Elimina automáticamente los espacios en blanco al inicio y al final del comentario.
2. **Límites de Longitud (`min_length=1`, `max_length=500`):** Garantiza que el usuario no envíe un string vacío (lanzando HTTP 422) y establece un límite máximo de caracteres para prevenir ataques de saturación de contexto (VRAM) en el LLM.
3. **Filtro Semántico del LLM:** Mediante *Few-Shot Prompting*, el LLM tolera faltas de ortografía (ej. "gusto" en lugar de "gustó"), pero identifica texto basura o incomprensible para interceptarlo y lanzar un error controlado HTTP 400.
4. **Procesamiento Híbrido (spaCy):** Una vez que el LLM aprueba y clasifica el sentimiento del texto, el pipeline utiliza spaCy en la CPU para extraer las palabras clave del comentario, optimizando los recursos del sistema.

### Herramienta usada para probar
Las pruebas de los endpoints y validaciones se realizaron utilizando la interfaz interactiva **Swagger UI** provista nativamente por FastAPI (`http://127.0.0.1:8000/docs`).

### Evidencias de Prueba


**1. Prueba Exitosa (200 OK):**  
![Prueba Exitosa](/images/validar-texto.png)  
*Descripción: Captura de Swagger UI mostrando la validacion de texto de habilidaades personalizadas.*

**2. Prueba Exitosa (200 OK):**  
![Prueba Exitosa](/images/diagnostico.png)  
*Descripción: Captura de Swagger UI mostrando el resultado del diagnostico de carreras.*

**3. Prueba Exitosa (200 OK):**  
![Prueba Exitosa](/images/explorar.png)  
*Descripción: Captura de Swagger UI mostrando el resultado de la exploracion de carreras.*

**4. Prueba Exitosa (200 OK):**  
![Prueba Exitosa](/images/resenia-pos.png)  
*Descripción: Captura de Swagger UI mostrando la extracción de palabras clave y clasificación correcta del sentimiento.*

**5. Prueba de Error Controlado (400 Bad Request):**  
![Error 400](/images/resenia-error400.png)  
*Descripción: Captura mostrando el rechazo de la petición cuando el LLM detecta texto sin sentido.*

**6. Prueba de Validación Pydantic (422 Unprocessable Entity):**  
![Error 422](/images/resenia-error422.png)  
*Descripción: Captura mostrando la intercepción de Pydantic al enviar espacios en blanco.*

**7. Prueba Exitosa (200 OK):**  
![Prueba Exitosa](/images/health.png)  
*Descripción: Captura de Swagger UI mostrando la informacion del healt.*

**7. Prueba Exitosa (200 OK):**  
![Prueba Exitosa](/images/metadata.png)  
*Descripción: Captura de Swagger UI mostrando la informacion proporcionada por el metadata.*