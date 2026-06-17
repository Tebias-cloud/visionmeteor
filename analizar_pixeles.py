import cv2
import numpy as np
import os

folder = r"c:\Users\Esteban\Desktop\visionmeteor\backend\data\ejemplos_demostracion"

# Cargar la imagen de Tarapaca (ya está limpia y en grises)
vis_path = os.path.join(folder, "6_tarapaca_camanchaca_vis.jpg")
ir_path = os.path.join(folder, "6_tarapaca_camanchaca_ir.jpg")

vis = cv2.imread(vis_path, cv2.IMREAD_GRAYSCALE)
ir = cv2.imread(ir_path)

if vis is not None and ir is not None:
    print(f"Imagen visible cargada: {vis.shape}")
    
    # 1. Analizar el desierto (parte derecha de la imagen, sin nubes idealmente)
    h, w = vis.shape
    desierto_x_start = int(w * 0.7)
    desierto_vis = vis[:, desierto_x_start:]
    desierto_ir_rojo = ir[:, desierto_x_start:, 2] # Canal rojo (frialdad) en BGR
    
    print(f"\n--- ZONA DESIERTO (Derecha) ---")
    print(f"Brillo Visible: Min={desierto_vis.min()}, Max={desierto_vis.max()}, Media={desierto_vis.mean():.1f}")
    print(f"Frialdad IR (Rojo): Min={desierto_ir_rojo.min()}, Max={desierto_ir_rojo.max()}, Media={desierto_ir_rojo.mean():.1f}")
    
    # 2. Analizar Camanchaca (asumiendo que está en el centro-izquierda)
    cam_x_start = int(w * 0.2)
    cam_x_end = int(w * 0.5)
    cam_vis = vis[:, cam_x_start:cam_x_end]
    cam_ir_rojo = ir[:, cam_x_start:cam_x_end, 2]
    
    print(f"\n--- ZONA CAMANCHACA/MAR (Centro-Izquierda) ---")
    print(f"Brillo Visible: Min={cam_vis.min()}, Max={cam_vis.max()}, Media={cam_vis.mean():.1f}")
    print(f"Frialdad IR (Rojo): Min={cam_ir_rojo.min()}, Max={cam_ir_rojo.max()}, Media={cam_ir_rojo.mean():.1f}")
    
else:
    print("No se encontraron las imagenes de Tarapaca en la carpeta.")
