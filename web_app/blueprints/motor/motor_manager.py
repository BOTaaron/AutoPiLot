from web_app.blueprints.motor.motor_controller import MotorController


def get_motor_controller(socketio):
    return MotorController(socketio)
