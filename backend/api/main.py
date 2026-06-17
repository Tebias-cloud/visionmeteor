from fastapi import FastAPI, HTTPException, File, UploadFile
import shutil
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import json
import sys
import os
from datetime import datetime

# Agregar la ruta base al path para importar el core
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
sys.path.append(PROJECT_ROOT)

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

from backend.core.clasificador_v12 import ClasificadorV12

# Instancia global del modelo para mantenerlo cargado en memoria RAM
motor_analisis = ClasificadorV12()

app = FastAPI(title="VisionMeteor API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OUTPUTS_DIR = os.path.join(BASE_DIR, "data", "outputs")
INPUTS_DIR = os.path.join(BASE_DIR, "data", "inputs")

# Servir archivos estáticos para que Next.js consuma las imágenes por URL
os.makedirs(OUTPUTS_DIR, exist_ok=True)
os.makedirs(INPUTS_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory=OUTPUTS_DIR), name="static")

@app.post("/api/upload")
async def upload_images(
    visible: UploadFile = File(...), 
    infrarroja: UploadFile = File(...)
):
    """Sube y reemplaza las imágenes de entrada para análisis."""
    try:
        ruta_rgb = os.path.join(INPUTS_DIR, "imagen_visible.jpg")
        ruta_ir = os.path.join(INPUTS_DIR, "imagen_infrarroja.jpg")
        
        with open(ruta_rgb, "wb") as buffer:
            shutil.copyfileobj(visible.file, buffer)
            
        with open(ruta_ir, "wb") as buffer:
            shutil.copyfileobj(infrarroja.file, buffer)

        return {"status": "success", "message": "Imágenes cargadas y listas para analizar."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir: {str(e)}")

@app.post("/api/analizar")
def ejecutar_analisis():
    """Ejecuta el pipeline sobre las imágenes en data/inputs y devuelve el reporte real."""
    ruta_rgb = os.path.join(INPUTS_DIR, "imagen_visible.jpg")
    ruta_ir = os.path.join(INPUTS_DIR, "imagen_infrarroja.jpg")
    
    if not os.path.exists(ruta_rgb) or not os.path.exists(ruta_ir):
        raise HTTPException(status_code=400, detail="Faltan las imágenes en backend/data/inputs/")
    
    try:
        # Usamos el motor cargado globalmente
        res = motor_analisis.analizar(
            ruta_rgb, 
            ruta_ir, 
            ruta_mascara_tierra=None, 
            carpeta_salida=OUTPUTS_DIR, 
            guardar=True
        )
        r = res['resultados']
        amenaza, nivel = motor_analisis.determinar_amenaza_principal(r['porcentajes'])
        
        reporte = {
            "fecha": datetime.now().isoformat(),
            "amenaza_principal": {
                "clase": amenaza,
                "nivel": nivel
            },
            "estadisticas": {
                "porcentaje_nubes_total": r['porcentaje_nubes_total'],
                "porcentaje_superficie_total": r['porcentaje_superficie_total'],
                "desglose_porcentajes": r['porcentajes'],
                "contadores_pixeles": r['contadores']
            },
            "imagenes": res.get("archivos", {})
        }
        
        ruta_json = os.path.join(OUTPUTS_DIR, "reporte_meteorologico.json")
        with open(ruta_json, "w") as f:
            json.dump(reporte, f, indent=4)
            
        # Generar Boletín PDF de Nivel Enterprise
        try:
            from backend.core.generador_pdf import GeneradorPDF
            pdf = GeneradorPDF()
            ruta_pdf = os.path.join(OUTPUTS_DIR, "boletin_meteorologico.pdf")
            
            rutas_absolutas = {}
            archivos = res.get("archivos", {})
            if 'comparacion' in archivos:
                rutas_absolutas['comparacion'] = os.path.join(OUTPUTS_DIR, archivos['comparacion'])
            if 'heatmap' in archivos:
                rutas_absolutas['heatmap'] = os.path.join(OUTPUTS_DIR, archivos['heatmap'])
                
            pdf.generar_boletin(reporte, rutas_absolutas, ruta_pdf)
            reporte["boletin_pdf"] = "boletin_meteorologico.pdf"
        except ImportError:
            print("Librería fpdf2 no instalada. Omitiendo generación de PDF.")
            reporte["boletin_pdf"] = None
        except Exception as e:
            print(f"Error generando PDF: {e}")
            reporte["boletin_pdf"] = None
            
        return reporte
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=500, 
            content={
                "error": True, 
                "message": f"Error interno en el motor de Machine Learning: {str(e)}",
                "detalles_tecnicos": "El servidor capturó la excepción y sigue funcionando."
            }
        )

@app.get("/api/reporte")
def get_reporte():
    """Devuelve el último reporte meteorológico generado"""
    ruta_json = os.path.join(OUTPUTS_DIR, "reporte_meteorologico.json")
    if not os.path.exists(ruta_json):
        raise HTTPException(status_code=404, detail="Reporte no encontrado. Ejecuta el análisis primero.")
    
    with open(ruta_json, "r") as f:
        data = json.load(f)
    return data

@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "VisionMeteor API"}
