from flask import Blueprint, request, jsonify
from services import mininet_service as Mininet
from flask_cors import CORS, cross_origin
import time
import resource

mininet_route = Blueprint("mininet_route", __name__)
CORS(mininet_route)

@mininet_route.route("/mininet/startsample", methods=["POST"])
def startsample():
    time_init = time.time()
    content = request.json["data"]
    n_hosts = content["n_hosts"] + 1
    n_switches = content["n_switches"] + 1
    hosts = range(1, n_hosts)
    switches = range(1, n_switches)
    auto_set_macs = False
    ip =  "127.0.0.1"
    links = dict()
    for s in switches:
        links_s = ['s'+str(i) for i in switches if i != s] + ['h'+str(i) for i in hosts]
        links.update({"s"+str(s): links_s})
    for h in hosts:
        links_h = ['s'+str(i) for i in switches] + ['h'+str(i) for i in hosts if i != h]
        links.update({"h"+str(h): links_h})

    Mininet.startNetwork(auto_set_macs, hosts, ip, links, switches)
    time_end = time.time()

    time_ms = time_end - time_init
    memory_kilobytes = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    return jsonify({
        "status": "Topology started on IP " + ip,
        "time_ms": time_ms,
        "memory_kilobytes": memory_kilobytes
    })


@mininet_route.route("/mininet/start", methods=["POST"])
def start():
    time_init = time.time()
    content = request.json["data"]
    auto_set_macs = content["autoSetMacs"]
    hosts = content["hosts"]
    ip = content["ip"]
    links = content["links"]
    switches = content["switches"]
    Mininet.startNetwork(auto_set_macs, hosts, ip, links, switches)
    time_end = time.time()

    time_ms = time_end - time_init
    memory_kilobytes = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    return jsonify({
        "status": "Topology started on IP " + ip,
        "time_ms": time_ms,
        "memory_kilobytes": memory_kilobytes
    })

@mininet_route.route("/mininet/ping", methods=["POST"])
def ping():
    Mininet.pingAll()
    return jsonify({"status": "Ping all completed"})

@mininet_route.route("/mininet/ips", methods=["GET"])
def get_ips():
    ips = Mininet.getHosts()
    return jsonify({"ips": ips})

@mininet_route.route("/mininet/stop", methods=["POST"])
def stop():
    Mininet.stopNetwork()
    return jsonify({"status": "Network stopped"})