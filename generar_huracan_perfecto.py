import cv2
import numpy as np
import os

folder = r"c:\Users\Esteban\Desktop\visionmeteor\backend\data\ejemplos_demostracion"

h, w = 1000, 1000

vis = np.zeros((h, w), dtype=np.uint8)
ir = np.zeros((h, w, 3), dtype=np.uint8)

# Mar de fondo (Muy oscuro, < 50)
vis[:] = 40
ir[:] = [200, 50, 0] # Cálido

# Huracán en el centro
center = (w//2, h//2)
radius = 400

# Crear una máscara radial para el huracán
for y in range(h):
    for x in range(w):
        dist = np.sqrt((x - center[0])**2 + (y - center[1])**2)
        if dist < radius:
            # Espiral simple
            angle = np.arctan2(y - center[1], x - center[0])
            spiral = np.sin(dist/20.0 - angle*3)
            
            # El ojo del huracán (dist < 40) es mar (despejado)
            if dist < 40:
                continue
                
            if spiral > 0:
                # Nube muy brillante (> 160)
                # OJO: Nunca usamos valores entre 60 y 150 para evitar "Tierra"
                intensidad = int(160 + (1.0 - dist/radius) * 90)
                vis[y, x] = intensidad
                
                # IR: Muy frío (Rojo alto > 160)
                ir_rojo = int(160 + (1.0 - dist/radius) * 90)
                ir[y, x] = [50, 50, ir_rojo]

# Añadir textura base
noise = np.random.randint(0, 10, (h, w), dtype=np.uint8)
vis = cv2.add(vis, noise)

vis = cv2.GaussianBlur(vis, (15, 15), 0)
ir = cv2.GaussianBlur(ir, (15, 15), 0)

# Asegurar de nuevo que no hayan píxeles de Tierra (60 a 150) debido al blur
vis = np.where((vis > 60) & (vis <= 150), np.where(vis > 105, 155, 55), vis).astype(np.uint8)

vis_3c = cv2.cvtColor(vis, cv2.COLOR_GRAY2BGR)

cv2.imwrite(os.path.join(folder, "huracan_vis.jpg"), vis_3c)
cv2.imwrite(os.path.join(folder, "huracan_ir.jpg"), ir)

print("Huracán sintético perfecto generado sin píxeles verdes (60-150).")
