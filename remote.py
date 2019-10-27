from address import Address
from node import Node
from env import *

# class to call any remote node other than local one, always called by the local one
class RemoteConnection(object):
  """docstring for Remote"""
  def __init__(self, address):
    # ip addresses
    self._address = address
    self._base_address = address[0]

    # all slots, a ring
    nodes = [None for x in range(NUM_SLOTS)]
    self._nodes = nodes

    # create an initial nodes and add it to the Chord ring
    addr = Address(self._base_address)
    index = addr.__hash__()

    # avoid collision of hashing
    while self._nodes[index] is not None:
      index = (index + 1) % NUM_SLOTS
    self._nodes[index] = Node(addr, self)

    for x in range(1, len(address)):
      self.addNode(address[x], self._base_address)

  def addNode(self, address, remote_address = None):
    Node(Address(address), self, Address(remote_address))
    
    # print('--------')

  def addToNetwork(self, index, node):
    # print('target_address: ', target_address.__hash__())

    # avoid collision of hashing
    while self._nodes[index] is not None:
      index = (index + 1) % NUM_SLOTS
    self._nodes[index] = node

  def notify(self, index):
    return self._nodes[index]

  # get remote node on the Chord ring by its address
  def getRemoteNode(self, address):
    node = None

    index = address.__hash__()
    node = self._nodes[index]

    return node

  def getRemoteNodeByID(self, id):
    return self._nodes[id]

  # return all slots on the ring
  def getNodes(self):
    return self._nodes

  # print nodes
  def printNodes(self):
    for x in range(len(self._nodes)):
      if self._nodes[x]:
        print(x, self._nodes[x].address().__str__())
      else:
        print(x, self._nodes[x])
    