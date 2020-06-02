from flask import Blueprint
routes = Blueprint('routes', __name__)

from .mininet import *
from .reachability import *
from .rules import *
