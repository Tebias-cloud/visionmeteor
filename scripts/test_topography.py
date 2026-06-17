import cv2
import numpy as np

def infer_topography(name, vis_path, ir_path):
    vis = cv2.imread(vis_path, cv2.IMREAD_GRAYSCALE)
    ir = cv2.imread(ir_path)
    b, g, r = cv2.split(ir)
    
    h, w = vis.shape
    
    # 1. Identify Clear Sky
    # Clouds are bright. Clear ground/ocean is dark.
    # Exception: Desert can be bright (vis up to 130).
    # Storms/Snow are very bright (>150).
    clear_sky = (vis < 130)
    
    # 2. Classify clear pixels
    # Desert/Land is high Green thermal (>90)
    # Ocean is low Green thermal (<80)
    is_tierra = clear_sky & (g > 90)
    is_mar = clear_sky & (g <= 90)
    
    # 3. Create initial mask (0: Mar, 255: Tierra, 128: Unknown)
    topo = np.full((h, w), 128, dtype=np.uint8)
    topo[is_mar] = 0
    topo[is_tierra] = 255
    
    # If the image has almost no clear sky, default to Ocean if it's a hurricane?
    # Actually, nearest neighbor interpolation!
    # We can use distance transform to find the nearest known pixel.
    
    # Create mask for known pixels
    known_mask = (topo != 128).astype(np.uint8)
    
    # If NO known pixels exist, default to MAR (e.g., massive storm covering everything)
    if np.sum(known_mask) == 0:
        topo[:] = 0
    else:
        # Distance to TIERRA
        dist_to_tierra, labels_tierra = cv2.distanceTransformWithLabels((topo != 255).astype(np.uint8), cv2.DIST_L2, 5)
        # Distance to MAR
        dist_to_mar, labels_mar = cv2.distanceTransformWithLabels((topo != 0).astype(np.uint8), cv2.DIST_L2, 5)
        
        # Fill unknown
        unknown = (topo == 128)
        # If distance to Tierra is smaller than distance to Mar, it's Tierra!
        topo[unknown] = np.where(dist_to_tierra[unknown] < dist_to_mar[unknown], 255, 0)
        
    # Analyze the result
    porc_tierra = np.sum(topo == 255) / (h*w) * 100
    print(f"[{name}] Inferered Topography -> Tierra: {porc_tierra:.1f}%, Mar: {100 - porc_tierra:.1f}%")
    
    # Save debug image
    cv2.imwrite(f'backend/data/outputs/topo_{name}.jpg', topo)

demo_dir = 'backend/data/ejemplos_demostracion'
infer_topography('HURACAN', f'{demo_dir}/1_huracan_vis.jpg', f'{demo_dir}/1_huracan_ir.jpg')
infer_topography('TARAPACA', f'{demo_dir}/6_tarapaca_camanchaca_vis.jpg', f'{demo_dir}/6_tarapaca_camanchaca_ir.jpg')
infer_topography('DESIERTO', f'{demo_dir}/4_desierto_despejado_vis.jpg', f'{demo_dir}/4_desierto_despejado_ir.jpg')
infer_topography('ARCHIPIELAGO', f'{demo_dir}/3_archipielago_vis.jpg', f'{demo_dir}/3_archipielago_ir.jpg')
