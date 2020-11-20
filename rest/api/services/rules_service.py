#!/usr/bin/env python

import logging
import os
import sys
from os import system
import json
import time
from . import flowtable_service as FlowtableService

logger = logging.getLogger("conflicts")
logging.basicConfig(level = logging.INFO)

#-> Info - Match - Flowtable
eth_src = ""
eth_dst = ""
eth_type = ""
in_port = ""
eth_vlan_vid = ""
eth_vlan_pcp = ""
ip_proto = ""
ipv4_src = ""
ipv4_dst = ""
ipv6_src = ""
ipv6_dst = ""
ipv6_label = ""
ip_tos = ""
ip_ecn = ""
ip_dscp = ""
tp_src = ""
tp_dst = ""
udp_src = ""
udp_dst = ""
tcp_src = ""
tcp_dst = ""
sctp_src = ""
sctp_dst = ""
icmpv4_type = ""
icmpv4_code = ""
icmpv6_type = ""
icmpv6_code = ""
ipv6_nd_ssl = ""
ipv6_nd_ttl = ""
ipv6_nd_target = ""
arp_opcode = ""
arp_tha = ""
arp_spa = ""
arp_tpa = ""
mpls_label = ""
mpls_tc = ""
mpls_bos = ""
tunnel_id = ""
metadata = ""
#-> Info - Match - Firewall
dl_type = ""
nw_src_prefix = ""
any_nw_dst = ""
any_nw_proto = ""
any_in_port = ""
any_nw_srcany_tp_ds = ""
ruleid = ""
any_dl_type = ""
priority = ""
in_port = ""
any_dpid = ""
dl_src = ""
nw_src_maskbits = ""
nw_dst_maskbits = ""
dpid = ""
tp_src = ""
any_dl_dst = ""
nw_dst_prefix = ""
nw_proto = ""
tp_dst = ""
dl_dst = ""
any_tp_src = ""
action = ""

arquivoFormatadoJsonVB = "rest/api/data/dataflow_formatoVB.json"
arquivoFormatadoJson = "rest/api/data/dataflow_formato.json"  # VB: Variable buffer

def getId():
    import random

    return str(random.randint(1,100000000))

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

    var_buffer = open(arquivoFormatadoJsonVB, "w")
    var_buffer.write(strings)
    var_buffer.close()

def getConflictMessage(flowCI, flowCJ, SwitchC):
    return "Conflict detected between the flow " + str(flowCI) \
        + " and the flow " + str(flowCJ) + " on the switch " + str(SwitchC)

def getRedundancyMessage(flowCI, flowCJ, SwitchC):
    return "Redundancy detected between the flow " + str(flowCI) \
        + " and the flow " + str(flowCJ) + " on the switch " + str(SwitchC)

