#!/bin/bash
#
# 
sudo sqlite3 /home/pi/templog.db 'DROP TABLE temps;'
sudo sqlite3 /home/pi/templog.db 'CREATE TABLE temps(timestamp timestamp default (strftime('%s', 'now')), sensnum numeric, temp numeric);' 
