#!/bin/bash

echo "<?php echo \"$(ip route | grep -m1 -oP 'src \K[^ ]+')\"; ?>" | tee /srv/http/iothermostat/getip.php
