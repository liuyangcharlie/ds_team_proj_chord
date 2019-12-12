#!/bin/python

import socket

from node import Node
from remote import RemoteConnection
from address import Address
from env import *

m = M_BIT

# a list of docker containers' ip address
address = ["172.17.0.2", "172.17.0.3"]

local_ip = socket.gethostbyname(socket.gethostname())

# ring = RemoteConnection(address)
node = Node(Address(address[1]), Address(address[0]))

# ring.addNode("127.0.0.5", "127.0.0.1")

# ring.printNodes()

# n = None
# for x in range(len(ring._nodes)):
#   if ring._nodes[x] is not None:
#     n = ring._nodes[x]
#     break

# print('ring._nodes[0].id()', n.id())

# ring.nodeDepature(n.id())

# def printEverySuccessor():
#   while x in range(len(nodes)):
#     print(nodes[x].successor())

# printEverySuccessor()