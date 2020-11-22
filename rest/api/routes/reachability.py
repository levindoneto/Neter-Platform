from flask import Blueprint
from flask_cors import CORS, cross_origin

reachability_route = Blueprint("reachability_route", __name__)
CORS(reachability_route)

@reachability_route.route("/reachability", methods=["GET"])
def get_ips():
    ips = Mininet.getHosts()
    return jsonify({"ips": ips})