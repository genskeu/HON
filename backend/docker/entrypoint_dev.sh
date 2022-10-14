#!/usr/bin/env sh
#start gunicorn
echo "start flask-api development server"
# setup to develop and debug with vs code
python3 -m debugpy --listen 0.0.0.0:5678 -m wsgi --wait-for-client --multiprocess