import cv2
import numpy as np
import pandas as pd
import os

def extract_multiscale_pixels(image_name, label_boxes):
    vis_path = f'backend/data/ejemplos_demostracion/{image_name}_vis.jpg'
    ir_path = f'backend/data/ejemplos_demostracion/{image_name}_ir.jpg'
    
    vis = cv2.imread(vis_path, cv2.IMREAD_GRAYSCALE)
    ir = cv2.imread(ir_path)
    b, g, r = cv2.split(ir)
    
    laplacian = cv2.Laplacian(vis, cv2.CV_64F)
    tex = cv2.normalize(np.abs(laplacian), None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    
    # Precompute multiscale blurs
    scales = [11, 31, 101, 301]
    maps = {'vis': vis, 'r': r, 'g': g, 'b': b, 'tex': tex}
    features = { 'vis': vis.flatten(), 'r': r.flatten(), 'g': g.flatten(), 'b': b.flatten(), 'tex': tex.flatten() }
    
    for s in scales:
        for name, mat in maps.items():
            blurred = cv2.blur(mat, (s, s))
            features[f'{name}_{s}'] = blurred.flatten()
            
    # Compile full feature array
    feature_names = list(features.keys())
    data_stack = np.column_stack([features[k] for k in feature_names])
    
    data = []
    w_img = vis.shape[1]
    
    for label, box in label_boxes.items():
        x1, y1, x2, y2 = box
        # Convert 2D box coords to 1D indices
        indices = []
        for y in range(y1, y2):
            indices.extend(range(y * w_img + x1, y * w_img + x2))
            
        indices = np.array(indices)
        idx_sample = np.random.choice(indices, min(2000, len(indices)), replace=False)
        
        for i in idx_sample:
            row = list(data_stack[i])
            row.append(label)
            data.append(row)
            
    return data, feature_names

all_data = []
feature_names = []

all_data.extend(extract_multiscale_pixels('1_huracan', {
    'TORMENTA': [400, 400, 600, 600],
    'CIRROS': [700, 100, 900, 300],
    'MAR': [50, 50, 200, 200]
})[0])

all_data.extend(extract_multiscale_pixels('3_archipielago', {
    'MAR': [100, 100, 400, 400],
    'TIERRA': [600, 600, 900, 900]
})[0])

all_data.extend(extract_multiscale_pixels('4_desierto_despejado', {
    'TIERRA': [700, 200, 1000, 800],
    'MAR': [50, 50, 200, 200]
})[0])

all_data.extend(extract_multiscale_pixels('5_estratocumulos', {
    'NUBE_BAJA_MEDIA': [300, 300, 700, 700],
    'MAR': [800, 800, 1000, 1000]
})[0])

data_tara, f_names = extract_multiscale_pixels('6_tarapaca_camanchaca', {
    'NUBE_BAJA_MEDIA': [100, 300, 300, 800],
    'TIERRA': [700, 100, 1000, 900]
})
all_data.extend(data_tara)
feature_names = f_names + ['label']

df = pd.DataFrame(all_data, columns=feature_names)
df = df.sample(frac=1).reset_index(drop=True)

os.makedirs('backend/data', exist_ok=True)
df.to_csv('backend/data/dataset_multiscale.csv', index=False)
print(f"Dataset multiscale generado con {len(df)} muestras.")
