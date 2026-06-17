from fpdf import FPDF
import os
from datetime import datetime

class GeneradorPDF(FPDF):
    def header(self):
        # Logo o título principal
        self.set_font('helvetica', 'B', 20)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, 'VISIONMETEOR', border=0, align='C', new_x="LMARGIN", new_y="NEXT")
        self.set_font('helvetica', 'I', 12)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, 'Boletín Meteorológico Oficial', border=0, align='C', new_x="LMARGIN", new_y="NEXT")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Generado por Sistema VisionMeteor v11.0 (Machine Learning) - Página {self.page_no()}', align='C')

    def generar_boletin(self, reporte_data, imagenes_paths, ruta_salida):
        """Genera el PDF ensamblando datos e imágenes."""
        self.add_page()
        
        # Fecha de emisión
        self.set_font('helvetica', 'B', 10)
        self.set_text_color(50, 50, 50)
        self.cell(0, 6, f"Fecha de Emisión: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", new_x="LMARGIN", new_y="NEXT")
        
        # Nivel de Amenaza
        self.ln(5)
        self.set_font('helvetica', 'B', 14)
        amenaza_nivel_crudo = reporte_data['amenaza_principal']['nivel']
        
        import re
        amenaza_nivel = re.sub(r'[^\x00-\x7F\xC0-\xFF]', '', amenaza_nivel_crudo).strip()
        
        amenaza_clase = reporte_data['amenaza_principal']['clase']
        
        # Color rojo si es ALTA o EXTREMA, naranja si no
        if 'ALTA' in amenaza_nivel or 'EXTREMA' in amenaza_nivel:
            self.set_text_color(220, 20, 20)
        else:
            self.set_text_color(255, 140, 0)
            
        self.cell(0, 10, f"ESTADO DE ALERTA: {amenaza_nivel} ({amenaza_clase})", new_x="LMARGIN", new_y="NEXT")
        
        # Estadísticas Rápidas
        self.ln(5)
        self.set_font('helvetica', 'B', 14)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, "RESUMEN DE CONDICIONES", new_x="LMARGIN", new_y="NEXT")
        
        self.set_font('helvetica', '', 12)
        self.set_text_color(0, 0, 0)
        est = reporte_data['estadisticas']
        self.cell(0, 8, f"Cobertura Nubosa Total: {est['porcentaje_nubes_total']:.1f}%", new_x="LMARGIN", new_y="NEXT")
        self.cell(0, 8, f"Superficie Despejada: {est['porcentaje_superficie_total']:.1f}%", new_x="LMARGIN", new_y="NEXT")
        
        # Añadir Desglose
        self.ln(3)
        self.set_font('helvetica', 'B', 12)
        self.set_text_color(100, 100, 100)
        self.cell(0, 6, "Tipos de nubes detectadas:", new_x="LMARGIN", new_y="NEXT")
        self.set_font('helvetica', '', 12)
        self.set_text_color(50, 50, 50)
        for clase, porc in est['desglose_porcentajes'].items():
            if porc > 0.1:
                self.set_x(15)
                self.cell(0, 6, f"- {clase.replace('_', ' ').title()}: {porc:.1f}%", new_x="LMARGIN", new_y="NEXT")
        
        # Añadir Análisis Sinóptico y Ejecutivo
        self.ln(8)
        
        # 1. Resumen Ejecutivo (No Técnico)
        self.set_font('helvetica', 'B', 14)
        self.set_text_color(0, 51, 102)
        self.cell(0, 8, "Análisis Meteorológico:", new_x="LMARGIN", new_y="NEXT")
        
        self.set_font('helvetica', '', 11)
        self.set_text_color(40, 40, 40)
        texto_ejecutivo, texto_sinoptico, texto_heatmap = self._generar_textos(est['desglose_porcentajes'])
        self.multi_cell(0, 6, texto_ejecutivo)
        
        # 2. Detalles Técnicos
        self.ln(4)
        self.set_font('helvetica', 'B', 12)
        self.set_text_color(0, 51, 102)
        self.cell(0, 8, "Detalles Técnicos:", new_x="LMARGIN", new_y="NEXT")
        
        self.set_font('helvetica', '', 11)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 6, texto_sinoptico)
        
        self.ln(4)
        self.set_font('helvetica', 'I', 9)
        self.set_text_color(100, 100, 100)
        self.multi_cell(0, 5, "Referencias Bibliográficas:\n[1] World Meteorological Organization (WMO).\n[2] NOAA NESDIS. GOES-R Advanced Baseline Imager (ABI).")
        
        # Salto de página para evitar que las imágenes se corten
        self.add_page()
        
        # Añadir Imágenes
        self.set_font('helvetica', 'B', 14)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, "1. Mapa de Nubosidad y Cobertura", new_x="LMARGIN", new_y="NEXT")
        self.ln(2)
        
        if 'comparacion' in imagenes_paths:
            try:
                self.image(imagenes_paths['comparacion'], x=10, w=190)
            except Exception as e:
                self.cell(0, 10, f"Error cargando imagen comparativa: {e}", new_x="LMARGIN", new_y="NEXT")
        
        self.add_page()
        self.set_font('helvetica', 'B', 14)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, "2. Mapa de Calor (Infrarrojo Termal)", new_x="LMARGIN", new_y="NEXT")
        self.ln(2)
        
        # Agregar análisis del heatmap justo debajo del título del heatmap
        self.set_font('helvetica', '', 11)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 6, texto_heatmap)
        self.ln(5)
        
        if 'heatmap' in imagenes_paths:
            try:
                self.image(imagenes_paths['heatmap'], x=30, w=150)
            except Exception as e:
                self.cell(0, 10, f"Error cargando heatmap térmico: {e}", new_x="LMARGIN", new_y="NEXT")
        
        self.output(ruta_salida)
        return True

    def _generar_textos(self, porcentajes):
        """Genera un análisis en lenguaje común, otro técnico y uno para el mapa de calor."""
        ejecutivo = ""
        tecnico = "El análisis satelital actual se basa en la combinación de firmas de reflectancia y temperaturas de brillo infrarrojas. "
        heatmap = "En el mapa de calor adjunto, los colores representan las diferentes temperaturas de las superficies y nubes detectadas. "
        
        p_tormenta = porcentajes.get('TORMENTA', 0)
        p_cirros = porcentajes.get('CIRROS', 0)
        p_bajas = porcentajes.get('NUBE_BAJA_MEDIA', 0)
        p_nubes = p_tormenta + p_cirros + p_bajas
        
        if p_tormenta > 10.0:
            ejecutivo += "Actualmente observamos un sistema de tormentas muy importante sobre la región. Las nubes tienen gran desarrollo vertical, lo que significa que podríamos esperar lluvias intensas, ráfagas de viento fuertes e incluso condiciones severas. Es recomendable tomar precauciones.\n"
            tecnico += f"Se ha detectado convección profunda que cubre el {p_tormenta:.1f}% del área visible. Los topes de estas nubes presentan temperaturas por debajo de los -50°C, indicando actividad convectiva intensa y posible ciclogénesis.\n"
            heatmap += "Las zonas en tonos rojos y morados oscuros indican nubes muy frías a gran altitud, revelando el núcleo y la intensidad de este sistema de tormentas.\n"
        elif p_tormenta > 0:
            ejecutivo += "Estamos viendo la formación de algunas tormentas dispersas. Aunque no cubren toda la región, podrían generar chubascos locales fuertes en las próximas horas.\n"
            tecnico += "Se observan núcleos convectivos aislados con moderado desarrollo vertical y temperaturas de brillo frías en sus topes.\n"
            heatmap += "Se pueden apreciar algunas manchas aisladas de colores cálidos a fríos que marcan el desarrollo vertical de estas nubes de tormenta locales.\n"
            
        if p_cirros > 10.0:
            ejecutivo += "El cielo presenta nubes altas y finas (cirros). Estas nubes están formadas por cristales de hielo muy arriba en la atmósfera. Normalmente indican buen tiempo, aunque a veces nos avisan que un cambio de clima viene en camino.\n"
            tecnico += f"Existe una cobertura del {p_cirros:.1f}% de nubes cirriformes. Estas muestran una alta reflectancia pero son muy frías, típicamente asociadas a los niveles altos de la troposfera o corrientes en chorro.\n"
            heatmap += "Las áreas azuladas o celestes en el mapa muestran la firma fría de estos cristales de hielo, flotando muy por encima de la superficie.\n"
            
        if p_bajas > 15.0:
            ejecutivo += "Hay una presencia notable de nubes bajas o bancos de niebla. Este tipo de nubosidad suele mantener las temperaturas frescas y puede reducir la visibilidad si toca el suelo, pero raramente produce más que lloviznas débiles.\n"
            tecnico += f"El {p_bajas:.1f}% del área está cubierta por nubosidad estratiforme baja. Presentan reflectancia visible moderada pero temperaturas en el infrarrojo relativamente cálidas, lo que indica que están cerca de la superficie.\n"
            heatmap += "Como estas nubes están bajas, su temperatura es más cercana a la de la tierra o el mar, por lo que aparecen en colores intermedios (verdes o amarillos claros) en el mapa de calor.\n"
            
        if p_nubes < 10.0:
            ejecutivo += "Las condiciones generales son excelentes, con cielos en su mayoría despejados. No se observan sistemas meteorológicos importantes, por lo que podemos esperar un clima tranquilo y estable.\n"
            tecnico += "La atmósfera se presenta estable con dominancia de altas presiones. Los sensores satelitales registran una transmisión casi total en el espectro visible hacia la superficie.\n"
            heatmap += "Al no haber nubes, el mapa de calor muestra directamente la temperatura de la superficie terrestre u oceánica, predominando los colores cálidos (naranjas y amarillos) que indican áreas despejadas y expuestas al sol.\n"
            
        return ejecutivo.strip(), tecnico.strip(), heatmap.strip()
