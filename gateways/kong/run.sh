touch temp
envsubst '${USER_URL},${AUTH_URL}' \
 < /kong/kong.yml \
 > temp
cat temp > /kong/kong.yml
rm temp

kong restart --v
