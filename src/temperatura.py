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

data = load_data()


# 3. Implementación de la Barra de Navegación
menu = st.sidebar.radio(
    "Selecciona una opción:",
    ["Inicio", "Datos", "Visualización", "Configuración"]
)

# 4. Mostrar los Datos
if menu == "Datos":
    st.subheader("📂 Datos Generados")
    st.dataframe(data, height=500, use_container_width=True)

# 5. Filtrar por Fecha
data["DATE"] = pd.to_datetime(data["DATE"], format="%d/%m/%Y", dayfirst=True)
filtered_data = data  # Asegurar que filtered_data esté definido en todo el script
if menu == "Visualización":
    st.subheader("📅 Filtrar por Fecha")

    # Convertir las fechas a tipo date
    min_date = data["DATE"].min().date()
    max_date = data["DATE"].max().date()

    fecha_inicio, fecha_fin = st.sidebar.date_input(
        "Selecciona el rango de fechas:",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

    # Convertir fecha_inicio y fecha_fin a datetime para la comparación
    fecha_inicio = pd.to_datetime(fecha_inicio)
    fecha_fin = pd.to_datetime(fecha_fin)

    filtered_data = filtered_data[
        (filtered_data["DATE"] >= fecha_inicio) & (filtered_data["DATE"] <= fecha_fin)
    ]
    
     # 8. Botón para Reiniciar Filtros
    if st.sidebar.button("Reiniciar Filtros"):
        filtered_data = data
        st.rerun()

# 11. Ejecución del Script
if __name__ == "__main__":
    st.sidebar.info("Ejecuta este script con: streamlit run d:/Usuario/Descargas/larco/src/temperatura.py")