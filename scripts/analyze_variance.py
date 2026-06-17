import cv2
import numpy as np

def analyze_variance(name, vis_path, ir_path):
    vis = cv2.imread(vis_path, cv2.IMREAD_GRAYSCALE)
    ir = cv2.imread(ir_path)
    b, g, r = cv2.split(ir)
    
    # Texture is the Laplacian
    laplacian = cv2.Laplacian(vis, cv2.CV_64F)
    tex = cv2.normalize(np.abs(laplacian), None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    
    # Compute local variance of texture (31x31 window)
    mean_tex = cv2.blur(tex, (31, 31))
    mean_sq_tex = cv2.blur(tex**2, (31, 31))
    var_tex = mean_sq_tex - mean_tex**2
    var_tex = np.clip(var_tex, 0, None)
    
    # Isolate the bright cold areas
    bright_cold = (vis > 150) & (r > 150) & (g < 100)
    
    if np.any(bright_cold):
        print(f"[{name}] Bright Cold Area -> Tex Var 31: {var_tex[bright_cold].mean():.1f}, Tex Mean 31: {mean_tex[bright_cold].mean():.1f}")
    else:
        print(f"[{name}] No bright cold areas.")

demo_dir = 'backend/data/ejemplos_demostracion'
analyze_variance('HURACAN (Storm)', f'{demo_dir}/1_huracan_vis.jpg', f'{demo_dir}/1_huracan_ir.jpg')
analyze_variance('TARAPACA (Andes)', f'{demo_dir}/6_tarapaca_camanchaca_vis.jpg', f'{demo_dir}/6_tarapaca_camanchaca_ir.jpg')
