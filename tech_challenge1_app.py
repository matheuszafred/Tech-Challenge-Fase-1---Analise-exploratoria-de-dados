import pandas as pd
import streamlit as st
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

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

#Streamlit - Dados 1

st.markdown('## Tech Challenge Fase 1 - Análise exploratória')

st.markdown('#### 1. Dados Vinícola')

st.markdown('##### 1.1 - Comercialização de vinhos')

texto = """
         
Dando uma introdução ao nosso primeiro tópico, trouxemos aqui uma comparação das vendas (litros) totais dos principais produtos e categorias de 2023:

- **Vinho de Mesa**: Total de 187,016,848 litros
- **Vinho Fino de Mesa**: Total de 18,589,310 litros
- **Vinho Frizante**: Total de 2,843,600 litros
- **Vinho Orgânico**: Total de 9,123 litros

É evidente que o vinho de mesa é o líder em termos de volume de vendas, com mais de 187 milhões de litros vendidos. O vinho fino de mesa vem em segundo lugar, com cerca de 18,6 milhões de litros. O vinho frisante e orgânico têm volumes significativamente menores em comparação.

         """

st.write(texto)

st.table(dados1_4)

#2. Dados de exportação

# Lendo o arquivo csv
dados2 = pd.read_csv('ExpVinho.csv', sep=';')

