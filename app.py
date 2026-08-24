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
    df = st.session_state.df
    analyzer = DataAnalyzer(df)
    numericas, categoricas = analyzer.clasificar_variables()

    tabs = st.tabs([
        "1. Info general",
        "2. Clasificación",
        "3. Descriptivas",
        "4. Valores faltantes",
        "5. Distribución numérica",
        "6. Variables categóricas",
        "7. Numérico vs categórico",
        "8. Categórico vs categórico",
        "9. Análisis dinámico",
        "10. Hallazgos clave"
    ])
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
        st.caption("Clasificación se obtiene usando la función personalizada `clasificar_variables()` de la clase DataAnalyzer")
        col1, col2 = st.columns(2)
 
        with col1:
            st.markdown(f"**Variables numéricas ({len(numericas)})**")
            st.write(numericas)
 
        with col2:
            st.markdown(f"**Variables categóricas ({len(categoricas)})**")
            st.write(categoricas)

      # Ítem 3: Estadísticas descriptivas
    with tabs[2]:
        st.subheader("Estadísticas descriptivas")

        st.markdown("**`.describe()`**")
        st.dataframe(analyzer.estadisticas_descriptivas())

        st.markdown("**Interpretación básica**")
        col1, col2, col3 = st.columns(3)
        columna_sel = st.selectbox("Selecciona una variable numérica:", numericas, key="item3_select")
        medidas = analyzer.medidas_tendencia_central(columna_sel)
        col1.metric("Media", f"{medidas['media']:.2f}")
        col2.metric("Mediana", f"{medidas['mediana']:.2f}")
        col3.metric("Moda", f"{medidas['moda']:.2f}")
        st.caption(
            f"La media y la mediana de **{columna_sel}** "
            f"{'son similares, es una distribución de tendencia simétrica.' if abs(medidas['media'] - medidas['mediana']) / (medidas['mediana'] + 1e-9) < 0.1 else 'son muy diferentes, es una distribución de tendencia asimetría.'}"
        )

    # Ítem 4: Análisis de valores faltantes
    with tabs[3]:
        st.subheader("Análisis de valores faltantes")

        nulos = analyzer.resumen_nulos()

        if nulos.empty:
            st.success("El dataset no presenta valores faltantes en ninguna columna.")
        else:
            st.markdown("**Conteo de valores nulos por columna**")
            st.dataframe(nulos.rename("Nulos"))

            st.markdown("**Visualización**")
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.barplot(x=nulos.values, y=nulos.index, ax=ax, color="steelblue")
            ax.set_xlabel("Cantidad de nulos")
            ax.set_ylabel("Columna")
            st.pyplot(fig)

            st.markdown("**Discusión**")
            st.write(
                f"Las columnas con más valores faltantes son "
                f"**{', '.join(nulos.index[:3].tolist())}**. "
                "Esto debe resolverse antes de realizar los análisis, "
                "ya sea mediante imputación o exclusión de datos."
            )
        # Ítem 5: Distribución de variables numéricas
    with tabs[4]:
        st.subheader("Distribución de variables numéricas")

        columna_num = st.selectbox("Selecciona una variable numérica:", numericas, key="item5_select")

        fig, ax = plt.subplots(figsize=(8, 4))
        sns.histplot(df[columna_num].dropna(), kde=True, ax=ax, color="steelblue")
        ax.set_xlabel(columna_num)
        ax.set_ylabel("Frecuencia")
        st.pyplot(fig)

        st.caption(
            f"El histograma de **{columna_num}** permite observar la forma de la distribución "
            "(simétrica, sesgada, con posibles valores atípicos)."
        )

    # Ítem 6: Análisis de variables categóricas
    with tabs[5]:
        st.subheader("Análisis de variables categóricas")

        if not categoricas:
            st.info("El dataset no tiene variables categóricas.")
        else:
            columna_cat = st.selectbox("Selecciona una variable categórica:", categoricas, key="item6_select")

            conteo = df[columna_cat].value_counts()
            proporcion = df[columna_cat].value_counts(normalize=True) * 100

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Conteo**")
                st.dataframe(conteo.rename("Conteo"))

            with col2:
                st.markdown("**Proporción (%)**")
                st.dataframe(proporcion.round(2).rename("Proporción (%)"))

            fig, ax = plt.subplots(figsize=(8, 4))
            sns.barplot(x=conteo.index, y=conteo.values, ax=ax, color="steelblue")
            ax.set_xlabel(columna_cat)
            ax.set_ylabel("Conteo")
            plt.xticks(rotation=45)
            st.pyplot(fig)
         
    # Ítem 7: Análisis bivariado (numérico vs categórico)
    with tabs[6]:
        st.subheader("Análisis bivariado: numérico vs categórico")

        col1, col2 = st.columns(2)
        with col1:
            var_num = st.selectbox("Variable numérica:", numericas, key="item7_num")
        with col2:
            var_cat = st.selectbox("Variable categórica:", categoricas, key="item7_cat")

        st.markdown(f"**Comparación de `{var_num}` según `{var_cat}`**")
        st.dataframe(analyzer.comparar_grupos(var_num, var_cat))

        fig, ax = plt.subplots(figsize=(8, 4))
        sns.boxplot(data=df, x=var_cat, y=var_num, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # Ítem 8: Análisis bivariado (categórico vs categórico)
    with tabs[7]:
        st.subheader("Análisis bivariado: categórico vs categórico")

        if len(categoricas) < 2:
            st.info("Se necesitan al menos dos variables categóricas para este análisis.")
        else:
            col1, col2 = st.columns(2)
            with col1:
                var_cat1 = st.selectbox("Primera variable categórica:", categoricas, key="item8_cat1")
            with col2:
                opciones_cat2 = [c for c in categoricas if c != var_cat1]
                var_cat2 = st.selectbox("Segunda variable categórica:", opciones_cat2, key="item8_cat2")

            tabla_cruzada = pd.crosstab(df[var_cat1], df[var_cat2])
            st.markdown(f"**Tabla cruzada: `{var_cat1}` vs `{var_cat2}`**")
            st.dataframe(tabla_cruzada)

            fig, ax = plt.subplots(figsize=(8, 4))
            tabla_cruzada.plot(kind="bar", stacked=True, ax=ax)
            plt.xticks(rotation=45)
            st.pyplot(fig)

#Rutas
if modulo == "Home":
    modulo_home()
elif modulo == "Carga de Datos":
    modulo_carga()
elif modulo == "Análisis Exploratorio (EDA)":
    modulo_eda()
