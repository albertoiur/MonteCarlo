# -*- coding: utf-8 -*-
"""
Created on Tue Sep  5 14:27:46 2017

MONTE CARLO SIMULATION

Estrategia utilizada:
    - Cria aleatoriamente 250 preços "função cria250precos()"
    - Caso o preço da accao seja > que média móvel de 25 dias(mm25) e a mm25 seja > mm50 compra accão
      Valor inicial = 25000 €
      Gasta a totalidade do valor inicial
      Calcula o stop-loss
      Caso o novo preço seja menor que o valor do stop-loss VENDE
      Senão:
       Calcula novo stop-Loss, e continua com a acção
    - Enquanto o preço for superior ao stop-loss não vende
    
Nota: A ideia é utilizar o stop loss para diminuir as perdas e deixar o lucro correr.
      É criado um gráfico com as várias percentagens de lucro/perdas    

@author: Rui
"""

import pylab as plt
import random
import numpy as np

lista = []


def cria250precos():
    """
    Cria uma lista aleatoria com 250 numeros reais (5.0 - 25.78)
    Cada valor criado simula o preço de fecho de uma acção
    """

    #Primeiro valor aleatorio
    x = random.uniform(5.0, 25.78)
    for f in range(250):
        #calcula limite maximo para novo preço +10%
        topo = float(x + ((x*10)/100))
        #valor -10% do preço de fecho
        fundo = float(x - ((x*10)/100))
        #Calcula novo preço
        x = random.uniform(fundo, topo)
        #adiciona na lista
        lista.append(x)
    return lista


def calculoMedia25(lista):
    """
    Calcula a media dos ultimos n dias
    """

    ultimos_25_dias = []
    # Seleciona os ultimos n numeros da lista global (lista)
    ultimos_25_dias.extend(lista[-25:])
    media25 = sum(ultimos_25_dias)/25

    return media25

def calculoMedia50(lista):
    """
    Calcula a media dos ultimos n dias
    """

    ultimos_50_dias = []
    # Seleciona os ultimos n numeros da lista global (lista)
    ultimos_50_dias.extend(lista[-50:])
    media50 = sum(ultimos_50_dias)/50

    return media50
    
def calcula_stop_loss(preco_actual, preco_inicial):
    """
    Calcula o valor de um stop loss
    Sempre que o preco actual for superior em 3% ao preco anterior
    é colocado um stop-loss
    """

    tmp_stop_loss = float((preco_actual*3.0)/100)
    stop_loss = float(preco_actual - tmp_stop_loss)
    return stop_loss
    
    
         
    
        
