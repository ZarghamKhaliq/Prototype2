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
        
class slot():
    
    def __init__(self,id,start,end):
        self.id=id
        self.start=start
        self.end=end
        
    
       
        