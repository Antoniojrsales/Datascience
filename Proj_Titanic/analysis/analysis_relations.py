import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analysis_relations_pclassVsurvived(df_titanic):
    #Analisa a relação entre as colunas Pclass Vs Survived.
    taxa_sobrevivencia_classe = df_titanic.groupby('Pclass')['Survived'].mean() * 100
    print('Taxa de Sobrevivência por Classe no Titanic')
    for classe, taxa in taxa_sobrevivencia_classe.items():
        print(f'Classe {classe}: {taxa:.2f}%')

    # Gráfico de barras da taxa de sobrevivência por classe
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=taxa_sobrevivencia_classe.index, y=taxa_sobrevivencia_classe.values, ax=ax, palette='viridis', hue=taxa_sobrevivencia_classe.index, legend=True)
    plt.title('Taxa de Sobrevivência por Classe')
    plt.xlabel('Classe')
    plt.ylabel('Taxa de Sobrevivência (%)')
    for i, v in enumerate(taxa_sobrevivencia_classe.values):
        plt.text(i, v + 1, f'{v:.2f}', ha='center')
    plt.legend(title='Classe do Passageiro', loc='upper right')
    plt.show()

def analysis_relations_sexoVsurvived(df_titanic):
    #Analisa a relação entre as colunas Pclass Vs Survived.
    df_titanic.loc[df_titanic['Sex'] == 'male', 'Sex'] = 'Masculino'
    df_titanic.loc[df_titanic['Sex'] == 'female', 'Sex'] = 'Feminino'
    taxa_sobrevivencia_sexo = df_titanic.groupby('Sex')['Survived'].mean() * 100
    print('Taxa de Sobrevivência por Sexo no Titanic')
    for classe, taxa in taxa_sobrevivencia_sexo.items():
        print(f'Classe {classe}: {taxa:.2f}%')

    # Gráfico de barras da taxa de sobrevivência por classe
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.barplot(x=taxa_sobrevivencia_sexo.index, y=taxa_sobrevivencia_sexo.values, ax=ax, palette='cividis', hue=taxa_sobrevivencia_sexo.index, legend=True)
    plt.title('Taxa de Sobrevivência por Classe')
    plt.xlabel('Sexo')
    plt.ylabel('Taxa de Sobrevivência (%)')
    for i, v in enumerate(taxa_sobrevivencia_sexo.values):
        plt.text(i, v + 1, f'{v:.2f}', ha='center')
    plt.legend(title='Classe por sexo', loc='upper right')
    plt.show()

if __name__ == "__main__":
    try:
        df_titanic = pd.read_csv('data/train.csv')
        analysis_relations_pclassVsurvived(df_titanic)
        analysis_relations_sexoVsurvived(df_titanic)
    except FileNotFoundError:
        print("Erro: Arquivo 'train.csv' não encontrado.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")