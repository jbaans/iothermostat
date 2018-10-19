## iothermostat - Independent Open-source Thermostat


Built for the HestiaPi Touch system, see: https://hestiapi.com/

## Features:

Displays current temperature, humidity and pressure.

Allows changing set temperature.

Allows setting modes: Auto/On/Off/Boost/Sleep

Allows scheduling, browse to scheduler.php.

Security is based on restricting access to the webinterface using (digest) web server authentication.

# INSTALLATION INSTRUCTIONS

(Sorry, these instructions are a mess still. To be updated soon!)

## Download the pre-configured Arch ARM v6 image here:

https://drive.google.com/file/d/1FxYcYQ5RrKbFVnKMtyjQSLOg3z8utUXH/view?usp=sharing

MD5 (disk2-archarmv6-iothermostat-181016.img.zip) = e8c209d1e5275c36f82b6012f401aae7

Features:

    Arch ARM v6 Linux
    IOThermostat https://github.com/jbaans/iothermostat
    Python
    Lighttpd
    Mosquitto
    Blackbox
    Midori
    Wifi hotspot when no Wifi network available
    
    
Follow the instructions on:
https://community.hestiapi.com/t/iothermostat-image/806


## Complete manual installation:

Follow these instruction to set up the OS:

https://github.com/jbaans/iothermostat/wiki/Install-Arch-Linux-ARM-with-Wifi-on-Raspberry-Pi-Zero,B

Then install these packages:
<pre>sudo pacman -Syu git python python-pip lighttpd fcgi wget pwgen php php-cgi php-sqlite sqlite libwebsockets fail2ban midori blackbox</pre>

 install these packages with python/pip:
<pre>python -m pip install paho-mqtt apscheduler sqlalchemy</pre>

 download and copy iothermostat/* to /home/iothermostat/iothermostat/
 
 download and copy webinterface/* to /srv/http/iothermostat/
 
 download configuration_files to /home/iothermostat/

<pre> cd /home/iothermostat/configuration_files </pre>

Copy (with backup enabled) config files and scripts to their locations:

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
Follow from step 7 (set passwords).


