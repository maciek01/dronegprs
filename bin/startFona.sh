#!/bin/bash

#exec 1> >(logger -s -t $(basename $0)) 2>&1

#cleanup wifi
sudo ifconfig wlan0 up

#wait for USB
while [ `lsusb |grep Qualcomm|wc -l ` -eq '0' ]
do
    sleep 1
done

#modem is up
sleep 1

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

#reset and ping the modem
echo "ATZ" >>$MODEM
sleep 2
echo "AT+CFUN=1,1" >>$MODEM
sleep 2

#dial up
pon mobile-noauth-${MODEM: -4}
sleep 1

#wait for ppp0
while [ `ifconfig |grep ppp0|wc -l ` -eq '0' ]
do
    sleep 1
done
sleep 5

>$HOME/modemup

#capture ppp0 interface ip
IP=`/sbin/ip addr show ppp0 | grep peer | awk ' { print $4 } ' | sed 's/\/32//'`
echo ppp0 ip $IP
echo $IP >$HOME/ppp0-ip

#capture wlan0 interface ip and gateway
WLAN_IP=`/sbin/ip addr show wlan0 | grep peer | awk ' { print $4 } ' | sed 's/\/32//'`
echo wlan0 ip $WLAN_IP
echo $WLAN_IP >$HOME/wlan0-ip

WLAN_GW=`/sbin/ip addr show wlan0 | grep peer | awk ' { print $4 } ' | sed 's/\/32//'`
echo wlan0 gw $WLAN_GW
echo $WLAN_GW >$HOME/wlan0-gw

#fixup dns
sudo cp $HOME/dronegprs/resolv.conf.8.8.8.8 /etc/resolv.conf
sudo cp $HOME/pi/dronegprs/resolv.conf.8.8.8.8 /etc/ppp/resolv.conf

#fixup routing

#default state
#Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
#default         192.168.2.1     0.0.0.0         UG    304    0        0 wlan0
#10.64.64.64     *               255.255.255.255 UH    0      0        0 ppp0
#192.168.2.0     *               255.255.255.0   U     304    0        0 wlan0

set +e
sudo route delete default gw 192.168.2.1 wlan0
sudo route add default gw $IP ppp0
set -e

#autonomous state
#Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
#default         10.64.64.64     0.0.0.0         UG    0      0        0 ppp0
#10.64.64.64     *               255.255.255.255 UH    0      0        0 ppp0
#192.168.2.0     *               255.255.255.0   U     304    0        0 wlan0

#stop wifi
if [ ! -f $HOME/wifi ]; then
    echo "turn wifi off"
    sudo ifconfig wlan0 down
fi

