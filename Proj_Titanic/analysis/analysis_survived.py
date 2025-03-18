import pandas as pd
import matplotlib.pyplot as plt

def contar_sobreviventes(df):
    """Agrupa e conta os sobreviventes."""
    agrupando_survived = df['Survived'].value_counts()
    agrupando_survived.index = ['Não Sobreviveram', 'Sobreviveram']
    return agrupando_survived

def criar_grafico_barras(agrupando_survived):
    """Cria o gráfico de barras da contagem de sobreviventes."""
    agrupando_survived.plot(kind='bar', color=['blue', 'green'], alpha=0.7)
    plt.title('Contagem (Sobreviveram vs Não Sobreviveram)')
    plt.xlabel('Status de Sobrevivência')
    plt.ylabel('Quantidade')
    plt.xticks(rotation=0)
    plt.grid(True, linestyle='--', alpha=0.7)
    for i, v in enumerate(agrupando_survived):
        plt.text(i, v + 5, str(v), ha='center', fontsize=10)
    plt.show()

def calcular_porcentagem_sobreviventes(df, agrupando_survived):
    """Calcula e exibe a porcentagem de sobreviventes."""
    total = len(df)
    porcentagem_nao_sobreviveu = (agrupando_survived[0] / total) * 100
    porcentagem_sobreviveu = (agrupando_survived[1] / total) * 100
    print(f'Porcentagem de Não Sobreviventes: {porcentagem_nao_sobreviveu:.2f}%')
    print(f'Porcentagem de Sobreviventes: {porcentagem_sobreviveu:.2f}%')

def analisar_survived(df):
    """Analisa a coluna 'Survived'."""
    agrupando_survived = contar_sobreviventes(df)
    criar_grafico_barras(agrupando_survived)
    calcular_porcentagem_sobreviventes(df, agrupando_survived)

if __name__ == "__main__":
    try:
        df_titanic = pd.read_csv('data/train.csv')
        analisar_survived(df_titanic)
    except FileNotFoundError:
        print("Erro: Arquivo 'train.csv' não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
