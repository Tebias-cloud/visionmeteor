import cv2
import numpy as np

def test_logic(name, vis_path, ir_path):
    visible_gris = cv2.imread(vis_path, cv2.IMREAD_GRAYSCALE)
    img_ir_color = cv2.imread(ir_path)
    canal_azul, canal_verde, canal_rojo = cv2.split(img_ir_color)
    h, w = visible_gris.shape
    
    conds = [
        (visible_gris < 80) & (canal_azul > canal_rojo),                      # MAR
        (visible_gris > 160) & (canal_rojo > 150) & (canal_verde < 80),       # TORMENTA
        (canal_rojo > 120) & (canal_verde > 120) & (canal_azul < 80),         # TIERRA_DESIERTO
        (visible_gris <= 160) & (canal_rojo > 150) & (canal_verde < 80),      # TIERRA_ANDES
        (visible_gris > 100) & (canal_verde > 100) & (canal_azul > 80) & (canal_rojo < 150), # NUBE_BAJA_MEDIA
        (visible_gris > 100) & (canal_rojo > 120),                            # CIRROS
        (visible_gris < 100),                                                 # TIERRA_DEFAULT
        (visible_gris >= 100)                                                 # NUBE_DEFAULT
    ]
    
    choices = [
        'MAR', 'TORMENTA', 'TIERRA', 'TIERRA', 'NUBE_BAJA_MEDIA', 'CIRROS', 'TIERRA', 'NUBE_BAJA_MEDIA'
    ]
    
    res = np.select(conds, choices, default='TIERRA')
    
    total = h * w
    print(f"[{name}]")
    for clase in set(choices):
        porc = np.sum(res == clase) / total * 100
        print(f"  {clase}: {porc:.1f}%")
    print("-" * 30)

demo_dir = 'backend/data/ejemplos_demostracion'
test_logic('HURACAN', f'{demo_dir}/1_huracan_vis.jpg', f'{demo_dir}/1_huracan_ir.jpg')
test_logic('DESIERTO', f'{demo_dir}/4_desierto_despejado_vis.jpg', f'{demo_dir}/4_desierto_despejado_ir.jpg')
test_logic('TARAPACA', f'{demo_dir}/6_tarapaca_camanchaca_vis.jpg', f'{demo_dir}/6_tarapaca_camanchaca_ir.jpg')
test_logic('ESTRATOS', f'{demo_dir}/5_estratocumulos_vis.jpg', f'{demo_dir}/5_estratocumulos_ir.jpg')
test_logic('ARCHIPIE', f'{demo_dir}/3_archipielago_vis.jpg', f'{demo_dir}/3_archipielago_ir.jpg')
test_logic('BLIZZARD', f'{demo_dir}/2_blizzard_vis.jpg', f'{demo_dir}/2_blizzard_ir.jpg')
