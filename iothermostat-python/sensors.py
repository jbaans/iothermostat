#!/usr/bin/env python
# -*- coding: UTF-8 -*-

""" sensors.py: Provides the Sensors class which handles getting data from 
                the implemented sensors for the IOThermostat package """

import smbus2
import bme280

__author__ = "Jan Bonne Aans"
__copyright__ = "Copyright 2021, Jan Bonne Aans"
__credits__ = []
__license__ = "GPLv3"
__version__ = "2"
__maintainer__ = "Jan Bonne Aans"
__email__ = "jbaans-at-gmail.com"
__status__ = "Development"

class Sensors:

    T_OFFSET = 0
    H_OFFSET = 0
    P_OFFSET = 0
    port = 1
    address = 0x76
    bus = None
    calibration_params = None

    def __init__(self,t_offset,p_offset,h_offset):
    
        print("IOThermostat: Starting Sensors module..")
        self.T_OFFSET = t_offset
        self.P_OFFSET = p_offset
        self.H_OFFSET = h_offset

        self.bus = smbus2.SMBus(self.port)
        self.calibration_params = bme280.load_calibration_params(self.bus, self.address)

        print("IOThermostat: Sensors module active.")


    def getData(self):

        # return sensor data, rounded to sensible numbers
        # Note: use str().rstrip('0').rstrip('.') to remove trailing 0 with print
        # t temperature in Celcius
        # p pressure in hPa
        # h humidity in %

        data = bme280.sample(self.bus, self.address, self.calibration_params)

        t = data.temperature
        p = data.pressure
        h = data.humidity

        t = round(t+self.T_OFFSET,1)      # deg C
        p = round(p/100+self.P_OFFSET,0)  # hPa
        h = round(h+self.H_OFFSET,0)      # %

        return (t,p,h)

    # call this function when closing
    def close(self):
        print('IOThermostat: WARNING: Stopping Sensors is not implemented.')
