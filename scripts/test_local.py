import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from backend.core.clasificador_v11 import ClasificadorNubesV11
import cv2

demo_dir = 'backend/data/ejemplos_demostracion'
vis_src = os.path.join(demo_dir, '1_huracan_vis.png')
ir_src = os.path.join(demo_dir, '1_huracan_ir.png')

vis_dst = 'backend/data/inputs/imagen_visible.jpg'
ir_dst = 'backend/data/inputs/imagen_infrarroja.jpg'

import shutil
shutil.copy(vis_src, vis_dst)
shutil.copy(ir_src, ir_dst)

c = ClasificadorNubesV11()
res = c.analizar(vis_dst, ir_dst, 'backend/data/outputs')
print(f"Nubes: {res['porcentajes']['porcentaje_nubes_total']}% | Superficie: {res['porcentajes']['porcentaje_superficie_total']}%")
print(res['porcentajes'])
