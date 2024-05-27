from flask import Blueprint, jsonify
from web_app.blueprints.motor.motor_manager import get_motor_controller

motor_bp = Blueprint('motor', __name__, url_prefix='/motor')


def create_motor_routes(socketio):
    motor_controller = get_motor_controller(socketio)

    @motor_bp.route('/calibrate', methods=['POST'])
    def calibrate():
        motor_controller.calibrate()
        return jsonify({'status': 'Calibration started'})

    @motor_bp.route('/arm', methods=['POST'])
    def arm():
        motor_controller.arm()
        return jsonify({'status': 'Arming complete'})

    @motor_bp.route('/go', methods=['POST'])
    def go():
        motor_controller.go(True)  # Assuming True for increasing throttle for simplicity
        return jsonify({'status': 'Motor running'})

    @motor_bp.route('/stop', methods=['POST'])
    def stop_motor():
        motor_controller.stop()
        return jsonify({'status': 'Motor stopped'})

    return motor_bp
