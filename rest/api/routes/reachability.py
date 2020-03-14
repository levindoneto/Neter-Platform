from flask import Blueprint

reachability_route = Blueprint('reachability_route', __name__)

@reachability_route.route("/reachability")
def get_reachability():
    return "NOT IMPLEMENTED"