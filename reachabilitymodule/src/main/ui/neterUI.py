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
    print("| 1 - Read the network  file [.csv]           |")
    print("| 2 - Verify reachability                     |")
    print("|---------------------------------------------|")
    opt = input("\nChoice an option: ")
    return opt