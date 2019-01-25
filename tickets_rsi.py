# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 22:26:50 2018

@author: ruialberto
"""

"""
Guarda em ficheiro de texto o nome das accoes(quotes), que estão
de acordo com o filtro utilizado (data de inicio e fim, e valores 
do RSI).
"""

from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
import pandas as pd
import datetime
import numpy as np
#import random
import warnings
warnings.filterwarnings("ignore")


yf.pdr_override()


inicio = datetime.datetime(2018,9,5)
fim = datetime.datetime(2019,1,25)


'''
inicio = datetime.datetime(2017,3,29)
fim = datetime.datetime.today()
'''

#ficheiro onde consta a lista das 500 S&P equities
#nome_ficheiro = 'lista_sp500.txt'
nome_ficheiro = 'euro_new.txt'
#nome_ficheiro = 'euro.txt'
#Abrir ficheiro para leitura
try:
        fhand = open(nome_ficheiro)

except:
        print ('Nao e possivel abrir o ficheiro: ', fhand)


lista = []

#Cria lista com os ticket do SP500
for f in fhand:
    linha = f.strip().split(',')
    ticker = linha[0]
    lista.append(ticker)


    
def RSI(series, period):
    delta = series.diff().dropna()
    u = delta * 0
    d = u.copy()
    u[delta > 0] = delta[delta > 0]
    d[delta < 0] = -delta[delta < 0]
    u[u.index[period-1]] = np.mean( u[:period] ) #first value is sum of avg gains
    u = u.drop(u.index[:(period-1)])
    d[d.index[period-1]] = np.mean( d[:period] ) #first value is sum of avg losses
    d = d.drop(d.index[:(period-1)])
    rs = pd.stats.moments.ewma(u, com=period-1, adjust=False) / \
    pd.stats.moments.ewma(d, com=period-1, adjust=False)
    return 100 - 100 / (1 + rs)




    
def obter_precos(ticket):
    try:
        df = pdr.get_data_yahoo(ticket,inicio, fim)
        preco_fecho = df['Close']
        #data = df['Date']
        #mm25 = df['Close'].rolling(window=25).mean()
        #mm50 = df['Close'].rolling(window=50).mean()
        rsi = RSI(preco_fecho, 14)
        return rsi.tolist()
    except:
        print('Nao foi possivel obter dados do ticket: ',ticket)
        return

   
def executa_calculos():
    for valor in lista:
        try:
            lista_rsi = obter_precos(valor)
            #if lista_rsi[-1] > 20 and lista_rsi[-1] < 35:
            if lista_rsi[-1] > 70:    
                with open('rsi_maior_rsi70_euro_240119.txt','a') as file:
                    file.write('{0} : RSI {1}\n'.format(valor,lista_rsi[-1]))
            else:
                print(valor)
        except:
            continue


        
executa_calculos()








            
            
    
    
