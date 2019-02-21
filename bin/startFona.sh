#!/bin/bash

#exec 1> >(logger -s -t $(basename $0)) 2>&1

#clear state

sudo ifconfig wlan0 up

#wait for USB

while [ `lsusb |grep Qualcomm|wc -l ` -eq '0' ]
do
    sleep 1
done

#stop wifi
if [ ! -f $HOME/wifi ]; then
    echo "turn wifi off"
    sudo ifconfig wlan0 down
fi

#modem is up

sleep 2



#start gprs

#MODEM="$($HOME/dronegprs/src/getModem.py)"
MODEM="/dev/ttyUSB2"

echo "Modem id "$MODEM - ${MODEM: -4}

echo $MODEM > $HOME/modemline

if [ "$MODEM" == "" ]; then
	echo "no modem line"
	exit
else
      echo "modem found"
fi

sleep 2
echo "ATZ" >>$MODEM
sleep 2
echo "AT+CFUN=1,1" >>$MODEM
sleep 5

#sudo pon fonaUSB0 debug dump logfd 2 updetach
#sudo pon fonaUSB0

pon mobile-noauth-${MODEM: -4}

sleep 1


#wait for USB

while [ `ifconfig |grep ppp0|wc -l ` -eq '0' ]
do
    sleep 1
done

sleep 5

>$HOME/modemup

sudo cp /home/pi/dronegprs/resolv.conf.8.8.8.8 /etc/resolv.conf
sudo cp /home/pi/dronegprs/resolv.conf.8.8.8.8 /etc/ppp/resolv.conf


IP=`/sbin/ip addr show ppp0 | grep peer | awk ' { print $4 } ' | sed 's/\/32//'`
echo $IP
echo $IP >$HOME/ppp0-ip


