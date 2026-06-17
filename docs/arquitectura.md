# Arquitectura VisionMeteor

## Flujo de Datos

1. **Captura y Decodificación (RTL-SDR + SatDump)**
   - El receptor RTL-SDR captura la señal del pase satelital (ej. NOAA o Meteor M2).
   - SatDump o WXtoImg decodifican el archivo de audio base y generan imágenes RGB (visible) y compuestas IR (temperatura).

2. **Procesamiento y Clasificación (Python / Backend Core)**
   - El módulo `clasificador_v11.py` ingiere las imágenes en `backend/data/inputs/`.
   - Utilizando OpenCV y NumPy Vectorizado, extrae brillo, textura y rangos térmicos.
   - Aplica lógica meteorológica para categorizar píxel por píxel la cobertura nubosa y los riesgos.
   - Exporta mapas dibujados y un `reporte_meteorologico.json` a `backend/data/outputs/`.

3. **Exposición de Datos (FastAPI)**
   - La API (`backend/api/main.py`) lee el JSON y expone endpoints ligeros y rápidos para ser consumidos.

4. **Visualización (Next.js / Frontend)**
   - El dashboard interactivo consume la API REST.
   - Presenta las tarjetas de métricas, niveles de amenaza y muestra al usuario los mapas renderizados.
