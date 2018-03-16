# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 18:04:09 2016
@author: ruialberto
 Monte Carlo - Simulação:
 - Compra e venda de accões utilizando as MM como sinal compra/venda
 - Preço da accao acima da MM venda
 - Preço actual acima determinada percentagem do preço compra - "Vender c/ lucro"
 - Preço abaixo da MM vender
"""
import pylab as plt
import random

lista = []


def cria250precos():
    """
    Cria uma lista aleatoria com 250 numeros reais (5.0 - 25.78)
    Cada valor criado simula o preço de fecho de uma acção
    """

    #Primeiro valor aleatorio
    x = random.uniform(0.10, 0.40)
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


def calculoMedia25():
    """
    Calcula a media dos ultimos n dias
    """

    ultimos_25_dias = []
    # Seleciona os ultimos n numeros da lista global (lista)
    ultimos_25_dias.extend(lista[-25:])
    media25 = sum(ultimos_25_dias)/25

    return media25

def calculoMedia50():
    """
    Calcula a media dos ultimos n dias
    """

    ultimos_50_dias = []
    # Seleciona os ultimos n numeros da lista global (lista)
    ultimos_50_dias.extend(lista[-50:])
    media50 = sum(ultimos_50_dias)/50

    return media50

def calculaOpcaoCompra(dias):
    """
    Cria um novo preço. Simula o preço do fecho de hoje.
    O valor diario, será aleatoriamente calculado, em relação ao valor do dia
    anterior.
    Intervalo de escolha : (top - valor dia anterior + 10%;
                            fundo - valor dia anterior - 10%)
    """
    n_accoes = 0
    minha_conta = 25000.0
    cria250precos() # Chama a funcão que cria uma lista inicial de 250 preços
    conta_fim = 25000.0

    print ()
    print ('Inicio da Conta: ',minha_conta)
    print ('--------------------------')
    print ()
    while dias > 0:

        #Calcula a media dos ultimos 25 dias
        mm25 = calculoMedia25()
        #Calcula a media dos últimos 50 dias
        mm50 = calculoMedia50()
        #preço do dia anterior
        ultimo_preco = lista[-1]
        #valor +10% do preço de fecho
        top = float(ultimo_preco + ((ultimo_preco*10)/100))
        #valor -10% do preço de fecho
        fundo = float(ultimo_preco - ((ultimo_preco*10)/100))
        #simula o preço de hoje
        x = random.uniform(fundo,top)
        #adiciona o novo preço (preço de hoje) à lista global (lista)
        lista.append(x)
        #Se preço de hoje > MM, e não temos accoes - Comprar
        if x > mm25 and n_accoes == 0:
            print('Media 25: %.2f' %mm25)
            print('Valor da accao de hoje: %.2f' %x)
            n_accoes = minha_conta//x
            ultimo_preco = x
            print('Comprar ', n_accoes, ' accoes.')
            conta_fim = minha_conta # Mantem o valor da minha conta até ao final
            minha_conta -= minha_conta
            print('Valor da minha conta actual: %.2f' %minha_conta)
            dias = dias - 1
            print('Faltam ', dias, 'para terminar.')
            print('----------------------------------\n')
        #Se tenho lucro de x % vender
        elif x > mm25 and n_accoes > 0 and ((x - ultimo_preco) > ((ultimo_preco*4)/100)):
            minha_conta = n_accoes * x
            conta_fim = minha_conta
            n_accoes = 0
            dias = dias -1
            print('Venda das accoes: LUCRO LUCRO LUCRO')
            p = (100* (x-ultimo_preco))/ultimo_preco
            print ('Percentagem lucro: %.2f' %p)
            print('Valor da compra: %.2f' %ultimo_preco)
            print('Valor da venda: %.2f' %x)
            print ('Valor Conta Actual: %.2f' %minha_conta)
            print('Faltam ', dias, 'para terminar.')
            print('----------------------------------\n')
        #Se preço desce abaixo MM, vender
        elif x < mm25 and mm25 < mm50 and n_accoes > 0:
        #elif x < mm25 and n_accoes > 0 and ((x - ultimo_preco) < ((ultimo_preco*3)/100)):
            minha_conta = n_accoes * x
            conta_fim = minha_conta
            print('Media 25: %.2f' %mm25)
            print('Valor da accao de hoje: %.2f' %x)
            print('Venda das accoes: PREJUIZO')
            print ('Valor Conta Actual: %.2f' %minha_conta)
            n_accoes = 0
            dias = dias - 1
            print('Faltam ', dias, 'para terminar.')
            print('----------------------------------\n')
        #Senão não faz nada
        else:
            dias = dias - 1
            print ('Valor accao hoje: %.2f' %x)
            print ('Media 25: %.2f' %mm25)
            print('Faltam ', dias, 'para terminar.')
            print('----------------------------------\n')


    return conta_fim


def simulacao(num_vezes):
        lista_res = []
        #lista_plot = []
        nada, trimestre_lucro, trimestre_prejuizo = (0,0,0)
        total_lucro = 0
        total_prej = 0
        for i in range(num_vezes):
            r_final = calculaOpcaoCompra(66) # 66 dias = trimestre
            dif = float(r_final - 25000)
            lista_res.append(dif)

        for f in lista_res:
            if f == 0:
                nada += 1
            elif f > 0:
                trimestre_lucro +=1
                total_lucro = total_lucro + f
            else:
                trimestre_prejuizo +=1
                total_prej = total_prej + f

        num_plot = total_lucro + total_prej
        prob_l = trimestre_lucro / num_vezes
        prob_pjz = trimestre_prejuizo / num_vezes

        #return round(num_plot,2)
        #lista_plot.append(num_plot)

        print('Lista de Lucros/Prejuizos: ', lista_res)
        print()
        print()
        print('---------------------------------------\n')
        print('---------   DADOS FINAIS   ------------\n')
        print('---------------------------------------\n')
        print('Trimestre Lucro: ', trimestre_lucro)
        print('Valor do Lucro: %.2f' %total_lucro)
        print('Trimestre Prejuizo: ', trimestre_prejuizo)
        print('Valor do Prejuizo: %.2f' %total_prej)
        print('Igual (25000 iniciais)): ', nada)
        print('Probabilidade de lucro = %.2f' %prob_l)
        print('Probabilidade de prejuizo = %.2f' %prob_pjz)
        print('---------------------------------------\n')
        print('FINAL = %.2f' %num_plot)
        print('---------------------------------------\n')

        #return num_plot
        plt.figure('MM25',figsize=(12, 10), dpi=80, facecolor='w', edgecolor='k')
        plt.clf()
        plt.axhline(y=0.0, color='r', linestyle='-')
        plt.xlabel('Trimestres')
        plt.ylabel('Valor Lucro/Prejuizo')
        plt.ylim(-50000,50000)
        plt.plot(lista_res, 'bo')
        plt.title('Monte Carlo Simulation - Stock MM25')


simulacao(20)

"""
ganhou,perdeu,gains,losses=(0,0,0,0)
lista_res_2 = []
for f in range(10):
    lista_res_2.append(simulacao(20))
print (lista_res_2)
for num in lista_res_2:
    if num >= 0:
        ganhou += 1
        gains += num
    else:
        perdeu += 1
        losses -= num
print ('\nGanhou ',ganhou, ' vezes.')
print ('Perdeu ',perdeu, ' vezes.')
print ('Gains: ', gains)
print ('Losses: ', losses)
print ('Total Final: ', round(float(gains-losses),2))
#plt.figure('MM25')
#plt.clf()
#plt.xlabel('Resultados em €')
#plt.ylabel('Nº de Simulações')
#plt.plot(lista_res_2, 'r')
#plt.title('Monte Carlo Simulation - Stock MM25')
#print('Minha conta: %.2f' %calculaOpcaoCompra(22))

"""