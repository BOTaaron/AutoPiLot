''' The script to test the thrust output of my Pi 4 using a load cell with HX711 amplifier
    VCC is analog voltage to power the amplifier and connected to pin 2 (5v) on the Pi
    GND is ground connected to GND pin 9 on the Pi
    DT pin is data pin and connected to GPIO5 (pin 29)
    Clock pin is connected to GPIO 6 (pin 31)'''

import RPi.GPIO