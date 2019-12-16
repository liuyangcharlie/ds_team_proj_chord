#!/bin/sh

###########
# This script is to run the whole application from the top-most level.
# It runs a few docker containers that are Node instances.
###########

# remove shared file if there is
rm ./node_addr

# loop to start docker container
# a ip addr list
# docker run --ip=$(ip) --publish=$(port):8080 --name=$(name) -it -v ~/Documents/GWU/Code/distributed_system:/home/c/ds_team_proj_chord_dev vibrant_elbakyan/chord
make start_docker name="node4" port="8081"

# write ip to a shared file
# DONE in docker container

# start server, server reads shared file
# python3 ./manage.py runserver