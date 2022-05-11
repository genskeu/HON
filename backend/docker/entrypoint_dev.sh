#!/usr/bin/env sh
#start gunicorn
static_dir="app/static/dependencies/"

if [ ! -d "$static_dir" ]
then
    echo "download js dependencies"
    ./get_js_dep.sh
fi
echo "starting devlopment server"
flask run --host=0.0.0.0 --port=80