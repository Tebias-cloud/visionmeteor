import cv2
import numpy as np
import os

base_dir = r"c:\Users\Esteban\Desktop\visionmeteor\backend\data"
demo_dir = os.path.join(base_dir, "ejemplos_demostracion")
inputs_dir = os.path.join(base_dir, "inputs")
os.makedirs(inputs_dir, exist_ok=True)

# Load original tarapaca
img_path = os.path.join(demo_dir, "6_tarapaca_camanchaca_vis.jpg")
img_rgb = cv2.imread(img_path)

if img_rgb is None:
    print("No se encontró la original. Usando sintética base.")
    img_rgb = np.zeros((1024, 1024, 3), dtype=np.uint8)
    img_rgb[:, :450] = [30, 30, 30]
    img_rgb[:, 450:] = [100, 100, 100]

h, w = img_rgb.shape[:2]
gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

x_coords = np.tile(np.arange(w), (h, 1))
ocean_mask = x_coords < int(w*0.42)
land_mask = x_coords >= int(w*0.42)

# --- ESCENARIO 1: DESPEJADO ---
despejado = np.zeros_like(gray)
# Océano: 0 a 60
despejado[ocean_mask] = np.clip(gray[ocean_mask], 0, 60)
despejado[ocean_mask] = np.where(despejado[ocean_mask] > 50, 30, despejado[ocean_mask]) # Forzar más oscuro
# Tierra: 61 a 150
despejado[land_mask] = np.clip(gray[land_mask], 61, 150)
despejado[land_mask] = np.where(despejado[land_mask] < 70, 100, despejado[land_mask]) # Forzar más brillante que el mar

despejado_color = cv2.cvtColor(despejado, cv2.COLOR_GRAY2BGR)

# --- ESCENARIO 2: CAMANCHACA ---
camanchaca = despejado.copy()
cloud_mask_camanchaca = (x_coords > int(w*0.35)) & (x_coords < int(w*0.55))
noise = np.random.randint(0, 100, size=(h, w))
cloud_mask_camanchaca = cloud_mask_camanchaca & (noise > 20)
camanchaca[cloud_mask_camanchaca] = 180 + np.random.randint(0, 50, size=np.sum(cloud_mask_camanchaca))
camanchaca_color = cv2.cvtColor(camanchaca, cv2.COLOR_GRAY2BGR)

# --- ESCENARIO 3: NUBOSIDAD PARCIAL ---
parcial = despejado.copy()
for i in range(12):
    cx = np.random.randint(int(w*0.2), int(w*0.9))
    cy = np.random.randint(0, h)
    cv2.ellipse(parcial, (cx, cy), (120, 30), np.random.randint(0,180), 0, 360, (200), -1)

# Difuminar para que parezcan nubes reales
parcial = cv2.GaussianBlur(parcial, (21, 21), 0)
# Asegurar que las nubes queden arriba de 150
parcial[parcial > 130] = np.clip(parcial[parcial > 130] + 50, 160, 255)

parcial_color = cv2.cvtColor(parcial, cv2.COLOR_GRAY2BGR)

# Save them to inputs/
cv2.imwrite(os.path.join(inputs_dir, "tarapaca_despejado.jpg"), despejado_color)
cv2.imwrite(os.path.join(inputs_dir, "tarapaca_camanchaca.jpg"), camanchaca_color)
cv2.imwrite(os.path.join(inputs_dir, "tarapaca_nubosidad_parcial.jpg"), parcial_color)

# Create IR maps for pipeline
def make_ir(img_gray):
    ir = np.zeros((h, w, 3), dtype=np.uint8)
    ir[img_gray <= 60] = [200, 50, 0]
    ir[(img_gray > 60) & (img_gray <= 150)] = [50, 200, 50]
    ir[img_gray > 150] = [0, 50, 200]
    return ir

cv2.imwrite(os.path.join(inputs_dir, "tarapaca_despejado_ir.jpg"), make_ir(despejado))
cv2.imwrite(os.path.join(inputs_dir, "tarapaca_camanchaca_ir.jpg"), make_ir(camanchaca))
cv2.imwrite(os.path.join(inputs_dir, "tarapaca_nubosidad_parcial_ir.jpg"), make_ir(parcial))

print("✅ Entornos sintéticos calibrados exitosamente.")
