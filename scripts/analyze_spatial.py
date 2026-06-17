import cv2
import numpy as np

def analyze_spatial(name, vis_path, ir_path):
    vis = cv2.imread(vis_path, cv2.IMREAD_GRAYSCALE)
    ir = cv2.imread(ir_path)
    b, g, r = cv2.split(ir)
    
    # Isolate the bright cold areas
    bright_cold = (vis > 150) & (r > 150) & (g < 100)
    
    vis_blur_51 = cv2.blur(vis, (51, 51))
    
    if np.any(bright_cold):
        print(f"[{name}] Bright Cold Area -> Vis: {vis[bright_cold].mean():.1f}, Vis Blur 51x51: {vis_blur_51[bright_cold].mean():.1f}")
    else:
        print(f"[{name}] No bright cold areas.")

demo_dir = 'backend/data/ejemplos_demostracion'
analyze_spatial('HURACAN (Storm)', f'{demo_dir}/1_huracan_vis.jpg', f'{demo_dir}/1_huracan_ir.jpg')
analyze_spatial('TARAPACA (Andes)', f'{demo_dir}/6_tarapaca_camanchaca_vis.jpg', f'{demo_dir}/6_tarapaca_camanchaca_ir.jpg')
