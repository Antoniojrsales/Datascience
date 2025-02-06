#https://www.invertexto.com/fundamentosaula01#
#https://docs.google.com/presentation/d/1PUFZxgGoNns-7umvAmsJvBts0IdqDTU2/edit#slide=id.g1e170a61b16_0_26

''' 1 - Realize a leitura do dataset Iris e faça uma amostragem estratificada de 80% (40 amostras de cada classe) que deve ser usado para ajustar o algoritmo que você vai criar e os 20% (10 amostras de cada classe) restantes devem ser usados para medir a performance.
'''

#Bibiotecas
from sklearn.datasets import load_iris
import pandas as pd

iris = load_iris() # Carrega o conjunto de dados Iris
x_data = pd.DataFrame(iris['data'], columns=iris['feature_names']) # Cria um DataFrame com os dados de entrada (features) e nomeia as colunas com os nomes das características
x_data['target'] = iris['target'] # Adiciona uma coluna chamada 'target' ao DataFrame, que contém os rótulos das classes das flores (0, 1, 2)

#Amostra training dos dados 80%
trainingx_data0 = x_data.loc[x_data['target'] == 0].iloc[10:]
trainingx_data1 = x_data.loc[x_data['target'] == 1].iloc[10:]
trainingx_data2 = x_data.loc[x_data['target'] == 2].iloc[10:]
trainingx_data = pd.concat([trainingx_data0, trainingx_data1, trainingx_data2], axis=0).reset_index(drop=True)

print(trainingx_data) # Exibe o DataFrame completo

'''2 - Usando os dados amostrais, modele e crie um algoritmo (Usando técnicas de estatística como: média, mediana e desvio padrão, entre outras. Além de funções matemáticas de sua escolha, como a distância euclidiana.) que diferencie as classes virginica e setosa, que tenha uma performance (acertos/total) de pelo menos 70% de acerto.'''


'''3 - Agora, repita o processo, só que incluindo a classe versicolor.'''