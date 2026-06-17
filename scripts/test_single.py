import os, json, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from backend.api.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

demo_dir = 'backend/data/ejemplos_demostracion'
vis_src = os.path.join(demo_dir, '1_huracan_vis.png')
ir_src = os.path.join(demo_dir, '1_huracan_ir.png')

vis_dst = 'backend/data/inputs/imagen_visible.jpg'
ir_dst = 'backend/data/inputs/imagen_infrarroja.jpg'

import shutil
shutil.copy(vis_src, vis_dst)
shutil.copy(ir_src, ir_dst)

res = client.post("/api/analizar")
stats = res.json()
print(f"Nubes: {stats['estadisticas']['porcentaje_nubes_total']}% | Superficie: {stats['estadisticas']['porcentaje_superficie_total']}%")
print(stats['estadisticas']['desglose_porcentajes'])
