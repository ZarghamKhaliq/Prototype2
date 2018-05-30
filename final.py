# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 16:41:31 2018

@author: Zeekay
"""
import os

from DAL import DAL
from meeting import meeting,slot
import datetime as dt

def next_weekday(weekday):
    currentDate=dt.datetime.now()
    year=currentDate.year
    month=currentDate.month
    day=currentDate.day
    d = dt.date(year, month, day)
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: 
        days_ahead += 7
    return d + dt.timedelta(days_ahead)

dal=DAL()
"""
s=slot("Wednesday","2:00 am","3:00 am")
if(dal.addSlots(s)):
    print("added")
else:
    print("Failed")
"""        
    
if(dal.getMeetings()):
    print("Found meeting")
else:
    print("Failed meeting")
        

"""
slot=1
name="Machine Learning Things"
date=next_weekday(1)
part="Ali"

slots=dal.getFreeSlots(date)

print(len(slots))
if(len(slots)!=0):
    print("inserting")
    m=meeting(name,part,date,slots[0])
    dal.insert_meeting(m)
    
m=meeting(name,part,date,3)
#dal.cancelMeeting(m)
"""

os.system('pause')
