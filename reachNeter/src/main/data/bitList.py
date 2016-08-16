#!/usr/bin/python
# coding: UTF-8

import collections
import pickle

bitList    = []  #__init__ of BitVectorList, the lsb is a action bit # Match
dstList    = []  # This list contains only information about destination of packages in the network
actionList = []  # This list contains only information about actions of predicates with the same index of the match informations
