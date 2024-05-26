from flask import Blueprint, Response
# from web_app.blueprints.cameras.thermal import ThermalCamera
from web_app.blueprints.cameras.video import VideoCamera

camera_bp = Blueprint('camera', __name__, url_prefix='/camera')

thermal_camera = None
video_camera = None

"""def get_thermal_camera():
    
    create an instance of thermal camera if it does not exist
    
    global thermal_camera
    if thermal_camera is None:
        thermal_camera = ThermalCamera()
    return thermal_camera"""

"""@camera_bp.route('/thermal_feed')
def thermal_feed():
    
    generates frames using generate_frames() in thermal.py
    
    print("camera route used")
    camera = get_thermal_camera()
    return Response(camera.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')"""

def get_video_camera():
    global video_camera
    if video_camera is None:
        video_camera = VideoCamera()
    return video_camera

@camera_bp.route('/video_feed')
def video_feed():
    print("Video camera route used")
    camera = get_video_camera()
    return Response(camera.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')