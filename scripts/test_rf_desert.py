import joblib
import pandas as pd

modelo = joblib.load('backend/core/modelo_v12.pkl')

# Test Desert Pixel
pixel_desert = pd.DataFrame([[153, 206, 236, 21, 60]], columns=['brillo', 'rojo', 'verde', 'azul', 'textura'])
print(f"Desert Pixel Prediction: {modelo.predict(pixel_desert)[0]}")
