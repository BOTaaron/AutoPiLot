import time
import RPi.GPIO as GPIO
import threading


class MotorController:
    _instance = None

    def __new__(cls, socketio, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MotorController, cls).__new__(cls, *args, **kwargs)
            cls._instance.socketio = socketio
        return cls._instance

    def __init__(self, socketio):
        if not hasattr(self, 'initialised'):
            self.ESC_GPIO = 23
            self.MIN_PULSE_WIDTH = 1100
            self.MAX_PULSE_WIDTH = 1940
            self.FREQUENCY = 50
            self.pwm = None
            self.current_pulse_width = self.MIN_PULSE_WIDTH
            self.setup_gpio()
            self.calibration_event = threading.Event()
            self.calibration_active = False
            self.socketio = socketio
            self.initialised = True
            self.setup_socket_listener()

    def setup_gpio(self):
        if self.pwm is not None:
            self.cleanup_gpio()
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.ESC_GPIO, GPIO.OUT)
            self.pwm = GPIO.PWM(self.ESC_GPIO, self.FREQUENCY)
            self.pwm.start(0)
            print("setup success")
        except Exception as e:
            print(f"Failed to set up GPIO: {str(e)}")
            GPIO.cleanup()

    def cleanup_gpio(self):
        if self.pwm:
            self.pwm.stop()
            self.pwm = None
        GPIO.cleanup()

    def set_duty_cycle(self, pulse_width):
        self.current_pulse_width = pulse_width
        duty_cycle = (pulse_width / 20000.0) * 100
        self.pwm.ChangeDutyCycle(duty_cycle)

    def set_duty_cycle(self, pulse_width):
        self.current_pulse_width = pulse_width
        duty_cycle = (pulse_width / 20000.0) * 100
        self.pwm.ChangeDutyCycle(duty_cycle)

    def calibrate(self):
        threading.Thread(target=self._calibrate).start()

    def _calibrate(self):
        try:
            self.socketio.emit('console_output', "Set throttle to maximum and connect the battery. Press Enter to continue.")
            self.wait_for_user_input()
            self.set_duty_cycle(self.MAX_PULSE_WIDTH)
            self.socketio.emit('console_output', "Waiting for ♪123 sound...")
            time.sleep(2)  # Wait for the user to hear the sound

            self.socketio.emit('console_output', "After hearing two short beeps, press Enter.")
            self.wait_for_user_input()
            self.set_duty_cycle(self.MIN_PULSE_WIDTH)
            self.socketio.emit('console_output', "Throttle set to minimum. Waiting for completion...")
            time.sleep(2)  # Wait for ESC to recognize the minimum throttle
            self.socketio.emit('console_output', "Calibration complete. Listen for the number of LiPo cells and a long beep.")
        except Exception as e:
            self.socketio.emit('console_output', f"Error during calibration: {str(e)}")

    def wait_for_user_input(self):
        self.calibration_event.clear()
        self.calibration_active = True
        self.calibration_event.wait()
        self.calibration_active = False

    def setup_socket_listener(self):
        @self.socketio.on('console_input')
        def handle_console_input(message):
            if self.calibration_active and message.strip().lower() == 'enter':
                self.socketio.emit('user_acknowledged')
                self.calibration_event.set()

    def arm(self):
        if not self.pwm:
            print("PWM not initialised, initialising...")
            self.setup_gpio()
        print("Arming motor")
        self.set_duty_cycle(self.MIN_PULSE_WIDTH)
        time.sleep(1)
        print("Motor armed")

    def arm(self):
        if not self.pwm:
            print("PWM not initialised, initialising...")
            self.setup_gpio()
        print("Arming motor")
        self.set_duty_cycle(self.MIN_PULSE_WIDTH)
        time.sleep(1)
        print("Motor armed")

    """Placeholder function, will later be changed to launch the drone"""
    def go(self, increase):
        if increase:
            new_pulse_width = min(self.MAX_PULSE_WIDTH, self.current_pulse_width + 100)
        else:
            new_pulse_width = max(self.MIN_PULSE_WIDTH, self.current_pulse_width - 100)
        self.set_duty_cycle(new_pulse_width)

    def stop(self):
        print("Stopping motor")
        self.pwm.ChangeDutyCycle(0)
        self.cleanup_gpio()

    def get_motor_data(self):
        percentage_output = (self.current_pulse_width - self.MIN_PULSE_WIDTH) / (self.MAX_PULSE_WIDTH - self.MIN_PULSE_WIDTH) * 100
        print(percentage_output)
        return percentage_output
