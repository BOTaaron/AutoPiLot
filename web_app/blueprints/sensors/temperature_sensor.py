import smbus2

class TemperatureSensor:
    """
    Temperature sensor is included in the BerryGPS v4 as part of the IMU.
    Sensor included is an LSM6DSL and BMP388. Uses register on the BMP388 to enable the sensor,
    outputs to LSM6DSL registers.
    """
    def __init__(self, bus_number=1, bmp388_address=0x77, lsm6dsl_address=0x6a):
        self.bus = smbus2.SMBus(bus_number)
        self.bmp388_address = bmp388_address
        self.lsm6dsl_address = lsm6dsl_address
        self.enable_temperature_sensor()

    def enable_temperature_sensor(self):
        """
        Enable the temperature setting by setting the TEMP_EN bit in the PWR_CTRL register on the BMP388.
        For more info, the datasheet for this sensor is available at https://ozzmaker.com/wp-content/uploads/2020/08/lis3mdl.pdf
        """
        PWR_CTRL = 0x12 # Temperature sensor register
        TEMP_EN = 0x80  # Set bit 1 to enable the sensor
        current_value = self.bus.read_byte_data(self.bmp388_address, PWR_CTRL)
        new_value = current_value | TEMP_EN
        self.bus.write_byte_data(self.bmp388_address, PWR_CTRL, new_value)

    def read_temperature(self):
        """
        Temperature data is read from the OUT_L_TEMP and OUT_H_TEMP registers.
        The temperature is returned in LSB/C and must be converted into a readable unit.
        Read high and low bytes and combine before converting to celsius.
        """
        OUT_L_TEMP = 0x20 # Temperature output registers are at 0x20 and 0x21 as per Ozzmaker's datasheet
        OUT_H_TEMP = 0x21
        temp_l = self.bus.read_byte_data(self.lsm6dsl_address, OUT_L_TEMP)
        temp_h = self.bus.read_byte_data(self.lsm6dsl_address, OUT_H_TEMP)
        temp_raw = (temp_h << 8) | temp_l
        return self.convert_temp_to_celsius(temp_raw)

    def convert_temp_to_celsius(self, raw_temp):
        """Convert the 16-bit two's complement value to a signed integer"""
        if raw_temp & (1 << 15):
            raw_temp -= (1 << 16)
        temp_celsius = raw_temp / 256.0
        return temp_celsius

    def format_temperature(self, temp):
        # Format the temperature to 2 decimal places
        return "{:.2f}".format(temp) if temp % 1 != 0 else "{:.1f}".format(temp)


# Initialize sensor and read temperature
sensor = TemperatureSensor()
temperature = sensor.read_temperature()
formatted_temp = sensor.format_temperature(temperature)
print(f"Temperature: {formatted_temp} °C")