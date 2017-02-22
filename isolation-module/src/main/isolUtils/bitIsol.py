#!/usr/bin/python
# coding: UTF-8

# Libraries utilized
import csv
from BitVector import BitVector

'''#Define'''
IS_NOT_ORDERED = 0
IS_ORDERED     = 1

SWITCH_INFO    = 0
MATCH_PACK     = 0
MATCH_INFO     = 1
DST_PACK       = 1
DST_INFO       = 2
ACTION_INFO    = 3
VISITED_INFO   = 4

def makeBitVector(AtomicPredicate):
    AtomicPredicate = BitVector(intVal=AtomicPredicate)
    return AtomicPredicate