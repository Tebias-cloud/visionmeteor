import cv2
import numpy as np
import os
import shutil
import sys

# Add project root to path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from backend.api.main import ejecutar_analisis

inputs_dir = 'backend/data/inputs'
outputs_dir = 'backend/data/outputs'
artifact_dir = os.path.join(BASE_DIR, 'artifacts', 'images')
os.makedirs(artifact_dir, exist_ok=True)

test_cases = {
    '7_ai_huracan': {
        'vis': r'C:\Users\Esteban\.gemini\antigravity\brain\adf6dfa8-7024-4cac-9c67-51e84cc4e8b0\ai_huracan_vis_1781581051992.png',
        'ir': r'C:\Users\Esteban\.gemini\antigravity\brain\adf6dfa8-7024-4cac-9c67-51e84cc4e8b0\ai_huracan_ir_1781581063425.png'
    },
    '8_ai_tarapaca': {
        'vis': r'C:\Users\Esteban\.gemini\antigravity\brain\adf6dfa8-7024-4cac-9c67-51e84cc4e8b0\ai_tarapaca_vis_1781581074416.png',
        'ir': r'C:\Users\Esteban\.gemini\antigravity\brain\adf6dfa8-7024-4cac-9c67-51e84cc4e8b0\ai_tarapaca_ir_1781581084534.png'
    }
}

for name, paths in test_cases.items():
    print(f'\n--- PROCESANDO {name} ---')
    
    # Read images
    vis_img = cv2.imread(paths['vis'])
    ir_img = cv2.imread(paths['ir'])
    
    if vis_img is None or ir_img is None:
        print(f"Error loading images for {name}")
        continue
        
    # Resize to 1024x1024
    vis_img = cv2.resize(vis_img, (1024, 1024))
    ir_img = cv2.resize(ir_img, (1024, 1024))
    
    # Save as jpg in inputs
    vis_dst = os.path.join(inputs_dir, 'imagen_visible.jpg')
    ir_dst = os.path.join(inputs_dir, 'imagen_infrarroja.jpg')
    mask_dst = os.path.join(inputs_dir, 'mascara_tierra.png')
    
    cv2.imwrite(vis_dst, vis_img)
    cv2.imwrite(ir_dst, ir_img)
    
    # Create empty mask (all ocean = 0)
    empty_mask = np.zeros((1024, 1024), dtype=np.uint8)
    cv2.imwrite(mask_dst, empty_mask)
    
    try:
        stats = ejecutar_analisis()
        print(f"Nubes: {stats['estadisticas']['porcentaje_nubes_total']}% | Superficie: {stats['estadisticas']['porcentaje_superficie_total']}%")
        print(stats['estadisticas']['desglose_porcentajes'])
        
        # Copiar la comparacion
        import glob
        comparisons = glob.glob(os.path.join(outputs_dir, '03_comparacion_*.jpg'))
        if comparisons:
            latest = max(comparisons, key=os.path.getctime)
            target_path = os.path.join(artifact_dir, f'{name}_comparacion.jpg')
            shutil.copy(latest, target_path)
            print(f"Guardado en {target_path}")
            
    except Exception as e:
        print(f'ERROR: {e}')
