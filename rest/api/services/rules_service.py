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

    arquivo_regras = open("rest/api/data/regras.txt", "w")
    arquivo_regras_conflitantes = open("rest/api/data/regras_conflitantes.txt", "w")
    arquivo_regras_redundantes = open("rest/api/data/regras_redundantes.txt", "w")

    flowList = []

    contSwitch = 0
    lista_switches.sort()
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
        
        # verification
        if json_data[0].has_key('priority') == True:
            lista_prioridade.append(json_data[0]['priority'])
        else:
            lista_prioridade.append("x") # wildcard
        if json_data[0].has_key('hard_timeout_s') == True:
            lista_hard_timeout_s.append(str(json_data[0]['hard_timeout_s']))
        else:
            lista_hard_timeout_s.append("x") # wildcard
        
        if json_data[0].has_key('byte_count') == True:
            lista_byte_count.append(str(json_data[0]['byte_count']))
        else:
            lista_byte_count.append("x") # wildcard
        
        if json_data[0].has_key('idle_timeout_s') == True:
            lista_idle_timeout_s.append(str(json_data[0]['idle_timeout_s']))
        else:
            lista_idle_timeout_s.append("x") # wildcard
        
        if json_data[0].has_key('duration_nsec') == True:
            lista_duration_nsec.append(str(json_data[0]['duration_nsec']))
        else:
            lista_duration_nsec.append("x") # wildcard
        
        if json_data[0].has_key('packet_count') == True:
            lista_packet_count.append(str(json_data[0]['packet_count']))
        else:
            lista_packet_count.append("x") # wildcard
        
        if json_data[0].has_key('duration_sec') == True:
            lista_duration_sec.append(str(json_data[0]['duration_sec']))
        else:
            lista_duration_sec.append("x") # wildcard
        
        if json_data[0].has_key('version') == True:
            lista_version.append(str(json_data[0]['version']))
        else:
            lista_version.append("x") # wildcard
        
        if json_data[0].has_key('table_id') == True:
            lista_table_id.append(str(json_data[0]['table_id']))
        else:
            lista_table_id.append("x") # wildcard

        if json_data[0].has_key('instructions') == True:
            lista_actions.append(str(json_data[0]['instructions']['instruction_apply_actions']['actions']))
        else:
            lista_actions.append("x")

        if json_data[0].has_key('durationSeconds') == True:
            lista_duracao.append(str(json_data[0]['durationSeconds']))
        else:
            lista_duracao.append("x")

        if json_data[0].has_key('byteCount') == True:
            lista_byteCount.append(str(json_data[0]['byteCount']))
        else:
            lista_byteCount.append("x")

        if json_data[0].has_key('packetCount') == True:
            lista_packetCount.append(str(json_data[0]['packetCount']))
        else:
            lista_packetCount.append("x")

        if json_data[0].has_key('cookie') == True:
            lista_cookie.append(str(json_data[0]['cookie']))
        else:
            lista_cookie.append("x")

        if json_data[0].has_key('match') == True:
            json_data[0] = json_data[0]["match"]

            if json_data[0].has_key('eth_src') == True:
                lista_ethSrc.append(str(json_data[0]['match']['eth_src']))
            else:
                lista_ethSrc.append("x")

            if json_data[0].has_key('eth_dst') == True:
                lista_ethDst.append(str(json_data[0]['match']['eth_dst']))
            else:
                lista_ethDst.append("x")

            if json_data[0].has_key('eth_type') == True:
                lista_ethType.append(str(json_data[0]['match']['eth_type']))
            else:
                lista_ethType.append("x")

            if json_data[0].has_key('in_port') == True:
                lista_inPort.append(str(json_data[0]['match']['in_port']))
            else:
                lista_inPort.append("x")

            if json_data[0].has_key('eth_vlan_vid') == True:
                lista_eth_vlan_vid.append(str(json_data[0]['match']['eth_vlan_vid']))
            else:
                lista_eth_vlan_vid.append("x")

            if json_data[0].has_key('eth_vlan_pcp') == True:
                lista_eth_vlan_pcp.append(str(json_data[0]['match']['eth_vlan_pcp']))
            else:
                lista_eth_vlan_pcp.append("x")

            if json_data[0].has_key('ip_proto') == True:
                lista_ip_proto.append(str(json_data[0]['match']['ip_proto']))
            else:
                lista_ip_proto.append("x")

            if json_data[0].has_key('lista_ipv4_src') == True:
                lista_ipv4_src.append(str(json_data[0]['match']['lista_ipv4_src']))
            else:
                lista_ipv4_src.append("x")

            if json_data[0].has_key('lista_ipv4_dst') == True:
                lista_ipv4_dst.append(str(json_data[0]['match']['lista_ipv4_dst']))
            else:
                lista_ipv4_dst.append("x")

            if json_data[0].has_key('lista_ipv6_src') == True:
                lista_ipv6_src.append(str(json_data[0]['match']['lista_ipv6_src']))
            else:
                lista_ipv6_src.append("x")

            if json_data[0].has_key('lista_ipv6_dst') == True:
                lista_ipv6_dst.append(str(json_data[0]['match']['lista_ipv6_dst']))
            else:
                lista_ipv6_dst.append("x")

            if json_data[0].has_key('ipv6_label') == True:
                lista_ipv6_label.append(str(json_data[0]['match']['ipv6_label']))
            else:
                lista_ipv6_label.append("x")

            if json_data[0].has_key('ip_tos') == True:
                lista_ip_tos.append(str(json_data[0]['match']['ip_tos']))
            else:
                lista_ip_tos.append("x")

            if json_data[0].has_key('ip_ecn') == True:
                lista_ip_ecn.append(str(json_data[0]['match']['ip_ecn']))
            else:
                lista_ip_ecn.append("x")

            if json_data[0].has_key('ip_dscp') == True:
                lista_ip_dscp.append(str(json_data[0]['match']['ip_dscp']))
            else:
                lista_ip_dscp.append("x")

            if json_data[0].has_key('tp_src') == True:
                lista_tp_src.append(str(json_data[0]['match']['tp_src']))
            else:
                lista_tp_src.append("x")

            if json_data[0].has_key('tp_dst') == True:
                lista_tp_dst.append(str(json_data[0]['match']['tp_dst']))
            else:
                lista_tp_dst.append("x")

            if json_data[0].has_key('udp_src') == True:
                lista_udp_src.append(str(json_data[0]['match']['udp_src']))
            else:
                lista_udp_src.append("x")

            if json_data[0].has_key('udp_dst') == True:
                lista_udp_dst.append(str(json_data[0]['match']['udp_dst']))
            else:
                lista_udp_dst.append("x")

            if json_data[0].has_key('tcp_src') == True:
                lista_tcp_src.append(str(json_data[0]['match']['tcp_src']))
            else:
                lista_tcp_src.append("x")

            if json_data[0].has_key('tcp_dst') == True:
                lista_tcp_dst.append(str(json_data[0]['match']['tcp_dst']))
            else:
                lista_tcp_dst.append("x")

            if json_data[0].has_key('sctp_src') == True:
                lista_sctp_src.append(str(json_data[0]['match']['sctp_src']))
            else:
                lista_sctp_src.append("x")

            if json_data[0].has_key('sctp_dst') == True:
                lista_sctp_dst.append(str(json_data[0]['match']['sctp_dst']))
            else:
                lista_sctp_dst.append("x")

            if json_data[0].has_key('icmpv4_type') == True:
                lista_icmpv4_type.append(str(json_data[0]['match']['icmpv4_type']))
            else:
                lista_icmpv4_type.append("x")
            if json_data[0].has_key('icmpv4_code') == True:
                lista_icmpv4_code.append(str(json_data[0]['match']['icmpv4_code']))
            else:
                lista_icmpv4_code.append("x")
            if json_data[0].has_key('icmpv6_type') == True:
                lista_icmpv6_type.append(str(json_data[0]['match']['icmpv6_type']))
            else:
                lista_icmpv6_type.append("x")

            if json_data[0].has_key('icmpv6_code') == True:
                lista_icmpv6_code.append(str(json_data[0]['match']['icmpv6_code']))
            else:
                lista_icmpv6_code.append("x")

            if json_data[0].has_key('ipv6_nd_ssl') == True:
                lista_ipv6_nd_ssl .append(str(json_data[0]['match']['ipv6_nd_ssl']))
            else:
                lista_ipv6_nd_ssl .append("x")

            if json_data[0].has_key('ipv6_nd_ttl') == True:
                lista_ipv6_nd_ttl.append(str(json_data[0]['match']['ipv6_nd_ttl']))
            else:
                lista_ipv6_nd_ttl.append("x")

            if json_data[0].has_key('ipv6_nd_target') == True:
                lista_ipv6_nd_target.append(str(json_data[0]['match']['ipv6_nd_target']))
            else:
                lista_ipv6_nd_target.append("x")

            if json_data[0].has_key('arp_opcode') == True:
                lista_arp_opcode.append(str(json_data[0]['match']['arp_opcode']))
            else:
                lista_arp_opcode.append("x")

            if json_data[0].has_key('arp_tha') == True:
                lista_arp_tha.append(str(json_data[0]['match']['arp_tha']))
            else:
                lista_arp_tha.append("x")

            if json_data[0].has_key('arp_spa') == True:
                lista_arp_spa.append(str(json_data[0]['match']['arp_spa']))
            else:
                lista_arp_spa.append("x")

            if json_data[0].has_key('arp_tpa') == True:
                lista_arp_tpa.append(str(json_data[0]['match']['arp_tpa']))
            else:
                lista_arp_tpa.append("x")

            if json_data[0].has_key('mpls_label') == True:
                lista_mpls_label.append(str(json_data[0]['match']['mpls_label']))
            else:
                lista_mpls_label.append("x")

            if json_data[0].has_key('mpls_tc') == True:
                lista_mpls_tc.append(str(json_data[0]['match']['mpls_tc']))
            else:
                lista_mpls_tc.append("x")

            if json_data[0].has_key('mpls_bos') == True:
                lista_mpls_bos.append(str(json_data[0]['match']['mpls_bos']))
            else:
                lista_mpls_bos.append("x")

            if json_data[0].has_key('tunnel_id') == True:
                lista_tunnel_id.append(str(json_data[0]['match']['tunnel_id']))
            else:
                lista_tunnel_id.append("x")

            if json_data[0].has_key('metadata') == True:
                lista_metadata.append(str(json_data[0]['match']['metadata']))
            else:
                lista_metadata.append("x")

        # cont += 1

        m = 0 # Flow Index
        arquivo_regras.write("[Switch: " + s + "]\n")
        # for m in range(len(lista_switches)):
        print("lista_ethDst[m]: ", m, lista_ethDst[m])
        arquivo_regras.write("("+ str(lista_prioridade[m]) + " ^ " + str(lista_hard_timeout_s[m]) + " ^ " + str(lista_byte_count[m]) + " ^ " + str(lista_idle_timeout_s[m]) + " ^ " + str(lista_duration_nsec[m]) + " ^ " + str(lista_packet_count[m]) + " ^ " + str(lista_duration_sec[m]) + " ^ " + str(lista_version[m]) + " ^ " + str(lista_table_id[m])+str(lista_ethSrc[m]) + " ^ " + str(lista_ethDst[m]) + " ^ " + str(lista_ethType[m]) + " ^ " + str(lista_inPort[m]) + " ^ " + str(lista_eth_vlan_vid[m]) + " ^ " + str(lista_eth_vlan_pcp[m]) + " ^ " + str(lista_ip_proto[m]) + " ^ " + str(lista_ipv4_src[m]) + " ^ " + str(lista_ipv4_dst[m]) + " ^ " + str(lista_ipv6_src[m]) + " ^ " + str(lista_ipv6_dst[m]) + " ^ " + str(lista_ipv6_label[m]) + " ^ " + str(lista_ip_tos[m]) + " ^ " + str(lista_ip_ecn[m]) + " ^ " + str(lista_ip_dscp[m]) + " ^ " + str(lista_tp_src[m]) + " ^ " + str(lista_tp_dst[m]) + " ^ " + str(lista_udp_src[m]) + " ^ " + str(lista_udp_dst[m]) + " ^ " + str(lista_tcp_src[m]) + " ^ " + str(lista_tcp_dst[m]) + " ^ " + str(lista_sctp_src[m]) + " ^ " + str(lista_sctp_dst[m]) + " ^ " + str(lista_icmpv4_type[m]) + " ^ " + str(lista_icmpv4_code[m]) + " ^ " + str(lista_icmpv6_type[m]) + " ^ " + str(lista_icmpv6_code[m]) + " ^ " + str(lista_ipv6_nd_ssl[m]) + " ^ " + str(lista_ipv6_nd_ttl[m]) + " ^ " + str(lista_ipv6_nd_target[m]) + " ^ " + str(lista_arp_opcode[m]) + " ^ " + str(lista_arp_opcode[m]) + " ^ " + str(lista_arp_tha[m]) + " ^ " + str(lista_arp_spa[m]) + " ^ " + str(lista_arp_tpa[m]) + " ^ " + str(lista_mpls_label[m]) + " ^ " + str(lista_mpls_tc[m]) + " ^ " + str(lista_mpls_bos[m]) + " ^ " + str(lista_tunnel_id[m]) + " ^ " + str(lista_metadata[m]) + ") -> " + str(lista_actions[m]) + "\n")
        dicFlows.update({s:[lista_prioridade[m],lista_hard_timeout_s[m],lista_byte_count[m],lista_idle_timeout_s[m],lista_duration_nsec[m],lista_packet_count[m],lista_duration_sec[m],lista_version[m],lista_table_id[m]]})
        m += 1
        arquivo_regras.write("\n\n")
        i = 0
        j = 0

        for l in range(len(lista_actions)-1):
            j = i + 1
            for k in range(len(lista_actions)-(i+1)):
                if (lista_ethSrc[i]=='x'):
                    lista_ethSrc[i] = lista_ethSrc[j]
                if (lista_ethDst[i]=='x'):
                    lista_Dst[i] = lista_Dst[j]
                if (lista_ethType[i]=='x'):
                    lista_ethType[i] = lista_ethType[j]
                if (lista_inPort[i]=='x'):
                    lista_inPort[i] = lista_inPort[j]
                if (lista_eth_vlan_vid[i]=='x'):
                    lista_eth_vlan_vid[i] = lista_eth_vlan_vid[j]
                if (lista_eth_vlan_pcp[i]=='x'):
                    lista_eth_vlan_pcp[i] = lista_eth_vlan_pcp[j] 
                if (lista_ip_proto[i]=='x'):
                    lista_ip_proto[i] = lista_ip_proto[j]
                if (lista_ipv4_src[i]=='x'):
                    lista_ipv4_src[i] = lista_ipv4_src[j]
                if (lista_ipv4_dst[i]=='x'):
                    lista_ipv4_dst[i] = lista_ipv4_dst[j]
                if (lista_ipv6_src[i]=='x'):
                    lista_ipv6_src[i] = lista_ipv6_src[j]
                if (lista_ipv6_dst[i]=='x'):
                    lista_ipv6_dst[i] = lista_ipv6_dst[j]
                if (lista_ipv6_label[i]=='x'):
                    lista_ipv6_label[i] = lista_ipv6_label[j]
                if (lista_ip_tos[i]=='x'):
                    lista_ip_tos[i] = lista_ip_tos[j]
                if (lista_ip_ecn[i]=='x'):
                    lista_ip_ecn[i] = lista_ip_ecn[j]
                if (lista_ip_dscp[i]=='x'):
                    lista_ip_dscp[i] = lista_ip_dscp[j]
                if (lista_tp_src[i]=='x'):
                    lista_tp_src[i] = lista_tp_src[j]
                if (lista_tp_dst[i]=='x'):
                    lista_tp_dst[i] = lista_tp_dst[j]
                if (lista_udp_src[i]=='x'):
                    lista_udp_src[i] = lista_udp_src[j]
                if (lista_udp_dst[i]=='x'):
                    lista_udp_dst[i] = lista_udp_dst[j]
                if (lista_tcp_src[i]=='x'):
                    lista_tcp_src[i] = lista_tcp_src[j]
                if (lista_tcp_dst[i]=='x'):
                    lista_tcp_dst[i] = lista_tcp_dst[j]
                if (lista_sctp_src[i]=='x'):
                    lista_sctp_src[i] = lista_sctp_src[j]
                if (lista_sctp_dst[i]=='x'):
                    lista_sctp_dst[i] = lista_sctp_dst[j]
                if (lista_icmpv4_type[i]=='x'):
                    lista_icmpv4_type[i] = lista_icmpv4_type[j]
                if (lista_icmpv4_code[i]=='x'):
                    lista_icmpv4_code[i] = lista_icmpv4_code[j]
                if (lista_icmpv6_type[i]=='x'):
                    lista_icmpv6_type[i] = lista_icmpv6_type[j]
                if (lista_icmpv6_code[i]=='x'):
                    lista_icmpv6_code[i] = lista_icmpv6_code[j]
                if (lista_ipv6_nd_ssl[i]=='x'):
                    lista_ipv6_nd_ssl[i] = lista_ipv6_nd_ssl[j]
                if (lista_ipv6_nd_ttl[i]=='x'):
                    lista_ipv6_nd_ttl[i] = lista_ipv6_nd_ttl[j]
                if (lista_ipv6_nd_target[i]=='x'):
                    lista_ipv6_nd_target[i] = lista_ipv6_nd_target[j]
                if (lista_arp_opcode[i]=='x'):
                    lista_arp_opcode[i] = lista_arp_opcode[j]
                if (lista_arp_opcode[i]=='x'):
                    lista_arp_opcode[i] = lista_arp_opcode[j]
                if (lista_arp_tha[i]=='x'):
                    lista_arp_tha[i] = lista_arp_tha[j]
                if (lista_arp_spa[i]=='x'):
                    lista_arp_spa[i] = lista_arp_spa[j]
                if (lista_arp_tpa[i]=='x'):
                    lista_arp_tpa[i] = lista_arp_tpa[j]
                if (lista_mpls_label[i]=='x'):
                    lista_mpls_label[i] = lista_mpls_label[j]
                if (lista_mpls_tc[i]=='x'):
                    lista_mpls_tc[i] = lista_mpls_tc[j]
                if (lista_mpls_bos[i]=='x'):
                    lista_mpls_bos[i] = lista_mpls_bos[j]
                if (lista_tunnel_id[i]=='x'):
                    lista_tunnel_id[i] = lista_tunnel_id[j]
                if (lista_metadata[i]=='x'):
                    lista_metadata[i] = lista_metadata[j]
                if (lista_actions[i]=='x'):
                    lista_actions[i] = lista_actions[j]
                if (lista_ethSrc[j]=='x'):
                    lista_ethSrc[j] = lista_ethSrc[i]
                if (lista_ethDst[j]=='x'):
                    lista_Dst[j] = lista_Dst[i]
                if (lista_ethType[j]=='x'):
                    lista_ethType[j] = lista_ethType[i]
                if (lista_inPort[j]=='x'):
                    lista_inPort[j] = lista_inPort[i]
                if (lista_eth_vlan_vid[j]=='x'):
                    lista_eth_vlan_vid[j] = lista_eth_vlan_vid[i]
                if (lista_eth_vlan_pcp[j]=='x'):
                    lista_eth_vlan_pcp[j] = lista_eth_vlan_pcp[i]
                if (lista_ip_proto[j]=='x'):
                    lista_ip_proto[j] = lista_ip_proto[i]
                if (lista_ipv4_src[j]=='x'):
                    lista_ipv4_src[j] = lista_ipv4_src[i]
                if (lista_ipv4_dst[j]=='x'):
                    lista_ipv4_dst[j] = lista_ipv4_dst[i]
                if (lista_ipv6_src[j]=='x'):
                    lista_ipv6_src[j] = lista_ipv6_src[i]
                if (lista_ipv6_dst[j]=='x'):
                    lista_ipv6_dst[j] = lista_ipv6_dst[i]
                if (lista_ipv6_label[j]=='x'):
                    lista_ipv6_label[j] = lista_ipv6_label[i]
                if (lista_ip_tos[j]=='x'):
                    lista_ip_tos[j] = lista_ip_tos[i]
                if (lista_ip_ecn[j]=='x'):
                    lista_ip_ecn[j] = lista_ip_ecn[i]
                if (lista_ip_dscp[j]=='x'):
                    lista_ip_dscp[j] = lista_ip_dscp[i]
                if (lista_tp_src[j]=='x'):
                    lista_tp_src[j] = lista_tp_src[i]
                if (lista_tp_dst[j]=='x'):
                    lista_tp_dst[j] = lista_tp_dst[i]
                if (lista_udp_src[j]=='x'):
                    lista_udp_src[j] = lista_udp_src[i]
                if (lista_udp_dst[j]=='x'):
                    lista_udp_dst[j] = lista_udp_dst[i]
                if (lista_tcp_src[j]=='x'):
                    lista_tcp_src[j] = lista_tcp_src[i]
                if (lista_tcp_dst[j]=='x'):
                    lista_tcp_dst[j] = lista_tcp_dst[i]
                if (lista_sctp_src[j]=='x'):
                    lista_sctp_src[j] = lista_sctp_src[i]
                if (lista_sctp_dst[j]=='x'):
                    lista_sctp_dst[j] = lista_sctp_dst[i]
                if (lista_icmpv4_type[j]=='x'):
                    lista_icmpv4_type[j] = lista_icmpv4_type[i]
                if (lista_icmpv4_code[j]=='x'):
                    lista_icmpv4_code[j] = lista_icmpv4_code[i]
                if (lista_icmpv6_type[j]=='x'):
                    lista_icmpv6_type[j] = lista_icmpv6_type[i]
                if (lista_icmpv6_code[j]=='x'):
                    lista_icmpv6_code[j] = lista_icmpv6_code[i]
                if (lista_ipv6_nd_ssl[j]=='x'):
                    lista_ipv6_nd_ssl[j] = lista_ipv6_nd_ssl[i]
                if (lista_ipv6_nd_ttl[j]=='x'):
                    lista_ipv6_nd_ttl[j] = lista_ipv6_nd_ttl[i]
                if (lista_ipv6_nd_target[j]=='x'):
                    lista_ipv6_nd_target[j] = lista_ipv6_nd_target[i]
                if (lista_arp_opcode[j]=='x'):
                    lista_arp_opcode[j] = lista_arp_opcode[i]
                if (lista_arp_opcode[j]=='x'):
                    lista_arp_opcode[j] = lista_arp_opcode[i]
                if (lista_arp_tha[j]=='x'):
                    lista_arp_tha[j] = lista_arp_tha[i]
                if (lista_arp_spa[j]=='x'):
                    lista_arp_spa[j] = lista_arp_spa[i]
                if (lista_arp_tpa[j]=='x'):
                    lista_arp_tpa[j] = lista_arp_tpa[i]
                if (lista_mpls_label[j]=='x'):
                    lista_mpls_label[j] = lista_mpls_label[i]
                if (lista_mpls_tc[j]=='x'):
                    lista_mpls_tc[j] = lista_mpls_tc[i]
                if (lista_mpls_bos[j]=='x'):
                    lista_mpls_bos[j] = lista_mpls_bos[i]
                if (lista_tunnel_id[j]=='x'):
                    lista_tunnel_id[j] = lista_tunnel_id[i]
                if (lista_metadata[j]=='x'):
                    lista_metadata[j] = lista_metadata[i]
                if (lista_actions[j]=='x'):
                    lista_actions[j] = lista_actions[i]
                if(lista_ethSrc[i]==lista_ethSrc[j] and lista_ethDst[i]==lista_ethDst[j] and lista_ethType[i]==lista_ethType[j] and lista_inPort[i]==lista_inPort[j] and lista_eth_vlan_vid[i]==lista_eth_vlan_vid[j] and lista_eth_vlan_pcp[i]==lista_eth_vlan_pcp[j] and lista_ip_proto[i]==lista_ip_proto[j] and lista_ipv4_src[i]==lista_ipv4_src[j] and lista_ipv4_dst[i]==lista_ipv4_dst[j] and lista_ipv6_src[i]==lista_ipv6_src[j] and lista_ipv6_dst[i]==lista_ipv6_dst[j] and lista_ipv6_label[i]==lista_ipv6_label[j] and lista_ip_tos[i]==lista_ip_tos[j] and lista_ip_ecn[i]==lista_ip_ecn[j] and lista_ip_dscp[i]==lista_ip_dscp[j] and lista_tp_src[i]==lista_tp_src[j] and lista_tp_dst[i]==lista_tp_dst[j] and lista_udp_src[i]==lista_udp_src[j] and lista_udp_dst[i]==lista_udp_dst[j] and lista_tcp_src[i]==lista_tcp_src[j] and lista_tcp_dst[i]==lista_tcp_dst[j] and lista_sctp_src[i]==lista_sctp_src[j] and lista_sctp_dst[i]==lista_sctp_dst[j] and lista_icmpv4_type[i]==lista_icmpv4_type[j] and lista_icmpv4_code[i]==lista_icmpv4_code[j] and lista_icmpv6_type[i]==lista_icmpv6_type[j] and lista_icmpv6_code[i]==lista_icmpv6_code[j] and lista_ipv6_nd_ssl[i]==lista_ipv6_nd_ssl[j] and  lista_ipv6_nd_ttl[i]==lista_ipv6_nd_ttl[j] and lista_ipv6_nd_target[i]==lista_ipv6_nd_target[j] and  lista_arp_opcode[i]==lista_arp_opcode[j] and lista_arp_tha[i]==lista_arp_tha[j] and  lista_arp_spa[i]==lista_arp_spa[j] and lista_arp_tpa[i]==lista_arp_tpa[j] and lista_mpls_label[i]==lista_mpls_label[j] and lista_mpls_tc[i]==lista_mpls_tc[j] and lista_mpls_bos[i]==lista_mpls_bos[j] and lista_tunnel_id[i]==lista_tunnel_id[j] and lista_metadata[i]==lista_metadata[j]):
                    if (lista_actions[i] != lista_actions[j]):
                        arquivo_regras_conflitantes.write("(" + str(lista_ethSrc[i]) + " ^ " + str(lista_ethDst[i]) + " ^ " + str(lista_eth_vlan_vid[i]) + " ^ " + str(lista_eth_vlan_pcp[i]) + " ^ " + str(lista_ip_proto[i]) + " ^ " + str(lista_ipv4_src[i]) + " ^ " + str(lista_ipv4_dst[i]) + " ^ " + str(lista_ipv6_src[i]) + " ^ " + str(lista_ipv6_dst[i]) + " ^ " + str(lista_ipv6_label[i]) + " ^ " + str(lista_ip_tos[i]) + " ^ " + str(lista_ip_ecn[i]) + " ^ " + str(lista_ip_dscp[i]) + " ^ " + str(lista_tp_src[i]) + " ^ " + str(lista_tp_dst[i]) + " ^ " + str(lista_udp_src[i]) + " ^ " + str(lista_udp_dst[i]) + " ^ " + str(lista_tcp_src[i]) + " ^ " + str(lista_tcp_dst[i]) + " ^ " + str(lista_sctp_src[i]) + " ^ " + str(lista_sctp_dst[i]) + " ^ " + str(lista_icmpv4_type[i]) + " ^ " + str(lista_icmpv4_code[i]) + " ^ " + str(lista_icmpv6_type[i]) + " ^ " + str(lista_icmpv6_code[i]) + " ^ " + str(lista_ipv6_nd_ssl[i]) + " ^ " + str(lista_ipv6_nd_ttl[i]) + " ^ " + str(lista_ipv6_nd_target[i]) + " ^ " + str(lista_arp_opcode[i]) + " ^ " + str(lista_arp_tha[i]) + " ^ " + str(lista_arp_spa[i]) + " ^ " + str(lista_arp_tpa[i]) + " ^ " + str(lista_mpls_label[i]) + " ^ " + str(lista_mpls_tc[i]) + " ^ " + str(lista_mpls_bos[i]) + " ^ " + str(lista_tunnel_id[i]) + " ^ " + str(lista_metadata[i]) + ") -> " + str(lista_actions[i]) + "\n")
                        arquivo_regras_conflitantes.write("Detectado conflito entre o fluxo " + str(i) + " e entre o fluxo " + str(j) + " no switch " + str(contSwitch) + "\n\n")
                        conflito(i,j,contSwitch)
                        flag_confRed = 1
                    else:
                        arquivo_regras_redundantes.write("(" + str(lista_ethSrc[i]) + " ^ " + str(lista_ethDst[i]) + " ^ " + str(lista_eth_vlan_vid[i]) + " ^ " + str(lista_eth_vlan_pcp[i]) + " ^ " + str(lista_ip_proto[i]) + " ^ " + str(lista_ipv4_src[i]) + " ^ " + str(lista_ipv4_dst[i]) + " ^ " + str(lista_ipv6_src[i]) + " ^ " + str(lista_ipv6_dst[i]) + " ^ " + str(lista_ipv6_label[i]) + " ^ " + str(lista_ip_tos[i]) + " ^ " + str(lista_ip_ecn[i]) + " ^ " + str(lista_ip_dscp[i]) + " ^ " + str(lista_tp_src[i]) + " ^ " + str(lista_tp_dst[i]) + " ^ " + str(lista_udp_src[i]) + " ^ " + str(lista_udp_dst[i]) + " ^ " + str(lista_tcp_src[i]) + " ^ " + str(lista_tcp_dst[i]) + " ^ " + str(lista_sctp_src[i]) + " ^ " + str(lista_sctp_dst[i]) + " ^ " + str(lista_icmpv4_type[i]) + " ^ " + str(lista_icmpv4_code[i]) + " ^ " + str(lista_icmpv6_type[i]) + " ^ " + str(lista_icmpv6_code[i]) + " ^ " + str(lista_ipv6_nd_ssl[i]) + " ^ " + str(lista_ipv6_nd_ttl[i]) + " ^ " + str(lista_ipv6_nd_target[i]) + " ^ " + str(lista_arp_opcode[i]) + " ^ " + str(lista_arp_tha[i]) + " ^ " + str(lista_arp_spa[i]) + " ^ " + str(lista_arp_tpa[i]) + " ^ " + str(lista_mpls_label[i]) + " ^ " + str(lista_mpls_tc[i]) + " ^ " + str(lista_mpls_bos[i]) + " ^ " + str(lista_tunnel_id[i]) + " ^ " + str(lista_metadata[i]) + ") -> " + str(lista_actions[i]) + "\n")
                        arquivo_regras_redundantes.write("Detectada a redundancia acima entre o fluxo " + str(i) + " e entre o fluxo " + str(j) + " no switch " + str(contSwitch) + "\n\n")
                        redundancia(i,j,contSwitch)
                        flag_confRed = 1
                j = j + 1
            i = i + 1

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
    return True

def getConflictsFlowtable(verificationId):
    filename = "rest/api/data/conflicts_" + verificationId
    filesize = os.path.getsize(filename)
    if (0 == filesize):
        return {"status": "No conflicts detected for the current topology"}
    else:
        conflictsFile = open(filename, "r")
        return {"status": conflictsFile.read()}

