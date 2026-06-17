import os, shutil, sys

# Add project root to path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from backend.api.main import ejecutar_analisis

demo_dir = 'backend/data/ejemplos_demostracion'
inputs_dir = 'backend/data/inputs'
outputs_dir = 'backend/data/outputs'
artifact_dir = os.path.join(BASE_DIR, 'artifacts', 'images')
os.makedirs(artifact_dir, exist_ok=True)

pairs = ['1_huracan', '6_tarapaca_camanchaca']

for p in pairs:
    print(f'\n--- TESTING {p} ---')
    vis_src = os.path.join(demo_dir, f'{p}_vis.jpg')
    ir_src = os.path.join(demo_dir, f'{p}_ir.jpg')
    mask_src = os.path.join(demo_dir, f'{p}_mask.png')
    vis_dst = os.path.join(inputs_dir, 'imagen_visible.jpg')
    ir_dst = os.path.join(inputs_dir, 'imagen_infrarroja.jpg')
    mask_dst = os.path.join(inputs_dir, 'mascara_tierra.png')
    
    shutil.copy(vis_src, vis_dst)
    shutil.copy(ir_src, ir_dst)
    shutil.copy(mask_src, mask_dst)
    
    try:
        stats = ejecutar_analisis()
        print(f"Nubes: {stats['estadisticas']['porcentaje_nubes_total']}% | Superficie: {stats['estadisticas']['porcentaje_superficie_total']}%")
        print(stats['estadisticas']['desglose_porcentajes'])
        
        # Copiar las imagenes resultantes al artifact dir
        # Buscar la imagen mas reciente
        import glob
        comparisons = glob.glob(os.path.join(outputs_dir, '03_comparacion_*.jpg'))
        if comparisons:
            latest = max(comparisons, key=os.path.getctime)
            target_path = os.path.join(artifact_dir, f'{p}_comparacion.jpg')
            shutil.copy(latest, target_path)
            print(f"Guardado en {target_path}")
            
    except Exception as e:
        print(f'ERROR: {e}')
