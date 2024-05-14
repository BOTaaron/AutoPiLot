import smbus2
import json
import numpy as np
import time

class Gyroscope:
    def __init__(self, bus_number=1, address=0x6a, calibration_file='gyro_calibration.json'):
        self.bus = smbus2.SMBus(bus_number)
        self.address = address
        self.calibration_file = calibration_file
        self.gyro_offsets = {'x': 0, 'y': 0, 'z': 0}
        self.setup_gyroscope()
        self.load_calibration()

    def setup_gyroscope(self):
        """
        Set control register of gyroscope (CTRL2_G) and set output data rate (ODR)
        """
        CTRL2_G = 0x11
        ODR_G = 0x60
        self.bus.write_byte_data(self.address, CTRL2_G, ODR_G)

    def read_raw_gyro(self):
        """
        Raw data output by the gyroscope before calibration offsets are applied
        """
        OUTX_L_G = 0x22
        data = self.bus.read_i2c_block_data(self.address, OUTX_L_G, 6)
        x = (data[1] << 8) | data[0]
        y = (data[3] << 8) | data[2]
        z = (data[5] << 8) | data[4]
        if x > 32767:
            x -= 65536
        if y > 32767:
            y -= 65536
        if z > 32767:
            z -= 65536
        return x, y, z

    def calibrate_gyro(self, samples=500):
        """
        Calibrate the gyroscope and save result to json calibration file.
        Calibration assumes the device is on a perfectly flat surface, not moving.
        """
        print("Calibrating gyroscope...")
        offsets = {'x': 0, 'y': 0, 'z': 0}
        for _ in range(samples):
            x, y, z = self.read_raw_gyro()
            offsets['x'] += x
            offsets['y'] += y
            offsets['z'] += z
            time.sleep(0.01)
        self.gyro_offsets = {k: v / samples for k, v in offsets.items()}
        self.save_calibration()
        print("Calibration complete.")

    def save_calibration(self):
        """
        Write calibration data to json file
        """
        with open(self.calibration_file, 'w') as f:
            json.dump(self.gyro_offsets, f)
        print("Calibration data saved.")

    def load_calibration(self):
        """
        Load calibration data from json file
        """
        try:
            with open(self.calibration_file, 'r') as f:
                self.gyro_offsets = json.load(f)
            print("Calibration data loaded.")
        except FileNotFoundError:
            print("No calibration data found. Calibrating now.")
            self.calibrate_gyro()

    def read_gyro(self):
        """
        Read data from gyroscope, taking into account offsets from calibration file
        """
        x, y, z = self.read_raw_gyro()
        x -= self.gyro_offsets['x']
        y -= self.gyro_offsets['y']
        z -= self.gyro_offsets['z']
        return x, y, z

