# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 16:38:30 2018

@author: Zeekay
"""

class meeting():
    
    def __init__(self,name,participant,date,slot):
        self.name=name
        self.date=date
        self.participant=participant
        self.slot=slot
    
    def printDetails(self):
        print(self.name," : ",self.date," : ",self.participant)
        
class slot():
    
    def __init__(self,day,start,end):
        
        self.day=day
        self.start=start
        self.end=end
        
    def printDetails(self):
        print(self.day," : ",self.start," : ",self.end)
        
    
       
        