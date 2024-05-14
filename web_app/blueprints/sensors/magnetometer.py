import smbus2
import time
import math
import json
import numpy as np


class LIS3MDL:
    def __init__(self, i2c_bus=1, address=0x1C, calibration_file='magnetometer_calibration.json'):
        self.bus = smbus2.SMBus(i2c_bus)
        self.address = address
        self.sensitivity = 6842  # Sensitivity for FS=4 gauss
        self.calibration_file = calibration_file
        self.offsets = {'x': 0, 'y': 0, 'z': 0}
        self.init_magnetometer()
        self.load_calibration()

    def init_magnetometer(self):
        if self.bus.read_byte_data(self.address, 0x0F) != 0x3D:
            raise RuntimeError("LIS3MDL not found")
        self.bus.write_byte_data(self.address, 0x20, 0x70)  # Ultra-high-performance mode for X and Y, 80 Hz ODR
        self.bus.write_byte_data(self.address, 0x21, 0x00)  # +/-4 gauss
        self.bus.write_byte_data(self.address, 0x22, 0x00)  # Continuous-conversion mode
        self.bus.write_byte_data(self.address, 0x23, 0x0C)  # Ultra-high-performance mode for Z

    def read_magnetometer(self):
        x = self.read_axis(0x28, 0x29) - self.offsets['x']
        y = self.read_axis(0x2A, 0x2B) - self.offsets['y']
        z = self.read_axis(0x2C, 0x2D) - self.offsets['z']
        return x / self.sensitivity, y / self.sensitivity, z / self.sensitivity

    def read_axis(self, lsb_addr, msb_addr):
        lsb = self.bus.read_byte_data(self.address, lsb_addr)
        msb = self.bus.read_byte_data(self.address, msb_addr)
        value = msb << 8 | lsb
        if value > 32767:
            value -= 65536
        return value

    def calibrate(self, samples=500):
        """
        Calibrate sensor using number of samples from samples parameter.
        Rotate the Pi along all three axes in a slow figure of eight. Pitch, roll, and yaw.
        """
        print("Starting calibration...")
        max_vals, min_vals = {'x': -np.inf, 'y': -np.inf, 'z': -np.inf}, {'x': np.inf, 'y': np.inf, 'z': np.inf}
        for _ in range(samples):
            x, y, z = self.read_magnetometer() * self.sensitivity
            max_vals['x'], min_vals['x'] = max(max_vals['x'], x), min(min_vals['x'], x)
            max_vals['y'], min_vals['y'] = max(max_vals['y'], y), min(min_vals['y'], y)
            max_vals['z'], min_vals['z'] = max(max_vals['z'], z), min(min_vals['z'], z)
            time.sleep(0.02)
        self.offsets = {axis: (max_vals[axis] + min_vals[axis]) / 2 for axis in 'xyz'}
        self.save_calibration()

    def save_calibration(self):
        """
        Save calibration data to json file
        """
        with open(self.calibration_file, 'w') as f:
            json.dump(self.offsets, f)
        print("Calibration saved")

    def load_calibration(self):
        """
        Load calibration data from json file
        """
        try:
            with open(self.calibration_file, 'r') as f:
                self.offsets = json.load(f)
            print("Calibration loaded")
        except FileNotFoundError:
            print("No calibration file found. Please calibrate before proceeding.")
            self.calibrate()

    def calculate_heading(self, x, y):
        """
        Calculate heading of drone in degrees
        """
        heading = math.atan2(y, x)
        heading_degrees = math.degrees(heading)
        return heading_degrees + 360 if heading_degrees < 0 else heading_degrees


# output data for testing
if __name__ == '__main__':
    lis3mdl = LIS3MDL()
    while True:
        x, y, z = lis3mdl.read_magnetometer()
        print(f"Magnetic Field in X: {x}, Y: {y}, Z: {z}")
        heading = lis3mdl.calculate_heading(x, y)
        print(f"Heading: {heading} degrees")
        time.sleep(1)
