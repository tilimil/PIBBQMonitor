#!/bin/bash
sqlite3 /home/pi/templog.db "delete from temps where timestamp <= strftime('%s', 'now') - 86400;"
