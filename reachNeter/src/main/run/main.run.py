#!/usr/bin/python
# coding: UTF-8
import csv
from src.main.bitUtils import bitVectorUtils as classBit
from src.main.data import bitList as classBitList
from BitVector import BitVector
import time
csvData = "../data/data.csv"


allow = classBit.makeBitVector(1)
deny = classBit.makeBitVector(0)

swinc = 0    # Switch counter (for csv file)

# Parsing CSV (Regras)
auxMatchKey = BitVector(size=0) # __init__ BitVect
rule_index = 0
with open(csvData, "rb") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='\'')
    for row in spamreader:   #Linha a linha do csv
        info_index = 0           # Indice
        classBitList.bitList.append([])



        for ind in range(len(row)):          # Coluna a coluna do csv
            ''' FAZER NESSE MODELO O ACTION
            # Catch action informations and put this in a specific list
            n = 0
            for rule_id in range(len(classBitList.bitList)):
                classBitList.actionList.append(classBitList.bitList[n][-1])                           # <<<< NAO VAI TER MAIS ESSE LANCE DE PEGAR O ULTIMO COM -1
                n += 1
            '''

            row[info_index] = classBit.stringToIntFormated(row[info_index])  #Tudo vira inteiro
            row[info_index] = classBit.makeBitVector(row[info_index])
            classBitList.bitList[rule_index].append(row[info_index])


            #adicionar mais uma coluna com o switch, talvez algo antes, que mexa direto no arquivo de maneira separada

            info_index += 1
        if (len(classBitList.bitList[rule_index]) == 0):
            print "incrementou swinc"


        rule_index += 1

swinc = 0
for i in range(len(classBitList.bitList)):
    if (len(classBitList.bitList[i]) == 0):
        swinc += 1
    for j in range(len(classBitList.bitList[0])): # All lists have the same len

        try:
            print "sw: ", swinc
            print classBitList.bitList[i][j]
        except:
            pass
#print classBitList.bitList[64][6]
#print classBitList.bitList[64][9]

new_index = 0
# Catch match informations and put this in a specific list
for rule_id in classBitList.bitList:
    auxPredicate = BitVector(size=0)
    for info_id in rule_id[0:-2]:
        auxPredicate += info_id
    classBitList.bitList[new_index] = auxPredicate
    new_index += 1

print ">>>>>", classBitList.actionList ,"<<<<"

#print classBitList.bitList[0], " -> ", classBitList.actionList[0]
#print classBitList.bitList[2], " -> ", classBitList.actionList[2]
#print type(classBitList.bitList[0]), " -> ", type(classBitList.actionList[0])
#print classBitList.bitList[4][-1]

print (classBitList.bitList[0] in classBitList.bitList)  #So'

# Insirindo pacote de teste
testePack = raw_input("Insert the test package [Bit String]: ")
testePack = classBit.stringToBit(testePack)

start = time.time()  #__init time
'''
if (testePack in classBitList.bitList):
    index_testePack = classBitList.bitList.index(testePack)
    if (classBitList.actionList[index_testePack] == allow):
        print "Package pass"
    elif (classBitList.actionList[index_testePack] == deny):
        print "Package does not pass"
else:
    print "Package not found"
print type(testePack)
'''
end = time.time()
print (end - start), "seconds"
