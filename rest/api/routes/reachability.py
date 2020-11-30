from flask import Blueprint, request, jsonify
from flask_cors import CORS, cross_origin
from services import reachability_service as Reachability

reachability_route = Blueprint("reachability_route", __name__)
CORS(reachability_route)

@reachability_route.route("/reachability", methods=["POST"])
def reachability():
    content = request.json["data"]
    topologyLinks = content["topologyLinks"]
    origin = content["origin"]
    destination = content["destination"]
    
    respReachability = Reachability.verifyReachability(topologyLinks, origin, destination)

    return jsonify(respReachability)