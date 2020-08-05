#!/usr/bin/python
# -*- coding: UTF-8 -*-

""" heatobject.py: Contains HeatObject class which simulates the heat flux in an object
                   for the IOThermostat package """

__author__ = "Jan Bonne Aans"
__copyright__ = "Copyright 2020, Jan Bonne Aans"
__credits__ = []
__license__ = "GPLv3"
__version__ = "1"
__maintainer__ = "Jan Bonne Aans"
__email__ = "jbaans-at-gmail.com"
__status__ = "Development"

class HeatObject:
    """ Models the heat flux of an object
        The HeatObject can have heat flux to its outside
        The HeatObject can have a HeatObject inside
    """    
    
    def __init__(self,
                temperature=0, 
                specific_heat=0,
                external_area=0,
                volume=0,
                ht_coefficient=0):
                    
        self.temperature = temperature              # K
        # Note: Should change this to standard specific heat units of J.kg^-1.K^-1
        self.heat_capacity = specific_heat*volume   # J.m^-3.K^-1
        self.external_area = external_area          # m^2
        self.volume = volume                        # m^3
        self.ht_coefficient = ht_coefficient        # heat transfer coefficient W.m^-2.K^-1
        self.parent = None                          # HeatObjects this one is inside of
        self.childs = []                            # HeatObjects inside this one
        self.time = 0                               # seconds
        
    def addChild(self, child):
        self.childs.append(child)
        child.parent=self

    def getHeatFluxOut(self):
        """ returns heat flux to outside
        """
        """ Heat Flux is defined by

            Q = A . U . (T2 - T1)
            Where
            Q is heat flux [W]
            A is area [m^-2]
            U is heat transfer coefficient [W.m^-2.K^-1]
            T1 is internal temperatures [K]
            T2 is external temperatures [K]
        """
        A = self.external_area
        U = self.ht_coefficient
        T1 = self.temperature
        if self.parent is not None:
            T2 = self.parent.temperature
        else:
            T2 = T1
            
        Q = A * U * (T2 - T1)
        
        return Q
        
    def getHeatFluxIn(self):
        
        """ there is heat flux from the childs inside this object
        """
        Q = 0
        for child in self.childs:
            Q -= child.getHeatFluxOut()
            
        return Q
        
            
    def lapse(self, seconds):
        """ calculate temperature of this object and all its childs
            after given amount of seconds
        """
        """ Air specific heat is approx 1000 J/m^-3/K^-1
            Water specific heat is approx 4200000 J/m^-3/K^-1

            T = T + Q . s / c
            Where
            T is current temperature [C]
            Q is total heat flux [W]
            s is time [seconds]
            c is heat capacity of the object [J/K]
        """

        for child in self.childs:
            child.lapse(seconds)
            
        Q = self.getHeatFluxIn() + self.getHeatFluxOut()
        s = seconds
        c = self.heat_capacity
        
        self.temperature += (Q * s / c )
        
        self.time += seconds




