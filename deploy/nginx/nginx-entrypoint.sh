#!/bin/bash

/bin/bash -c "envsubst '\$NGINX_HOST,\$SCHEME' < /etc/nginx/conf.d/mysite.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"
