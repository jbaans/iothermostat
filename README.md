## iothermostat - Independent Open-source Thermostat


Built for the HestiaPi Touch system, see: https://hestiapi.com/



 INSTALLATION INSTRUCTIONS

(Sorry, these instructions are a mess still. To be updated soon!)

 These are for a non-https webinterface
 
 Note: A secure / https configuration requires much more config files (instructions to be added).


 Don't use this on public accessible systems.
 
 Restrict access to the webinterface using (digest) web server authentication.
 

 Requirements: mosquitto, python3, a web server (like lighttpd), sqlite
 

 install these packages with your package manager:
<pre>git python python-pip lighttpd fcgi wget pwgen php php-cgi php-sqlite sqlite</pre>

 install these packages with python/pip:
<pre>python -m pip install paho-mqtt apscheduler sqlalchemy</pre>


 copy iothermostat/* to /home/YOURUSERNAME/iothermostat/
 
 copy webinterface/* to /srv/http/iothermostat/



 ## mosquitto installation:

 install mosquitto MQTT with websockets
<pre>
cd /home/YOURNAME/builds 
git clone https://github.com/eclipse/mosquitto.git
cd mosquitto
</pre>
select 2018 feb 23 version:
<pre>
git checkout 4f838e5
</pre>

edit config.mk to contain:
<pre>
WITH_WEBSOCKETS:=yes
WITH_DOCS:=no
</pre>

build mosquitto:
<pre>make binary</pre>
<pre>make install</pre>


 edit /etc/mosquitto/mosquitto.conf to contain:


<pre>include_dir /etc/mosquitto/conf.d</pre>


 edit/create /etc/mosquitto/aclfile to contain:

<pre>
#iothermostat backend user access:
user pyiothermostat
topic write iothermostat0/sensor/#
topic write iothermostat0/state/#
topic readwrite iothermostat0/settings/#

# iothermostat GUI frontend user access:
user jsiothermostat
topic read iothermostat0/sensor/#
topic read iothermostat0/state/#
topic readwrite iothermostat0/settings/#
</pre>


 generate/append /etc/mosquitto/credentials:
generate a strong password (not required for login):
<pre>echo $(pwgen -1)$(pwgen -1)</pre>
 copy paste password after running:
 (only use switch -c if /etc/mosquitto/credentials does not exist):
<pre>sudo mosquitto_passwd -c /etc/mosquitto/credentials pyiothermostat</pre>
 edit and copy paste the pyiothermostat password to replace PASSWORD in:
<pre>/home/YOURUSERNAME/iothermostat/mqttconf.py</pre>

 generate a strong password (not required for login):
<pre>echo $(pwgen -1)$(pwgen -1)</pre>
<pre>sudo mosquitto_passwd /etc/mosquitto/credentials jsiothermostat</pre>
 edit and copy paste the jsiothermostat password to replace PASSWORD in:
<pre>/srv/http/iothermostat/store.php</pre>

 adjust rights:
<pre>sudo chmod 700 /etc/mosquitto/credentials</pre>


 create /etc/mosquitto/conf.d/iothermostat.conf:

<pre>
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
</pre>


 configure iothermostat datalog, in /home/YOURUSERNAME/iothermostat/iothermostat.py edit:
<pre>DATALOGFILE = '/home/YOURUSERNAME/iothermostat.csv'</pre>



 (re)start mosquitto:

<pre>sudo systemctl restart mosquitto</pre>


## Running iothermostat backend

Test iothermostat:

<pre>cd /home/YOURUSERNAME/iothermostat</pre>
<pre>sudo python iothermostat.py</pre>



Check logs:

<pre>sudo journalctl -r -b</pre>


If everything runs without errors, the webinterface should be able to connect with the python backend via mosquitto.


## Configuring iothermostat as a service
 start iothermostat with  a systemd unit file:

 create /etc/systemd/system/iothermostat.service containing:
<pre>
[Unit]
Description=IOThermostat Backend Service
After=multi-user.target mosquitto.target

[Service]
Type=idle
ExecStart=/usr/bin/python -u /home/YOURUSERNAME/iothermostat/iothermostat.py

[Install]
WantedBy=multi-user.target
</pre>

 reload units:
<pre>sudo systemctl daemon-reload</pre>
<pre>sudo systemctl start iothermostat.service</pre>

 run iothermostat at boot
<pre>sudo systemctl enable iothermostat.service</pre>



