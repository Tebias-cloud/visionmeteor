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


class ClasificadorNubesV11:
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
            'MAR': (0, 0, 0),                              # Negro
            'TIERRA': (0, 100, 0),                         # Verde oscuro
            'NUBE_BAJA_MEDIA': (180, 180, 180),           # Gris
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
            'visible_gris': visible_gris,
            'mapa_textura': mapa_textura,
            'canal_rojo': canal_r,
            'canal_azul': canal_b,
            'img_ir_color': img_ir_color,
            'dimensiones': (h, w)
        }
        
        print(f"\n   ✅ Todos los mapas preparados. Dimensiones: {h}x{w} = {h*w:,} píxeles")
        
        return mapas
    
    # ========== PASO 2: CLASIFICADOR PÍXEL POR PÍXEL ==========
    
    def clasificar_pixel_v11(self, brillo, textura, canal_rojo, canal_azul):
        """
        Clasificador jerárquico aplicado a un ÚNICO píxel.
        
        Args:
            brillo: Intensidad del píxel en escala de grises (0-255)
            textura: Magnitud del Laplaciano en ese píxel
            canal_rojo: Intensidad del canal R de IR (frialdad, 255=muy frío)
            canal_azul: Intensidad del canal B de IR (calor, 255=muy cálido)
            
        Returns:
            str: Clase asignada al píxel
        """
        # --- NIVEL 1: ¿ES NUBE O SUPERFICIE? ---
        
        if brillo > self.UMBRAL_BRILLO_NUBE:
            # ES NUBE (brillante en imagen visible)
            
            # --- NIVEL 2: SUB-CLASIFICACIÓN DE NUBES ---
            
            # TORMENTA: Muy fría (roja en IR) + Alta textura
            if canal_rojo > self.UMBRAL_IR_FRIO and textura > self.UMBRAL_TEXTURA_ALTA:
                return "TORMENTA"
            
            # CIRROS: Muy fría (roja en IR) + Baja textura
            elif canal_rojo > self.UMBRAL_IR_FRIO:
                return "CIRROS"
            
            # NUBE BAJA/MEDIA: No es fría
            else:
                return "NUBE_BAJA_MEDIA"
        
        else:
            # NO ES NUBE (oscura en imagen visible)
            
            # MAR: Muy cálida (azul en IR)
            if canal_azul > self.UMBRAL_IR_CALIDO:
                return "MAR"
            
            # TIERRA: No es muy cálida
            else:
                return "TIERRA"
    
    def clasificar_imagen_pixel_por_pixel(self, mapas):
        """
        Clasifica cada píxel de la imagen usando vectorización de NumPy.
        Este proceso es extremadamente RÁPIDO y PRECISO.
        """
        print("\n🔬 PASO 2: Clasificando píxel por píxel (VECTORIZADO)...")
        
        h, w = mapas['dimensiones']
        total_pixeles = h * w
        
        print(f"   ⏳ Procesando {total_pixeles:,} píxeles de forma paralela...")
        
        # Extraer mapas
        visible_gris = mapas['visible_gris']
        mapa_textura = mapas['mapa_textura']
        canal_rojo = mapas['canal_rojo']
        canal_azul = mapas['canal_azul']
        
        # === VECTORIZACIÓN NUMPY: Evaluación concurrente ===
        
        # 1. Crear máscaras booleanas base (Condiciones lógicas)
        cond_nube = visible_gris > self.UMBRAL_BRILLO_NUBE
        cond_no_nube = ~cond_nube
        cond_frio = canal_rojo > self.UMBRAL_IR_FRIO
        cond_textura_alta = mapa_textura > self.UMBRAL_TEXTURA_ALTA
        cond_calido = canal_azul > self.UMBRAL_IR_CALIDO
        
        # 2. Crear máscaras para cada clase respetando la lógica de negocio
        mascara_tormenta = cond_nube & cond_frio & cond_textura_alta
        mascara_cirros = cond_nube & cond_frio & ~cond_textura_alta
        mascara_nube_baja = cond_nube & ~cond_frio
        mascara_mar = cond_no_nube & cond_calido
        mascara_tierra = cond_no_nube & ~cond_calido
        
        # 3. Asignar clases y colores en bloque (eliminando el ciclo for)
        mapa_clases = np.empty((h, w), dtype=object)
        mapa_colores = np.zeros((h, w, 3), dtype=np.uint8)
        
        mapa_clases[mascara_tormenta] = 'TORMENTA'
        mapa_colores[mascara_tormenta] = self.colores['TORMENTA']
        
        mapa_clases[mascara_cirros] = 'CIRROS'
        mapa_colores[mascara_cirros] = self.colores['CIRROS']
        
        mapa_clases[mascara_nube_baja] = 'NUBE_BAJA_MEDIA'
        mapa_colores[mascara_nube_baja] = self.colores['NUBE_BAJA_MEDIA']
        
        mapa_clases[mascara_mar] = 'MAR'
        mapa_colores[mascara_mar] = self.colores['MAR']
        
        mapa_clases[mascara_tierra] = 'TIERRA'
        mapa_colores[mascara_tierra] = self.colores['TIERRA']
        
        # 4. Calcular contadores usando np.sum sobre las máscaras booleanas
        contadores = {
            'MAR': int(np.sum(mascara_mar)),
            'TIERRA': int(np.sum(mascara_tierra)),
            'NUBE_BAJA_MEDIA': int(np.sum(mascara_nube_baja)),
            'CIRROS': int(np.sum(mascara_cirros)),
            'TORMENTA': int(np.sum(mascara_tormenta))
        }
        
        print(f"   ✅ {total_pixeles:,} píxeles clasificados exitosamente en milisegundos!")
        
        # Calcular porcentajes
        porcentajes = {}
        for clase in contadores.keys():
            porcentajes[clase] = (contadores[clase] / total_pixeles) * 100
        
        # Agrupar
        porcentaje_nubes_total = (
            porcentajes['TORMENTA'] + 
            porcentajes['CIRROS'] + 
            porcentajes['NUBE_BAJA_MEDIA']
        )
        
        porcentaje_superficie_total = (
            porcentajes['MAR'] + 
            porcentajes['TIERRA']
        )
        
        print(f"\n   📊 CLASIFICACIÓN COMPLETA:")
        print(f"\n      === SUPERFICIE ===")
        print(f"      • Mar:     {porcentajes['MAR']:.2f}% ({contadores['MAR']:,} píxeles)")
        print(f"      • Tierra:  {porcentajes['TIERRA']:.2f}% ({contadores['TIERRA']:,} píxeles)")
        print(f"      -" + "-"*50)
        print(f"      • TOTAL:   {porcentaje_superficie_total:.2f}%")
        
        print(f"\n      === NUBES ===")
        print(f"      • Tormenta (Cumulonimbus): {porcentajes['TORMENTA']:.2f}% ({contadores['TORMENTA']:,} píxeles)")
        print(f"      • Cirros (Nube Alta):      {porcentajes['CIRROS']:.2f}% ({contadores['CIRROS']:,} píxeles)")
        print(f"      • Nube Baja/Media:         {porcentajes['NUBE_BAJA_MEDIA']:.2f}% ({contadores['NUBE_BAJA_MEDIA']:,} píxeles)")
        print(f"      -" + "-"*50)
        print(f"      • TOTAL:                   {porcentaje_nubes_total:.2f}%")
        
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
        if porcentajes['TORMENTA'] > 2.0:
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
        """Dibuja panel con análisis."""
        img_pil = Image.fromarray(cv2.cvtColor(mapa_colores, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil)
        
        h, w = mapa_colores.shape[:2]
        
        # Dimensiones del panel
        panel_w = 900
        panel_h = 900
        panel_x = 30
        panel_y = 30
        
        # Fondo del panel
        overlay = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.rectangle(
            [(panel_x, panel_y), (panel_x + panel_w, panel_y + panel_h)],
            fill=(5, 5, 20, 245)
        )
        img_pil = Image.alpha_composite(img_pil.convert('RGBA'), overlay).convert('RGB')
        draw = ImageDraw.Draw(img_pil)
        
        y = panel_y + 20
        
        # Título
        draw.text((panel_x + 20, y), 
                 "☁️ CLASIFICACIÓN METEOROLÓGICA",
                 font=self.fuentes['titulo'],
                 fill=(0, 255, 255))
        y += 50
        
        draw.text((panel_x + 20, y), 
                 "Sistema v11.0 - Análisis Píxel por Píxel (Máxima Precisión)",
                 font=self.fuentes['pequeño'],
                 fill=(150, 150, 150))
        y += 40
        
        draw.line([(panel_x + 20, y), (panel_x + panel_w - 20, y)],
                 fill=(0, 255, 255), width=3)
        y += 25
        
        # Porcentajes
        porcentajes = resultados['porcentajes']
        contadores = resultados['contadores']
        
        draw.text((panel_x + 20, y), 
                 "(Porcentaje del total de la imagen)",
                 font=self.fuentes['pequeño'],
                 fill=(180, 180, 180))
        y += 35
        
        # === SECCIÓN NUBES ===
        draw.text((panel_x + 20, y), 
                 "=== NUBES ===",
                 font=self.fuentes['mediano'],
                 fill=(255, 255, 100))
        y += 40
        
        clases_nubes = ['TORMENTA', 'CIRROS', 'NUBE_BAJA_MEDIA']
        
        for clase in clases_nubes:
            porc = porcentajes[clase]
            pixeles = contadores[clase]
            color_clase = self.colores[clase]
            color_rgb = (color_clase[2], color_clase[1], color_clase[0])
            
            # Cuadrado de color
            draw.rectangle(
                [(panel_x + 40, y), (panel_x + 70, y + 25)],
                fill=color_rgb,
                outline=(255, 255, 255),
                width=2
            )
            
            # Texto
            draw.text((panel_x + 85, y + 2), 
                     f"{self.nombres[clase]}: {porc:.2f}%",
                     font=self.fuentes['mediano'],
                     fill=(255, 255, 255))
            y += 38
        
        y += 5
        draw.line([(panel_x + 40, y), (panel_x + panel_w - 40, y)],
                 fill=(100, 100, 100), width=1)
        y += 15
        
        # Total nubes
        nubes_total = resultados['porcentaje_nubes_total']
        draw.text((panel_x + 40, y), 
                 f"■ NUBES (Total): {nubes_total:.2f}%",
                 font=self.fuentes['grande'],
                 fill=(200, 200, 255))
        y += 50
        
        # === SECCIÓN SUPERFICIE ===
        draw.text((panel_x + 20, y), 
                 "=== SUPERFICIE ===",
                 font=self.fuentes['mediano'],
                 fill=(150, 255, 150))
        y += 40
        
        clases_superficie = ['MAR', 'TIERRA']
        
        for clase in clases_superficie:
            porc = porcentajes[clase]
            color_clase = self.colores[clase]
            color_rgb = (color_clase[2], color_clase[1], color_clase[0])
            
            draw.rectangle(
                [(panel_x + 40, y), (panel_x + 70, y + 25)],
                fill=color_rgb,
                outline=(255, 255, 255),
                width=2
            )
            
            draw.text((panel_x + 85, y + 2), 
                     f"{self.nombres[clase]}: {porc:.2f}%",
                     font=self.fuentes['mediano'],
                     fill=(220, 220, 220))
            y += 38
        
        y += 5
        draw.line([(panel_x + 40, y), (panel_x + panel_w - 40, y)],
                 fill=(100, 100, 100), width=1)
        y += 15
        
        # Total superficie
        superficie_total = resultados['porcentaje_superficie_total']
        draw.text((panel_x + 40, y), 
                 f"■ SUPERFICIE (Total): {superficie_total:.2f}%",
                 font=self.fuentes['grande'],
                 fill=(150, 150, 150))
        y += 60
        
        # === AMENAZA PRINCIPAL ===
        amenaza, nivel = self.determinar_amenaza_principal(porcentajes)
        
        draw.line([(panel_x + 20, y), (panel_x + panel_w - 20, y)],
                 fill=(255, 0, 0) if 'ALTA' in nivel else (255, 255, 0), 
                 width=3)
        y += 25
        
        color_amenaza = (255, 0, 0) if 'ALTA' in nivel else (255, 255, 100)
        
        draw.text((panel_x + 20, y), 
                 nivel,
                 font=self.fuentes['grande'],
                 fill=color_amenaza)
        y += 45
        
        draw.text((panel_x + 20, y), 
                 self.nombres[amenaza],
                 font=self.fuentes['mediano'],
                 fill=(255, 255, 255))
        y += 45
        
        # Justificación
        draw.text((panel_x + 20, y), 
                 "📋 JUSTIFICACIÓN:",
                 font=self.fuentes['mediano'],
                 fill=(200, 255, 200))
        y += 35
        
        justificacion = self.generar_justificacion(amenaza)
        lineas = justificacion.split('\n')
        for linea in lineas:
            draw.text((panel_x + 40, y), 
                     linea.strip(),
                     font=self.fuentes['pequeño'],
                     fill=(220, 220, 220))
            y += 24
        
        # Marca de versión
        y += 15
        draw.text((panel_x + 20, y), 
                 "🔬 Método: Clasificación Píxel por Píxel (Sin Superpíxeles)",
                 font=self.fuentes['pequeño'],
                 fill=(100, 200, 255))
        
        # Timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        draw.text((w - 350, h - 40), 
                 f"Análisis: {timestamp}",
                 font=self.fuentes['pequeño'],
                 fill=(120, 120, 120))
        
        return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    
    def crear_comparacion(self, imagen_rgb, mapa_con_panel):
        """Crea visualización lado a lado."""
        h, w = imagen_rgb.shape[:2]
        
        if mapa_con_panel.shape[:2] != (h, w):
            mapa_con_panel = cv2.resize(mapa_con_panel, (w, h))
        
        comparacion = np.hstack([imagen_rgb, mapa_con_panel])
        
        img_pil = Image.fromarray(cv2.cvtColor(comparacion, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil)
        
        # Barra superior
        overlay = Image.new('RGBA', (w * 2, h), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.rectangle([(0, 0), (w * 2, 75)], fill=(0, 0, 0, 220))
        img_pil = Image.alpha_composite(img_pil.convert('RGBA'), overlay).convert('RGB')
        draw = ImageDraw.Draw(img_pil)
        
        draw.text((30, 20), "📷 IMAGEN SATELITAL ORIGINAL", 
                 font=self.fuentes['titulo'], fill=(255, 255, 255))
        draw.text((w + 30, 20), "☁️ ANÁLISIS v11.0 (Píxel × Píxel)", 
                 font=self.fuentes['titulo'], fill=(0, 255, 255))
        
        # Línea divisoria
        for y_pos in range(0, h, 10):
            draw.line([(w, y_pos), (w, y_pos + 5)], fill=(255, 255, 255), width=4)
        
        return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    
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
    
    def analizar(self, ruta_visible_rgb, ruta_infrarroja_ir, 
                 carpeta_salida="resultados_v11_pixel_por_pixel", guardar=True):
        """Pipeline completo de análisis."""
        print("\n" + "="*70)
        print("☁️  SISTEMA DE CLASIFICACIÓN DE NUBES v11.0")
        print("   Análisis Píxel por Píxel - Máxima Precisión")
        print("="*70)
        
        # PASO 1: Cargar y preparar mapas
        mapas = self.cargar_y_preparar_mapas(ruta_visible_rgb, ruta_infrarroja_ir)
        
        # PASO 2: Clasificar píxel por píxel
        resultados = self.clasificar_imagen_pixel_por_pixel(mapas)
        
        # PASO 3: Visualizar
        print("\n🎨 PASO 3: Generando visualizaciones...")
        mapa_con_panel = self.dibujar_panel(
            resultados['mapa_colores'].copy(), resultados)
        
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
            
            print(f"\n💾 Guardando resultados...")
            cv2.imwrite(f"{carpeta_salida}/01_mapa_clasificacion_{timestamp}.jpg", 
                       resultados['mapa_colores'])
            cv2.imwrite(f"{carpeta_salida}/02_mapa_con_panel_{timestamp}.jpg", 
                       mapa_con_panel)
            cv2.imwrite(f"{carpeta_salida}/03_comparacion_{timestamp}.jpg", 
                       comparacion)
            cv2.imwrite(f"{carpeta_salida}/04_visualizacion_canales_IR_{timestamp}.jpg", 
                       vis_canales)
            
            print(f"   ✅ Resultados guardados en: {carpeta_salida}/")
        
        print("\n" + "="*70)
        print("✅ ANÁLISIS COMPLETADO")
        print("="*70)
        
        return {
            'mapa_colores': resultados['mapa_colores'],
            'mapa_con_panel': mapa_con_panel,
            'comparacion': comparacion,
            'vis_canales': vis_canales,
            'resultados': resultados
        }


# ========== SCRIPT PRINCIPAL ==========

def main():
    """Script principal."""
    print("\n" + "="*70)
    print("  ☁️  CLASIFICADOR DE NUBES v11.0  ☁️")
    print("  Análisis Píxel por Píxel (Fuerza Bruta)")
    print("="*70)
    
    # Rutas de imágenes
    ruta_rgb = "imagen_visible.jpg"
    ruta_ir = "imagen_infrarroja.jpg"
    
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
    clasificador = ClasificadorNubesV11()
    
    # Ejecutar
    try:
        resultados = clasificador.analizar(ruta_rgb, ruta_ir, guardar=True)
        
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
            }
        }
        
        with open("reporte_meteorologico.json", "w") as f:
            json.dump(reporte, f, indent=4)
            
        print(f"\n💾 Reporte JSON exportado exitosamente como 'reporte_meteorologico.json'")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Verificar dependencias (ya NO necesitamos scikit-image)
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