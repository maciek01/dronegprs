

docker container prune --force
docker run --name groundstation-nginx -v /home/pi/dronegprs/groundstation:/usr/share/nginx/html:ro -d -p 8000:80 nginx

#cd /home/pi/dronegprs/groundstation
#nohup ./server.py 2>&1 >server.log &


