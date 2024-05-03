import time
import RPi.GPIO as GPIO


class MotorController:
    def __init__(self):
        self.ESC_GPIO = 23
        self.MIN_PULSE_WIDTH = 770
        self.MAX_PULSE_WIDTH = 2000
        self.FREQUENCY = 50
        self.pwm = None
        self.setup_gpio()

    def setup_gpio(self):
        if self.pwm is not None:
            self.cleanup_gpio()
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.ESC_GPIO, GPIO.OUT)
            self.pwm = GPIO.PWM(self.ESC_GPIO, self.FREQUENCY)
            self.pwm.start(0)
        except Exception as e:
            print(f"Failed to set up GPIO: {str(e)}")
            GPIO.cleanup()

    def cleanup_gpio(self):
        if self.pwm:
            self.pwm.stop()
            self.pwm = None
        GPIO.cleanup()

    def set_duty_cycle(self, pulse_width):
        duty_cycle = (pulse_width / 20000.0) * 100
        self.pwm.ChangeDutyCycle(duty_cycle)

    def calibrate(self):
        self.set_duty_cycle(self.MAX_PULSE_WIDTH)
        time.sleep(2)
        self.set_duty_cycle(self.MIN_PULSE_WIDTH)
        time.sleep(2)
        print("Calibration Complete")

    def arm(self):
        if not self.pwm:
            print("PWM not initialised, initialising...")
            self.setup_gpio()
        print("Arming motor")
        self.setup_gpio()
        self.set_duty_cycle(self.MIN_PULSE_WIDTH)
        time.sleep(1)
        print("Motor armed")

    """Placeholder function, will later be changed to launch the drone"""
    def go(self, increase):
        if increase:
            new_duty = min(self.MAX_PULSE_WIDTH, self.current_duty + 100)
        else:
            new_duty = max(self.MIN_PULSE_WIDTH, self.current_duty - 100)
        self.set_duty_cycle(new_duty)

    def stop(self):
        print("Stopping motor")
        self.pwm.ChangeDutyCycle(0)
        self.cleanup_gpio()



