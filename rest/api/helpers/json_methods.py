import json
from os import system
import time

cont_time = 0

formattedJsonBuffer = "../data/dataflow_formatoVB.json"

def formatJson(filename):
    jsonFile = filename
    var_buffer = open(jsonFile, "r")
    dicttable = ""

    for i in var_buffer:
        dicttable += i

    strings = ""
    cont = 0

    for j in dicttable:
        if j == "u":
            if dicttable[cont+1] == "'":
                strings +=""
            else:
                strings += j
        else:
            strings += j
        cont += 1

    dicttable = ""

    for k in strings:
        if k!= "'":
            dicttable += k
        else:
            dicttable += '"'

    strings = ""
    for l in dicttable:
        if l=="]" or l=="}":
            strings += "\n" + l
        elif l==",":
            strings += l + "\n"
        elif l=="{" or l=="[":
            strings += "\n" + l + "\n"
        else:
            strings += l

    var_buffer = open(formattedJsonBuffer, "w")
    var_buffer.write(strings)
    var_buffer.close()
