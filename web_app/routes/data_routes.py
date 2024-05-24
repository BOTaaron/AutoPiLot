from flask import Blueprint, jsonify
from web_app.blueprints.sensors.sensor_controller import SensorController
from web_app.blueprints.motor.motor_manager import get_motor_controller

data_bp = Blueprint('data', __name__, url_prefix='/data')
controller = SensorController()
motor_controller = get_motor_controller()


@data_bp.route('/motor_output', methods=['GET'])
def motor_output():
    """
    get the motor output to display in the gauge, calculating a % from duty cycle
    """
    output = motor_controller.get_motor_data()
    return jsonify({'motor_output': output})


@data_bp.route('/acceleration')
def get_acceleration():
    """
    get the accelerometer data to display on the web page
    """
    return jsonify(controller.get_acceleration())


@data_bp.route('/barometric')
def get_barometric_data():
    """
    get data from the barometric pressure sensor to display on the web page
    """
    temperature, pressure, altitude = controller.get_barometric_data()
    print(altitude)
    return jsonify({
        'temperature': temperature,
        'pressure': pressure,
        'altitude': altitude
    })


@data_bp.route('/gyroscope')
def get_gyroscope_data():
    """
    get data from the gyroscope to display on the web page
    """
    return jsonify(controller.get_gyroscope_data())