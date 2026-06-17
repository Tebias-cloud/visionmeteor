import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from backend.core.clasificador_v12 import ClasificadorV12

demo_dir = 'backend/data/ejemplos_demostracion'
vis_src = os.path.join(demo_dir, '4_desierto_despejado_vis.jpg')
ir_src = os.path.join(demo_dir, '4_desierto_despejado_ir.jpg')

vis_dst = 'backend/data/inputs/imagen_visible.jpg'
ir_dst = 'backend/data/inputs/imagen_infrarroja.jpg'

import shutil
shutil.copy(vis_src, vis_dst)
shutil.copy(ir_src, ir_dst)

c = ClasificadorV12()
res = c.analizar(vis_dst, ir_dst, 'backend/data/outputs')
print(f"Nubes: {res['resultados']['porcentaje_nubes_total']}% | Superficie: {res['resultados']['porcentaje_superficie_total']}%")
print(res['resultados']['porcentajes'])
