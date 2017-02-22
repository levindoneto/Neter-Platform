#!/usr/bin/python
# coding: UTF-8

from BitVector import BitVector
from src.main.isolUtils import BitIsol as SliceIsolUtils
import collections

'''#Define'''
IS_NOT_ORDERED = 0
IS_ORDERED     = 1

# Vertice information
SWITCH_INFO    = 0
SET_RULES      = 1
SET_HOSTS      = 2
LST_PORTS      = 3
VISITED_INFO   = 4

# Set information
MATCH_INFO     = 0
ACTION_INFO    = 1

DENY = SliceIsolUtils.makeBitVector(0)   # Low Logical Level
ALLOW = SliceIsolUtils.makeBitVector(1)  # High Logical Level


graph = {}

'''
This function make a graph with the carachteristics of the network topology
    @:parameter : BV Lists: switches(main), set of rules (matches, actions), set of hosts (with the its ports), visited information(graph)
    @:return    : BV Graph '''
def makeGraphTopology (switches, rules_set, hosts_set, visited_info):
    return 0