from flask import Blueprint

redundancies_route = Blueprint('redundancies_route', __name__)

@redundancies_route.route("/redundancies")
def get_redundancies():
    return "NOT IMPLEMENTED"