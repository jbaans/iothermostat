chown root:root -R etc
find etc -type f -exec chmod 644 {} +
find etc -type d -exec chmod 755 {} +
cp -R --backup etc/* /etc
