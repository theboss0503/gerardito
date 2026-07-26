# Registro de Errores y Correcciones (Testing y CI/CD)

1. **Bloqueo de Importación de Módulos (CI/CD y Local)**
   - **Error:** `ModuleNotFoundError: No module named 'app'` al ejecutar pytest.
   - **Causa:** El entorno aislado de GitHub Actions no reconocía el directorio raíz como parte del `PYTHONPATH`.
   - **Corrección:** Se modificó el comando de ejecución de pruebas en el pipeline a `python -m pytest -v test/` para forzar la inclusión del directorio actual en la ruta de búsqueda de módulos.

2. **Falta de Dependencias en el Pipeline**
   - **Error:** `ModuleNotFoundError: No module named 'langchain_openai'` durante el flujo de CI.
   - **Causa:** La dependencia necesaria para la conexión remota con la IA no estaba declarada en los pasos de instalación del contenedor virtual de GitHub.
   - **Corrección:** Se agregó la dependencia al comando de instalación en `ci.yml`.

3. **Error de Enrutamiento en Entorno de Pruebas**
   - **Error:** Todos los endpoints devolvían error `404 Not Found` durante la ejecución de los tests.
   - **Causa:** El cliente de pruebas (`TestClient`) estaba solicitando rutas absolutas (ej. `/diagnostico`), pero la aplicación principal enruta todo bajo un prefijo ( `/api/v1/diagnostico`).
   - **Corrección:** Se actualizaron las URLs en el archivo `test/test_main.py` para coincidir con el enrutador de la aplicación principal.

4. **Vulnerabilidad en Validación de Datos (Pydantic)**
   - **Error:** El sistema procesaba listas vacías `[]` retornando un código HTTP `200 OK`, lo cual es un comportamiento indeseado para el motor de diagnóstico.
   - **Causa:** El esquema de Pydantic `PerfilEstudiante` validaba el tipo de dato (lista), pero no su longitud mínima.
   - **Corrección:** Se modificó el esquema agregando `min_length=1` mediante `Field()` a las propiedades de habilidades e intereses, logrando que el sistema retorne el código de error `422 Unprocessable Entity` antes de ejecutar la lógica de negocio.