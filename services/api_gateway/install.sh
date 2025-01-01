touch temp
envsubst '${USERS_URL}' \
 < /kong/kong.yml \
 > temp
cat temp > /kong/kong.yml
rm temp
