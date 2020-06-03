#!/usr/bin/env python

import logging
import os
import sys
import json
from os import system
import time

logger = logging.getLogger("flowtable_service")
logging.basicConfig(level = logging.INFO)

"""
Get all flows from flowtable
"""
def getFlows(ip, port):
    command = "curl http://" + ip + ":" + port + "/wm/core/switch/all/flow/json"
    command_output = os.popen(command).read()
    topology = json.loads(command_output)

    return {"topology": topology}

"""
Create data flow file
"""
def createDataFlow(topology):
    dataFlowPath = "rest/api/data/dataflow"
    dataFlow = open(dataFlowPath, "w")
    dataFlow.write(str(topology))
    dataFlow.close()
    
    return dataFlowPath