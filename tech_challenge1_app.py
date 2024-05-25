import pandas as pd
import streamlit as st

#1. Dados Comercialização

# Lendo arquivo csv
dados1 = pd.read_csv('ComercioVinho.csv', sep=';')

# Considerando somente dados de vinhos
dados1_1 = dados1
dados1_1 = dados1_1.iloc[0:10]

# Selecionando colunas usaveis
dados1_2 = dados1_1
dados1_2 = dados1_2[["Produto", "2023"]]

# Alterando nomes das colunas
dados1_2.columns = ["Produtos", "Qtde 2023 (L.)"]

# Formatando os valores
dados1_3 = dados1_2
def format_number(x):
    return f'{x:,}'.replace(',', '.') if isinstance(x, int) else x

# Aplicando a formatação na coluna '2023'
dados1_3['Qtde 2023 (L.)'] = dados1_3['Qtde 2023 (L.)'].apply(format_number)

# Aplicando o negrito nas linhas totais
dados1_4 = dados1_3
def highlight_rows(s, row_indices):
    return ['font-weight: bold' if i in row_indices else '' for i in range(len(s))]

dados1_4 = dados1_4.style.apply(highlight_rows, row_indices=[0, 4, 8, 9], axis=0)

st.markdown('# Olá, este é o meu Tech Challenge')
st.dataframe(dados1_4)


