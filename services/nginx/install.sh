touch temp
envsubst '${DOMAIN},${API_GATEWAY_ADDR},${XRAY_FALLBACK_PORT},${AUTH_ADDR}' \
 < /etc/nginx/conf.d/nginx.conf \
 > temp
cat temp > /etc/nginx/conf.d/nginx.conf
rm temp
