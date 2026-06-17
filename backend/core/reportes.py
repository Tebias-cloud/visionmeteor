import cv2
import numpy as np
from PIL import Image, ImageDraw
from backend.core.config import FUENTES, UMBRAL_IR_FRIO, UMBRAL_TEXTURA_ALTA, UMBRAL_IR_CALIDO

def determinar_amenaza_principal(porcentajes):
    """Determina la amenaza más relevante."""
    if porcentajes['TORMENTA'] > 5.0 or (porcentajes['TORMENTA'] > porcentajes.get('CIRROS', 0) and porcentajes['TORMENTA'] > 3.0):
        return 'HURACÁN / CICLÓN', '🚨 AMENAZA EXTREMA'
    elif porcentajes['TORMENTA'] > 1.5:
        return 'TORMENTA', '🚨 AMENAZA ALTA'
    elif porcentajes['CIRROS'] > 15.0:
        return 'CIRROS', '⚠️ VIGILANCIA (Nubes Altas)'
    elif porcentajes['NUBE_BAJA_MEDIA'] > 20.0:
        return 'NUBE_BAJA_MEDIA', '☁️ CONDICIONES NUBLADAS'
    elif porcentajes['MAR'] > porcentajes.get('TIERRA', 0):
        return 'MAR', '🌊 DESPEJADO (Océano)'
    else:
        return 'TIERRA', '🏞️ DESPEJADO (Tierra)'

def generar_justificacion(clase):
    """Genera justificación técnica."""
    justificaciones = {
        'HURACÁN / CICLÓN':
            f'Detectadas extensas áreas de convección profunda (>5%).\n'
            'Indicador crítico de sistema ciclónico organizado.\n'
            '⚠️ RIESGO EXTREMO: Vientos destructivos y marejada.',
        'TORMENTA': 
            f'Detectadas áreas frías (Canal R > {UMBRAL_IR_FRIO}) con\n'
            f'alta textura (var > {UMBRAL_TEXTURA_ALTA}). Indica desarrollo\n'
            'vertical intenso típico de Cumulonimbus.\n'
            '⚠️ RIESGO: Tormentas eléctricas, granizo y turbulencia severa.',
        
        'CIRROS': 
            f'Detectadas áreas frías (Canal R > {UMBRAL_IR_FRIO}) con\n'
            f'textura suave (var ≤ {UMBRAL_TEXTURA_ALTA}). Nubes de hielo\n'
            'a gran altitud. Generalmente indican buen tiempo pero\n'
            'pueden preceder sistemas frontales.',
        
        'NUBE_BAJA_MEDIA': 
            f'Áreas brillantes pero templadas (Canal R < {UMBRAL_IR_FRIO}).\n'
            'Nubes de baja a media altitud. Condiciones estables.\n'
            'Pueden producir lluvia ligera o llovizna.',
        
        'MAR': 
            f'Áreas oscuras y muy cálidas (Canal B > {UMBRAL_IR_CALIDO}).\n'
            'Superficie oceánica sin cobertura nubosa significativa.\n'
            'Buena visibilidad.',
        
        'TIERRA': 
            f'Áreas oscuras y templadas (Canal B < {UMBRAL_IR_CALIDO}).\n'
            'Superficie terrestre sin cobertura nubosa.\n'
            'Buena visibilidad.'
    }
    return justificaciones.get(clase, 'Sin datos.')

def dibujar_panel(imagen, resultados):
    """Retorna la imagen limpia sin el panel de texto, ya que la UI web lo maneja."""
    return imagen

def crear_comparacion(imagen_rgb, mapa_con_panel):
    """Crea visualización lado a lado minimalista y limpia."""
    h, w = imagen_rgb.shape[:2]
    if mapa_con_panel.shape[:2] != (h, w):
        mapa_con_panel = cv2.resize(mapa_con_panel, (w, h))
    
    comparacion = np.hstack([imagen_rgb, mapa_con_panel])
    return comparacion

def crear_visualizacion_canales_ir(img_ir_color, canal_r, canal_b):
    """Crea visualización de los canales IR."""
    h, w = img_ir_color.shape[:2]
    
    canal_r_vis = cv2.applyColorMap(canal_r, cv2.COLORMAP_JET)
    canal_b_vis = cv2.applyColorMap(canal_b, cv2.COLORMAP_JET)
    
    fila_superior = np.hstack([img_ir_color, canal_r_vis])
    fila_inferior = np.hstack([canal_b_vis, np.zeros_like(img_ir_color)])
    
    visualizacion = np.vstack([fila_superior, fila_inferior])
    
    img_pil = Image.fromarray(cv2.cvtColor(visualizacion, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    
    draw.text((20, 20), "IR Original", font=FUENTES.get('grande'), fill=(255, 255, 255))
    draw.text((w + 20, 20), "Canal ROJO (Frialdad)", font=FUENTES.get('grande'), fill=(255, 255, 255))
    draw.text((20, h + 20), "Canal AZUL (Calor)", font=FUENTES.get('grande'), fill=(255, 255, 255))
    
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
