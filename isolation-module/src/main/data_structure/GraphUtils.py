#!/usr/bin/python
# coding: UTF-8

from BitVector import BitVector
from src.main.isolUtils import BitIsol as SliceIsolUtils

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

'''
    This method is used to detect the reaching of a package when it enters in the network topology
    @:parameter
        BitVector Package
        BitVector Graph Topology
        List Mapping: Switchs - Hosts - Ports
        BitVector Visited
    @:return
        Packet reached its destination      -> 1
        Packet didn't reach its destination -> 0
'''
def DFS():
    found = 0

    return found

'''
    This method is used to give all available informations about the following vertice's data:
        - Switch (00)
        - Host   (01)
        - Port   (10)
        - Rules  (11)
    @:parameter
        00 - 11 for a specific information or X (don't care) for all informations
    @:return
        A list of the required informations
 '''
def mapping():

    return theCompleteInformation