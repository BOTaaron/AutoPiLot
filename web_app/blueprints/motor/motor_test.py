import time
import RPi.GPIO as GPIO

ESC_GPIO = 23
MIN_PULSE_WIDTH = 1100
MAX_PULSE_WIDTH = 1940
FREQUENCY = 50
pwm = None
current_pulse_width = MIN_PULSE_WIDTH

def setup_gpio():
    global pwm
    if pwm is not None:
        cleanup_gpio()
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(ESC_GPIO, GPIO.OUT)
        pwm = GPIO.PWM(ESC_GPIO, FREQUENCY)
        pwm.start(0)
        print("GPIO setup success")
    except Exception as e:
        print(f"Failed to set up GPIO: {str(e)}")
        GPIO.cleanup()

def cleanup_gpio():
    global pwm
    if pwm:
        pwm.stop()
        pwm = None
    GPIO.cleanup()

def set_duty_cycle(pulse_width):
    global pwm, current_pulse_width
    current_pulse_width = pulse_width
    duty_cycle = (pulse_width / 20000.0) * 100
    pwm.ChangeDutyCycle(duty_cycle)

def calibrate():
    input("Set throttle to maximum and connect the battery. Press Enter to continue.")
    set_duty_cycle(MAX_PULSE_WIDTH)
    print("Waiting for ♪123 sound...")
    time.sleep(2)

    input("After hearing two short beeps, press Enter.")
    set_duty_cycle(MIN_PULSE_WIDTH)
    print("Throttle set to minimum. Waiting for completion...")
    time.sleep(2)
    print("Calibration complete. Listen for the number of LiPo cells and a long beep.")

def arm():
    print("Arming motor")
    set_duty_cycle(MIN_PULSE_WIDTH)
    time.sleep(1)
    print("Motor armed")

def start_motor():
    print("Starting motor")
    set_duty_cycle(MIN_PULSE_WIDTH + 200)
    time.sleep(1)
    print("Motor started")

def stop_motor():
    print("Stopping motor")
    pwm.ChangeDutyCycle(0)
    cleanup_gpio()
    print("Motor stopped")

def increase_power():
    global current_pulse_width
    new_pulse_width = min(MAX_PULSE_WIDTH, current_pulse_width + 100)
    set_duty_cycle(new_pulse_width)
    print(f"Increased power to {new_pulse_width}")

def decrease_power():
    global current_pulse_width
    new_pulse_width = max(MIN_PULSE_WIDTH, current_pulse_width - 100)
    set_duty_cycle(new_pulse_width)
    print(f"Decreased power to {new_pulse_width}")

def main():
    setup_gpio()
    while True:
        command = input("Enter command (calibrate, arm, start, stop, +, -): ").strip().lower()
        if command == "calibrate":
            calibrate()
        elif command == "arm":
            arm()
        elif command == "start":
            start_motor()
        elif command == "stop":
            stop_motor()
        elif command == "+":
            increase_power()
        elif command == "-":
            decrease_power()
        elif command == "exit":
            stop_motor()
            break
        else:
            print("Unknown command")

if __name__ == "__main__":
    main()
