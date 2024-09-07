touch temp
envsubst '${DOMAIN},${PORT}' \
 < /etc/nginx/conf.templates/default.conf \
 > temp
echo >> temp
cat /etc/nginx/conf.d/infanasotku.conf >> temp
cat temp > /etc/nginx/conf.d/infanasotku.conf
rm temp