
sudo apt-get install python-pip python-dev screen python-wxgtk2.8 python-matplotlib python-opencv python-numpy python-dev libxml2-dev libxslt-dev ppp screen elinks


sudo pip install httplib2
sudo pip install pyserial
#sudo pip install pymavlink
sudo pip install mavproxy
sudo pip install dronekit

#on sim PC:
#sudo pip install dronekit-sitl





#install gprs
sudo ln -s /home/pi/dronegprs/droneclient/etc/ppp/peers/fonaUSB0 /etc/ppp/peers/fonaUSB0
sudo ln -s /home/pi/dronegprs/droneclient/etc/ppp/peers/fonaUSB1 /etc/ppp/peers/fonaUSB1
sudo ln -s /home/pi/dronegprs/droneclient/etc/ppp/peers/fonaUSB2 /etc/ppp/peers/fonaUSB2
sudo ln -s /home/pi/dronegprs/droneclient/etc/ppp/peers/fonaUSB3 /etc/ppp/peers/fonaUSB3

#install client daemon
sudo ln -s /home/pi/dronegprs/droneclient/bin/droneclientd.sh /etc/init.d/droneclientd
sudo ln -s /home/pi/dronegprs/droneclient/bin/mavlinkd.sh /etc/init.d/mavlinkd
sudo ln -s /home/pi/dronegprs/droneclient/bin/fonad.sh /etc/init.d/fonad
sudo update-rc.d droneclientd defaults
sudo update-rc.d mavlinkd defaults
sudo update-rc.d fonad defaults





