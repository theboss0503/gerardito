# Registro de Riesgos Técnicos y Deuda Técnica

## 1. Introducción
El presente documento identifica, clasifica y evalúa los riesgos técnicos y la deuda técnica actual del prototipo "Gerardito". La identificación honesta de estas vulnerabilidades es el primer paso crítico para la refactorización arquitectónica que se llevará a cabo durante las Semanas 2 a la 6 del Módulo 4. El objetivo no es ocultar las deficiencias del sistema actual (Streamlit monolítico), sino trazar un plan de mitigación realista hacia un entorno escalable, seguro y persistente.

---

## 2. Matriz de Riesgos y Deuda Técnica

| Riesgo | Categoría | Probabilidad | Impacto | Mitigación propuesta |
| :--- | :--- | :--- | :--- | :--- |
| **Pérdida de Historial y Cuellos de Botella**<br>Los datos residen en memoria volátil. Si se somete a pruebas de carga, la memoria colapsará y no hay persistencia. Usar una base local (como SQLite) bloquearía las escrituras simultáneas. *(Deuda Técnica)* | Datos | Alta | Alto | **Semana 2-3:** Integrar un motor cliente-servidor robusto (**SQL Server**) mediante un ORM y *pool* de conexiones para soportar transacciones concurrentes de múltiples usuarios. |
| ***Resuelto:* Fuerte Acoplamiento UI/Backend**<br>Toda la lógica y presentación convivían en un solo archivo, impidiendo la escalabilidad. *(Deuda Técnica)* | Código | Baja | N/A | ***Mitigado (Semana 2):*** Sistema desacoplado exitosamente creando una API RESTful independiente con FastAPI y validación estricta mediante Pydantic. |
| **Saturación de Memoria VRAM**<br>Llama 3.1 (8B) exige aproximadamente 5GB de VRAM. Peticiones simultáneas o sobrecarga en el contexto podrían desbordar los 8GB de la GPU anfitriona. | Despliegue | Media | Alto | **Semana 4 y 5:** Limitar la generación de tokens de salida (`num_predict`), implementar control de concurrencia en FastAPI y mantener el modelo cargado con `keep_alive`. |
| **Inyección de Prompts y "Jailbreaks"**<br>Usuarios malintencionados podrían introducir *prompts* que alteren el comportamiento del modelo, haciéndole ignorar sus reglas de sistema. | Seguridad | Media | Medio | **Semana 3:** Refinar los bloqueos semánticos previos a la inferencia (usando clasificación Zero-Shot) e implementar pruebas automatizadas para validar los rechazos. |
| **Alucinaciones de Contexto**<br>El LLM podría repetir comportamientos pasados (como volver a preguntar cosas que ya resolvió) si lee historiales muy largos. | Modelo | Media | Medio | Aislar el historial en el prompt final, pasando únicamente la instrucción estricta de la fase correspondiente (ej. generar reseña). |
| **Conflictos de Entorno y Librerías**<br>La combinación de dependencias para IA (LangChain, Ollama, spaCy) puede causar el problema de "funciona en mi máquina" en los equipos de los evaluadores. | Dependencias | Media | Medio | **Semana 4:** Contenerizar el Frontend y Backend utilizando Docker, y utilizar un archivo estricto de `requirements.txt` / `package.json`. |
| **Curva de Aprendizaje Breve**<br>El equipo debe migrar de Python puro (Streamlit) a un ecosistema de React.js y FastAPI en un plazo de tiempo muy ajustado (5 semanas). | Equipo | Baja | Medio | Asignación de roles claros. Utilizar la documentación autogenerada de FastAPI (Swagger UI) para facilitar la integración rápida con el frontend. |
| **Fricción en Despliegue con GPU**<br>Configurar un contenedor Docker en Windows para que reconozca directamente la tarjeta gráfica dedicada (NVIDIA) suele presentar fallos. | Configuración | Alta | Alto | **Semana 4:** Mantener el servidor de Ollama corriendo nativamente en el *Host* (Windows) y hacer que los contenedores de Docker se comuniquen con él a través de la red interna. |

---

## 3. Conclusión del Análisis
Habiendo mitigado exitosamente el mayor riesgo de código (el acoplamiento) mediante la implementación de la API con FastAPI, el volumen de riesgo actual se concentra en la **Capa de Datos y el Rendimiento Bajo Carga**. La decisión de descartar bases de datos de archivo único en favor de un motor robusto (SQL Server) preparará al sistema para soportar pruebas de estrés reales. A nivel de infraestructura, mantener Ollama en ejecución nativa y contenerizar únicamente el *Backend* y el *Frontend* sigue siendo la estrategia más inteligente para evitar los cuellos de botella de la virtualización de hardware gráfico.