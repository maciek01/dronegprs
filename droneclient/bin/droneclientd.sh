#!/bin/sh

### BEGIN INIT INFO
# Provides:          droneclientd
# Required-Start:    $remote_fs $syslog $mavlinkd
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: droneclientd service
# Description:       droneclientd manages comms with FC via mavlink
### END INIT INFO

# Change the next 3 lines to suit where you install your script and what you want to call it
#DIR=/home/pi/dronegprs/droneclient/src
DIR=/usr/bin
#DAEMON=$DIR/Main.py
DAEMON=$DIR/screen
DAEMON_NAME=droneclientd

# Add any command line options for your daemon here
#DAEMON_OPTS=""
DAEMON_OPTS="-dmS $DAEMON_NAME -t $DAEMON_NAME -L -s /bin/bash /home/pi/dronegprs/droneclient/src/Main.py"


# This next line determines what user the script runs as.
# Root generally not recommended but necessary if you are using the Raspberry Pi GPIO from Python.
DAEMON_USER=pi
HOME_DIR=/home/$DAEMON_USER

# The process ID of the script when it runs is stored here:
PIDFILE=/var/run/$DAEMON_NAME/pid

. /lib/lsb/init-functions

do_start () {
    log_daemon_msg "Starting user $DAEMON_NAME daemon"

    cd $HOME_DIR
    rm -rf /home/pi/dronegprs/droneclient/src/*.pyc
    sudo mkdir -p /var/run/$DAEMON_NAME
    sudo chown $DAEMON_USER:$DAEMON_USER /var/run/$DAEMON_NAME

    #start-stop-daemon --start --background --pidfile $PIDFILE --make-pidfile --user $DAEMON_USER --chuid $DAEMON_USER:$DAEMON_USER --startas $DAEMON -- $DAEMON_OPTS
    sudo -u $DAEMON_USER $DAEMON $DAEMON_OPTS

    log_end_msg $?
}
do_stop () {
    log_daemon_msg "Stopping user $DAEMON_NAME daemon"
    start-stop-daemon --stop --remove-pidfile --pidfile $PIDFILE --retry 10
    log_end_msg $?
}

case "$1" in

    start|stop)
        do_${1}
        ;;

    restart|reload|force-reload)
        do_stop
        do_start
        ;;

    status)
        status_of_proc "$DAEMON_NAME" "$DAEMON" && exit 0 || exit $?
        ;;

    *)
        echo "Usage: /etc/init.d/$DAEMON_NAME {start|stop|restart|status}"
        exit 1
        ;;

esac
exit 0

