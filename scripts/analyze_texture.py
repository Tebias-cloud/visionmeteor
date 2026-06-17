import cv2
import numpy as np

def analyze_texture(name, vis_path, ir_path):
    vis = cv2.imread(vis_path, cv2.IMREAD_GRAYSCALE)
    ir = cv2.imread(ir_path)
    b, g, r = cv2.split(ir)
    
    laplacian = cv2.Laplacian(vis, cv2.CV_64F)
    tex = cv2.normalize(np.abs(laplacian), None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    
    # Isolate the bright cold areas
    bright_cold = (vis > 150) & (r > 150) & (g < 100)
    
    if np.any(bright_cold):
        print(f"[{name}] Bright Cold Area -> Vis: {vis[bright_cold].mean():.0f}, R: {r[bright_cold].mean():.0f}, Tex: {tex[bright_cold].mean():.0f}, Max Tex: {tex[bright_cold].max()}")
    else:
        print(f"[{name}] No bright cold areas.")

demo_dir = 'backend/data/ejemplos_demostracion'
analyze_texture('HURACAN (Storm)', f'{demo_dir}/1_huracan_vis.jpg', f'{demo_dir}/1_huracan_ir.jpg')
analyze_texture('TARAPACA (Andes)', f'{demo_dir}/6_tarapaca_camanchaca_vis.jpg', f'{demo_dir}/6_tarapaca_camanchaca_ir.jpg')
