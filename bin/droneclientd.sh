#!/bin/sh

### BEGIN INIT INFO
# Provides:          droneclientd
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: droneclientd service
# Description:       droneclientd manages comms with FC via mavlink
### END INIT INFO

# Change the next 3 lines to suit where you install your script and what you want to call it
#DIR=/home/pi/dronegprs/src
DIR=/usr/bin
DAEMON=$DIR/screen
DAEMON_NAME=droneclientd

# Add any command line options for your daemon here
DAEMON_OPTS="-c /tmp/screenrc.$$ -dmS $DAEMON_NAME -t $DAEMON_NAME -L -s /bin/bash /home/pi/dronegprs/src/Main.py"



DAEMON=$DIR/python

# Add any command line options for your daemon here
DAEMON_OPTS="/home/pi/dronegprs/src/Main.py"




# This next line determines what user the script runs as.
# Root generally not recommended but necessary if you are using the Raspberry Pi GPIO from Python.
DAEMON_USER=pi
HOME_DIR=/home/$DAEMON_USER

DAEMON_OPTS="$DAEMON_OPTS --config $HOME_DIR/main.cfg"

# The process ID of the script when it runs is stored here:
PIDFILE=/var/run/$DAEMON_NAME/pid

. /lib/lsb/init-functions

#setup screen config
cat << EOF >/tmp/screenrc.$$
logfile $HOME_DIR/pilot.log
EOF

do_start () {
    log_daemon_msg "Starting user $DAEMON_NAME daemon"

    cd $HOME_DIR
    rm -rf /home/pi/dronegprs/src/*.pyc
    rm -rf /home/pi/modemup
    sudo mkdir -p /var/run/$DAEMON_NAME
    sudo chown $DAEMON_USER:$DAEMON_USER /var/run/$DAEMON_NAME
    start-stop-daemon --start --background --pidfile $PIDFILE --make-pidfile --user $DAEMON_USER --chuid $DAEMON_USER:$DAEMON_USER --startas /bin/bash -- -c "exec $DAEMON $DAEMON_OPTS > $HOME_DIR/pilot.log 2>&1"
    #sudo -u $DAEMON_USER $DAEMON $DAEMON_OPTS
    rm /tmp/screenrc.$$
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

