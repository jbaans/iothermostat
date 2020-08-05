#!/usr/bin/python
# -*- coding: UTF-8 -*-

""" pidtest.py: Contains code to test the PID controller functionality
                   for the IOThermostat package """
                   
""" Use this to test and tune the PID controller.

    The PID controller can be used to drive a Modulating Heater,
    which is more efficient than an On/Off Heater.
    
    Run this code in your favourite python interpreter.
    
    Follow these steps:
    1. Setup your heat environment by filling out the external_area and
      volume dimensions of your room and your heater, approximately.
      Set sensible heat transport coefficients for your heater and room.
      Test your heat environment by letting it cool down, with the PID
      set point set to zero. The temperature dynamics should match your
      actual home situation.
      
    2. Setup the PID controller by adjusting P. For this set I to zero
      and set PID set point to the desired room temperature.
      Observe the temperature dynamics in the console output.
      Increase P until the heater temperature starts oscillating, then
      adjust it down until the oscillation is gone.
      Slightly increase I to improve the PID response.
      
    3. To be determined. In future, the PID controller output should be 
      used to set your modulating heater temperature.
"""

import math
from pid import PID
from heatobject import HeatObject

__author__ = "Jan Bonne Aans"
__copyright__ = "Copyright 2020, Jan Bonne Aans"
__credits__ = []
__license__ = "GPLv3"
__version__ = "1"
__maintainer__ = "Jan Bonne Aans"
__email__ = "jbaans-at-gmail.com"
__status__ = "Development"

""" Setup the heat environment.
    Using realistic specific heat values (here in J.m^-3.K^-1), 
    air has 1000 J.m^-3.K, water has 4200000 J.m^-3.K^-1
"""
MyEnvironment = HeatObject(temperature=15+272,
                        name="Environment",
                        specific_heat=1000,         # air
                        external_area=math.inf,
                        volume=math.inf,
                        ht_coefficient=0)
                        
MyRoom = HeatObject(temperature=16+272, 
                        name="MyRoom",
                        specific_heat=25000,        # mixed
                        external_area=4 * 5 * 3,
                        volume=5 * 5 * 3,
                        ht_coefficient=0.2)

MyRoomHeater = HeatObject(temperature=MyRoom.temperature, 
                        name="MyRoomHeater",
                        specific_heat=4200000,      # water
                        external_area=2 * 4 * 0.5,
                        volume=0.010,
                        ht_coefficient=15) 
                        
MyEnvironment.addChild(MyRoom)
MyRoom.addChild(MyRoomHeater)


""" Setup the PID controller, using our own locak time system
"""
currenttime = 0                 # seconds
timestep = 600                  # seconds
heaterhc = MyRoomHeater.heat_capacity   # the defined heat capacity of the heater
maxheatertemperature = 60+272   # K
P = 50                          # P = 50, I = 0.15, D = 0.001 work for my 
I = 0.15                        # example room. P and I may need tuning.
D = 0.001
pid = PID(P, I, D,current_time=currenttime)
pid.SetPoint=20+272             # desired room temperature [K]
pid.setSampleTime(timestep/2)   # if SampleTime < timestep the pid will do nothing
pid.setWindup(2000)             # prevents big steps in output due to I term


""" Start running the time of the setup system
"""
print("Time(s)\t\tT Environment\tT Room\tT Heater (C)")
for i in range(240):
    currenttime = i*timestep
    print( "{:.0f}\t\t{:.1f}\t\t{:.1f}\t{:.1f}".format(currenttime, 
                                                    MyEnvironment.temperature-272,
                                                    MyRoom.temperature-272,
                                                    MyRoomHeater.temperature-272) )

    """ get the heater temperature value the PID controller think is optimal
        Heater On is simulated by setting the optimal temperature and setting
        the heat capacity to infinite.
        Switching the heater off can be simulated by changing the heat capacity 
        back to its original value. The temperature will then start dropping
        by means of the model, since it's simply loosing heat until it's at
        room temperature.
    """
    pid_feedback = MyRoom.temperature
    pid.update(pid_feedback,currenttime)
    pid_output = pid.output                     # this is the optimal temperature for
                                                # the modulated heater
    
    if pid_output < MyRoom.temperature:
        MyRoomHeater.heat_capacity = heaterhc   # heater is off
    elif pid_output > maxheatertemperature:
        MyRoomHeater.temperature = maxheatertemperature
        MyRoomHeater.heat_capacity = math.inf   # heater is maximally on        
    else:
        MyRoomHeater.temperature = pid_output
        MyRoomHeater.heat_capacity = math.inf   # heater is on, modulated
    
    # do a time step for the heat system
    MyEnvironment.lapse(timestep)
