#!/usr/bin/python
# coding: UTF-8
from os import system

''' Text Interface of the aplication
    @parameter : void
    @return    : int '''
def menu():
    system("clear")
    print("|---------------------------------------------|")
    print("|--------- SCRIPT FLOWTABLE FIREWALL ---------|")
    print("| 7 - Ler arquivo de dados [.csv]             |")
    print("| 2 - Verificar reachability                  |")
    print("|---------------------------------------------|")
    opt = input("\nEscolha: ")
    return opt