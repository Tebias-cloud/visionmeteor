import cv2
import numpy as np
import pandas as pd
import os

def extract_pixels(image_name, label_boxes):
    vis_path = f'backend/data/ejemplos_demostracion/{image_name}_vis.jpg'
    ir_path = f'backend/data/ejemplos_demostracion/{image_name}_ir.jpg'
    
    vis = cv2.imread(vis_path, cv2.IMREAD_GRAYSCALE)
    ir = cv2.imread(ir_path)
    b, g, r = cv2.split(ir)
    
    laplacian = cv2.Laplacian(vis, cv2.CV_64F)
    tex = cv2.normalize(np.abs(laplacian), None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    
    data = []
    
    for label, box in label_boxes.items():
        x1, y1, x2, y2 = box
        # Extract the region
        vis_roi = vis[y1:y2, x1:x2].flatten()
        r_roi = r[y1:y2, x1:x2].flatten()
        g_roi = g[y1:y2, x1:x2].flatten()
        b_roi = b[y1:y2, x1:x2].flatten()
        tex_roi = tex[y1:y2, x1:x2].flatten()
        
        # Subsample to avoid massive datasets (take 1000 pixels per box)
        idx = np.random.choice(len(vis_roi), min(2000, len(vis_roi)), replace=False)
        
        for i in idx:
            data.append([vis_roi[i], r_roi[i], g_roi[i], b_roi[i], tex_roi[i], label])
            
    return data

all_data = []

# Bounding boxes: [x1, y1, x2, y2]
# Image is 1024x1024

# 1_huracan: Eye wall is storm. Outer is cirrus. Edges are ocean.
all_data.extend(extract_pixels('1_huracan', {
    'TORMENTA': [400, 400, 600, 600],
    'CIRROS': [700, 100, 900, 300],
    'MAR': [50, 50, 200, 200]
}))

# 3_archipielago: Top left is ocean. Bottom right is ice/land.
all_data.extend(extract_pixels('3_archipielago', {
    'MAR': [100, 100, 400, 400],
    'TIERRA': [600, 600, 900, 900]
}))

# 4_desierto_despejado: Right side is desert land. Left is ocean/low cloud.
# We will use pure desert.
all_data.extend(extract_pixels('4_desierto_despejado', {
    'TIERRA': [700, 200, 1000, 800],
    'MAR': [50, 50, 200, 200]
}))

# 5_estratocumulos: Middle is low cloud. Bottom right is ocean.
all_data.extend(extract_pixels('5_estratocumulos', {
    'NUBE_BAJA_MEDIA': [300, 300, 700, 700],
    'MAR': [800, 800, 1000, 1000]
}))

# 6_tarapaca_camanchaca: Left is Camanchaca (low cloud). Right is Andes (Land).
all_data.extend(extract_pixels('6_tarapaca_camanchaca', {
    'NUBE_BAJA_MEDIA': [100, 300, 300, 800],
    'TIERRA': [700, 100, 1000, 900]
}))

df = pd.DataFrame(all_data, columns=['brillo', 'rojo', 'verde', 'azul', 'textura', 'label'])
df = df.sample(frac=1).reset_index(drop=True)

os.makedirs('backend/data', exist_ok=True)
df.to_csv('backend/data/dataset_real.csv', index=False)
print(f"Dataset real generado con {len(df)} muestras: backend/data/dataset_real.csv")
print(df['label'].value_counts())
