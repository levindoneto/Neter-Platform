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

arquivoFormatadoJsonVB = "../data/dataflow_formatoVB.json"
arquivoFormatadoJson = "../data/dataflow_formato.json"  # VB: Variable buffer

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


def getConflictMessage(flowCI, flowCJ, SwitchC):
    return "Conflict detected between the flow " + str(flowCI) \
        + " and the flow " + str(flowCJ) + " on the switch " + str(SwitchC)

def getRedundancyMessage(flowCI, flowCJ, SwitchC):
    return "Redundancy detected between the flow " + str(flowCI) \
        + " and the flow " + str(flowCJ) + " on the switch " + str(SwitchC)

def verifyFirewall():
    formatJson("rest/api/data/rulesFirewall.json")
    flag_confRedFW = 0

    string_firewall = ""
    fluxos_firewall = open("rest/api/data/rulesFirewall.json", "r")
    for f in fluxos_firewall:
        string_firewall += f
    fluxos_firewall.close()

    with open("rest/api/data/rulesFirewall.json") as fw:
        dataFW = fw.read()
        json_dataFW = json.loads(dataFW)

    list_switchesFW = json_dataFW.keys()
    fileRulesFW = open("rest/api/data/fileRulesFW.txt", "w")
    fileConflictsFW = open("rest/api/data/fileConflictsFW.txt", "w")
    fileRedundanciesFW = open("rest/api/data/fileRedundanciesFW.txt", "w")
    list_csvFW = []
    contSwitchFW = 0

    for sfw in list_switchesFW:
        dicFlowsFW = {}
        with open("rest/api/data/rulesFirewall.json") as fw:
            dataFW = fw.read()
            json_dataFW = json.loads(dataFW)
            print("json_dataFW \n", json_dataFW, "\n\n")
        json_dataFW = json_dataFW[str(sfw)]
        json_dataFW = json_dataFW["flows"]
        # flowtable_rules
        list_eth_src = []
        list_eth_dst = []
        list_eth_type = []
        list_in_port = []
        list_eth_vlan_vid = []
        list_eth_vlan_pcp = []
        list_ip_proto = []
        list_ipv4_src = []
        list_ipv4_dst = []
        list_ipv6_src = []
        list_ipv6_dst = []
        list_ipv6_label = []
        list_ip_tos = []
        list_ip_ecn = []
        list_ip_dscp = []
        list_tp_src = []
        list_tp_dst = []
        list_udp_src = []
        list_udp_dst = []
        list_tcp_src = []
        list_tcp_dst = []
        list_sctp_src = []
        list_sctp_dst = []
        list_icmpv4_type = []
        list_icmpv4_code = []
        list_icmpv6_type = []
        list_icmpv6_code = []
        list_ipv6_nd_ssl = []
        list_ipv6_nd_ttl = []
        list_ipv6_nd_target = []
        list_arp_opcode = []
        list_arp_tha = []
        list_arp_spa = []
        list_arp_tpa = []
        list_mpls_label = []
        list_mpls_tc = []
        list_mpls_bos = []
        list_tunnel_id = []
        list_metadata = []
        # firewall_rules
        list_version = []
        list_command = []
        list_cookie = []
        list_src_ip = []
        list_dst_ip = []
        list_dl_type = []
        list_nw_dst_prefix = []
        list_nw_src_prefix = []
        list_nw_src_maskbits = []
        list_nw_dst_maskbits = []
        list_any_nw_dst = []
        list_any_nw_proto = []
        list_any_in_port = []
        list_any_nw_srcany_tp_ds = []
        list_ruleid = []
        list_idleTimeoutSec = []
        list_hardTimeoutSec = []
        list_any_dl_type = []
        list_priority = []
        list_in_port = []
        list_any_dpid = []
        list_dl_src = []
        list_dpid = []
        list_tp_src = []
        list_any_dl_dst = []
        list_nw_proto = []
        list_tp_dst = []
        list_dl_dst = []
        list_any_tp_src = []
        list_outPort = []
        list_src_mac = []
        list_dst_mac = []
        list_action = []
        dicAuxFW = {}
        contFW = 0 # Indice do fluxo

        for durFW in json_dataFW[0:-1]:
            dicAuxFW = json_dataFW[contSwitchFW]

            # Informacoes apenas do Firewall
            if dicAuxFW.has_key('version') == True:
                list_version.append(str(json_dataFW[contFW]['version']))
            else:
                list_version.append("x")

            if dicAuxFW.has_key('command') == True:
                list_command.append(str(json_dataFW[contFW]['command']))
            else:
                list_command.append("x")

            if dicAuxFW.has_key('cookie') == True:
                list_cookie.append(str(json_dataFW[contFW]['cookie']))
            else:
                list_cookie.append("x")

            if dicAuxFW.has_key('src_ip') == True:
                list_src_ip.append(str(json_dataFW[contFW]['src_ip']))
            else:
                list_src_ip.append("x")

            if dicAuxFW.has_key('dst_ip') == True:
                list_dst_ip.append(str(json_dataFW[contFW]['dst_ip']))
            else:
                list_dst_ip.append("x")

            if dicAuxFW.has_key('dl_type') == True:
                list_dl_type.append(str(json_dataFW[contFW]['dl_type']))
            else:
                list_dl_type.append("x")

            if dicAuxFW.has_key('nw_dst_prefix') == True:
                list_nw_dst_prefix.append(str(json_dataFW[contFW]['nw_dst_prefix']))
            else:
                list_nw_dst_prefix.append("x")

            if dicAuxFW.has_key('nw_src_prefix') == True:
                list_nw_src_prefix.append(str(json_dataFW[contFW]['nw_src_prefix']))
            else:
                list_nw_src_prefix.append("x")

            if dicAuxFW.has_key('nw_src_maskbits') == True:
                list_nw_src_maskbits.append(str(json_dataFW[contFW]['nw_src_maskbits']))
            else:
                list_nw_src_maskbits.append("x")

            if dicAuxFW.has_key('nw_dst_maskbits') == True:
                list_nw_dst_maskbits.append(str(json_dataFW[contFW]['nw_dst_maskbits']))
            else:
                list_nw_dst_maskbits.append("x")

            if dicAuxFW.has_key('any_nw_dst') == True:
                list_any_nw_dst.append(str(json_dataFW[contFW]['any_nw_dst']))
            else:
                list_any_nw_dst.append("x")

            if dicAuxFW.has_key('any_nw_proto') == True:
                list_any_nw_proto.append(str(json_dataFW[contFW]['any_nw_proto']))
            else:
                list_any_nw_proto.append("x")

            if dicAuxFW.has_key('any_in_port') == True:
                list_any_in_port.append(str(json_dataFW[contFW]['any_in_port']))
            else:
                list_any_in_port.append("x")

            if dicAuxFW.has_key('any_nw_srcany_tp_ds') == True:
                list_any_nw_srcany_tp_ds.append(str(json_dataFW[contFW]['any_nw_srcany_tp_ds']))
            else:
                list_any_nw_srcany_tp_ds.append("x")

            if dicAuxFW.has_key('ruleid') == True:
                list_ruleid.append(str(json_dataFW[contFW]['ruleid']))
            else:
                list_ruleid.append("x")

            if dicAuxFW.has_key('idleTimeoutSec') == True:
                list_idleTimeoutSec.append(str(json_dataFW[contFW]['idleTimeoutSec']))
            else:
                list_idleTimeoutSec.append("x")

            if dicAuxFW.has_key('hardTimeoutSec') == True:
                list_hardTimeoutSec.append(str(json_dataFW[contFW]['hardTimeoutSec']))
            else:
                list_hardTimeoutSec.append("x")

            if dicAuxFW.has_key('any_dl_type') == True:
                list_any_dl_type.append(str(json_dataFW[contFW]['any_dl_type']))
            else:
                list_any_dl_type.append("x")

            if dicAuxFW.has_key('priority') == True:
                list_priority.append(str(json_dataFW[contFW]['priority']))
            else:
                list_priority.append("x")

            if dicAuxFW.has_key('in_port') == True:
                list_in_port.append(str(json_dataFW[contFW]['in_port']))
            else:
                list_in_port.append("x")

            if dicAuxFW.has_key('any_dpid') == True:
                list_any_dpid.append(str(json_dataFW[contFW]['any_dpid']))
            else:
                list_any_dpid.append("x")

            if dicAuxFW.has_key('dl_src') == True:
                list_dl_src.append(str(json_dataFW[contFW]['dl_src']))
            else:
                list_dl_src.append("x")

            if dicAuxFW.has_key('dpid') == True:
                list_dpid.append(str(json_dataFW[contFW]['dpid']))
            else:
                list_dpid.append("x")

            if dicAuxFW.has_key('tp_src') == True:
                list_tp_src.append(str(json_dataFW[contFW]['tp_src']))
            else:
                list_tp_src.append("x")

            if dicAuxFW.has_key('any_dl_dst') == True:
                list_any_dl_dst.append(str(json_dataFW[contFW]['any_dl_dst']))
            else:
                list_any_dl_dst.append("x")

            if dicAuxFW.has_key('nw_proto') == True:
                list_nw_proto.append(str(json_dataFW[contFW]['nw_proto']))
            else:
                list_nw_proto.append("x")

            if dicAuxFW.has_key('tp_dst') == True:
                list_tp_dst.append(str(json_dataFW[contFW]['tp_dst']))
            else:
                list_tp_dst.append("x")

            if dicAuxFW.has_key('dl_dst') == True:
                list_dl_dst.append(str(json_dataFW[contFW]['dl_dst']))
            else:
                list_dl_dst.append("x")

            if dicAuxFW.has_key('any_tp_src') == True:
                list_any_tp_src.append(str(json_dataFW[contFW]['any_tp_src']))
            else:
                list_any_tp_src.append("x")

            if dicAuxFW.has_key('outPort') == True:
                list_outPort.append(str(json_dataFW[contFW]['outPort']))
            else:
                list_outPort.append("x")

            if dicAuxFW.has_key('src_mac') == True:
                list_src_mac.append(str(json_dataFW[contFW]['src_mac']))
            else:
                list_src_mac.append("x")

            if dicAuxFW.has_key('dst_mac') == True:
                list_dst_mac.append(str(json_dataFW[contFW]['dst_mac']))
            else:
                list_dst_mac.append("x")

            if dicAuxFW.has_key('action') == True:
                list_action.append(str(json_dataFW[contFW]['action']))
            else:
                list_action.append("x")

            if dicAuxFW.has_key('match') == True:
                dicAuxFW = dicAuxFW["match"]
                print("\n\n\njson_dataFW[contFW]: ", json_dataFW[contFW], "\n\n\n")

                if dicAuxFW.has_key('eth_src') == True:
                    list_eth_src.append(str(json_dataFW[contFW]["match"]['eth_src']))
                else:
                    list_eth_src.append("x")

                if dicAuxFW.has_key('eth_dst') == True:
                    list_eth_dst.append(str(json_dataFW[contFW]["match"]['eth_dst']))
                else:
                    list_eth_dst.append("x")

                if dicAuxFW.has_key('eth_type') == True:
                    list_eth_type.append(str(json_dataFW[contFW]["match"]['eth_type']))
                else:
                    list_eth_type.append("x")

                if dicAuxFW.has_key('in_port') == True:
                    list_in_port.append(str(json_dataFW[contFW]["match"]['in_port']))
                else:
                    list_in_port.append("x")

                if dicAuxFW.has_key('eth_vlan_vid') == True:
                    list_eth_vlan_vid.append(str(json_dataFW[contFW]["match"]['eth_vlan_vid']))
                else:
                    list_eth_vlan_vid.append("x")

                if dicAuxFW.has_key('eth_vlan_pcp') == True:
                    list_eth_vlan_pcp.append(str(json_dataFW[contFW]["match"]['eth_vlan_pcp']))
                else:
                    list_eth_vlan_pcp.append("x")

                if dicAuxFW.has_key('ip_proto') == True:
                    list_ip_proto.append(str(json_dataFW[contFW]["match"]['ip_proto']))
                else:
                    list_ip_proto.append("x")

                if dicAuxFW.has_key('ipv4_src') == True:
                    list_ipv4_src.append(str(json_dataFW[contFW]["match"]['ipv4_src']))
                else:
                    list_ipv4_src.append("x")

                if dicAuxFW.has_key('ipv4_dst') == True:
                    list_ipv4_dst.append(str(json_dataFW[contFW]["match"]['ipv4_dst']))
                else:
                    list_ipv4_dst.append("x")

                if dicAuxFW.has_key('ipv6_src') == True:
                    list_ipv6_src.append(str(json_dataFW[contFW]["match"]['ipv6_src']))
                else:
                    list_ipv6_src.append("x")

                if dicAuxFW.has_key('ipv6_dst') == True:
                    list_ipv6_dst.append(str(json_dataFW[contFW]["match"]['ipv6_dst']))
                else:
                    list_ipv6_dst.append("x")

                if dicAuxFW.has_key('ipv6_label') == True:
                    list_ipv6_label.append(str(json_dataFW[contFW]["match"]['ipv6_label']))
                else:
                    list_ipv6_label.append("x")

                if dicAuxFW.has_key('ip_tos') == True:
                    list_ip_tos.append(str(json_dataFW[contFW]["match"]['ip_tos']))
                else:
                    list_ip_tos.append("x")

                if dicAuxFW.has_key('ip_ecn') == True:
                    list_ip_ecn.append(str(json_dataFW[contFW]["match"]['ip_ecn']))
                else:
                    list_ip_ecn.append("x")

                if dicAuxFW.has_key('ip_dscp') == True:
                    list_ip_dscp.append(str(json_dataFW[contFW]["match"]['ip_dscp']))
                else:
                    list_ip_dscp.append("x")

                if dicAuxFW.has_key('tp_src') == True:
                    list_tp_src.append(str(json_dataFW[contFW]["match"]['tp_src']))
                else:
                    list_tp_src.append("x")

                if dicAuxFW.has_key('tp_dst') == True:
                    list_tp_dst.append(str(json_dataFW[contFW]["match"]['tp_dst']))
                else:
                    list_tp_dst.append("x")

                if dicAuxFW.has_key('udp_src') == True:
                    list_udp_src.append(str(json_dataFW[contFW]["match"]['udp_src']))
                else:
                    list_udp_src.append("x")

                if dicAuxFW.has_key('udp_dst') == True:
                    list_udp_dst.append(str(json_dataFW[contFW]["match"]['udp_dst']))
                else:
                    list_udp_dst.append("x")

                if dicAuxFW.has_key('tcp_src') == True:
                    list_tcp_src.append(str(json_dataFW[contFW]["match"]['tcp_src']))
                else:
                    list_tcp_src.append("x")

                if dicAuxFW.has_key('tcp_dst') == True:
                    list_tcp_dst.append(str(json_dataFW[contFW]["match"]['tcp_dst']))
                else:
                    list_tcp_dst.append("x")

                if dicAuxFW.has_key('sctp_src') == True:
                    list_sctp_src.append(str(json_dataFW[contFW]["match"]['sctp_src']))
                else:
                    list_sctp_src.append("x")

                if dicAuxFW.has_key('sctp_dst') == True:
                    list_sctp_dst.append(str(json_dataFW[contFW]["match"]['sctp_dst']))
                else:
                    list_sctp_dst.append("x")

                if dicAuxFW.has_key('icmpv4_type') == True:
                    list_icmpv4_type.append(str(json_dataFW[contFW]["match"]['icmpv4_type']))
                else:
                    list_icmpv4_type.append("x")

                if dicAuxFW.has_key('icmpv4_code') == True:
                    list_icmpv4_code.append(str(json_dataFW[contFW]["match"]['icmpv4_code']))
                else:
                    list_icmpv4_code.append("x")

                if dicAuxFW.has_key('icmpv6_type') == True:
                    list_icmpv6_type.append(str(json_dataFW[contFW]["match"]['icmpv6_type']))
                else:
                    list_icmpv6_type.append("x")

                if dicAuxFW.has_key('icmpv6_code') == True:
                    list_icmpv6_code.append(str(json_dataFW[contFW]["match"]['icmpv6_code']))
                else:
                    list_icmpv6_code.append("x")

                if dicAuxFW.has_key('ipv6_nd_ssl') == True:
                    list_ipv6_nd_ssl.append(str(json_dataFW[contFW]["match"]['ipv6_nd_ssl']))
                else:
                    list_ipv6_nd_ssl.append("x")

                if dicAuxFW.has_key('arp_spa') == True:
                    list_arp_spa.append(str(json_dataFW[contFW]["match"]['arp_spa']))
                else:
                    list_arp_spa.append("x")

                if dicAuxFW.has_key('arp_tpa') == True:
                    list_arp_tpa.append(str(json_dataFW[contFW]["match"]['arp_tpa']))
                else:
                    list_arp_tpa.append("x")

                if dicAuxFW.has_key('ipv6_nd_target') == True:
                    list_ipv6_nd_target.append(str(json_dataFW[contFW]["match"]['ipv6_nd_target']))
                else:
                    list_ipv6_nd_target.append("x")

                if dicAuxFW.has_key('arp_opcode') == True:
                    list_arp_opcode.append(str(json_dataFW[contFW]["match"]['arp_opcode']))
                else:
                    list_arp_opcode.append("x")

                if dicAuxFW.has_key('arp_tha') == True:
                    list_arp_tha.append(str(json_dataFW[contFW]["match"]['arp_tha']))
                else:
                    list_arp_tha.append("x")

                if dicAuxFW.has_key('arp_spa') == True:
                    list_arp_spa.append(str(json_dataFW[contFW]["match"]['arp_spa']))
                else:
                    list_arp_spa.append("x")

                if dicAuxFW.has_key('arp_tpa') == True:
                    list_arp_tpa.append(str(json_dataFW[contFW]["match"]['arp_tpa']))
                else:
                    list_arp_tpa.append("x")

                if dicAuxFW.has_key('mpls_label') == True:
                    list_mpls_label.append(str(json_dataFW[contFW]["match"]['mpls_label']))
                else:
                    list_mpls_label.append("x")

                if dicAuxFW.has_key('mpls_tc') == True:
                    list_mpls_tc.append(str(json_dataFW[contFW]["match"]['mpls_tc']))
                else:
                    list_mpls_tc.append("x")

                if dicAuxFW.has_key('mpls_bos') == True:
                    list_mpls_bos.append(str(json_dataFW[contFW]["match"]['mpls_bos']))
                else:
                    list_mpls_bos.append("x")

                if dicAuxFW.has_key('tunnel_id') == True:
                    list_tunnel_id.append(str(json_dataFW[contFW]["match"]['tunnel_id']))
                else:
                    list_tunnel_id.append("x")

                if dicAuxFW.has_key('metadata') == True:
                    list_metadata.append(str(json_dataFW[contFW]["match"]['metadata']))
                else:
                    list_metadata.append("x")

                contFW += 1
            flowContFW = 0

        fileRulesFW.write("[Switch: " + str(contSwitchFW + 1) + "]\n")

        for mfw in range(contFW):
            fileRulesFW.write("(" + str(list_eth_src[flowContFW]) + " ^ " + str(list_eth_dst[flowContFW]) + " ^ " + str(list_eth_type[flowContFW]) + " ^ " + str(list_in_porteth_vlan_videth_vlan_pcp[flowContFW]) + " ^ " + str(list_ip_proto[flowContFW]) + " ^ " + str(list_ipv4_src[flowContFW]) + " ^ " + str(list_ipv4_dstipv6_src[flowContFW]) + " ^ " + str(list_ipv6_dst[flowContFW]) + " ^ " + str(list_ipv6_label[flowContFW]) + " ^ " + str(list_ip_tos[flowContFW]) + " ^ " + str(list_ip_ecn[flowContFW]) + " ^ " + str(list_ip_dscp[flowContFW]) + " ^ " + str(list_tp_src[flowContFW]) + " ^ " + str(list_tp_dst[flowContFW]) + " ^ " + str(list_udp_src[flowContFW]) + " ^ " + str(list_udp_dst[flowContFW]) + " ^ " + str(list_tcp_srctcp_dst[flowContFW]) + " ^ " + str(list_sctp_src[flowContFW]) + " ^ " + str(list_sctp_dst[flowContFW]) + " ^ " + str(list_icmpv4_type[flowContFW]) + " ^ " + str(list_icmpv4_code[flowContFW]) + " ^ " + str(list_icmpv6_type[flowContFW]) + " ^ " + str(list_icmpv6_code[flowContFW]) + " ^ " + str(list_ipv6_nd_ssl[flowContFW]) + " ^ " + str(list_ipv6_nd_ttl[flowContFW]) + " ^ " + str(list_arp_tpa[flowContFW]) + " ^ " + str(list_ipv6_nd_target[flowContFW]) + " ^ " + str(list_arp_opcode[flowContFW]) + " ^ " + str(list_arp_tha[flowContFW]) + " ^ " + str(list_arp_spa[flowContFW]) + " ^ " + str(list_arp_tpaipv6_label[flowContFW]) + " ^ " + str(list_ip_tos[flowContFW]) + " ^ " + str(list_ip_ecn[flowContFW]) + " ^ " + str(list_ip_dscp[flowContFW]) + " ^ " + str(list_tp_src[flowContFW]) + " ^ " + str(list_tp_dst[flowContFW]) + " ^ " + str(list_udp_src[flowContFW]) + " ^ " + str(list_udp_dst[flowContFW]) + " ^ " + str(list_tcp_src[flowContFW]) + " ^ " + str(list_tcp_dst[flowContFW]) + " ^ " + str(list_sctp_src[flowContFW]) + " ^ " + str(list_sctp_dst[flowContFW]) + " ^ " + str(list_icmpv4_type[flowContFW]) + " ^ " + str(list_icmpv4_code[flowContFW]) + " ^ " + str(list_icmpv6_type[flowContFW]) + " ^ " + str(list_icmpv6_code[flowContFW]) + " ^ " + str(list_ipv6_nd_ssl[flowContFW]) + " ^ " + str(list_ipv6_nd_ttl[flowContFW]) + " ^ " + str(list_ipv6_nd_target[flowContFW]) + " ^ " + str(list_arp_opcode[flowContFW]) + " ^ " + str(list_arp_tha[flowContFW]) + " ^ " + str(list_arp_spa[flowContFW]) + " ^ " + str(list_arp_tpa[flowContFW]) + " ^ " + str(list_mpls_label[flowContFW]) + " ^ " + str(list_mpls_tc[flowContFW]) + " ^ " + str(list_mpls_bos[flowContFW]) + " ^ " + str(list_tunnel_id[flowContFW]) + " ^ " + str(list_metadata[flowContFW]) + " ^ " + str(list_version[flowContFW]) + " ^ " + str(list_command[flowContFW]) + " ^ " + str(list_cookie[flowContFW]) + " ^ " + str(list_src_ip[flowContFW]) + " ^ " + str(list_dst_ip[flowContFW]) + " ^ " + str(list_dl_type[flowContFW]) + " ^ " + str(list_nw_dst_prefix[flowContFW]) + " ^ " + str(list_nw_src_prefix[flowContFW]) + " ^ " + str(list_nw_src_maskbits[flowContFW]) + " ^ " + str(list_nw_dst_maskbits[flowContFW]) + " ^ " + str(list_any_nw_dst[flowContFW]) + " ^ " + str(list_any_nw_proto[flowContFW]) + " ^ " + str(list_any_in_port[flowContFW]) + " ^ " + str(list_any_nw_srcany_tp_ds[flowContFW]) + " ^ " + str(list_ruleid[flowContFW]) + " ^ " + str(list_idleTimeoutSec[flowContFW]) + " ^ " + str(list_hardTimeoutSec[flowContFW]) + " ^ " + str(list_any_dl_type[flowContFW]) + " ^ " + str(list_priority[flowContFW]) + " ^ " + str(list_in_port[flowContFW]) + " ^ " + str(list_any_dpid[flowContFW]) + " ^ " + str(list_dl_src[flowContFW]) + " ^ " + str(list_dpid[flowContFW]) + " ^ " + str(list_tp_src[flowContFW]) + " ^ " + str(list_any_dl_dst[flowContFW]) + " ^ " + str(list_nw_proto[flowContFW]) + " ^ " + str(list_tp_dst[flowContFW]) + " ^ " + str(list_dl_dst[flowContFW]) + " ^ " + str(list_any_tp_src[flowContFW]) + " ^ " + str(list_outPort[flowContFW]) + " ^ " + str(list_src_mac[flowContFW]) + " ^ " + str(list_dst_mac[flowContFW]) + " ^ " + ") -> " + str(list_action[flowContFW]) + "\n")
            dicFlowsFW.update({str(mfw):[list_eth_src[flowContFW], list_eth_dst[flowContFW], list_eth_type[flowContFW], list_in_porteth_vlan_videth_vlan_pcp[flowContFW], list_ip_proto[flowContFW], list_ipv4_src[flowContFW], list_ipv4_dstipv6_src[flowContFW], list_ipv6_dst[flowContFW], list_ipv6_label[flowContFW], list_ip_tos[flowContFW], list_ip_ecn[flowContFW], list_ip_dscp[flowContFW], list_tp_src[flowContFW], list_tp_dst[flowContFW], list_udp_src[flowContFW], list_udp_dst[flowContFW], list_tcp_srctcp_dst[flowContFW], list_sctp_src[flowContFW], list_sctp_dst[flowContFW], list_icmpv4_type[flowContFW], list_icmpv4_code[flowContFW], list_icmpv6_type[flowContFW], list_icmpv6_code[flowContFW], list_ipv6_nd_ssl[flowContFW], list_ipv6_nd_ttl[flowContFW], list_arp_tpa[flowContFW], list_ipv6_nd_target[flowContFW], list_arp_opcode[flowContFW], list_arp_tha[flowContFW], list_arp_spa[flowContFW], list_arp_tpaipv6_label[flowContFW], list_ip_tos[flowContFW], list_ip_ecn[flowContFW], list_ip_dscp[flowContFW], list_tp_src[flowContFW], list_tp_dst[flowContFW], list_udp_src[flowContFW], list_udp_dst[flowContFW], list_tcp_src[flowContFW], list_tcp_dst[flowContFW], list_sctp_src[flowContFW], list_sctp_dst[flowContFW], list_icmpv4_type[flowContFW], list_icmpv4_code[flowContFW], list_icmpv6_type[flowContFW], list_icmpv6_code[flowContFW], list_ipv6_nd_ssl[flowContFW], list_ipv6_nd_ttl[flowContFW], list_ipv6_nd_target[flowContFW], list_arp_opcode[flowContFW], list_arp_tha[flowContFW], list_arp_spa[flowContFW], list_arp_tpa[flowContFW], list_mpls_label[flowContFW], list_mpls_tc[flowContFW], list_mpls_bos[flowContFW], list_tunnel_id[flowContFW], list_metadata[flowContFW], list_[flowContFW], list_version[flowContFW], list_command[flowContFW], list_cookie[flowContFW], list_src_ip[flowContFW], list_dst_ip[flowContFW], list_dl_type[flowContFW], list_nw_dst_prefix[flowContFW], list_nw_src_prefix[flowContFW], list_nw_src_maskbits[flowContFW], list_nw_dst_maskbits[flowContFW], list_any_nw_dst[flowContFW], list_any_nw_proto[flowContFW], list_any_in_port[flowContFW], list_any_nw_srcany_tp_ds[flowContFW], list_ruleid[flowContFW], list_idleTimeoutSec[flowContFW], list_hardTimeoutSec[flowContFW], list_any_dl_type[flowContFW], list_priority[flowContFW], list_in_port[flowContFW], list_any_dpid[flowContFW], list_dl_src[flowContFW], list_dpid[flowContFW], list_tp_src[flowContFW], list_any_dl_dst[flowContFW], list_nw_proto[flowContFW], list_tp_dst[flowContFW], list_dl_dst[flowContFW], list_any_tp_src[flowContFW], list_outPort[flowContFW], list_src_mac[flowContFW], list_dst_mac[flowContFW], list_action[flowContFW]]})
            flowContFW += 1
        fileRulesFW.write("\n\n")
        contSwitchFW += 1

        # Verification Algorithm
        ifw = 0
        jfw = 0
        for lfw in range(len(list_actions) - 1):
            jfw = ifw + 1
            for kfw in range(len(list_actions) - (ifw + 1)):
                if (list_eth_src[ifw] == "x"):
                    list_eth_src[ifw] = list_eth_src[jfw]
                if (list_eth_dst[ifw] == "x"):
                    list_eth_dst[ifw] = list_eth_dst[jfw]
                if (list_eth_type[ifw] == "x"):
                    list_eth_type[ifw] = list_eth_type[jfw]
                if (list_in_port[ifw] == "x"):
                    list_in_port[ifw] = list_in_port[jfw]
                if (lista_eth_vlan_vid[ifw] == "x"):
                    lista_eth_vlan_vid[ifw] = lista_eth_vlan_pcp[jfw]
                if (lista_eth_vlan_pcp[ifw] == "x"):
                    lista_eth_vlan_pcp[ifw] = lista_eth_vlan_pcp[jfw]
                if (list_ip_proto[ifw] == "x"):
                    list_ip_proto[ifw] = list_ip_proto[jfw]
                if (list_ipv4_src[ifw] == "x"):
                    list_ipv4_src[ifw] = list_ipv4_src[jfw]
                if (list_ipv4_dstipv6_src[ifw] == "x"):
                    list_ipv4_dstipv6_src[ifw] = list_ipv4_dstipv6_src[jfw]
                if (list_ipv6_dst[ifw] == "x"):
                    list_ipv6_dst[ifw] = list_ipv6_dst[jfw]
                if (list_ipv6_label[ifw] == "x"):
                    list_ipv6_label[ifw] = list_ipv6_label[jfw]
                if (list_ip_tos[ifw] == "x"):
                    list_ip_tos[ifw] = list_ip_tos[jfw]
                if (list_ip_ecn[ifw] == "x"):
                    list_ip_ecn[ifw] = list_ip_ecn[jfw]
                if (list_ip_dscp[ifw] == "x"):
                    list_ip_dscp[ifw] = list_ip_dscp[jfw]
                if (list_tp_src[ifw] == "x"):
                    list_tp_src[ifw] = list_tp_src[jfw]
                if (list_tp_dst[ifw] == "x"):
                    list_tp_dst[ifw] = list_tp_dst[jfw]
                if (list_udp_src[ifw] == "x"):
                    list_udp_src[ifw] = list_udp_src[jfw]
                if (list_udp_dst[ifw] == "x"):
                    list_udp_dst[ifw] = list_udp_dst[jfw]
                if (list_tcp_srctcp_dst[ifw] == "x"):
                    list_tcp_srctcp_dst[ifw] = list_tcp_srctcp_dst[jfw]
                if (list_sctp_src[ifw] == "x"):
                    list_sctp_src[ifw] = list_sctp_src[jfw]
                if (list_sctp_dst[ifw] == "x"):
                    list_sctp_dst[ifw] = list_sctp_dst[jfw]
                if (list_icmpv4_type[ifw] == "x"):
                    list_icmpv4_type[ifw] = list_icmpv4_type[jfw]
                if (list_icmpv4_code[ifw] == "x"):
                    list_icmpv4_code[ifw] = list_icmpv4_code[jfw]
                if (list_icmpv6_type[ifw] == "x"):
                    list_icmpv6_type[ifw] = list_icmpv6_type[jfw]
                if (list_icmpv6_code[ifw] == "x"):
                    list_icmpv6_code[ifw] = list_icmpv6_code[jfw]
                if (list_ipv6_nd_ssl[ifw] == "x"):
                    list_ipv6_nd_ssl[ifw] = list_ipv6_nd_ssl[jfw]
                if (list_ipv6_nd_ttl[ifw] == "x"):
                    list_ipv6_nd_ttl[ifw] = list_ipv6_nd_ttl[jfw]
                if (list_arp_tpa[ifw] == "x"):
                    list_arp_tpa[ifw] = list_arp_tpa[jfw]
                if (list_ipv6_nd_target[ifw] == "x"):
                    list_ipv6_nd_target[ifw] = list_ipv6_nd_target[jfw]
                if (list_arp_opcode[ifw] == "x"):
                    list_arp_opcode[ifw] = list_arp_opcode[jfw]
                if (list_arp_tha[ifw] == "x"):
                    list_arp_tha[ifw] = list_arp_tha[jfw]
                if (list_arp_spa[ifw] == "x"):
                    list_arp_spa[ifw] = list_arp_spa[jfw]
                if (list_arp_tpaipv6_label[ifw] == "x"):
                    list_arp_tpaipv6_label[ifw] = list_arp_tpaipv6_label[jfw]
                if (list_ip_tos[ifw] == "x"):
                    list_ip_tos[ifw] = list_ip_tos[jfw]
                if (list_ip_ecn[ifw] == "x"):
                    list_ip_ecn[ifw] = list_ip_ecn[jfw]
                if (list_ip_dscp[ifw] == "x"):
                    list_ip_dscp[ifw] = list_ip_dscp[jfw]
                if (list_tp_src[ifw] == "x"):
                    list_tp_src[ifw] = list_tp_src[jfw]
                if (list_tp_dst[ifw] == "x"):
                    list_tp_dst[ifw] = list_tp_dst[jfw]
                if (list_udp_src[ifw] == "x"):
                    list_udp_src[ifw] = list_udp_src[jfw]
                if (list_udp_dst[ifw] == "x"):
                    list_udp_dst[ifw] = list_udp_dst[jfw]
                if (list_tcp_src[ifw] == "x"):
                    list_tcp_src[ifw] = list_tcp_src[jfw]
                if (list_tcp_dst[ifw] == "x"):
                    list_tcp_dst[ifw] = list_tcp_dst[jfw]
                if (list_sctp_src[ifw] == "x"):
                    list_sctp_src[ifw] = list_sctp_src[jfw]
                if (list_sctp_dst[ifw] == "x"):
                    list_sctp_dst[ifw] = list_sctp_dst[jfw]
                if (list_icmpv4_type[ifw] == "x"):
                    list_icmpv4_type[ifw] = list_icmpv4_type[jfw]
                if (list_icmpv4_code[ifw] == "x"):
                    list_icmpv4_code[ifw] = list_icmpv4_code[jfw]
                if (list_icmpv6_type[ifw] == "x"):
                    list_icmpv6_type[ifw] = list_icmpv6_type[jfw]
                if (list_icmpv6_code[ifw] == "x"):
                    list_icmpv6_code[ifw] = list_icmpv6_code[jfw]
                if (list_ipv6_nd_ssl[ifw] == "x"):
                    list_ipv6_nd_ssl[ifw] = list_ipv6_nd_ssl[jfw]
                if (list_ipv6_nd_ttl[ifw] == "x"):
                    list_ipv6_nd_ttl[ifw] = list_ipv6_nd_ttl[jfw]
                if (list_ipv6_nd_target[ifw] == "x"):
                    list_ipv6_nd_target[ifw] = list_ipv6_nd_target[jfw]
                if (list_arp_opcode[ifw] == "x"):
                    list_arp_opcode[ifw] = list_arp_opcode[jfw]
                if (list_arp_tha[ifw] == "x"):
                    list_arp_tha[ifw] = list_arp_tha[jfw]
                if (list_arp_spa[ifw] == "x"):
                    list_arp_spa[ifw] = list_arp_spa[jfw]
                if (list_arp_tpa[ifw] == "x"):
                    list_arp_tpa[ifw] = list_arp_tpa[jfw]
                if (list_mpls_label[ifw] == "x"):
                    list_mpls_label[ifw] = list_mpls_label[jfw]
                if (list_mpls_tc[ifw] == "x"):
                    list_mpls_tc[ifw] = list_mpls_tc[jfw]
                if (list_mpls_bos[ifw] == "x"):
                    list_mpls_bos[ifw] = list_mpls_bos[jfw]
                if (list_tunnel_id[ifw] == "x"):
                    list_tunnel_id[ifw] = list_tunnel_id[jfw]
                if (list_metadata[ifw] == "x"):
                    list_metadata[ifw] = list_metadata[jfw]
                if (list_[ifw] == "x"):
                    list_[ifw] = list_[jfw]
                if (list_version[ifw] == "x"):
                    list_version[ifw] = list_version[jfw]
                if (list_command[ifw] == "x"):
                    list_command[ifw] = list_command[jfw]
                if (list_cookie[ifw] == "x"):
                    list_cookie[ifw] = list_cookie[jfw]
                if (list_src_ip[ifw] == "x"):
                    list_src_ip[ifw] = list_src_ip[jfw]
                if (list_dst_ip[ifw] == "x"):
                    list_dst_ip[ifw] = list_dst_ip[jfw]
                if (list_dl_type[ifw] == "x"):
                    list_dl_type[ifw] = list_dl_type[jfw]
                if (list_nw_dst_prefix[ifw] == "x"):
                    list_nw_dst_prefix[ifw] = list_nw_dst_prefix[jfw]
                if (list_nw_src_prefix[ifw] == "x"):
                    list_nw_src_prefix[ifw] = list_nw_src_prefix[jfw]
                if (list_nw_src_maskbits[ifw] == "x"):
                    list_nw_src_maskbits[ifw] = list_nw_src_maskbits[jfw]
                if (list_nw_dst_maskbits[ifw] == "x"):
                    list_nw_dst_maskbits[ifw] = list_nw_dst_maskbits[jfw]
                if (list_any_nw_dst[ifw] == "x"):
                    list_any_nw_dst[ifw] = list_any_nw_dst[jfw]
                if (list_any_nw_proto[ifw] == "x"):
                    list_any_nw_proto[ifw] = list_any_nw_proto[jfw]
                if (list_any_in_port[ifw] == "x"):
                    list_any_in_port[ifw] = list_any_in_port[jfw]
                if (list_any_nw_srcany_tp_ds[ifw] == "x"):
                    list_any_nw_srcany_tp_ds[ifw] = list_any_nw_srcany_tp_ds[jfw]
                if (list_ruleid[ifw] == "x"):
                    list_ruleid[ifw] = list_ruleid[jfw]
                if (list_idleTimeoutSec[ifw] == "x"):
                    list_idleTimeoutSec[ifw] = list_idleTimeoutSec[jfw]
                if (list_hardTimeoutSec[ifw] == "x"):
                    list_hardTimeoutSec[ifw] = list_hardTimeoutSec[jfw]
                if (list_any_dl_type[ifw] == "x"):
                    list_any_dl_type[ifw] = list_any_dl_type[jfw]
                if (list_priority[ifw] == "x"):
                    list_priority[ifw] = list_priority[jfw]
                if (list_in_port[ifw] == "x"):
                    list_in_port[ifw] = list_in_port[jfw]
                if (list_any_dpid[ifw] == "x"):
                    list_any_dpid[ifw] = list_any_dpid[jfw]
                if (list_dl_src[ifw] == "x"):
                    list_dl_src[ifw] = list_dl_src[jfw]
                if (list_dpid[ifw] == "x"):
                    list_dpid[ifw] = list_dpid[jfw]
                if (list_tp_src[ifw] == "x"):
                    list_tp_src[ifw] = list_tp_src[jfw]
                if (list_any_dl_dst[ifw] == "x"):
                    list_any_dl_dst[ifw] = list_any_dl_dst[jfw]
                if (list_nw_proto[ifw] == "x"):
                    list_nw_proto[ifw] = list_nw_proto[jfw]
                if (list_tp_dst[ifw] == "x"):
                    list_tp_dst[ifw] = list_tp_dst[jfw]
                if (list_dl_dst[ifw] == "x"):
                    list_dl_dst[ifw] = list_dl_dst[jfw]
                if (list_any_tp_src[ifw] == "x"):
                    list_any_tp_src[ifw] = list_any_tp_src[jfw]
                if (list_outPort[ifw] == "x"):
                    list_outPort[ifw] = list_outPort[jfw]
                if (list_src_mac[ifw] == "x"):
                    list_src_mac[ifw] = list_src_mac[jfw]
                if (list_dst_mac[ifw] == "x"):
                    list_dst_mac[ifw] = list_dst_mac[jfw]
                if (list_action[ifw] == "x"):
                    list_action[ifw] = list_action[jfw]

                if(True):#list_eth_src[ifw]==list_eth_src[jfw] and list_eth_dst[ifw]==list_eth_dst[jfw] and list_eth_type[ifw]==list_eth_type[jfw] and list_in_porteth_vlan_videth_vlan_pcp[ifw]==list_in_porteth_vlan_videth_vlan_pcp[jfw] and list_ip_proto[ifw]==list_ip_proto[jfw] and list_ipv4_src[ifw]==list_ipv4_src[jfw] and list_ipv4_dstipv6_src[ifw]==list_ipv4_dstipv6_src[jfw] and list_ipv6_dst[ifw]==list_ipv6_dst[jfw] and list_ipv6_label[ifw]==list_ipv6_label[jfw] and list_ip_tos[ifw]==list_ip_tos[jfw] and list_ip_ecn[ifw]==list_ip_ecn[jfw] and list_ip_dscp[ifw]==list_ip_dscp[jfw] and list_tp_src[ifw]==list_tp_src[jfw] and list_tp_dst[ifw]==list_tp_dst[jfw] and list_udp_src[ifw]==list_udp_src[jfw] and list_udp_dst[ifw]==list_udp_dst[jfw] and list_tcp_srctcp_dst[ifw]==list_tcp_srctcp_dst[jfw] and list_sctp_src[ifw]==list_sctp_src[jfw] and list_sctp_dst[ifw]==list_sctp_dst[jfw] and list_icmpv4_type[ifw]==list_icmpv4_type[jfw] and list_icmpv4_code[ifw]==list_icmpv4_code[jfw] and list_icmpv6_type[ifw]==list_icmpv6_type[jfw] and list_icmpv6_code[ifw]==list_icmpv6_code[jfw] and list_ipv6_nd_ssl[ifw]==list_ipv6_nd_ssl[jfw] and list_ipv6_nd_ttl[ifw]==list_ipv6_nd_ttl[jfw] and list_arp_tpa[ifw]==list_arp_tpa[jfw] and list_ipv6_nd_target[ifw]==list_ipv6_nd_target[jfw] and list_arp_opcode[ifw]==list_arp_opcode[jfw] and list_arp_tha[ifw]==list_arp_tha[jfw] and list_arp_spa[ifw]==list_arp_spa[jfw] and list_arp_tpaipv6_label[ifw]==list_arp_tpaipv6_label[jfw] and list_ip_tos[ifw]==list_ip_tos[jfw] and list_ip_ecn[ifw]==list_ip_ecn[jfw] and list_ip_dscp[ifw]==list_ip_dscp[jfw] and list_tp_src[ifw]==list_tp_src[jfw] and list_tp_dst[ifw]==list_tp_dst[jfw] and list_udp_src[ifw]==list_udp_src[jfw] and list_udp_dst[ifw]==list_udp_dst[jfw] and list_tcp_src[ifw]==list_tcp_src[jfw] and list_tcp_dst[ifw]==list_tcp_dst[jfw] and list_sctp_src[ifw]==list_sctp_src[jfw] and list_sctp_dst[ifw]==list_sctp_dst[jfw] and list_icmpv4_type[ifw]==list_icmpv4_type[jfw] and list_icmpv4_code[ifw]==list_icmpv4_code[jfw] and list_icmpv6_type[ifw]==list_icmpv6_type[jfw] and list_icmpv6_code[ifw]==list_icmpv6_code[jfw] and list_ipv6_nd_ssl[ifw]==list_ipv6_nd_ssl[jfw] and list_ipv6_nd_ttl[ifw]==list_ipv6_nd_ttl[jfw] and list_ipv6_nd_target[ifw]==list_ipv6_nd_target[jfw] and list_arp_opcode[ifw]==list_arp_opcode[jfw] and list_arp_tha[ifw]==list_arp_tha[jfw] and list_arp_spa[ifw]==list_arp_spa[jfw] and list_arp_tpa[ifw]==list_arp_tpa[jfw] and list_mpls_label[ifw]==list_mpls_label[jfw] and list_mpls_tc[ifw]==list_mpls_tc[jfw] and list_mpls_bos[ifw]==list_mpls_bos[jfw] and list_tunnel_id[ifw]==list_tunnel_id[jfw] and list_metadata[ifw]==list_metadata[jfw] and list_[ifw]==list_[jfw] and list_version[ifw]==list_version[jfw] and list_command[ifw]==list_command[jfw] and list_cookie[ifw]==list_cookie[jfw] and list_src_ip[ifw]==list_src_ip[jfw] and list_dst_ip[ifw]==list_dst_ip[jfw] and list_dl_type[ifw]==list_dl_type[jfw] and list_nw_dst_prefix[ifw]==list_nw_dst_prefix[jfw] and list_nw_src_prefix[ifw]==list_nw_src_prefix[jfw] and list_nw_src_maskbits[ifw]==list_nw_src_maskbits[jfw] and list_nw_dst_maskbits[ifw]==list_nw_dst_maskbits[jfw] and list_any_nw_dst[ifw]==list_any_nw_dst[jfw] and list_any_nw_proto[ifw]==list_any_nw_proto[jfw] and list_any_in_port[ifw]==list_any_in_port[jfw] and list_any_nw_srcany_tp_ds[ifw]==list_any_nw_srcany_tp_ds[jfw] and list_ruleid[ifw]==list_ruleid[jfw] and list_idleTimeoutSec[ifw]==list_idleTimeoutSec[jfw] and list_hardTimeoutSec[ifw]==list_hardTimeoutSec[jfw] and list_any_dl_type[ifw]==list_any_dl_type[jfw] and list_priority[ifw]==list_priority[jfw] and list_in_port[ifw]==list_in_port[jfw] and list_any_dpid[ifw]==list_any_dpid[jfw] and list_dl_src[ifw]==list_dl_src[jfw] and list_dpid[ifw]==list_dpid[jfw] and list_tp_src[ifw]==list_tp_src[jfw] and list_any_dl_dst[ifw]==list_any_dl_dst[jfw] and list_nw_proto[ifw]==list_nw_proto[jfw] and list_tp_dst[ifw]==list_tp_dst[jfw] and list_dl_dst[ifw]==list_dl_dst[jfw] and list_any_tp_src[ifw]==list_any_tp_src[jfw] and list_outPort[ifw]==list_outPort[jfw] and list_src_mac[ifw]==list_src_mac[jfw] and list_dst_mac[ifw]==list_dst_mac[jfw]):
                    if(list_action[ifw] == list_action[jfw]):
                        fileConflictsFW.write("(" + str(list_eth_src[ifw]) + " ^ " + str(list_eth_dst[ifw]) + " ^ " + str(list_eth_type[ifw]) + " ^ " + str(list_in_porteth_vlan_videth_vlan_pcp[ifw]) + " ^ " + str(list_ip_proto[ifw]) + " ^ " + str(list_ipv4_src[ifw]) + " ^ " + str(list_ipv4_dstipv6_src[ifw]) + " ^ " + str(list_ipv6_dst[ifw]) + " ^ " + str(list_ipv6_label[ifw]) + " ^ " + str(list_ip_tos[ifw]) + " ^ " + str(list_ip_ecn[ifw]) + " ^ " + str(list_ip_dscp[ifw]) + " ^ " + str(list_tp_src[ifw]) + " ^ " + str(list_tp_dst[ifw]) + " ^ " + str(list_udp_src[ifw]) + " ^ " + str(list_udp_dst[ifw]) + " ^ " + str(list_tcp_srctcp_dst[ifw]) + " ^ " + str(list_sctp_src[ifw]) + " ^ " + str(list_sctp_dst[ifw]) + " ^ " + str(list_icmpv4_type[ifw]) + " ^ " + str(list_icmpv4_code[ifw]) + " ^ " + str(list_icmpv6_type[ifw]) + " ^ " + str(list_icmpv6_code[ifw]) + " ^ " + str(list_ipv6_nd_ssl[ifw]) + " ^ " + str(list_ipv6_nd_ttl[ifw]) + " ^ " + str(list_arp_tpa[ifw]) + " ^ " + str(list_ipv6_nd_target[ifw]) + " ^ " + str(list_arp_opcode[ifw]) + " ^ " + str(list_arp_tha[ifw]) + " ^ " + str(list_arp_spa[ifw]) + " ^ " + str(list_arp_tpaipv6_label[ifw]) + " ^ " + str(list_ip_tos[ifw]) + " ^ " + str(list_ip_ecn[ifw]) + " ^ " + str(list_ip_dscp[ifw]) + " ^ " + str(list_tp_src[ifw]) + " ^ " + str(list_tp_dst[ifw]) + " ^ " + str(list_udp_src[ifw]) + " ^ " + str(list_udp_dst[ifw]) + " ^ " + str(list_tcp_src[ifw]) + " ^ " + str(list_tcp_dst[ifw]) + " ^ " + str(list_sctp_src[ifw]) + " ^ " + str(list_sctp_dst[ifw]) + " ^ " + str(list_icmpv4_type[ifw]) + " ^ " + str(list_icmpv4_code[ifw]) + " ^ " + str(list_icmpv6_type[ifw]) + " ^ " + str(list_icmpv6_code[ifw]) + " ^ " + str(list_ipv6_nd_ssl[ifw]) + " ^ " + str(list_ipv6_nd_ttl[ifw]) + " ^ " + str(list_ipv6_nd_target[ifw]) + " ^ " + str(list_arp_opcode[ifw]) + " ^ " + str(list_arp_tha[ifw]) + " ^ " + str(list_arp_spa[ifw]) + " ^ " + str(list_arp_tpa[ifw]) + " ^ " + str(list_mpls_label[ifw]) + " ^ " + str(list_mpls_tc[ifw]) + " ^ " + str(list_mpls_bos[ifw]) + " ^ " + str(list_tunnel_id[ifw]) + " ^ " + str(list_metadata[ifw]) + " ^ " + str(list_[ifw]) + " ^ " + str(list_version[ifw]) + " ^ " + str(list_command[ifw]) + " ^ " + str(list_cookie[ifw]) + " ^ " + str(list_src_ip[ifw]) + " ^ " + str(list_dst_ip[ifw]) + " ^ " + str(list_dl_type[ifw]) + " ^ " + str(list_nw_dst_prefix[ifw]) + " ^ " + str(list_nw_src_prefix[ifw]) + " ^ " + str(list_nw_src_maskbits[ifw]) + " ^ " + str(list_nw_dst_maskbits[ifw]) + " ^ " + str(list_any_nw_dst[ifw]) + " ^ " + str(list_any_nw_proto[ifw]) + " ^ " + str(list_any_in_port[ifw]) + " ^ " + str(list_any_nw_srcany_tp_ds[ifw]) + " ^ " + str(list_ruleid[ifw]) + " ^ " + str(list_idleTimeoutSec[ifw]) + " ^ " + str(list_hardTimeoutSec[ifw]) + " ^ " + str(list_any_dl_type[ifw]) + " ^ " + str(list_priority[ifw]) + " ^ " + str(list_in_port[ifw]) + " ^ " + str(list_any_dpid[ifw]) + " ^ " + str(list_dl_src[ifw]) + " ^ " + str(list_dpid[ifw]) + " ^ " + str(list_tp_src[ifw]) + " ^ " + str(list_any_dl_dst[ifw]) + " ^ " + str(list_nw_proto[ifw]) + " ^ " + str(list_tp_dst[ifw]) + " ^ " + str(list_dl_dst[ifw]) + " ^ " + str(list_any_tp_src[ifw]) + " ^ " + str(list_outPort[ifw]) + " ^ " + str(list_src_mac[ifw]) + " ^ " + str(list_dst_mac[ifw]) + ") -> " + str(list_actions[ifw]) + "\n")
                        fileConflictsFW.write(getConflictMessage(ifw, jfw, contSwitchFW) + "\n\n")
                        logger.info(getRedundancyMessage(ifw, jfw, contSwitchFW))
                    else:
                        fileRedundanciesFW.write("(" + str(list_eth_src[ifw]) + " ^ " + str(list_eth_dst[ifw]) + " ^ " + str(list_eth_type[ifw]) + " ^ " + str(list_in_porteth_vlan_videth_vlan_pcp[ifw]) + " ^ " + str(list_ip_proto[ifw]) + " ^ " + str(list_ipv4_src[ifw]) + " ^ " + str(list_ipv4_dstipv6_src[ifw]) + " ^ " + str(list_ipv6_dst[ifw]) + " ^ " + str(list_ipv6_label[ifw]) + " ^ " + str(list_ip_tos[ifw]) + " ^ " + str(list_ip_ecn[ifw]) + " ^ " + str(list_ip_dscp[ifw]) + " ^ " + str(list_tp_src[ifw]) + " ^ " + str(list_tp_dst[ifw]) + " ^ " + str(list_udp_src[ifw]) + " ^ " + str(list_udp_dst[ifw]) + " ^ " + str(list_tcp_srctcp_dst[ifw]) + " ^ " + str(list_sctp_src[ifw]) + " ^ " + str(list_sctp_dst[ifw]) + " ^ " + str(list_icmpv4_type[ifw]) + " ^ " + str(list_icmpv4_code[ifw]) + " ^ " + str(list_icmpv6_type[ifw]) + " ^ " + str(list_icmpv6_code[ifw]) + " ^ " + str(list_ipv6_nd_ssl[ifw]) + " ^ " + str(list_ipv6_nd_ttl[ifw]) + " ^ " + str(list_arp_tpa[ifw]) + " ^ " + str(list_ipv6_nd_target[ifw]) + " ^ " + str(list_arp_opcode[ifw]) + " ^ " + str(list_arp_tha[ifw]) + " ^ " + str(list_arp_spa[ifw]) + " ^ " + str(list_arp_tpaipv6_label[ifw]) + " ^ " + str(list_ip_tos[ifw]) + " ^ " + str(list_ip_ecn[ifw]) + " ^ " + str(list_ip_dscp[ifw]) + " ^ " + str(list_tp_src[ifw]) + " ^ " + str(list_tp_dst[ifw]) + " ^ " + str(list_udp_src[ifw]) + " ^ " + str(list_udp_dst[ifw]) + " ^ " + str(list_tcp_src[ifw]) + " ^ " + str(list_tcp_dst[ifw]) + " ^ " + str(list_sctp_src[ifw]) + " ^ " + str(list_sctp_dst[ifw]) + " ^ " + str(list_icmpv4_type[ifw]) + " ^ " + str(list_icmpv4_code[ifw]) + " ^ " + str(list_icmpv6_type[ifw]) + " ^ " + str(list_icmpv6_code[ifw]) + " ^ " + str(list_ipv6_nd_ssl[ifw]) + " ^ " + str(list_ipv6_nd_ttl[ifw]) + " ^ " + str(list_ipv6_nd_target[ifw]) + " ^ " + str(list_arp_opcode[ifw]) + " ^ " + str(list_arp_tha[ifw]) + " ^ " + str(list_arp_spa[ifw]) + " ^ " + str(list_arp_tpa[ifw]) + " ^ " + str(list_mpls_label[ifw]) + " ^ " + str(list_mpls_tc[ifw]) + " ^ " + str(list_mpls_bos[ifw]) + " ^ " + str(list_tunnel_id[ifw]) + " ^ " + str(list_metadata[ifw]) + " ^ " + str(list_[ifw]) + " ^ " + str(list_version[ifw]) + " ^ " + str(list_command[ifw]) + " ^ " + str(list_cookie[ifw]) + " ^ " + str(list_src_ip[ifw]) + " ^ " + str(list_dst_ip[ifw]) + " ^ " + str(list_dl_type[ifw]) + " ^ " + str(list_nw_dst_prefix[ifw]) + " ^ " + str(list_nw_src_prefix[ifw]) + " ^ " + str(list_nw_src_maskbits[ifw]) + " ^ " + str(list_nw_dst_maskbits[ifw]) + " ^ " + str(list_any_nw_dst[ifw]) + " ^ " + str(list_any_nw_proto[ifw]) + " ^ " + str(list_any_in_port[ifw]) + " ^ " + str(list_any_nw_srcany_tp_ds[ifw]) + " ^ " + str(list_ruleid[ifw]) + " ^ " + str(list_idleTimeoutSec[ifw]) + " ^ " + str(list_hardTimeoutSec[ifw]) + " ^ " + str(list_any_dl_type[ifw]) + " ^ " + str(list_priority[ifw]) + " ^ " + str(list_in_port[ifw]) + " ^ " + str(list_any_dpid[ifw]) + " ^ " + str(list_dl_src[ifw]) + " ^ " + str(list_dpid[ifw]) + " ^ " + str(list_tp_src[ifw]) + " ^ " + str(list_any_dl_dst[ifw]) + " ^ " + str(list_nw_proto[ifw]) + " ^ " + str(list_tp_dst[ifw]) + " ^ " + str(list_dl_dst[ifw]) + " ^ " + str(list_any_tp_src[ifw]) + " ^ " + str(list_outPort[ifw]) + " ^ " + str(list_src_mac[ifw]) + " ^ " + str(list_dst_mac[ifw]) + ") -> " + str(list_actions[ifw]) + "\n")
                        fileRedundanciesFW.write(getRedundancyMessage(ifw, jfw, contSwitchFW) + "\n\n")
                        logger.info(getRedundancyMessage(ifw, jfw, contSwitchFW))
                    flag_confRedFW = 1
            jfw += 1
        ifw += 1
    fileRulesFW.close()
    fileConflictsFW.close()
    fileRedundanciesFW.close()
    list_csvFW.append(dicFlowsFW)
    fwDataFile = open("rest/api/data/fwDataFile.csv", "w")

    if flag_confRed != 1:
        return {"status": "No conflict or redundancy found"}

    for rfw in range(len(list_csvFW)):
        dicAux_CSV = list_csvFW[r]
        for nfw in range(len(list_csvFW[r])):
            fwDataFile.write(str(dicAux_CSVFW[str(nfw)]) + "\n")
        fwDataFile.write("\n")

    fwDataFile.close()
    return True

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

    lista_switches = json_data.keys()
    print (lista_switches)

    # Arquivos de regras
    arquivo_regras = open("../data/regras.txt", "w")
    arquivo_regras_conflitantes = open("../data/regras_conflitantes.txt", "w")
    arquivo_regras_redundantes = open("../data/regras_redundantes.txt", "w")

    lista_csv = []                                    # Lista para armazenar os dicionarios que serao impressos no arquivo .csv
    contSwitch = 0
    for s in lista_switches:
        dicFlows = {}                             #Inicia/limpa dicFlows a cada execucao
        # Tabela com os fluxos sendo as linhas e as informacoes sendo as colunas
        with open(arquivoFormatadoJsonVB) as f:
            data = f.read()
            json_data = json.loads(data)

        try:
            json_data = json_data[str(s)] # Tem que salvar isso no nome do switch
            json_data = json_data["flows"]
        except:
            pass







    return True

