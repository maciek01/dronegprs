cd /home/pi/dronegprs/droneclient

#start gprs

sleep 5
sudo pon fonaUSB0
sleep 5

IP=`/sbin/ip addr show ppp0 | grep peer | awk ' { print $4 } ' | sed 's/\/32//'`

#sudo route del default
#sudo route add default ppp0



#start mavlink

screen -d -m /home/pi/dronegprs/droneclient/mavproxy.sh 2>&1 >>/dev/null &

#start drone controller

/usr/bin/python /home/pi/dronegprs/droneclient/Main.py 2>&1 >>/dev/null &
#/usr/bin/python /home/pi/dronegprs/droneclient/Main.py 2>&1 >>/dev/null &

