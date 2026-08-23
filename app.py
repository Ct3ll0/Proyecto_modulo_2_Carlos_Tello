import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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
    st.markdown("*(contenido del módulo Home — pendiente de desarrollar)*")


#Dataset
def modulo_carga():
    st.title("📤 Carga del Dataset")
    st.markdown("*(contenido del módulo de carga — pendiente de desarrollar)*")


#Analisis exploratorio de datos (EDA)
def modulo_eda():
    st.title("🔍 Análisis Exploratorio de Datos (EDA)")

    if st.session_state.df is None:
        st.warning("⚠️ Primero debes cargar el dataset en el módulo 'Carga de Datos'.")
        return

    st.markdown("*(contenido del módulo EDA — pendiente de desarrollar)*")


#Rutas
if modulo == "Home":
    modulo_home()
elif modulo == "Carga de Datos":
    modulo_carga()
elif modulo == "Análisis Exploratorio (EDA)":
    modulo_eda()
