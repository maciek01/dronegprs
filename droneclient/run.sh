cd /home/pi/dronegprs/droneclient
screen -d -m /home/pi/dronegprs/droneclient/mavproxy.sh 2>&1 >>drone.log &
/usr/bin/python /home/pi/dronegprs/droneclient/Main.py 2>&1 >>drone.log &
#/usr/bin/python /home/pi/dronegprs/droneclient/Main.py 2>&1 >/dev/null &

