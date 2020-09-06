#!/usr/bin/env python
# -*- coding: UTF-8 -*-

""" heatercontroller.py: Contains HeaterController class that provides and interface to
    IO to a heater for the IOThermostat package """

import asyncio
print("IOThermostat: WARNING: heatercontroller.py: using pyotgw for opentherm communication")
from pyotgw import pyotgw
import RPi.GPIO as GPIO
from PID import PID
from notPID import PID as notPID

__author__ = "Jan Bonne Aans"
__copyright__ = "Copyright 2020, Jan Bonne Aans"
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

        print("IOThermostat: WARNING: heatercontroller.py: assuming OpenTherm Gateway serial controller on /dev/ttyUSB0")
        self.SERIALPORT = '/dev/ttyUSB0'
        loop = asyncio.get_event_loop()
        """ this will only attempt tp listen to the OpenTherm Gateway """
        loop.run_until_complete(otgw_connect_and_subscribe())
        
        self.gpio_state = GPIO.LOW
        self.GPIO_PIN = 23 # hestiapi touch has heater on 23 and hot tap water on 12
        self.pid = None

        # PID feedback settings
        # Best Kp,Ki and Kd depend on the room thermodynamics
        # Note: the actual thermodynamic system is slow and overshoot must be small
        Kp = 50
        Ki = 0.15
        Kd = 0.001
        pid_sample_time = 1 # seconds; if SampleTime < time between calling, the pid will do nothing. TODO: needs better implementation
        pid_windup = 2000

        # create PID controller
        print("IOThermostat: WARNING: heatercontroller.py: using PID control, this has not been tested!")
        #self.pid = notPID(Kp, Ki, Kd)
        self.pid = PID(Kp, Ki, Kd)
        self.pid.setSampleTime(pid_sample_time)
        self.pid.setWindup(pid_windup)

        # initialise GPIO
        self.openGPIO()

        print('IOThermostat: Heater Controller active.')
        

    async def otgw_print_status(status):
        """Receive and print status."""
        print("IOThermostat: OTGW: Received status update:\n{}".format(status))
   

    async def otgw_connect_and_subscribe():
        """Connect to the OpenTherm Gateway and subscribe to status updates."""

        # Create the object
        gw = pyotgw()

        # Connect to OpenTherm Gateway on PORT
        status = await gw.connect(asyncio.get_event_loop(), PORT)
            print("IOThermostat: OTGW: Initial status after connecting:\n{}".format(status))

        # Subscribe to updates from the gateway
        if not gw.subscribe(otgw_print_status):
            print("IOThermostat: OTGW: Could not subscribe to status updates.")

        # Keep the event loop alive...
        while True:
            await asyncio.sleep(1)

        
    def update(self,temperature,targettemperature):

        self.pid.setSetPoint(targettemperature)
        self.pid.update(temperature)

        print("IOThermostat: HeaterController: PID output = {}".format(self.pid.output))

        
        print("IOThermostat: WARNING: heatercontroller.py: Modulation through OpenTherm not yet implemented! Using On/Off scheme.")
        if (self.pid.output < targettemperature) and self.isEnabled():
            self.enableHeater(False)
        elif (self.pid.output > targettemperature) and not self.isHeaterEnabled():
            self.enableHeater(True)


    def enableHeater(self,enable):
        """ GPIO.LOW is off, i.e. when power fails the heater will be off. """
        if enable and not self.isHeaterEnabled():
            # turn on
            self.gpio_state = GPIO.HIGH
        elif not enable and self.isHeaterEnabled():
            # turn off
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
