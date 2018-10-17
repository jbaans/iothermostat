#!/bin/bash
if [ $EUID -ne 0 ]; then
    echo "Please run script as root. Aborting."
    exit 2
fi

IFS= read -s  -p 'GUI Password:' passwd
echo ""
user='iothermostat'
realm='Login required'
hash=`echo -n "$user:$realm:$passwd" | md5sum | cut -b -32`
echo "$user:$realm:$hash" > /etc/lighttpd/credentials
chown http:http /etc/lighttpd/credentials
chmod 600 /etc/lighttpd/credentials
