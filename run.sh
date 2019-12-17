#!/bin/sh

###########
# This script is to run the whole application from the top-most level.
# It runs a few docker containers that are Node instances.
###########

# remove shared file if there is
rm ./node_addr

# loop to start docker container
port=8080
for i in {3..8}
do
    echo "starting node$i..."
    make start_docker name="node$i" port="`expr $port + $i`"
done

echo "nodes started"

# start server, server reads shared file
# python3 ./manage.py runserver