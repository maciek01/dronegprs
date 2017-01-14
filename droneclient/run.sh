cd /home/pi/dronegprs/droneclient

#start gprs

sleep 1

echo "AT" >>/dev/ttyUSB0
echo "AT" >>/dev/ttyUSB0
echo "AT+CFUN=1,1" >>/dev/ttyUSB0

sleep 5

sudo pon fonaUSB0 debug debug dump logfd 2 updetach

sleep 1

IP=`/sbin/ip addr show ppp0 | grep peer | awk ' { print $4 } ' | sed 's/\/32//'`
echo $IP




#sudo route del default
#sudo route add default ppp0



#start mavlink
screen -d -m /home/pi/dronegprs/droneclient/mavproxy.sh 2>&1 >>/dev/null &

#start drone controller
/usr/bin/python /home/pi/dronegprs/droneclient/Main.py 2>&1 >>/dev/null &

