# VisionMeteor - Backend (Motor Matemático y ML)

## 📡 Descripción General
El backend de VisionMeteor es el núcleo de procesamiento de imágenes satelitales obtenidas a través de estaciones terrenas RTL-SDR y procesadas primariamente por SatDump. Su objetivo es recibir datos espectrales (canal visible e infrarrojo térmico) y aplicar algoritmos de **Machine Learning No Supervisado** y **Visión por Computadora** para clasificar fenómenos meteorológicos y extraer métricas.

## 🏗️ Arquitectura del Sistema
El backend está estructurado bajo una arquitectura de microservicios con FastAPI, priorizando la ejecución asíncrona y el desacoplamiento:

*   `api/main.py`: Punto de entrada de la aplicación. Expone los endpoints RESTful (`/api/upload`, `/api/analizar`, `/api/reporte`) y sirve los archivos estáticos de resultados a través de la red local.
*   `core/clasificador_v11.py`: El "Cerebro" matemático. Extrae las características físicas (Albedo, Frialdad Radiométrica, Calor Térmico) de las imágenes y utiliza `cv2.kmeans` (K-Means Clustering) para agrupar los píxeles en 5 clases meteorológicas puras, evadiendo la necesidad de thresholds estáticos frágiles. También procesa mapas de calor en formato `cv2.COLORMAP_INFERNO`.
*   `core/generador_pdf.py`: Módulo de reportabilidad Enterprise. Compila los JSON generados por el modelo en Boletines Meteorológicos vectoriales en formato PDF para el usuario final.
*   `data/`: Almacenamiento local temporal.
    *   `inputs/`: Directorio de ingesta de datos crudos (imágenes visibles e infrarrojas entrantes).
    *   `outputs/`: Directorio de volcado de datos procesados (JSON, imágenes con paneles informativos superpuestos, mapas de calor y PDFs).

## 🧠 Flujo de Datos del Modelo (Machine Learning)
1.  **Ingesta:** Se reciben dos imágenes de espectro NOAA.
2.  **Aplanamiento de Feature Space:** Se crea un hiperespacio de 3 dimensiones `[Brillo, Frialdad, Calor]`.
3.  **Clustering:** El modelo K-Means se entrena al vuelo buscando $K=5$ grupos dominantes (o $K=2$ si detecta homogeneidad extrema, como un océano abierto vacío, para evitar alucinaciones).
4.  **Mapeo Determinista:** Los centroides resultantes se evalúan térmicamente para etiquetarlos en: `TORMENTA`, `CIRROS`, `NUBE_BAJA_MEDIA`, `MAR` y `TIERRA`.
5.  **Reconstrucción y Exportación:** Se generan mapas visuales segmentados y un JSON estructurado con la amenaza dominante calculada.

## 🚀 Requisitos y Configuración
El proyecto requiere **Python 3.11+** para maximizar la compatibilidad con OpenCV y NumPy.

**Dependencias principales:**
*   `fastapi` / `uvicorn` (Servidor Web de alto rendimiento)
*   `opencv-python` (Procesamiento de imágenes y K-Means ML)
*   `numpy` (Cálculos de matrices eficientes)
*   `fpdf2` (Generación de PDFs)
*   `python-multipart` (Soporte de subida de archivos en API)

**Instalación Rápida:**
```bash
pip install -r requirements.txt
```

**Ejecución Rápida (Desarrollo):**
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```
(O simplemente ejecute el `start.bat` en la raíz del proyecto para inicializar todo automáticamente).
