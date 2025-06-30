import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title ('modelo de predicción')
with st.form ('Formulario'):
    densidad= st.text_input ('Densidad:')
    alcohol= st.text_input ('Alcohol')
    
    bottom = st.form_submit_button ('Enviar') 

if bottom:
    st.subheader ('Valores de la predicción:')
    st.write('Densidad:', densidad)
    st.write('Alcohol:', alcohol)
