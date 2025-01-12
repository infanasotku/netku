touch temp
envsubst '${DOMAIN},${KONG_ADDR},${XRAY_FALLBACK_PORT},${AUTH_ADDR}' \
 < /etc/nginx/conf.d/default.conf \
 > temp
cat temp > /etc/nginx/conf.d/default.conf
rm temp
