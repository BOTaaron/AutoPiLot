# AutoPiLot

AutoPiLot is an experimental project for university. The intention is to create a 3D printed plane that is piloted autonomously by a Raspberry Pi 5, along with a number of servos, brushless motor, IMU sensor board, and some cameras. The plane will use the GPS for location mapping and will search a target area using the thermal camera, followed by the video camera if it reads a target. 

To set up the GPS, follow the instructions at:

https://ozzmaker.com/berrygps-setup-guide-raspberry-pi/

# Requirements

## Python 3.11

#### Flask

Web framework used for rendering the app to control the drone

#### rpi-lgpio

Compatability package to provide compatibility with rpi-gpio on a Raspberry Pi 5

#### lgpio

Module to control the GPIO pins on the Raspberry Pi

#### Sphinx 

Used to create the documentation for the project

#### Requests

Allows HTTP requests to be sent

#### flask-socketio

Used to send commands to the Python terminal from the web app

#### smbus2

#### numpy


## System Wide Packages

#### gpsd, gpsmon, cgps

Used to convert NMEA GPS sentences into user readable data




