import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

def entrenar_modelo_multiscale():
    print("⏳ Cargando dataset SDR Multiscale (CNN simulada)...")
    ruta_csv = os.path.join(os.path.dirname(__file__), '..', 'backend', 'data', 'dataset_multiscale.csv')
    df = pd.read_csv(ruta_csv)
    
    # Separar Features (X) y Target (y)
    # The columns are all except 'label'
    X = df.drop('label', axis=1)
    y = df['label']
    
    print(f"   ✓ Entrenando Bosque Espacial (Multiscale RF) con {len(X)} píxeles y {len(X.columns)} canales de contexto...")
    # Entrenar un bosque aleatorio muy poderoso
    modelo = RandomForestClassifier(n_estimators=150, max_depth=25, random_state=42, n_jobs=-1)
    modelo.fit(X, y)
    
    # Guardar el modelo
    ruta_modelo = os.path.join(os.path.dirname(__file__), '..', 'backend', 'core', 'modelo_v12.pkl')
    os.makedirs(os.path.dirname(ruta_modelo), exist_ok=True)
    joblib.dump(modelo, ruta_modelo)
    
    print(f"✅ Modelo Espacial entrenado y guardado en {ruta_modelo}")

if __name__ == '__main__':
    entrenar_modelo_multiscale()
