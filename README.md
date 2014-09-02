PIBBQMonitor
============

Raspberry PI with 3 BBQ meat thermometers<br>
Thanks to Tomas Holderness and adafruit for the code I started with for this project<br>
https://learn.adafruit.com/reading-a-analog-in-and-controlling-audio-volume-with-the-raspberry-pi/script<br>
https://github.com/talltom/PiThermServer<br>


Description
============
Raspberry PI project leveraging the MCP3008 ADC and Thermoworks TX-1001X-OP thermistor temprature probes to create a 3 sensor wireless BBQ Temperature monitor.

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
1.  Install node and its deendencies: node-sqlite3, node-static
2.  Install python and other packages: 
    sudo apt-get install python-dev<br>
    sudo apt-get install python-setuptools<br>
    sudo easy_install rpi.gpio<br>
    sudo apt-get install alsa-utils<br>
    sudo apt-get install mpg321<br>
3.  Clone git repository to /home/pi
4.  Execute build_db.sh to create SQLite DB
5.  Execute "sudo node thermserv" to start the node app.  You can enable this as a server to automatically start if you would like
6.  Execute "sudo crontab -e" and paste the following lines into your crontab.  Logger will log the temp to the DB every minute. The dbcleanup.sh will limit the DB to 24 hours worth of data:<br>
      */1 * * * * /home/pi/logger.py<br>
      0 * * * * /home/pi/dbcleanup.sh<br>

