import pandas as pd
from utils import visualization

def load_data(filepath):
    """Carrega os dados do arquivo CSV."""
    return pd.read_csv(filepath)

def analysis_survived(df_titanic):
    """Analisa a coluna 'Survived'."""
    # ... código para análise da coluna 'Survived' ...
    visualization.plot_bar_chart(df_titanic['Survived'].value_counts(), 'Contagem de Sobreviventes')

def analysis_pclass(df_titanic):
    """Analisa a coluna 'Survived'."""
    # ... código para análise da coluna 'Survived' ...
    visualization.plot_bar_chart(df_titanic['Pclass'].value_counts(), 'Contagem de Passageiros por Classe')

if __name__ == "__main__":
    df_titanic = load_data('data/train.csv')
    analysis_survived(df_titanic)
    analysis_pclass(df_titanic)