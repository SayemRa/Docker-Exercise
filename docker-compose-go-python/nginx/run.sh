#!/bin/sh

envsubst < nginx.conf > /etc/nginx/conf.d/default.conf

htpasswd -c -b /etc/nginx/.htpasswd sayem rahman

nginx -g "daemon off;"