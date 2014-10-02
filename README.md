PIBBQMonitor
============

Raspberry PI with 3 meat thermometers<br>
Thanks to Tomas Holderness and adafruit for the code I started with for this project<br>
https://learn.adafruit.com/reading-a-analog-in-and-controlling-audio-volume-with-the-raspberry-pi/script<br>
https://github.com/talltom/PiThermServer<br>


Description
============
Raspberry PI project leveraging the MCP3008 ADC and Thermoworks TX-1001X-OP thermistor temperature probes to create a 3 sensor wireless BBQ Temperature monitor.

logger.py - python script that reads ADC, calculates temp and logs to SQLite database<br>
alert.py - python script that monitors temperature against user defines thresholds and sends email alerts<br>
dbcleanup.sh - shell script to clear entries older than 24 hours<br>
build_db.sh - script to build sqlite databse<br>
/web/thermserv - node web server<br>
/web/index.html - web interface<br>

Dependencies
============
NodeJS<br>
SQLite3<br>
node-sqlite3<br>
node-static<br>
Twitter Bootstrap 3.2.0 (included in repository)<br>
Highcharts (included in repository)<br>
JQuery (included in repository)<br>
python-dev<br>
python-setuptools<br>
alsa-utils<br>
mpg321<br>

Setup
============
1.  Install node and its dependencies: node-sqlite3, node-static
2.  Install python and other packages: <br>
    sudo apt-get install python-dev<br>
    sudo apt-get install python-setuptools<br>
    sudo easy_install rpi.gpio<br>
    sudo apt-get install alsa-utils<br>
    sudo apt-get install mpg321<br>
3.  Clone git repository to /home/pi.  i.e. logger.py should be in /home/pi directory
4.  Execute build_db.sh to create SQLite DB
5.  Disable any webserver that may already be running on port 80.
6.  Execute "sudo node thermserv" to start the node app.  You can enable this as a server to automatically start if you would like
7.  Execute "sudo crontab -e" and paste the following lines into your crontab.  Logger will log the temp to the DB every minute. The dbcleanup.sh will limit the DB to 24 hours worth of data:<br>
      */1 * * * * /home/pi/logger.py<br>
      0 * * * * /home/pi/dbcleanup.sh<br>
      */1 * * * * /home/pi/alert.py<br>

