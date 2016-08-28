import smtplib
from email.mime.text import MIMEText
import uuid
import socket
import re, subprocess
from threading import Timer
import sched,time

MAIL_HOST = "smtp.163.com"
MAIL_USER = 'gdga51'
MAIL_PWD = '135asdfghjkl'
MAIL_POSTFIX = "163.com"

# In[25]:

def send_mail(to_list, sub, content):
    me = MAIL_USER + '@' + MAIL_POSTFIX
    msg = MIMEText(content, _subtype='plain')
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