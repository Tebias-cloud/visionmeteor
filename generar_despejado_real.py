import cv2
import numpy as np
import os

folder = r"c:\Users\Esteban\Desktop\visionmeteor\backend\data\ejemplos_demostracion"

vis_path = os.path.join(folder, "6_tarapaca_camanchaca_vis.jpg")
ir_path = os.path.join(folder, "6_tarapaca_camanchaca_ir.jpg")

if os.path.exists(vis_path) and os.path.exists(ir_path):
    vis = cv2.imread(vis_path)
    ir = cv2.imread(ir_path)
    
    # 1. Crear Tarapacá Despejado
    vis_desp = vis.copy()
    ir_desp = ir.copy()
    
    h, w = vis.shape[:2]
    
    # Encontrar píxeles brillantes en el mar (Camanchaca)
    # El mar está en la mitad izquierda (aprox w*0.5)
    gray = cv2.cvtColor(vis, cv2.COLOR_BGR2GRAY)
    mask_nubes = (gray > 120)
    
    # Reemplazar las nubes del mar con el color del océano (gris muy oscuro ~40)
    for x in range(int(w * 0.5)):
        col_mask = mask_nubes[:, x]
        vis_desp[col_mask, x] = [40, 40, 40]
        # En IR, el mar es cálido (Rojo bajo ~40, Azul alto ~200)
        # BGR
        ir_desp[col_mask, x] = [200, 100, 40]
        
    # Difuminar un poco las áreas reemplazadas para que se vea natural
    vis_desp = cv2.GaussianBlur(vis_desp, (5, 5), 0)
    ir_desp = cv2.GaussianBlur(ir_desp, (5, 5), 0)
    
    # Guardar la nueva imagen "real" pero despejada
    cv2.imwrite(os.path.join(folder, "test_tarapaca_despejado_vis.jpg"), vis_desp)
    cv2.imwrite(os.path.join(folder, "test_tarapaca_despejado_ir.jpg"), ir_desp)
    
    print("Se generó exitosamente la imagen REAL de Tarapacá sin nubes (Despejado).")
else:
    print("No se encontraron las imágenes base.")
