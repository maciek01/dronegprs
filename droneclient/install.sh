
sudo apt-get install python-pip
sudo pip install httplib2
sudo pip install pyserial
sudo ln -s /home/pi/dronegprs/droneclient/droneclientd.sh /etc/init.d/droneclientd

sudo update-rc.d droneclientd defaults
