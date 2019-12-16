#!/bin/python
import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path + '/chordsite')

from node import Node
from address import Address
from env import *
from util import local_ip

m = M_BIT

# address = ["127.0.0.1", "127.0.0.2", "127.0.0.3", "127.0.0.4"]
# address = ["127.0.0.1", "127.0.0.2", "127.0.0.3"]
# a list of docker containers' ip address
address = ["172.17.0.2", "172.17.0.3", "172.17.0.4"]

n = Node(local_ip(), address[0])