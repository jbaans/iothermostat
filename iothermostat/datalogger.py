#!/usr/bin/env python
# -*- coding: UTF-8 -*-

""" datalogger.py: Contains DataLogger class which logs IOThermostat data to file
                   for the IOThermostat package """

import csv
import gzip
import shutil
import os.path
from datetime import datetime

__author__ = "Jan Bonne Aans"
__copyright__ = "Copyright 2018, Jan Bonne Aans"
__credits__ = []
__license__ = "GPLv3"
__version__ = "1"
__maintainer__ = "Jan Bonne Aans"
__email__ = "jbaans-at-gmail.com"
__status__ = "Development"

class DataLogger:

    KEYS = []
    FILE = None
    MAXFILESIZE = None
    datalog = []
    

    def __init__(self,file,keys,maxfilesize):
    
        print("IOThermostat: Starting DataLogger module..")

        self.KEYS = keys
        self.FILE = file
        self.MAXFILESIZE = maxfilesize
        
        print('IOThermostat: Logging data to {}'.format(file))

        print('IOThermostat: DataLogger active.')
    
    
    def write(self, datalog):
    
        file_exists = os.path.isfile(self.FILE)
        file_size = os.path.getsize(self.FILE)

        # limit file size. compress and restart
        if file_exists and file_size > self.MAXFILESIZE:
            with open(self.FILE, 'rb') as f_in:
                with gzip.open(self.FILE + '.gz', 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            os.remove(self.FILE)
            print('IOThermostat: datalog file {} exceeded limit of {}B. Compressed to {}'.format(self.FILE,self.MAXFILESIZE,self.FILE+'.gz'))

        try:
            with open(self.FILE, 'a', newline='') as f:
            
                headers = ['datetime']+self.KEYS
                writer = csv.DictWriter(f, delimiter=',', fieldnames=headers, restval=' ')
                
                # at this point file existed already or is created and size is 0
                if not file_exists:
                    writer.writeheader()
                    
                for dict in datalog:
                    writer.writerow(dict)
        except Exception as e:
            print('IOThermostat: {}'.format(e))
            return False
        
        return True
                
    
    def log(self, messages):
    
        if not messages:
            return

        data = {}

        # filter out the specified keys
        for topic,value in messages.items():
            if topic in self.KEYS:
                data[topic] = value
                
        if not data:
            # there's no new data
            return
        
        data['datetime'] = datetime.now()

        self.datalog.append(data)
        
        if len(self.datalog) > 99:
            # write to file when collected enough
            if self.write(self.datalog):
                self.datalog = []

    # call this function when closing
    def close(self):
    
        # write unsaved data to file
        self.write(self.datalog)
        self.datalog = []
        print('IOThermostat: Stopped DataLogger.')
