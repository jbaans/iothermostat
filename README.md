## IOThermostat - Independent Open-source Thermostat

!!! currently changing to Raspberry Pi OS Lite, instructions may be incomplete !!!

Built for the HestiaPi Touch with Raspberry Pi OS Lite system with high security in mind, see: https://hestiapi.com/

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
sudo apt update; sudo apt upgrade
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
Note: If you have the RTL8188eu Wifi chip, the command <pre>sudo install-wifi</pre> has to be run after every kernel update to load the right driver! We should probably find am automatic solution for that.

# INSTALLATION INSTRUCTIONS

You can download a pre-configured image or you can do everything yourself, see below. The pre-configured image is built  according to the complete manual installation instructions. Disk image is built for a 8GB SD card.

## Recipe for installing Raspberry Pi OS Lite and IOThermostat:

https://github.com/jbaans/iothermostat/wiki/Install-IOThermostat-on-Raspberry-Pi-OS-Lite


## Recipe for installing Arch Linux ARM and IOThermostat:

https://github.com/jbaans/iothermostat/wiki/Install-IOThermostat-on-Arch-Linux-ARM

## Image with Raspberry Pi OS Lite and IOThermostat preinstalled:

>link tbd<

1. Download, verify MD5 sum, unzip and write image to microsd card
2. Configure your network in /boot/network.conf
3. Insert the card into the RPi and power up. Display should show start log and finish into the IOThermostat GUI.
4. Find the ip of the IOThermostat (see GUI->[i] button, or check your router or use `nmap -sP` and `arp` commands) and ssh into it on port 22 with user iothermostat, password iothermostat2021.
5. Finally follow the instructions on:

https://github.com/jbaans/iothermostat/wiki/IOThermostat-configuration


