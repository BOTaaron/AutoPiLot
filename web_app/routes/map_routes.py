from flask import render_template
from web_app.blueprints.maps import maps_bp

@maps_bp.route('/large_map')
def large_map():
    return render_template('large_map.html')
