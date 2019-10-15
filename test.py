#!/bin/python
from node import Node
from address import Address

# m-bit hash, 2^3 = 8 slots
m = 3


# the rest slots are blank
gap = 3

# create an initial node and add it to the Chord ring
node = Node(Address("127.0.0.1"))

nodes = [node]
address = ["127.0.0.2", "127.0.0.3", "127.0.0.4"]

i = 0
for x in range(0, 2 ** m, gap):
  nodes.append(Node(Address(address[i])))
  i += 1

print(nodes[1])