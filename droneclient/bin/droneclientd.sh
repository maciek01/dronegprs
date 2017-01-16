#!/bin/bash
# /etc/init.d/droneclientd

### BEGIN INIT INFO
# Provides:          droneclient
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Example initscript
# Description:       This service is used to manage drone 
### END INIT INFO


case "$1" in 
    start)
        echo "Starting droneclientd"
        sudo -u pi /home/pi/dronegprs/droneclient/bin/run.sh
        ;;
    stop)
        echo "Stopping droneclientd"
        sudo -u pi killall /usr/bin/python
        ;;
    *)
        echo "Usage: /etc/init.d/droneclientd start|stop"
        exit 1
        ;;
esac

exit 0

