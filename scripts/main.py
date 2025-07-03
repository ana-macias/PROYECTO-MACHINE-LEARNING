import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from PIL import Image
import base64
import pickle

with open('../models/modelo_abc.pkl', 'rb') as file:
    modelo = pickle.load(file)

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
- **Cloruros** (chlorides)
- **Densidad** (density)
- **Alcohol** (alcohol)
""")

with st.form("Formulario"): 
    volatile_acidity = st.number_input("Acidez volátil (ej: 0.5)", min_value=0.0, max_value=2.0, step=0.001, format="%.3f")
    chlorides = st.number_input("Cloruros (ej: 0.05)", min_value=0.0, max_value=1.0, step=0.001, format="%.3f")
    density = st.number_input("Densidad (ej: 0.99)", min_value=0.9, max_value=1.1, step=0.001, format="%.4f")
    alcohol = st.number_input("Alcohol (ej: 10.5)", min_value=8.0, max_value=15.0, step=0.1, format="%.3f")
    
    submit_button = st.form_submit_button("Predecir Calidad")

# Predecir al hacer clic
if submit_button:
    # Crear DataFrame con los inputs
    input_data = pd.DataFrame({
        'volatile acidity': [volatile_acidity],
        'chlorides': [chlorides],
        'density': [density],
        'alcohol': [alcohol]
    })
    
    # Hacer la predicción
    scaler = StandardScaler()
    input_data_scaled = scaler.fit_transform(input_data)
    prediction = modelo.predict(input_data_scaled)[0]
    
    # Se mapea la predicción a categorías
    calidad_dict = {0: "baja", 1: "media", 2: "alta"} 
    
    # Mostrar resultado
    st.success(f"**Calidad predicha:** {prediction.capitalize()}")


