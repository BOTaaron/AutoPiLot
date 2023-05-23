'''
GNU GENERAL PUBLIC LICENSE
                       Version 3, 29 June 2007

 Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>
 Everyone is permitted to copy and distribute verbatim copies
 of this license document, but changing it is not allowed.

 This script is used to calibrate and test a brushless electric motor. 
 I am using an Overlander 1300KV outrunner motor along with a Hobbywing Skywalker 20A ESC with built-in BEC 2A@5V.
 It is possible this will work with other motor and ESC combos but I cannot make promises. I suggest checking
 your ESC manual and adjusting the pulses to what is stated there. 

 I have reprogrammed pin 12 to PWM using RPi.GPIO from pypi.org/project/RPi.GPIO. Feel free to give it a try 
 and let me know if any issues. I highly recommend removing the propellor while running the test.
 This uses software PWM.
'''

import RPi.GPIO as GPIO
from time import sleep

PWM = 12 # Set pin 12 to PWM for signal to ESC
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # Here we set the numbering system. We use BOARD as it is less confusing to use pin numbers rather than GPIO numbers
GPIO.setup(PWM, GPIO.OUT)

MIN_PULSES = 800
MAX_PULSES = 2000

pi_esc = GPIO.PWM(PWM, 0) # create a PWM object on pin 12 with 0 frequency
pi_esc.start(0)

print("If you are using the motor for the first time, type 'calibrate' and press enter")
print("If you just want to test the motor, check all connections and type 'go'. When done, disconnect the battery or type 'stop'.")

def calibrate():
    '''
    It is necessary to calibrate the ESC the first time it is used. On this particular ESC,
    the minimum pulses is around 800 and the maximum is 2000. It varies between different units, but is often 1000-2000 
    if you have no luck, try adjusting the values. It is usually set to the minimum value followed by the maximum
    '''
    print("You have selected to calibrate the ESC. Disconnect the battery from ESC and press enter to continue")
    selection = input()
    if selection == "":
        pi_esc.ChangeFrequency(MAX_PULSES)
        print("If the ESC is beeping, wait a couple of seconds and press enter")
        selection = input()
        if selection == "":
            pi_esc.ChangeFrequency(MIN_PULSES)
            print("Wait a few seconds for the ESC to calibrate")
            sleep(5)
            pi_esc.ChangeFrequency(0)
            sleep(2)
            pi_esc.ChangeFrequency(MIN_PULSES)
            sleep(1)
            selection = input("Calibration complete. Type 'go' to start the motor or 'stop' to exit here")
            if selection == "go":
                go()
            elif selection == "stop":
                stop()
            else:
                print("Sorry, what you typed is not a valid input.")

def go():
    '''
    This function is used to control the motor manually. '+' will increase pulses by 10, while '++' will increase by 100
    '-' will decrease pulses by 10 and '--' will decrease by 100. This will keep on running until 'stop' is entered into the console.
    As mentioned before, make sure no propellor is connected when testing as it can be dangerous.
    '''
    print("The motor should be starting in a moment...")

def stop():
    print("Stopping motor...")
