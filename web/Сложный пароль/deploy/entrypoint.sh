#!/bin/bash
envsubst '${SERVER_NAME}' < /etc/nginx/conf.d/default.conf.template  > /etc/nginx/conf.d/default.conf
service nginx start
php-fpm