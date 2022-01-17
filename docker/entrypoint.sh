#!/usr/bin/env sh
#start gunicorn
echo "starting gunicorn"
mkdir /var/log/gunicorn/
gunicorn -w 8 --threads 32 -D --reload --log-file /var/log/gunicorn/error.log --access-logfile /var/log/gunicorn/access.log wsgi:app

#start nginx
echo "starting nginx"
mkdir /var/log/nginx/
nginx -g 'pid /run/nginx/nginx.pid;daemon off;' -c /etc/nginx/nginx.conf