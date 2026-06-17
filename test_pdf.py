import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

try:
    sys.stdout.reconfigure(encoding='utf-8')
except:
    pass

from backend.core.generador_pdf import GeneradorPDF

reporte = {
    "fecha": "2026-06-17T12:00:00",
    "amenaza_principal": {
        "clase": "TORMENTA",
        "nivel": "AMENAZA ALTA"
    },
    "estadisticas": {
        "porcentaje_nubes_total": 45.2,
        "porcentaje_superficie_total": 54.8,
        "desglose_porcentajes": {"MAR": 30.5, "TIERRA": 24.3, "NUBE_BAJA_MEDIA": 15.0, "CIRROS": 10.2, "TORMENTA": 20.0},
        "contadores_pixeles": {}
    }
}

rutas = {
    "comparacion": "test_sintetico_vis.jpg", # fake path just to test
    "heatmap": "test_sintetico_ir.jpg"
}

pdf = GeneradorPDF()
print("Iniciando generacion de PDF...")
pdf.generar_boletin(reporte, rutas, "test_pdf_salida.pdf")
print("Exito!")
