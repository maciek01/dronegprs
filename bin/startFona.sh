#!/bin/bash

#exec 1> >(logger -s -t $(basename $0)) 2>&1


#wait for USB

while [ `lsusb |grep Qualcomm|wc -l ` -eq '0' ]
do
    sleep 1
done


#start gprs

sleep 2
echo "AT" >>/dev/ttyUSB0
sleep 1
echo "AT" >>/dev/ttyUSB0
sleep 1
echo "AT+CFUN=1,1" >>/dev/ttyUSB0
sleep 5

#sudo pon fonaUSB0 debug dump logfd 2 updetach
#sudo pon fonaUSB0
pon mobile-noauth-USB2

sleep 5

IP=`/sbin/ip addr show ppp0 | grep peer | awk ' { print $4 } ' | sed 's/\/32//'`
echo $IP

#sudo route del default
#sudo route add default ppp0

