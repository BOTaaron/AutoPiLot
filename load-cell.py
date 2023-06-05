''' The script to test the thrust output of my Pi 4 using a load cell with HX711 amplifier
    VCC is analog voltage to power the amplifier and connected to pin 2 (5v) on the Pi
    GND is ground connected to GND pin 9 on the Pi
    DT pin is data pin and connected to GPIO5 (pin 29)
    Clock pin is connected to GPIO 6 (pin 31)'''

import RPi.GPIO as GPIO
from hx711 import HX711
from time import sleep


hx711 = HX711(
    dout_pin=5, #I have connected my signal with a yellow wire to GPIO5
    pd_sck_pin=6, #Serial clock input (SCK) is connected to GPIO6 with a white wire
    channel='A',
    gain=64
  )

hx711.reset() #Resets the HX711
measures = str(hx711.get_raw_data(1))
GPIO.cleanup()

print("\n" + measures)