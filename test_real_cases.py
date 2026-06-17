import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

from backend.core.clasificador_v12 import ClasificadorV12

motor = ClasificadorV12()
folder = r"c:\Users\Esteban\Desktop\visionmeteor\backend\data\ejemplos_demostracion"

casos = [
    ("HURACAN", "huracan_vis.jpg", "huracan_ir.jpg"),
    ("TARAPACA NUBES", "tarapaca_camanchaca_vis.jpg", "tarapaca_camanchaca_ir.jpg"),
    ("TARAPACA DESPEJADO", "tarapaca_despejado_vis.jpg", "tarapaca_despejado_ir.jpg")
]

for nombre, vis_file, ir_file in casos:
    print(f"\n--- Probando Caso: {nombre} ---")
    vis = os.path.join(folder, vis_file)
    ir = os.path.join(folder, ir_file)
    
    try:
        res = motor.analizar(vis, ir, guardar=False)
        porc = res['resultados']['porcentajes']
        amenaza, nivel = motor.determinar_amenaza_principal(porc)
        print(f"Amenaza Principal: {amenaza} ({nivel})")
        print(f"Nubes Totales: {res['resultados']['porcentaje_nubes_total']:.1f}%")
        for k, v in porc.items():
            if v > 0:
                print(f"  {k}: {v:.1f}%")
    except Exception as e:
        print(f"Error: {e}")
