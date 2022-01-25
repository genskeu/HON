#!/usr/bin/env sh
#start gunicorn
echo "starting gunicorn"
if [ ! -d "/var/log/gunicorn/" ]
then
    mkdir /var/log/gunicorn/
fi
gunicorn -w 8 --threads 32 -D --reload --log-file /var/log/gunicorn/error.log --access-logfile /var/log/gunicorn/access.log wsgi:app

#start nginx
echo "starting nginx"
if [ ! -d "/var/log/nginx/" ]
then
    mkdir /var/log/nginx/
fi
nginx -g 'pid /run/nginx/nginx.pid;daemon off;' -c /etc/nginx/nginx.conf