## IOThermostat - Independent Open-source Thermostat

Built for the HestiaPi Touch with Raspberry Pi OS Lite, see: https://hestiapi.com/

Intended users: developers

Highlights:

* Disk image and instructions for Raspberry Pi Zero, Zero W or 1 A/B + Waveshare LCD

* Complete manual installation instructions available

* For use on a non Raspberry Pi compatible device, simply use your own GPIO driver

* Speed and security

## How to use:

The main screen shows current temperature, humidity and pressure. A flame icon is shown when the heater is on. The number above the + and - buttons is the set temperature for the selected mode. The set temperature is adjusted by the + and - buttons.

Possible modes are: 
- Auto (runs the scheduled program)
- On (keeps the room at the set temperature)
- Off (keeps heater off)
- Boost (keeps room at set temperature for one hour)
- Sleep (keeps the heater off for 24 hours)

The information screen shows information about the system.

The GUI is also available through the web interface, which uses username/password authentication. In the web interface, heater scheduling for Auto mode can be programmed. Click [i] button and then the configuration button.

The system security can be hardened according to the wiki. Full encryption of web traffic is then set, the network configuration is more strict and firewalling and blocking unwanted access is enabled.


# UPGRADING INSTRUCTIONS

SSH into the system, run the following commands:

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
Note: If you have the RTL8188eu Wifi chip, the command <pre>sudo install-wifi</pre> has to be run after every kernel update to load the right driver! (We should probably find am automatic solution for that).

# INSTALLATION INSTRUCTIONS

You can download a pre-configured image or you can do everything yourself, see below. The pre-configured image is built  according to the complete manual installation instructions.

## Recipe for installing Raspberry Pi OS Lite and IOThermostat:

https://github.com/jbaans/iothermostat/wiki/Install-IOThermostat-on-Raspberry-Pi-OS-Lite


## Recipe for installing Arch Linux ARM and IOThermostat:

https://github.com/jbaans/iothermostat/wiki/Install-IOThermostat-on-Arch-Linux-ARM

## Installing using a prebuilt image:

file: [Raspberry Pi OS Lite + IOThermostat 211110 image](https://drive.google.com/file/d/1WP6vVLdWi4tQ19mdr5PPpEfxfckhLEsv) (1.2 GB)

file: [SHA256 sum](https://drive.google.com/file/d/1EQ4Z4KUDI7oIOrqZHKeobqhc7s50WVQt/view?usp=sharing) (0.1 kB)

1. Download both files

2. Verify SHA256 sum <pre>sha256sum -c rpioslite-iothermostat-211216.img.gz.sha256sum</pre>

3. Write image to a microSD card >= 4 GB with Raspberry Pi Imager or <pre>sudo gunzip -c rpioslite-iothermostat-211216.img.gz | sudo dd iflag=fullblock oflag=direct conv=fsync status=progress bs=4M of=/dev/sdX</pre> where sdX is your microSD card.

4. Make new file `wpa_supplicant.conf` in the boot partition, it should contain:

<pre>
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
country=GB
update_config=1
network={
ssid="YOUR SSD"
psk="your wifi password"
key_mgmt=WPA-PSK
}
</pre>

Adjust the country code if needed.

3. Insert the card into the RPi and power up. Display should show start log and finish into a display calibration screen. Go through the calibration (or just wait). After that, it will start the IOThermostat GUI.

4. Find the ip of the IOThermostat (see GUI->[i] button, or check your router or use `nmap -sP` and `arp` commands) and ssh into it on port 22 with user iothermostat, password iothermostat2021.

5. Finally follow the instructions on:

https://github.com/jbaans/iothermostat/wiki/IOThermostat-configuration

Note: this image is based on Raspbery Pi OS Lite. It is built according to the recipe https://github.com/jbaans/iothermostat/wiki/Install-IOThermostat-on-Raspberry-Pi-OS-Lite . It runs an X server with Matchbox, loads the GUI in luakit, runs a Mosquitto mqtt server and a Lighttpd webserver. The IOThermostat backend runs in Python3.

