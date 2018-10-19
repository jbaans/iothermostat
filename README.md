## iothermostat - Independent Open-source Thermostat


Built for the HestiaPi Touch system, see: https://hestiapi.com/

## Features:

Displays current temperature, humidity and pressure.

Allows changing set temperature.

Allows setting modes: Auto/On/Off/Boost/Sleep

Allows scheduling, browse to scheduler.php.

Security is based on restricting access to the webinterface using (digest) web server authentication.

# INSTALLATION INSTRUCTIONS

You can download a pre-configured image or you can do everything yourself, see below. The pre-configured image is built  according to the complete manual installation instructions.

## Using the pre-configured Arch image:

Get disk2-archarmv6-iothermostat-181016.img.zip from this link:

https://drive.google.com/file/d/1FxYcYQ5RrKbFVnKMtyjQSLOg3z8utUXH/view?usp=sharing

MD5 (disk2-archarmv6-iothermostat-181016.img.zip) = e8c209d1e5275c36f82b6012f401aae7

The image includes:

    Arch Linux ARM v6
    IOThermostat https://github.com/jbaans/iothermostat
    Python
    Lighttpd
    Mosquitto
    Blackbox
    Midori
    Wifi hotspot when no Wifi network available
    
1. Download, verify MD5 sum, unzip and write image to microsd card
2. Insert the card and power up. Display should show start log and finish into the IOThermostat GUI.
3. Connect your PC to hotspot IOTHERMOSTAT with password iothermostat0.
4. ssh to 10.42.0.1 on port 2222 with user iothermostat, password iothermostat2018.
5. Replace connectWifi.sh with that from https://github.com/jbaans/iothermostat/blob/master/configuration_files/home/connectWifi.sh (this fixes two passphrase bugs). Configure your wifi network (drops connection):

<pre> sudo ./connectWifi.sh YOURSSID </pre>

6. Connect your PC to YOURSSID, find the ip of iothermostat (see display-advanced/router/network) and ssh to x.x.x.x on port 2222 with user iothermostat, password iothermostat2018.

7. Finally follow the instructions on:

https://github.com/jbaans/iothermostat/wiki/IOThermostat-installation


## Completely Manual:

1. Follow these instruction to set up the OS:

https://github.com/jbaans/iothermostat/wiki/Install-Arch-Linux-ARM-with-Wifi-on-Raspberry-Pi-Zero,B

2. Install these packages (Note: I need to update this list):
<pre>sudo pacman -Syu git python python-pip lighttpd fcgi wget pwgen php php-cgi php-sqlite sqlite libwebsockets fail2ban midori blackbox ddclient certbot nftables</pre>

3. Install these packages with python/pip:
<pre>python -m pip install paho-mqtt apscheduler sqlalchemy</pre>

4. Copy configuration files in:

download and copy iothermostat/* to /home/iothermostat/iothermostat/
 
download and copy webinterface/* to /srv/http/iothermostat/
 
download configuration_files to /home/iothermostat/

<pre> cd /home/iothermostat/configuration_files </pre>

Copy (with backup enabled) config files and scripts to their locations:

<pre> sudo ./deployetc.sh </pre>
<pre> ./deployhome.sh </pre>

<pre> sudo cp LCD-show/waveshare35a-overlay.dtb /boot </pre>


5. Mosquitto installation:

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

6. Finally follow the instructions on:

https://github.com/jbaans/iothermostat/wiki/IOThermostat-installation


