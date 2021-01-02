df -h

sudo apt update -y
sudo apt upgrade -y
sudo apt dist-upgrade -y
sudo apt clean -y
sudo apt autoclean -y
sudo apt remove -y
sudo apt autoremove -y

sudo apt install git python-pip python-dev screen python-wxgtk2.8 python-matplotlib python-opencv python-numpy libxml2-dev libxslt-dev ppp elinks python3-lxml python-lxml dnsutils cu sqlite3 python-pysqlite2 -y
sudo apt install libgstreamer1.0-0 libgstreamer1.0-0-dbg libgstreamer1.0-dev liborc-0.4-0 liborc-0.4-0-dbg liborc-0.4-dev liborc-0.4-doc gir1.2-gst-plugins-base-1.0 gir1.2-gstreamer-1.0 gstreamer1.0-alsa gstreamer1.0-doc gstreamer1.0-omx gstreamer1.0-plugins-bad gstreamer1.0-plugins-bad-dbg gstreamer1.0-plugins-bad-doc gstreamer1.0-plugins-base gstreamer1.0-plugins-base-apps gstreamer1.0-plugins-base-dbg gstreamer1.0-plugins-base-doc gstreamer1.0-plugins-good gstreamer1.0-plugins-good-dbg gstreamer1.0-plugins-good-doc gstreamer1.0-plugins-ugly gstreamer1.0-plugins-ugly-dbg gstreamer1.0-plugins-ugly-doc gstreamer1.0-pulseaudio gstreamer1.0-tools gstreamer1.0-x libgstreamer-plugins-bad1.0-0 libgstreamer-plugins-bad1.0-dev libgstreamer-plugins-base1.0-0 libgstreamer-plugins-base1.0-dev -y


sudo pip install --upgrade future httplib2 requests pyserial
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

#sudo rpi-update
