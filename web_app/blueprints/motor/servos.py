import RPi.GPIO as GPIO
import time


class Servo:
    """
    A class to control a servo motor using PWM on a Raspberry Pi.

    Attributes:
    gpio_pin (int): The GPIO pin number to which the servo is connected.
    pwm (PWM): The PWM instance for the servo.
    min_pulse_width (float): The minimum pulse width for the servo.
    max_pulse_width (float): The maximum pulse width for the servo.
    frequency (int): The frequency of the PWM signal.
    current_pulse_width (float): The current pulse width being sent to the servo.
    """

    def __init__(self, gpio_pin, min_pulse_width=0.5, max_pulse_width=2.5, frequency=50):
        """
        Initialize the Servo object with the given GPIO pin, pulse width range, and frequency.

        Parameters:
        gpio_pin (int): The GPIO pin number to which the servo is connected.
        min_pulse_width (float): The minimum pulse width for the servo. Default is 0.5 ms.
        max_pulse_width (float): The maximum pulse width for the servo. Default is 2.5 ms.
        frequency (int): The frequency of the PWM signal. Default is 50 Hz.
        """
        self.gpio_pin = gpio_pin
        self.min_pulse_width = min_pulse_width
        self.max_pulse_width = max_pulse_width
        self.frequency = frequency
        self.current_pulse_width = self.min_pulse_width

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.OUT)

        self.pwm = GPIO.PWM(self.gpio_pin, self.frequency)
        self.pwm.start(0)
        self.set_position(0)  # Initialize to the middle position

    def set_position(self, angle):
        """
        Set the position of the servo based on the given angle.

        Parameters:
        angle (float): The desired angle for the servo (from -90 to 90 degrees).
        """
        if angle < -90 or angle > 90:
            raise ValueError("Angle must be between -90 and 90 degrees")

        pulse_width = self.angle_to_pulse_width(angle)
        self.current_pulse_width = pulse_width
        duty_cycle = self.pulse_width_to_duty_cycle(pulse_width)
        self.pwm.ChangeDutyCycle(duty_cycle)

    def angle_to_pulse_width(self, angle):
        """
        Convert an angle to a pulse width.

        Parameters:
        angle (float): The desired angle for the servo (from -90 to 90 degrees).

        Returns:
        float: The corresponding pulse width in milliseconds.
        """
        # Map the angle to pulse width
        pulse_width_range = self.max_pulse_width - self.min_pulse_width
        pulse_width = self.min_pulse_width + (angle + 90) / 180 * pulse_width_range
        return pulse_width

    def pulse_width_to_duty_cycle(self, pulse_width):
        """
        Convert a pulse width to a duty cycle percentage.

        Parameters:
        pulse_width (float): The pulse width in milliseconds.

        Returns:
        float: The corresponding duty cycle percentage.
        """
        # Convert pulse width to duty cycle percentage
        duty_cycle = (pulse_width / (1000 / self.frequency)) * 100
        return duty_cycle

    def cleanup(self):
        """
        Stop the PWM signal and clean up the GPIO.
        """
        self.pwm.stop()
        GPIO.cleanup(self.gpio_pin)