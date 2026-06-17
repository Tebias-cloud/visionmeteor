import os, shutil, sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from backend.api.main import ejecutar_analisis

demo_dir = 'backend/data/ejemplos_demostracion'
inputs_dir = 'backend/data/inputs'
p = '6_tarapaca_camanchaca'

print(f'\n--- TESTING {p} ---')
vis_src = os.path.join(demo_dir, f'{p}_vis.jpg')
ir_src = os.path.join(demo_dir, f'{p}_ir.jpg')
vis_dst = os.path.join(inputs_dir, 'imagen_visible.jpg')
ir_dst = os.path.join(inputs_dir, 'imagen_infrarroja.jpg')

shutil.copy(vis_src, vis_dst)
shutil.copy(ir_src, ir_dst)

stats = ejecutar_analisis()
print(stats['estadisticas']['desglose_porcentajes'])
