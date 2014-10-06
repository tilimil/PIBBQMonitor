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
1.  Install node
    sudo wget http://node-arm.herokuapp.com/node_latest_armhf.deb
    sudo dpkg -i node_latest_armhf.deb
    Make sure node install was good by checking "sudo node-v".  Should return node version.
2.  Install python and other packages: <br>
    sudo apt-get upgrade
    sudo apt-get update
    sudo apt-get install python-dev<br>
    sudo apt-get install python-setuptools<br>
    sudo easy_install rpi.gpio<br>
    sudo apt-get install alsa-utils<br>
    sudo apt-get install mpg321<br>
    sudo apt-get install sqlite3<br>
    sudo apt-get install libsqlite3-dev<br>
    sudo apt-get install npm<br>
3.  Install node dependencies with NPM
    npm install -g node-gyp
    npm install node-static
    npm install node-sqlite3
4.  Clone git repository to /home/pi.  i.e. logger.py should be in /home/pi directory
    git clone git://github.com/tilimil/PIBBQMonitor.git
    cp -R ~pi/PIBBQMonitor/* ~pi/
5.  Run command to create DB.  Build_db.sh is not working currently
    sudo sqlite3 /home/pi/templog.db
    SQLite version 3.7.13 2012-06-11 02:05:22
    Enter ".help" for instructions
    Enter SQL statements terminated with a ";"
    sqlite> drop table temps; 
    Error: no such table: temps
    sqlite> CREATE TABLE temps(timestamp timestamp default (strftime('%s', 'now')), sensnum numeric, temp numeric); 
    sqlite> .quit
5.  Disable any webserver that may already be running on port 80.
    sudo update-rc.d apache2 disable
6.  Setup the thermserv node app as a service
    sudo cp /home/pi/thermserv_initfile /etc/init.d/thermserv
    sudo chmod 755 /etc/init.d/thermserv
    update-rc.d thermserv defaults
7.  Execute "sudo crontab -e" and paste the following lines into your crontab.  Logger will log the temp to the DB every minute. The dbcleanup.sh will limit the DB to 24 hours worth of data:<br>
      */1 * * * * /home/pi/logger.py<br>
      0 * * * * /home/pi/dbcleanup.sh<br>
      */1 * * * * /home/pi/alert.py<br>

