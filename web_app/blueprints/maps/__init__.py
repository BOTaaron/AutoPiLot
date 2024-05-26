from flask import Blueprint

maps_bp = Blueprint('maps', __name__, template_folder='../../templates', static_folder='../../static')
