#!/bin/bash
sqlite3 /var/www/templog.db "delete from temps where timestamp <= strftime('%s', 'now') - 86400;"
