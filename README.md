## IOThermostat - Independent Open-source Thermostat


Built for the HestiaPi Touch system with high security in mind, see: https://hestiapi.com/

## Features:

Display current temperature, humidity and pressure.

Set modes: Auto/On/Off/Boost (1h)/Sleep (24h)

Set temperature for each mode.

Remote web interface with authentication.

Scheduling for Auto mode: browse to iothermostat/scheduler.php.

Full SSL encryption.

Many security features.

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

Note: This is a rather lengthy process.

1. Follow these instruction to set up the OS:

https://github.com/jbaans/iothermostat/wiki/Install-Arch-Linux-ARM-with-Wifi-on-Raspberry-Pi-Zero,B

2. Install these packages (Note: I need to update this list):
<pre>sudo pacman -Syu python python-pip lighttpd fcgi php php-cgi midori xorg-server xorg-xinit xf86-video-fbdev xterm ttf-dejavu xf86-video-fbturbo xorg-xauth blackbox ddclient php-sqlite libwebsockets xinput_calibrator nftables fail2ban</pre>

3. Reconfigure libraries (for libwebsockets):
<pre>sudo ldconfig</pre>

4. Install these packages with python/pip:
<pre>python -m pip install paho-mqtt apscheduler sqlalchemy</pre>

5. Copy configuration files in:

download/copy iothermostat/* to /home/iothermostat/iothermostat/
 
download/copy webinterface/* to /srv/http/iothermostat/
 
download/copy configuration_files to /home/iothermostat/

<pre> cd /home/iothermostat/configuration_files </pre>

Copy (with backup enabled) config files and scripts to their locations:

<pre>
chmod +x *.sh
sudo ./deployetc.sh
./deployhome.sh 
sudo systemctl daemon-reload
</pre>

<pre> sudo cp LCD-show/waveshare35a-overlay.dtb /boot </pre>


6. Install mosquitto MQTT with websockets:
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

build and install:
<pre>make binary
sudo make install
sudo useradd -r -s /bin/false mosquitto
sudo mkdir /var/lib/mosquitto
chown mosquitto:mosquitto /var/lib/mosquitto</pre>

6. Setup BM280 T/H/P sensor:

<pre>
cd /home/iothermostat/builds 
git clone https://github.com/cmur2/python-bme280.git
cd python-bme280/
sudo python setup.py install
</pre>

7. Setup Waveshare display:

<pre>
su
cp --backup configuration_files/LCD-show/usr/share/X11/xorg.conf.d/99-fbturbo.conf /usr/share/X11/xorg.conf.d/
chmod 644 /usr/share/X11/xorg.conf.d/99-fbturbo.conf
</pre>

8. Block caching in midori:
<pre>
mkdir -p /home/iothermostat/.cache/midori
chmod -R -w /home/iothermostat/.cache/midori
</pre>

9. Start X remotely for calibration:
<pre>
cd /home/iothermostat
xinit -- :1
</pre>

10. Copy-paste the output of the previous step to /etc/X11/xorg.conf.d/99-calibration.conf and to fix swapped x and y, add:
<pre>
Option "TransformationMatrix"  "0 -1 1 1 0 0 0 0 1”
</pre>

example Section:
<pre>
Section "InputClass"
        Identifier      "calibration"
        MatchProduct    "ADS7846 Touchscreen"
        Option  "MinX"  "21856"
        Option  "MaxX"  "22311"
        Option  "MinY"  "49919"
        Option  "MaxY"  "48690"
        Option  "SwapXY"        "1" # unless it was already set to 1
        Option  "InvertX"       "0"  # unless it was already set
        Option  "InvertY"       "0"  # unless it was already set
        Option "TransformationMatrix"  "0 -1 1 1 0 0 0 0 1"
EndSection
</pre>

11.  Comment out xinput_calibrator line in .xinitrc to disable it:
<pre>
#exec xinput_calibrator
</pre>

12. Start the services required for IOThermostat:
<pre>
sudo systemctl daemon-reload
sudo systemctl restart nftables.service lighttpd.service fstrim.timer mosquitto.service getty@tty1.service iothermostat.service
</pre>

13.  Browse to http://x.x.x.x/iothermostat/ and login with user: iothermostat and your GUI password.

14. If screen and web interface work, make permanent and test by rebooting:
<pre>
sudo systemctl enable nftables.service lighttpd.service fstrim.timer mosquitto.service getty@tty1.service iothermostat.service
sudo reboot now
</pre>

15. Finally follow the instructions on:

https://github.com/jbaans/iothermostat/wiki/IOThermostat-installation


