#!/usr/bin/env python

import logging
import os
import sys
import json
from os import system
import time
import firewall_rules from ../constants as FIREWALL_RULES
import flowtable_rules from ../constants as FLOWTABLE_RULES

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

