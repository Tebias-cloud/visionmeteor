import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from backend.core.clasificador_v11 import ClasificadorNubesV11
import cv2

demo_dir = 'backend/data/ejemplos_demostracion'
vis_src = os.path.join(demo_dir, '6_tarapaca_camanchaca_vis.jpg')
ir_src = os.path.join(demo_dir, '6_tarapaca_camanchaca_ir.jpg')

vis_dst = 'backend/data/inputs/imagen_visible.jpg'
ir_dst = 'backend/data/inputs/imagen_infrarroja.jpg'

import shutil
shutil.copy(vis_src, vis_dst)
shutil.copy(ir_src, ir_dst)

c = ClasificadorNubesV11()
res = c.analizar(vis_dst, ir_dst, 'backend/data/outputs_v11')
print(res['resultados']['porcentajes'])
