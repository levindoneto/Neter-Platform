#!/usr/bin/python
# coding: UTF-8
import csv
from src.main.bitUtils import bitVectorUtils as classBit
from src.main.data import bitList as classBitList
from BitVector import BitVector
import time
csvData = "../data/data.csv"

graph = {"a": ["c"],
         "b": ["c", "e"],
         "c": ["a", "b", "d", "e"],
         "d": ["c"],
         "e": ["c", "b"],
         "f": []
         }


def generate_edges(graph):
    edges = []
    for node in graph:
        for neighbour in graph[node]:
            edges.append((node, neighbour))

    return edges

def find_isolated_nodes(graph):
    """ returns a list of isolated nodes. """
    isolated = []
    for node in graph:
        if not graph[node]:
            isolated += node
    return isolated

''' Convert a integer atomic predicate in a Bitvector atomic predicate
    @:parameter : BV Lists: switches, match, destination, action
    @:return    : BV Graph '''
def make_graph(diffSwitches, Switch_rule, Match, Destination, Action): # Type of all parameters -> List of BitVectors
    graph = {}
    for i in range(len(diffSwitches)):
        i+=1          # For the switch to start at one
        ruleList = [] # Format: [[Match0, Destination0, Action0],[Match1, Destionation1, Action1],...] -> BitVector Elements
                      # __init__ the list each switch
        for j in range(len(Switch_rule)):
            ruleList.append([])               # Sublist
            ruleList[j].append(Match[j])
            ruleList[j].append(Destination[j])
            ruleList[j].append(Action[j])
        #graph.update({2:[2,3]})
        graph.update({classBit.makeBitVector(i):ruleList})
    return graph

#print(find_isolated_nodes(graph))
