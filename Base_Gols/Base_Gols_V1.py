#Bibliotecas
import pandas as pd
import numpy as np
import gspread

# Autorizações para acesso remoto 
gc = gspread.service_account(filename='GBQjson.json')

# Caminho para o arquivo 
dfs = gc.open_by_url('https://docs.google.com/spreadsheets/d/154gX579nPaM0WhcBtNUES2EMRDQqP2jDbdvSpJ_Fstc/edit?gid=1457355959#gid=1457355959')

# Acessa as abas específicas e coleta os dados
worksheet_day = dfs.worksheet('Day')
worksheet_day.get_all_values()
colunas_aba1 = worksheet_day.get_all_values().pop(0)

worksheet_BD_GolsGeral = dfs.worksheet('BD_GolsGeral')
worksheet_BD_GolsGeral.get_all_values()
colunas_aba2 = worksheet_BD_GolsGeral.get_all_values().pop(0)

worksheet_BD_Gols05HTHome = dfs.worksheet('BD_Gols05HTHome')
worksheet_BD_Gols05HTHome.get_all_values()
colunas_aba3 = worksheet_BD_Gols05HTHome.get_all_values().pop(0)

worksheet_BD_Gols05HTAway = dfs.worksheet('BD_Gols05HTAway')
worksheet_BD_Gols05HTAway.get_all_values()
colunas_aba4 = worksheet_BD_Gols05HTAway.get_all_values().pop(0)

#Criando os Dataframe 
df_aba1 = pd.DataFrame(data=worksheet_day.get_all_values(), columns=colunas_aba1).drop(index=0).reset_index(drop=True)
df_aba2 = pd.DataFrame(data=worksheet_BD_GolsGeral.get_all_values(), columns=colunas_aba2).drop(index=0).reset_index(drop=True)
df_aba3 = pd.DataFrame(data=worksheet_BD_Gols05HTHome.get_all_values(), columns=colunas_aba3).drop(index=0).reset_index(drop=True)
df_aba4 = pd.DataFrame(data=worksheet_BD_Gols05HTAway.get_all_values(), columns=colunas_aba4).drop(index=0).reset_index(drop=True)

# Remover espaços extras e padronizar capitalização nas colunas 'Campeonato' e 'Time'
for df in [df_aba2, df_aba3, df_aba4]:
    df['Campeonato'] = df['Campeonato'].str.strip().str.lower()
    df['Time'] = df['Time'].str.strip().str.lower()

df_aba1['Time'] = df_aba1['Time'].str.strip().str.lower()
df_aba1['Time_Away'] = df_aba1['Time_Away'].str.strip().str.lower()

# Selecionar colunas específicas
df_selecionada_aba2 = df_aba2[['Campeonato', 'Time', 'Partidas', 'Avg', 'FT15', 'FT25']]
df_selecionada_aba3 = df_aba3[['Campeonato', 'Time', 'HT05HOME']]
df_selecionada_aba4 = df_aba4[['Campeonato', 'Time', 'HT05AWAY']]

# Juntando os dados das abas e criando a base df_basegols
df_temp = pd.merge(df_selecionada_aba2, df_selecionada_aba3, on=['Campeonato', 'Time'], how='left')
df_basegols = pd.merge(df_temp, df_selecionada_aba4, on=['Campeonato', 'Time'], how='left')

# Criando uma copy para manipular os dados do time Away
df_basegols_Away = df_basegols.copy()
df_basegols_Away.rename(columns={'FT15': 'FT15Away', 'FT25': 'FT25Away'}, inplace=True)
df_basegols_Away.rename(columns={'Avg': 'Avg_Away', 'Time': 'Time_Away'}, inplace=True)
df_basegols_Away.drop(columns=['HT05HOME'], inplace=True)

df_time_Home = pd.merge(df_aba1, df_basegols, on=['Time'], how='left')
#df_time_Away = pd.merge(df_aba1, df_basegols_Away, on=['Time_Away'], how='left')
df_jogodia = pd.merge(df_time_Home, df_basegols_Away, on=['Time_Away'], how='left')

ordem = ['Campeonato_x', 'Time', 'X', 'Time_Away', 'Campeonato_y', 'Partidas_x', 'Avg', 
         'HT05HOME', 'FT15', 'FT25',  'Partidas_y', 'Avg_Away', 'HT05AWAY_y', 'FT15Away', 'FT25Away']
df_jogodia = df_jogodia[ordem]

df_jogodia.rename(columns={
    'HT05AWAY_y': 'HT05Away','HT05HOME': 'HT05Home',
    'FT25': 'FT25Home','FT15': 'FT15Home','Avg': 'Avg_Home',
    'Time': 'Time_Home', 'Campeonato_x': 'Campeonato_Home',
    'Partidas_x': 'Partidas_Home', 'Campeonato_y': 'Campeonato_Away',
    'Partidas_y': 'Partidas_Away'}, inplace=True)  

#df_jogodia.fillna(0, inplace=True)

# Converter colunas numéricas para float, tratando possíveis valores ausentes
df_jogodia['Avg_Home'] = pd.to_numeric(df_jogodia['Avg_Home'], errors='coerce')
df_jogodia['HT05Home'] = pd.to_numeric(df_jogodia['HT05Home'], errors='coerce')
df_jogodia['Avg_Away'] = pd.to_numeric(df_jogodia['Avg_Away'], errors='coerce')
df_jogodia['HT05Away'] = pd.to_numeric(df_jogodia['HT05Away'], errors='coerce')

# Fazer a query comparando o valor numérico
df_jogos_selecionados = df_jogodia.query('Avg_Home > 2.5 and HT05Home > 75 and Avg_Away > 2.5 and HT05Away > 70')

print(df_jogos_selecionados)

#df_jogos_selecionados.to_excel('Jogos_Selecionados.xlsx', index=False)