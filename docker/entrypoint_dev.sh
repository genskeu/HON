#!/usr/bin/env sh
#start gunicorn


if [ ! -d "/home/HON/app/static/dependencies/" ]
echo "download js dependencies"
then
    ./get_js_dep.sh
fi
echo "starting devlopment server"
flask run --host=0.0.0.0 --port=80