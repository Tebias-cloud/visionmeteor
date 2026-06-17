import cv2
import numpy as np

def check_image(name, vis_path, mask_path):
    vis = cv2.imread(vis_path, cv2.IMREAD_GRAYSCALE)
    mask = cv2.imread(mask_path)
    b, g, r = cv2.split(mask)
    
    h, w = vis.shape
    left_half = mask[:, :w//2]
    right_half = mask[:, w//2:]
    
    def get_color_percentages(half):
        total = half.shape[0] * half.shape[1]
        b_half, g_half, r_half = cv2.split(half)
        
        is_black = (b_half == 0) & (g_half == 0) & (r_half == 0)
        is_grey = (b_half == 200) & (g_half == 200) & (r_half == 200)
        is_green = (b_half == 34) & (g_half == 139) & (r_half == 34)
        is_red = (b_half == 0) & (g_half == 0) & (r_half == 255)
        is_white = (b_half == 255) & (g_half == 255) & (r_half == 255)
        
        return {
            'Ocean/Black': np.sum(is_black) / total * 100,
            'Cloud/Grey': np.sum(is_grey) / total * 100,
            'Land/Green': np.sum(is_green) / total * 100,
            'Storm/Red': np.sum(is_red) / total * 100,
            'Cirrus/White': np.sum(is_white) / total * 100
        }
        
    print(f"[{name}] Left Half (Should be mostly Cloud/Grey and Ocean/Black):")
    print(get_color_percentages(left_half))
    print(f"[{name}] Right Half (Should be mostly Land/Green):")
    print(get_color_percentages(right_half))
    print("-" * 30)

demo_dir = 'backend/data/ejemplos_demostracion'
out_dir = 'backend/data/outputs'
check_image('TARAPACA', f'{demo_dir}/6_tarapaca_camanchaca_vis.jpg', f'{out_dir}/resultados_6_tarapaca_camanchaca/mapa_segmentacion.png')
check_image('DESIERTO', f'{demo_dir}/4_desierto_despejado_vis.jpg', f'{out_dir}/resultados_4_desierto_despejado/mapa_segmentacion.png')
