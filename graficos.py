import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import missingno as msno

pd.options.display.max_rows = 999
pd.options.display.max_columns = 999

df = pd.read_csv('Aula 7 - 2024/transf_wine_treino.csv')

#g1
sns.set(font_scale = 1.3) 
coluna = 'fixed acidity'

sns.displot(
    df[coluna], 
    height=4, 
    aspect=2, 
    kind='kde' 
)
plt.show() 

#g2
sns.set(font_scale = 1.3) 
coluna = 'alcohol' 

sns.displot(
    df[coluna], 
    height=4, 
    aspect=2, 
    kind='kde',

)
plt.show()

#g3
df.plot(
    x='fixed acidity',
    y='density', 
    c='type', 
    kind='scatter'
)
plt.savefig('images/scatter_acidity_density.png', dpi=150, bbox_inches='tight')
plt.show()


#importante!

#g4
sns.set_context(font_scale=0.7)
sns.pairplot(df, # Dados para plotar
             hue='type', #Cada gráfico separado pelo tipo, nossa variável categórica
            vars=['residual sugar','chlorides','fixed acidity'] # Variáveis a serem analisadas
            )
plt.savefig('images/pairplot.png', dpi=150, bbox_inches='tight')
plt.show()

#matriz

#g5
df.drop('type', inplace = True, axis = 1) #tirar coluna type, poderia tornar boll tbm

sns.set_context(font_scale=1.9)
plt.figure(figsize=(12,8))
sns.heatmap(
    df.corr(), #Fonte dos dados, nossa matriz de correlação
    annot=True, #Anotar os valores das correlações nas caixinhas coloridas
    fmt='.2f', # Formato float de 2 dígitos, para arredondar os números
    cmap='RdBu', # Mapa de cores do vermelho (menor) para o azul (maior)
    mask=np.triu( # Faz uma matriz triangular
        np.ones_like(df.corr()) # usando como base uma matriz de '1's, do mesmo tamanho que a matriz de correlação
    ) # A máscara vai então 'apagar' a diagonal superior da matriz
           )
plt.savefig('images/heatmap_correlacao.png', dpi=150, bbox_inches='tight')
plt.show()

#g6

msno.matrix(df)
plt.show()