import supp
from supp import *
import scipy
import os
from matplotlib import pyplot as plt
import statistics as stats
import openpyxl



UNIDADES = set()
JORNADAS = set()
CATEGORIAS = set()

usp_data = {}

#-------------------------------------
#-------------- ORGANIZE DATA -------- 
#-------------------------------------
for i in range(9,13):
    file = open(f"texts/{str(i)}-14.txt", "r")
    date_dic = {}
    for line in file:
        terms = line.strip().split(';')
        if terms[0] != ' Nome' and terms[0] != 'Nome':
            date_dic[f'{terms[0]}'] = {'Unidade': terms[1], 'Departamento': terms[2], 'Jornada' : f'{terms[3]}', 'Categoria' : terms[4],'Ingresso/Aposentadoria' : terms[5], 'Nivel' : terms[6],'Funcao' : terms[8],'Tempo_de_usp' : empty_to_zero(terms[11]),'Bonus' : empty_to_zero(terms[12].split(',')[0]),'Bruto' : empty_to_zero(terms[13].split(',')[0]),'Liquido' : empty_to_zero(terms[14].split(',')[0])}
    
    usp_data[f"{i}-{14}"] = date_dic
    file.close()


for j in range(15,24):
    for i in range(1,13):    
        file = open(f"texts/{str(i)}-{str(j)}.txt", "r")
        date_dic = {}
        for line in file:
            terms = line.strip().split(';')
            if terms[0] != ' Nome' and terms[0] != 'Nome':
                try:
                    date_dic[f'{terms[0]}'] = {'Unidade': terms[1], 'Departamento': terms[2], 'Jornada' : f'{terms[3]}', 'Categoria' : terms[4],'Ingresso/Aposentadoria' : terms[5], 'Nivel' : terms[6],'Funcao' : terms[8],'Tempo_de_usp' : empty_to_zero(terms[11]),'Bonus' : empty_to_zero(terms[12].split(',')[0]),'Bruto' : empty_to_zero(terms[13].split(',')[0]),'Liquido' : empty_to_zero(terms[14].split(',')[0])}
                except:
                    print(i,j,terms[0])

        usp_data[f"{i}-{j}"] = date_dic
        
        file.close()


for i in range(1,10):
        
        file = open(f"texts/{str(i)}-{str(24)}.txt", "r")
        date_dic = {}
        for line in file:
            terms = line.strip().split(';')
            if terms[0] != ' Nome' and terms[0] != 'Nome':
                UNIDADES.add(terms[1])
                JORNADAS.add(terms[3])
                CATEGORIAS.add(terms[4])
                date_dic[f'{terms[0]}'] = {'Unidade': terms[1], 'Departamento': terms[2], 'Jornada' : f'{terms[3]}', 'Categoria' : terms[4],'Ingresso/Aposentadoria' : terms[5], 'Nivel' : terms[6],'Funcao' : terms[8],'Tempo_de_usp' : empty_to_zero(terms[11]),'Bonus' : empty_to_zero(terms[12].split(',')[0]),'Bruto' : empty_to_zero(terms[13].split(',')[0]),'Liquido' : empty_to_zero(terms[14].split(',')[0])}
        usp_data[f"{i}-{24}"] = date_dic
        
        file.close()

supp.usp_data = usp_data
#----------------------------------------------------------

#--------------------- temporal series of wages -----------

#plotwages()
#plotcorrectedmedians()

#plot_min_max('Bruto')
#
#
##-------------------- institutes analysis -----------------
#
#unit_sizes = {}
#
#texto =  open('tabelainstitutos.txt', 'w')
#
#for inst in UNIDADES:
##    counter = 0
#
##    for person_data in usp_data[f'{9}-{24}'].values():
##        if person_data["Unidade"] == inst:
##            counter+=1
##    unit_sizes[inst] = counter
#    inmeans = givemean(f'{8}-{24}',[inst])
#    texto.write(f'{inst} & {int(inmeans[0])} & {int(inmeans[1])}')
#    texto.write(f'\n')
##
##----------------------------------------------------------
print(JORNADAS)
years = []
brute_wages = []
liquid_wages = []
cats_info = {}
for cat in CATEGORIAS:
    cats_info[cat] = [[],[],[]]

