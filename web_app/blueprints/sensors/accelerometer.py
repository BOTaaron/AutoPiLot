import smbus2
import time
import json
import os


class Accelerometer:
    """
    Adapted from Ozzmaker's repository for the BerryGPS IMU at https://github.com/ozzmaker/BerryIMU/tree/master/python-BerryIMU-measure-G.
    Since it uses a BerryGPS v4 redundant code has been removed to only include what is needed.
    Accelerometer included in LSM6DSL sensor with datasheet available at https://ozzmaker.com/wp-content/uploads/2020/08/lsm6dsl-datasheet.pdf
    """
    LSM6DSL_ADDRESS = 0x6A  # Address of LSM6DSL
    LSM6DSL_WHO_AM_I = 0x0F
    LSM6DSL_CTRL1_XL = 0x10
    LSM6DSL_CTRL3_C = 0x12
    LSM6DSL_OUTX_L_XL = 0x28
    LSM6DSL_OUTX_H_XL = 0x29
    LSM6DSL_OUTY_L_XL = 0x2A
    LSM6DSL_OUTY_H_XL = 0x2B
    LSM6DSL_OUTZ_L_XL = 0x2C
    LSM6DSL_OUTZ_H_XL = 0x2D
    CALIBRATION_FILE = os.path.join(os.path.dirname(__file__), 'accelerometer_calibration.json')

    def __init__(self):
        self.bus = smbus2.SMBus(1)
        if not self.init_imu():
            raise Exception("Failed to initialize LSM6DSL")
        self.offsets = self.load_calibration()

    def write_byte(self, register, value):
        self.bus.write_byte_data(self.LSM6DSL_ADDRESS, register, value)

    def read_accelerometer(self):
        data = self.bus.read_i2c_block_data(self.LSM6DSL_ADDRESS, self.LSM6DSL_OUTX_L_XL, 6)
        x, y, z = [(data[i+1] << 8) | data[i] for i in range(0, 6, 2)]
        x, y, z = [n if n < 32768 else n - 65536 for n in [x, y, z]]
        return x * 0.061 / 1000, y * 0.061 / 1000, z * 0.061 / 1000

    def init_imu(self):
        who_am_i = self.bus.read_byte_data(self.LSM6DSL_ADDRESS, self.LSM6DSL_WHO_AM_I)
        if who_am_i != 0x6A:
            print("LSM6DSL not found")
            return False
        self.write_byte(self.LSM6DSL_CTRL1_XL, 0x60)
        self.write_byte(self.LSM6DSL_CTRL3_C, 0x44)
        return True

    def calibrate_accel(self, samples=500):
        """
        Calibrate the accelerometer and save offsets to a JSON file.
        To calibrate, orient the device on each axis as directed.
        Easiest way may be to strap the Pi inside a box and lay it flat and still on each side.
        """
        orientations = ["front", "back", "left", "right", "top", "bottom"]
        calibration_data = {'x': 0, 'y': 0, 'z': 0}

        for orientation in orientations:
            input(f"Place the accelerometer with the {orientation} side facing up and press Enter to continue...")
            offsets = {'x': 0, 'y': 0, 'z': 0}
            for _ in range(samples):
                x, y, z = self.read_accelerometer()
                offsets['x'] += x
                offsets['y'] += y
                offsets['z'] += z
                time.sleep(0.01)

            # Calculate the average for this orientation
            offsets = {k: v / samples for k, v in offsets.items()}
            print(f"Offsets for {orientation}: {offsets}")

            # Accumulate the offsets for averaging later
            calibration_data['x'] += offsets['x']
            calibration_data['y'] += offsets['y']
            calibration_data['z'] += offsets['z']

        # Calculate overall averages
        calibration_data = {k: v / len(orientations) for k, v in calibration_data.items()}

        # Save the calibration data
        with open(self.CALIBRATION_FILE, 'w') as f:
            json.dump(calibration_data, f)
        print("Calibration complete and saved to", self.CALIBRATION_FILE)

    def load_calibration(self):
        """
        Load the calibration offsets from a JSON file
        """
        try:
            with open(self.CALIBRATION_FILE, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("No calibration file found. Calibrating now.")
            return None

    def get_acceleration_data(self):
        """
        Return the acceleration data in Gs, taking into account any offset data
        """
        x, y, z = self.read_accelerometer()
        x -= self.offsets['x']
        y -= self.offsets['y']
        z -= self.offsets['z']
        return x, y, z
