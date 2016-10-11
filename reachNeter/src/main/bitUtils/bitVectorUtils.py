#!/usr/bin/python
# coding: UTF-8

# Libraries utilized
import os
import sys
import json
import csv
from os import system
import time
#from bitarray import bitarray
from src.main.data import bitList as classBitList
from BitVector import BitVector
from BitVector import BitVector
'''Global Variables'''
switch_info  = 0
match_info   = 1
dst_info     = 2
action_info  = 3
visited_info = 4


''' Convert a string atomic predicate in a integer atomic predicate
    @:parameter : Integer
    @:return    : BitVector '''
def stringToIntFormated (stringp):
    #Retirando caracteres nao numericos
    if (stringp == ''):
        return None
    else:
        newAtomicPredicate = ""
        for j in stringp:
            if (j>='0' and j<='9'):
                newAtomicPredicate += j
        newAtomicPredicate = int(newAtomicPredicate)
        return newAtomicPredicate

''' Return a package in form of in-predicate (LSB=1, it's 1, because a package in always try to pass)
    @:parameter : Integer
    @:return    : BitVector '''
def makePackVector(packVector):
    packVector = int(packVector) * 2
    packVector = BitVector(intVal=(packVector + 1))
    return packVector

''' Convert a integer atomic predicate in a Bitvector atomic predicate
    @:parameter : Integer
    @:return    : BitVector '''
def makeBitVector(AtomicPredicate):
    AtomicPredicate = BitVector(intVal=AtomicPredicate)
    return AtomicPredicate

'''Return a in-predicate in form of vector with n bits [n-1: match, 1(lLSB): action ]
    @:parameter : String
    @:return    : BitVector '''

def makePredicateVector(value):
    #Retirando caracteres nao numericos
    new_value = ""
    for i in value:
        if (i>='1' and i<='9'):
            new_value += i
    new_value = int(new_value)
    new_value = BitVector(intVal=new_value)
    return new_value

'''Return the MSB (n-1, Match) bits of a vector with n bits
    @:parameter : BitVector
    @:return    : BitVector '''
def sliceMatch(predicadoM):
    predicadoM = predicadoM[0:((len(predicadoM))-1)]
    return predicadoM

''' Return the LSB (Action) of a vector with n bits
    @:parameter : BitVector
    @:return    : BitVector '''
def sliceAction(predicadoA):
    predicadoA = predicadoA[((len(predicadoA))-1):len(predicadoA)]
    return predicadoA

''' Convert a bit string in BitVector
    @:parameter : String
    @:return    : BitVector '''
def stringToBit(bvstring):
    bvstring = BitVector(bitstring=str(bvstring))
    return bvstring

''' Convert a integer output in a BitVector Action with 8 bits width
    @:parameter: Integer
    @:return: BitVector '''
def outputToAction(output):
    action = classBit.makeBitVector(output)
    return action

''' Receive a list with informations about header of one rule and return a BitVector package test
    @:parameter: *List
    @:return: BitVector package [match, dst]
'''
def makeTest(rule):
    dst = makeBitVector(rule[6])
    package = []  # Informations: rule, destination
    auxRule = BitVector(size=0)
    for j in range(len(rule)):
        auxRule += makeBitVector(rule[j]) # Concatenating for to generate a package (int)
    package.append(auxRule)
    package.append(dst)
    return package

''' Receive a topology file and converts this in a hash table, where key->switch and value->host
    for use in a dict.get(key) method
    @:parameter: CSV file
    @:return: BitVector hash table with switch:host
'''
def getLink(topology_link):
    hashlink = {}
    with open(topology_link, "rb") as csvlink:
        spamreader = csv.reader(csvlink, delimiter=',', quotechar='\'')
        info_index = 0
        for row in spamreader:                                         # Line by line of CSV file
            row[0] = stringToIntFormated(row[0])                       # String -> Int
            row[0] = makeBitVector(row[0])                             # Int -> BitVector
            row[1] = stringToIntFormated(row[1])                       # String -> Int
            row[1] = makeBitVector(row[1])                             # Int -> BitVector

            hashlink.update({row[0]:row[1]})
            info_index += 1
    return hashlink
