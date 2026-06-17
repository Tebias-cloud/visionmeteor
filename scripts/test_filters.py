import cv2
import numpy as np

def test_filters():
    # Load Hurricane
    vis_h = cv2.imread('backend/data/ejemplos_demostracion/1_huracan_vis.jpg', cv2.IMREAD_GRAYSCALE)
    ir_h = cv2.imread('backend/data/ejemplos_demostracion/1_huracan_ir.jpg')
    tex_h = cv2.normalize(np.abs(cv2.Laplacian(vis_h, cv2.CV_64F)), None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    
    # Load Tarapaca
    vis_t = cv2.imread('backend/data/ejemplos_demostracion/6_tarapaca_camanchaca_vis.jpg', cv2.IMREAD_GRAYSCALE)
    ir_t = cv2.imread('backend/data/ejemplos_demostracion/6_tarapaca_camanchaca_ir.jpg')
    tex_t = cv2.normalize(np.abs(cv2.Laplacian(vis_t, cv2.CV_64F)), None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    
    # Analyze false TIERRA in hurricane
    # False tierra is likely where Vis is around 100-150 and it's not super cold.
    b, g, r = cv2.split(ir_h)
    print("Huracan pixels that might be falsely classified as Tierra (Vis 100-150, B > 100):")
    mask_false_tierra = (vis_h > 100) & (vis_h < 180) & (b > 100)
    print(f"Count: {np.sum(mask_false_tierra)}")
    
    # Analyze false TORMENTA in Andes
    b2, g2, r2 = cv2.split(ir_t)
    # Snow is where Vis > 150, R > 150, G < 100
    mask_snow = (vis_t > 150) & (r2 > 150) & (g2 < 100)
    print("Andes Snow pixels (Falsely classified as Tormenta):")
    print(f"Mean Texture: {tex_t[mask_snow].mean():.1f}")
    
    # True Tormenta in Hurricane
    mask_storm = (vis_h > 150) & (r > 150) & (g < 100)
    print("Hurricane Storm pixels:")
    print(f"Mean Texture: {tex_h[mask_storm].mean():.1f}")

test_filters()
