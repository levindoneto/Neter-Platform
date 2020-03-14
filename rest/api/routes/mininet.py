from flask import Blueprint
from services import mininet as Mininet

mininet_route = Blueprint('mininet_route', __name__)

@mininet_route.route("/mininet/redundancies")
def get_redundancies():
    return "NOT IMPLEMENTED"

@mininet_route.route('/mininet/topology', methods=['POST'])
def topology():
    return "NOT IMPLEMENTED"

@mininet_route.route('/mininet/ping', methods=['POST'])
def ping():
    return "NOT IMPLEMENTED"

@mininet_route.route('/mininet/ips', methods=['GET'])
def get_ips():
    return "NOT IMPLEMENTED"

@mininet_route.route('/mininet/stop', methods=['POST'])
def stop():
    return "NOT IMPLEMENTED"

@mininet_route.route('/mininet/attack', methods=['POST'])
def attack():
    return "NOT IMPLEMENTED"

@mininet_route.route('/mininet/close', methods=['POST'])
def close():
    return "NOT IMPLEMENTED"
