
import time
from RPi import GPIO


ESC_GPIO = 23  # GPIO pin connected to the ESC signal line
MIN_PULSE_WIDTH = 770  # Minimum pulse width in milliseconds
MAX_PULSE_WIDTH = 2000  # Maximum pulse width in milliseconds
FREQUENCY = 50  # Frequency for PWM signal (50Hz is common for servos and ESCs)

GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
GPIO.setup(ESC_GPIO, GPIO.OUT)

pwm = GPIO.PWM(ESC_GPIO, FREQUENCY)  # Create PWM instance with frequency
pwm.start(0)  # Initialize with 0 duty cycle


def set_duty_cycle(pulse_width):
    duty_cycle = (pulse_width / 20000.0) * 100
    pwm.ChangeDutyCycle(duty_cycle)


def calibrate():
    print("Calibration Start")

    # 1. Move throttle stick to the top position (simulate max throttle)
    print("Setting throttle to maximum. Please connect the battery now, then press Enter.")
    input()
    set_duty_cycle(MAX_PULSE_WIDTH)
    time.sleep(2)  # Wait for the ESC to initialize

    # 2. Wait for the "Beep-Beep-" tone
    print("The top point of throttle range has been confirmed. Press Enter to continue.")
    input()

    # 3. Move throttle stick to the bottom position (simulate min throttle)
    print("Setting throttle to minimum. Wait for several 'beep-' tones indicating the battery cells.")
    set_duty_cycle(MIN_PULSE_WIDTH)
    time.sleep(2)  # Give the user time to count the beeps for battery cells

    # 4. Confirmation of the lowest point
    print(
        "Wait for a long 'Beep-' tone indicating the lowest point of throttle range has been confirmed, then press Enter.")
    input()
    print("Calibration completed.")
    pwm.stop()  # Stop PWM after calibration


def arm():
    print("Arming ESC. Ensure throttle is at minimum.")
    # Ensuring the throttle (simulated by PWM pulse width) is at its minimum.
    set_duty_cycle(MIN_PULSE_WIDTH)
    time.sleep(1)  # Wait a bit before powering ESC to ensure it detects this as the minimum position.
    print("Please connect the battery now. Waiting for special tone indicating power supply is OK.")
    input("Press Enter after hearing the tone.")
    print("Waiting for the number of 'beep-' tones indicating battery cells.")
    time.sleep(2)  # Give user time to observe and count the beeps for battery cells.
    print("Waiting for the long 'beep-----' tone indicating the self-test is finished.")
    input("Press Enter after hearing the long 'beep' tone.")
    print("ESC is now armed. Ready to go flying.")
    print("Use the 'go' command to start the motor.")


def go():
    print("Ready to increase throttle. Use '+' or '++' to increase, '-' or '--' to decrease. Type 'stop' to end.")
    pwm.start(0)  # Re-initializing PWM in case it was stopped.
    pulses = MIN_PULSE_WIDTH  # Ensuring we start at minimum throttle.
    set_duty_cycle(pulses)  # Apply the minimum pulse width to ensure it's properly set.
    try:
        while True:
            command = input("Command (+, ++, -, --, stop): ")
            if command == '+':
                pulses += 10
                # Increase pulse width by 10
            elif command == '++':
                pulses += 100
                # Increase pulse width by 100
            elif command == '-':
                pulses -= 10
                # Decrease pulse width by 10
            elif command == '--':
                pulses -= 100
                # Decrease pulse width by 100
            elif command == 'stop':
                break
    except KeyboardInterrupt:
        pass
    finally:
        pwm.stop()
        GPIO.cleanup()


userInput = input("Enter 'calibrate', 'arm', or 'go': ")
if userInput == 'calibrate':
    calibrate()
elif userInput == 'arm':
    arm()
elif userInput == 'go':
    go()
