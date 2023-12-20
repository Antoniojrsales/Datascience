import streamlit as st

st.title('Exemplo de Imagem no Streamlit')
radio_selecionado = st.radio('Selecione a variedade',[":rainbow[Setosa]","Versicolor",'Virginica'],horizontal=True)
if radio_selecionado == ":rainbow[Setosa]":
   # Carregando e exibindo a imagem
   imagem = 'setosa.png'
   st.image(imagem, width=300)
elif radio_selecionado == 'Versicolor':
   # Carregando e exibindo a imagem
   imagem = 'versicolor.png'
   st.image(imagem, width=300)
elif radio_selecionado == 'Virginica':
   # Carregando e exibindo a imagem
   imagem = 'virginica.png'
   st.image(imagem, width=300)
