cd /home/pi/dronegprs/droneclient

#start gprs

sudo pon fonaUSB0

#start mavlink

screen -d -m /home/pi/dronegprs/droneclient/mavproxy.sh 2>&1 >>/dev/null &

#start drone controller

/usr/bin/python /home/pi/dronegprs/droneclient/Main.py 2>&1 >>/dev/null &
#/usr/bin/python /home/pi/dronegprs/droneclient/Main.py 2>&1 >>/dev/null &

