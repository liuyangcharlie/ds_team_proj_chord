from address import Address
from node import Node
from env import *

# class to call any remote node other than local one, always called by the local one
class Remote(object):
  """docstring for Remote"""
  def __init__(self, address):
    nodes = [None for x in range(NUM_SLOTS)]
    
    # create an initial nodes and add it to the Chord ring
    for x in range(len(address)):
      nodes.append(Node(Address(address[x]), self, None))

    self._nodes = nodes

  def getNodes(self):
    return self._nodes

  def printNodes(self):
    for x in range(len(self._nodes)):
      print(self._nodes[x])
    