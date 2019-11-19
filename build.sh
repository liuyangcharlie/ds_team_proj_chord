#!/bin/sh

# install python package detecting dependencies
pip3 install pipreqs --user

# detect dependencies
pipreqs --force .

# install dependencies
pip3 install --user -r requirements.txt
