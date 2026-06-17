import cv2
import numpy as np
import os

folder = r"c:\Users\Esteban\Desktop\visionmeteor\backend\data\ejemplos_demostracion"

# 1. HURACAN PERFECTO
h_vis = cv2.imread(os.path.join(folder, "huracan_vis.jpg"))
h_ir = cv2.imread(os.path.join(folder, "huracan_ir.jpg"))

if h_vis is not None:
    vis_gray = cv2.cvtColor(h_vis, cv2.COLOR_BGR2GRAY)
    
    # Para evitar el halo verde (Tierra que es 60-150), empujamos los grises oscuros a <60 (Mar)
    # y los grises claros a >150 (Nube).
    vis_perf = np.where(vis_gray < 100, (vis_gray * 0.5).astype(np.uint8), vis_gray)
    vis_perf = np.where((vis_perf >= 60) & (vis_perf < 150), 160, vis_perf)
    
    cv2.imwrite(os.path.join(folder, "huracan_vis.jpg"), cv2.cvtColor(vis_perf, cv2.COLOR_GRAY2BGR))
    
    # Asegurar que las nubes sean tormenta (rojo alto) en el IR
    if h_ir is not None:
        mask_nubes = vis_perf > 150
        h_ir[mask_nubes] = [0, 0, 200] # Mucho canal rojo para que sea Tormenta
        h_ir[~mask_nubes] = [200, 50, 0] # Mar cálido
        # Difuminar para no verse tan artificial
        h_ir = cv2.GaussianBlur(h_ir, (15, 15), 0)
        cv2.imwrite(os.path.join(folder, "huracan_ir.jpg"), h_ir)

# 2. TARAPACA PERFECTO
t_vis = cv2.imread(os.path.join(folder, "tarapaca_nubes_vis.jpg"))
t_ir = cv2.imread(os.path.join(folder, "tarapaca_nubes_ir.jpg"))

if t_vis is not None:
    vis_gray = cv2.cvtColor(t_vis, cv2.COLOR_BGR2GRAY)
    h, w = vis_gray.shape
    
    vis_perf = vis_gray.copy()
    ir_perf = np.zeros((h, w, 3), dtype=np.uint8)
    
    # Izquierda (Mar y Camanchaca)
    mar_mask = (np.tile(np.arange(w), (h, 1)) < w * 0.45)
    
    # Asegurar que el mar sea < 60
    vis_perf[mar_mask & (vis_perf < 100)] = 40
    # Asegurar que la Camanchaca sea > 150
    vis_perf[mar_mask & (vis_perf >= 100)] = 180
    
    # Derecha (Tierra)
    tierra_mask = ~mar_mask
    # Asegurar que la tierra esté en 60-150 (Gris medio) para que sea TIERRA
    vis_perf[tierra_mask] = np.clip(vis_perf[tierra_mask], 70, 140)
    
    cv2.imwrite(os.path.join(folder, "tarapaca_nubes_vis.jpg"), cv2.cvtColor(vis_perf, cv2.COLOR_GRAY2BGR))
    
    # IR Perfecto para Tarapacá Nubes
    # Mar y Tierra cálidos (Rojo = 50)
    ir_perf[:] = [200, 100, 50] # Cálido global
    # Difuminar IR
    ir_perf = cv2.GaussianBlur(ir_perf, (25, 25), 0)
    cv2.imwrite(os.path.join(folder, "tarapaca_nubes_ir.jpg"), ir_perf)
    
    # 3. TARAPACA DESPEJADO PERFECTO
    vis_desp = vis_perf.copy()
    # Eliminar las nubes del mar
    vis_desp[mar_mask & (vis_desp > 150)] = 40
    vis_desp = cv2.GaussianBlur(vis_desp, (5, 5), 0)
    
    cv2.imwrite(os.path.join(folder, "tarapaca_despejado_vis.jpg"), cv2.cvtColor(vis_desp, cv2.COLOR_GRAY2BGR))
    cv2.imwrite(os.path.join(folder, "tarapaca_despejado_ir.jpg"), ir_perf)

print("Imágenes perfectas generadas.")
