import smbus2 as smbus
import time
import json
import math
import os

# Constants for the LIS3MDL sensor magnetometer registers
LIS3MDL_ADDRESS = 0x1C
LIS3MDL_CTRL_REG1 = 0x20
LIS3MDL_CTRL_REG2 = 0x21
LIS3MDL_CTRL_REG3 = 0x22
LIS3MDL_CTRL_REG4 = 0x23
LIS3MDL_OUT_X_L = 0x28
LIS3MDL_OUT_X_H = 0x29
LIS3MDL_OUT_Y_L = 0x2A
LIS3MDL_OUT_Y_H = 0x2B
LIS3MDL_OUT_Z_L = 0x2C
LIS3MDL_OUT_Z_H = 0x2D
CALIBRATION_FILE = os.path.join(os.path.dirname(__file__), 'magnetometer_calibration.json')


class Magnetometer:
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.init_magnetometer()
        self.mag_min = [32767, 32767, 32767]
        self.mag_max = [-32768, -32768, -32768]
        self.load_calibration()

    def init_magnetometer(self):
        # Initialize the magnetometer
        self.bus.write_byte_data(LIS3MDL_ADDRESS, LIS3MDL_CTRL_REG1, 0b11011100)  # High performance, 80 Hz, Temp sensor enabled
        self.bus.write_byte_data(LIS3MDL_ADDRESS, LIS3MDL_CTRL_REG2, 0b00100000)  # ±8 gauss
        self.bus.write_byte_data(LIS3MDL_ADDRESS, LIS3MDL_CTRL_REG3, 0x00)  # Continuous-conversion mode

    def read_magnetometer_data(self):
        x = self.read_data(LIS3MDL_OUT_X_L, LIS3MDL_OUT_X_H)
        y = self.read_data(LIS3MDL_OUT_Y_L, LIS3MDL_OUT_Y_H)
        z = self.read_data(LIS3MDL_OUT_Z_L, LIS3MDL_OUT_Z_H)
        return x * 0.29, y * 0.29, z * 0.29

    def read_data(self, out_l, out_h):
        low = self.bus.read_byte_data(LIS3MDL_ADDRESS, out_l)
        high = self.bus.read_byte_data(LIS3MDL_ADDRESS, out_h)
        value = high << 8 | low
        return value if value < 32768 else value - 65536

    def calibrate(self):
        print("Rotate the magnetometer in all directions")
        try:
            while True:
                x, y, z = self.read_magnetometer_data()
                self.mag_min = [min(self.mag_min[i], v) for i, v in enumerate([x, y, z])]
                self.mag_max = [max(self.mag_max[i], v) for i, v in enumerate([x, y, z])]
                print(f"Min: {self.mag_min}, Max: {self.mag_max}")
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.save_calibration()

    def save_calibration(self):
        calibration_data = {'min': self.mag_min, 'max': self.mag_max}
        with open(CALIBRATION_FILE, 'w') as f:
            json.dump(calibration_data, f)
        print("Calibration data saved.")

    def load_calibration(self):
        try:
            with open(CALIBRATION_FILE, 'r') as f:
                calibration_data = json.load(f)
                self.mag_min = calibration_data['min']
                self.mag_max = calibration_data['max']
                print("Calibration data loaded.")
        except FileNotFoundError:
            print("Calibration file not found. Please calibrate the magnetometer.")

    def heading(self):
        x, y, z = self.read_magnetometer_data()
        heading = math.atan2(x, y)
        if heading < 0:
            heading += 2 * math.pi
        heading_degrees = math.degrees(heading)
        return heading_degrees


"""if __name__ == "__main__":
    mag = Magnetometer()

    #mag.calibrate()
    while True:
        x, y, z = mag.read_magnetometer_data()
        heading = mag.heading()
        print(heading)
        #print(f"X: {x}, Y: {y}, Z: {z}")
        time.sleep(1)"""
