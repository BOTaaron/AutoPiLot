import smbus2 as smbus
import time
import json
import os

# Constants for the LSM6DSL sensor gyroscope registers
LSM6DSL_ADDRESS = 0x6A
LSM6DSL_CTRL2_G = 0x11
LSM6DSL_OUTX_L_G = 0x22
LSM6DSL_OUTX_H_G = 0x23
LSM6DSL_OUTY_L_G = 0x24
LSM6DSL_OUTY_H_G = 0x25
LSM6DSL_OUTZ_L_G = 0x26
LSM6DSL_OUTZ_H_G = 0x27
CALIBRATION_FILE = os.path.join(os.path.dirname(__file__), 'gyro_calibration.json')

class Gyroscope:
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.offsets = {'x': 0, 'y': 0, 'z': 0}
        self.init_gyro()
        self.load_calibration()

    def init_gyro(self):
        # ODR (Output Data Rate) = 416 Hz, 2000 dps full scale
        self.bus.write_byte_data(LSM6DSL_ADDRESS, LSM6DSL_CTRL2_G, 0b10011100)

    def calibrate_gyro(self, samples=100):
        """
        Calibrate gyroscope by taking average of 100 samples and averaging them
        """
        print("Calibrating gyroscope...")
        sum_x, sum_y, sum_z = 0, 0, 0
        for _ in range(samples):
            x, y, z = self.read_gyro_data()
            sum_x += x
            sum_y += y
            sum_z += z
            time.sleep(0.1)
        self.offsets['x'] = sum_x / samples
        self.offsets['y'] = sum_y / samples
        self.offsets['z'] = sum_z / samples
        self.save_calibration()
        print("Calibration complete.")

    def save_calibration(self):
        """
        Save calibration offsets to JSON file
        """
        with open(CALIBRATION_FILE, 'w') as f:
            json.dump(self.offsets, f)

    def load_calibration(self):
        """
        Load calibration offsets from JSON file
        """
        try:
            with open(CALIBRATION_FILE, 'r') as f:
                self.offsets = json.load(f)
            print("Calibration loaded.")
        except FileNotFoundError:
            print("Calibration file not found. Calibrating now.")
            self.calibrate_gyro()

    def read_gyro_data(self):
        """
        Gets gyroscope data and returns in degrees per second.
        """
        # Read the gyro raw data (16-bit values for each axis)
        x_low = self.bus.read_byte_data(LSM6DSL_ADDRESS, LSM6DSL_OUTX_L_G)
        x_high = self.bus.read_byte_data(LSM6DSL_ADDRESS, LSM6DSL_OUTX_H_G)
        y_low = self.bus.read_byte_data(LSM6DSL_ADDRESS, LSM6DSL_OUTY_L_G)
        y_high = self.bus.read_byte_data(LSM6DSL_ADDRESS, LSM6DSL_OUTY_H_G)
        z_low = self.bus.read_byte_data(LSM6DSL_ADDRESS, LSM6DSL_OUTZ_L_G)
        z_high = self.bus.read_byte_data(LSM6DSL_ADDRESS, LSM6DSL_OUTZ_H_G)

        # Combine high and low bytes
        x = x_high << 8 | x_low
        y = y_high << 8 | y_low
        z = z_high << 8 | z_low

        # Convert to signed values
        x = x if x < 32768 else x - 65536
        y = y if y < 32768 else y - 65536
        z = z if z < 32768 else z - 65536

        # Convert to degrees per second
        x_dps = x * 0.07
        y_dps = y * 0.07
        z_dps = z * 0.07

        return x_dps, y_dps, z_dps


