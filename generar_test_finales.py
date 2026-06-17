import cv2
import numpy as np
import os

folder = r"c:\Users\Esteban\Desktop\visionmeteor\backend\data\ejemplos_demostracion"

def create_image_set(name, cloud_type):
    h, w = 500, 500
    vis = np.zeros((h, w, 3), dtype=np.uint8)
    ir = np.zeros((h, w, 3), dtype=np.uint8)
    
    # Base: Mar (Izquierda), Tierra (Derecha)
    # Visible: Mar es oscuro (30), Tierra es gris (100)
    vis[:, :w//2] = (30, 30, 30)
    vis[:, w//2:] = (100, 100, 100)
    
    # Infrarrojo: Mar (cálido, rojo bajo, azul alto), Tierra (más cálida, rojo bajo, azul/verde alto)
    # Formato BGR
    ir[:, :w//2] = (200, 50, 20)   # Azulado
    ir[:, w//2:] = (150, 100, 20)  # Verdoso/Naranja
    
    if cloud_type == "HURACAN":
        # Nube espiral muy brillante y muy fría sobre el mar
        cv2.circle(vis, (w//3, h//2), 120, (255, 255, 255), -1)
        # Infrarrojo frío: alto canal rojo (ej 255), bajo azul (0)
        cv2.circle(ir, (w//3, h//2), 120, (50, 50, 250), -1) # BGR: Red es 250
        
    elif cloud_type == "NIEBLA":
        # Nube brillante baja (cálida) sobre la costa
        cv2.rectangle(vis, (int(w*0.4), int(h*0.2)), (int(w*0.8), int(h*0.8)), (220, 220, 220), -1)
        # Infrarrojo cálido (NUBE BAJA): rojo bajo (<100), canal azul alto
        cv2.rectangle(ir, (int(w*0.4), int(h*0.2)), (int(w*0.8), int(h*0.8)), (180, 150, 60), -1)
        
    elif cloud_type == "CIRROS":
        # Nube fina y fría sobre la tierra
        cv2.line(vis, (int(w*0.6), 100), (int(w*0.9), 400), (180, 180, 180), 40)
        # Infrarrojo frío medio: rojo 130
        cv2.line(ir, (int(w*0.6), 100), (int(w*0.9), 400), (100, 100, 130), 40)
        
    # Difuminar para realismo
    vis = cv2.GaussianBlur(vis, (25, 25), 0)
    ir = cv2.GaussianBlur(ir, (25, 25), 0)
    
    cv2.imwrite(os.path.join(folder, f"test_{name}_vis.jpg"), vis)
    cv2.imwrite(os.path.join(folder, f"test_{name}_ir.jpg"), ir)

create_image_set("huracan", "HURACAN")
create_image_set("niebla", "NIEBLA")
create_image_set("despejado", "DESPEJADO")

print("Imágenes finales de prueba generadas.")
