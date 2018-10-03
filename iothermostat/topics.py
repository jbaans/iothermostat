#!/usr/bin/env python
# -*- coding: UTF-8 -*-

""" topics.py: Contains the topic configuration for the MQTT messaging
               for the IOThermostat package """

# system name
SYSTEMNAME =        'iothermostat0'

# topic definition
# sensors (python user only writes)
TEMPERATURE =       SYSTEMNAME+'/sensor/temperature'
HUMIDITY =          SYSTEMNAME+'/sensor/humidity'
PRESSURE =          SYSTEMNAME+'/sensor/pressure'
D_TEMPERATURE =     SYSTEMNAME+'/sensor/d_temperature'
D_HUMIDITY =        SYSTEMNAME+'/sensor/d_humidity'
D_PRESSURE =        SYSTEMNAME+'/sensor/d_pressure'

# states (python user only writes)
HEATERON =          SYSTEMNAME+'/state/heateron'
MODEENDTIME =       SYSTEMNAME+'/state/modeendtime'
IOTHERMUPTIME =     SYSTEMNAME+'/state/iothermuptime'
SYSTEMUPTIME =      SYSTEMNAME+'/state/systemuptime'
IOTHERMSTATUS =     SYSTEMNAME+'/state/iothermstatus'
IOTHERMVERSION =    SYSTEMNAME+'/state/iothermversion'

# settings
MODE =              SYSTEMNAME+'/settings/mode'
TARGETTEMPERATURE = SYSTEMNAME+'/settings/targettemperature'
SCHEDULE =          SYSTEMNAME+'/settings/schedule'
