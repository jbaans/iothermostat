#!/usr/bin/python
#

""" notPID.py: Provides a PID class which only acts as a conditional on/ff switch 
               for the IOThermostat package """

__author__ = "Jan Bonne Aans"
__copyright__ = "Copyright 2018, Jan Bonne Aans"
__credits__ = []
__license__ = "GPLv3"
__version__ = "1"
__maintainer__ = "Jan Bonne Aans"
__email__ = "jbaans-at-gmail.com"
__status__ = "Development"

class PID:
    """ not a PID Controller
        doesn't use feedback
        for testing purposes
    """

    def __init__(self, P=0.2, I=0.0, D=0.0):
        self.output = 0.0

    def clear(self):
        pass

    def setSetPoint(self, set_point):
        self.SetPoint = set_point

    def update(self, feedback_value):
        # just return 5 above or below SetPoint with margin
        if feedback_value < self.SetPoint - 0.2:
            self.output = self.SetPoint - 5
        elif feedback_value > self.SetPoint - 0.1:
            self.output = self.SetPoint + 5

    def setKp(self, proportional_gain):
        pass

    def setKi(self, integral_gain):
        pass

    def setKd(self, derivative_gain):
        pass

    def setWindup(self, windup):
        pass

    def setSampleTime(self, sample_time):
        pass
