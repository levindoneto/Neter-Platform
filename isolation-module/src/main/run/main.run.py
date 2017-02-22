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












