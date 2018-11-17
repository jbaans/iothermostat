#!/bin/bash
if [ $EUID -ne 0 ]; then
    echo "Please run script as root. Aborting."
    exit 2
fi

pypasswd=$(pwgen -1)$(pwgen -1)
jspasswd=$(pwgen -1)$(pwgen -1)
pwfile="/etc/mosquitto/credentials"

touch $pwfile
mosquitto_passwd -b $pwfile pyiothermostat $pypasswd 
mosquitto_passwd -b $pwfile jsiothermostat $jspasswd
chmod 700 $pwfile

cat <<EOF > /srv/http/iothermostat/store.php
<?php
\$credentials = array("user" => "jsiothermostat", "password" => "$jspasswd");
echo json_encode(\$credentials);
?>
EOF

echo "password = \"$pypasswd\"" >> /home/iothermostat/iothermostat-python/mqttconf.py

systemctl restart lighttpd mosquitto iothermostat getty@tty1
