#!/bin/bash
if [ $EUID -ne 0 ]; then
    echo "Please run script as root. Aborting."
    exit 2
fi

# if after 120 seconds no connection is active, create new fallback hotspot

SSID=IOTHERMOSTAT
PASSPHRASE=iothermostat0

sleep 120

ACTIVE=$(nmcli -t connection show --active)
logger -s "Network Manager active connections: $ACTIVE" 

# if no active connections reported, create one
if [ -z "$ACTIVE" ]; then
  # delete existing config
  nmcli connection delete id "$SSID"

  # create, connect and configure new hotspot according to device capabilities
  nmcli device wifi hotspot con-name "$SSID" ssid "$SSID" password "$PASSPHRASE" 
  nmcli connection mod "$SSID" wifi.hidden no
  nmcli connection mod "$SSID" connection.autoconnect yes
  nmcli connection mod "$SSID" connection.autoconnect-priority -10
fi
