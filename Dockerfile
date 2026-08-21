# 1. Usar una imagen oficial de Python ligera
FROM python:3.11-slim

# 2. Evitar que Python escriba archivos .pyc y forzar que la salida estándar se muestre en consola
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Copiar solo el archivo de dependencias
COPY requirements.txt .

# 5. Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# ---> AGREGAR ESTO: Descargar el modelo de spaCy durante la construcción
RUN python -m spacy download es_core_news_sm

# 6. Copiar el resto del codigo del proyecto al contenedor
COPY . .

# 7. Crear usuario no-root
RUN useradd --create-home --shell /bin/bash appuser
USER appuser

# 8. Exponer el puerto
EXPOSE 8000

# 9. Comando para iniciar
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]