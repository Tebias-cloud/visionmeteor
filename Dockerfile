# Dockerfile para desplegar el Backend de VisionMeteor
FROM python:3.11-slim

# Instalar dependencias del sistema operativo que requiere OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar e instalar los requerimientos
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código del backend
COPY backend /app/backend

# Crear los directorios de datos para que existan en el servidor
RUN mkdir -p /app/backend/data/inputs /app/backend/data/outputs

EXPOSE 8000

# Comando para arrancar el servidor
CMD ["uvicorn", "backend.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
