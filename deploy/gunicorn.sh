#!/bin/bash

cd /app/code/

gunicorn -c /gunicorn.conf api.wsgi -w 4 -b 0.0.0.0:8001 --chdir=/app/code
