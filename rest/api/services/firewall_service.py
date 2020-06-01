#!/usr/bin/env python

import logging
import os
import sys
import json
from os import system
import time
import firewall_rules from ../constants as FIREWALL_RULES
import flowtable_rules from ../constants as FLOWTABLE_RULES

logger = logging.getLogger("firewall_service")
logging.basicConfig(level = logging.INFO)

def areRulesAvailable(objRule):
    for i in objRule.keys():
        return False if (!(i in FIREWALL_RULES.RULES) or !(i in FLOWTABLE_RULES.RULES))
    return True

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
    if (len(objRule) < 1):
        logger.error("New rule is empty")
        return {"error": "New rule is empty"}
    elif !("switch" in objRule):
        logger.error("New rule has no addressed switch")
        return {"error": "New rule has no addressed switch"}
    elif(areRulesAvailable(objRule)):
        print("TODO")
        
    string_regraFirewall = raw_input("Insira a string com a regra: ")

    # Colocar IP:PORTA
    command = "curl -s -d '{" + string_regraFirewall + "}' http://143.54.12.10:8080/wm/staticflowpusher/json"

    verificaMenu = raw_input("\n\n[1] - Ver opcao desejada (Durante 5 segundos)\n[2] - Menu\n[3] - Adicionar mais regras ao Firewall\n[4] - Sair\n-> ")

    command_output = os.popen(command).read()
    status_regraAdicionada = json.loads(command_output)
    print "\nStatus da regra adicionada: ", status_regraAdicionada, "\n"

def startNetwork(auto_set_macs, hosts, ip, links, switches):
    
    return True