#!/usr/bin/python
# coding: UTF-8
import csv
from src.main.bitUtils import bitVectorUtils as classBit
from src.main.data import bitList as classBitList
from BitVector import BitVector
import time
csvData = "../data/arquivoDados.csv"

allow = classBit.makeBitVector(1)
deny = classBit.makeBitVector(0)



# Parsing CSV (Regras)
auxMatchKey = BitVector(size=0) # __init__ BitVect
rule_index = 0
with open(csvData, "rb") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='\'')
    for row in spamreader:   #Linha a linha do csv
        info_index = 0           # Indice
        classBitList.bitList.append([])
        for ind in range(len(row)):          # Coluna a coluna do csv
            row[info_index] = classBit.stringToIntFormated(row[info_index])  #Tudo vira inteiro
            row[info_index] = classBit.makeBitVector(row[info_index])
            classBitList.bitList[rule_index].append(row[info_index])
            info_index += 1
        rule_index += 1


# Catch action informations and put this in a specific list
n=0
for rule_id in range(len(classBitList.bitList)):

    classBitList.actionList.append(classBitList.bitList[n][-1])
    n += 1

new_index = 0
# Catch match informations and put this in a specific list
for rule_id in classBitList.bitList:
    auxPredicate = BitVector(size=0)
    for info_id in rule_id[0:-2]:
        auxPredicate += info_id
    classBitList.bitList[new_index] = auxPredicate
    new_index += 1



print classBitList.bitList[0], " -> ", classBitList.actionList[0]
print classBitList.bitList[2], " -> ", classBitList.actionList[2]
print type(classBitList.bitList[0]), " -> ", type(classBitList.actionList[0])
#print classBitList.bitList[4][-1]

print (classBitList.bitList[0] in classBitList.bitList)  #So'



# Insirindo pacote de teste
testePack = raw_input("Insira o pacote de teste[String de bits]: ")
testePack = classBit.stringToBit(testePack)

start = time.time()  #__init time
if (testePack in classBitList.bitList):
    index_testePack = classBitList.bitList.index(testePack)
    if (classBitList.actionList[index_testePack] == allow):
        print "OK"
    elif (classBitList.actionList[index_testePack] == deny):
        print "NAO OK"
else:
    print "pacote nao encontrado"
print type(testePack)

end = time.time()
print (end - start), "seconds"