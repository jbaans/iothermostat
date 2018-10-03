# iothermostat
Independent Open-source Thermostat

### INSTALLATION INSTRUCTIONS for IOTHERMOSTAT
###
### These are for a non-https webinterface
### Note: Https requires much more configuration (instructions to be added).
###
### Don't use this on public accessible systems.
### Restrict access to the webinterface using (digest) web server authentication.
###
### Requirements: mosquitto, python3, a web server (like lighttpd), sqlite

### install these packages with your package manager:
git python python-pip lighttpd fcgi wget pwgen php php-cgi php-sqlite sqlite

### install these packages with python/pip:
python -m pip install paho-mqtt apscheduler sqlalchemy


### copy iothermostat/* to /home/YOURUSERNAME/iothermostat/
### copy webinterface/* to /srv/http/iothermostat/


###
### mosquitto installation:
###
# install mosquitto MQTT with websockets
cd /home/YOURNAME/builds 
git clone https://github.com/eclipse/mosquitto.git
cd mosquitto
# select 2018 feb 23 version:
git checkout 4f838e5
nano config.mk -->
#
WITH_WEBSOCKETS:=yes
WITH_DOCS:=no
#
make binary
make install

###
### edit /etc/mosquitto/mosquitto.conf to contain:
###

include_dir /etc/mosquitto/conf.d

###
### edit/create /etc/mosquitto/aclfile to contain:
###
# iothermostat backend user access:
user pyiothermostat
topic write iothermostat0/sensor/#
topic write iothermostat0/state/#
topic readwrite iothermostat0/settings/#

# iothermostat GUI frontend user access:
user jsiothermostat
topic read iothermostat0/sensor/#
topic read iothermostat0/state/#
topic readwrite iothermostat0/settings/#

###
### generate/append /etc/mosquitto/credentials:
###
# generate a strong password (not required for login):
echo $(pwgen -1)$(pwgen -1)
# copy paste password after running:
# (only use switch -c if /etc/mosquitto/credentials does not exist):
sudo mosquitto_passwd -c /etc/mosquitto/credentials pyiothermostat
# edit and copy paste the pyiothermostat password to replace PASSWORD in:
/home/YOURUSERNAME/iothermostat/mqttconf.py

# generate a strong password (not required for login):
echo $(pwgen -1)$(pwgen -1)
sudo mosquitto_passwd /etc/mosquitto/credentials jsiothermostat
# edit and copy paste the jsiothermostat password to replace PASSWORD in:
/srv/http/iothermostat/store.php

# adjust rights:
sudo chmod 700 /etc/mosquitto/credentials

###
### create /etc/mosquitto/conf.d/iothermostat.conf:
###
user mosquitto
pid_file /var/run/mosquitto.pid

acl_file /etc/mosquitto/aclfile
password_file /etc/mosquitto/credentials
allow_anonymous false

## SSL socket
#listener 9001
#max_connections 32
#protocol websockets
#cafile /etc/letsencrypt/live/YOURDOMAIN/fullchain.pem
#certfile /etc/letsencrypt/live/YOURDOMAIN/cert.pem
#keyfile /etc/letsencrypt/live/YOURDOMAIN/privkey.pem

listener 9002
max_connections 32
protocol websockets

listener 1883
max_connections 16
protocol mqtt

message_size_limit 10240
autosave_interval 3600
autosave_on_changes false
persistence true
persistence_file mosquitto.db
persistence_location /var/lib/mosquitto/

#logging debug, error, warning, notice, information, subscribe, unsubscribe, websockets
connection_messages true
#websockets_log_level 7
log_type error
log_type warning
log_type websockets
log_type notice
log_type information


###
### configure iothermostat datalog:
###
#in /home/YOURUSERNAME/iothermostat/iothermostat.py edit:
DATALOGFILE = '/home/YOURUSERNAME/iothermostat.csv'


###
### (re)start mosquitto:
###
sudo systemctl restart mosquitto


###
### test iothermostat backend
###
cd /home/YOURUSERNAME/iothermostat
sudo python iothermostat.py


###
### check logs:
###
sudo journalctl -r -b


###
### start iothermostat with  a systemd unit file:
###
### create /etc/systemd/system/iothermostat.service containing:
[Unit]
Description=IOThermostat Backend Service
After=multi-user.target mosquitto.target

[Service]
Type=idle
ExecStart=/usr/bin/python -u /home/YOURUSERNAME/iothermostat/iothermostat.py

[Install]
WantedBy=multi-user.target

### reload units:
sudo systemctl daemon-reload
sudo systemctl start iothermostat.service

### run iothermostat at boot
sudo systemctl enable iothermostat.service

