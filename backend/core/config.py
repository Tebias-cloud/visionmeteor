import platform
import os
from PIL import ImageFont

# === UMBRALES DE CALIBRACIÓN ===
UMBRAL_BRILLO_NUBE = 85        # Brillo de imagen visible
UMBRAL_IR_FRIO = 150           # Canal Rojo IR (frialdad)
UMBRAL_IR_CALIDO = 200         # Canal Azul IR (calor)
UMBRAL_TEXTURA_ALTA = 45       # Desarrollo vertical

# === PALETA DE COLORES (BGR) ===
COLORES = {
    'MAR': (0, 0, 0),                              # Negro
    'TIERRA': (0, 100, 0),                         # Verde oscuro
    'NUBE_BAJA_MEDIA': (180, 180, 180),           # Gris
    'CIRROS': (255, 200, 0),                       # Cian
    'TORMENTA': (0, 0, 255),                       # Rojo
}

# === NOMBRES COMPLETOS ===
NOMBRES = {
    'MAR': 'SUPERFICIE (Mar)',
    'TIERRA': 'SUPERFICIE (Tierra)',
    'NUBE_BAJA_MEDIA': 'NUBE BAJA / MEDIA (Cúmulos/Estratos)',
    'CIRROS': 'NUBE ALTA (Cirros)',
    'TORMENTA': 'TORMENTA (Cumulonimbus)',
}

def cargar_fuentes():
    """Carga fuentes del sistema."""
    fuentes = {}
    sistema = platform.system()
    
    if sistema == "Darwin":
        rutas = ["/System/Library/Fonts/Helvetica.ttc"]
    elif sistema == "Windows":
        rutas = ["C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/arialbd.ttf"]
    else:
        rutas = ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
    
    tamaños = {'titulo': 42, 'grande': 34, 'mediano': 26, 'pequeño': 20}
    
    for ruta in rutas:
        if os.path.exists(ruta):
            try:
                for nombre, tamaño in tamaños.items():
                    fuentes[nombre] = ImageFont.truetype(ruta, tamaño)
                print(f"✅ Fuentes cargadas: {os.path.basename(ruta)}")
                return fuentes
            except Exception:
                continue
    
    print("Usando fuente por defecto")
    for nombre, tamaño in tamaños.items():
        fuentes[nombre] = ImageFont.load_default()
    return fuentes

FUENTES = cargar_fuentes()
