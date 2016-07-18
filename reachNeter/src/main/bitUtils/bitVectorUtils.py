#!/usr/bin/python
# coding: UTF-8

# Bibliotecas utilizadas
import os
import sys
import json
import csv
from os import system
import time
#from bitarray import bitarray
from BitVector import BitVector


''' Convert a string atomic predicate in a integer atomic predicate
    @parameter : int
    @return    : BitVector '''
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
    @parameter : int
    @return    : BitVector '''
def makePackVector(packVector):
    packVector = int(packVector) * 2
    packVector = BitVector(intVal=(packVector + 1))
    return packVector

''' Convert a integer atomic predicate in a Bitvector atomic predicate
    @parameter : int
    @return    : BitVector '''
def makeBitVector(AtomicPredicate):
    AtomicPredicate = BitVector(intVal=AtomicPredicate)
    return AtomicPredicate

'''Return a in-predicate in form of vector with n bits [n-1: match, 1(lLSB): action ]
    @parameter : string
    @return    : BitVector '''
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
    @parameter : BitVector
    @return    : BitVector '''
def sliceMatch(predicadoM):
    predicadoM = predicadoM[0:((len(predicadoM))-1)]
    return predicadoM

''' Return the LSB (Action) of a vector with n bits
    @parameter : BitVector
    @return    : BitVector '''
def sliceAction(predicadoA):
    predicadoA = predicadoA[((len(predicadoA))-1):len(predicadoA)]
    return predicadoA

''' Convert a bit string in BitVector
    @parameter : string
    @return    : BitVector '''
def stringToBit(bvstring):
    bvstring = BitVector(bitstring=str(bvstring))
    return bvstring