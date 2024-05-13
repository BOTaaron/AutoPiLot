import smbus2

class Accelerometer:
    def __init__(self, bus_number=1, address=0x6a):
        self.bus = smbus2.SMBus(bus_number)
        self.address = address
        self.setup_accelerometer()

    def setup_accelerometer(self):
        """
        Set control register of accelerometer (CTRL1_XL) and set output data rate (ODR)
        """
        CTRL1_XL = 0x10
        ODR_XL = 0x60
        self.bus.write_byte_data(self.address, CTRL1_XL, ODR_XL)

    def read_accelerometer(self):
        """
        Read the data from output registers in the form of x, y, z coordinates
        """
        OUTX_L_XL = 0x28
        data = self.bus.read_i2c_block_data(self.address, OUTX_L_XL, 6)
        x = data[0] | (data[1] << 8)
        y = data[2] | (data[3] << 8)
        z = data[4] | (data[5] << 8)
        return x, y, z


accelerometer = Accelerometer()
accelerometer_data = accelerometer.read_accelerometer()

print("Accelerometer data: ", accelerometer_data)