import streamlit as st
import pickle 
# load
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)
st.sidebar.title('Sidebar')
# Opções na barra lateral
opcao_1 = st.sidebar.slider('sepal length (cm)', 0.00, 10.00, 0.1)
opcao_2 = st.sidebar.slider('sepal width (cm)', 0.00, 10.00, 0.1)
opcao_3 = st.sidebar.slider('petal length (cm)', 0.00, 10.00, 0.1)
opcao_4 = st.sidebar.slider('petal width (cm)', 0.00, 10.00, 0.1)

new_data = [[opcao_1, opcao_2, opcao_3, opcao_4]]
predicted = model.predict(new_data)


btn = st.button('Clique aqui para fazer a previsao', type='primary')

if btn:
    # 'setosa', 'versicolor', 'virginica'
    #st.write(predicted)
    if predicted[0] == 0:
        imagem = 'setosa.png'
        st.image(imagem, width=300)
    elif predicted[0] == 1:
        imagem = 'versicolor.png'
        st.image(imagem, width=300)
    elif predicted[0] == 2:
        imagem = 'virginica.png'
        st.image(imagem, width=300)