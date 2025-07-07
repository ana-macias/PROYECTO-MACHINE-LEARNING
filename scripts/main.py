import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from PIL import Image
import base64
import pickle
import plotly.express as px

with open('../models/modelo_abc1.pkl', 'rb') as file:
    modelo = pickle.load(file)
    #st.success("Modelo cargado correctamente")
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
set_background('../docs/vino_uvas.jpg')  

# Configuración de página (opcional)
st.set_page_config(layout="wide")

# CSS para hacer los inputs 50% más estrechos
st.markdown("""
    <style>
    /* Aplica a los contenedores de cada input */
    .stNumberInput {
        max-width: 200px;
        margin-bottom: 1rem;
    }
    /* Asegura que los inputs también respeten el ancho */
    div[data-baseweb="input"] {
        width: 100% !important;
    }
    
    /* Aumentar especificidad con [class^=""] */
    [data-testid="stNumberInput"] > label {
        font-weight: bold !important;
        font-size: 16px !important;
    }
    </style>
""", unsafe_allow_html=True)

# st.title ('🍷 MODELO DE PREDICCION DE CALIDAD DEL VINO')
st.markdown("<h1 style='color:#800000;'>🍷 MODELO DE PREDICCIÓN DE CALIDAD DEL VINO</h1>", unsafe_allow_html=True)

st.markdown("""
Ingresa los valores de las siguientes características del vino:
- **Acidez volátil** (volatile acidity) 
- **SO₂ total** (total sulfur dioxide)
- **Densidad** (density)
- **pH** (pH)
- **Alcohol** (alcohol)
""")
def reset_form():
    st.session_state.volatile_acidity = 0.0
    st.session_state.total_sulfur_dioxide = 0.0
    st.session_state.density = 0.9
    st.session_state.pH = 7.0
    st.session_state.alcohol = 8.0

# Inicializar los valores si no existen
if 'volatile_acidity' not in st.session_state:
    reset_form()


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
    
    # Definir colores sólidos (puedes ajustar los códigos HEX)
    color_baja = "#FF0000"     # Rojo sólido
    color_media = "#FFA500"    # Naranja sólido
    color_alta = "#00FF00"     # Verde sólido

    # Mostrar el resultado con estilo personalizado
    if clase_predicha == "baja":
        st.markdown(
            f'<div style="background-color: {color_baja}; padding: 10px; border-radius: 5px;'
            f'color: white; font-weight: bold; text-align: center;">'
            f'Calidad predicha: {clase_predicha.capitalize()}'
            '</div>',
            unsafe_allow_html=True
        )
    elif clase_predicha == "media":
        st.markdown(
            f'<div style="background-color: {color_media}; padding: 10px; border-radius: 5px;'
            f'color: white; font-weight: bold; text-align: center;">'
            f'Calidad predicha: {clase_predicha.capitalize()}'
            '</div>',
            unsafe_allow_html=True
        )
    else:  # alta
        st.markdown(
            f'<div style="background-color: {color_alta}; padding: 10px; border-radius: 5px;'
            f'color: white; font-weight: bold; text-align: center;">'
            f'Calidad predicha: {clase_predicha.capitalize()}'
            '</div>',
            unsafe_allow_html=True
        )
    
    # Botón para nueva predicción
    if st.button("Hacer nueva predicción"):
        reset_form()
        st.rerun()  
    
    # Crear gráfico interactivo
    fig = px.bar(
        x=list(prob_dict.keys()),
        y=list(prob_dict.values()),
        color=list(prob_dict.values()),  # Usa los valores para el gradiente
        color_continuous_scale='YlOrRd',  # 'Viridis', 'Plasma', 'Inferno', 'Magma', 'RdBu', 'YlOrRd'
        labels={'x': 'Calidad', 'y': 'Probabilidad'}
    )

    # Ajuste de tamaño clave aquí:
    fig.update_layout(
        width=500,  # Ancho más estrecho
        height=350,
        coloraxis_showscale=False,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=False)  # Desactiva el ajuste automático al contenedor

