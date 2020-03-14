from flask import Blueprint
routes = Blueprint('routes', __name__)

from .conflicts import *
from .mininet import *
from .reachability import *
from .redundancies import *
