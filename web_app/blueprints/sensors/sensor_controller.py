from barometric_pressure import BarometricPressureSensor
from magnetometer import Magnetometer
from accelerometer import Accelerometer
from gyroscope import Gyroscope

class SensorController:
    def __init__(self):
        # initialise all the sensors
        self.barometric_sensor = BarometricPressureSensor()
        self.magnetometer = Magnetometer()
        self.accelerometer = Accelerometer()
        self.gyroscope = Gyroscope()

    def get_all_sensor_data(self):
        """
        Fetches data from all the sensors and returns it
        """
        temperature, pressure, altitude = self.barometric_sensor.get_temperature_and_pressure_and_altitude()
        mag_x, mag_y, mag_z = self.magnetometer.read_magnetometer()
        heading = self.magnetometer.calculate_heading(mag_x, mag_y)
        accel_x, accel_y, accel_z = self.accelerometer.read_accelerometer()
        gyro_x, gyro_y, gyro_z = self.gyroscope.read_gyro()

        return {
            "temperature": temperature,
            "pressure": pressure,
            "altitude": altitude,
            "magnetic_field": {"x": mag_x, "y": mag_y, "z": mag_z},
            "heading": heading,
            "acceleration": {"x": accel_x, "y": accel_y, "z": accel_z},
            "gyroscope": {"x": gyro_x, "y": gyro_y, "z": gyro_z}
        }


# Code used to test code. Running file will begin calibration/data output
if __name__ == "__main__":
    sensor_controller = SensorController()
    while True:
        all_sensors_data = sensor_controller.get_all_sensor_data()
        print(all_sensors_data)