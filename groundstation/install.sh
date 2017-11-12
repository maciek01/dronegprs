
sudo apt-get install python screen python-pip python-dev

sudo pip install httplib2
sudo pip install pyserial

sudo ln -s /home/pi/dronegprs/groundstation/groundstationd.sh /etc/init.d/groundstationd

sudo update-rc.d groundstationd defaults

sudo curl -sSL https://get.docker.com | sh
sudo usermod -aG docker pi

docker pull nginx
docker pull postgres

docker run --name groundstation-nginx --restart always -v /home/pi/dronegprs/groundstation:/usr/share/nginx/html:ro -d -p 8000:80 nginx



