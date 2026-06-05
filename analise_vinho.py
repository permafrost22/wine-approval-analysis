import warnings
warnings.filterwarnings('ignore')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pd.options.display.max_rows = 999
pd.options.display.max_columns = 999

plt.style.use('ggplot')

dados_treino = pd.read_csv('Aula 7 - 2024/transf_wine_treino.csv',index_col=0).drop('index',axis=1)
dados_teste = pd.read_csv('Aula 7 - 2024/transf_wine_teste.csv',index_col=0).drop('index',axis=1)
print(dados_treino.groupby('type')['aprovado'].mean())

#passo 1 
#criando uma nova coluna denominada: 'chlorides'

coluna = 'chlorides'
minimo_vinhos = 50
dados_treino[coluna+'_faixa'] = pd.cut(dados_treino[coluna],bins=5)

print("passo 1!!")
print(dados_treino[[coluna+'_faixa']].head())
print("-"*50)

#passo 2 
#agrupando as colunas e tirando a média de vinhos aprovados por faixa de 'chlorides'

agrupamento2 = dados_treino.groupby(coluna+'_faixa')['aprovado'].agg(['count','mean'])
agrupamento2.columns = ['contagem','fração vinhos aprovados']
print("passo 2!!")
print(agrupamento2)
print("-"*50)

#passo3
#filtrando as faixas de 'chlorides' que são maior ou igual a 50 vinhos

agrupamento_filtro = agrupamento2[agrupamento2['contagem']>=minimo_vinhos]
print("passo 3!!")
print(agrupamento_filtro)
print("-"*50)

#passo 4
#agrupar de forma decrescente pela fração de vinhos aprovados

agrupamento_filtro.sort_values(by='fração vinhos aprovados',ascending=False)
print("passo 4!!")
print(agrupamento_filtro)
print("-"*50)

#passo 5
#agrupar pela fração de vinhos aprovados e pegar a faixa com maior média de vinhos aprovados

faixa_final = agrupamento_filtro.sort_values(by='fração vinhos aprovados',ascending=False).iloc[0] 

print("passo 5!!")
print(faixa_final)
print("-"*50)

#passo 6
#transformar a seleção em um dataframe pra simplificar o resultado

faixa_final = faixa_final.to_frame().T

print("passo 6!!")
print(faixa_final)
print("-"*50)

print("todos os passos foram executados com sucesso!!")
print("-"*50)


faixa_final = faixa_final.reset_index() # Para transformar a faixa em uma coluna separada, que chamararemos de 'melhor faixa'
faixa_final.columns = ['melhor faixa','contagem','fração vinhos aprovados']
faixa_final['coluna'] = coluna
faixa_final.set_index('coluna', inplace=True)
print(faixa_final)


def seleciona_faixa(dados, coluna, min_vinhos=100, faixas=10):
    # Função que parte dos dados e da coluna, selecionando a melhor faixa dentre as faixas escolhidas
    # Passo 1 - Selecionar a variável e fazer a coluna de faixas
    dados_treino[coluna+'_faixa'] = pd.cut(dados_treino[coluna],bins=faixas)
    # Passo 2 - Agrupar pela coluna de faixas e calcular média da coluna 'aprovado'
    agrupamento = dados_treino.groupby(coluna+'_faixa')['aprovado'].agg(['count','mean'])
    agrupamento.columns = ['contagem','fração vinhos aprovados']
    # Passo 3 - Selecionar apenas as faixas com um número mínimo de vinhos
    agrupamento_filtro = agrupamento[agrupamento['contagem']>=min_vinhos]
    # Passo 4 - Ordenar pela fração de vinhos aprovados, e selecionar a melhor faixa
    faixa_final = agrupamento_filtro.sort_values(by='fração vinhos aprovados',ascending=False).reset_index().iloc[0].to_frame().T
    # Ajustando nomes
    faixa_final.columns = ['faixa','contagem','fração vinhos aprovados']
    # Criando uma nova coluna com o nome da variável testada, e colocando-a como índice
    faixa_final['coluna'] = coluna
    faixa_final.set_index('coluna',inplace=True)
    # Salvando as seleções em um dataframe
    return faixa_final
    # Não vamos retornar nada nessa função

teste_faixas = seleciona_faixa(dados_treino,'chlorides')


print()
print(teste_faixas.head())
print("-"*50)
print("passo final!!!")

# Novamente selecionando as colunas numéricas
colunas_numericas = list(dados_treino.select_dtypes(include='float').columns)

# Rodando a função para todas as colunas (excluindo a 'chlorides', que já fizemos)
for col in colunas_numericas[1:]:
    teste_faixas = pd.concat([teste_faixas,seleciona_faixa(dados_treino,col)]) # Concatenar os Dataframes dentro da lista
teste_faixas

print(teste_faixas.sort_values(by='fração vinhos aprovados',ascending=False))

filtro_teste = dados_teste[dados_teste.alcohol.between(12.14,12.83)]

# Média de vinhos aprovados
print("Média de vinhos aprovados com este filtro:")
print(filtro_teste.aprovado.mean())
