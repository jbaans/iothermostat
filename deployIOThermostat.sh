#!/bin/bash
mkdir -p /srv/http/iothermostat
sudo cp -R iothermostat-http/* /srv/http/iothermostat
cp -R iothermostat-python ~
