#!/usr/bin/env python

import logging
import os
import sys
import json
from os import system
import time
from helpers import json_methods as jsonMethods

logger = logging.getLogger("conflicts")
logging.basicConfig(level = logging.INFO)

#-> Informações - Match - Flowtable
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
#-> Informações - Match - Firewall
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

def getConflictMessage(flowCI, flowCJ, SwitchC):
    return "Conflict detected between the flow " + str(flowCI) \
        + " and the flow " + str(flowCJ) + " on the switch " + str(SwitchC)

def getRedundancyMessage(flowCI, flowCJ, SwitchC):
    return "Redundancy detected between the flow " + str(flowCI) \
        + " and the flow " + str(flowCJ) + " on the switch " + str(SwitchC)

def verifyFlowtable():
    #jsonMethods.formatJson("../data/rulesFirewall.json", "arquivoJsonFW")
    flag_confRedFW = 0

    string_firewall = ""
    fluxos_firewall = open("../data/rulesFirewall.json", "r")
    for f in fluxos_firewall:
        string_firewall += f
    fluxos_firewall.close()

    with open("../data/rulesFirewall.json") as fw:
        dataFW = fw.read()
        json_dataFW = json.loads(dataFW)

    list_switchesFW = json_dataFW.keys()
    fileRulesFW = open("../data/fileRulesFW.txt", "w")
    fileConflictsFW = open("../data/fileConflictsFW.txt", "w")
    fileRedundanciesFW = open("../data/fileRedundanciesFW.txt", "w")
    list_csvFW = []
    contSwitchFW = 0

    for sfw in list_switchesFW:
        dicFlowsFW = {}
        with open("../data/rulesFirewall.json") as fw:
            dataFW = fw.read()
            json_dataFW = json.loads(dataFW)
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
            if dicAuxFW.has_key(list_versionlist_) == True:
                list_version.append(str(json_dataFW[contFW][list_versionlist_]))
            else:
                list_version.append("x")

            if dicAuxFW.has_key(list_commandlist_) == True:
                list_command.append(str(json_dataFW[contFW][list_commandlist_]))
            else:
                list_command.append("x")

            if dicAuxFW.has_key(list_cookielist_) == True:
                list_cookie.append(str(json_dataFW[contFW][list_cookielist_]))
            else:
                list_cookie.append("x")

            if dicAuxFW.has_key(list_src_iplist_) == True:
                list_src_ip.append(str(json_dataFW[contFW][list_src_iplist_]))
            else:
                list_src_ip.append("x")

            if dicAuxFW.has_key(list_dst_iplist_) == True:
                list_dst_ip.append(str(json_dataFW[contFW][list_dst_iplist_]))
            else:
                list_dst_ip.append("x")

            if dicAuxFW.has_key(list_dl_typelist_) == True:
                list_dl_type.append(str(json_dataFW[contFW][list_dl_typelist_]))
            else:
                list_dl_type.append("x")

            if dicAuxFW.has_key(list_nw_dst_prefixlist_) == True:
                list_nw_dst_prefix.append(str(json_dataFW[contFW][list_nw_dst_prefixlist_]))
            else:
                list_nw_dst_prefix.append("x")

            if dicAuxFW.has_key(list_nw_src_prefixlist_) == True:
                list_nw_src_prefix.append(str(json_dataFW[contFW][list_nw_src_prefixlist_]))
            else:
                list_nw_src_prefix.append("x")

            if dicAuxFW.has_key(list_nw_src_maskbitslist_) == True:
                list_nw_src_maskbits.append(str(json_dataFW[contFW][list_nw_src_maskbitslist_]))
            else:
                list_nw_src_maskbits.append("x")

            if dicAuxFW.has_key(list_nw_dst_maskbitslist_) == True:
                list_nw_dst_maskbits.append(str(json_dataFW[contFW][list_nw_dst_maskbitslist_]))
            else:
                list_nw_dst_maskbits.append("x")

            if dicAuxFW.has_key(list_any_nw_dstlist_) == True:
                list_any_nw_dst.append(str(json_dataFW[contFW][list_any_nw_dstlist_]))
            else:
                list_any_nw_dst.append("x")

            if dicAuxFW.has_key(list_any_nw_protolist_) == True:
                list_any_nw_proto.append(str(json_dataFW[contFW][list_any_nw_protolist_]))
            else:
                list_any_nw_proto.append("x")

            if dicAuxFW.has_key(list_any_in_portlist_) == True:
                list_any_in_port.append(str(json_dataFW[contFW][list_any_in_portlist_]))
            else:
                list_any_in_port.append("x")

            if dicAuxFW.has_key(list_any_nw_srcany_tp_dslist_) == True:
                list_any_nw_srcany_tp_ds.append(str(json_dataFW[contFW][list_any_nw_srcany_tp_dslist_]))
            else:
                list_any_nw_srcany_tp_ds.append("x")

            if dicAuxFW.has_key(list_ruleidlist_) == True:
                list_ruleid.append(str(json_dataFW[contFW][list_ruleidlist_]))
            else:
                list_ruleid.append("x")

            if dicAuxFW.has_key(list_idleTimeoutSeclist_) == True:
                list_idleTimeoutSec.append(str(json_dataFW[contFW][list_idleTimeoutSeclist_]))
            else:
                list_idleTimeoutSec.append("x")

            if dicAuxFW.has_key(list_hardTimeoutSeclist_) == True:
                list_hardTimeoutSec.append(str(json_dataFW[contFW][list_hardTimeoutSeclist_]))
            else:
                list_hardTimeoutSec.append("x")

            if dicAuxFW.has_key(list_any_dl_typelist_) == True:
                list_any_dl_type.append(str(json_dataFW[contFW][list_any_dl_typelist_]))
            else:
                list_any_dl_type.append("x")

            if dicAuxFW.has_key(list_prioritylist_) == True:
                list_priority.append(str(json_dataFW[contFW][list_prioritylist_]))
            else:
                list_priority.append("x")

            if dicAuxFW.has_key(list_in_portlist_) == True:
                list_in_port.append(str(json_dataFW[contFW][list_in_portlist_]))
            else:
                list_in_port.append("x")

            if dicAuxFW.has_key(list_any_dpidlist_) == True:
                list_any_dpid.append(str(json_dataFW[contFW][list_any_dpidlist_]))
            else:
                list_any_dpid.append("x")

            if dicAuxFW.has_key(list_dl_srclist_) == True:
                list_dl_src.append(str(json_dataFW[contFW][list_dl_srclist_]))
            else:
                list_dl_src.append("x")

            if dicAuxFW.has_key(list_dpidlist_) == True:
                list_dpid.append(str(json_dataFW[contFW][list_dpidlist_]))
            else:
                list_dpid.append("x")

            if dicAuxFW.has_key(list_tp_srclist_) == True:
                list_tp_src.append(str(json_dataFW[contFW][list_tp_srclist_]))
            else:
                list_tp_src.append("x")

            if dicAuxFW.has_key(list_any_dl_dstlist_) == True:
                list_any_dl_dst.append(str(json_dataFW[contFW][list_any_dl_dstlist_]))
            else:
                list_any_dl_dst.append("x")

            if dicAuxFW.has_key(list_nw_protolist_) == True:
                list_nw_proto.append(str(json_dataFW[contFW][list_nw_protolist_]))
            else:
                list_nw_proto.append("x")

            if dicAuxFW.has_key(list_tp_dstlist_) == True:
                list_tp_dst.append(str(json_dataFW[contFW][list_tp_dstlist_]))
            else:
                list_tp_dst.append("x")

            if dicAuxFW.has_key(list_dl_dstlist_) == True:
                list_dl_dst.append(str(json_dataFW[contFW][list_dl_dstlist_]))
            else:
                list_dl_dst.append("x")

            if dicAuxFW.has_key(list_any_tp_srclist_) == True:
                list_any_tp_src.append(str(json_dataFW[contFW][list_any_tp_srclist_]))
            else:
                list_any_tp_src.append("x")

            if dicAuxFW.has_key(list_outPortlist_) == True:
                list_outPort.append(str(json_dataFW[contFW][list_outPortlist_]))
            else:
                list_outPort.append("x")

            if dicAuxFW.has_key(list_src_maclist_) == True:
                list_src_mac.append(str(json_dataFW[contFW][list_src_maclist_]))
            else:
                list_src_mac.append("x")

            if dicAuxFW.has_key(list_dst_maclist_) == True:
                list_dst_mac.append(str(json_dataFW[contFW][list_dst_maclist_]))
            else:
                list_dst_mac.append("x")

            if dicAuxFW.has_key(list_actionlist_) == True:
                list_action.append(str(json_dataFW[contFW][list_actionlist_]))
            else:
                list_action.append("x")

            if dicAuxFW.has_key(list_matchlist_) == True:
                dicAuxFW = dicAuxFW["match"]

                if dicAuxFW.has_key(list_eth_srclist_) == True:
                    list_eth_src.append(str(json_dataFW[contFW][list_eth_srclist_]))
                else:
                    list_eth_src.append("x")

                if dicAuxFW.has_key(list_eth_dstlist_) == True:
                    list_eth_dst.append(str(json_dataFW[contFW][list_eth_dstlist_]))
                else:
                    list_eth_dst.append("x")

                if dicAuxFW.has_key(list_eth_typelist_) == True:
                    list_eth_type.append(str(json_dataFW[contFW][list_eth_typelist_]))
                else:
                    list_eth_type.append("x")

                if dicAuxFW.has_key(list_in_portlist_) == True:
                    list_in_port.append(str(json_dataFW[contFW][list_in_portlist_]))
                else:
                    list_in_port.append("x")

                if dicAuxFW.has_key(list_eth_vlan_vidlist_) == True:
                    list_eth_vlan_vid.append(str(json_dataFW[contFW][list_eth_vlan_vidlist_]))
                else:
                    list_eth_vlan_vid.append("x")

                if dicAuxFW.has_key(list_eth_vlan_pcplist_) == True:
                    list_eth_vlan_pcp.append(str(json_dataFW[contFW][list_eth_vlan_pcplist_]))
                else:
                    list_eth_vlan_pcp.append("x")

                if dicAuxFW.has_key(list_ip_protolist_) == True:
                    list_ip_proto.append(str(json_dataFW[contFW][list_ip_protolist_]))
                else:
                    list_ip_proto.append("x")

                if dicAuxFW.has_key(list_ipv4_srclist_) == True:
                    list_ipv4_src.append(str(json_dataFW[contFW][list_ipv4_srclist_]))
                else:
                    list_ipv4_src.append("x")

                if dicAuxFW.has_key(list_ipv4_dstlist_) == True:
                    list_ipv4_dst.append(str(json_dataFW[contFW][list_ipv4_dstlist_]))
                else:
                    list_ipv4_dst.append("x")

                if dicAuxFW.has_key(list_ipv6_srclist_) == True:
                    list_ipv6_src.append(str(json_dataFW[contFW][list_ipv6_srclist_]))
                else:
                    list_ipv6_src.append("x")

                if dicAuxFW.has_key(list_ipv6_dstlist_) == True:
                    list_ipv6_dst.append(str(json_dataFW[contFW][list_ipv6_dstlist_]))
                else:
                    list_ipv6_dst.append("x")

                if dicAuxFW.has_key(list_ipv6_labellist_) == True:
                    list_ipv6_label.append(str(json_dataFW[contFW][list_ipv6_labellist_]))
                else:
                    list_ipv6_label.append("x")

                if dicAuxFW.has_key(list_ip_toslist_) == True:
                    list_ip_tos.append(str(json_dataFW[contFW][list_ip_toslist_]))
                else:
                    list_ip_tos.append("x")

                if dicAuxFW.has_key(list_ip_ecnlist_) == True:
                    list_ip_ecn.append(str(json_dataFW[contFW][list_ip_ecnlist_]))
                else:
                    list_ip_ecn.append("x")

                if dicAuxFW.has_key(list_ip_dscplist_) == True:
                    list_ip_dscp.append(str(json_dataFW[contFW][list_ip_dscplist_]))
                else:
                    list_ip_dscp.append("x")

                if dicAuxFW.has_key(list_tp_srclist_) == True:
                    list_tp_src.append(str(json_dataFW[contFW][list_tp_srclist_]))
                else:
                    list_tp_src.append("x")

                if dicAuxFW.has_key(list_tp_dstlist_) == True:
                    list_tp_dst.append(str(json_dataFW[contFW][list_tp_dstlist_]))
                else:
                    list_tp_dst.append("x")

                if dicAuxFW.has_key(list_udp_srclist_) == True:
                    list_udp_src.append(str(json_dataFW[contFW][list_udp_srclist_]))
                else:
                    list_udp_src.append("x")

                if dicAuxFW.has_key(list_udp_dstlist_) == True:
                    list_udp_dst.append(str(json_dataFW[contFW][list_udp_dstlist_]))
                else:
                    list_udp_dst.append("x")

                if dicAuxFW.has_key(list_tcp_srclist_) == True:
                    list_tcp_src.append(str(json_dataFW[contFW][list_tcp_srclist_]))
                else:
                    list_tcp_src.append("x")

                if dicAuxFW.has_key(list_tcp_dstlist_) == True:
                    list_tcp_dst.append(str(json_dataFW[contFW][list_tcp_dstlist_]))
                else:
                    list_tcp_dst.append("x")

                if dicAuxFW.has_key(list_sctp_srclist_) == True:
                    list_sctp_src.append(str(json_dataFW[contFW][list_sctp_srclist_]))
                else:
                    list_sctp_src.append("x")

                if dicAuxFW.has_key(list_sctp_dstlist_) == True:
                    list_sctp_dst.append(str(json_dataFW[contFW][list_sctp_dstlist_]))
                else:
                    list_sctp_dst.append("x")

                if dicAuxFW.has_key(list_icmpv4_typelist_) == True:
                    list_icmpv4_type.append(str(json_dataFW[contFW][list_icmpv4_typelist_]))
                else:
                    list_icmpv4_type.append("x")

                if dicAuxFW.has_key(list_icmpv4_codelist_) == True:
                    list_icmpv4_code.append(str(json_dataFW[contFW][list_icmpv4_codelist_]))
                else:
                    list_icmpv4_code.append("x")

                if dicAuxFW.has_key(list_icmpv6_typelist_) == True:
                    list_icmpv6_type.append(str(json_dataFW[contFW][list_icmpv6_typelist_]))
                else:
                    list_icmpv6_type.append("x")

                if dicAuxFW.has_key(list_icmpv6_codelist_) == True:
                    list_icmpv6_code.append(str(json_dataFW[contFW][list_icmpv6_codelist_]))
                else:
                    list_icmpv6_code.append("x")

                if dicAuxFW.has_key(list_ipv6_nd_ssllist_) == True:
                    list_ipv6_nd_ssl.append(str(json_dataFW[contFW][list_ipv6_nd_ssllist_]))
                else:
                    list_ipv6_nd_ssl.append("x")

                if dicAuxFW.has_key(list_arp_spalist_) == True:
                    list_arp_spa.append(str(json_dataFW[contFW][list_arp_spalist_]))
                else:
                    list_arp_spa.append("x")

                if dicAuxFW.has_key(list_arp_tpalist_) == True:
                    list_arp_tpa.append(str(json_dataFW[contFW][list_arp_tpalist_]))
                else:
                    list_arp_tpa.append("x")

                if dicAuxFW.has_key(list_ipv6_nd_targetlist_) == True:
                    list_ipv6_nd_target.append(str(json_dataFW[contFW][list_ipv6_nd_targetlist_]))
                else:
                    list_ipv6_nd_target.append("x")

                if dicAuxFW.has_key(list_arp_opcodelist_) == True:
                    list_arp_opcode.append(str(json_dataFW[contFW][list_arp_opcodelist_]))
                else:
                    list_arp_opcode.append("x")

                if dicAuxFW.has_key(list_arp_thalist_) == True:
                    list_arp_tha.append(str(json_dataFW[contFW][list_arp_thalist_]))
                else:
                    list_arp_tha.append("x")

                if dicAuxFW.has_key(list_arp_spalist_) == True:
                    list_arp_spa.append(str(json_dataFW[contFW][list_arp_spalist_]))
                else:
                    list_arp_spa.append("x")

                if dicAuxFW.has_key(list_arp_tpalist_) == True:
                    list_arp_tpa.append(str(json_dataFW[contFW][list_arp_tpalist_]))
                else:
                    list_arp_tpa.append("x")

                if dicAuxFW.has_key(list_mpls_labellist_) == True:
                    list_mpls_label.append(str(json_dataFW[contFW][list_mpls_labellist_]))
                else:
                    list_mpls_label.append("x")

                if dicAuxFW.has_key(list_mpls_tclist_) == True:
                    list_mpls_tc.append(str(json_dataFW[contFW][list_mpls_tclist_]))
                else:
                    list_mpls_tc.append("x")

                if dicAuxFW.has_key(list_mpls_boslist_) == True:
                    list_mpls_bos.append(str(json_dataFW[contFW][list_mpls_boslist_]))
                else:
                    list_mpls_bos.append("x")

                if dicAuxFW.has_key(list_tunnel_idlist_) == True:
                    list_tunnel_id.append(str(json_dataFW[contFW][list_tunnel_idlist_]))
                else:
                    list_tunnel_id.append("x")

                if dicAuxFW.has_key(list_metadatalist_) == True:
                    list_metadata.append(str(json_dataFW[contFW][list_metadatalist_]))
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
                if (list_eth_src[ifw] == list_xlist_):
                    list_eth_src[ifw] = list_eth_src[jfw]
                if (list_eth_dst[ifw] == list_xlist_):
                    list_eth_dst[ifw] = list_eth_dst[jfw]
                if (list_eth_type[ifw] == list_xlist_):
                    list_eth_type[ifw] = list_eth_type[jfw]
                if (list_in_porteth_vlan_videth_vlan_pcp[ifw] == list_xlist_):
                    list_in_porteth_vlan_videth_vlan_pcp[ifw] = list_in_porteth_vlan_videth_vlan_pcp[jfw]
                if (list_ip_proto[ifw] == list_xlist_):
                    list_ip_proto[ifw] = list_ip_proto[jfw]
                if (list_ipv4_src[ifw] == list_xlist_):
                    list_ipv4_src[ifw] = list_ipv4_src[jfw]
                if (list_ipv4_dstipv6_src[ifw] == list_xlist_):
                    list_ipv4_dstipv6_src[ifw] = list_ipv4_dstipv6_src[jfw]
                if (list_ipv6_dst[ifw] == list_xlist_):
                    list_ipv6_dst[ifw] = list_ipv6_dst[jfw]
                if (list_ipv6_label[ifw] == list_xlist_):
                    list_ipv6_label[ifw] = list_ipv6_label[jfw]
                if (list_ip_tos[ifw] == list_xlist_):
                    list_ip_tos[ifw] = list_ip_tos[jfw]
                if (list_ip_ecn[ifw] == list_xlist_):
                    list_ip_ecn[ifw] = list_ip_ecn[jfw]
                if (list_ip_dscp[ifw] == list_xlist_):
                    list_ip_dscp[ifw] = list_ip_dscp[jfw]
                if (list_tp_src[ifw] == list_xlist_):
                    list_tp_src[ifw] = list_tp_src[jfw]
                if (list_tp_dst[ifw] == list_xlist_):
                    list_tp_dst[ifw] = list_tp_dst[jfw]
                if (list_udp_src[ifw] == list_xlist_):
                    list_udp_src[ifw] = list_udp_src[jfw]
                if (list_udp_dst[ifw] == list_xlist_):
                    list_udp_dst[ifw] = list_udp_dst[jfw]
                if (list_tcp_srctcp_dst[ifw] == list_xlist_):
                    list_tcp_srctcp_dst[ifw] = list_tcp_srctcp_dst[jfw]
                if (list_sctp_src[ifw] == list_xlist_):
                    list_sctp_src[ifw] = list_sctp_src[jfw]
                if (list_sctp_dst[ifw] == list_xlist_):
                    list_sctp_dst[ifw] = list_sctp_dst[jfw]
                if (list_icmpv4_type[ifw] == list_xlist_):
                    list_icmpv4_type[ifw] = list_icmpv4_type[jfw]
                if (list_icmpv4_code[ifw] == list_xlist_):
                    list_icmpv4_code[ifw] = list_icmpv4_code[jfw]
                if (list_icmpv6_type[ifw] == list_xlist_):
                    list_icmpv6_type[ifw] = list_icmpv6_type[jfw]
                if (list_icmpv6_code[ifw] == list_xlist_):
                    list_icmpv6_code[ifw] = list_icmpv6_code[jfw]
                if (list_ipv6_nd_ssl[ifw] == list_xlist_):
                    list_ipv6_nd_ssl[ifw] = list_ipv6_nd_ssl[jfw]
                if (list_ipv6_nd_ttl[ifw] == list_xlist_):
                    list_ipv6_nd_ttl[ifw] = list_ipv6_nd_ttl[jfw]
                if (list_arp_tpa[ifw] == list_xlist_):
                    list_arp_tpa[ifw] = list_arp_tpa[jfw]
                if (list_ipv6_nd_target[ifw] == list_xlist_):
                    list_ipv6_nd_target[ifw] = list_ipv6_nd_target[jfw]
                if (list_arp_opcode[ifw] == list_xlist_):
                    list_arp_opcode[ifw] = list_arp_opcode[jfw]
                if (list_arp_tha[ifw] == list_xlist_):
                    list_arp_tha[ifw] = list_arp_tha[jfw]
                if (list_arp_spa[ifw] == list_xlist_):
                    list_arp_spa[ifw] = list_arp_spa[jfw]
                if (list_arp_tpaipv6_label[ifw] == list_xlist_):
                    list_arp_tpaipv6_label[ifw] = list_arp_tpaipv6_label[jfw]
                if (list_ip_tos[ifw] == list_xlist_):
                    list_ip_tos[ifw] = list_ip_tos[jfw]
                if (list_ip_ecn[ifw] == list_xlist_):
                    list_ip_ecn[ifw] = list_ip_ecn[jfw]
                if (list_ip_dscp[ifw] == list_xlist_):
                    list_ip_dscp[ifw] = list_ip_dscp[jfw]
                if (list_tp_src[ifw] == list_xlist_):
                    list_tp_src[ifw] = list_tp_src[jfw]
                if (list_tp_dst[ifw] == list_xlist_):
                    list_tp_dst[ifw] = list_tp_dst[jfw]
                if (list_udp_src[ifw] == list_xlist_):
                    list_udp_src[ifw] = list_udp_src[jfw]
                if (list_udp_dst[ifw] == list_xlist_):
                    list_udp_dst[ifw] = list_udp_dst[jfw]
                if (list_tcp_src[ifw] == list_xlist_):
                    list_tcp_src[ifw] = list_tcp_src[jfw]
                if (list_tcp_dst[ifw] == list_xlist_):
                    list_tcp_dst[ifw] = list_tcp_dst[jfw]
                if (list_sctp_src[ifw] == list_xlist_):
                    list_sctp_src[ifw] = list_sctp_src[jfw]
                if (list_sctp_dst[ifw] == list_xlist_):
                    list_sctp_dst[ifw] = list_sctp_dst[jfw]
                if (list_icmpv4_type[ifw] == list_xlist_):
                    list_icmpv4_type[ifw] = list_icmpv4_type[jfw]
                if (list_icmpv4_code[ifw] == list_xlist_):
                    list_icmpv4_code[ifw] = list_icmpv4_code[jfw]
                if (list_icmpv6_type[ifw] == list_xlist_):
                    list_icmpv6_type[ifw] = list_icmpv6_type[jfw]
                if (list_icmpv6_code[ifw] == list_xlist_):
                    list_icmpv6_code[ifw] = list_icmpv6_code[jfw]
                if (list_ipv6_nd_ssl[ifw] == list_xlist_):
                    list_ipv6_nd_ssl[ifw] = list_ipv6_nd_ssl[jfw]
                if (list_ipv6_nd_ttl[ifw] == list_xlist_):
                    list_ipv6_nd_ttl[ifw] = list_ipv6_nd_ttl[jfw]
                if (list_ipv6_nd_target[ifw] == list_xlist_):
                    list_ipv6_nd_target[ifw] = list_ipv6_nd_target[jfw]
                if (list_arp_opcode[ifw] == list_xlist_):
                    list_arp_opcode[ifw] = list_arp_opcode[jfw]
                if (list_arp_tha[ifw] == list_xlist_):
                    list_arp_tha[ifw] = list_arp_tha[jfw]
                if (list_arp_spa[ifw] == list_xlist_):
                    list_arp_spa[ifw] = list_arp_spa[jfw]
                if (list_arp_tpa[ifw] == list_xlist_):
                    list_arp_tpa[ifw] = list_arp_tpa[jfw]
                if (list_mpls_label[ifw] == list_xlist_):
                    list_mpls_label[ifw] = list_mpls_label[jfw]
                if (list_mpls_tc[ifw] == list_xlist_):
                    list_mpls_tc[ifw] = list_mpls_tc[jfw]
                if (list_mpls_bos[ifw] == list_xlist_):
                    list_mpls_bos[ifw] = list_mpls_bos[jfw]
                if (list_tunnel_id[ifw] == list_xlist_):
                    list_tunnel_id[ifw] = list_tunnel_id[jfw]
                if (list_metadata[ifw] == list_xlist_):
                    list_metadata[ifw] = list_metadata[jfw]
                if (list_[ifw] == list_xlist_):
                    list_[ifw] = list_[jfw]
                if (list_version[ifw] == list_xlist_):
                    list_version[ifw] = list_version[jfw]
                if (list_command[ifw] == list_xlist_):
                    list_command[ifw] = list_command[jfw]
                if (list_cookie[ifw] == list_xlist_):
                    list_cookie[ifw] = list_cookie[jfw]
                if (list_src_ip[ifw] == list_xlist_):
                    list_src_ip[ifw] = list_src_ip[jfw]
                if (list_dst_ip[ifw] == list_xlist_):
                    list_dst_ip[ifw] = list_dst_ip[jfw]
                if (list_dl_type[ifw] == list_xlist_):
                    list_dl_type[ifw] = list_dl_type[jfw]
                if (list_nw_dst_prefix[ifw] == list_xlist_):
                    list_nw_dst_prefix[ifw] = list_nw_dst_prefix[jfw]
                if (list_nw_src_prefix[ifw] == list_xlist_):
                    list_nw_src_prefix[ifw] = list_nw_src_prefix[jfw]
                if (list_nw_src_maskbits[ifw] == list_xlist_):
                    list_nw_src_maskbits[ifw] = list_nw_src_maskbits[jfw]
                if (list_nw_dst_maskbits[ifw] == list_xlist_):
                    list_nw_dst_maskbits[ifw] = list_nw_dst_maskbits[jfw]
                if (list_any_nw_dst[ifw] == list_xlist_):
                    list_any_nw_dst[ifw] = list_any_nw_dst[jfw]
                if (list_any_nw_proto[ifw] == list_xlist_):
                    list_any_nw_proto[ifw] = list_any_nw_proto[jfw]
                if (list_any_in_port[ifw] == list_xlist_):
                    list_any_in_port[ifw] = list_any_in_port[jfw]
                if (list_any_nw_srcany_tp_ds[ifw] == list_xlist_):
                    list_any_nw_srcany_tp_ds[ifw] = list_any_nw_srcany_tp_ds[jfw]
                if (list_ruleid[ifw] == list_xlist_):
                    list_ruleid[ifw] = list_ruleid[jfw]
                if (list_idleTimeoutSec[ifw] == list_xlist_):
                    list_idleTimeoutSec[ifw] = list_idleTimeoutSec[jfw]
                if (list_hardTimeoutSec[ifw] == list_xlist_):
                    list_hardTimeoutSec[ifw] = list_hardTimeoutSec[jfw]
                if (list_any_dl_type[ifw] == list_xlist_):
                    list_any_dl_type[ifw] = list_any_dl_type[jfw]
                if (list_priority[ifw] == list_xlist_):
                    list_priority[ifw] = list_priority[jfw]
                if (list_in_port[ifw] == list_xlist_):
                    list_in_port[ifw] = list_in_port[jfw]
                if (list_any_dpid[ifw] == list_xlist_):
                    list_any_dpid[ifw] = list_any_dpid[jfw]
                if (list_dl_src[ifw] == list_xlist_):
                    list_dl_src[ifw] = list_dl_src[jfw]
                if (list_dpid[ifw] == list_xlist_):
                    list_dpid[ifw] = list_dpid[jfw]
                if (list_tp_src[ifw] == list_xlist_):
                    list_tp_src[ifw] = list_tp_src[jfw]
                if (list_any_dl_dst[ifw] == list_xlist_):
                    list_any_dl_dst[ifw] = list_any_dl_dst[jfw]
                if (list_nw_proto[ifw] == list_xlist_):
                    list_nw_proto[ifw] = list_nw_proto[jfw]
                if (list_tp_dst[ifw] == list_xlist_):
                    list_tp_dst[ifw] = list_tp_dst[jfw]
                if (list_dl_dst[ifw] == list_xlist_):
                    list_dl_dst[ifw] = list_dl_dst[jfw]
                if (list_any_tp_src[ifw] == list_xlist_):
                    list_any_tp_src[ifw] = list_any_tp_src[jfw]
                if (list_outPort[ifw] == list_xlist_):
                    list_outPort[ifw] = list_outPort[jfw]
                if (list_src_mac[ifw] == list_xlist_):
                    list_src_mac[ifw] = list_src_mac[jfw]
                if (list_dst_mac[ifw] == list_xlist_):
                    list_dst_mac[ifw] = list_dst_mac[jfw]
                if (list_action[ifw] == list_xlist_):
                    list_action[ifw] = list_action[jfw]

                if(list_eth_src[ifw]==list_eth_src[jfw] and list_eth_dst[ifw]==list_eth_dst[jfw] and list_eth_type[ifw]==list_eth_type[jfw] and list_in_porteth_vlan_videth_vlan_pcp[ifw]==list_in_porteth_vlan_videth_vlan_pcp[jfw] and list_ip_proto[ifw]==list_ip_proto[jfw] and list_ipv4_src[ifw]==list_ipv4_src[jfw] and list_ipv4_dstipv6_src[ifw]==list_ipv4_dstipv6_src[jfw] and list_ipv6_dst[ifw]==list_ipv6_dst[jfw] and list_ipv6_label[ifw]==list_ipv6_label[jfw] and list_ip_tos[ifw]==list_ip_tos[jfw] and list_ip_ecn[ifw]==list_ip_ecn[jfw] and list_ip_dscp[ifw]==list_ip_dscp[jfw] and list_tp_src[ifw]==list_tp_src[jfw] and list_tp_dst[ifw]==list_tp_dst[jfw] and list_udp_src[ifw]==list_udp_src[jfw] and list_udp_dst[ifw]==list_udp_dst[jfw] and list_tcp_srctcp_dst[ifw]==list_tcp_srctcp_dst[jfw] and list_sctp_src[ifw]==list_sctp_src[jfw] and list_sctp_dst[ifw]==list_sctp_dst[jfw] and list_icmpv4_type[ifw]==list_icmpv4_type[jfw] and list_icmpv4_code[ifw]==list_icmpv4_code[jfw] and list_icmpv6_type[ifw]==list_icmpv6_type[jfw] and list_icmpv6_code[ifw]==list_icmpv6_code[jfw] and list_ipv6_nd_ssl[ifw]==list_ipv6_nd_ssl[jfw] and list_ipv6_nd_ttl[ifw]==list_ipv6_nd_ttl[jfw] and list_arp_tpa[ifw]==list_arp_tpa[jfw] and list_ipv6_nd_target[ifw]==list_ipv6_nd_target[jfw] and list_arp_opcode[ifw]==list_arp_opcode[jfw] and list_arp_tha[ifw]==list_arp_tha[jfw] and list_arp_spa[ifw]==list_arp_spa[jfw] and list_arp_tpaipv6_label[ifw]==list_arp_tpaipv6_label[jfw] and list_ip_tos[ifw]==list_ip_tos[jfw] and list_ip_ecn[ifw]==list_ip_ecn[jfw] and list_ip_dscp[ifw]==list_ip_dscp[jfw] and list_tp_src[ifw]==list_tp_src[jfw] and list_tp_dst[ifw]==list_tp_dst[jfw] and list_udp_src[ifw]==list_udp_src[jfw] and list_udp_dst[ifw]==list_udp_dst[jfw] and list_tcp_src[ifw]==list_tcp_src[jfw] and list_tcp_dst[ifw]==list_tcp_dst[jfw] and list_sctp_src[ifw]==list_sctp_src[jfw] and list_sctp_dst[ifw]==list_sctp_dst[jfw] and list_icmpv4_type[ifw]==list_icmpv4_type[jfw] and list_icmpv4_code[ifw]==list_icmpv4_code[jfw] and list_icmpv6_type[ifw]==list_icmpv6_type[jfw] and list_icmpv6_code[ifw]==list_icmpv6_code[jfw] and list_ipv6_nd_ssl[ifw]==list_ipv6_nd_ssl[jfw] and list_ipv6_nd_ttl[ifw]==list_ipv6_nd_ttl[jfw] and list_ipv6_nd_target[ifw]==list_ipv6_nd_target[jfw] and list_arp_opcode[ifw]==list_arp_opcode[jfw] and list_arp_tha[ifw]==list_arp_tha[jfw] and list_arp_spa[ifw]==list_arp_spa[jfw] and list_arp_tpa[ifw]==list_arp_tpa[jfw] and list_mpls_label[ifw]==list_mpls_label[jfw] and list_mpls_tc[ifw]==list_mpls_tc[jfw] and list_mpls_bos[ifw]==list_mpls_bos[jfw] and list_tunnel_id[ifw]==list_tunnel_id[jfw] and list_metadata[ifw]==list_metadata[jfw] and list_[ifw]==list_[jfw] and list_version[ifw]==list_version[jfw] and list_command[ifw]==list_command[jfw] and list_cookie[ifw]==list_cookie[jfw] and list_src_ip[ifw]==list_src_ip[jfw] and list_dst_ip[ifw]==list_dst_ip[jfw] and list_dl_type[ifw]==list_dl_type[jfw] and list_nw_dst_prefix[ifw]==list_nw_dst_prefix[jfw] and list_nw_src_prefix[ifw]==list_nw_src_prefix[jfw] and list_nw_src_maskbits[ifw]==list_nw_src_maskbits[jfw] and list_nw_dst_maskbits[ifw]==list_nw_dst_maskbits[jfw] and list_any_nw_dst[ifw]==list_any_nw_dst[jfw] and list_any_nw_proto[ifw]==list_any_nw_proto[jfw] and list_any_in_port[ifw]==list_any_in_port[jfw] and list_any_nw_srcany_tp_ds[ifw]==list_any_nw_srcany_tp_ds[jfw] and list_ruleid[ifw]==list_ruleid[jfw] and list_idleTimeoutSec[ifw]==list_idleTimeoutSec[jfw] and list_hardTimeoutSec[ifw]==list_hardTimeoutSec[jfw] and list_any_dl_type[ifw]==list_any_dl_type[jfw] and list_priority[ifw]==list_priority[jfw] and list_in_port[ifw]==list_in_port[jfw] and list_any_dpid[ifw]==list_any_dpid[jfw] and list_dl_src[ifw]==list_dl_src[jfw] and list_dpid[ifw]==list_dpid[jfw] and list_tp_src[ifw]==list_tp_src[jfw] and list_any_dl_dst[ifw]==list_any_dl_dst[jfw] and list_nw_proto[ifw]==list_nw_proto[jfw] and list_tp_dst[ifw]==list_tp_dst[jfw] and list_dl_dst[ifw]==list_dl_dst[jfw] and list_any_tp_src[ifw]==list_any_tp_src[jfw] and list_outPort[ifw]==list_outPort[jfw] and list_src_mac[ifw]==list_src_mac[jfw] and list_dst_mac[ifw]==list_dst_mac[jfw] and list_action[ifw]==list_action[jfw]):
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
    fwDataFile = open("../data/fwDataFile.csv", "w")

    if flag_confRed != 1:
        return {"status": "No conflict or redundancy found"}

    for rfw in range(len(list_csvFW)):
        dicAux_CSV = list_csvFW[r]
        for nfw in range(len(list_csvFW[r])):
            fwDataFile.write(str(dicAux_CSVFW[str(nfw)]) + "\n")
        fwDataFile.write("\n")

    fwDataFile.close()
    return True

def verifyFirewall():
    
    return True