# Selecionarndo os ultimos 15 anos
dados2_1 = dados2[["País", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023" ]]

# Alterando nome da coluna 'País'
dados2_2 = dados2_1.rename(columns={'País':'País de destino'})

# Acrescentando a coluna 'pais de origem'(Brasil)
dados2_3 = dados2_2
dados2_3['País de origem'] = 'Brasil'

#Ordenando as colunas
dados2_4 = dados2_3[['País de origem', 'País de destino', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023']]

#Somando as quantidades
dados2_5 = dados2_4
dados2_5["Total"] = dados2_5['2009'] + dados2_5['2010'] + dados2_5['2011'] + dados2_5['2012'] + dados2_5['2013'] + dados2_5['2014'] + dados2_5['2015'] + dados2_5['2016'] +  dados2_5['2017'] + dados2_5['2018'] + dados2_5['2019'] + dados2_5['2020'] + dados2_5['2021'] + dados2_5['2022'] + dados2_5['2023']

#Selecionar do maior para menor
dados2_6 = dados2_5.sort_values(by='Total', ascending=False)

#Somando os ultimos 5 anos
dados2_7 = dados2_6
dados2_7["Total 5 anos"] = dados2_7['2019'] + dados2_7['2020'] + dados2_7['2021'] + dados2_7['2022'] + dados2_7['2023']

#Selecionar do maior para menor
dados2_8 = dados2_7.sort_values(by='Total 5 anos', ascending=False)

# Selecionando as colunas
dados2_9 = dados2_8[["País de destino", "2019", "2020", "2021", "2022", "2023", "Total 5 anos" ]]

#Ajustando o indice
dados2_10 = dados2_9.set_index("País de destino")


#Streamlit - Dados 2

st.markdown('##### 1.2 - Exportação de vinhos')

texto = """ 

Segundo os dados de exportação e considerando as tendências e variações ao longo dos ultimos 5 anos, esses são alguns países que destacamos para nossa análise:

- **Paraguai** é o maior importador com um crescimento impressionante e consistente ao longo dos anos.
- **Haiti, Uruguai e EUA** apresentam crescimentos notáveis, embora com algumas variações.
- **China, Rússia e Nigéria** têm variações mais erráticas, indicando mercados menos estáveis.
- **Curaçao e Japão** mostram crescimento mais lento e constante.
- **Venezuela** apresenta um crescimento recente significativo, apesar de valores iniciais baixos.


"""

st.write(texto)

st.dataframe(dados2_10.head(10))

st.write("Tabela de vendas (litros) - Ultimos 15 anos")

st.dataframe(dados2_6.head(10))


#3. Dados climáticos
dados3 = pd.read_excel('tabela_clima_cons_RS_2023.xlsx')

# Substituir dados faltantes (NaN) por 0
dados3.fillna(0)

#inserir nova coluna 'Mes'
dados3_1 = dados3

meses_ptbr = {'January':'01-Janeiro',
              'February':'02-Fevereiro',
              'March':'03-Março',
              'April':'04-Abril',
              'May':'05-Maio',
              'June':'06-Junho',
              'July':'07-Julho',
              'August':'08-Agosto',
              'September':'09-Setembro',
              'October':'10-Outubro',
              'November':'11-Novembro',
              'December':'12-Dezembro'}

dados3_1['Mes'] = dados3_1['Data'].dt.month_name().replace(meses_ptbr)

#Considerar somente colunas usaveis
dados3_2 = dados3_1[["Estações-RS", "Data", "Temp. [Hora] (C)", "Umi. (%)","Chuva [Diaria] (mm)", "Mes"]]

dados3_3 = dados3_2.groupby('Mes')['Temp. [Hora] (C)'].mean().reset_index()

# Criando o gráfico
plt.figure(figsize=(16, 5))
plt.plot(dados3_3['Mes'], dados3_3['Temp. [Hora] (C)'], marker='o')

# Adicionando títulos e rótulos
plt.title('Temperatura Média por Mês')
plt.xlabel('Mês')
plt.grid(axis='y', color='lightgrey')
plt.ylabel('Temperatura (°C)')
plt.xticks(rotation=45)
plt.show()

#Streamlit - Dados 3

st.markdown('#### 2. Dados externos')

st.markdown('##### 2.1 - Dados climáticos')

texto = """

Segundo os dados do INMET 2023 das principais estações do Rio Grande do Sul, dividimos essa análise em duas partes onde destacamos o melhor periodo para produção e o periodo com maior desafio.

**Período de Melhor Produção**

- **Verão (Dezembro a Fevereiro):** As altas temperaturas (23.57°C a 25.19°C) são ideais para a maturação das uvas, promovendo bom acúmulo de açúcares e desenvolvimento de sabores ricos.
- **Outono (Março a Maio):** As temperaturas moderadas no outono (17.09°C a 24.09°C) são ideais para a colheita, preservando aromas e acidez das uvas.

**Período de Maior Desafio**

- **Inverno (Junho a Agosto):** Embora necessário para a dormência das videiras, as temperaturas mais baixas (14.30°C a 15.77°C) apresentam risco de geadas tardias, especialmente no início da primavera.
- **Primavera (Setembro a Novembro):** O risco de geadas tardias pode prejudicar o desenvolvimento inicial dos brotos e flores, tornando este período crítico para o manejo adequado das videiras.


"""

st.write(texto)

st.pyplot(plt)

#Dados demograficos e economicos
#4. Faixa etaria

dados4 = pd.read_csv('tabela_censo2022_idade_brasilv2.csv', sep=";", thousands=".")

#Criando um dicionario
grupos_idade = ["0 a 9 anos", "10 a 19 anos", "20 a 29 anos", "30 a 39 anos",
                "40 a 49 anos", "50 a 59 anos", "60 a 69 anos", "70 a 79 anos",
                "80 a 89 anos", "90 a 99 anos", "100 anos ou mais"]
populacao_feminina = [12981329, 13740642, 15541422, 16281290, 15382114,
                      12733791, 9626735, 5432779, 2300732, 500247, 27244]
populacao_masculina = [13472971, 14310261, 15394764, 15364618, 14330168,
                       11433896, 8193886, 4273136, 1503501, 244660, 10570]

# Criando do gráfico
fig, ax = plt.subplots(figsize=(12, 8))

# Criação das barras horizontais
y = np.arange(len(grupos_idade))  # Posições das barras no eixo Y
barra1 = ax.barh(y - 0.2, populacao_feminina, height=0.4, label='População feminina(pessoas)', color='pink')
barra2 = ax.barh(y + 0.2, populacao_masculina, height=0.4, label='População masculina(pessoas)', color='lightblue')

# Configurações do eixo Y
ax.set_yticks(y)
ax.set_yticklabels(grupos_idade)
ax.invert_yaxis()  # Inverte a ordem dos grupos de idade para o gráfico ficar mais intuitivo

# Aplicando a formatação ao eixo X
ax.xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))

# Adicionando os valores dentro das barras
for bar in barra1:
    width = bar.get_width()
    ax.text(width - 0.1 * width, bar.get_y() + bar.get_height() / 2,
            f'{width/1e2:,.2f}', ha='right', va='center', color='black', fontsize=10)

for bar in barra2:
    width = bar.get_width()
    ax.text(width - 0.1 * width, bar.get_y() + bar.get_height() / 2,
            f'{width/1e2:,.2f}', ha='right', va='center', color='black', fontsize=10)


# Configurações dos rótulos e título
ax.set_xlabel('População (pessoas)')
ax.set_title('População por Grupo de Idade e Gênero')
ax.legend()

# Exibição do gráfico
plt.tight_layout()
plt.show()

#Streamlit - Dados 4

st.markdown('##### 2.2 - Dados demográficos')

texto = """

**Faixa etária**

- Adultos Jovens (20 a 39 anos): Este grupo representa uma parcela significativa da população e inclui muitos consumidores em fase de ascensão profissional e financeira, que podem ter maior disposição e renda para consumir vinhos.

"""
st.write(texto)

st.pyplot(plt)

#5. Variação anual do PIB

dados5 = pd.read_excel('tabela_pibv2.xlsx')

#filtrando apenas a linha PIB
dados5_1 = dados5[dados5.index == 16]

#alterando o indice
dados5_2 = dados5_1
dados5_2 = dados5_2.set_index("Setores e subsetores")

# Plotando o grafico
dados5_3 = dados5_2
ax = dados5_3.T.plot(kind='bar', figsize= (16,5))
plt.xlabel('Trimestre')
plt.xticks(rotation=45)
plt.grid(axis='y', color='lightgrey')
plt.ylabel('Variação PIB')
plt.title('Gráfico PIB - Variação anual')

# Adicionando os valores nas barras
for p in ax.patches:
    ax.annotate(str(round(p.get_height(), 2)),
                (p.get_x() * 1.005, p.get_height() * 1.01))
    
#Streamlit - Dados 5

texto = """

**Variação do PIB anual**

- O PIB apresenta variações significativas e flutuações moderadas ao longo do período analisado. Enquanto alguns trimestres registram crescimento expressivo (2º trimestre de 2021), outros mostram taxas mais moderadas. Apesar disso, o PIB demonstra certa estabilidade ao longo do período, sem oscilações extremas que indiquem instabilidade econômica grave.

"""

st.write(texto)

st.pyplot(plt)

texto = """

De acordo com a análise dos dados demográficos e do PIB, sugerimos que:

- A indústria do vinho pode focar suas estratégias de marketing em grupos de 20 a 49 anos, aproveitando o crescimento econômico para promover vinhos de qualidade e experiências associadas ao consumo desse produto.

"""

st.write(texto)

#6. Dados PMC - Comercio de Bebidas

dados6 = pd.read_excel('tabela_pmc_8190_receita_comercio_2023v2.xlsx', skiprows=3, skipfooter=1)

#excluir a linha 0
dados6_1 = dados6.drop(0, axis=0)

#alterar nome da coluna 1
dados6_2 = dados6_1
dados6_2.rename(columns={'Unnamed: 0': 'UF'},
                inplace=True)

meses_dados6 = ['janeiro 2022', 'fevereiro 2022', 'março 2022',
       'abril 2022', 'maio 2022', 'junho 2022', 'julho 2022', 'agosto 2022',
       'setembro 2022', 'outubro 2022', 'novembro 2022', 'dezembro 2022', 'janeiro 2023', 'fevereiro 2023', 'março 2023',
       'abril 2023', 'maio 2023', 'junho 2023', 'julho 2023', 'agosto 2023',
       'setembro 2023', 'outubro 2023', 'novembro 2023', 'dezembro 2023']

dados6_2[meses_dados6] = dados6_2[meses_dados6].astype(int)

#Agregando novas colunas (trimestre)
dados6_3 = dados6_2
dados6_3['1º tri 2022'] = (dados6_3['janeiro 2022'] + dados6_3['fevereiro 2022'] + dados6_3['março 2022']) / 3
dados6_3['2º tri 2022'] = (dados6_3['abril 2022'] + dados6_3['maio 2022'] + dados6_3['junho 2022']) / 3
dados6_3['3º tri 2022'] = (dados6_3['julho 2022'] + dados6_3['agosto 2022'] + dados6_3['setembro 2022']) / 3
dados6_3['4º tri 2022'] = (dados6_3['outubro 2022'] + dados6_3['novembro 2022'] + dados6_3['dezembro 2022']) / 3
dados6_3['1º tri 2023'] = (dados6_3['janeiro 2023'] + dados6_3['fevereiro 2023'] + dados6_3['março 2023']) / 3
dados6_3['2º tri 2023'] = (dados6_3['abril 2023'] + dados6_3['maio 2023'] + dados6_3['junho 2023']) / 3
dados6_3['3º tri 2023'] = (dados6_3['julho 2023'] + dados6_3['agosto 2023'] + dados6_3['setembro 2023']) / 3
dados6_3['4º tri 2023'] = (dados6_3['outubro 2023'] + dados6_3['novembro 2023'] + dados6_3['dezembro 2023']) / 3

#somando todos os trimestres
dados6_4 = dados6_3
dados6_4["total"] = dados6_4['1º tri 2022'] + dados6_4['2º tri 2022'] + dados6_4['3º tri 2022'] + dados6_4['4º tri 2022'] + dados6_4['1º tri 2023'] + dados6_4['2º tri 2023'] + dados6_4['3º tri 2023'] + dados6_4['4º tri 2023']

#agrupando do maior para menor
dados6_5 = dados6_4
dados6_5 = dados6_5.sort_values(by='total', ascending=False)

#alteração indice para UF
dados6_5 = dados6_5.set_index("UF")

dados6_6 = dados6_5[['1º tri 2022', '2º tri 2022',
       '3º tri 2022', '4º tri 2022', '1º tri 2023', '2º tri 2023',
       '3º tri 2023', '4º tri 2023']]

dados6_6.head(5).T.plot(kind='line', figsize= (16,5))
plt.xlabel('Trimestre')
plt.ylabel('Numero-Indice')
plt.title('Gráfico Indice PMC - Trimestral 2022 a 2023')
plt.grid(axis='y', color='lightgrey')
plt.legend(title='UF')

#Streamlit - Dados 6

st.markdown('##### 2.3 - Dados econômicos')

texto = """

**Indice PMC**

Com base no indice PMC (Pesquisa Mensal de Comércio) dos ultimos 3 anos, podemos destacar as tendências de consumo da seguinte forma:

- **Crescimento Sazonal:** A maioria dos estados experimentou picos de consumo no final de 2022, provavelmente devido a fatores sazonais como festas de fim de ano.
- **Quedas e Recuperações:** Estados como Minas Gerais, São Paulo e Pernambuco mostraram padrões de quedas após os picos, seguidos por diferentes graus de recuperação.
- **Estabilidade Relativa:** Rio de Janeiro e Espírito Santo apresentaram um crescimento mais estável e menos volátil, indicando uma tendência de consumo mais consistente.

O comportamento de consumo de alimentos e bebidas variou significativamente entre os estados, com alguns apresentando picos sazonais e quedas subsequentes, enquanto outros mostraram uma tendência de crescimento mais estável.

"""

st.write(texto)

st.pyplot(plt)


#8. Dados Taxa Cambio - Ultimos 3 anos

dados8 = pd.read_excel('tabela_taxa_cambiov2.xlsx')

#inserir nova coluna 'Mes' e 'Ano'

meses_ptbr = {'January':'01-Janeiro',
              'February':'02-Fevereiro',
              'March':'03-Março',
              'April':'04-Abril',
              'May':'05-Maio',
              'June':'06-Junho',
              'July':'07-Julho',
              'August':'08-Agosto',
              'September':'09-Setembro',
              'October':'10-Outubro',
              'November':'11-Novembro',
              'December':'12-Dezembro'}

dados8['Mes'] = dados8['data'].dt.month_name().replace(meses_ptbr)
dados8['Ano'] = dados8['data'].dt.year
dados8.head()

dados8_1 = dados8.groupby(['Mes', 'Ano']).mean(['valor']).reset_index()

#Tabela pivô para reorganizar os dados:
pivot_dados8_1 = dados8_1.pivot(index='Mes', columns='Ano', values='valor')

# Plotando o gráfico
ax = pivot_dados8_1.plot(kind='line', figsize= (16,5))

# Ajustando a granularidade do eixo x
ax.set_xticks(range(0, 12))  # Define os ticks de 1 a 12
ax.set_xticklabels(['01-Janeiro', '02-Fevereiro', '03-Março', '04-Abril', '05-Maio', '06-Junho', '07-Julho', '08-Agosto', '09-Setembro', '10-Outubro', '11-Novembro', '12-Dezembro'])

plt.title('Valores por Mês para cada Ano')
plt.xlabel('Meses')
plt.ylabel('Valor US$')
ax.grid(axis='y', color='lightgrey')
plt.legend(title='Ano')

texto = """

**Taxa de Câmbio**

De acordo a Taxa de Câmbio e analisando a variação do dólar nos ultimos três anos, observamos algumas tendências significativas que podem impactar a exportação de produtos do agronegócio brasileiro.

**Competitividade dos Produtos Brasileiros:**

- **Dólar Alto:** Um dólar mais alto em 2021 aumentou a competitividade dos produtos brasileiros no mercado internacional, pois os produtos ficaram mais baratos para compradores estrangeiros.
- **Dólar em Queda:** A queda no valor do dólar em 2022 e 2023 pode reduzir essa competitividade. Produtos brasileiros se tornam mais caros para compradores internacionais, o que pode levar a uma redução na demanda externa.

**Receita de Exportação:** 

- Quando o dólar está mais alto, os exportadores brasileiros recebem mais reais por cada dólar ganho, aumentando a receita em moeda local. Com a queda do dólar, essa receita diminui.

**Custos de Produção:** 

- Muitos insumos agrícolas, como fertilizantes e defensivos agrícolas, são importados e pagos em dólares. A queda do dólar pode reduzir os custos de produção, melhorando a margem de lucro dos produtores.

**Tendencias e estratégias:**

- **Continuação da Queda do Dólar: S**e a tendência de queda do dólar continuar, os produtos do agronegócio brasileiro podem enfrentar maior competitividade global, exigindo estratégias diferenciadas para manter a participação no mercado internacional.
- **Estratégias de Hedge:** Produtores e exportadores podem adotar estratégias de hedge para se proteger contra a volatilidade cambial, garantindo um valor fixo do dólar para suas transações futuras.


"""

st.write(texto)

st.pyplot(plt)

#9. Dados Avaliação de vinhos por Região

dados9 = pd.read_excel('tabela_avaliação_vinalies2023.xlsx')

# Exclluindo região sem dado
dados9 = dados9[dados9['Region'] != '--']

# Contando as medalhas por região e tipo
medal_count9 = dados9.pivot_table(index='Region', columns='Medal', aggfunc='size', fill_value=0)

colors = {
    'Grande Ouro': '#FFD700',  # Dourado
    'Ouro': '#FFFF00',        # Amarelo
    'Prata': '#C0C0C0'     # Cinza
}

# Plotando o gráfico de barras empilhadas horizontal
ax = medal_count9.plot(kind='barh', stacked=True, figsize=(14, 5), color=[colors[col] for col in medal_count9.columns])

# Adicionando título e rótulos
plt.title('Premiações por Região')
plt.xlabel('Número de Medalhas')
plt.ylabel('')
plt.legend(title='Tipo de Medalha', bbox_to_anchor=(0.8, 1), loc='upper left')

# Adicionando os valores dentro das barras, omitindo zeros
for container in ax.containers:
    labels = [int(v) if v > 0 else '' for v in container.datavalues]
    ax.bar_label(container, labels=labels, label_type='center')

# Ajustando layout para evitar corte de elementos
plt.tight_layout()

st.markdown('##### 2.4 - Avaliação de vinhos brasileiros')

texto = """

**Avaliação por região (Rio Grande do Sul)**

Para trazer os dados de avaliações de vinho, consideramos levantar informações sobre a ultima premiação feita pela Vinalies Internacionales (2023), onde eles avaliam vinhos do mundo todo e classificam com uma nota de Grande Ouro, Ouro e Prata. 

Analisando as medalhas de vinhos do Brasil, podemos listar 2 regiões que se destacam:

- **Campos de Cima da Serra:** Esta região tem uma predominância de medalhas, principalmente ouro e grande ouro, com várias premiações para vinhos brancos. No geral, esta região lidera em termos de reconhecimento de qualidade.
- **Serra Gaúcha:**  Esta região também demonstra uma forte presença no cenário vinícola brasileiro, com várias medalhas conquistadas, especialmente em vinhos espumantes. A região é reconhecida pela sua qualidade e variedade, destacando-se na produção de espumantes premiados. As medalhas de ouro e prata atribuídas aos espumantes e outros vinhos da região são testemunho do seu potencial de atrair consumidores tanto no mercado nacional quanto internacional.

"""

st.write(texto)

st.pyplot(plt)

#10. Avaliação de vinhos por Cor

dados10 = pd.read_excel('tabela_avaliação_vinalies2023.xlsx')

# Contar as medalhas por cor e tipo
medal_count10 = dados10.pivot_table(index='Color', columns='Medal', aggfunc='size', fill_value=0)

# Definir as cores para cada tipo de medalha
colors = {
    'Grande Ouro': '#FFD700',  # Dourado
    'Ouro': '#FFFF00',        # Amarelo
    'Prata': '#C0C0C0'     # Cinza
}

# Ordenar as cores do DataFrame
medal_count10 = medal_count10[['Grande Ouro', 'Ouro', 'Prata']]

# Definir a posição das barras
ind = np.arange(len(medal_count10))  # Posições para as cores
width = 0.2  # Largura das barras

# Criar o gráfico de barras agrupadas
fig, ax = plt.subplots(figsize=(10, 5))

# Adicionar as barras agrupadas
bars = []
for i, medal in enumerate(medal_count10.columns):
    bars.append(ax.bar(ind + i * width, medal_count10[medal], width, label=medal, color=colors[medal]))

# Adicionar título e rótulos
ax.set_title('Número de Medalhas por Cor do Vinho')
ax.set_xlabel('')
ax.set_ylabel('Número de Medalhas')
ax.set_xticks(ind + width)
ax.set_xticklabels(medal_count10.index)
ax.legend(title='Tipo de Medalha')

# Adicionar os valores dentro das barras
for bar in bars:
    ax.bar_label(bar, labels=[f'{v}' if v > 0 else '' for v in bar.datavalues], label_type='center')

# Ajustar layout para evitar corte de elementos
plt.tight_layout()

texto = """

**Avaliação de vinho por Cor**

Olhando para a distribuição das medalhas por cor de vinho na tabela, podemos observar que a maioria das medalhas de ouro e grande ouro foi concedida a vinhos brancos, com uma representação significativa de espumantes. Isso pode sugerir uma tendência de mercado onde os consumidores estão valorizando mais os vinhos brancos e espumantes, possivelmente devido à sua versatilidade, frescor e capacidade de harmonização com uma variedade de pratos.

Essa tendência pode ser impulsionada pelo aumento da preferência por estilos de vida mais leves e saudáveis, nos quais vinhos brancos e espumantes muitas vezes se encaixam melhor.

"""

st.write(texto)

st.pyplot(plt)

st.markdown('##### 3. Estretégias Recomendadas')

texto = """

- **Focar em mercados estáveis e em crescimento** como Paraguai e Haiti, além de explorar o potencial em EUA e Uruguai.
- **Promover vinhos premiados** da região da Serra Gaúcha, destacando a qualidade e os prêmios conquistados para atrair consumidores premium.
- **Adotar tecnologias de manejo e proteção** contra riscos climáticos, como geadas, para garantir a consistência da produção.
- **Implementar estratégias de hedge** para proteger-se contra a volatilidade cambial e manter a competitividade dos produtos brasileiros no exterior.
- **Desenvolver campanhas de marketing sazonais** para estados com consumo volátil e focar em um público jovem com poder de compra crescente.

Essas ações poderão fortalecer a posição da vinícola no mercado, aumentar a competitividade e mitigar os desafios, promovendo um crescimento sustentável e robusto.

"""

st.write(texto)






