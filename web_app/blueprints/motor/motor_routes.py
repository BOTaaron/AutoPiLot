from flask import Blueprint, jsonify
from .motor_controller import MotorController


motor_bp = Blueprint('motor', __name__, url_prefix='/motor')

# Create an instance of MotorController
motor_controller = None


def get_motor_controller():
    global motor_controller
    if motor_controller is None:
        motor_controller = MotorController()
        motor_controller.setup_gpio()
    return motor_controller


@motor_bp.route('/calibrate', methods=['POST'])
def calibrate():
    motor = get_motor_controller()
    motor.calibrate()
    return jsonify({'status': 'Calibration started'})


@motor_bp.route('/arm', methods=['POST'])
def arm():
    motor = get_motor_controller()
    motor.arm()
    return jsonify({'status': 'Arming complete'})


@motor_bp.route('/go', methods=['POST'])
def go():
    motor = get_motor_controller()
    motor.go(True)  # Assuming True for increasing throttle for simplicity
    return jsonify({'status': 'Motor running'})


@motor_bp.route('/stop', methods=['POST'])
def stop_motor():
    motor = get_motor_controller()
    motor.stop()
    return jsonify({'status': 'Motor stopped'})
