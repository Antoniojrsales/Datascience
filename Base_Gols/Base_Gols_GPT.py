# Importando as bibliotecas
import pandas as pd
import gspread

# Autorização para acesso ao Google Sheets
gc = gspread.service_account(filename='GBQjson.json')

# Abrir a planilha
spreadsheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/154gX579nPaM0WhcBtNUES2EMRDQqP2jDbdvSpJ_Fstc/edit?gid=1457355959')

# Carregar e configurar os dados de cada aba
def carregar_aba(nome_aba):
    worksheet = spreadsheet.worksheet(nome_aba)
    data = worksheet.get_all_values()
    colunas = data.pop(0)
    return pd.DataFrame(data, columns=colunas)

# Carregar cada aba como DataFrame
df_aba1 = carregar_aba('Day')
df_aba2 = carregar_aba('BD_GolsGeral')
df_aba3 = carregar_aba('BD_Gols05HTHome')
df_aba4 = carregar_aba('BD_Gols05HTAway')

# Limpar e padronizar os campos 'Campeonato' e 'Time' para junções
def padronizar_campos(df, colunas):
    for coluna in colunas:
        df[coluna] = df[coluna].str.strip().str.lower()
    return df

df_aba1 = padronizar_campos(df_aba1, ['Time', 'Time_Away'])
df_aba2 = padronizar_campos(df_aba2, ['Campeonato', 'Time'])
df_aba3 = padronizar_campos(df_aba3, ['Campeonato', 'Time'])
df_aba4 = padronizar_campos(df_aba4, ['Campeonato', 'Time'])

# Selecionar colunas necessárias e fazer junções
df_selecionada_aba2 = df_aba2[['Campeonato', 'Time', 'Partidas', 'Avg', 'FT15', 'FT25']]
df_selecionada_aba3 = df_aba3[['Campeonato', 'Time', 'HT05HOME']]
df_selecionada_aba4 = df_aba4[['Campeonato', 'Time', 'HT05AWAY']]

df_basegols = df_selecionada_aba2.merge(df_selecionada_aba3, on=['Campeonato', 'Time'], how='left').merge(df_selecionada_aba4, on=['Campeonato', 'Time'], how='left')

# Ajustar colunas para manipular time Away
df_basegols_Away = df_basegols.rename(columns={
    'FT15': 'FT15Away', 'FT25': 'FT25Away', 'Avg': 'Avg_Away', 
    'Time': 'Time_Away', 'HT05HOME': 'HT05Home', 'HT05AWAY': 'HT05Away'
}).drop(columns=['HT05Home'])

# Realizar junções para criar o DataFrame final
df_time_Home = pd.merge(df_aba1, df_basegols, on='Time', how='left')
df_jogodia = pd.merge(df_time_Home, df_basegols_Away, on='Time_Away', how='left')

# Reordenar e renomear colunas para o DataFrame final
df_jogodia.rename(columns={
    'HT05AWAY_y': 'HT05Away', 'HT05HOME': 'HT05Home',
    'FT25': 'FT25Home', 'FT15': 'FT15Home', 'Avg': 'Avg_Home',
    'Time': 'Time_Home', 'Campeonato_x': 'Campeonato_Home',
    'Partidas_x': 'Partidas_Home', 'Campeonato_y': 'Campeonato_Away',
    'Partidas_y': 'Partidas_Away'}, inplace=True)

ordem = ['Campeonato_Home', 'Time_Home', 'X', 'Time_Away', 'Campeonato_Away', 'Partidas_Home', 'Avg_Home', 
         'HT05Home', 'FT15Home', 'FT25Home',  'Partidas_Away', 'Avg_Away', 'HT05Away', 'FT15Away', 'FT25Away']
df_jogodia = df_jogodia[ordem]

# Converter colunas numéricas para float, tratando possíveis valores ausentes
df_jogodia['Avg_Home'] = pd.to_numeric(df_jogodia['Avg_Home'], errors='coerce')
df_jogodia['HT05Home'] = pd.to_numeric(df_jogodia['HT05Home'], errors='coerce')
df_jogodia['Avg_Away'] = pd.to_numeric(df_jogodia['Avg_Away'], errors='coerce')
df_jogodia['HT05Away'] = pd.to_numeric(df_jogodia['HT05Away'], errors='coerce')

# Filtrar jogos selecionados
df_jogos_selecionados = df_jogodia.query('Avg_Home > 2.5 and HT05Home > 75 and Avg_Away > 2.5 and HT05Away > 70')

# Exportar para Excel, se necessário
# df_jogos_selecionados.to_excel('Jogos_Selecionados.xlsx', index=False)

print(df_jogos_selecionados)
