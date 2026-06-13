# 🛰️ VisionMeteor: Sistema de Clasificación Meteorológica

Sistema avanzado para la clasificación meteorológica píxel por píxel de imágenes satelitales (NOAA/Meteor) obtenidas vía RTL-SDR. Utiliza técnicas vectorizadas de Visión por Computadora con OpenCV y NumPy para analizar la nubosidad y clasificar amenazas meteorológicas (Tormentas, Cirros, etc.).

## 🚀 Requisitos Previos

Asegúrate de tener Python 3.8+ instalado en tu sistema. Luego, instala las dependencias necesarias ejecutando:

```bash
pip install opencv-python numpy Pillow
```

## 📸 Paso a Paso: Cómo usar el sistema correctamente

Para que el script funcione, necesitas proveer dos imágenes satelitales de la **misma zona geográfica y en el mismo instante** (usualmente extraídas de programas como WXtoImg o SatDump).

### 1. Preparar las imágenes
1. **`imagen_visible.jpg`**: Una imagen satelital normal en luz visible (RGB). El sistema utilizará esto para determinar el brillo (detectar qué es nube y qué es superficie) y la textura de la imagen (detectar turbulencias o nubes de gran desarrollo vertical como los Cumulonimbus).
2. **`imagen_infrarroja.jpg`**: Una imagen infrarroja (IR) termal en **falso color**. El sistema usará el canal de color Rojo para medir la frialdad (congelamiento en cumbres de nubes altas) y el canal Azul para detectar focos cálidos (como el océano).

> [!IMPORTANT]  
> Ambas imágenes deben estar alineadas y representar exactamente la misma perspectiva. Si provienen del mismo pase satelital, coincidirán. 

### 2. Renombrar y ubicar los archivos
Coloca ambas imágenes en la misma carpeta donde se encuentra el script `analisis_meteorologico.py`. 
Asegúrate de renombrarlas exactamente con los siguientes nombres:

```text
visionmeteor/
│
├── analisis_meteorologico.py
├── imagen_visible.jpg        <-- (¡Importante! Renombrar así)
├── imagen_infrarroja.jpg     <-- (¡Importante! Renombrar así)
└── README.md
```

### 3. Ejecutar el Análisis
Abre tu terminal (Símbolo del sistema, PowerShell o Terminal de VS Code), navega a la carpeta del proyecto y ejecuta el script:

```bash
python analisis_meteorologico.py
```

### 4. Comprender los Resultados Generados
Gracias a la vectorización de NumPy, el sistema procesará millones de píxeles en fracciones de segundo y generará las siguientes salidas:

- **Imágenes de Visualización** (Se crearán en una carpeta llamada `resultados_v11_pixel_por_pixel/`):
  1. `01_mapa_clasificacion_[fecha].jpg`: El lienzo limpio con colores sólidos de la clasificación (Rojo=Tormenta, Cian=Cirros, etc.).
  2. `02_mapa_con_panel_[fecha].jpg`: La misma imagen pero con una Interfaz (UI) flotante con porcentajes y nivel de amenaza.
  3. `03_comparacion_[fecha].jpg`: Una imagen ancha comparando lado a lado tu foto visible contra el mapa resultante.
  4. `04_visualizacion_canales_IR_[fecha].jpg`: Diagnóstico para que veas cómo el script interpretó el frío y el calor de la imagen infrarroja.

- **Reporte de Datos JSON (Backend / Frontend)**:
  - Se creará un archivo `reporte_meteorologico.json` en la raíz de la carpeta.
  - Contiene los contadores de píxeles, porcentajes exactos, y la amenaza principal identificada. 
  - Este archivo es la pieza clave para que conectes el motor de Python con una futura interfaz web o aplicación construida en Next.js.

## 🛠️ Modificar la Sensibilidad (Opcional)
Si notas que tu antena/receptor RTL-SDR arroja imágenes más oscuras o más claras de lo normal y el script clasifica mal, puedes calibrar el motor fácilmente modificando los umbrales ubicados al inicio de `analisis_meteorologico.py` (líneas 23 al 26):
- `UMBRAL_BRILLO_NUBE = 85`: Auméntalo si el script clasifica la tierra como nube.
- `UMBRAL_IR_FRIO = 150`: Auméntalo si hay demasiadas falsas alertas de tormenta.
- `UMBRAL_IR_CALIDO = 200`: Umbral de calor oceánico.
- `UMBRAL_TEXTURA_ALTA = 45`: Magnitud de la rugosidad para detectar una tormenta eléctrica vs un cirro inofensivo.
