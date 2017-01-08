
/usr/bin/java -jar /home/pi/dronegprs/droneserver/releases/droneserver.jar 2>&1 >>/dev/null &

cd /home/pi/dronegprs/groundstation
nohup ./server.py 2>&1 >server.log &
