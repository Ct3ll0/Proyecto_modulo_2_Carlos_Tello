import io
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#clase dataanalyzer
class DataAnalyzer:
 
    def __init__(self, df: pd.DataFrame):
        self.df = df
 
    def clasificar_variables(self):
        numericas = self.df.select_dtypes(include=np.number).columns.tolist()
        categoricas = self.df.select_dtypes(exclude=np.number).columns.tolist()
        return numericas, categoricas
 
    def resumen_nulos(self):
        nulos = self.df.isnull().sum()
        nulos = nulos[nulos > 0].sort_values(ascending=False)
        return nulos
 
    def estadisticas_descriptivas(self, columnas=None):
        if columnas:
            return self.df[columnas].describe()
        return self.df.describe()
 
    def medidas_tendencia_central(self, columna: str):
        serie = self.df[columna]
        return {
            "media": serie.mean(),
            "mediana": serie.median(),
            "moda": serie.mode().iloc[0] if not serie.mode().empty else None,
        }
 
    def comparar_grupos(self, columna_numerica: str, columna_categorica: str):
        return self.df.groupby(columna_categorica)[columna_numerica].describe()

#configuracion de página
st.set_page_config(
    page_title="Proyecto 2 DMC",
    layout="wide",
)

#Session state
if "df" not in st.session_state:
    st.session_state.df = None


#Sidebar
st.sidebar.title("Navegación")
modulo = st.sidebar.radio(
    "Selecciona un módulo:",
    ["Home", "Carga de Datos", "Análisis Exploratorio (EDA)"],
)

st.sidebar.markdown("---")
st.sidebar.caption("Especialización Python for Analytics")
st.sidebar.caption("Carlos Tello")


#Home
def modulo_home():
    st.title("Análisis Exploratorio de Datos - Insurance Company")
 
    st.markdown(
        """
        Esta aplicación permite explorar y analizar el dataset
        InsuranceCompany, con el fin de identificar los factores
        que influyen en la renovación de las pólizas de seguro.

        Se aplican conceptos de análisis de datos, estadística descriptiva
        y visualización.

        """    
    )
 
    st.markdown("---")
 
    col1, col2 = st.columns(2)
 
    with col1:
        st.subheader("Datos del autor")
        st.markdown(
            """
            - **Nombre completo:** Carlos Tello
            - **Curso / Especialización:** Especialización en Python for Analytics
            - **Año:** 2026
            """
        )
    
    st.markdown("---")
 
    st.subheader("Explicación del dataset")
    st.markdown(
        """
        Este dataset contiene información histórica acerca de los clientes de una compañía
        de seguros, incluyen variables demográficas, económicas, historial
        de morosidad, canal de captación, tipo de residencia, valor de la prima
        y puntaje de evaluación del cliente.

        """
    )

    with col2:
        st.subheader("Tecnologías utilizadas")
        st.markdown(
            """
            - Python
            - Pandas 
            - NumPy
            - Streamlit
            - Matplotlib
            - Seaborn
            """
        )
 
#Dataset
def modulo_carga():
    st.title("Carga del Dataset")
 
    st.markdown(
        """
        Sube el archivo InsuranceCompany.csv para habilitar el módulo. Los análisis no se ejecutarán
        hasta que el archivo sea cargado correctamente.
        """
    )
 
    archivo = st.file_uploader("Selecciona el archivo csv", type=["csv"])
 
    if archivo is not None:
        try:
            df = pd.read_csv(archivo)
        except Exception as e:
            st.error(f" Ocurrió un error al leer el archivo: {e}")
            st.session_state.df = None
            return
 
        # Validación de archivo vacío
        if df.empty:
            st.error("El archivo cargado está vacío.")
            st.session_state.df = None
            return
        if "renewal" in df.columns:
            df["renewal"] = df["renewal"].map({1: "Sí", 0: "No"}).fillna(df["renewal"])
            df["renewal"] = df["renewal"].astype(str)
            
        st.session_state.df = df
        st.success("Archivo cargado correctamente.")
 
        st.subheader("Vista previa del dataset")
        st.dataframe(df.head())
 
        st.subheader("Dimensiones del dataset")
        col1, col2 = st.columns(2)
        col1.metric("Filas", df.shape[0])
        col2.metric("Columnas", df.shape[1])
 
    else:
        st.info("Aún no se ha cargado ningún archivo.")
        st.session_state.df = None
 


#Analisis exploratorio de datos (EDA)
def modulo_eda():
    st.title("Análisis Exploratorio de Datos (EDA)")

    if st.session_state.df is None:
        st.warning("Primero debes cargar el dataset en el módulo 'Carga de Datos'.")
        return

    # Ítem 1: Información general del dataset
    with tabs[0]:
        st.subheader("Información general del dataset")
 
        st.markdown("**`.info()`**")
        buffer = io.StringIO()
        df.info(buf=buffer)
        st.text(buffer.getvalue())
 
        col1, col2 = st.columns(2)
 
        with col1:
            st.markdown("**Tipos de datos**")
            st.dataframe(df.dtypes.astype(str).rename("Tipo de dato"))
 
        with col2:
            st.markdown("**Conteo de valores nulos**")
            nulos = analyzer.resumen_nulos()
            if nulos.empty:
                st.success("El dataset no tiene valores nulos.")
            else:
                st.dataframe(nulos.rename("Nulos"))
 
    # Ítem 2: Clasificación de variables
    with tabs[1]:
        st.subheader("Clasificación de variables")
 
        col1, col2 = st.columns(2)
 
        with col1:
            st.markdown(f"**Variables numéricas ({len(numericas)})**")
            st.write(numericas)
 
        with col2:
            st.markdown(f"**Variables categóricas ({len(categoricas)})**")
            st.write(categoricas)


#Rutas
if modulo == "Home":
    modulo_home()
elif modulo == "Carga de Datos":
    modulo_carga()
elif modulo == "Análisis Exploratorio (EDA)":
    modulo_eda()
