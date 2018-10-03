#!/usr/bin/env python
# -*- coding: UTF-8 -*-

""" modemanager.py: Contains the ModeManager class which provides states (Modes) 
    in the IOThermostat package """

from heaterscheduler import Job, Schedule

__author__ = "Jan Bonne Aans"
__copyright__ = "Copyright 2018, Jan Bonne Aans"
__credits__ = []
__license__ = "GPLv3"
__version__ = "1"
__maintainer__ = "Jan Bonne Aans"
__email__ = "jbaans-at-gmail.com"
__status__ = "Development"

class ModeManager:

    class Mode:

        endtime = None
        triggerin = None
        name = None
        targettemperature = None
        schedule = None

        def __init__(self,name):
            self.name = name
        
        def __eq__(self, other):
            if other:
                return self.name == other.name
            else:
                return False
        

    # ModeManager variables:
    currentmode = None
    previousmode = None
    scheduler = None
    callbackfunc = None

    # modes:
    MODELIST = None
    AUTO = None
    OFF = None
    ON = None
    SLEEP = None
    BOOST = None

    def __init__(self,scheduler=None, callbackfunc=None):

        print('IOThermostat: Starting Mode Manager..')

        if not scheduler:
            raise RuntimeError('Scheduler required!')
        self.scheduler = scheduler

        if not callbackfunc:
            raise RuntimeError('callbackfunc required!')
        self.callbackfunc = callbackfunc

        
        # modes:
        self.AUTO = self.Mode('Auto')
        self.OFF = self.Mode('Off')
        self.ON = self.Mode('On')
        self.SLEEP = self.Mode('Sleep')
        self.BOOST = self.Mode('Boost')

        self.MODELIST = [self.AUTO,self.OFF,self.ON,self.SLEEP,self.BOOST]

        self.OFF.targettemperature = 15.0 # Celcius
        self.ON.targettemperature = 21.0 # Celcius
        self.AUTO.targettemperature = self.OFF.targettemperature

        self.SLEEP.targettemperature = self.OFF.targettemperature
        self.SLEEP.triggerin = {'days':1,'hours':0,'minutes':0}

        self.BOOST.targettemperature = self.ON.targettemperature + 1
        self.BOOST.triggerin = {'days':0,'hours':1,'minutes':0}

        print('IOThermostat: Mode Manager Started.')


    # required for HeaterScheduler callback
    def setPreviousMode(self):
        
        self.setMode( self.previousmode )
        self.callbackfunc()        

    def stringToMode(self,name):

        for mode in self.MODELIST:
            if mode.name == name:
                return mode
        raise ValueError('Mode name not recognised: {}'.format(name))


    def setMode(self, mode, force=False):
        
        # sanity checks
        if not mode in self.MODELIST:
            raise ValueError('Bad mode: {}'.format(mode))

        if mode == self.currentmode and not force:
            # nothing changed, return nothing
            return self.currentmode
        
        if mode == self.SLEEP or mode == self.BOOST:
            # do scheduling for SLEEP and BOOST modes
   
            job = Job(func=self.setPreviousMode)
            job.triggerIn(  days=mode.triggerin['days'],  
                            hours=mode.triggerin['hours'], 
                            minutes=mode.triggerin['minutes'])

            mode.endtime = job.getTimeString()
            mode.schedule = Schedule(joblist=[job])

        #previousmode is never SLEEP or BOOST
        if self.currentmode in [self.SLEEP, self.BOOST]:
            self.previousmode = self.AUTO
        else:
            self.previousmode = self.currentmode
        self.currentmode = mode
        print('IOThermostat: ModeManager: Current mode = {}'.format(self.currentmode.name))

        # set current mode schedule
        self.scheduler.setSchedule(self.currentmode.schedule)
