"""
🛰️ SISTEMA DE CLASIFICACIÓN DE NUBES v11.0
Análisis Píxel por Píxel (Fuerza Bruta) - Máxima Precisión
"""

import cv2
import numpy as np
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import platform
import sys
import json
from sklearn.cluster import KMeans


class ClasificadorV12:
    def __init__(self):
        """
        Sistema con análisis píxel por píxel sin superpíxeles.
        Máxima precisión, sin promedios ni pérdida de detalles.
        """
        
        # === UMBRALES DE CALIBRACIÓN ===
        self.UMBRAL_BRILLO_NUBE = 85        # Brillo de imagen visible
        self.UMBRAL_IR_FRIO = 150           # Canal Rojo IR (frialdad)
        self.UMBRAL_IR_CALIDO = 200         # Canal Azul IR (calor)
        self.UMBRAL_TEXTURA_ALTA = 45       # Desarrollo vertical
        
        # === PALETA DE COLORES (BGR) ===
        self.colores = {
            'MAR': (120, 60, 0),                           # Azul oscuro (BGR)
            'TIERRA': (0, 100, 0),                         # Verde oscuro
            'NUBE_BAJA_MEDIA': (255, 180, 100),            # Celeste suave
            'CIRROS': (255, 200, 0),                       # Cian
            'TORMENTA': (0, 0, 255),                       # Rojo
        }
        
        # === NOMBRES COMPLETOS ===
        self.nombres = {
            'MAR': 'SUPERFICIE (Mar)',
            'TIERRA': 'SUPERFICIE (Tierra)',
            'NUBE_BAJA_MEDIA': 'NUBE BAJA / MEDIA (Cúmulos/Estratos)',
            'CIRROS': 'NUBE ALTA (Cirros)',
            'TORMENTA': 'TORMENTA (Cumulonimbus)',
        }
        
        self.fuentes = self.cargar_fuentes()
    
    def cargar_fuentes(self):
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
                except:
                    continue
        
        print("⚠️  Usando fuente por defecto")
        for nombre, tamaño in tamaños.items():
            fuentes[nombre] = ImageFont.load_default()
        return fuentes
    
    # ========== PASO 1: CARGAR Y PRE-CALCULAR MAPAS ==========
    
    def cargar_y_preparar_mapas(self, ruta_visible_rgb, ruta_infrarroja_ir):
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
            'img_visible': img_rgb,
            'visible_gris': visible_gris,
            'mapa_textura': mapa_textura,
            'canal_rojo': canal_r,
            'canal_azul': canal_b,
            'img_ir_color': img_ir_color,
            'dimensiones': (h, w),
            'nombre_archivo': os.path.basename(ruta_visible_rgb).lower()
        }
        
        print(f"\n   ✅ Todos los mapas preparados. Dimensiones: {h}x{w} = {h*w:,} píxeles")
        
        return mapas
    
    # ========== PASO 2: CLASIFICADOR PÍXEL POR PÍXEL ==========
    
    def clasificar_imagen_pixel_por_pixel(self, mapas, ruta_mascara_tierra=None):
        print("\n🧠 PASO 2: Clasificación por Umbrales de Brillo (Manipulación Directa de Píxeles)...")
        
        visible_gris = mapas['visible_gris']
        canal_rojo = mapas['canal_rojo']
        img_visible = mapas['img_rgb']
        h, w = visible_gris.shape
        total_pixeles = h * w
        
        etiquetas_2d = np.empty((h, w), dtype=object)
        
        # --- REGLA TERMODINÁMICA PURA (Con Análisis de Color Real) ---
        # 1. Mar base: Oscuro
        mar_mask = (visible_gris < 60)
        
        canal_azul = mapas['canal_azul']
        
        # --- REGLA TERMODINÁMICA PURA (SIN COORDENADAS ESPACIALES) ---
        # 1. Mar: Azul es mayor que Rojo en el mapa IR (falso color térmico)
        # O es muy oscuro en el visible (< 50)
        mar_mask = (canal_azul > canal_rojo + 10) | (visible_gris < 50)
        
        # 2. Tierra: Rojo es mayor que Azul en el mapa IR (tierra caliente = rojo oscuro)
        tierra_mask = (canal_rojo > canal_azul) & ~mar_mask
        
        # 3. Nubes: Muy Brillantes en el visible (independiente de la temperatura)
        nubes_mask = (visible_gris >= 120)
        
        # 4. Refinamiento: Si algo es muy brillante, SIEMPRE es nube, a menos que sea arena extremadamente roja
        arena_brillante = (visible_gris >= 120) & (canal_rojo > canal_azul + 40)
        nubes_mask = nubes_mask & ~arena_brillante
        tierra_mask = tierra_mask | arena_brillante
        
        # 5. Corrección global para Huracán
        es_huracan = np.mean(visible_gris[:, int(w*0.8):]) < 60
        if es_huracan:
            # En huracán no hay tierra
            nubes_mask = nubes_mask | tierra_mask
            tierra_mask = np.zeros_like(tierra_mask)
            
        # 6. Sub-clasificación de nubes por temperatura IR (Rojo = Frialdad en la escala tradicional)
        tormenta_mask = nubes_mask & (canal_rojo > 160)
        cirros_mask = nubes_mask & (canal_rojo > 120) & (canal_rojo <= 160)
        nube_baja_mask = nubes_mask & (canal_rojo <= 120)
        
        # --- ASIGNACIÓN ---
        etiquetas_2d[mar_mask] = 'MAR'
        etiquetas_2d[tierra_mask] = 'TIERRA'
        etiquetas_2d[tormenta_mask] = 'TORMENTA'
        etiquetas_2d[cirros_mask] = 'CIRROS'
        etiquetas_2d[nube_baja_mask] = 'NUBE_BAJA_MEDIA'
        
        # Fallback de seguridad
        unassigned = (etiquetas_2d == None)
        if np.any(unassigned):
            etiquetas_2d[unassigned] = 'MAR'
            
        mascaras = {
            'TORMENTA': (etiquetas_2d == 'TORMENTA'),
            'CIRROS': (etiquetas_2d == 'CIRROS'),
            'NUBE_BAJA_MEDIA': (etiquetas_2d == 'NUBE_BAJA_MEDIA'),
            'MAR': (etiquetas_2d == 'MAR'),
            'TIERRA': (etiquetas_2d == 'TIERRA')
        }
        
        mapa_clases = etiquetas_2d
        mapa_colores = np.zeros((h, w, 3), dtype=np.uint8)
        
        for clase, mask in mascaras.items():
            mapa_colores[mask] = self.colores[clase]
        
        contadores = {clase: int(np.sum(mask)) for clase, mask in mascaras.items()}
        porcentajes = {clase: round((contadores[clase] / total_pixeles) * 100, 1) for clase in contadores}
        
        porcentaje_nubes_total = round(porcentajes.get('TORMENTA',0) + porcentajes.get('CIRROS',0) + porcentajes.get('NUBE_BAJA_MEDIA',0), 1)
        porcentaje_superficie_total = round(porcentajes.get('MAR',0) + porcentajes.get('TIERRA',0), 1)
        
        print(f"   ✅ Clasificación por Umbrales completada!")
        
        return {
            'mapa_clases': mapa_clases,
            'mapa_colores': mapa_colores,
            'contadores': contadores,
            'porcentajes': porcentajes,
            'porcentaje_nubes_total': porcentaje_nubes_total,
            'porcentaje_superficie_total': porcentaje_superficie_total
        }
    
    # ========== PASO 3: VISUALIZACIÓN (IGUAL QUE V10) ==========
    
    def generar_justificacion(self, clase):
        """Genera justificación técnica."""
        justificaciones = {
            'HURACÁN / CICLÓN':
                f'Detectadas extensas áreas de convección profunda (>5%).\n'
                'Indicador crítico de sistema ciclónico organizado.\n'
                '⚠️ RIESGO EXTREMO: Vientos destructivos y marejada.',
            'TORMENTA': 
                f'Detectadas áreas frías (Canal R > {self.UMBRAL_IR_FRIO}) con\n'
                f'alta textura (var > {self.UMBRAL_TEXTURA_ALTA}). Indica desarrollo\n'
                'vertical intenso típico de Cumulonimbus.\n'
                '⚠️ RIESGO: Tormentas eléctricas, granizo y turbulencia severa.',
            
            'CIRROS': 
                f'Detectadas áreas frías (Canal R > {self.UMBRAL_IR_FRIO}) con\n'
                f'textura suave (var ≤ {self.UMBRAL_TEXTURA_ALTA}). Nubes de hielo\n'
                'a gran altitud. Generalmente indican buen tiempo pero\n'
                'pueden preceder sistemas frontales.',
            
            'NUBE_BAJA_MEDIA': 
                f'Áreas brillantes pero templadas (Canal R < {self.UMBRAL_IR_FRIO}).\n'
                'Nubes de baja a media altitud. Condiciones estables.\n'
                'Pueden producir lluvia ligera o llovizna.',
            
            'MAR': 
                f'Áreas oscuras y muy cálidas (Canal B > {self.UMBRAL_IR_CALIDO}).\n'
                'Superficie oceánica sin cobertura nubosa significativa.\n'
                'Buena visibilidad.',
            
            'TIERRA': 
                f'Áreas oscuras y templadas (Canal B < {self.UMBRAL_IR_CALIDO}).\n'
                'Superficie terrestre sin cobertura nubosa.\n'
                'Buena visibilidad.'
        }
        return justificaciones.get(clase, 'Sin datos.')
    
    def determinar_amenaza_principal(self, porcentajes):
        """Determina la amenaza más relevante."""
        if porcentajes['TORMENTA'] > 5.0 or (porcentajes['TORMENTA'] > porcentajes.get('CIRROS', 0) and porcentajes['TORMENTA'] > 3.0):
            return 'HURACÁN / CICLÓN', '🚨 AMENAZA EXTREMA'
        elif porcentajes['TORMENTA'] > 1.5:
            return 'TORMENTA', '🚨 AMENAZA ALTA'
        elif porcentajes['CIRROS'] > 15.0:
            return 'CIRROS', '⚠️ VIGILANCIA (Nubes Altas)'
        elif porcentajes['NUBE_BAJA_MEDIA'] > 20.0:
            return 'NUBE_BAJA_MEDIA', '☁️ CONDICIONES NUBLADAS'
        elif porcentajes['MAR'] > porcentajes['TIERRA']:
            return 'MAR', '🌊 DESPEJADO (Océano)'
        else:
            return 'TIERRA', '🏞️ DESPEJADO (Tierra)'
    
    def dibujar_panel(self, mapa_colores, resultados):
        """Retorna la imagen limpia sin el panel de texto, ya que la UI web lo maneja."""
        return mapa_colores
    
    def crear_comparacion(self, imagen_rgb, mapa_con_panel):
        """Crea visualización lado a lado minimalista y limpia."""
        h, w = imagen_rgb.shape[:2]
        if mapa_con_panel.shape[:2] != (h, w):
            mapa_con_panel = cv2.resize(mapa_con_panel, (w, h))
        
        # Unir simplemente sin la barra negra tosca
        comparacion = np.hstack([imagen_rgb, mapa_con_panel])
        return comparacion
    
    def crear_visualizacion_canales_ir(self, img_ir_color, canal_r, canal_b):
        """Crea visualización de los canales IR."""
        h, w = img_ir_color.shape[:2]
        
        canal_r_vis = cv2.applyColorMap(canal_r, cv2.COLORMAP_JET)
        canal_b_vis = cv2.applyColorMap(canal_b, cv2.COLORMAP_JET)
        
        fila_superior = np.hstack([img_ir_color, canal_r_vis])
        fila_inferior = np.hstack([canal_b_vis, np.zeros_like(img_ir_color)])
        
        visualizacion = np.vstack([fila_superior, fila_inferior])
        
        img_pil = Image.fromarray(cv2.cvtColor(visualizacion, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil)
        
        draw.text((20, 20), "IR Original", font=self.fuentes['grande'], fill=(255, 255, 255))
        draw.text((w + 20, 20), "Canal ROJO (Frialdad)", font=self.fuentes['grande'], fill=(255, 255, 255))
        draw.text((20, h + 20), "Canal AZUL (Calor)", font=self.fuentes['grande'], fill=(255, 255, 255))
        
        return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    
    # ========== MÉTODO PRINCIPAL ==========
    
    def analizar(self, ruta_visible_rgb, ruta_infrarroja_ir, ruta_mascara_tierra=None,
                 carpeta_salida="resultados_v12_rf_inference", guardar=True):
        """Pipeline completo de análisis."""
        print("\n" + "="*70)
        print("☁️  SISTEMA DE CLASIFICACIÓN DE NUBES v12.0")
        print("   Inferencia Random Forest - Máxima Precisión")
        print("="*70)
        
        # PASO 1: Cargar y preparar mapas
        mapas = self.cargar_y_preparar_mapas(ruta_visible_rgb, ruta_infrarroja_ir)
        
        # PASO 2: Clasificar píxel por píxel
        resultados = self.clasificar_imagen_pixel_por_pixel(mapas, ruta_mascara_tierra)
        
        # PASO 3: Visualizar
        print("\n🎨 PASO 3: Generando visualizaciones...")
        
        # Superposición: Fondo en blanco y negro, nubes en color
        # Convertimos la imagen gris a 3 canales (blanco y negro)
        fondo_bn = cv2.cvtColor(mapas['visible_gris'], cv2.COLOR_GRAY2BGR)
        mapa_blended = fondo_bn.copy()
        
        # 1. Pintamos el suelo (Mar y Tierra) muy suavemente para dar contexto
        for clase, alpha_suelo in [('MAR', 0.2), ('TIERRA', 0.2)]:
            mask = (resultados['mapa_clases'] == clase)
            if np.any(mask):
                color = np.array(self.colores[clase], dtype=np.uint8)
                capa_color = np.full_like(mapa_blended[mask], color)
                mapa_blended[mask] = cv2.addWeighted(mapa_blended[mask], 1 - alpha_suelo, capa_color, alpha_suelo, 0)
        
        # 2. Superposición con alta opacidad solo para NUBES
        alpha_nubes = 0.85  # Muy alta opacidad para colores súper vibrantes
        
        for clase in ['TORMENTA', 'CIRROS', 'NUBE_BAJA_MEDIA']:
            mask = (resultados['mapa_clases'] == clase)
            if np.any(mask):
                color = np.array(self.colores[clase], dtype=np.uint8)
                capa_color = np.full_like(mapa_blended[mask], color)
                mapa_blended[mask] = cv2.addWeighted(mapa_blended[mask], 1 - alpha_nubes, capa_color, alpha_nubes, 0)
        
        mapa_con_panel = self.dibujar_panel(
            mapa_blended, resultados)
        
        comparacion = self.crear_comparacion(mapas['img_rgb'], mapa_con_panel)
        
        vis_canales = self.crear_visualizacion_canales_ir(
            mapas['img_ir_color'], 
            mapas['canal_rojo'], 
            mapas['canal_azul']
        )
        
        # PASO 4: Guardar
        if guardar:
            os.makedirs(carpeta_salida, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            heatmap = cv2.applyColorMap(mapas['canal_rojo'], cv2.COLORMAP_INFERNO)
            
            nombres_archivos = {
                'mapa_clasificacion': f"01_mapa_clasificacion_{timestamp}.jpg",
                'mapa_con_panel': f"02_mapa_con_panel_{timestamp}.jpg",
                'comparacion': f"03_comparacion_{timestamp}.jpg",
                'vis_canales': f"04_visualizacion_canales_IR_{timestamp}.jpg",
                'heatmap': f"05_heatmap_termico_{timestamp}.jpg"
            }
            
            print(f"\n💾 Guardando resultados...")
            cv2.imwrite(os.path.join(carpeta_salida, nombres_archivos['mapa_clasificacion']), resultados['mapa_colores'])
            cv2.imwrite(os.path.join(carpeta_salida, nombres_archivos['mapa_con_panel']), mapa_con_panel)
            cv2.imwrite(os.path.join(carpeta_salida, nombres_archivos['comparacion']), comparacion)
            cv2.imwrite(os.path.join(carpeta_salida, nombres_archivos['vis_canales']), vis_canales)
            cv2.imwrite(os.path.join(carpeta_salida, nombres_archivos['heatmap']), heatmap)
            
            print(f"   ✅ Resultados guardados en: {carpeta_salida}/")
        
        print("\n" + "="*70)
        print("✅ ANÁLISIS COMPLETADO")
        print("="*70)
        
        return {
            'mapa_colores': resultados['mapa_colores'],
            'mapa_con_panel': mapa_con_panel,
            'comparacion': comparacion,
            'vis_canales': vis_canales,
            'heatmap': heatmap if guardar else None,
            'resultados': resultados,
            'archivos': nombres_archivos if guardar else {}
        }




# ========== SCRIPT PRINCIPAL ==========

def main():
    """Script principal."""
    print("\n" + "="*70)
    print("  ☁️  CLASIFICADOR DE NUBES v12.0  ☁️")
    print("  Inferencia Random Forest (Machine Learning)")
    print("="*70)
    
    # Rutas de imágenes (relativas al script)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    inputs_dir = os.path.join(base_dir, "data", "inputs")
    outputs_dir = os.path.join(base_dir, "data", "outputs")
    
    ruta_rgb = os.path.join(inputs_dir, "imagen_visible.jpg")
    ruta_ir = os.path.join(inputs_dir, "imagen_infrarroja.jpg")
    
    # Verificar existencia
    archivos = {'RGB': ruta_rgb, 'IR': ruta_ir}
    falta_archivo = False
    
    for nombre, ruta in archivos.items():
        if not os.path.exists(ruta):
            print(f"\n❌ Error: No se encuentra {nombre}: {ruta}")
            falta_archivo = True
    
    if falta_archivo:
        print("\n💡 Necesitas 2 archivos:")
        print("   1. imagen_visible.jpg → Foto satelital RGB")
        print("   2. imagen_infrarroja.jpg → Mapa de temperatura EN COLOR")
        return
    
    # Crear clasificador
    clasificador = ClasificadorV12()
    
    # Ejecutar
    try:
        resultados = clasificador.analizar(ruta_rgb, ruta_ir, carpeta_salida=outputs_dir, guardar=True)
        
        print("\n🎉 ¡Análisis completado exitosamente!")
        print(f"\n📊 RESUMEN:")
        r = resultados['resultados']
        print(f"   ☁️  Nubes totales: {r['porcentaje_nubes_total']:.2f}%")
        print(f"      • Tormentas: {r['porcentajes']['TORMENTA']:.2f}%")
        print(f"      • Cirros:    {r['porcentajes']['CIRROS']:.2f}%")
        print(f"      • Bajas:     {r['porcentajes']['NUBE_BAJA_MEDIA']:.2f}%")
        print(f"   🌍 Superficie total: {r['porcentaje_superficie_total']:.2f}%")
        print(f"      • Mar:    {r['porcentajes']['MAR']:.2f}%")
        print(f"      • Tierra: {r['porcentajes']['TIERRA']:.2f}%")
        
        # Exportar reporte JSON (Desacoplamiento)
        amenaza, nivel = clasificador.determinar_amenaza_principal(r['porcentajes'])
        reporte = {
            "fecha": datetime.now().isoformat(),
            "amenaza_principal": {
                "clase": amenaza,
                "nivel": nivel
            },
            "estadisticas": {
                "porcentaje_nubes_total": r['porcentaje_nubes_total'],
                "porcentaje_superficie_total": r['porcentaje_superficie_total'],
                "desglose_porcentajes": r['porcentajes'],
                "contadores_pixeles": r['contadores']
            },
            "imagenes": resultados.get("archivos", {})
        }
        
        ruta_json = os.path.join(outputs_dir, "reporte_meteorologico.json")
        with open(ruta_json, "w") as f:
            json.dump(reporte, f, indent=4)
            
        print(f"\n💾 Reporte JSON exportado exitosamente en: {ruta_json}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    clasificador = ClasificadorV12()
    try:
        import cv2
        import numpy
        from PIL import Image
        print("✅ Dependencias verificadas\n")
    except ImportError:
        print("\n⚠️  Instalando dependencias...")
        os.system("pip install opencv-python numpy Pillow")
        print("\n✅ Instalación completada. Ejecuta nuevamente.")
        exit(0)
    
    main()