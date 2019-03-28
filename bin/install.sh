

#git clone https://github.com/maciek01/dronegprs.git

#install pppd for wireless

# 3G:
sudo ln -s /home/pi/dronegprs/etc/ppp/chatscripts /etc/ppp/chatscripts
sudo ln -s /home/pi/dronegprs/etc/ppp/options-mobile /etc/ppp/options-mobile

sudo ln -s /home/pi/dronegprs/etc/ppp/peers/mobile-noauth-USB0 /etc/ppp/peers/mobile-noauth-USB0
sudo ln -s /home/pi/dronegprs/etc/ppp/peers/mobile-noauth-USB1 /etc/ppp/peers/mobile-noauth-USB1
sudo ln -s /home/pi/dronegprs/etc/ppp/peers/mobile-noauth-USB2 /etc/ppp/peers/mobile-noauth-USB2
sudo ln -s /home/pi/dronegprs/etc/ppp/peers/mobile-noauth-USB3 /etc/ppp/peers/mobile-noauth-USB3

# 2G:
sudo ln -s /home/pi/dronegprs/etc/ppp/peers/fonaUSB0 /etc/ppp/peers/fonaUSB0
sudo ln -s /home/pi/dronegprs/etc/ppp/peers/fonaUSB1 /etc/ppp/peers/fonaUSB1
sudo ln -s /home/pi/dronegprs/etc/ppp/peers/fonaUSB2 /etc/ppp/peers/fonaUSB2
sudo ln -s /home/pi/dronegprs/etc/ppp/peers/fonaUSB3 /etc/ppp/peers/fonaUSB3

#install client daemon

sudo ln -s /home/pi/dronegprs/bin/droneclientd.sh /etc/init.d/droneclientd
#mavlink is only necessary to bridge over between on board and offboard computers
#sudo ln -s /home/pi/dronegprs/bin/mavlinkd.sh /etc/init.d/mavlinkd
sudo ln -s /home/pi/dronegprs/bin/fonad.sh /etc/init.d/fonad
sudo update-rc.d droneclientd defaults
#sudo update-rc.d mavlinkd defaults
sudo update-rc.d fonad defaults

sudo usermod -a -G dip pi
#sudo usermod -G pi,adm,dialout,cdrom,sudo,audio,video,plugdev,games,users,input,netdev,gpio,i2c,spi,dip pi

