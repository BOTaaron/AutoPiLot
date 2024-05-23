from web_app.blueprints.motor.motor_controller import MotorController
from ...extensions import socketio

motor = MotorController(socketio)


def get_motor_controller():
    return motor
