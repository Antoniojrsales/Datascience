import pandas as pd
import matplotlib.pyplot as plt

def contar_sobreviventes_sexo(df_titanic):
    df_titanic.loc[df_titanic['Sex'] == 'male', 'Sex'] = 'Masculino'
    df_titanic.loc[df_titanic['Sex'] == 'female', 'Sex'] = 'Feminino'
    agrupando_sexo = df_titanic['Sex'].value_counts()
    return agrupando_sexo

def criar_grafico_barras(agrupando_sexo):
    """Cria o gráfico de barras da contagem de passageiros por classe."""
    agrupando_sexo.plot(kind='bar', color=['blue', 'pink'], alpha=0.7)
    plt.title('Distribuição de passageiros por sexo')
    plt.xlabel('Sexo')
    plt.ylabel('Quantidade')
    plt.xticks(rotation=0)
    plt.grid(True, linestyle='--', alpha=0.7)
    for i, v in enumerate(agrupando_sexo):
        plt.text(i, v + 5, str(v), ha='center', fontsize=10)
    plt.show()

def calcular_porcentagem_sobreviventes_sexo(df_titanic, agrupando_sexo):
    """Calcula e exibe a porcentagem de passageiros por sexo."""
    total = len(df_titanic)
    porcentagem_masculino = (agrupando_sexo[0] / total) * 100
    porcentagem_feminino = (agrupando_sexo[1] / total) * 100
    print(f'Porcentagem de Masculino: {porcentagem_masculino:.2f}%')
    print(f'Porcentagem de Feminino: {porcentagem_feminino:.2f}%')

def calcular_taxa_sobrevivencia_sexo(df_titanic):
    """Calcula e exibe a taxa de sobrevivência por sexo."""
    taxa_sobrevivencia = df_titanic.groupby('Sex')['Survived'].mean() * 100
    print('Taxa de Sobrevivência por Sexo:')
    for sexo, taxa in taxa_sobrevivencia.items():
        print(f'{sexo}: {taxa:.2f}%')

def analisar_sex(df_titanic):
    """Analisa a coluna 'Pclass'."""
    agrupando_sexo = contar_sobreviventes_sexo(df_titanic)
    criar_grafico_barras(agrupando_sexo)
    calcular_porcentagem_sobreviventes_sexo(df_titanic, agrupando_sexo)
    calcular_taxa_sobrevivencia_sexo(df_titanic)

if __name__ == "__main__":
    try:
        df_titanic = pd.read_csv('data/train.csv')
        analisar_sex(df_titanic)
    except FileNotFoundError:
        print("Erro: Arquivo 'train.csv' não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")