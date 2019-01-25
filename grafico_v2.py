# -*- coding: utf-8 -*-
"""
Created on Sat Jan 19 14:49:11 2019

@author: ruialberto
"""

import pylab as plt

lista_percentagens =[5.07,
-0.20,
8.47,
0.84,
-3.80,
3.48,
7.06,
-4.21,
0.19,
5.66,
4.78,
1.17,
6.12,
-3.19,
4.92,
1.14,
7.50,
17.95,
0.41,
2.96,
2.87,
0.78,
-0.06,
-3.81,
3.61,
3.07,
-4.62,
12.51,
-3.50,
3.28,
8.17,
5.39,
2.50,
2.87,
-0.13,
2.01,
-1.04,
-0.47,
0.96,
3.24,
-3.08,
-11.71,
0.50,
1.98,
1.56,
1.27,
1.14,
1.48,
-0.43,
-0.98,
1.23,
1.18,
0.99,
1.98,
1.68,
0.98,
2.39,
2.31,
0.51,
-2.30,
0.29,
1.44,
2.08,
1.64,
-4.44,
-7.98,
-0.06,
-7.63,
-3.00,
-12.66,
3.94,
10.91,
5.30,
5.01,
-7.13,
1.15,
0.29,
4.11,
6.16,
7.60,
-0.13,
1.00,
1.08,
1.33,
1.91,
1.89,
-4.35,
-1.96,
-0.50,
-3.48,
2.09,
-5.15,
-3.83,
-2.55,
3.16,
-5.06,
5.87,
3.59,
1.99,
1.34,
1.63,
0.89,
1.21,
3.02,
3.68,
1.23,
3.24,
2.05,
]




lista_valores_finais=[153.70,
146.50,
419.50,
487.00,
352.00,
479.20,
761.20,
678.70,
685.45,
846.60,
1080.60,
1122.95,
1220.85,
1168.45,
1365.05,
1383.85,
1646.35,
2318.35,
2333.40,
2436.25,
2541.25,
2567.85,
2565.65,
2495.15,
2625.15,
2733.05,
2577.05,
2913.05,
2868.25,
2910.25,
3145.13,
3355.13,
3532.93,
3638.23,
3634.57,
3726.37,
3684.77,
3668.15,
3702.15,
3813.91,
3761.26,
3561.06,
3576.66,
3626.82,
3680.02,
3726.02,
3770.93,
3845.61,
3828.61,
3782.06,
3831.51,
3870.26,
3909.26,
4002.26,
4069.48,
4102.12,
4179.88,
4278.68,
4296.28,
4216.28,
4226.68,
4274.15,
4346.15,
4402.25,
4327.25,
4176.50,
4174.50,
4070.55,
4020.55,
3768.55,
3842.80,
4054.00,
4155.50,
4258.00,
4033.00,
4062.25,
4070.25,
4180.50,
4343.70,
4532.70,
4528.85,
4584.10,
4622.10,
4662.10,
4725.10,
4782.85,
4646.35,
4588.85,
4574.45,
4524.45,
4554.45,
4480.65,
4425.75,
4385.25,
4430.25,
4349.25,
4524.75,
4572.45,
4621.40,
4654.40,
4684.10,
4704.85,
4732.85,
4807.85,
4897.55,
4927.45,
5005.75,
5055.90
]


                    

lista_positivos = [i for i in lista_percentagens if i  >= 0.0]
lista_negativos = [i for i in lista_percentagens if i < 0.0]
total_negocios_fechados = len(lista_percentagens)
total_negativos = len(lista_negativos)
percentagem_negativos = (100*total_negativos)/total_negocios_fechados
percentagem_positivos = 100 - round(percentagem_negativos,2)

print('\n Total de negócios fechados: ', total_negocios_fechados)
print('\n Total de negócios positivos: ', len(lista_positivos))
print('\n Total de negócios negativos: ', len(lista_negativos))
print('\n Percentagem de negócios positivos: ',round(percentagem_positivos,2),'%')
print('\n Percentagem de negócios negativos: ',round(percentagem_negativos,2),'%')


plt.figure('MM25',figsize=(14, 8), dpi=80, facecolor='w', edgecolor='k')
plt.clf()
plt.axhline(y=0.0, color='r', linestyle='-')
plt.xlabel('Negócios')
plt.ylabel('Valor Lucro/Prejuizo %')
plt.ylim(-20.0,50.0)
plt.plot(lista_percentagens, 'bo')
plt.title('Gráfico - Long: Dados reais 2018')


print('\n\n')

plt.figure('Acumulacao',figsize=(14, 8), dpi=80, facecolor='w', edgecolor='k')
plt.clf()
plt.axhline(y=0.0, color='r', linestyle='-')
plt.xlabel('Total de Negócios')
plt.ylabel('Valor Acumulado em €')
plt.ylim(-1000.0,6000.0)
plt.plot(lista_valores_finais, 'bo-')
plt.title('Gráfico - Dados reais 2018 (Abril - Janeiro):')
print('\n')
print('\n Resultado Actual: ', lista_valores_finais[-1],'€')
