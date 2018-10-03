#!/usr/bin/env python
# -*- coding: UTF-8 -*-

""" heatercontroller.py: Contains HeaterController class that provides and interface to
    IO to a heater for the IOThermostat package """

import RPi.GPIO as GPIO
#from PID import PID
print("IOThermostat: WARNING: heatercontroller.py: using notPID  instead of PID")
from notPID import PID

__author__ = "Jan Bonne Aans"
__copyright__ = "Copyright 2018, Jan Bonne Aans"
__credits__ = []
__license__ = "GPLv3"
__version__ = "1"
__maintainer__ = "Jan Bonne Aans"
__email__ = "jbaans-at-gmail.com"
__status__ = "Development"

class HeaterController:


    gpio_state = None
    GPIO_PIN = None
    pid = None

    def __init__(self):

        print('IOThermostat: Starting Heater Controller..')

        self.gpio_state = GPIO.LOW
        self.GPIO_PIN = 12 # this can be 23 as well
        self.pid = None

        # PID feedback settings
        # Best Kp,Ki and Kd depend on the room thermodynamics
        # Note: the system is slow and overshoot should be very low
        Kp = 1.2
        Ki = 1
        Kd = 0.001
        pid_sample_time = 3 # seconds
        pid_windup = 20

        # create PID controller
        self.pid = PID(Kp, Ki, Kd)
        self.pid.setSampleTime(pid_sample_time)
        self.pid.setWindup(pid_windup)

        # initialise GPIO
        self.openGPIO()

        print('IOThermostat: Heater Controller active.')


    def update(self,temperature,targettemperature):

        self.pid.setSetPoint(targettemperature)
        self.pid.update(temperature)

        #print("HeaterController: PID output = {}".format(self.pid.output))

        #TODO this seems to be a bug. Expecting:
        # if (self.pid.output < targettemperature) and self.isEnabled():
        #    self.enableHeater(False)
        if (self.pid.output > targettemperature) and self.isHeaterEnabled():
            self.enableHeater(False)
        elif (self.pid.output < targettemperature) and not self.isHeaterEnabled():
            self.enableHeater(True)


    def enableHeater(self,enable):
        if enable and not self.isHeaterEnabled():
            # turn off
            self.gpio_state = GPIO.HIGH
        elif not enable and self.isHeaterEnabled():
            # turn on
            self.gpio_state = GPIO.LOW        

        print('IOThermostat: GPIO.output({},{})'.format(self.GPIO_PIN, self.gpio_state))
        GPIO.output(self.GPIO_PIN, self.gpio_state)

    def isHeaterEnabled(self):
        if self.gpio_state == GPIO.LOW:
            return False
        elif self.gpio_state == GPIO.HIGH:
            return True
        else:
            raise ValueError('gpio_state has an unexpected value: {}'.format(self.gpio_state))

    def openGPIO(self):
        # setup the gpio pin for heating
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.GPIO_PIN, GPIO.OUT)

    # call this function when closing
    def close(self):
        GPIO.cleanup()
        print('IOThermostat: Stopped Heater Controller.')
