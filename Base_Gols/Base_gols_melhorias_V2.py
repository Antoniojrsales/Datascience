# Importação de bibliotecas
import pandas as pd
import numpy as np
import gspread
from gspread_dataframe import set_with_dataframe

# Configuração para acesso ao Google Sheets
try:
    gc = gspread.service_account(filename='GBQjson.json')
    dfs = gc.open_by_url('https://docs.google.com/spreadsheets/d/154gX579nPaM0WhcBtNUES2EMRDQqP2jDbdvSpJ_Fstc/edit?gid=1457355959')
except Exception as e:
    print(f"Erro ao conectar com o Google Sheets: {e}")

# Função para carregar e processar cada aba
def load_worksheet_data(worksheet_name):
    try:
        worksheet = dfs.worksheet(worksheet_name)
        data = worksheet.get_all_values()
        colunas = data.pop(0)
        df = pd.DataFrame(data, columns=colunas).drop(index=0).reset_index(drop=True)
        return df
    except Exception as e:
        print(f"Erro ao carregar dados da aba {worksheet_name}: {e}")
        return pd.DataFrame()

# Carregamento e preparação de dados
df_aba1 = load_worksheet_data('Day')
df_aba2 = load_worksheet_data('BD_GolsGeral')
df_aba3 = load_worksheet_data('BD_Gols05HTHome')
df_aba4 = load_worksheet_data('BD_Gols05HTAway')

# Seleção de colunas específicas
df_selecionada_aba2 = df_aba2[['Campeonato', 'Time', 'Partidas', 'Avg', 'FT15', 'FT25']]
df_selecionada_aba3 = df_aba3[['Campeonato', 'Time', 'HT05HOME']]
df_selecionada_aba4 = df_aba4[['Campeonato', 'Time', 'HT05AWAY']]

# Juntando dados
try:
    df_temp = pd.merge(df_selecionada_aba2, df_selecionada_aba3, on=['Campeonato', 'Time'], how='left')
    df_basegols = pd.merge(df_temp, df_selecionada_aba4, on=['Campeonato', 'Time'], how='left')
except Exception as e:
    print(f"Erro ao mesclar as abas: {e}")

# Renomeando colunas time away
df_basegols_Away = df_basegols.rename(columns={
    'FT15': 'FT15Away', 'FT25': 'FT25Away', 'Avg': 'Avg_Away', 
    'Time': 'Time_Away'}).drop(columns=['HT05HOME'], errors='ignore')

# Mesclando as tabelas principais para análise
try:
    df_time_Home = pd.merge(df_aba1, df_basegols, on=['Time'], how='left')
    df_jogodia = pd.merge(df_time_Home, df_basegols_Away, on=['Time_Away'], how='left')
except Exception as e:
    print(f"Erro ao combinar dados de time: {e}")

df_jogodia['Data'] = pd.Timestamp.today().date()

# Renomeação de colunas
df_jogodia.rename(columns={
    'HT05AWAY_y': 'HT05Away', 'HT05HOME': 'HT05Home',
    'FT25': 'FT25Home', 'FT15': 'FT15Home', 'Avg': 'Avg_Home',
    'Time': 'Time_Home', 'Campeonato_x': 'Campeonato_Home',
    'Partidas_x': 'Partidas_Home', 'Campeonato_y': 'Campeonato_Away',
    'Partidas_y': 'Partidas_Away'
}, inplace=True)

ordem = ['Data', 'Campeonato_Home', 'Time_Home', 'X', 'Time_Away', 'Campeonato_Away', 'Partidas_Home', 'Avg_Home', 
         'HT05Home', 'FT15Home', 'FT25Home',  'Partidas_Away', 'Avg_Away', 'HT05Away', 'FT15Away', 'FT25Away']
df_jogodia = df_jogodia[ordem]

# Conversão para float nas colunas numéricas
for col in ['Avg_Home', 'HT05Home', 'Avg_Away', 'HT05Away']:
    df_jogodia[col] = pd.to_numeric(df_jogodia[col], errors='coerce')

# Consulta final
df_jogos_selecionados = df_jogodia.query('Avg_Home > 2.5 and HT05Home > 75 and Avg_Away > 2.5 and HT05Away > 70')
df_jogos_selecionados2 = df_jogodia.query('FT25Home > "70" and FT25Away > "70"')

'''#Automatiza o envio dos dados coletados do Dataframe para o Google Sheets
try:
    worksheet = dfs.worksheet("Novas_Apostas")
except gspread.exceptions.WorksheetNotFound:
    worksheet = dfs.add_worksheet(title="Novas_Apostas", rows=10000, cols=20)

# Encontre a última linha preenchida
last_row = len(worksheet.get_all_values())
set_with_dataframe(worksheet, df_jogos_selecionados, row=last_row + 1)

print("Dados enviados com sucesso para o Google Sheets.")'''

print(df_jogos_selecionados)
print(df_jogos_selecionados.shape)

'''#Salvamento opcional dos dados finais
try:
    df_jogos_selecionados.to_excel('Jogos_Selecionados.xlsx', index=False)
    print("Arquivo salvo com sucesso.")
except Exception as e:
    print(f"Erro ao salvar o arquivo: {e}")'''
