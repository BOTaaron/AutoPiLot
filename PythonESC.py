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
import lgpio
from time import sleep


pinNumber = 18 # Set GPIO 18/Pin 12 to PWM for signal to ESC
handle = lgpio.gpiochip_open(0) # if OK this will return 0, otherwise negative number is an error
MIN_PULSES = 770
MAX_PULSES = 2000



print("If you are using the motor for the first time, type 'calibrate' and press enter\n")
print("If you just want to test the motor, check all connections and type 'go'. When done, disconnect the battery or type 'stop'.\n")

def calibrate():
    '''
    It is necessary to calibrate the ESC the first time it is used. On this particular ESC,
    the minimum pulses is around 800 and the maximum is 2000. It varies between different units, but is often 1000-2000 
    if you have no luck, try adjusting the values. It is usually set to the minimum value followed by the maximum
    '''
    print("You have selected to calibrate the ESC. Disconnect the battery from ESC and press enter to continue\n")
    selection = input()
    if selection == "":
        lgpio.tx_servo(handle, pinNumber, MAX_PULSES, 80)
        print("Reconnect the battery. Press enter when done.")
        selection = input()
        print("Your 'throttle' is set to max. Press enter when the ESC beeps.")
        sleep(4) # for my motor in particular the throttle must be set to max for 2 seconds. This is represented by max pulses of 2000. The ESC expects to hold for 2 seconds.
        selection = input()
        if selection == "":
            lgpio.tx_servo(handle, pinNumber, MIN_PULSES, 80)
            print("Your 'throttle' is now set to minimum. The ESC will beep the number of battery cells present. In my case, this is 3 beeps.")
            sleep(6)
            lgpio.tx_servo(handle, pinNumber, 0, 80)
            sleep(2)
            lgpio.tx_servo(handle, pinNumber, MIN_PULSES, 80)
            print("A long beep should have played, If not, something went wrong.")
            sleep(1)
            selection = input("Calibration complete. Type 'go' to start the motor or 'stop' to exit here\n")
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
    arm()
    print("The motor should be starting in 3 seconds, ensure the area is clear...")
    sleep(3)
    pulses = MIN_PULSES
    print("Entering '-' or '--' will decrease pulses by 10 or 100. Entering '+' or '++' will increase them by 100.")
    print("If you would like to stop the motor, simply type 'stop'")
    print(f"Your starting pulse is {pulses}")

    while True:
        selection = input()
        lgpio.tx_servo(handle, pinNumber, pulses, 50)
        if selection == '-':
            pulses -= 10
            print(f"Your pulse number is now {pulses}")
        elif selection =='--':
            pulses -= 100
            print(f"Your pulse number is now {pulses}")
        elif selection == '+':
            pulses += 10
            print(f"Your pulse number is now {pulses}")
        elif selection == '++':
            pulses += 100
            print(f"Your pulse number is now {pulses}")
        elif selection == 'stop':
            stop()
            
def arm():
    lgpio.tx_servo(handle, pinNumber, MIN_PULSES, 50)

def stop():
    print("Stopping motor...")
    lgpio.gpiochip_close(handle)


userInput = input()
if userInput == 'calibrate':
    calibrate()
elif userInput == 'go':
    go()
elif userInput == 'stop':
    stop()
    sleep(5)
    exit(0)
elif userInput == 'arm':
    arm()
