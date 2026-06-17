import cv2
import numpy as np

def simulate_v14(name, vis_path, ir_path):
    visible_gris = cv2.imread(vis_path, cv2.IMREAD_GRAYSCALE)
    img_ir_color = cv2.imread(ir_path)
    canal_azul = img_ir_color[:,:,0]
    canal_verde = img_ir_color[:,:,1]
    canal_rojo = img_ir_color[:,:,2]
    
    conds = [
        (visible_gris < 80) & (canal_azul > 80),                               # MAR (Oscuro y frío)
        (visible_gris > 140) & (canal_rojo > 150) & (canal_verde < 45),        # TORMENTA (Rojo extremo, nada de verde)
        (visible_gris > 80) & (canal_rojo > 150) & (canal_verde >= 45) & (canal_verde < 100), # ANDES (Nieve fría pero con algo de verde térmico)
        (canal_rojo > 120) & (canal_verde > 120) & (canal_azul < 80),          # DESIERTO (Amarillo térmico)
        (visible_gris > 100) & (canal_verde > 100) & (canal_azul > 80),        # NUBE BAJA (Blanco/Cian térmico)
        (visible_gris > 100) & (canal_rojo > 120) & (canal_verde >= 100),      # CIRROS
        (visible_gris < 100),                                                  # TIERRA FALLBACK
        (visible_gris >= 100)                                                  # NUBE FALLBACK
    ]
    
    choices = [
        'MAR', 'TORMENTA', 'TIERRA', 'TIERRA', 'NUBE_BAJA_MEDIA', 'CIRROS', 'TIERRA', 'NUBE_BAJA_MEDIA'
    ]
    
    res = np.select(conds, choices, default='TIERRA')
    
    h, w = visible_gris.shape
    total = h * w
    print(f"[{name}]")
    for clase in set(choices):
        porc = np.sum(res == clase) / total * 100
        if porc > 0:
            print(f"  {clase}: {porc:.1f}%")
    print("-" * 30)

demo_dir = 'backend/data/ejemplos_demostracion'
simulate_v14('HURACAN', f'{demo_dir}/1_huracan_vis.jpg', f'{demo_dir}/1_huracan_ir.jpg')
simulate_v14('TARAPACA', f'{demo_dir}/6_tarapaca_camanchaca_vis.jpg', f'{demo_dir}/6_tarapaca_camanchaca_ir.jpg')
simulate_v14('BLIZZARD', f'{demo_dir}/2_blizzard_vis.jpg', f'{demo_dir}/2_blizzard_ir.jpg')
