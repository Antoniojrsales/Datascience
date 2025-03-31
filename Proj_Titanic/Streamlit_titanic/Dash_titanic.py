import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image
import io

@st.cache_data
def gerar_df():
    df_titanic = pd.read_csv('data/train.csv')
    return df_titanic

with st.sidebar:
    st.header('Titanic')
    logo = Image.open('titanic.jpeg')
    st.image(logo, use_container_width=True)
    st.subheader('EDA (Ánalise exploratoria de dados)')
    fcoluna = st.selectbox(
        "Visão geral do Dataset",
        options=['Default', 'Dataset', 'Info', 'Describe', 'isnull']
    )

df_titanic = gerar_df()

df_titanic = gerar_df()

if fcoluna == 'Dataset':
    st.subheader('Dataset')
    st.dataframe(df_titanic)
elif fcoluna == 'Info':
    st.subheader('Informações do Dataset')
    buffer = io.StringIO()
    df_titanic.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)  # Usar st.text() para exibir a string
elif fcoluna == 'Describe':
    st.subheader('Estatísticas Descritivas')
    st.write(df_titanic.describe())
elif fcoluna == 'isnull':
    st.subheader('Valores Nulos')
    st.write(df_titanic.isnull().sum())
elif fcoluna == 'Default':
    st.write("Selecione uma opção na barra lateral para visualizar os dados.")