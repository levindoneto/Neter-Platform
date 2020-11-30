#!/usr/bin/env python

import logging
import os
import sys
import networkx as nx
from os import system
import json
import time
import resource

logger = logging.getLogger("reachability_service")
logging.basicConfig(level = logging.INFO)

def getPort(device):
    return int(device[-1:]) - 1 if int(device[-1:]) != 1 else int(device[-1:])

"""
Verify reachability
"""
def verifyReachability(topologyLinks, origin, destination):
    for d in topologyLinks:
        topologyLinks[d] = filter(lambda device: device.strip(), topologyLinks[d])
    time_init = time.time()
    graph = nx.Graph(topologyLinks)
    paths = nx.single_source_shortest_path(graph, origin)
    statusVerb = ""
    trace = ""
    if (not(destination in paths)):
        statusVerb = " not"
        trace = "No trace available"
    else:
        for p in paths[destination]:
            trace += "[" + p + "]-(" + str(getPort(p)) + ")->"
        trace = trace[:-6]
    time_end = time.time()
    memory_kilobytes = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return {
        "status": "The destination " + destination + " is" + statusVerb + " reachable from the origin " + origin,
        "time_ms": time_end - time_init,
        "trace": trace,
        "memory_kilobytes": memory_kilobytes / 8
    }