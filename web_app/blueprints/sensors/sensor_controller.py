from barometric_pressure import BarometricPressureSensor
from magnetometer import Magnetometer
from accelerometer import Accelerometer
from gyroscope import Gyroscope
from gps_sensor import GPS


class SensorController:
    """
    Class to return sensor data to be accessed by other parts of the project
    """
    def __init__(self):
        # initialise all the sensors
        self.accelerometer = Accelerometer()
        self.barometric = BarometricPressureSensor()

    def get_acceleration(self):
        accel_x, accel_y, accel_z = self.accelerometer.get_acceleration_data()
        return {"x": accel_x, "y": accel_y, "z": accel_z}

    def get_barometric_data(self):
        temperature, pressure, altitude = self.barometric.get_temperature_and_pressure_and_altitude()
        return {"Temperature: ": temperature, "Pressure: ": pressure, "Altitude: ": altitude}


controller = SensorController()
acceleration = controller.get_acceleration()
barometric = controller.get_barometric_data()
print(acceleration)
print(barometric)
