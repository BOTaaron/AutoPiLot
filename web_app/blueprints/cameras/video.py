import io
import time
from PIL import Image
from picamera2 import Picamera2


class VideoCamera:
    """
    Class to get an image from the camera and display it to the web page.
    Since this project uses a Pi Camera Module v3, it is currently only supported by the libcamera stack.
    For this reason, the only current option is to use Picamera2 installed via pip, which is not recommended.
    This will likely change eventually.
    """
    def __init__(self):
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_preview_configuration(main={"size": (1920, 1080)}))
        self.picam2.start()
        print("Camera initialized successfully")

    def __del__(self):
        self.picam2.stop()
        self.picam2.close()

    def get_frame(self):
        """
        Returns the frames to be displayed on the page
        """
        frame = self.picam2.capture_array()
        if frame is not None:
            return frame
        else:
            print("Failed to capture frame")
            return None

    def generate_frames(self):
        """
        Generates frames for the video feed in the form of a JPEG
        """
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
            time.sleep(0.1)


