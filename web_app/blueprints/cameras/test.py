import smbus2 as smbus
import time

MLX90640_I2CADDR = 0x33
bus = smbus.SMBus(4)

try:
    # Write a test command to the sensor
    bus.write_byte(MLX90640_I2CADDR, 0x00)
    print("I2C communication successful.")
except Exception as e:
    print("I2C communication error: ", e)
finally:
    bus.close()