def verifyFlowtable(ip, port):
    topology = FlowtableService.getFlows(ip, port)
    dataFlowPath = FlowtableService.createDataFlow(topology)
    formatJson(dataFlowPath)

    flag_confRed = 0

    strings = ""
    arquivo_dados = open(arquivoFormatadoJsonVB, "r")
    for i in arquivo_dados:
        strings += i
    arquivo_dados.close()

    with open(arquivoFormatadoJsonVB) as f:
        data = f.read()
        json_data = json.loads(data)

    lista_switches = json_data[json_data.keys()[0]].keys() # json_data.keys()[0] is the topology key
    print("lista_switches: ", lista_switches)

    fileId = getId()
    arquivo_regras = open("rest/api/data/flowtable_" + fileId + ".txt", "w")
    arquivo_regras_conflitantes = open("rest/api/data/conflicts_" + fileId + ".txt", "w")
    arquivo_regras_redundantes = open("rest/api/data/redundancies_" + fileId + ".txt", "w")

    flowList = []

    contSwitch = 0
    lista_switches.sort()
    time_init = time.time()
    n_flows = 0
    for s in lista_switches:
        dicFlows = {}
        with open(arquivoFormatadoJsonVB) as f:
            data = f.read()
            json_data = json.loads(data)
        try:
            json_data = json_data[json_data.keys()[0]]
            json_data = json_data[s]
            json_data = json_data["flows"]
        except:
            pass

        lista_prioridade =      []
        lista_hard_timeout_s =  []
        lista_byte_count =      []
        lista_idle_timeout_s =  []
        lista_duration_nsec =   []
        lista_packet_count =    []
        lista_duration_sec =    []
        lista_version =         []
        lista_table_id =        []
        lista_duracao =         []
        lista_byteCount =       []
        lista_packetCount =     []
        lista_cookie =          []
        # Lists - Match
        lista_ethSrc =          []
        lista_ethDst =          []
        lista_ethType =         []
        lista_inPort =          []
        lista_outPort =          []
        lista_eth_vlan_vid =    []
        lista_eth_vlan_pcp =    []
        lista_ip_proto =        []
        lista_ipv4_src =        []
        lista_ipv4_dst =        []
        lista_ipv6_src =        []
        lista_ipv6_dst =        []
        lista_ipv6_label =      []
        lista_ip_tos =          []
        lista_ip_ecn =          []
        lista_ip_dscp =         []
        lista_tp_src =          []
        lista_tp_dst =          []
        lista_udp_src =         []
        lista_udp_dst =         []
        lista_tcp_src =         []
        lista_tcp_dst =         []
        lista_sctp_src =        []
        lista_sctp_dst =        []
        lista_icmpv4_type =     []
        lista_icmpv4_code =     []
        lista_icmpv6_type =     []
        lista_icmpv6_code =     []
        lista_ipv6_nd_ssl =     []
        lista_ipv6_nd_ttl =     []
        lista_ipv6_nd_target =  []
        lista_arp_opcode =      []
        lista_arp_opcode =      []
        lista_arp_tha =         []
        lista_arp_spa =         []
        lista_arp_tpa =         []
        lista_mpls_label =      []
        lista_mpls_tc =         []
        lista_mpls_bos =        []
        lista_tunnel_id =       []
        lista_metadata =        []
        lista_actions =         []
        
        print("LEN json_data: ", len(json_data))
        
        arquivo_regras.write("[Switch: " + s + "]\n")
        for rule_index in range(len(json_data)):
            if json_data[rule_index].has_key('priority') == True:
                lista_prioridade.append(json_data[rule_index]['priority'])
            else:
                lista_prioridade.append("x") # wildcard
            if json_data[rule_index].has_key('hard_timeout_s') == True:
                lista_hard_timeout_s.append(str(json_data[rule_index]['hard_timeout_s']))
            else:
                lista_hard_timeout_s.append("x") # wildcard
            
            if json_data[rule_index].has_key('byte_count') == True:
                lista_byte_count.append(str(json_data[rule_index]['byte_count']))
            else:
                lista_byte_count.append("x") # wildcard
            
            if json_data[rule_index].has_key('idle_timeout_s') == True:
                lista_idle_timeout_s.append(str(json_data[rule_index]['idle_timeout_s']))
            else:
                lista_idle_timeout_s.append("x") # wildcard
            
            if json_data[rule_index].has_key('duration_nsec') == True:
                lista_duration_nsec.append(str(json_data[rule_index]['duration_nsec']))
            else:
                lista_duration_nsec.append("x") # wildcard
            
            if json_data[rule_index].has_key('packet_count') == True:
                lista_packet_count.append(str(json_data[rule_index]['packet_count']))
            else:
                lista_packet_count.append("x") # wildcard
            
            if json_data[rule_index].has_key('duration_sec') == True:
                lista_duration_sec.append(str(json_data[rule_index]['duration_sec']))
            else:
                lista_duration_sec.append("x") # wildcard
            
            if json_data[rule_index].has_key('version') == True:
                lista_version.append(str(json_data[rule_index]['version']))
            else:
                lista_version.append("x") # wildcard
            
            if json_data[rule_index].has_key('table_id') == True:
                lista_table_id.append(str(json_data[rule_index]['table_id']))
            else:
                lista_table_id.append("x") # wildcard

            if json_data[rule_index].has_key('instructions') == True:
                if json_data[rule_index]['instructions'].has_key('instruction_apply_actions') == True:
                    lista_actions.append(str(json_data[rule_index]['instructions']['instruction_apply_actions']['actions']))
                else:
                    lista_actions.append(str(json_data[rule_index]['instructions']['none']))
            else:
                lista_actions.append("x")

            if json_data[rule_index].has_key('packetCount') == True:
                lista_packetCount.append(str(json_data[rule_index]['packetCount']))
            else:
                lista_packetCount.append("x")

            if json_data[rule_index].has_key('match') == True:
                if json_data[rule_index]['match'].has_key('out_port') == True:
                    lista_outPort.append(str(json_data[rule_index]['match']['out_port']))
                else:
                    lista_outPort.append("x")

            arquivo_regras.write("("+ 
                str(lista_prioridade[rule_index]) + " ^ " + 
                str(lista_hard_timeout_s[rule_index]) + " ^ " + 
                str(lista_byte_count[rule_index]) + " ^ " + 
                str(lista_idle_timeout_s[rule_index]) + " ^ " + 
                str(lista_duration_nsec[rule_index]) + " ^ " + 
                str(lista_packet_count[rule_index]) + " ^ " + 
                str(lista_duration_sec[rule_index]) + " ^ " + 
                str(lista_version[rule_index]) + " ^ " + 
                str(lista_table_id[rule_index])+ " ^ " + 
                # str(lista_inPort[rule_index]) + " ^ " +
                str(lista_outPort[rule_index]) +
                ") -> " + str(lista_actions[rule_index]) + "\n")
            dicFlows.update({
                s:[
                    lista_prioridade[rule_index],
                    lista_idle_timeout_s[rule_index],
                    lista_hard_timeout_s[rule_index],
                    lista_byte_count[rule_index],
                    lista_duration_nsec[rule_index],
                    lista_packet_count[rule_index],
                    lista_duration_sec[rule_index],
                    lista_version[rule_index],
                    # lista_inPort,
                    lista_outPort,
                    lista_actions
                ]
            })
        arquivo_regras.write("\n\n")
        i = 0
        j = 0

        #verification
        for l in range(len(lista_actions)-1):
            j = i + 1
            for k in range(len(lista_actions)-(i+1)):
                if (lista_prioridade[i]=='x'):
                    lista_prioridade[i] = lista_prioridade[j]
                if (lista_idle_timeout_s[i]=='x'):
                    lista_idle_timeout_s[i] = lista_idle_timeout_s[j]
                if (lista_hard_timeout_s[i]=='x'):
                    lista_hard_timeout_s[i] = lista_hard_timeout_s[j]
                if (lista_byte_count[i]=='x'):
                    lista_byte_count[i] = lista_byte_count[j]
                if (lista_duration_nsec[i]=='x'):
                    lista_duration_nsec[i] = lista_duration_nsec[j]
                if (lista_packet_count[i]=='x'):
                    lista_packet_count[i] = lista_packet_count[j]
                if (lista_duration_sec[i]=='x'):
                    lista_duration_sec[i] = lista_duration_sec[j]
                if (lista_version[i]=='x'):
                    lista_version[i] = lista_version[j]
                # if (lista_inPort[i]=='x'):
                #     lista_inPort[i] = lista_inPort[j]
                if (lista_outPort[i]=='x'):
                    lista_outPort[i] = lista_outPort[j]
                if(lista_prioridade[i]==lista_prioridade[j] and 
                    lista_idle_timeout_s[i]==lista_idle_timeout_s[j] and
                    lista_hard_timeout_s[i]==lista_hard_timeout_s[j] and
                    lista_byte_count[i]==lista_byte_count[j] and
                    lista_duration_nsec[i]==lista_duration_nsec[j] and
                    lista_packet_count[i]==lista_packet_count[j] and
                    lista_duration_sec[i]==lista_duration_sec[j] and
                    lista_version[i]==lista_version[j] and
                    # lista_inPort[i]==lista_inPort[j] and
                    lista_outPort[i]==lista_outPort[j]):
                    if (lista_actions[i] != lista_actions[j]):
                        arquivo_regras_conflitantes.write(
                            "("+ str(lista_prioridade[i]) + " ^ " + 
                            str(lista_hard_timeout_s[i]) + " ^ " + 
                            str(lista_byte_count[i]) + " ^ " + 
                            str(lista_idle_timeout_s[i]) + " ^ " + 
                            str(lista_duration_nsec[i]) + " ^ " + 
                            str(lista_packet_count[i]) + " ^ " + 
                            str(lista_duration_sec[i]) + " ^ " + 
                            str(lista_version[i]) + " ^ " + 
                            str(lista_table_id[i])+ " ^ " + 
                            # str(lista_inPort[i]) + " ^ " +
                            str(lista_outPort[i]) +
                            ") -> " + str(lista_actions[i]) + "\n")
                        arquivo_regras_conflitantes.write(" [Conflict detected between the rule " 
                            + str(i) + " and the rule " + str(j) + " in the switch "
                            + "00:00:00:00:00:00:00::0"+str(contSwitch+1) + "], ")
                        getConflictMessage(i,j,contSwitch)
                        flag_confRed = 1
                    else:
                        arquivo_regras_redundantes.write(
                            "("+ str(lista_prioridade[i]) + " ^ " + 
                            str(lista_hard_timeout_s[i]) + " ^ " + 
                            str(lista_byte_count[i]) + " ^ " + 
                            str(lista_idle_timeout_s[i]) + " ^ " + 
                            str(lista_duration_nsec[i]) + " ^ " + 
                            str(lista_packet_count[i]) + " ^ " + 
                            str(lista_duration_sec[i]) + " ^ " + 
                            str(lista_version[i]) + " ^ " + 
                            str(lista_table_id[i])+ " ^ " + 
                            # str(lista_inPort[i]) + " ^ " +
                            str(lista_outPort[i]) +
                            ") -> " + str(lista_actions[i]) + "\n")
                        arquivo_regras_redundantes.write(", [Redundancy detected between the rule " 
                            + str(i) + " and the rule " + str(j) + " in the switch "
                            + "00:00:00:00:00:00:00::0"+str(contSwitch+1) + "]")
                        getRedundancyMessage(i,j,contSwitch)
                        flag_confRed = 1
                j = j + 1
            i = i + 1
        
        n_flows += 1
        flowList.append(dicFlows)

    arquivo_regras.close()
    arquivo_regras_conflitantes.close()
    arquivo_regras_redundantes.close()

    arquivoDadosCSV = open("rest/api/data/arquivoDados.csv", "w")

    if flag_confRed != 1:
        print ("\nNenhum conflito e nenhuma redundancia foram encontrados!\n")

    arquivoDadosCSV.write("switch,flows\n")
    flowList.sort()
    for switch in flowList:
        arquivoDadosCSV.write(str(switch.keys()[0]) + "," + str(switch.values()[0])[1:-1] + "\n")

    arquivoDadosCSV.close()
    time_end = time.time()
    
    print("::: ", [fileId, time_end-time_init, n_flows])
    return [fileId, time_end-time_init, n_flows]

