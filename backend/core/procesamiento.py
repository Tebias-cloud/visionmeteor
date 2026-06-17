import cv2
import numpy as np

def cargar_y_preparar_mapas(ruta_visible_rgb, ruta_infrarroja_ir):
    """
    Carga imágenes y pre-calcula todos los mapas de características.
    Este paso es crítico para optimizar el análisis píxel por píxel.
    """
    print("\n📂 PASO 1: Cargando imágenes y pre-calculando mapas...")
    
    # Cargar imagen visible RGB
    img_rgb = cv2.imread(ruta_visible_rgb)
    if img_rgb is None:
        raise ValueError(f"❌ No se pudo cargar: {ruta_visible_rgb}")
    print(f"   ✓ Imagen RGB cargada: {img_rgb.shape}")
    
    # Convertir a escala de grises para brillo
    visible_gris = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    print(f"   ✓ Mapa de brillo preparado: {visible_gris.shape}")
    
    # Pre-calcular mapa de textura (Laplaciano)
    print(f"   ⏳ Pre-calculando mapa de textura (Laplaciano)...")
    mapa_laplaciano = cv2.Laplacian(visible_gris, cv2.CV_64F)
    mapa_textura = np.abs(mapa_laplaciano)  # Usar valor absoluto
    print(f"   ✓ Mapa de textura calculado")
    
    # Cargar imagen IR en color
    img_ir_color = cv2.imread(ruta_infrarroja_ir)
    if img_ir_color is None:
        raise ValueError(f"❌ No se pudo cargar: {ruta_infrarroja_ir}")
    print(f"   ✓ Imagen IR cargada EN COLOR: {img_ir_color.shape}")
    
    # Redimensionar IR si es necesario
    h, w = img_rgb.shape[:2]
    if img_ir_color.shape[:2] != (h, w):
        img_ir_color = cv2.resize(img_ir_color, (w, h))
        print(f"   ✓ Imagen IR redimensionada a: {img_ir_color.shape}")
    
    # Separar canales IR (BGR)
    canal_b, canal_g, canal_r = cv2.split(img_ir_color)
    
    print(f"\n   📊 Estadísticas de canales IR:")
    print(f"      • Canal AZUL (calor):   min={canal_b.min()}, max={canal_b.max()}, avg={canal_b.mean():.1f}")
    print(f"      • Canal VERDE:          min={canal_g.min()}, max={canal_g.max()}, avg={canal_g.mean():.1f}")
    print(f"      • Canal ROJO (frialdad): min={canal_r.min()}, max={canal_r.max()}, avg={canal_r.mean():.1f}")
    
    # Preparar diccionario de mapas
    mapas = {
        'img_rgb': img_rgb,
        'visible_gris': visible_gris,
        'mapa_textura': mapa_textura,
        'canal_rojo': canal_r,
        'canal_azul': canal_b,
        'img_ir_color': img_ir_color,
        'dimensiones': (h, w)
    }
    
    print(f"\n   ✅ Todos los mapas preparados. Dimensiones: {h}x{w} = {h*w:,} píxeles")
    
    return mapas
