from servos import Servo

aileron_left = Servo(gpio_pin=21)
aileron_right = Servo(gpio_pin=23)
rudder = Servo(gpio_pin=26)
elevator = Servo(gpio_pin=12)