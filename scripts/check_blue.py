import cv2
import numpy as np

def check_blue(name, vis_path, ir_path):
    vis = cv2.imread(vis_path, cv2.IMREAD_GRAYSCALE)
    ir = cv2.imread(ir_path)
    b, g, r = cv2.split(ir)
    
    # Isolate the bright cold areas
    bright_cold = (vis > 140) & (r > 150) & (g < 100)
    
    if np.any(bright_cold):
        print(f"[{name}] Bright Cold Pixels: {np.sum(bright_cold)}")
        print(f"[{name}]   Pixels with B < 10: {np.sum(bright_cold & (b < 10))}")
        print(f"[{name}]   Pixels with B >= 10: {np.sum(bright_cold & (b >= 10))}")
    else:
        print(f"[{name}] No bright cold areas.")

demo_dir = 'backend/data/ejemplos_demostracion'
check_blue('HURACAN', f'{demo_dir}/1_huracan_vis.jpg', f'{demo_dir}/1_huracan_ir.jpg')
check_blue('TARAPACA', f'{demo_dir}/6_tarapaca_camanchaca_vis.jpg', f'{demo_dir}/6_tarapaca_camanchaca_ir.jpg')
check_blue('BLIZZARD', f'{demo_dir}/2_blizzard_vis.jpg', f'{demo_dir}/2_blizzard_ir.jpg')
