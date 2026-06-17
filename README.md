# 🛰️ VisionMeteor: Sistema de Clasificación Meteorológica

Plataforma Full-Stack para la clasificación meteorológica de imágenes satelitales (NOAA/Meteor) obtenidas vía RTL-SDR. 

## 🏗️ Arquitectura del Proyecto

El proyecto está dividido en dos capas principales:

- **Backend (`/backend`)**: Motor en Python puro impulsado por FastAPI, OpenCV y NumPy. Se encarga de procesar las imágenes térmicas y visibles, generar la clasificación de nubes vectorizada (milisegundos) y servir los reportes vía API REST.
- **Frontend (`/frontend`)**: Dashboard interactivo en Next.js (React) que consume la API del backend para mostrar tarjetas de métricas, niveles de riesgo, y los mapas generados de forma visual.

Para más detalles técnicos sobre el flujo de datos desde el RTL-SDR hasta la web, consulta [docs/arquitectura.md](docs/arquitectura.md).

## 🚀 Requisitos Previos

- Python 3.8+
- Node.js 18+ y npm

## ⚙️ Instalación y Uso

### 1. Iniciar el Backend (Python)
Abre una terminal y navega a la carpeta principal del proyecto:

```bash
# 1. Instala las dependencias del motor
pip install -r backend/requirements.txt

# 2. Coloca tus imágenes satelitales en la carpeta de inputs:
# backend/data/inputs/imagen_visible.jpg
# backend/data/inputs/imagen_infrarroja.jpg

# 3. Ejecuta el clasificador meteorológico (Procesamiento)
python backend/core/clasificador_v11.py

# 4. Inicia la API para servir los datos al frontend
uvicorn backend.api.main:app --reload --port 8000
```
> *Nota: Tras ejecutar el clasificador (Paso 3), los mapas resultantes y el `reporte_meteorologico.json` se generarán automáticamente en `backend/data/outputs/`.*

### 2. Iniciar el Frontend (Next.js)
Abre una segunda terminal:

```bash
cd frontend
npm install
npm run dev
```

El Dashboard estará disponible en `http://localhost:3000`.

## 🛠️ Calibración del Clasificador
Puedes afinar la sensibilidad del sistema modificando los umbrales en `backend/core/clasificador_v11.py`:
- `UMBRAL_BRILLO_NUBE = 85`: Auméntalo si clasifica tierra como nube.
- `UMBRAL_IR_FRIO = 150`: Frialdad mínima (Canal Rojo) para considerar tormentas.
- `UMBRAL_IR_CALIDO = 200`: Calor (Canal Azul) para el océano.
- `UMBRAL_TEXTURA_ALTA = 45`: Magnitud Laplaciana para Cumulonimbus.
