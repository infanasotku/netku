touch temp
envsubst '${DOMAIN},${PORT},${XRAY_FALLBACK_PORT}' \
 < /etc/nginx/conf.d/nginx.conf \
 > temp
cat temp > /etc/nginx/conf.d/nginx.conf
rm temp