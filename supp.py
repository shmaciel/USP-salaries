import scipy
import os
from matplotlib import pyplot as plt
import statistics as stats
import openpyxl


#-------------------------------------
#-------------- SET UP ---------------
#------------------------------------

usp_data = {}

def empty_to_zero(word):
    if word == "":
        return 0
    else:
        return int(word)

#-------------------------------------
#-------------- METHODS -------------
#-------------------------------------

def finddata(dix,data_name,Inst = None):
# receive a month-dict and a data tag and filter by institute
# returns a list containing such data
    data = []
    for person_data in dix.values():
        if Inst==None:
            data.append(person_data[data_name])
        elif person_data["Unidade"] in Inst:
            data.append(person_data[data_name])
    if data!=[]:
        return data
    else:
        return [0]
    
def plot_person_wage(person, person2 = None):
    Parcels_L = []
    Parcels_B = []
    Parcels_Bon = []
    for month in usp_data.values():
        try:
            Parcels_L.append(month[f"{person}"]["Liquido"])
            Parcels_B.append(month[f"{person}"]["Bruto"])
            Parcels_Bon.append(month[f"{person}"]["Bonus"])
        except:
            Parcels_L.append(month[f"{person2}"]["Liquido"])
            Parcels_B.append(month[f"{person2}"]["Bruto"])
            Parcels_Bon.append(month[f"{person2}"]["Bonus"])
    plt.plot(Parcels_L)
    plt.plot(Parcels_B)
    plt.plot(Parcels_Bon)
    plt.title(f'{person}')
    plt.savefig(f'{person}.png')

def calculatemean(date, institutes):
#prints the
    for ins in institutes:
        avg_l = stats.mean(finddata(usp_data[date], 'Liquido', [ins]))
        avg_b = stats.mean(finddata(usp_data[date], 'Bruto', [ins]))
        print(f"mean liquid wage of {ins} at {date}: {avg_l}")
        print(f"mean brute wage of {ins} at {date}: {avg_b}")

def givemean(date, institutes):
#prints the
    for ins in institutes:
        avg_l = stats.mean(finddata(usp_data[date], 'Liquido', [ins]))
        avg_b = stats.mean(finddata(usp_data[date], 'Bruto', [ins]))
        return avg_b, avg_l

def calculatesdv(date, institutes):
#prints the
    for ins in institutes:
        avg_l = stats.stdev(finddata(usp_data[date], 'liquido', [ins]))
        avg_b = stats.stdev(finddata(usp_data[date], 'bruto', [ins]))
        print(f"stdev liquid wage of {ins} at {date}: {avg_l}")
        print(f"stdev brute wage of {ins} at {date}: {avg_b}")


def plotwages(Institutes = None):
    if Institutes != None:
        for ins in Institutes:
            liquids = []
            brutes = []
            for dix in usp_data.values():
                liquids.append(stats.mean(finddata(dix, 'Liquido',[ins])))
                brutes.append(stats.mean(finddata(dix,'Bruto',[ins])))
            plt.plot(liquids)
            plt.plot(brutes)
            plt.title(f'media salarial {ins}')
            plt.savefig(f'media salarial {ins}.png')
    else:
        liquids = []
        brutes = []
        for dix in usp_data.values():
            liquids.append(stats.mean(finddata(dix, 'Liquido')))
            brutes.append(stats.mean(finddata(dix,'Bruto')))
        plt.plot(liquids)
        plt.plot(brutes)
        plt.title('media salarial')
        plt.savefig('media salaria.png')


def plotmedians(Institutes = None):
    if Institutes != None:
        for ins in Institutes:
            liquids = []
            brutes = []
            for dix in usp_data.values():
                liquids.append(stats.median(finddata(dix, 'Liquido',[ins])))
                brutes.append(stats.median(finddata(dix,'Bruto',[ins])))
            plt.plot(liquids)
            plt.plot(brutes)
            plt.title(f'mediana salarial {ins}')
            plt.savefig(f'mediana salarial {ins}.png')
    else:
        liquids = []
        brutes = []
        for dix in usp_data.values():
            liquids.append(stats.median(finddata(dix, 'Liquido')))
            brutes.append(stats.median(finddata(dix,'Bruto')))
        plt.plot(liquids)
        plt.plot(brutes)
        plt.title('mediana salarial')
        plt.savefig('mediana salaria.png')

def plotcorrectedmedians(Institutes = None):
    if Institutes != None:
        for ins in Institutes:
            liquids = []
            brutes = []
            for dix in usp_data.values():
                liquids.append(stats.median(finddata(dix, 'Liquido',[ins])))
                brutes.append(stats.median(finddata(dix,'Bruto',[ins])))
            plt.plot(correct_by_inflation(liquids))
            plt.plot(correct_by_inflation(brutes))
            plt.title(f'mediana salarial real {ins}')
            plt.savefig(f'mediana salarial real {ins}.png')
    else:
        liquids = []
        brutes = []
        for dix in usp_data.values():
            liquids.append(stats.median(finddata(dix, 'Liquido')))
            brutes.append(stats.median(finddata(dix,'Bruto')))
        plt.plot(correct_by_inflation(liquids))
        plt.plot(correct_by_inflation(brutes))
        plt.title(f'mediana salarial real')
        plt.savefig(f'mediana salarial real.png')

def get_accumulated(frequencies):
    accumulation = []
    total = sum(frequencies)
    for i in range(0,len(frequencies)):
        if i==0:
            accumulation.append(100*frequencies[0]/total)
        else:
            accumulation.append(100*frequencies[i]/total + accumulation[i-1])
    return accumulation

#--------------------------------------------------------------------------

#------------------------------------------------------
#-------------------- SPECIFIC ANALYSIS ---------------
#------------------------------------------------------


def plot_min_max(numericalkey, Inst = None):
    minvalues = []
    maxvalues = []
    for dix in usp_data.values():
        allwages = []
        vals = finddata(dix,numericalkey, Inst)
        c = vals.count(0)
        while min(vals)==0:
            vals.remove(0)
        maxvalues.append(max(vals))
        minvalues.append(min(vals))
#    plt.plot(minvalues)
    plt.plot(maxvalues)
    if Inst==None:
        plt.title(f'salario maximo de {numericalkey}')
    else:
        plt.title(f'salario maximo de {numericalkey} nos institutos {Inst}')
    plt.savefig(f'minmax {numericalkey}')
    plt.close()
    

def correct_by_inflation(wages):
    infl_series = []
    real_wages = []
    wb = openpyxl.load_workbook('inflation.xlsx')
    sheet = wb.get_sheet_by_name(wb.get_sheet_names()[0])
    for i in range(0,121):
        infl_series.append(sheet.cell(5,2+i).value)
    
    ind = 0
    while ind < 121:
        real_wages.append(wages[ind]*infl_series[-1]/infl_series[ind])
        ind+=1
    return real_wages

