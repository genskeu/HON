#!/usr/bin/env sh
#start gunicorn
echo "starting nginx"
if [ ! -d "/var/log/nginx/" ]
then
mkdir /var/log/nginx/
fi
nginx -g 'pid /run/nginx/nginx.pid;daemon off;' -c /etc/nginx/nginx.conf