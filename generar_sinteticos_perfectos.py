import cv2
import numpy as np
import os

folder = r"c:\Users\Esteban\Desktop\visionmeteor\backend\data\ejemplos_demostracion"
os.makedirs(folder, exist_ok=True)

h, w = 800, 1000

# Función para crear textura (perlin simple)
def create_texture(h, w, scale):
    noise = np.random.randint(0, 50, (h//scale, w//scale), dtype=np.uint8)
    noise = cv2.resize(noise, (w, h), interpolation=cv2.INTER_LINEAR)
    return noise

# ==========================================
# 1. TARAPACA CON NUBES (CAMANCHACA)
# ==========================================
vis = np.zeros((h, w), dtype=np.uint8)
ir = np.zeros((h, w, 3), dtype=np.uint8)

# Mar (izquierda) y Tierra (derecha). La costa es irregular.
for y in range(h):
    costa_x = int(w * 0.45 + np.sin(y/50.0)*30 + np.sin(y/10.0)*10)
    
    # Mar: Muy oscuro (30 a 50)
    vis[y, :costa_x] = 40 + np.random.randint(-10, 10)
    # IR Mar: Cálido (BGR: Azul alto, Rojo bajo)
    ir[y, :costa_x] = [200, 100, 50]
    
    # Tierra: Gris medio
    vis[y, costa_x:] = 80 + np.random.randint(-10, 10)
    # IR Tierra: Muy Cálido (BGR: Rojo bajo)
    ir[y, costa_x:] = [180, 120, 40]

# Texturizar
vis = cv2.add(vis, create_texture(h, w, 10))

# Agregar Camanchaca sobre el mar (Nube baja/media)
# Brillante (Visible = 180), pero Cálida (IR Rojo = 50)
for y in range(h):
    nube_borde = int(w * 0.4 + np.sin(y/40.0)*40 + np.cos(y/20.0)*20)
    # Rellenar nube
    vis[y, int(w*0.1):nube_borde] = 180 + np.random.randint(-20, 20)
    # Mantener el IR cálido para que sea "Nube Baja Media" y no Tormenta
    ir[y, int(w*0.1):nube_borde] = [200, 120, 60] # Rojo = 60 (< 100)

vis_nubes = cv2.GaussianBlur(vis, (15, 15), 0)
ir_nubes = cv2.GaussianBlur(ir, (15, 15), 0)

# Convertir visible a 3 canales para guardarlo
vis_nubes_3c = cv2.cvtColor(vis_nubes, cv2.COLOR_GRAY2BGR)
cv2.imwrite(os.path.join(folder, "tarapaca_nubes_vis.jpg"), vis_nubes_3c)
cv2.imwrite(os.path.join(folder, "tarapaca_nubes_ir.jpg"), ir_nubes)

# ==========================================
# 2. TARAPACA DESPEJADO
# ==========================================
vis_desp = np.zeros((h, w), dtype=np.uint8)
ir_desp = np.zeros((h, w, 3), dtype=np.uint8)

for y in range(h):
    costa_x = int(w * 0.45 + np.sin(y/50.0)*30 + np.sin(y/10.0)*10)
    vis_desp[y, :costa_x] = 40 + np.random.randint(-10, 10)
    ir_desp[y, :costa_x] = [200, 100, 50]
    vis_desp[y, costa_x:] = 80 + np.random.randint(-10, 10)
    ir_desp[y, costa_x:] = [180, 120, 40]

vis_desp = cv2.add(vis_desp, create_texture(h, w, 10))

vis_desp = cv2.GaussianBlur(vis_desp, (15, 15), 0)
ir_desp = cv2.GaussianBlur(ir_desp, (15, 15), 0)

vis_desp_3c = cv2.cvtColor(vis_desp, cv2.COLOR_GRAY2BGR)
cv2.imwrite(os.path.join(folder, "tarapaca_despejado_vis.jpg"), vis_desp_3c)
cv2.imwrite(os.path.join(folder, "tarapaca_despejado_ir.jpg"), ir_desp)

print("Imágenes generadas desde cero perfectamente.")
