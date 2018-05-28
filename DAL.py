# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 16:29:53 2018

@author: Zeekay
"""

import datetime as dt
import calendar
import MySQLdb
import datefinder
#from final import final

class DAL():
    
    
    def __init__(self):
         try:
             self.db = MySQLdb.connect("localhost","root","1122","whizaide" )
         except:
            print ("Error: unable to connect")
            
    def insert_meeting(self,meeting):
        result=False
        cursor = self.db.cursor()
        sql = sql = "INSERT INTO meetings(name,date,participant,slot) \
                        VALUES ('%s',' %s',' %s','%d')" % \
       (meeting.name,meeting.date,meeting.participant,meeting.slot)
   
        try:
            # Execute the SQL command
            cursor.execute(sql)
            # Commit your changes in the database
            self.db.commit()
            result=True
        except:
            # Rollback in case there is any error
            self.db.rollback()
            print ("Error: unable to insert")
       
        return result

    def getFreeSlots(self,d):
        date=str(d)
        day=calendar.day_name[d.weekday()]
        slots=[]
        cursor = self.db.cursor()
        sql="SELECT * FROM time_table left outer join (select * from meetings where meetings.date ='"+date+"') AS A on A.slot=time_table.id where A.date is null and time_table.day='"+day+"' "    
        try:
            cursor.execute(sql)
        except:
            print("Error: Excuting sql")

        results = cursor.fetchall()
        for row in results:
            slots.append(row[0])
            print ("id=%d" % row[0])
            
        return slots
    
    def cancelMeeting(self,meeting):
        result=False
        date=str(meeting.date)
   
        cursor = self.db.cursor()
        #sql="Delete from meetings where meetings.date ='"+date+"' and meetings.slot= '"+str(meeting.slot)+"'";    
        sql="Delete from meetings where meetings.date =%s and meetings.slot= %s";    
        
        try:
            cursor.execute(sql,(date,meeting.slot))
            self.db.commit()
            result=True
        except:
            print("Error: Excuting sql cancel")

        return result
    
    def updateMeeting(self,old,new):
        result=False
        olddate=str(old.date)
   
        cursor = self.db.cursor()
        sql="Update meetings  SET meetings.date='"+str(new.date)+"',meetings.slot='"+str(new.slot)+"'  where meetings.date ='"+olddate+"' and meetings.slot= '"+str(old.slot)+"'";    
        try:
            cursor.execute(sql)
            self.db.commit()
            result=True
        except:
            print("Error: Excuting sql cancel")

        return result
            