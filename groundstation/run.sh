

docker container prune --force
docker run --name groundstation-nginx -v /home/pi/dronegprs/groundstation:/usr/share/nginx/html:ro -d -p 8000:80 nginx
docker run --name pi-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=pi -d -p 5432:5432 postgres

#cd /home/pi/dronegprs/groundstation
#nohup ./server.py 2>&1 >server.log &


