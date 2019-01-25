# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 12:15:32 2018

@author: ruialberto
"""

"""
Escolhe aleatoriamente uma accão (através da lista de quotes),
e verifica se as condicões de filtragem (ex: valor do RSI), estão validadas.
Se sim, simula uma operação de compra e venda. Apresentando os valores finais.
"""

from pandas_datareader import data as pdr
#from stockstats import StockDataFrame as Sdf
import fix_yahoo_finance as yf
import pandas as pd
import datetime
import random
import pylab as plt
import numpy as np
import warnings
warnings.filterwarnings("ignore")


yf.pdr_override()


inicio = datetime.datetime(2018,8,31)
fim = datetime.datetime(2019,1,20)


'''
inicio = datetime.datetime(2017,3,29)
fim = datetime.datetime.today()
'''

#ficheiro onde consta a lista das 500 S&P equities
#nome_ficheiro = 'lista_sp500.txt'
nome_ficheiro = 'euro_new.txt'
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


    
def calcula_stop_loss(preco_actual, preco_inicial):
    """
    Calcula o valor de um stop loss
    Sempre que o preco actual for superior em 3% ao preco anterior
    é colocado um stop-loss
    """

    tmp_stop_loss = float((preco_actual*3.3)/100)
    stop_loss = float(preco_actual - tmp_stop_loss)
    return stop_loss



def calcula_stop_win(preco_actual, preco_inicial):
    """
    Calcula o valor de um stop loss
    Sempre que o preco actual for superior em 3% ao preco anterior
    é colocado um stop-loss
    """

    tmp_stop_win = float((preco_actual*80.0)/100)
    stop_win = float(preco_actual + tmp_stop_win)
    return stop_win



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
        mm25 = df['Close'].rolling(window=25).mean()
        mm50 = df['Close'].rolling(window=50).mean()
        rsi = RSI(preco_fecho, 14)
        return preco_fecho.tolist(), mm25.tolist(), mm50.tolist(), rsi.tolist()
    except:
        print('Nao foi possivel obter dados do ticket: ',ticket)
        return

         
conta_final = 0 
   
def calculaOpcaoCompra(valor_escolhido,conta_inicial,soma_dias):
    """
    Caso o preço da accao seja > que mm25 e
    a mm25 seja > mm50 compra accão
    Valor inicial = 25000 €
    Gasta a totalidade do valor inicial
    """
    
    #conta_final = 0
    contador = 0
    tenho_accoes = False
    valor_da_compra = 0
    valor_da_venda = 0
    valor_da_conta =0.1
    total_de_accoes = 0
    preco_compra = 0
    preco_medio = 0
    stop_loss_valor = 0
    stop_win_valor = 100000
    percentagem = 0.0
    n_compra = 0
    lista_de_precos = []
    valores_restantes = []
    preco_compra_primeiro =0.0
    #Cria automaticamente uma lista de preços aleatoria
    lista_de_precos,mm25,mm50, lista_rsi =obter_precos(valor_escolhido)
    #print('LISTA DE PREÇOS: ', lista_de_precos)
    ##print('Lista de preços: \n')
    ##print(lista_de_precos)    
    
    #preço do dia anterior
    valores_restantes_total = lista_de_precos[soma_dias:]
    mm25_restantes = mm25[soma_dias:]
    mm50_restantes = mm50[soma_dias:]
    rsi_restantes = lista_rsi[soma_dias:]
    
    valores_restantes_total = valores_restantes_total[14:]
    #valores_restantes = [valores for valores in valores_restantes_total if valores > mm25 and mm25 > mm50]    
    
    i=0
    dias = 0
    while(i < len(valores_restantes_total)):
        #print('CONTA INICIAL =', conta_inicial)
        x = valores_restantes_total[i]
        media_25 = mm25_restantes[i]
        media_50 = mm50_restantes[i]
        rsi_actual = rsi_restantes[i]
        rsi_anterior = rsi_restantes[i-1]
        #dia_da_operacao = datas[i]
        #print(i,'º Preco = ',x, '(', valor_escolhido, ')')
        #print ('VALORES de X = ',x)        
        if tenho_accoes == True and (x <= stop_loss_valor):
        #if tenho_accoes == True and ( x <= stop_loss_valor or x > stop_win_valor ):    
                print ('--- VENDA (atingiu Stop loss) --------',contador)
                tenho_accoes = False
                #valor_da_venda = stop_loss_valor * total_de_accoes
                valor_da_venda = x * total_de_accoes                   
                conta_final = valor_da_venda - valor_da_compra
                print('Resultado Final = ', round(conta_final,2))
                #print('Data da Venda = ', dia_da_operacao)
                #print('Accao preço compra = ',round(preco_compra,2))
                print('Accao preço venda  = ',round(x,2))
                print('Valor MM25= ',round(media_25,2), ' -- MM50= ',round(media_50,2))
                print('Valor do RSI = ', rsi_actual)
                #print('Valor do Stop Loss = ',round(stop_loss_valor,2))
                #percentagem = 100*(stop_loss_valor-preco_medio)/preco_medio
                percentagem = (100 * conta_final) / valor_da_compra
                print('\nPercentagem: ',round(percentagem,2), '%')
                #return
                #print ('----------------------------------------------')
                break
            
        if tenho_accoes == True and (x > stop_win_valor):
        #if tenho_accoes == True and ( x <= stop_loss_valor or x > stop_win_valor ):    
                print ('--- VENDA (atingiu Stop win valor) --------',contador)
                tenho_accoes = False
                valor_da_venda = stop_win_valor * total_de_accoes
                #valor_da_venda = x * total_de_accoes                   
                conta_final = valor_da_venda - valor_da_compra
                print('Resultado Final = ', round(conta_final,2))
                #print('Data da Venda = ', dia_da_operacao)
                #print('Accao preço compra = ',round(preco_compra,2))
                print('Accao preço venda  = ',round(x,2))
                print('Valor MM25= ',round(media_25,2), ' -- MM50= ',round(media_50,2))
                print('Valor do RSI = ', rsi_actual)
                #print('Valor do Stop Loss = ',round(stop_loss_valor,2))
                #percentagem = 100*(stop_loss_valor-preco_medio)/preco_medio
                percentagem = (100 * conta_final) / valor_da_compra
                print('\nPercentagem: ',round(percentagem,2), '%')
                #return
                #print ('----------------------------------------------')
                break
            
        #if rsi_actual>20 and rsi_actual<35 and rsi_anterior < rsi_actual and media_25 > media_50:
        #if rsi_actual>20 and rsi_actual<35 and rsi_anterior < rsi_actual:    
        #tenho_accoes = True
        if rsi_actual>70:
            preco_compra = x
            
            if n_compra == 0 and valor_da_conta != 0 and preco_compra > 5.0:
                tenho_accoes = True
                
                preco_compra_primeiro = preco_compra
                valor_da_conta = conta_inicial // 1
                total_de_accoes = valor_da_conta//x
                valor_da_conta = conta_inicial - valor_da_conta
                valor_da_compra = float(preco_compra_primeiro * total_de_accoes)
                stop_loss_valor = calcula_stop_loss(float(x), float(preco_compra_primeiro))
                stop_win_valor = calcula_stop_win(float(x), float(preco_compra_primeiro))
                n_compra = 1
                print('\n----------- COMPRA N.1 ----------------',contador, 'Nome: ',valor_escolhido)
                #print('Data da Compra = ', dia_da_operacao)
                print('Valor por accao= ',round(preco_compra_primeiro,2))
                print('Valor MM25= ',round(media_25,2), ' -- MM50= ',round(media_50,2))
                print('Valores do RSI = ', rsi_anterior, rsi_actual)
                print('Total da compra = ',round(valor_da_compra,2))
                print('Total de accoes = ', total_de_accoes)
                print ('Valor do STOP LOSS = ',round(stop_loss_valor,2))
                print ('Valor do STOP WIN = ',round(stop_win_valor,2))
            """    
            elif n_compra == 1 and valor_da_conta != 0 and preco_compra > (((preco_compra_primeiro*5.1)//100) + preco_compra_primeiro) :
                tenho_accoes = True
                preco_compra_segundo = preco_compra
                valor_da_conta1 = valor_da_conta // 2
                valor_da_conta = valor_da_conta - valor_da_conta1
                total_de_accoes2 = valor_da_conta1//x
                total_de_accoes = total_de_accoes + total_de_accoes2
                valor_da_compra2 = float(preco_compra_segundo * total_de_accoes2)
                valor_da_compra = valor_da_compra + valor_da_compra2
                preco_medio = valor_da_compra / total_de_accoes
                stop_loss_valor = calcula_stop_loss(float(preco_medio), float(preco_compra_segundo))
                n_compra = 2
                print('\n----------- COMPRA N.2 ----------------',contador, 'Nome: ',valor_escolhido)
                #print('Data da Compra = ', dia_da_operacao)
                print('Valor por accao= ',round(preco_compra_segundo,2))
                print('Valor MM25= ',round(media_25,2), ' -- MM50= ',round(media_50,2))
                print('Valor do RSI = ', rsi_actual)
                print('Preco medio por accao= ',round(preco_medio,2))
                print('Total da compra = ',round(valor_da_compra,2))
                print('Total de accoes 2 = ', total_de_accoes2)
                print('Total de accoes = ', total_de_accoes)
                print ('Valor do STOP LOSS = ',round(stop_loss_valor,2))
            elif n_compra == 2 and valor_da_conta != 0 and preco_compra > (((preco_compra_segundo*5.1)//100) + preco_compra_segundo ):
                tenho_accoes = True
                preco_compra_terceiro = preco_compra
                valor_da_conta2 = valor_da_conta
                valor_da_conta = 0
                total_de_accoes3 = valor_da_conta2 // x
                total_de_accoes = total_de_accoes + total_de_accoes3
                valor_da_compra3 = float(preco_compra_terceiro * total_de_accoes3)
                valor_da_compra = valor_da_compra + valor_da_compra3
                preco_medio = valor_da_compra / total_de_accoes
                stop_loss_valor = calcula_stop_loss(float(preco_medio), float(preco_compra_terceiro))
                n_compra = 3
                print('\n----------- COMPRA N.3 ----------------',contador, 'Nome: ',valor_escolhido)
                #print('Data da Compra = ', dia_da_operacao)
                print('Valor por accao= ',round(preco_compra_terceiro,2))
                print('Valor MM25= ',round(media_25,2), ' -- MM50= ',round(media_50,2))
                print('Valor do RSI = ', rsi_actual)
                print('Preco medio por accao= ',round(preco_medio,2))
                print('Total da compra = ',round(valor_da_compra,2))
                print('Total de accoes = ', total_de_accoes)
                print ('Valor do STOP LOSS = ',round(stop_loss_valor,2))
             """   
                           
                
                
        if tenho_accoes == True:
            print('Valor actual = ', round(x,2))
            #print('Valor do RSI = ', rsi_actual)
            #print('----------------------------------------------------')
            dias += 1
            stop_loss_valor_tmp = calcula_stop_loss(float(x), float(preco_compra))
                        
            if stop_loss_valor_tmp > stop_loss_valor:
                stop_loss_valor = stop_loss_valor_tmp
            else:
                stop_loss_valor = stop_loss_valor
                print ('Valor do STOP LOSS = ',round(stop_loss_valor,2))
                print ('----------------------------------------------')            
                    
        i += 1
        
    #Limpa a lista de preços    
    lista_de_precos.clear()
    valores_restantes.clear()
    print('\n Dias utilizados: ',dias)
    return (round(percentagem,2),round(conta_final,2),dias) 
    
    
# Simular a estratégia n vezes
# Criar gráfico com os resultados
totais_finais = []
totais_finais.append(30000)
   
def simulacao(num_times):
    lista_percentagens = []
    #totais_finais = []
    total_de_dias = []
    positivos,neutro,negativos = (0,0,0)
    #totais_finais.append(25000)
    soma_dias = 0
    for num in range(num_times):        
        valor_escolhido = random.choice(lista)
        try:
            #valor_per = calculaOpcaoCompra(valor_escolhido,totais_finais[-1])
            percentagem, conta_f, dias = calculaOpcaoCompra(valor_escolhido,sum(totais_finais),soma_dias)
            lista_percentagens.append(percentagem)
            print('TOTAL FINAL = ',conta_f)
            totais_finais.append(conta_f)
            total_de_dias.append(dias)
            soma_dias = sum(total_de_dias)
        except:
            continue
    
       
    #return num_plot
    plt.figure('MM25',figsize=(12, 10), dpi=80, facecolor='w', edgecolor='k')
    plt.clf()
    plt.axhline(y=0.0, color='r', linestyle='-')
    plt.xlabel('Simulações')
    plt.ylabel('Valor Lucro/Prejuizo %')
    plt.ylim(-20.0,50.0)
    plt.plot(lista_percentagens, 'bo')
    plt.title('Monte Carlo Simulation - BUY/SELL WITH STOP LOSS')
    print('\n---------------------------------------------------')         
    #print('\n Total final : ',round(sum(totais_finais),2))
    #print('\n Total de dias : ',round(sum(total_de_dias),2))
    print('\n Total final : ',round(sum(totais_finais)))
    print('\n Total de dias : ',round(sum(total_de_dias),2))
    
    
    
    '''
    plt.figure('Totais',figsize=(12, 10), dpi=80, facecolor='w', edgecolor='k')
    plt.clf()
    plt.axhline(y=0.0, color='r', linestyle='-')
    plt.axhline(y=(sum(totais_finais)//int(num_times)), color='g', linestyle='--')
    plt.xlabel('Simulações')
    plt.ylabel('Totais')
    plt.ylim()
    plt.plot(totais_finais)
    plt.title('Monte Carlo Simulation - Totais Finais')         
    
    
    
    
    plt.figure('hist',figsize=(12, 10), dpi=80, facecolor='w', edgecolor='k')
    plt.clf()
    plt.hist(totais_finais,bins=20)
    plt.axvline(np.percentile(totais_finais,5), color='r', linestyle='dashed', linewidth=2)
    plt.axvline(np.percentile(totais_finais,95), color='r', linestyle='dashed', linewidth=2)
    plt.axvline(np.mean(totais_finais), color='g', linestyle='dashed', linewidth=2)
    plt.title('Histograma - Totais finais  -') 
    #Probabilidade
    '''
    for i in totais_finais:
        if i>0:
            positivos += 1
        elif i<0:
            negativos +=1
        else:
            neutro += 1
            
    estProbabilidade_pos = round(positivos/num_times,2)
    estProbabilidade_neg = round(negativos/num_times,2)
    estProbabilidade_neu = round(neutro/num_times,2)
    
    print('\n Probabilidade de ter lucro = ',estProbabilidade_pos)
    print('\n Probabilidade de ter prejuizo = ',estProbabilidade_neg)
    print('\n Probabilidade de não fazer negócio = ',estProbabilidade_neu)
    print('\n Media da distribuição (valor de retorno esperado) = ', round(np.mean(totais_finais),2), '€')
    print("\n 5% quantile =",np.percentile(totais_finais,5))
    print("\n 95% quantile =",np.percentile(totais_finais,95))          
    #return (round(sum(totais_finais),2))
    #return totais_finais

simulacao(50)
    
    