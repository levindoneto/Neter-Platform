from flask import Blueprint

conflicts_route = Blueprint('conflicts_route', __name__)

@conflicts_route.route("/conflicts")
def get_conflicts():
    return "NOT IMPLEMENTED"