for person_data in usp_data[f'{9}-{24}'].values():
    y = person_data['Tempo_de_usp']
    b = person_data['Bruto']
    l = person_data['Liquido']
    years.append(y)
    brute_wages.append(b)
    liquid_wages.append(l)
    cats_info[f'{person_data["Categoria"]}'][0].append(y)
    cats_info[f'{person_data["Categoria"]}'][1].append(b)
    cats_info[f'{person_data["Categoria"]}'][2].append(l)

corr_b = stats.correlation(years,brute_wages)
corr_l = stats.correlation(years,liquid_wages)

print(f"The correlation between years of service and brute wage: {corr_b}")

print(f"The correlation between years of service and liquid wage: {corr_l}")

for cat in CATEGORIAS:
    if len(cats_info[cat][0]) != 0:
        try:
            c_b = stats.correlation(cats_info[cat][0],cats_info[cat][1])
            c_l = stats.correlation(cats_info[cat][0],cats_info[cat][1])
            print(f'Correlation brute for {cat}: {c_b}')
            print(f'Correlation liquid for {cat}: {c_l}')
        except:
            continue


av_wages_by_year = []
for i in range(0,20):
    this_year = []
    for person in usp_data[f'{9}-{24}'].values():
        if person['Tempo_de_usp'] == i:
            this_year.append(person['Bruto'])
    mean_this_year = stats.mean(this_year)
    av_wages_by_year.append(mean_this_year)

plt.plot(av_wages_by_year)
plt.show()



#current_brute = finddata(usp_data[f'{9}-{14}'],'Bruto')
#current_liquid = finddata(usp_data[f'{9}-{14}'],'Liquido')
#
#intervals = []
#freq_brute = []
#freq_liquid = []
#i=0
#while i*500 <= max(current_brute):
#    intervals.append(i*500)
#    counter_brute = 0
#    counter_liquid = 0
#    for value in current_brute:
#        if (i+1)*500 > value >= i*500:
#            counter_brute+=1
#    for value in current_liquid:
#        if (i+1)*500 > value >= i*500:
#            counter_liquid+=1
#    freq_brute.append(counter_brute)
#    freq_liquid.append(counter_liquid)
#    i+=1
#
#plt.scatter(intervals,freq_brute)
#plt.title('distribuição do salário bruto - setembro de 2014')
#plt.savefig('freq brute - set14')
#plt.close()
#plt.scatter(intervals,freq_liquid)
#plt.title('distribuição do salário líquido - setembro de 2014')
#plt.savefig('freq liquid - set14')
#plt.close()
#
#plt.scatter(intervals,get_accumulated(freq_brute))
#plt.title('salário bruto acumulado - setembro de 2014')
#plt.savefig('accum brute - set14')
#plt.close()
#plt.scatter(intervals,get_accumulated(freq_liquid))
#plt.title('salário líquido acumulado - setembro de 2014')
#plt.savefig('accum liquid - set14')
#plt.close()

#corrected1 = correct_by_inflation(brute_wages)
#corrected2 = correct_by_inflation(liquid_wages)
#plt.plot(corrected1)
#plt.plot(corrected2)
#plt.title('salario médio corrigido pela inflação')
#plt.savefig('media salarial real')




#------------------------------------------------------------------
#----------------------- ANALYSIS BY CAREER ---------------

#texto = open("tabelacategorias.txt", 'w')
#for cat in CATEGORIAS:
#    data_bruto = []
#    data_liquido = []
#    counter = 0
#    for person_data in usp_data[f'{8}-{24}'].values():
#        if person_data['Categoria'] == cat:
#            counter+=1
#            data_bruto.append(person_data['Bruto'])
#            data_liquido.append(person_data['Liquido'])
#    if len(data_bruto) == 0:
#        bru = 0
#        liq = 0
#    else:
#        bru = stats.mean(data_bruto)
#        liq = stats.mean(data_liquido)
#    texto.write(f'{cat} & {bru} & {liq}')
#    print(f'{cat}: {counter}')
#sdv_liquid_evolution = []
#sdv_brute_evolution = []
#sdv_bonus_evolution = []
#
#for dix in usp_data.values():
#    sdv_liquid_evolution.append(stats.stdev(finddata(dix,'Liquido')))
#    sdv_brute_evolution.append(stats.stdev(finddata(dix,'Bruto')))
#    sdv_bonus_evolution.append(stats.stdev(finddata(dix,'Bonus')))

