df -h

sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get dist-upgrade -y
sudo apt-get clean -y
sudo apt-get autoclean -y
sudo apt-get remove -y

sudo apt-get install git python-pip python-dev screen python-wxgtk2.8 python-matplotlib python-opencv python-numpy libxml2-dev libxslt-dev ppp elinks python3-lxml python-lxml dnsutils cu sqlite3 python-pysqlite2 -y

sudo pip install --upgrade future
sudo pip install --upgrade httplib2
sudo pip install --upgrade pyserial
sudo pip install --upgrade dronekit

#not needed for on board
#sudo pip install --upgrade mavproxy

#on sim PC:
#sudo pip install dronekit-sitl

sudo rpi-update
