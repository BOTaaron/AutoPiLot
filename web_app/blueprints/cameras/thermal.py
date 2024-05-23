import time
import numpy as np
import cv2
from flask import Flask, Response, Blueprint
import smbus2 as smbus
from MLX90640 import setup, get_frame, cleanup

app = Flask(__name__)

# Constants for the MLX90640
MLX90640_I2CADDR = 0x33
CHUNK_SIZE = 32

class ThermalCamera:
    def __init__(self):
        self.i2c_bus = smbus.SMBus(4)  # Use I2C bus 4
        time.sleep(2)
        setup(4)

    def generate_frames(self):
        try:
            while True:
                frame_data = get_frame()
                if frame_data is not None:
                    data_array = np.array(frame_data).reshape((24, 32))
                    data_array = cv2.normalize(data_array, None, 0, 255, cv2.NORM_MINMAX)
                    data_array = np.uint8(data_array)
                    data_array = cv2.applyColorMap(data_array, cv2.COLORMAP_JET)
                    _, jpeg = cv2.imencode('.jpg', data_array)
                    frame = jpeg.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
                    time.sleep(1)  # Maintain approximately 1 fps
                else:
                    print("Failed to get frame data")
        finally:
            cleanup()
