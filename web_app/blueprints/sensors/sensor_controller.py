import time
import numpy as np
from flight_system.kalman_filter import KalmanFilterOrientation
from web_app.blueprints.sensors.barometric_pressure import BarometricPressureSensor
from web_app.blueprints.sensors.magnetometer import Magnetometer
from web_app.blueprints.sensors.accelerometer import Accelerometer
from web_app.blueprints.sensors.gyroscope import Gyroscope




class SensorController:
    """
    Class to return sensor data to be accessed by other parts of the project
    """
    def __init__(self):
        # initialise all the sensors
        self.accelerometer = Accelerometer()
        self.barometric = BarometricPressureSensor()
        self.magnetometer = Magnetometer()
        self.gyroscope = Gyroscope()
        self.kalman_filter = KalmanFilterOrientation(dt=0.01)

    def get_acceleration(self):
        """
        Returns acceleration data in the form of Gs
        """
        accel_x, accel_y, accel_z = self.accelerometer.get_acceleration_data()
        return np.array([accel_x, accel_y, accel_z])

    def get_barometric_data(self):
        """
        Get data in the form of Celsius (temperature), hPa (pressure), metres (altitude)
        """

        temperature, pressure, altitude = self.barometric.get_temperature_and_pressure_and_altitude()
        return temperature, pressure, altitude

    def get_gyroscope_data(self):
        """
        Returns gyroscope data in the form of degrees per second
        """
        gyro_x, gyro_y, gyro_z = self.gyroscope.read_gyro_data()
        return np.radians(np.array([gyro_x, gyro_y, gyro_z]))  # Convert to radians per second

    def get_magnetometer_data(self):
        """
        get data from the magnetometer in the form of milligauss
        """
        mag_x, mag_y, mag_z = self.magnetometer.read_magnetometer_data()
        return np.array([mag_x, mag_y, mag_z])

    def get_orientation(self):
        """
        return the orientation of each axis from combined IMU sensors
        """
        accelerometer = self.get_acceleration()
        gyroscope = self.get_gyroscope_data()
        magnetometer = self.get_magnetometer_data()
        roll, pitch, yaw = self.kalman_filter.update_orientation(accelerometer, gyroscope, magnetometer)
        return pitch, roll, yaw

if __name__ == "__main__":
    sensor_controller = SensorController()

    while True:

        pitch, roll, yaw = sensor_controller.get_orientation()
        print(f"Pitch: {pitch}, Roll: {roll}, Yaw: {yaw}")
        time.sleep(0.01)


