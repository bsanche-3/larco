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
    layout="wide",
    initial_sidebar_state="expanded"
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

if menu == "Inicio":
    st.subheader("📄 Bienvenido al Dashboard de Larco")
    #readme_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "README.md"))
    readme_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "README.md"))
    st.write(f"Ruta del README: {readme_path}")
    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()
    # Mostrar el texto del README sin imágenes
    st.markdown(readme_content.split("## Capturas de Pantalla")[0], unsafe_allow_html=True)

    # Mostrar las imágenes manualmente
    image_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "images"))
    st.image(os.path.join(image_dir, "image.png"), caption="Inicio")
    st.image(os.path.join(image_dir, "image-1.png"), caption="Datos")
    st.image(os.path.join(image_dir, "image-2.png"), caption="Gráficos")
    st.image(os.path.join(image_dir, "image-3.png"), caption="KPI")

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
    tab1, tab2, tab3 = st.tabs(["📊 Gráficos", "📂 Datos", "📈 Estadísticos"])
    with tab1:
        st.subheader("Visualización de Datos")
        
        if st.checkbox("Mostrar Gráfico de Dispersión (TEMP vs RH)"):
            st.markdown("📌 **Propósito**: Visualizar la relación entre temperatura y humedad a lo largo del día.")
            fig_scatter = px.scatter(filtered_data, x="TEMP", y="RH", color="HOUR", title="Relación entre Temperatura y Humedad por Hora")
            st.plotly_chart(fig_scatter)

        if st.checkbox("Mostrar Evolución de Temperatura y Humedad"):
            st.markdown("📌 **Propósito**: Analizar cómo evolucionan la temperatura y la humedad a lo largo del tiempo.")
            fig_temp_hum = px.line(filtered_data, x="DATE", y=["TEMP", "RH"], title="Evolución de Temperatura y Humedad")
            st.plotly_chart(fig_temp_hum)

        if st.checkbox("Mostrar Boxplot de Temperatura por Hora"):
            st.markdown("📌 **Propósito**: Identificar la distribución de la temperatura a diferentes horas del día y detectar valores atípicos.")
            fig_box = px.box(filtered_data, x="HOUR", y="TEMP", title="Distribución de Temperatura por Hora del Día")
            st.plotly_chart(fig_box)

        if st.checkbox("Mostrar Histograma de Temperatura"):
            st.markdown("📌 **Propósito**: Mostrar la distribución de la temperatura y detectar patrones de frecuencia.")
            fig_hist = px.histogram(filtered_data, x="TEMP", nbins=20, title="Distribución de la Temperatura")
            st.plotly_chart(fig_hist)

        if st.checkbox("Mostrar Mapa de Calor"):
            st.markdown("📌 **Propósito**: Visualizar la densidad de temperatura y humedad en diferentes horas del día.")
            fig_heatmap = px.density_heatmap(filtered_data, x="HOUR", y="TEMP", z="RH", title="Mapa de Calor: Temperatura y Humedad por Hora")
            st.plotly_chart(fig_heatmap)

        if st.checkbox("Mostrar Mapa de Calor de Correlaciones"):
            st.markdown("📌 **Propósito**: Identificar correlaciones entre temperatura y humedad en los datos.")
            corr_matrix = filtered_data[["TEMP", "RH"]].corr()
            fig_heatmap = plt.figure(figsize=(6, 4))
            sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f")
            st.pyplot(fig_heatmap)

        if st.checkbox("Mostrar Distribución de la Temperatura"):
            st.markdown("📌 **Propósito**: Examinar la dispersión de la temperatura y detectar posibles anomalías.")
            fig_box = px.box(filtered_data, y="TEMP", title="Distribución de la Temperatura")
            st.plotly_chart(fig_box)

        if st.checkbox("Mostrar Temperatura Promedio por Hora"):
            st.markdown("📌 **Propósito**: Observar cómo varía la temperatura promedio en diferentes horas del día.")
            filtered_data["HOUR"] = pd.to_datetime(filtered_data["TIME"], format="%H:%M:%S").dt.hour
            temp_avg_hour = filtered_data.groupby("HOUR")["TEMP"].mean().reset_index()

            fig_bar = px.bar(temp_avg_hour, x="HOUR", y="TEMP", title="Temperatura Promedio por Hora", color="HOUR")
            st.plotly_chart(fig_bar)

    with tab2:
        st.subheader("Datos Crudos")
        st.dataframe(filtered_data)
    
    with tab3:
        st.subheader("Estadísticas Descriptivas")
        st.markdown("📌 **Propósito**: Ver estadísticas clave de las variables de temperatura y humedad.")

        stats = filtered_data[["TEMP", "RH"]].describe().T  # Transponer para mejor visualización
        stats.rename(columns={
            "count": "Conteo",
            "mean": "Promedio",
            "std": "Desviación Estándar",
            "min": "Mínimo",
            "25%": "Percentil 25",
            "50%": "Mediana",
            "75%": "Percentil 75",
            "max": "Máximo"
        }, inplace=True)
        
        # Mostrar tabla en Streamlit
        st.dataframe(stats)
    
        # Calcular métricas clave
        temp_min = filtered_data["TEMP"].min()
        temp_max = filtered_data["TEMP"].max()
        temp_mean = filtered_data["TEMP"].mean()
        temp_median = filtered_data["TEMP"].median()
        temp_std = filtered_data["TEMP"].std()

        rh_min = filtered_data["RH"].min()
        rh_max = filtered_data["RH"].max()
        rh_mean = filtered_data["RH"].mean()
        rh_median = filtered_data["RH"].median()
        rh_std = filtered_data["RH"].std()
        
        # Crear columnas para KPI Cards
        st.markdown("---")
        col1, col2, col3, col4, col5 = st.columns(5)

        # Estilo CSS para los bordes
        st.markdown("""
            <style>
            .main {
                padding: 20px;
                text-align: center; /* Centra el contenido del contenedor principal */
            }
            .stMetric {
                background-color: #000000;
                padding: 10px;
                border-radius: 5px;
                text-align: center; /* Centra el contenido de la métrica */
            }
            div[data-testid="stMetricValue"] {
                font-size: 20px !important;
                text-align: center; /* Asegura que el valor esté centrado */
            }
            </style>
        """, unsafe_allow_html=True)


        # Mostrar KPIs en cajas con bordes y fechas
        with col1:
            with st.container():
                st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
                st.metric(label="📈 Temp. Máxima (°C)", value=f"{temp_max:.2f}", delta=f"Fecha: {data.loc[data['TEMP'].idxmax(), 'DATE'].strftime('%d/%m/%Y')}")
                st.metric(label="💧 Humedad Máxima (%)", value=f"{rh_max:.2f}", delta=f"Fecha: {data.loc[data['RH'].idxmax(), 'DATE'].strftime('%d/%m/%Y')}")
                st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            with st.container():
                st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
                st.metric(label="📉 Temp. Mínima (°C)", value=f"{temp_min:.2f}", delta=f"Fecha: {data.loc[data['TEMP'].idxmin(), 'DATE'].strftime('%d/%m/%Y')}")
                st.metric(label="💧 Humedad Mínima (%)", value=f"{rh_min:.2f}", delta=f"Fecha: {data.loc[data['RH'].idxmin(), 'DATE'].strftime('%d/%m/%Y')}")
                st.markdown('</div>', unsafe_allow_html=True)

        with col3:
            with st.container():
                st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
                st.metric(label="🌡️ Temperatura Promedio (°C)", value=f"{temp_mean:.2f}")
                st.metric(label="💨 Humedad Promedio (%)", value=f"{rh_mean:.2f}")
                st.markdown('</div>', unsafe_allow_html=True)

        with col4:
            with st.container():
                st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
                st.metric(label="📊 Mediana Temp. (°C)", value=f"{temp_median:.2f}")
                st.metric(label="📊 Mediana Humedad (%)", value=f"{rh_median:.2f}")
                st.markdown('</div>', unsafe_allow_html=True)

        with col5:
            with st.container():
                st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
                st.metric(label="🌡️ Desviación Std. Temp. (°C)", value=f"{temp_std:.2f}")
                st.metric(label="💨 Desviación Std. Humedad (%)", value=f"{rh_std:.2f}")
                st.markdown('</div>', unsafe_allow_html=True)

# 11. Ejecución del Script
if __name__ == "__main__":
    st.sidebar.info("Ejecuta este script con: streamlit run d:/Usuario/Descargas/larco/src/temperatura.py")