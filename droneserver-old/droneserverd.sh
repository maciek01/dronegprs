#!/bin/bash
# /etc/init.d/droneserverd

### BEGIN INIT INFO
# Provides:          droneserver
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Example initscript
# Description:       This service is used to manage drone 
### END INIT INFO


case "$1" in 
    start)
        echo "Starting droneserverd"
        sudo -u pi /home/pi/dronegprs/droneserver/run.sh
        ;;
    stop)
        echo "Stopping droneserverd"
        sudo -u pi killall /usr/bin/java
        ;;
    *)
        echo "Usage: /etc/init.d/droneserverd start|stop"
        exit 1
        ;;
esac

exit 0

