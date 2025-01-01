touch temp
envsubst '${DOMAIN},${ASSISTANT_PORT},${XRAY_FALLBACK_PORT}' \
 < /etc/nginx/conf.d/nginx.conf \
 > temp
cat temp > /etc/nginx/conf.d/nginx.conf
rm temp
