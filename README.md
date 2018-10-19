## iothermostat - Independent Open-source Thermostat


Built for the HestiaPi Touch system, see: https://hestiapi.com/

## Features:

Displays current temperature, humidity and pressure.

Allows changing set temperature.

Allows setting modes: Auto/On/Off/Boost/Sleep

Allows scheduling, browse to scheduler.php.

# INSTALLATION INSTRUCTIONS

(Sorry, these instructions are a mess still. To be updated soon!)

For installation of the Arch ARM system, see:

https://github.com/jbaans/iothermostat/wiki/Install-Arch-Linux-ARM-on-Raspberry-Pi-Zero

 These are for a non-https webinterface
 
 Note: A secure / https setup requires some more configuration (instructions to be added).


 Don't use non-secure/https on public accessible systems.
 
 ### Security of this setup relies on restricting access to the webinterface using (digest) web server authentication!
 

 Requirements: mosquitto, python3, a web server (like lighttpd), sqlite; knowledge on how to host a php site and restricting access to it.
 

 install these packages with your package manager:
<pre>git python python-pip lighttpd fcgi wget pwgen php php-cgi php-sqlite sqlite</pre>

 install these packages with python/pip:
<pre>python -m pip install paho-mqtt apscheduler sqlalchemy</pre>


 download and copy iothermostat/* to /home/iothermostat/iothermostat/
 
 download and copy webinterface/* to /srv/http/iothermostat/
 
 download configuration_files to /home/iothermostat/

<pre> cd /home/iothermostat/configuration_files </pre>

on a fresh install run (these will copy (with backup enabled) config files and scripts to their locations:

<pre> ./deployetc.sh </pre>
<pre> ./deployhome.sh </pre>


 ## mosquitto installation:

 install mosquitto MQTT with websockets
<pre>
cd /home/iothermostat/builds 
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

# iothermostat installation:
See https://community.hestiapi.com/t/iothermostat-image/806
Follow from step 3.


