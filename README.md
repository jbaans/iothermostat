## IOThermostat - Independent Open-source Thermostat


Built for the HestiaPi Touch system with high security in mind, see: https://hestiapi.com/

Intended users: developers

Highlights:

* Disk image and instructions for Raspberry Pi Zero, Zero W or 1 A/B + Waveshare LCD

* Use Manual instructions for installing on a different device

* For use on a non Raspberry Pi compatible device, simply use your own GPIO driver

## Features:

Display current temperature, humidity and pressure.

Set modes: Auto/On/Off/Boost (1h)/Sleep (24h)

Set temperature for each mode.

Remote web interface with authentication.

Scheduling for Auto mode

Full encryption of web traffic.

Many security features.

# UPGRADING INSTRUCTIONS

<pre>
cd /home/iothermostat/builds
rm -rf iothermostat
git clone https://github.com/jbaans/iothermostat.git
cd iothermostat/configuration_files
chmod +x *.sh
./deployhome.sh
cd ..
chmod +x deployIOThermostat.sh
./deployIOThermostat.sh
cd /home/iothermostat
sudo ./setMQTTpasswd.sh
</pre>

# INSTALLATION INSTRUCTIONS

You can download a pre-configured image or you can do everything yourself, see below. The pre-configured image is built  according to the complete manual installation instructions. Disk image is built for a 8GB SD card.

## Using the pre-configured Arch image:

Get archarmv6-iothermostat-18-11-14.img.zip from this link:

https://drive.google.com/open?id=1iExmBiI6qe_kAGd4YWvHeuNpWI3UtBVP

MD5:

https://drive.google.com/open?id=10x5rpndLZjyVElBwawdyQ4kZWRSHnHNU

The image includes:

    Arch Linux ARM v6
    IOThermostat https://github.com/jbaans/iothermostat
    Python
    Lighttpd
    Mosquitto
    Blackbox
    Midori
    Script for Wifi hotspot when no Wifi network available or initial setup

Changes:

    Fixed Fallback Wifi
    Added updating features
    Fixed Python pytz installation
    Fixed Scheduler Button
    Fixed setMQTTpasswd script
    Fixed certbot service
    Fixed wifi driver blacklist
    Fixed datalog location
    Fixed screen calibration
    Fixed Lighttpd credentials path
    Fixed deployhome script

1. Download, verify MD5 sum, unzip and write image to microsd card
2. Insert the card and power up. Display should show start log and finish into the IOThermostat GUI.
3. Connect your PC to hotspot IOTHERMOSTAT with password iothermostat0.
4. ssh to 10.42.0.1 with user iothermostat, password iothermostat2018.
5. Configure your wifi network (drops connection):

<pre> sudo ./connectWifi.sh YOURSSID </pre>

6. Connect your PC to YOURSSID, find the ip of iothermostat (see display-advanced/router/network) and ssh to x.x.x.x on port 22 with user iothermostat, password iothermostat2018.

7. Finally follow the instructions on:

https://github.com/jbaans/iothermostat/wiki/IOThermostat-installation


## Completely manually:

Note: This is a rather lengthy process.

1. Follow these instruction to set up the OS:

https://github.com/jbaans/iothermostat/wiki/Install-Arch-Linux-ARM-with-Wifi-on-Raspberry-Pi-Zero,B

2. Follow these instruction to set up the packages IOThermostat depends on:

https://github.com/jbaans/iothermostat/wiki/IOThermostat-dependencies-installation

3. Follow these instruction to set up IOThermostat:

https://github.com/jbaans/iothermostat/wiki/IOThermostat-installation


