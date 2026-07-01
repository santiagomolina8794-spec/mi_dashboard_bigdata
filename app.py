import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(page_title="Dashboard Big Data", layout="wide")

# ==========================================
# MENU LATERAL (ESTILO POWER BI) - PERSONALIZADO
# ==========================================

# 1. Logo del Instituto
try:
    st.sidebar.image("logo_tec.png", use_container_width=True)
except:
    # Si aún no tienes la imagen en la carpeta, el código no se rompe
    st.sidebar.warning("📌 Coloca el archivo 'logo_tec.png' en la carpeta para ver el logo.")

st.sidebar.markdown("---")

# 2. Créditos del Desarrollador
st.sidebar.write("### 💻 Desarrollador:")
st.sidebar.info("**Santiago Molina**")
st.sidebar.write("*Tecnología Superior en Big Data*")
st.sidebar.write("**TEC Azuay**")

st.sidebar.markdown("---")

# 3. Menú de Navegación del Dashboard
st.sidebar.write("### 🗂️ Menú de Navegación")
menu = st.sidebar.selectbox(
    "Selecciona una sección:",
    ["📊 Exploración de Datos", "📈 Visualizaciones Estadísticas", "🧮 Análisis Avanzado"]
)

# ==========================================
# CONEXIÓN Y CARGA DE DATOS
# ==========================================
@st.cache_data
def cargar_datos():
    # Carga el archivo CSV local que ya pusiste en la carpeta
    df = pd.read_csv("datos_practica.csv", sep=",")
    df = df.replace("None", "Desconocido")
    df = df.fillna("Desconocido")
    return df

df = cargar_datos()

# ==========================================
# SECCIÓN 1: EXPLORACIÓN DE DATOS
# ==========================================
if menu == "📊 Exploración de Datos":
    st.title("📊 Dashboard Estilo Power BI - Big Data")
    st.subheader("Exploración General del Conjunto de Datos")
    
    # Métricas principales arriba en tarjetas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Registros", len(df))
    with col2:
        # Intenta calcular promedio de Edad si es numérica, si no pone texto
        try:
            edad_prom = round(pd.to_numeric(df['Edad'], errors='coerce').mean(), 1)
            st.metric("Edad Promedio", f"{edad_prom} años")
        except:
            st.metric("Edad Promedio", "N/D")
    with col3:
        try:
            salario_prom = round(pd.to_numeric(df['Salario'], errors='coerce').mean(), 2)
            st.metric("Salario Promedio", f"${salario_prom}")
        except:
            st.metric("Salario Promedio", "N/D")

    st.markdown("---")
    st.write("### Vista Previa de la Tabla de Datos")
    st.dataframe(df, use_container_width=True)

# ==========================================
# SECCIÓN 2: VISUALIZACIONES ESTADÍSTICAS
# ==========================================
elif menu == "📈 Visualizaciones Estadísticas":
    st.title("📈 Visualizaciones Estadísticas")
    st.subheader("Análisis Gráfico del Comportamiento de los Datos")

    col1, col2 = st.columns(2)

    with col1:
        st.write("#### Distribución de Frecuencias por Ciudad")
        if 'Ciudad' in df.columns:
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.countplot(data=df, x='Ciudad', ax=ax, palette='viridis')
            plt.xticks(rotation=45)
            st.pyplot(fig)
        else:
            st.warning("No se encontró la columna 'Ciudad'")

    with col2:
        st.write("#### Relación Edad vs Salario")
        try:
            df_num = df.copy()
            df_num['Edad'] = pd.to_numeric(df_num['Edad'], errors='coerce')
            df_num['Salario'] = pd.to_numeric(df_num['Salario'], errors='coerce')
            df_num = df_num.dropna(subset=['Edad', 'Salario'])
            
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.scatterplot(data=df_num, x='Edad', y='Salario', hue='Ciudad', ax=ax)
            st.pyplot(fig)
        except:
            st.warning("Asegúrate de que las columnas Edad y Salario contengan valores numéricos.")

# ==========================================
# SECCIÓN 3: ANÁLISIS AVANZADO Y DESCARGA
# ==========================================
elif menu == "🧮 Análisis Avanzado":
    st.title("🧮 Análisis Avanzado y Exportación")
    st.subheader("Procesamiento de Datos y Descargas")
    
    st.write("Aquí puedes descargar los datos limpios y procesados en un formato listo para el reporte final:")
    
    # Conversión del DataFrame a CSV para la descarga
    csv = df.to_csv(index=False).encode("utf-8")
    
    # Botón de descarga con el paréntesis cerrado correctamente
    st.download_button(
        label="⬇️ Descargar CSV Transformado",
        data=csv,
        file_name="datos_transformados.csv",
        mime="text/csv"
    )

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 - Sprint Final Big Data")
    

    

