import smbus2
import json
import time


class Accelerometer:
    def __init__(self, bus_number=1, address=0x6a, calibration_file='accelerometer_calibration.json'):
        self.bus = smbus2.SMBus(bus_number)
        self.address = address
        self.calibration_file = calibration_file
        self.accelerometer_offsets = {'x': 0, 'y': 0, 'z': 0}
        self.setup_accelerometer()
        self.load_calibration()

    def setup_accelerometer(self):
        """
        Set control register of accelerometer (CTRL1_XL) and set output data rate (ODR)
        """
        CTRL1_XL = 0x10
        ODR_XL = 0x60
        self.bus.write_byte_data(self.address, CTRL1_XL, ODR_XL)

    def calibrate_accel(self, samples=500):
        """
        Calibrate device on each of 6 axes. May be good idea to tape Pi inside a cube and lay flat on each side.
        """
        print("Calibrating accelerometer...")
        offsets = {'x': 0, 'y': 0, 'z': 0}
        for _ in range(samples):
            x, y, z = self.read_raw_accelerometer()
            offsets['x'] += x
            offsets['y'] += y
            offsets['z'] += z
            time.sleep(0.01)
        self.accelerometer_offsets = {k: v / samples for k, v in offsets.items()}
        self.save_calibration()
        print("Calibration complete.")

    def save_calibration(self):
        """
        Save calibration data to a json file
        """
        with open(self.calibration_file, 'w') as f:
            json.dump(self.accelerometer_offsets, f)
        print("Calibration data saved.")

    def load_calibration(self):
        """
        Load calibration data from a json file
        """
        try:
            with open(self.calibration_file, 'r') as f:
                self.accelerometer_offsets = json.load(f)
            print("Calibration data loaded.")
        except FileNotFoundError:
            print("No calibration data found. Calibrating now.")
            self.calibrate_accel()



    def read_raw_accelerometer(self):
        """
        Read accelerometer output before calibration offset is applied
        """
        OUTX_L_XL = 0x28
        data = self.bus.read_i2c_block_data(self.address, OUTX_L_XL, 6)
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

    def read_accelerometer(self):
        """
        Read data from the accelerometer while making adjustments for offsets
        """
        x, y, z = self.read_raw_accelerometer()
        x -= self.accelerometer_offsets['x']
        y -= self.accelerometer_offsets['y']
        z -= self.accelerometer_offsets['z']
        return x, y, z


accelerometer = Accelerometer()
accelerometer_data = accelerometer.read_accelerometer()

print("Accelerometer data: ", accelerometer_data)