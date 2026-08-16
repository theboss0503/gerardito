# Gerardito Frontend (React + TypeScript + Vite)

SPA en React.js que consume la API RESTful de Gerardito. Sustituye al prototipo
`legacy.py` (Streamlit), que se mantiene solo como referencia.

## Requisitos

- Node.js 20.19+ / 22.12+
- La API de Gerardito corriendo en `http://localhost:8000`

## Instalación y ejecución

```bash
npm install
npm run dev
```

Por defecto el servidor de desarrollo corre en `http://localhost:5173` y
redirige las peticiones `/api/*` hacia `http://localhost:8000` (proxy de Vite).

Si la API está en otro host, crea un `.env` a partir de `.env.example` y define
`VITE_API_URL`.

## Build de producción

```bash
npm run build
npm run preview
```

## Endpoints consumidos

| Pantalla | Endpoint |
|---|---|
| Validar habilidad/interés personalizada | `POST /api/v1/validar-texto` |
| Generar diagnóstico (tabla de afinidad) | `POST /api/v1/diagnostico` |
| Explorar carrera | `POST /api/v1/explorar` |
| Analizar reseña | `POST /api/v1/resena` |
