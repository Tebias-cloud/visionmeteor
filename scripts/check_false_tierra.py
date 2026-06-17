import cv2
import numpy as np
import joblib

def check_false_tierra():
    vis = cv2.imread('backend/data/ejemplos_demostracion/1_huracan_vis.jpg', cv2.IMREAD_GRAYSCALE)
    ir = cv2.imread('backend/data/ejemplos_demostracion/1_huracan_ir.jpg')
    b, g, r = cv2.split(ir)
    
    # Reload model
    from backend.core.clasificador_v12 import ClasificadorV12
    clf = ClasificadorV12()
    
    res = clf.analizar('backend/data/ejemplos_demostracion/1_huracan_vis.jpg', 'backend/data/ejemplos_demostracion/1_huracan_ir.jpg', guardar=False)
    
    # res['resultados']['mascara_clases'] contains the actual class for each pixel.
    # Actually wait, ClasificadorV12 doesn't return the raw mask matrix in `resultados`.
    # Let me just compute it manually here using the loaded model.
    pass

