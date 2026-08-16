# Documentación de la API - Gerardito

Este documento detalla los contratos de comunicación (endpoints), validaciones y respuestas del backend construido con FastAPI para el sistema de orientación vocacional de la UGB.

> **Prefijo base:** Todas las rutas se encuentran bajo `/api/v1/`.

---

## Header Requerido: `X-Session-Id`

Todos los endpoints de datos requieren el header `X-Session-Id` con un UUID que identifica la sesión del usuario. El frontend genera este ID automáticamente al iniciar y lo envía en cada petición.

```
X-Session-Id: 550e8400-e29b-41d4-a716-446655440000
```

---

## 1. Endpoint: Validación de Texto (Fase 1: Recolección)

**Método HTTP:** `POST`  
**Ruta:** `/api/v1/validar-texto`  
**Descripción:** Evalúa el texto ingresado por el usuario aplicando tolerancia fonética extrema y comprensión de jerga tecnológica (Spanglish). Bloquea texto "basura" y, si es válido, extrae el concepto limpio.

### Payload de Entrada (`ValidacionInput`)
```json
{
  "texto": "estremear juegos y jakear",
  "tipo": "habilidad"
}
```

### Respuesta Exitosa (`ValidacionResponse` - 200 OK)
```json
{
  "es_valido": true,
  "mensaje_ui": "Válido",
  "clasificacion": "Creación de Contenido y Ciberseguridad"
}
```

### Respuesta Rechazada (200 OK)
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
**Ruta:** `/api/v1/diagnostico`  
**Descripción:** Motor principal del sistema. Recibe las listas de habilidades e intereses ya validadas y cruza la información con el catálogo oficial de la UGB para generar la matriz de afinidad. **Persiste** la sesión y el diagnóstico en PostgreSQL.

### Payload de Entrada (`PerfilEstudiante`)
```json
{
  "habilidades": ["Creación de Contenido", "Ciberseguridad", "Lógica Matemática"],
  "intereses": ["Desarrollo Web", "Hardware"]
}
```

### Respuesta Exitosa (`DiagnosticoResponse` - 200 OK)
```json
{
  "resultado_markdown": "### 1. Ingeniería en Sistemas y Redes Informáticas (95%)\n\nTu afinidad por la ciberseguridad y el hardware hace que esta sea tu mejor opción..."
}
```

### Persistencia
- Crea un registro en la tabla `sesion` con el `X-Session-Id` y las habilidades/intereses.
- Crea un registro en la tabla `diagnostico` con el resultado markdown y las carreras extraídas.

---

## 3. Endpoint: Exploración de Carrera (Fase 3: Exploración)

**Método HTTP:** `POST`  
**Ruta:** `/api/v1/explorar`  
**Descripción:** Genera la respuesta final detallando la carrera elegida. **Persiste** la exploración en PostgreSQL vinculada al diagnóstico de la sesión.

### Payload de Entrada (`ExploracionInput`)
```json
{
  "carrera": "Ingeniería en Sistemas y Redes Informáticas"
}
```

### Respuesta Exitosa (`ExploracionResponse` - 200 OK)
```json
{
  "respuesta_chat": "¡Excelente elección! La Ingeniería en Sistemas y Redes Informáticas en la UGB te preparará en áreas de ciberseguridad, redes y desarrollo de software..."
}
```

### Persistencia
- Busca el diagnóstico asociado al `X-Session-Id`.
- Crea un registro en la tabla `exploracion` con la carrera, la respuesta del LLM y el ID del diagnóstico.

---

## 4. Endpoint: Evaluación de Reseñas (Fase 4: Feedback)

**Método HTTP:** `POST`  
**Ruta:** `/api/v1/resena`  
**Descripción:** Procesa el feedback del estudiante utilizando un pipeline NLP híbrido. Extrae palabras clave con spaCy y clasifica el sentimiento (POSITIVO, NEGATIVO, NEUTRAL o INVALIDO) con Gemma 4. **Persiste** la reseña en PostgreSQL.

### Payload de Entrada (`ResenaInput`)
```json
{
  "comentario": "no me gusto la respuesta"
}
```

### Respuesta Exitosa (200 OK)
```json
{
  "mensaje": "¡Gracias por tu reseña! Ha sido procesada.",
  "sentimiento": "NEGATIVO",
  "palabras_clave": ["respuesta"]
}
```

### Respuesta de Error 400 (Contenido sin sentido)
```json
{
  "detail": "El comentario no parece válido o no tiene sentido. Intenta de nuevo."
}
```

### Respuesta de Error 422 (Fallo de Validación Pydantic)
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "comentario"],
      "msg": "Value error, El comentario no puede estar vacío o contener solo espacios.",
      "input": "           "
    }
  ]
}
```

### Persistencia
- Crea un registro en la tabla `resena` con el comentario, sentimiento y palabras clave, vinculado al `X-Session-Id`.

---

## 5. Endpoint: Health Check

**Método HTTP:** `GET`  
**Ruta:** `/api/v1/health`  
**Descripción:** Verifica que la API esté en línea. No requiere `X-Session-Id`.

```json
{
  "status": "ok",
  "servicio": "Gerardito API"
}
```

---

## 6. Endpoint: Metadatos del Sistema

**Método HTTP:** `GET`  
**Ruta:** `/api/v1/metadata`  
**Descripción:** Devuelve información técnica de la API. No requiere `X-Session-Id`.

```json
{
  "version": "1.0",
  "proposito": "Sistema de Orientación Vocacional Inteligente UGB",
  "tecnologias": ["FastAPI", "Ollama Cloud (Gemma 4)", "LangChain", "spaCy", "PostgreSQL"],
  "modelo_ia_principal": "gemma4:31b"
}
```

---

## 7. Endpoint: Prueba de LLM

**Método HTTP:** `GET`  
**Ruta:** `/api/v1/prueba-llm`  
**Descripción:** Prueba directa de conexión con Ollama Cloud. No requiere `X-Session-Id`.

```json
{
  "respuesta": "La orientación vocacional es el proceso..."
}
```

---

## 8. Base de Datos (PostgreSQL)

### Esquema de Tablas

| Tabla | Columnas Principales | Relación |
|---|---|---|
| `sesion` | id (UUID PK), habilidades, intereses, timestamps | Raíz |
| `diagnostico` | id, sesion_id (FK), resultado_markdown, carreras_sugeridas | 1:1 con sesion |
| `exploracion` | id, sesion_id (FK), diagnostico_id (FK), carrera, respuesta_llm | 1:N con sesion |
| `resena` | id, sesion_id (FK), comentario, sentimiento, palabras_clave | 1:N con sesion |

### Variables de Entorno Requeridas

```env
DATABASE_URL=postgresql+asyncpg://gerardito:password@localhost:5432/gerardito_db
OLLAMA_HOST=https://ollama.com
MODEL_NAME=gemma4:31b
OLLAMA_API_KEY=tu_api_key
```

---

## 9. Validaciones Aplicadas

1. **Pydantic:** Elimina espacios, rechaza textos vacíos (HTTP 422), valida tipos y longitudes.
2. **Filtro Semántico del LLM:** Few-Shot Prompting que tolera faltas de ortografía pero identifica texto basura (HTTP 400).
3. **Procesamiento Híbrido (spaCy):** Extrae palabras clave después de que el LLM aprueba el sentimiento.

---

## 10. Herramienta de Prueba

Las pruebas se realizaron utilizando la interfaz **Swagger UI** (`http://localhost:8000/docs`) y el conjunto automatizado de `pytest`.
