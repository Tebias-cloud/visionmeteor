import os
import sys
from backend.core.clasificador_v12 import ClasificadorV12

base_dir = os.path.dirname(os.path.abspath(__file__))
inputs_dir = os.path.join(base_dir, "backend", "data", "inputs")
outputs_dir = os.path.join(base_dir, "resultados_test")

casos = [
    ("tarapaca_despejado.jpg", "tarapaca_despejado_ir.jpg"),
    ("tarapaca_camanchaca.jpg", "tarapaca_camanchaca_ir.jpg"),
    ("tarapaca_nubosidad_parcial.jpg", "tarapaca_nubosidad_parcial_ir.jpg")
]

clasificador = ClasificadorV12()

for vis, ir in casos:
    ruta_vis = os.path.join(inputs_dir, vis)
    ruta_ir = os.path.join(inputs_dir, ir)
    
    print(f"\n[{vis}] - Procesando escenario...")
    resultados = clasificador.analizar(ruta_vis, ruta_ir, carpeta_salida=outputs_dir, guardar=True)
    
    r = resultados['resultados']
    print("Resultados:")
    for clase, porcentaje in r['porcentajes'].items():
        if porcentaje > 0:
            print(f"  {clase}: {porcentaje}%")
    print("-" * 50)
