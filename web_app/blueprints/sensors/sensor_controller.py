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
        self.gyroscope = Gyroscope()

    def get_acceleration(self):
        """
        Returns acceleration data in the form of Gs
        """
        accel_x, accel_y, accel_z = self.accelerometer.get_acceleration_data()
        return {"x": accel_x, "y": accel_y, "z": accel_z}

    def get_barometric_data(self):
        """
        Get data in the form of Celsius (temperature), hPa (pressure), metres (altitude)
        """
        temperature, pressure, altitude = self.barometric.get_temperature_and_pressure_and_altitude()
        return {"Temperature: ": temperature, "Pressure: ": pressure, "Altitude: ": altitude}

    def get_gyroscope_data(self):
        """
        Returns gyroscope data in the form of degrees per second
        """
        x, y, z = self.gyroscope.read_gyro_data()
        return {"X: ": x, "Y: ": y, "Z: ": z}


controller = SensorController()
acceleration = controller.get_acceleration()
barometric = controller.get_barometric_data()
gyro = controller.get_gyroscope_data()
print(acceleration)
print(barometric)
print(gyro)
