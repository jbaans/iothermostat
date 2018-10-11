#!/bin/bash
if [ $EUID -ne 0 ]; then
    echo "Please run script as root. Aborting."
    exit 2
fi

SSID=$1
PASSPHRASE=$2

if [ "$SSID" == "" ]; then
    echo "You must pass an SSID. Aborting."
    exit 2
fi 
if [ "$PASSPHRASE" == "" ]; then
    echo "You must pass an PASSPHRASE. Aborting."
    exit 2
fi

### make sure that the script is called with `nohup nice ...`
if [ "$3" != "calling_myself" ]
then
    # this script has *not* been called recursively by itself
    nohup_out="$0".log
    echo "Forking to background..."
    nohup nice "$0" "$SSID" "$PASSPHRASE" "calling_myself" >> $nohup_out &
    sleep 1
    exit
else
    # this script has been called recursively by itself
    #shift # remove the termination condition flag in $1

    nmcli con down id IOTHERMOSTAT
    sleep 5
    nmcli device wifi connect "$SSID" password "$PASSPHRASE"
    #nmcli device wifi connect "$SSID" password "$PASSPHRASE" ip4 145.101.42.22
    sleep 10
    nmcli con mod "$SSID" connection.autoconnect yes
    nmcli con mod "$SSID" connection.autoconnect-priority 10
    nmcli -f NAME,AUTOCONNECT,AUTOCONNECT-PRIORITY,DEVICE c s
fi
