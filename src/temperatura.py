import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime
import os

# 1. Configuración inicial de la aplicación
st.set_page_config(
    page_title="Dashboard Temperaturas",
    page_icon="📊",
    layout="wide"
)
st.title("📊 Dashboard Interactivo de Temperaturas")
st.sidebar.title("🔍 Opciones de Navegación")

# 2. Carga de datos
@st.cache_data
def load_data():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print("Ruta actual:", os.getcwd())

    file_path = "../data/RHT20 02-21-25 _16.26.11_HOTEL_NOCK.csv"

    if os.path.exists(file_path):
        print(f"El archivo {file_path} existe.")
    else:
        print(f"⚠️ El archivo {file_path} NO existe. Verifica la ruta.")
    df = pd.read_csv(file_path)
    return df
df = load_data()


# 3. Implementación de la Barra de Navegación
menu = st.sidebar.radio(
    "Selecciona una opción:",
    ["Inicio", "Datos", "Visualización", "Configuración"]
)

# 4. Mostrar los Datos
if menu == "Datos":
    st.subheader("📂 Datos Generados")
    st.dataframe(df, height=500, use_container_width=True)

# 11. Ejecución del Script
if __name__ == "__main__":
    st.sidebar.info("Ejecuta este script con: streamlit run talento-roadmap-app.py")