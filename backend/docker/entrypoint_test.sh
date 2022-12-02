#!/usr/bin/env sh
#start gunicorn
echo "init backend"
flask init-app

echo "starting gunicorn"
if [ ! -d "/var/log/gunicorn/" ]
then
    mkdir /var/log/gunicorn/
fi
gunicorn -b 0.0.0.0 -w 8 --threads 32 --reload --log-file /var/log/gunicorn/error.log --access-logfile /var/log/gunicorn/access.log wsgi:app
