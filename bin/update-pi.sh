df -h

sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get dist-upgrade -y
sudo apt-get clean -y
sudo apt-get autoclean -y
sudo apt-get remove -y
sudo apt autoremove -y

sudo apt-get install git python-pip python-dev screen python-wxgtk2.8 python-matplotlib python-opencv python-numpy libxml2-dev libxslt-dev ppp elinks python3-lxml python-lxml dnsutils cu sqlite3 python-pysqlite2 -y

sudo pip install --upgrade future
sudo pip install --upgrade httplib2
sudo pip install --upgrade pyserial
sudo pip2 install --upgrade dronekit


#alternative:
#pip unistall pymavlink (multiple times)
#pip unistall dronekit (multiple times)
#cd ~
#git clone https://github.com/dronekit/dronekit-python.git
#cd ./dronekit-python
#sudo python setup.py build
#sudo python setup.py install



#not needed for on board
#sudo pip install --upgrade mavproxy

#on sim PC:
#sudo pip install dronekit-sitl

sudo rpi-update