def calculaOpcaoCompra():
    """
    Caso o preço da accao seja > que mm25 e
    a mm25 seja > mm50 compra accão
    Valor inicial = 25000 €
    Gasta a totalidade do valor inicial
    """
    conta_inicial = 25000
    conta_final = 0
    contador = 0
    tenho_accoes = False
    valor_da_compra = 0
    valor_da_venda = 0
    total_de_accoes = 0
    preco_compra = 0
    stop_loss_valor = 0
    percentagem = 0.0
    lista_de_precos = []
    
    #Cria automaticamente uma lista de preços aleatoria
    lista_de_precos=cria250precos()
    ##print('Lista de preços: \n')
    ##print(lista_de_precos)
    
    while(contador <250):
        ##print('\nDia(s) : ',contador)
        #Calcula a media dos ultimos 25 dias
        mm25 = calculoMedia25(lista_de_precos)
        #Calcula a media dos últimos 50 dias
        mm50 = calculoMedia50(lista_de_precos)
        #preço do dia anterior
        ultimo_preco = lista_de_precos[-1]
        #valor +10% do preço de fecho
        top = float(ultimo_preco + ((ultimo_preco*10)/100))
        #valor -10% do preço de fecho
        fundo = float(ultimo_preco - ((ultimo_preco*10)/100))
        #simula o preço de hoje
        x = random.uniform(fundo,top)
        #adiciona o novo preço (preço de hoje) à lista global (lista)
        lista_de_precos.append(x)
        
        #Se tenho accoes em carteira calculo o stop loss
        ##print('-----------------------------------------------')
        ##print('Valor actual = ',round(x,2))
        ##print('Media Movel 25 = ',round(mm25,2))
        ##print('Media Movel 50 = ',round(mm50,2))
        
        if tenho_accoes == True and x <= stop_loss_valor:
            ##print ('--- VENDA (atingiu Stop loss) --------')
            valor_da_venda = stop_loss_valor * total_de_accoes
            conta_final = valor_da_venda - valor_da_compra
            ###print('Resultado Final = ', round(conta_final,2))
            #print('Accao preço compra = ',round(preco_compra,2))
            #print('Accao preço venda  = ',round(stop_loss_valor,2))
            #print('Valor do Stop Loss = ',round(stop_loss_valor,2))
            percentagem = (100*(stop_loss_valor-preco_compra)/preco_compra)
            #print('\nPercentagem: ',round(percentagem,2), '%')
            break
        #print ('----------------------------------------------')
            
        if x > mm25 and mm25 > mm50 and tenho_accoes==False:
        #if x < mm25 and mm25 < mm50 and tenho_accoes==False:    
            tenho_accoes = True
            preco_compra = x
            total_de_accoes = conta_inicial//x
            valor_da_compra = float(preco_compra * total_de_accoes)
            stop_loss_valor = calcula_stop_loss(float(x), float(preco_compra))
            #print('----------- COMPRA ----------------')
            #print('Valor por accao= ',round(preco_compra,2))
            #print('Total da compra = ',round(valor_da_compra,2))
            #print('Total de accoes = ', total_de_accoes)
            #print ('Valor do STOP LOSS = ',round(stop_loss_valor,2))
            
        if tenho_accoes == True:
            #print('Valor actual = ', round(x,2))
            stop_loss_valor_tmp = calcula_stop_loss(float(x), float(preco_compra))
            if stop_loss_valor_tmp > stop_loss_valor:
                stop_loss_valor = stop_loss_valor_tmp
            else:
                stop_loss_valor = stop_loss_valor
            #print ('Valor do STOP LOSS = ',round(stop_loss_valor,2))
            #print ('----------------------------------------------')
            
        
        contador += 1
    #Limpa a lista de preços    
    lista_de_precos.clear()
    return (round(percentagem,2),round(conta_final,2))
        

# Simular a estratégia n vezes
# Criar gráfico com os resultados
   
def simulacao(num_times):
    lista_percentagens = []
    totais_finais = []
    positivos,neutro,negativos = (0,0,0)
  
    for num in range(num_times):
        valor_per = calculaOpcaoCompra()
        lista_percentagens.append(valor_per[0])
        totais_finais.append(valor_per[1])
    
       
    #return num_plot
    plt.figure('MM25',figsize=(12, 10), dpi=80, facecolor='w', edgecolor='k')
    plt.clf()
    plt.axhline(y=0.0, color='r', linestyle='-')
    plt.xlabel('Simulações')
    plt.ylabel('Valor Lucro/Prejuizo %')
    plt.ylim(-20.0,50.0)
    plt.plot(lista_percentagens, 'bo')
    plt.title('Monte Carlo Simulation - BUY/SELL WITH STOP LOSS')         
    print('\n Total final : ',round(sum(totais_finais),2))
    
    
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
    
    print('\nProbabilidade de ter lucro = ',estProbabilidade_pos)
    print('\nProbabilidade de ter prejuizo = ',estProbabilidade_neg)
    print('\nProbabilidade de não fazer negócio = ',estProbabilidade_neu)
    print('\nMedia da distribuição (valor de retorno esperado) = ', round(np.mean(totais_finais),2), '€')
    print("\n5% quantile =",np.percentile(totais_finais,5))
    print("\n95% quantile =",np.percentile(totais_finais,95))          
    #return (round(sum(totais_finais),2))
    #return totais_finais


simulacao(200)
      
            
            
   