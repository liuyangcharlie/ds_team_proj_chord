from .address import Address
from .node import Node
from .env import NUM_SLOTS

# class to simulate RPC call, call any remote node other than local one
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
    if remote_address is None:
      remote_address = self._base_address
    Node(Address(address), self, Address(remote_address))
    # print('address: ', address)
    self.printNodes()
    return self.ringShape()

  def addToNetwork(self, index, node):
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

  def ringShape(self):
    s = []
    for x in range(len(self._nodes)):
      if self._nodes[x] is not None:
        s.append({'addr': self._nodes[x]._address.__str__(), 'finger': self._nodes[x].get_finger()})
      else:
        s.append(None)

    return s

  def nodeDepature(self, id):
    self._nodes[id].leave()
    self._nodes[id] = None
    return self.ringShape()

  def lookup(self, key, id):
    node = self._nodes[id].find_successor(key)
    return node.id()

  # print nodes for testing
  def printNodes(self):
    for x in range(len(self._nodes)):
      if self._nodes[x]:
        print(x, self._nodes[x].address().__str__())
      else:
        print(x, self._nodes[x])
    