"""
Get conflicts within flowtable.
"""
def getConflictsFlowtable(verificationId, time_elapsed, n_flows):
    filename = "rest/api/data/conflicts_" + verificationId + ".txt"
    filesize = os.path.getsize(filename)
    if (0 == filesize):
        return {
            "status": "No conflicts detected for the current topology.",
            "time": time_elapsed,
            "n_flows": n_flows,
            "details": "No details available."
        }
    else:
        conflictsFile = open(filename, "r")
        return {
            "status": "Conflicts detected for the current topology.",
            "time": time_elapsed,
            "n_flows": n_flows,
            "details": conflictsFile.read()
        }

"""
Get redundancies within flowtable.
"""
def getRedundanciesFlowtable(verificationId, time_elapsed, n_flows):
    filename = "rest/api/data/redundancies_" + verificationId + ".txt"
    filesize = os.path.getsize(filename)
    if (0 == filesize):
        return {
            "status": "No redundancies detected for the current topology.",
            "time": time_elapsed,
            "n_flows": n_flows,
            "details": "No details available."
        }
    else:
        redundanciesFile = open(filename, "r")
        return {
            "status": "Redundancies detected for the current topology.",
            "time": time_elapsed,
            "n_flows": n_flows,
            "details": redundanciesFile.read()
        }

"""
Get whole flowtable.
"""
def getFlowtable(verificationId):
    filename = "rest/api/data/flowtable_" + verificationId + ".txt"
    filesize = os.path.getsize(filename)
    if (0 == filesize):
        return {"data": "Flowtable not found."}
    else:
        flowtableFile = open(filename, "r")
        return {"data": flowtableFile.read()}
