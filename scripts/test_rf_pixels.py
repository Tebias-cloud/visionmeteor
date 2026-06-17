import joblib
import pandas as pd

modelo = joblib.load('backend/core/modelo_v12.pkl')

# Test Andes Pixel
pixel_andes = pd.DataFrame([[229, 231, 70, 16, 3]], columns=['brillo', 'rojo', 'verde', 'azul', 'textura'])
print(f"Andes Pixel Prediction: {modelo.predict(pixel_andes)[0]}")

# Test Camanchaca Pixel
pixel_camanchaca = pd.DataFrame([[162, 11, 178, 184, 5]], columns=['brillo', 'rojo', 'verde', 'azul', 'textura'])
print(f"Camanchaca Pixel Prediction: {modelo.predict(pixel_camanchaca)[0]}")
