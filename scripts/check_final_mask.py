import cv2
import numpy as np
import os
import glob

def check_mask():
    out_dir = 'backend/data/outputs'
    files = glob.glob(f'{out_dir}/03_comparacion_*.jpg')
    if not files:
        print("No files found")
        return
    mask_path = max(files, key=os.path.getctime)
    
    mask = cv2.imread(mask_path)
    if mask is None:
        print(f"Could not read {mask_path}")
        return
        
    h, w, _ = mask.shape
    right_half = mask[:, w//2:]
    
    # Check left half of the right_half (which corresponds to the ocean/cloud)
    # Check right half of the right_half (which corresponds to the Andes)
    sub_w = right_half.shape[1]
    cloud_zone = right_half[:, :sub_w//2]
    andes_zone = right_half[:, sub_w//2:]
    
    def get_color_percentages(half):
        total = half.shape[0] * half.shape[1]
        b_half, g_half, r_half = cv2.split(half)
        
        is_black = (b_half < 50) & (g_half < 50) & (r_half < 50)  # MAR
        is_grey = (b_half > 150) & (g_half > 150) & (r_half > 150) & (b_half < 250) # NUBE BAJA
        is_green = (g_half > 100) & (b_half < 50) & (r_half < 50) # TIERRA
        is_red = (r_half > 150) & (g_half < 50) & (b_half < 50)   # TORMENTA
        is_white = (b_half > 250) & (g_half > 250) & (r_half > 250) # CIRROS
        
        return {
            'Ocean/Black': np.sum(is_black) / total * 100,
            'Cloud/Grey': np.sum(is_grey) / total * 100,
            'Land/Green': np.sum(is_green) / total * 100,
            'Storm/Red': np.sum(is_red) / total * 100,
            'Cirrus/White': np.sum(is_white) / total * 100
        }
        
    print(f"[TARAPACA MASK ANALYSIS]")
    print(f"Cloud Zone (Left side of the mask):")
    print(get_color_percentages(cloud_zone))
    print(f"Andes Zone (Right side of the mask):")
    print(get_color_percentages(andes_zone))
    print("-" * 30)

check_mask()
