import io
import time
from PIL import Image
from picamera2 import Picamera2


class VideoCamera:
    def __init__(self):
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_preview_configuration(main={"size": (640, 480)}))
        self.picam2.start()
        print("Camera initialized successfully")

    def __del__(self):
        self.picam2.stop()
        self.picam2.close()

    def get_frame(self):
        frame = self.picam2.capture_array()
        if frame is not None:
            return frame
        else:
            print("Failed to capture frame")
            return None

    def generate_frames(self):
        while True:
            frame = self.get_frame()
            if frame is not None:
                # Convert the frame to JPEG format
                image = Image.fromarray(frame).convert("RGB")
                with io.BytesIO() as output:
                    image.save(output, format="JPEG")
                    jpeg = output.getvalue()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + jpeg + b'\r\n\r\n')
            else:
                print("Failed to capture video frame")
            time.sleep(0.1)  # Maintain an appropriate frame rate


