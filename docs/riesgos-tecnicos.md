# Registro de Riesgos Técnicos y Deuda Técnica

## 1. Introducción
Este documento identifica, clasifica y evalúa los riesgos técnicos y la deuda técnica del proyecto "Gerardito". La mayoría de los riesgos iniciales han sido mitigados.

---

## 2. Matriz de Riesgos y Deuda Técnica

| Riesgo | Categoría | Probabilidad | Impacto | Estado / Mitigación |
| :--- | :--- | :--- | :--- | :--- |
| **Pérdida de Historial**<br>Los datos residían en memoria volátil. | Datos | ~~Alta~~ | ~~Alto~~ | ✅ **Resuelto (Semana 6):** PostgreSQL con ORM SQLAlchemy (async) persiste sesiones, diagnósticos, exploraciones y reseñas. |
| **Acoplamiento UI/Backend**<br>Toda la lógica convivía en un solo archivo. | Código | ~~Baja~~ | ~~N/A~~ | ✅ **Resuelto (Semana 2):** API RESTful independiente con FastAPI. |
| **Dependencias de Entorno**<br>"Funciona en mi máquina". | Dependencias | ~~Baja~~ | ~~N/A~~ | ✅ **Resuelto (Semana 4):** Docker y Docker Compose garantizan inmutabilidad del entorno. |
| **Saturación de VRAM**<br>Llama 3.1 exigía ~5GB de VRAM local. | Despliegue | ~~Media~~ | ~~Alto~~ | ✅ **Resuelto (Semana 6):** Migración a Ollama Cloud (Gemma 4 31B), sin dependencia de GPU local. |
| **Fricción GPU en Docker**<br>Virtualizar NVIDIA RTX en Windows era problemático. | Configuración | ~~Baja~~ | ~~N/A~~ | ✅ **Resuelto (Semana 6):** Ollama Cloud elimina la necesidad de GPU local. |
| **Inyección de Prompts**<br>Usuarios malintencionados podrían alterar el comportamiento del LLM. | Seguridad | Media | Medio | ⚠️ Parcialmente mitigado: Filtro semántico con Few-Shot Prompting. Pruebas automatizadas validan rechazos. |
| **Alucinaciones de Contexto**<br>El LLM podría repetir comportamientos pasados. | Modelo | Media | Medio | ⚠️ Parcialmente mitigado: Aislamiento del historial en prompts. |
| **Dependencia de Ollama Cloud**<br>La inferencia depende de la conectividad con el servicio remoto. | Despliegue | Baja | Medio | ⚠️ Riesgo aceptado: Sin internet, el sistema no genera diagnósticos. Mitigación:monitoreo de conectividad. |
| **Sin Migraciones de Esquema**<br>Cambios en modelos ORM requieren recrear tablas. | Datos | Baja | Bajo | ⚠️ Deuda técnica: Pendiente implementar Alembic para migraciones. |

---

## 3. Conclusión del Análisis

Los riesgos críticos (acoplamiento, dependencias, VRAM, GPU, persistencia) han sido **mitigados completamente**. El sistema actual está desplegado con una arquitectura de 5 capas, Docker Compose y PostgreSQL, eliminando la dependencia de hardware local para la inferencia de IA.

Los riesgos restantes son de impacto bajo o medio y no bloquean el funcionamiento del sistema en el contexto del Módulo 4.
