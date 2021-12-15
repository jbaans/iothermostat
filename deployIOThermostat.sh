#!/bin/bash
if [ $EUID -e 0 ]; then
    echo "Please run script as regular user, not as root. Aborting."
    exit 2
fi

sudo mkdir -p /srv/http/iothermostat
sudo cp -R iothermostat-http/* /srv/http/iothermostat
cp -R iothermostat-python ~
