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

DAEMON=/home/pi/dronegprs/droneclient/bin/run.sh
DAEMON_OPTS=""
NAME=droneclientd
DESC="droneclientd"
PID=/var/run/droneclientd.pid


case "$1" in 
    start)
	echo -n "Starting $DESC: "
	start-stop-daemon --start --chuid pi --pidfile "$PID" --start --exec "$DAEMON" -- $DAEMON_OPTS
	echo "$NAME."
        ;;
    stop)
	echo -n "Stopping $DESC: "
	start-stop-daemon --stop --quiet --retry=TERM/30/KILL/5 --pidfile $PIDFILE --exec $DAEMON
        ;;
    *)
        echo "Usage: /etc/init.d/droneclientd start|stop"
        exit 1
        ;;
esac

exit 0

