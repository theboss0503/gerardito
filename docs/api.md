# Documentación de la API - Gerardito

Este documento detalla los contratos de comunicación (endpoints), validaciones y respuestas del backend construido con FastAPI para el sistema de orientación vocacional de la UGB.

---

## 1. Endpoint: Evaluación de Reseñas

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

### Validaciones Aplicadas
1. **Limpieza de Pydantic (`strip_whitespace=True`):** Elimina automáticamente los espacios en blanco al inicio y al final del comentario.
2. **Longitud mínima (`min_length=1`):** Garantiza que el usuario no envíe un string vacío, bloqueando la petición con un error HTTP 422.
3. **Filtro Semántico del LLM:** Mediante *Few-Shot Prompting*, el LLM tolera faltas de ortografía (ej. "gusto" en lugar de "gustó"), pero identifica texto basura para lanzar un error HTTP 400.

### Herramienta usada para probar
Las pruebas de los endpoints y validaciones se realizaron utilizando la interfaz interactiva **Swagger UI** provista nativamente por FastAPI (`http://127.0.0.1:8000/docs`).

### Evidencias de Prueba

**1. Prueba Exitosa (200 OK):**  
![Prueba Exitosa](/images/resenia-pos.png)  
*Descripción: Captura de Swagger UI mostrando la extracción de palabras clave y clasificación correcta del sentimiento.*

**2. Prueba de Error Controlado (400 Bad Request):**  
![Error 400](/images/resenia-error400.png)  
*Descripción: Captura mostrando el rechazo de la petición cuando el LLM detecta texto sin sentido.*

**3. Prueba de Validación Pydantic (422 Unprocessable Entity):**  
![Error 422](/images/resenia-error422.png)  
*Descripción: Captura mostrando la intercepción de Pydantic al enviar espacios en blanco.*