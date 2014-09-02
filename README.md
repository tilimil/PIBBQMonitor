PIBBQMonitor
============

Raspberry PI with 3 BBQ meat thermometers
Thanks to Tomas Holderness and ADA fruit for the code I started with for this project
https://learn.adafruit.com/reading-a-analog-in-and-controlling-audio-volume-with-the-raspberry-pi/script
https://github.com/talltom/PiThermServer


Description
============


Dependencies
============
NodeJS
SQLite3
node-sqlite3
node-static
Twitter Bootstrap 3.2.0 (included in repository)
Highcharts (included in repository)
JQuery (included in repository)
python-dev
python-setuptools
alsa-utils
mpg321

Setup
============
1.  Install node and its deendencies: node-sqlite3, node-static
2.  Install python and other packages: 
    sudo apt-get install python-dev
    sudo apt-get install python-setuptools
    sudo easy_install rpi.gpio
    sudo apt-get install alsa-utils
    sudo apt-get install mpg321
3.  Clone git repository to /home/pi
4.  Execute build_db.sh to create SQLite DB
5.  Execute "sudo node thermserv" to start the node app.  You can enable this as a server to automatically start if you would like
6.  Execute "sudo crontab -e" and paste the following lines into your crontab.  Logger will log the temp to the DB every minute. The dbcleanup.sh will limit the DB to 24 hours worth of data:
      */1 * * * * /home/pi/logger.py
      0 * * * * /home/pi/dbcleanup.sh

