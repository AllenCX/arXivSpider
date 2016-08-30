import smtplib
from email.mime.text import MIMEText
import uuid
import socket
import re, subprocess
from threading import Timer
import sched,time
import json

# In[25]:

def send_mail(to_list, sub, content, _subtype='plain'):

    #Load the settings, see mail_settings.json
    with open("axspider/email_settings.json", 'r') as f:
        mail_settings = json.load(f)
    
    MAIL_HOST = mail_settings["MAIL_HOST"]
    MAIL_USER = mail_settings["MAIL_USER"]
    MAIL_PWD = mail_settings["MAIL_PWD"]
    MAIL_POSTFIX = mail_settings["MAIL_POSTFIX"]

    me = MAIL_USER + '@' + MAIL_POSTFIX
    msg = MIMEText(content, _subtype)
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ';'.join(to_list)
    try:
        server = smtplib.SMTP()
        server.connect(MAIL_HOST)
        server.login(MAIL_USER, MAIL_PWD)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception as e:
        print(str(e))
        return False