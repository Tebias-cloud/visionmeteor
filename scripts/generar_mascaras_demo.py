import cv2
import numpy as np

# 1024x1024 images
h, w = 1024, 1024

def save_mask(name, mask_array):
    cv2.imwrite(f'backend/data/ejemplos_demostracion/{name}_mask.png', mask_array)

# 1_huracan (100% Ocean)
m1 = np.zeros((h, w), dtype=np.uint8)
save_mask('1_huracan', m1)

# 2_blizzard (100% Land)
m2 = np.full((h, w), 255, dtype=np.uint8)
save_mask('2_blizzard', m2)

# 3_archipielago (50/50 roughly)
m3 = np.zeros((h, w), dtype=np.uint8)
m3[400:, 400:] = 255 # Bottom right is ice land
save_mask('3_archipielago', m3)

# 4_desierto_despejado (Right side is Land, Left is Ocean)
m4 = np.zeros((h, w), dtype=np.uint8)
m4[:, 300:] = 255
save_mask('4_desierto_despejado', m4)

# 5_estratocumulos (100% Ocean)
m5 = np.zeros((h, w), dtype=np.uint8)
save_mask('5_estratocumulos', m5)

# 6_tarapaca_camanchaca (Right side is Andes/Desert, Left is Ocean)
m6 = np.zeros((h, w), dtype=np.uint8)
m6[:, 400:] = 255
save_mask('6_tarapaca_camanchaca', m6)

print("Máscaras continentales estáticas generadas para los 6 ejemplos.")
