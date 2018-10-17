#!/bin/bash

declare -a proclist=("lighttpd" "mosquitto" "sshd" "nftables" "iothermostat" "fail2ban" "netctl@wlan0" "getty@tty1" "fake-hwclock" "certbot")
activeprocs="$(systemctl list-units)"

for proc in "${proclist[@]}"
do
    result="Not active"

    resproc=$(grep "$proc" <<< $activeprocs | tr -s ' ' | cut -d ' ' -f1,2,3,4)
    if [[ $resproc != 0 ]]; then
        result=$resproc
    fi

    echo "$proc - $result" 
done
