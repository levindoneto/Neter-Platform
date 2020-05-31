#!/usr/bin/env python

import logging
import os
import sys
import json
from os import system
import time

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

def startNetwork(auto_set_macs, hosts, ip, links, switches):
    
    return True