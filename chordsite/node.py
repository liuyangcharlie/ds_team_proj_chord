#!/bin/python
import sys
import random
import math
import threading

from .env import *
from .address import inrange
from .finger_entry import FingerEntry

# class representing a local peer
class Node(object):
  def __init__(self, local_address, remote, remote_address = None):
    self._address = local_address
    _id = self._address.__hash__() % NUM_SLOTS
    while remote.getRemoteNodeByID(_id) is not None:
      _id = (_id + 1) % NUM_SLOTS
    self._id = _id

    # communication with other node via _remote
    self._remote = remote
    # initialize successor
    self._successor = None
    # list of successors is to prevent lookup failure
    self._successors = [None for x in range(M_BIT)]
    # initialize predecessor
    self._predecessor = None
    # finger table
    self._finger = None
    self._leave = False

    self._remote.addToNetwork(self._id, self)

    # join the DHT
    self.join(remote_address)

    # in case any node depatures
    self.check_predecessor()

  def address(self):
    return self._address.__str__()

  # node leave
  def leave(self):
    self._leave = True

  # logging function
  def log(self, info):
    #   f = open("/tmp/chord.log", "a+")
    #   f.write(str(self.id()) + " : " +  info + "\n")
    #   f.close()
      print(str(self.id()) + " : " +  info)

  # return true if node does not leave, i.e. still in the Chord ring
  def ping(self):
    if self._leave:
      return False
    return True

  # find the exact successor by comparing the hash(n), can be regarded as a lookup
  # 1. initialize the predecessor and the finger table
  # 2. notify other nodes to update their predecessors and finger tables
  # 3. the new node takes over its responsible keys from its successor.
  def join(self, remote_address = None):
    # initialize finger table
    self._finger = [None for x in range(M_BIT)]

    if remote_address:
      # 1) add to a node `n`, n.find_successor(`to_be_added`)
      start = (self.id() + (2 ** 0)) % NUM_SLOTS
      remote_node = self._remote.getRemoteNode(remote_address)
      successor = remote_node.find_successor(start)
      self._finger[0] = FingerEntry(start, successor)
      # 2) point `to_be_added`’s `successor` to the node found
      self._successor = successor
      # 3) copy keys less than `ID(to_be_added)` from the `successor`
      # self._predecessor = self.find_predecessor(self.id())
      self._predecessor = successor._predecessor
      # update its successor's predecessor
      self._successor._predecessor = self

    else:
      # current node is the first node on the Chord ring
      self._successor = self
    #   self._finger[0] = FingerEntry(self.id(), self)
      self._predecessor = self

    # add other entries in finger table
    self.init_finger(remote_address)
    self.fix_finger()
    self.update_successors()

    # 4) call `to_be_added`.stabilize() to update the nodes between `to_be_added` and its predecessor
    self.stabilize()

    self.log("joined")

  # first node on circle that succeeds (n + 2^k−1) mod 2m, 1 <= k <= m
  # i-th entry means the 2^i far-away node from the current node
  def init_finger(self, remote_address = None):
    if remote_address:
      # get the arbitrary node in which the target node want to join
      remote_node = self._remote.getRemoteNode(remote_address)

      # successor
      successor = self.successor()
      if successor is None:
        successor = remote_node.find_successor(self.id())
        self._successor = successor

      # initialize finger table
      for x in range(1, M_BIT):
        start_id = (self.id() + 2 ** x) % NUM_SLOTS
        self._finger[x] = FingerEntry(start_id, None)

      for x in range(0, M_BIT - 1):
        start_id = self._finger[x + 1].start
        if inrange(start_id, self.id(), self._finger[x].node.id()):
          self._finger[x + 1].node = self._finger[x].node
        else:
          # 
          successor = self.find_successor(start_id)
          self._finger[x + 1] = FingerEntry(start_id, successor)

    else:
    # n is the only node in the network
      for x in range(0, M_BIT):
        start_id = math.floor((self.id() + 2 ** x) % NUM_SLOTS)
        self._finger[x] = FingerEntry(start_id, self)

    self.print_finger('init_finger')

  def update_successors(self):
    if self._leave:
      return
    successor = self._successor
    for x in range(M_BIT):
      if successor is not None:
        self._successors[x] = successor
        successor = successor.successor()

    threading.Timer(2, self.update_successors).start()

  def id(self, offset = 0):
    return self._id

  def successor(self):
    successor = self._successor
    print('current successor', self._successor.ping())

    if not successor.ping():
      for x in range(1, len(self._successors)):
        if self._successors[x].ping():
          successor = self._successors[x]

    print('current successor', successor.id())

    return successor

  def predecessor(self):
    return self._predecessor

  def find_successor(self, id):
    self.log("find_successor of {}".format(id))
    # if self._predecessor exists, and _predecessor.id < id < self.id, the successor is current node
    if self._predecessor and inrange(id, self._predecessor.id(), self.id()):
      return self
    return self.find_predecessor(id).successor()

  def find_predecessor(self, id):
    lg = "find_predecessor of: {}".format(id)
    self.log(lg)
    node = self
    # when the ring only has one node, node.id is the same as node.successor.id,
    # if we are alone in the ring, we are the pred(id)
    if node.id() == node.successor().id():
      return node
    while not inrange(id, node.id(), node.successor().id() + 1):
      node = node._closest_preceding_node(id)
    return node

  def _closest_preceding_node(self, id):
    # from m down to 1
    for x in reversed(range(len(self._finger))):
      entry = self._finger[x]
      if entry != None and entry.node != None and inrange(entry.node.id(), self.id(), id):
        return entry.node

    return self

  def get_finger(self):
    finger = []
    for x in range(len(self._finger)):
      if self._finger[x] is not None:
        finger.append({'start': self._finger[x].start, 'node': self._finger[x].node.id()})
      else:
        finger.append({})

    return finger

  def update_finger(self, successor, index):
    if self._finger[index] is not None:
      if inrange(successor.id(), self.id() - 1, self._finger[index].node.id()):
        self._finger[index].node = successor
        self._predecessor.update_finger(successor, index)
        # print('finger table of ', self.id(), 'start: ', self._finger[x].start, 'node', self._finger[x].node.id())

    # threading.Timer(2, self.update_finger).start()

  def update_others(self):
    for x in range(1, M_BIT + 1):
      # find last node whose i-th finger might be current node
      start = (self.id() - 2 ** (x - 1)) % NUM_SLOTS
      pre = self.find_predecessor(start)
      # if only one node on the ring, no need to update others
      if pre.id() == self.id():
        continue
      pre.update_finger(self, x)

  # called periodically
  # clear the node’s predecessor pointer if n.predecessor is alive, or has failed
  def check_predecessor(self):
    if self._leave:
      return
    # log = 'check_predecessor, predecessor of {}: , isAlive: {}'.format(self.predecessor().id(), self.predecessor().ping())
    # self.log(log)
    pre = self.predecessor()
    if pre is not None and not pre.ping():
      self._predecessor = None
    threading.Timer(2, self.check_predecessor).start()

  # called periodically
  # check its own successor if any new node added between its previous successor
  def stabilize(self):
    if self._leave:
      return
    # prevent successor failure
    successor = self.successor()

    pre = successor._predecessor
    if pre is not None and inrange(pre.id(), self.id(), successor.id()):
      self.log('stabilize calls update_successor')
      self.update_successor(pre)
    successor.notify(self)
    self.print_finger('stabilize')

    threading.Timer(2, self.stabilize).start()

  # receive request that some node thinks it might be our predecessor
  def notify(self, pre):
    # check if pre is the new predecessor
    if (self._predecessor is None or inrange(pre.id(), self._predecessor.id(), self.id())):
      self._predecessor = pre

  # called periodically
  # randomly update finger table
  def fix_finger(self):
    if self._leave:
      return
    self.log('fix_finger')
    index = random.randrange(M_BIT - 1) + 1
    self._finger[index].node = self.find_successor(self._finger[index].start)
    # self.print_finger('fix_finger')

    threading.Timer(2, self.fix_finger).start()

  # update both first entry in finger table and _successor
  def update_successor(self, new_s):
    self._successor = new_s
    self._finger[0].node = new_s

  def print_finger(self, mod='default'):
    for x in range(0, M_BIT):
      if self._finger[x] is not None:
        self.log('{}: finger table of {}, start: {}, node: {}'.format(mod, self.id(), self._finger[x].start, self._finger[x].node.id()))

