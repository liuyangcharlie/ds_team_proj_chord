#!/bin/sh

###########
# This script is used to initialize the node after docker container starts.
###########

ip_addr=`hostname -i`
working_dir="/home/c/ds_team_proj_chord_dev"
echo $ip_addr >> "$working_dir/node_addr"

cd $working_dir
echo `pwd`
python3 ./manage.py runserver 0.0.0.0:8080