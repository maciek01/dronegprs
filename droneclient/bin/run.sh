#!/bin/bash

#exec 1> >(logger -s -t $(basename $0)) 2>&1



cd /home/pi/dronegprs/droneclient


#start gprs

sleep 2
echo "AT" >>/dev/ttyUSB0
sleep 1
echo "AT" >>/dev/ttyUSB0
sleep 1
echo "AT+CFUN=1,1" >>/dev/ttyUSB0
sleep 5

#sudo pon fonaUSB0 debug dump logfd 2 updetach
sudo pon fonaUSB0
sleep 5

IP=`/sbin/ip addr show ppp0 | grep peer | awk ' { print $4 } ' | sed 's/\/32//'`
echo $IP




#sudo route del default
#sudo route add default ppp0



#start mavlink
screen -d -m /home/pi/dronegprs/droneclient/bin/mavproxy.sh 2>&1 >>/dev/null &
#screen -d -m /home/pi/dronegprs/droneclient/bin/mavproxy.sh 2>&1 &

#start drone controller
#/usr/bin/python /home/pi/dronegprs/droneclient/src/Main.py 2>&1 >>/dev/null &
/usr/bin/python /home/pi/dronegprs/droneclient/src/Main.py 2>&1 >>/home/pi/pilot.log &

