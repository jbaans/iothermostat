#!/usr/bin/env python
# -*- coding: UTF-8 -*-

""" iothermostat.py: Contains and runs main class of Independent Open-source Thermostat """

from time import sleep
from datetime import datetime,timedelta
import topics
from sensors import Sensors
from datalogger import DataLogger
from mqttclient import MqttClient
from heatercontroller import HeaterController
from heaterscheduler import HeaterScheduler
from modemanager import ModeManager

__author__ = "Jan Bonne Aans"
__copyright__ = "Copyright 2018, Jan Bonne Aans"
__credits__ = []
__license__ = "GPLv3"
__version__ = "1"
__maintainer__ = "Jan Bonne Aans"
__email__ = "jbaans-at-gmail.com"
__status__ = "Development"

class IOThermostat:

    # constants
    UPTIMEFILE = '/proc/uptime'
    STARTTIME = datetime.now()
    REFRESH_SECONDS = 3
    T_OFFSET = -0.5
    H_OFFSET = 0
    P_OFFSET = 0
    SUBSCRIBELIST = [topics.MODE, topics.TARGETTEMPERATURE, topics.SCHEDULE, topics.OTHERTEMPERATURE]
    USE_OTHERTEMPERATURE = False
    DATALOGFILE = '/home/iothermostat/iothermostat.csv'
    DATALOGMAXFILESIZE = 2*1000*1000 # 2MB in Bytes
    # topics to log, options are:
    # topics.TEMPERATURE,topics.PRESSURE,topics.HUMIDITY,topics.D_TEMPERATURE,topics.D_PRESSURE,topics.D_HUMIDITY,
    # topics.HEATERON,topics.IOTHERMUPTIME,topics.SYSTEMUPTIME
    DATALOGKEYS = [topics.TEMPERATURE,topics.PRESSURE,topics.HUMIDITY,topics.HEATERON]

    # default variable values
    previousmessages = None
    
    # objects
    scheduler = None
    mqttclient = None
    heatercontroller = None
    modemanager = None


    def schedulercallbackfunc(self, arg):
        # used for scheduler set temperature callback. 
        # arg is not an array, unlike the array that was given to apscheduler.add_job

        self.setTargetTemperature(arg)


    def modemanagercallbackfunc(self):
        # used for modemanager previous mode callback

        self.mqttclient.publish( {topics.MODE:self.modemanager.currentmode.name} )


    def setTargetTemperature(self,temperature,publish=True):

        self.modemanager.currentmode.targettemperature = temperature
        if publish:
            self.mqttclient.publish({topics.TARGETTEMPERATURE:temperature})
        

    def publishModeEndTime(self, endtime):
    
        if endtime:
            self.mqttclient.publish({topics.MODEENDTIME:endtime})


    def getSelfUptime(self):

        uptime = datetime.now() - self.STARTTIME
        uptime_string = str(uptime.days)
        return uptime_string


    def getSystemUptime(self):

        uptime_seconds = -1
        with open(self.UPTIMEFILE, 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
        uptime_string = str(timedelta(seconds = uptime_seconds).days)

        return uptime_string


    def processMessages(self, messages):
    
        # process new targettemperature
        if topics.TARGETTEMPERATURE in messages:
            self.modemanager.currentmode.targettemperature = float( messages[topics.TARGETTEMPERATURE] )
       
        # process new schedule
        if topics.SCHEDULE in messages:
            schedule = self.scheduler.stringToSchedule( messages[topics.SCHEDULE],
                                                        self.schedulercallbackfunc,
                                                        self.modemanager.OFF.targettemperature )
            self.modemanager.AUTO.schedule = schedule
            # reload schedule if mode is auto
            if self.modemanager.currentmode == self.modemanager.AUTO:
                self.scheduler.setSchedule(schedule)

        # process new mode
        if topics.MODE in messages:
            mode = self.modemanager.stringToMode( messages[topics.MODE] )
            self.modemanager.setMode( mode )
            self.mqttclient.publish({topics.TARGETTEMPERATURE:self.modemanager.currentmode.targettemperature})
            self.publishModeEndTime(mode.endtime)


    def prepareMessages(self, t, p, h, d_t, d_p, d_h):
    
        messages = {}
               
        # collect sensor states for publishing
        messages[topics.TEMPERATURE] = t
        messages[topics.PRESSURE] = int(p)
        messages[topics.HUMIDITY] = int(h)
        messages[topics.D_TEMPERATURE] = d_t
        messages[topics.D_PRESSURE] = d_p
        messages[topics.D_HUMIDITY] = d_h
        messages[topics.HEATERON] = self.heatercontroller.isHeaterEnabled()
        messages[topics.IOTHERMUPTIME] = self.getSelfUptime()
        messages[topics.SYSTEMUPTIME] = self.getSystemUptime()
        
        # only keep new data
        if self.previousmessages:
            newmessages = {}
            for topic,value in messages.items():
                if not topic in self.previousmessages or not value == self.previousmessages[topic]:
                    newmessages[topic] = value
                    self.previousmessages[topic] = value

            messages = newmessages
        else:
            self.previousmessages = messages.copy()

        return messages


    def run(self):

        sensors = None
        datalogger = None

        try:

            # initialise objects
            sensors = Sensors(self.T_OFFSET,self.P_OFFSET,self.H_OFFSET)
            datalogger = DataLogger(self.DATALOGFILE, self.DATALOGKEYS, self.DATALOGMAXFILESIZE)
            self.scheduler = HeaterScheduler()
            self.modemanager = ModeManager( scheduler=self.scheduler,
                                            callbackfunc=self.modemanagercallbackfunc)
            self.mqttclient = MqttClient(subscribelist=self.SUBSCRIBELIST)
            self.heatercontroller = HeaterController()
            
            # initialise state
            self.modemanager.setMode(self.modemanager.AUTO)

            # initial data
            t_avg,p_avg,h_avg = sensors.getData()

            # present ourselves
            self.mqttclient.publish({topics.IOTHERMSTATUS:'Active'})
            self.mqttclient.publish({topics.IOTHERMVERSION:__version__ +' '+ __status__})
            self.mqttclient.publish({topics.MODE:self.modemanager.currentmode.name})
            self.mqttclient.publish({topics.TARGETTEMPERATURE:self.modemanager.currentmode.targettemperature})

            while True:
               t,p,h = sensors.getData()
               messages = self.mqttclient.getData()
               
               # use temperature value from mqtt
               if self.USE_OTHERTEMPERATURE and topics.OTHERTEMPERATURE in messages:
                   t = float( messages[topics.OTHERTEMPERATURE] )
            
               # calculate averages
               t_avg = (t_avg + t)/2       
               p_avg = (p_avg + p)/2       
               h_avg = (h_avg + h)/2

               # calculate derivatives
               d_t = (t - t_avg)/self.REFRESH_SECONDS
               d_p = (p - p_avg)/self.REFRESH_SECONDS
               d_h = (h - h_avg)/self.REFRESH_SECONDS

               # process data from subscribed topics
               self.processMessages( messages )
           
               # prepare for publishing
               messages = self.prepareMessages(t, p, h, d_t, d_p, d_h)
               datalogger.log(messages)
               self.mqttclient.publish(messages)

               # update the heatercontroller with the current and target temperatures
               #print('targettemperature = {}'.format(self.modemanager.currentmode.targettemperature))
               self.heatercontroller.update(t,self.modemanager.currentmode.targettemperature)

               sleep(self.REFRESH_SECONDS)

        finally:
            print('IOThermostat: Stopping IOThermostat..')
            if datalogger:
                datalogger.close()
                
            if sensors:
                sensors.close()
                
            if self.scheduler:
                self.scheduler.close()
                
            if self.heatercontroller:
                self.heatercontroller.close()
                
            if self.mqttclient:
                self.mqttclient.close()
        

if __name__ == "__main__":
    iothermostat = IOThermostat()
    iothermostat.run()
    print('IOThermostat: Stopped IOThermostat.')
