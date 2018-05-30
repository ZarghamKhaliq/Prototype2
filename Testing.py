# -*- coding: utf-8 -*-
"""
Created on Wed May 30 15:41:05 2018

@author: Zeekay
"""
import imaplib
import email
import email.header
import os

def login(EMAIL_ACCOUNT,PASSWORD):
    
    

    try:
        login_msg=mail.login(EMAIL_ACCOUNT, PASSWORD)
        print(login_msg)
        return True
    except:
        print("Failed")
        return False
    


mail = imaplib.IMAP4_SSL('imap.gmail.com')
EMAIL_ACCOUNT = "l144083@lhr.nu.edu.pk"
#    EMAIL_ACCOUNT = email
PASSWORD = "1598741"

login(EMAIL_ACCOUNT,PASSWORD)    
    


os.system("pause")    