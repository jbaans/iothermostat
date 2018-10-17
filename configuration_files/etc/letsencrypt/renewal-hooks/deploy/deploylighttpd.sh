#!/bin/bash
# certbot output:
# Your certificate and chain have been saved at:
# /etc/letsencrypt/live/YOURDOMAIN/fullchain.pem
# Your key file has been saved at:
# /etc/letsencrypt/live/YOURDOMAIN/privkey.pem
domain="YOURDOMAIN"

sslpemfile="/etc/letsencrypt/live/${domain}/sslpemfile.pem"
certfile="/etc/letsencrypt/live/${domain}/cert.pem"
keyfile="/etc/letsencrypt/live/${domain}/privkey.pem"

/bin/cat "${certfile}" "${keyfile}" > "${sslpemfile}"

/usr/bin/systemctl reload lighttpd.service
