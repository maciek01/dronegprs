# dronegprs

Goal of the project is to establish 2 way control between ground station server and a fleet of UAVs (drones, planes, ...) leveraging GSM GPRS based data networks.

The idea is to enable governmental institutions to autonomously deploy drones in event of minor scale emergencies with ability to monitor and control the deployment of each indivudual UAV.


Scope of POC:

Each UAV will be equipped with MAVlink compatible flight controller, GPS module, Raspbery PI connected to USB GPRS modem. Raspberry pie will host the following software: DroneKit, custom developed status reporting service, as well as custom RESTfull server to enable processing of ground station commands.

"Ground station" is based on an HTTP RESTfull service deployed and available via public internet.


Each UAV will report its stats (position, speed, altitude, heading, battery state, etc.) to the ground station via HTTP client.

Groud station will allow operatios to monitor/visualize each UAV status/location, and command it remotely (via REST service deployed onboard). Examples of command: land immediately, return to home/abord the mission, deploy payload, alter course/go to waypoint, alter mission, swarm, travel to another UAV.


ground station console: http://home.kolesnik.org:8000/map.html



SETUP

run:

sudo raspi-config

and enable camera then restar RPi. Test camera: raspivid -o vid.h264

It shoudl capyture 10 secs of jmpeg video


Then run:

bin/update-pi.sh (may require some manual "pushing")

run:

bin/install.sh



