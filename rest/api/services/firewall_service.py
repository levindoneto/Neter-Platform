#!/usr/bin/env python

import logging
import os
import sys
import json
from os import system
import time

logger = logging.getLogger("conflicts")
logging.basicConfig(level = logging.INFO)

"""
Add rule to firewall
@param: rawRule
Format:
{
   "switch": <str>,
   <str:property>:<str:value>,
   ...
}
"""
def addRule(objRule, ip, port):
        string_regraFirewall = raw_input("Insira a string com a regra: ")

        # Colocar IP:PORTA
        comando = "curl -s -d '{" + string_regraFirewall + "}' http://143.54.12.10:8080/wm/staticflowpusher/json"

        verificaMenu = raw_input("\n\n[1] - Ver opcao desejada (Durante 5 segundos)\n[2] - Menu\n[3] - Adicionar mais regras ao Firewall\n[4] - Sair\n-> ")

        command_output = os.popen(comando).read()
        status_regraAdicionada = json.loads(command_output)
        print "\nStatus da regra adicionada: ", status_regraAdicionada, "\n"

def startNetwork(auto_set_macs, hosts, ip, links, switches):
    
    return True