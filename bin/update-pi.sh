df -h

sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get dist-upgrade -y
sudo apt-get clean -y
sudo apt-get autoclean -y
sudo apt-get remove -y
sudo apt autoremove -y

sudo apt-get install git python-pip python-dev screen python-wxgtk2.8 python-matplotlib python-opencv python-numpy libxml2-dev libxslt-dev ppp elinks python3-lxml python-lxml dnsutils cu sqlite3 python-pysqlite2 ffmpeg gstreamer-1.0 gstreamer1.0-tools gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly -y

sudo pip install --upgrade future
sudo pip install --upgrade httplib2
sudo pip install --upgrade pyserial
#sudo pip2 install --upgrade dronekit


#alternative - run each multiple time:
sudo pip uninstall pymavlink
sudo pip uninstall dronekit

cd ~
git clone https://github.com/dronekit/dronekit-python.git
cd ./dronekit-python
sudo python setup.py build
sudo python setup.py install
cd ~
sudo rm -rf dronekit-python

sudo rpi-update
