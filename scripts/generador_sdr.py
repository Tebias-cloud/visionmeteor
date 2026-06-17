import numpy as np
import pandas as pd
import os

def generar_datos_simulados(num_samples=200000):
    print(f"Generando {num_samples} muestras sintéticas SDR Perfectas (5D)...")
    
    # 1. MAR (Océano)
    n_mar = int(num_samples * 0.3)
    mar_brillo = np.random.normal(35, 15, n_mar)
    mar_rojo = np.random.normal(30, 15, n_mar)
    mar_verde = np.random.normal(60, 30, n_mar)
    mar_azul = np.random.normal(140, 20, n_mar)
    mar_textura = np.random.normal(10, 5, n_mar)
    mar_labels = ['MAR'] * n_mar
    
    # 2. TIERRA (Desierto y Montañas)
    n_tierra = int(num_samples * 0.3)
    n_desierto = int(n_tierra * 0.7)
    n_andes = n_tierra - n_desierto
    
    desierto_brillo = np.random.normal(150, 15, n_desierto)
    desierto_rojo = np.random.normal(210, 10, n_desierto)
    desierto_verde = np.random.normal(220, 10, n_desierto)
    desierto_azul = np.random.normal(20, 10, n_desierto)
    desierto_textura = np.random.normal(60, 20, n_desierto)
    
    andes_brillo = np.random.normal(220, 15, n_andes)
    andes_rojo = np.random.normal(230, 10, n_andes)
    andes_verde = np.random.normal(70, 10, n_andes)
    andes_azul = np.random.normal(20, 10, n_andes)
    andes_textura = np.random.normal(40, 15, n_andes) # Menos textura que una tormenta
    
    tierra_brillo = np.concatenate([desierto_brillo, andes_brillo])
    tierra_rojo = np.concatenate([desierto_rojo, andes_rojo])
    tierra_verde = np.concatenate([desierto_verde, andes_verde])
    tierra_azul = np.concatenate([desierto_azul, andes_azul])
    tierra_textura = np.concatenate([desierto_textura, andes_textura])
    tierra_labels = ['TIERRA'] * n_tierra
    
    # 3. NUBE BAJA / MEDIA (Camanchaca / Estratocúmulos)
    n_nubeb = int(num_samples * 0.2)
    nubeb_brillo = np.random.normal(170, 15, n_nubeb)
    nubeb_rojo = np.random.normal(80, 40, n_nubeb)
    nubeb_verde = np.random.normal(180, 20, n_nubeb)
    nubeb_azul = np.random.normal(160, 30, n_nubeb)
    nubeb_textura = np.random.normal(30, 15, n_nubeb)
    nubeb_labels = ['NUBE_BAJA_MEDIA'] * n_nubeb
    
    # 4. CIRROS (Nubes altas y delgadas)
    n_cirros = int(num_samples * 0.1)
    cirros_brillo = np.random.normal(160, 15, n_cirros)
    cirros_rojo = np.random.normal(180, 20, n_cirros)
    cirros_verde = np.random.normal(180, 20, n_cirros)
    cirros_azul = np.random.normal(50, 20, n_cirros)
    cirros_textura = np.random.normal(20, 10, n_cirros)
    cirros_labels = ['CIRROS'] * n_cirros
    
    # 5. TORMENTA (Convección profunda)
    n_tormenta = num_samples - (n_mar + n_tierra + n_nubeb + n_cirros)
    tormenta_brillo = np.random.normal(200, 15, n_tormenta)
    tormenta_rojo = np.random.normal(220, 10, n_tormenta)
    tormenta_verde = np.random.normal(30, 10, n_tormenta)
    tormenta_azul = np.random.normal(10, 10, n_tormenta)
    tormenta_textura = np.random.normal(130, 30, n_tormenta) # Mucha más textura que los Andes
    tormenta_labels = ['TORMENTA'] * n_tormenta
    
    # Concatenar todos
    brillo = np.concatenate([mar_brillo, tierra_brillo, nubeb_brillo, cirros_brillo, tormenta_brillo])
    rojo = np.concatenate([mar_rojo, tierra_rojo, nubeb_rojo, cirros_rojo, tormenta_rojo])
    verde = np.concatenate([mar_verde, tierra_verde, nubeb_verde, cirros_verde, tormenta_verde])
    azul = np.concatenate([mar_azul, tierra_azul, nubeb_azul, cirros_azul, tormenta_azul])
    textura = np.concatenate([mar_textura, tierra_textura, nubeb_textura, cirros_textura, tormenta_textura])
    labels = np.concatenate([mar_labels, tierra_labels, nubeb_labels, cirros_labels, tormenta_labels])
    
    # Limitar a [0, 255]
    brillo = np.clip(brillo, 0, 255)
    rojo = np.clip(rojo, 0, 255)
    verde = np.clip(verde, 0, 255)
    azul = np.clip(azul, 0, 255)
    textura = np.clip(textura, 0, 255)
    
    # Crear DataFrame
    df = pd.DataFrame({
        'brillo': brillo,
        'rojo': rojo,
        'verde': verde,
        'azul': azul,
        'textura': textura,
        'label': labels
    })
    
    # Mezclar aleatoriamente
    df = df.sample(frac=1).reset_index(drop=True)
    
    # Guardar a CSV
    os.makedirs('backend/data', exist_ok=True)
    df.to_csv('backend/data/dataset_sdr_simulado.csv', index=False)
    print(f"✅ Dataset generado y guardado en backend/data/dataset_sdr_simulado.csv")

if __name__ == '__main__':
    generar_datos_simulados(300000)
