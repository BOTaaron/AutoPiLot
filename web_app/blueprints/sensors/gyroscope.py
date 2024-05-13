import smbus2


class Gyroscope:
    def __init__(self, bus_number=1, address=0x6a):
        self.bus = smbus2.SMBus(bus_number)
        self.address = address
        self.setup_gyroscope()

    def setup_gyroscope(self):
        """
        Set control register of gyroscope (CTRL2_G) and set output data rate (ODR)
        """
        CTRL2_G = 0x11
        ODR_G = 0x60
        self.bus.write_byte_data(self.address, CTRL2_G, ODR_G)

    def read_gyro(self):
        """
        Read the data from output registers in the form of x, y, z coordinates
        """
        OUTX_L_G = 0x22
        data = self.bus.read_i2c_block_data(self.address, OUTX_L_G, 6)
        x = data[0] | (data[1] << 8)
        y = data[2] | (data[3] << 8)
        z = data[4] | (data[5] << 8)
        return x, y, z


gyro = Gyroscope()
gyroscope_data = gyro.read_gyro()
print("Gyro data:", gyroscope_data)