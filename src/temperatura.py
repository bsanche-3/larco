import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
import seaborn as sns
import matplotlib.pyplot as plt

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
    file_path = "../data/RHT20 02-21-25 _16.26.11_HOTEL_NOCK.csv"
    if not os.path.exists(file_path):
        st.error(f"⚠️ El archivo {file_path} NO existe. Verifica la ruta.")
        return None
    df = pd.read_csv(file_path)
    return df

data = load_data()
if data is None:
    st.stop()

# Convertir columnas
data["DATE"] = pd.to_datetime(data["DATE"], format="%d/%m/%Y", dayfirst=True)
data["HOUR"] = pd.to_datetime(data["TIME"], format="%H:%M:%S").dt.hour.astype(str)

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
filtered_data = data  # Asegurar que filtered_data esté definido en todo el script
if menu == "Visualización":
    st.subheader("📅 Filtrar por Fecha")
    min_date, max_date = data["DATE"].min().date(), data["DATE"].max().date()
    fecha_inicio, fecha_fin = st.sidebar.date_input("Selecciona el rango de fechas:", [min_date, max_date], min_value=min_date, max_value=max_date)
    filtered_data = filtered_data[(filtered_data["DATE"] >= pd.to_datetime(fecha_inicio)) & (filtered_data["DATE"] <= pd.to_datetime(fecha_fin))]

    if st.sidebar.button("Reiniciar Filtros"):
        filtered_data = data
        fecha_inicio = min_date  # Restablecer fecha de inicio al mínimo disponible
        fecha_fin = max_date  # Restablecer fecha de fin al máximo disponible
        st.rerun()
    
    # 9. Implementar Pestañas
    st.subheader("📌 Navegación entre Pestañas")
    tab1, tab2 = st.tabs(["📊 Gráficos", "📂 Datos"])
    with tab1:
        st.subheader("Visualización de Datos")
        
        if st.checkbox("Mostrar Gráfico de Dispersión (TEMP vs RH)"):
            st.markdown("📌 **Propósito**: Visualizar la relación entre temperatura y humedad a lo largo del día.")
            fig_scatter = px.scatter(
                filtered_data, 
                x="TEMP", 
                y="RH", 
                color="HOUR", 
                title="Relación entre Temperatura y Humedad por Hora",
                labels={"TEMP": "Temperatura (°C)", "RH": "Humedad Relativa (%)", "HOUR": "Hora del Día"}
            )
            st.plotly_chart(fig_scatter)

        if st.checkbox("Mostrar Evolución de Temperatura y Humedad"):
            st.markdown("📌 **Propósito**: Analizar cómo evolucionan la temperatura y la humedad a lo largo del tiempo.")
            fig_temp_hum = px.line(
                filtered_data, 
                x="DATE", 
                y=["TEMP", "RH"], 
                title="Evolución de Temperatura y Humedad",
                labels={"DATE": "Fecha", "TEMP": "Temperatura (°C)", "RH": "Humedad Relativa (%)"}
            )
            st.plotly_chart(fig_temp_hum)

        if st.checkbox("Mostrar Boxplot de Temperatura por Hora"):
            st.markdown("📌 **Propósito**: Identificar la distribución de la temperatura a diferentes horas del día y detectar valores atípicos.")
            fig_box = px.box(
                filtered_data, 
                x="HOUR", 
                y="TEMP", 
                title="Distribución de Temperatura por Hora del Día",
                labels={"HOUR": "Hora del Día", "TEMP": "Temperatura (°C)"}
            )
            st.plotly_chart(fig_box)

        if st.checkbox("Mostrar Histograma de Temperatura"):
            st.markdown("📌 **Propósito**: Mostrar la distribución de la temperatura y detectar patrones de frecuencia.")
            fig_hist = px.histogram(
                filtered_data, 
                x="TEMP", 
                nbins=20, 
                title="Distribución de la Temperatura",
                labels={"TEMP": "Temperatura (°C)"}
            )
            st.plotly_chart(fig_hist)

        if st.checkbox("Mostrar Mapa de Calor"):
            st.markdown("📌 **Propósito**: Visualizar la densidad de temperatura y humedad en diferentes horas del día.")
            fig_heatmap = px.density_heatmap(
                filtered_data, 
                x="HOUR", 
                y="TEMP", 
                z="RH", 
                title="Mapa de Calor: Temperatura y Humedad por Hora",
                labels={"HOUR": "Hora del Día", "TEMP": "Temperatura (°C)", "RH": "Humedad Relativa (%)"}
            )
            st.plotly_chart(fig_heatmap)

        if st.checkbox("Mostrar Mapa de Calor de Correlaciones"):
            st.markdown("📌 **Propósito**: Identificar correlaciones entre temperatura y humedad en los datos.")
            corr_matrix = filtered_data[["TEMP", "RH"]].corr()
            fig_heatmap = plt.figure(figsize=(6, 4))
            sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f")
            st.pyplot(fig_heatmap)

        if st.checkbox("Mostrar Distribución de la Temperatura"):
            st.markdown("📌 **Propósito**: Examinar la dispersión de la temperatura y detectar posibles anomalías.")
            fig_box = px.box(
                filtered_data, 
                y="TEMP", 
                title="Distribución de la Temperatura",
                labels={"TEMP": "Temperatura (°C)"}
            )
            st.plotly_chart(fig_box)

        if st.checkbox("Mostrar Temperatura Promedio por Hora"):
            st.markdown("📌 **Propósito**: Observar cómo varía la temperatura promedio en diferentes horas del día.")
            filtered_data["HOUR"] = pd.to_datetime(filtered_data["TIME"], format="%H:%M:%S").dt.hour
            temp_avg_hour = filtered_data.groupby("HOUR")["TEMP"].mean().reset_index()

            fig_bar = px.bar(
                temp_avg_hour, 
                x="HOUR", 
                y="TEMP", 
                title="Temperatura Promedio por Hora", 
                color="HOUR",
                labels={"HOUR": "Hora del Día", "TEMP": "Temperatura Promedio (°C)"}
            )
            st.plotly_chart(fig_bar)

    with tab2:
        st.subheader("Datos Crudos")
        st.dataframe(filtered_data)


# 11. Ejecución del Script
if __name__ == "__main__":
    st.sidebar.info("Ejecuta este script con: streamlit run d:/Usuario/Descargas/larco/src/temperatura.py")