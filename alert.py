#!/usr/bin/env python
import time
import re
import datetime
import os
import math
import sqlite3
import ConfigParser
import smtplib
from email.mime.text import MIMEText

def sendmail(fromaddr, toaddr, username, password, email_body, email_subject, smtpsrv, smtpport):
	# Build the email
	msg = MIMEText(email_body)
	msg['Subject'] = email_subject
	msg['From'] = fromaddr
	msg['To'] = toaddr

	try:
		# The actual mail send
		server = smtplib.SMTP(smtpsrv, smtpport)
		server.ehlo()
		server.starttls()
		server.login(username,password)
		server.sendmail(fromaddr, toaddr, msg.as_string())  
		server.quit()
		#print "email sent: %s" % fromaddr

	except Exception as e:
		print "Something went wrong when sending the email %s" % fromaddr
		print e

def get_temperature (sensnum):
	con=sqlite3.connect('/home/pi/templog.db')
	cur = con.cursor()
	cur.execute("SELECT (MAX(timestamp)*1000) as timestamp, sensnum, temp from temps where sensnum = ?", (sensnum,))
	Timestamp, Sensor, Temperature = cur.fetchone()
	con.commit()
	con.close()
	return Temperature

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

#grab all of the alert config variables for later use
Config = ConfigParser.ConfigParser()
Config.read("/home/pi/alerts.cfg")
Email= ConfigSectionMap("Config")['email']

#read holddown tracking file
open('/home/pi/alerthold.txt', 'a').close()
with open('/home/pi/alerthold.txt') as f:
    holddown = f.readlines()
f.close()
# preinitiailize holddown list if the file was empty
if holddown == []:
	holddown = [0 for x in range(6)]

msg = ''
count = 0
#iterate through all three sensors and look for alerts
for sensor in xrange(0,3):
	SensTemp=get_temperature(sensor)
	#print "Temp is %s for sensor %s.\n" % (sensor, SensTemp)
	Sensnum = sensor + 1
	alerts = [ ('s' + str(Sensnum) + '_high_alert'), ('s' + str(Sensnum) + '_low_alert') ]
	for alert in alerts:
		#print "Checking %s - temp is %s and threshold is %s\n" % (alert,SensTemp,ConfigSectionMap("Config")[alert])
		# if user set the alert to zero, skip it
		if ConfigSectionMap("Config")[alert] == '0':
			holddown[count] = 0
			#print "Skipping %s because alert is set to 0\n" % (alert)
			count += 1
			continue
		#check high alerts
		if re.search("high", alert) and int(SensTemp) > int(ConfigSectionMap("Config")[alert]):
			print "High Threshold exceeded for %s" % alert
			if int(holddown[count]) == int(ConfigSectionMap("Config")['alerthold']):
				msg += 'Sensor ' + str(Sensnum) + ' has exceeded ' + str(ConfigSectionMap("Config")[alert]) + " degrees F\n"
				#print "Reached holddown timer for %s\n" % (alert)
				holddown[count] = 0
				count += 1
			#Increment holddown timer if we have not reached it yet
			else:
				#print "Have not reached holddown timer for %s, not firing alert\n" % (alert)
				holddown[count] = int(holddown[count]) + 1
				count += 1
		#check low alerts
		elif re.search("low", alert) and int(SensTemp) < int(ConfigSectionMap("Config")[alert]):
			#print "Low Threshold exceeded for %s\n" % alert
			if int(holddown[count]) == int(ConfigSectionMap("Config")['alerthold']):
				msg += 'Sensor ' + str(Sensnum) + ' has dropped below ' + str(ConfigSectionMap("Config")[alert]) + " degrees F\n"
				#print "Reached holddown timer for %s, firing alert\n" % (alert)
				holddown[count] = 0
				count += 1
			#Increment holddown timer if we have not reached it yet
			else:
				#print "Have not reached holddown timer for %s, not firing alert\n" % (alert)
				holddown[count] = int(holddown[count]) + 1
				count += 1
		else:
			holddown[count] = 0
			count += 1

#write holddown counts to a file
with open('/home/pi/alerthold.txt', 'w+') as f:
	for item in holddown:
		f.write("%s\n" % item)
f.close()


#send email if there is a msg to send
if msg != '':
	Config = ConfigParser.ConfigParser()
	Config.read("/home/pi/email.cfg")
	msgSubject = 'BBQ Monitor Alert'
	sendmail(ConfigSectionMap("Config")['smtpemail'], Email, ConfigSectionMap("Config")['smtpuser'], ConfigSectionMap("Config")['smtppass'], 
		msg, msgSubject,smtpsrv= ConfigSectionMap("Config")['smtpsrv'], smtpport= ConfigSectionMap("Config")['smtpport'])
