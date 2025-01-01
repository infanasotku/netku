#!/bin/bash

# Waits for resolving assistant dns
while ! nslookup assistant; do
    sleep 5
done

# Runs nginx
nginx -g 'daemon off;'
