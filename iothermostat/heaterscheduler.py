#!/usr/bin/env python
# -*- coding: UTF-8 -*-

""" heaterscheduler.py: Contains the HeaterScheduler class that provides scheduling
    with the APScheduler package for the IOThermostat package """

import time
import os
from datetime import datetime,timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

__author__ = "Jan Bonne Aans"
__copyright__ = "Copyright 2018, Jan Bonne Aans"
__credits__ = []
__license__ = "GPLv3"
__version__ = "1"
__maintainer__ = "Jan Bonne Aans"
__email__ = "jbaans-at-gmail.com"
__status__ = "Development"

# wrapper for APScheduler job
class Job:

    day = None
    hour = None
    minute = None
    func = None
    args = None

    def __init__(self, day=0, hour=0, minute=0, func=None, args=None):

        self.func = func
        self.day = day
        self.hour = hour
        self.minute = minute
        self.args = args

    
    def __iter__(self):

        # usage: jobdict = dict(myjob)
        yield 'day', self.day
        yield 'hour', self.hour
        yield 'minute', self.minute
        yield 'func', self.func
        yield 'args', self.args


    def triggerIn(self, days=0, hours=0, minutes=0):

        # schedule to run in specified minutes, hours and days from now
        runtime = datetime.now() + timedelta(days=days, hours=hours, minutes=minutes)
        self.day = runtime.weekday()
        self.hour = runtime.hour
        self.minute = runtime.minute


    def getTimeString(self):

        return '{},{},{}'.format( self.day, self.hour, self.minute)


class Schedule(list):

    # extends list, Schedule is a list of Job objects
    def __init__(self, joblist=None):
        if joblist is not None:
            super().__init__(joblist)
        else:
            super().__init__([])


    def sort(self):
        self = sorted(self, key=lambda job: (job.day, job.hour, job.minute ))


    def getPreviousJob(self):

        now = datetime.now()
        today = now.weekday()
        hour = now.hour
        minute = now.minute

        self.sort()
        
        # find job right before now, if any
        previousjob = None
        for job in self:
            if ((job.day > today) or 
                (job.day == today and job.hour > hour) or
                (job.day == today and job.hour == hour and job.minute > minute)):
                # if this job is after now, stop searching
                break
            else:
                # if job is now or before now, continue searching
                previousjob = job
        
        # return last job before now or None
        return previousjob


class HeaterScheduler:

    job_defaults = None
    scheduler = None
    
    def __init__(self):
        '''
        Important

        If you schedule jobs in a persistent job store during your application's
        initialization, you MUST define an explicit ID for the job and use 
        replace_existing=True or you will get a new copy of the job every time your 
        application restarts!
        '''

        print('IOThermostat: Starting Heater scheduler..')

        self.jobstores = {
            'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
        }

        self.job_defaults = {
            'coalesce': True,
            'max_instances': 1,
            'misfire_grace_time': 15*60
        }

        self.scheduler = BackgroundScheduler(job_defaults=self.job_defaults)        
        self.scheduler.start(paused=True)

        print('IOThermostat: Heater scheduler active.')


    def start(self):
        self.scheduler.start()
        
        
    def resume(self):
        self.scheduler.resume()
        
        
    def pause(self):
        self.scheduler.pause()
        
        
    def shutdown(self):
        if self.scheduler.running:
            self.scheduler.shutdown(wait=False)


    def __chunks__(self, l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]


    def setSchedule(self, schedule):

        # accepts list of jobdicts

        #print('Pausing and clearing schedule...')
        self.scheduler.pause()
        self.scheduler.remove_all_jobs()     # requires the started scheduler


        if schedule is None:
            pass
        else:
            for i,job in enumerate(schedule):

                self.scheduler.add_job(job.func,
                                       args=job.args,
                                       replace_existing=True,
                                       id='{}'.format(i),
                                       trigger='cron',
                                       day_of_week=job.day,
                                       hour=job.hour,
                                       minute=job.minute)

            # get previous job
            job = schedule.getPreviousJob()
            if not job is None:
                # run job function
                job.func(job.args[0])

        self.scheduler.resume()
        #print('Started scheduler.')
        print('IOThermostat: Added jobs of new schedule.')


    def stringToSchedule(self, schedulestring, callbackfunc, offtemperature):
        # create schedule from string
        schedule = Schedule()
        
        rowlength = 6
        # convert string to lists of strings each with 6 items
        # each list contains the a row of items from the scheduler UI
        # in the format:
        # day,hour_start,minute_start,hour_end,minute_end,temperature
        rows = []
        if schedulestring is not None:
            # note split will return [''] for an empty string (>0 elements)
            rows = self.__chunks__( schedulestring.split(","), rowlength)

        for row in rows:
            onjob = Job(day=int(row[0]),
                             hour=int(row[1]),
                             minute=int(row[2]),
                             func=callbackfunc,
                             args=[float(row[5])] )

            offjob = Job(day=int(row[0]),
                              hour=int(row[3]),
                              minute=int(row[4]),
                              func=callbackfunc,
                              args=[offtemperature])
           
            schedule.append(onjob)
            schedule.append(offjob)
            
        return schedule


    def close(self):
        # for compatibility
        self.shutdown()
        print('IOThermostat: Stopped scheduler.')
