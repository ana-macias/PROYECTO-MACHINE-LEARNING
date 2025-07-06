import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from PIL import Image
import base64
import pickle

with open('../models/modelo_abc1.pkl', 'rb') as file:
    modelo = pickle.load(file)
    st.success("Modelo cargado correctamente")
#st.write("Clases que reconoce el modelo:", modelo.classes_)

with open('../models/scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)

# Función para convertir imagen a base64 (necesario para CSS)
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Función para establecer el fondo
def set_background(png_file):
    bin_str = get_base64(png_file) 
    page_bg_img = '''
    <style>
    .stApp {
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed; 
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

# --- Configuración de la página ---
st.set_page_config(layout="wide")


# Establecer imagen de fondo (reemplaza 'fondo.jpg' con tu archivo)
set_background('../docs/vino.jpg')  

# Configuración de página (opcional)
st.set_page_config(layout="wide")

st.title ('🍷 Modelo de predicción  de Calidad de Vino')

st.markdown("""
Ingresa los valores de las siguientes características del vino:
- **Acidez volátil** (volatile acidity) 
- **SO₂ total** (total sulfur dioxide)
- **Densidad** (density)
- **pH** (pH)
- **Alcohol** (alcohol)
""")

with st.form("Formulario"): 
    volatile_acidity = st.number_input("Acidez volátil (ej: 0.5)", min_value=0.0, max_value=2.0, step=0.01, format="%.2f")
    total_sulfur_dioxide = st.number_input("SO₂ total (ej: 0.5)", min_value=0.0, max_value=200.0, step=0.01, format="%.2f")
    density = st.number_input("Densidad (ej: 0.990)", min_value=0.9, max_value=1.1, step=0.001, format="%.4f")
    pH = st.number_input("pH (ej: 7.0)", min_value=1.0, max_value=14.0, step=0.01, format="%.2f" )
    alcohol = st.number_input("Alcohol (ej: 10.5)", min_value=8.0, max_value=15.0, step=0.1, format="%.3f")
    
    submit_button = st.form_submit_button("Predecir Calidad")

# Predecir al hacer clic
if submit_button:
    # Crear DataFrame con los inputs
    input_data = pd.DataFrame({
        'volatile acidity': [volatile_acidity],
        'total sulfur dioxide': [total_sulfur_dioxide],
        'density': [density],
        'pH': [pH],
        'alcohol': [alcohol]
    })
    
    # Hacer predicciones:
    input_scaled = scaler.transform(input_data)
    probabilidades = modelo.predict_proba(input_scaled)[0]
    clases_modelo = list(modelo.classes_)
    
    # Crear diccionario ordenado de probabilidades
    prob_dict = {clase: prob for clase, prob in zip(clases_modelo, probabilidades)}
    
    # Determinar la clase con mayor probabilidad
    clase_predicha = clases_modelo[np.argmax(probabilidades)]
    
    # Mostrar resultados
    st.success(f"**Calidad predicha:** {clase_predicha.capitalize()}")
    st.write(f"**Probabilidades:** {prob_dict}")
    
    # Botón para nueva predicción
    if st.button("Hacer nueva predicción"):
        st.experimental_rerun() 
    

