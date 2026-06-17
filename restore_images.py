import os
import shutil

src_dir = r"c:\Users\Esteban\Desktop\visionmeteor\backend\data\inputs"
dst_dir = r"c:\Users\Esteban\Desktop\visionmeteor\backend\data\ejemplos_demostracion"

os.makedirs(dst_dir, exist_ok=True)

# Limpiar directorio de destino
for f in os.listdir(dst_dir):
    p = os.path.join(dst_dir, f)
    if os.path.isfile(p):
        os.remove(p)

# Copiar archivos reales
mapa = {
    "huracan_fuerte_vis.jpg": "huracan_vis.jpg",
    "huracan_fuerte_ir.jpg": "huracan_ir.jpg",
    "tarapaca_camanchaca.jpg": "tarapaca_camanchaca_vis.jpg",
    "tarapaca_camanchaca_ir.jpg": "tarapaca_camanchaca_ir.jpg",
    "tarapaca_despejado.jpg": "tarapaca_despejado_vis.jpg",
    "tarapaca_despejado_ir.jpg": "tarapaca_despejado_ir.jpg"
}

for src_name, dst_name in mapa.items():
    src_path = os.path.join(src_dir, src_name)
    dst_path = os.path.join(dst_dir, dst_name)
    if os.path.exists(src_path):
        shutil.copy(src_path, dst_path)

print("Imagenes reales restauradas en ejemplos_demostracion.")
