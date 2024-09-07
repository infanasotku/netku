{ echo & \
 envsubst '${DOMAIN},${PORT}' \
 < /etc/nginx/conf.templates/default.conf; } \
 >> /etc/nginx/conf.d/infanasotku.conf