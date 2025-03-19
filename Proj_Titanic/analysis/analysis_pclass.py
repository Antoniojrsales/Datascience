import pandas as pd
import matplotlib.pyplot as plt

def contar_sobreviventes(df_titanic):
    """Agrupa e conta os passageiros por classe."""
    agrupando_pclass = df_titanic['Pclass'].value_counts()
    agrupando_pclass.index = ['Primeira classe', 'Segunda classe', 'Terceira classe']
    return agrupando_pclass

def criar_grafico_barras(agrupando_pclass):
    """Cria o gráfico de barras da contagem de passageiros por classe."""
    agrupando_pclass.plot(kind='bar', color=['gold', 'silver', 'brown'], alpha=0.7)
    plt.title('Distribuição de Passageiros por Classe')
    plt.xlabel('Classe')
    plt.ylabel('Quantidade')
    plt.xticks(rotation=0)
    plt.grid(True, linestyle='--', alpha=0.7)
    for i, v in enumerate(agrupando_pclass):
        plt.text(i, v + 5, str(v), ha='center', fontsize=10)
    plt.show()

def calcular_porcentagem_sobreviventes(df_titanic, agrupando_pclass):
    """Calcula e exibe a porcentagem de passageiros por classe."""
    total = len(df_titanic)
    porcentagem_classe1 = (agrupando_pclass[0] / total) * 100
    porcentagem_classe2 = (agrupando_pclass[1] / total) * 100
    porcentagem_classe3 = (agrupando_pclass[2] / total) * 100
    print(f'Porcentagem de Primeira Classe: {porcentagem_classe1:.2f}%')
    print(f'Porcentagem de Segunda Classe: {porcentagem_classe2:.2f}%')
    print(f'Porcentagem de Terceira Classe: {porcentagem_classe3:.2f}%')

def analisar_pclass(df_titanic):
    """Analisa a coluna 'Pclass'."""
    agrupando_pclass = contar_sobreviventes(df_titanic)
    criar_grafico_barras(agrupando_pclass)
    calcular_porcentagem_sobreviventes(df_titanic, agrupando_pclass)

if __name__ == "__main__":
    try:
        df_titanic = pd.read_csv('data/train.csv')
        analisar_pclass(df_titanic)
    except FileNotFoundError:
        print("Erro: Arquivo 'train.csv' não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")