#!/bin/python
from node import Node
from remote import Remote
from address import Address
from env import *

m = M_BIT

address = ["127.0.0.1", "127.0.0.2", "127.0.0.3", "127.0.0.4"]

ring = Remote(address)

ring.printNodes()

# def printEverySuccessor():
#   while x in range(len(nodes)):
#     print(nodes[x].successor())

# printEverySuccessor()