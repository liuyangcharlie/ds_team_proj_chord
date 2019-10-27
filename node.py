#!/bin/python
import sys
import random
import math
import threading

from env import *
from address import inrange
from finger_entry import FingerEntry

# class representing a local peer
class Node(object):
  def __init__(self, local_address, remote, remote_address = None):
    self._address = local_address
    # print("self id = ", self.id())
    _id = self._address.__hash__() % NUM_SLOTS
    while remote.getRemoteNodeByID(_id) is not None:
      _id = (_id + 1) % NUM_SLOTS
    self._id = _id

    # communication with other node via _remote
    self._remote = remote
    # initialize successor
    self._successor = None
    # list of successors is to prevent lookup failure
    self._successors = []
    # initialize predecessor
    self._predecessor = None
    # finger table
    self._finger = None
    self._shutdown = False

    self._remote.addToNetwork(self._id, self)

    # join the DHT
    self.join(remote_address)

    self.check_predecessor()

  def address(self):
    return self._address.__str__()

  # is this id within our range? i.e. is key in local node?
  def is_ours(self, id):
    # assert id >= 0 and id < SIZE
    # return inrange(id, self._predecessor.id(1), self.id(1))
    pass

  # node leave
  def shutdown(self):
    self._shutdown = True

  # logging function
  def log(self, info):
      f = open("/tmp/chord.log", "a+")
      f.write(str(self.id()) + " : " +  info + "\n")
      f.close()
      print(str(self.id()) + " : " +  info)

  # return true if node does not leave, i.e. still in the Chord ring
  def ping(self):
    if self._shutdown:
      return False
    return True

  # find the exact successor by comparing the hash(n), can be regarded as a lookup
  # 1. initialize the predecessor and the finger table
  # 2. notify other nodes to update their predecessors and finger tables
  # 3. the new node takes over its responsible keys from its successor.
  def join(self, remote_address = None):
    # initialize finger table
    self._finger = [None for x in range(M_BIT)]

    # initialize predecessor
    # self._predecessor = None

    if remote_address:
      # 1) add to a node `n`, n.find_successor(`to_be_added`)
      remote_node = self._remote.getRemoteNode(remote_address)
      successor = remote_node.find_successor(self.id())
      # 2) point `to_be_added`’s `successor` to the node found
      self._successor = successor
      # 3) copy keys less than `ID(to_be_added)` from the `successor`
      self._predecessor = self.find_predecessor(self.id())
    #   self._predecessor = self._successor._predecessor
      self._predecessor._successor = self
      # update its successor's predecessor
      self._successor._predecessor = self

    else:
      # current node is the first node on the Chord ring
      self._successor = self
    #   self._finger[0] = FingerEntry(self.id(), self)
      self._predecessor = self

    # add other entries in finger table
    self.init_finger(remote_address)
    self.update_finger()

    # 4) call `to_be_added`.stabilize() to update the nodes between `to_be_added` and its predecessor
    # self.stabilize()

    self.log("joined")

  # first node on circle that succeeds (n + 2^k−1) mod 2m, 1 <= k <= m
  # i-th entry means the 2^i far-away node from the current node
  def init_finger(self, remote_address = None):
    if remote_address:
      # get the arbitrary node in which the target node want to join
      remote_node = self._remote.getRemoteNode(remote_address)

      # get attribute `start` for the first entry in this finger table
      start = (self.id() + (2 ** 0)) % NUM_SLOTS

      # assign the first entry, find the successor(k)
      successor_k = remote_node.find_successor(start)
      self._finger[0] = FingerEntry(start, successor_k)

      # successor
      successor = self.successor()
      if successor is None:
        successor = remote_node.find_successor(self.id())
        self._successor = successor

      self._predecessor = self._successor._predecessor
      # update its successor's predecessor
      self._successor._predecessor = self

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

    for x in range(0, M_BIT):
      if self._finger[x] is not None:
        print('finger table of ', self.id(), 'start: ', self._finger[x].start, 'node', self._finger[x].node.id())

  def id(self, offset = 0):
    # return (self._address.__hash__() + offset) % SIZE

    return self._id

  def successor(self):
    return self._successor

  def predecessor(self):
    return self._predecessor

  def find_successor(self, id):
    self.log("find_successor of {}".format(id))
    # if self.predecessor() and 
    return self.find_predecessor(id).successor()

  def find_predecessor(self, id):
    lg = "find_predecessor of: {}".format(id)
    self.log(lg)
    node = self
    # when the ring only has one node, node.id is the same as node.successor.id,
    # if we are alone in the ring, we are the pred(id)
    if node.id() == node.successor().id():
      return node
    while not inrange(id, node.id(), node.successor().id()):
      node = node._closest_preceding_node(id)
    return node

  def _closest_preceding_node(self, id):
    # from m down to 1
    for x in reversed(range(len(self._finger))):
      entry = self._finger[x]
      if entry.node != None and inrange(entry.node.id(), self.id(), id):
        return entry.node

    return self

  def update_finger(self):
    for x in range(M_BIT):
      new_finger = self._remote.notify(self._finger[x].start)
      if new_finger is None:
        continue
      if x is 0:
        self._successor = new_finger

      self._finger[x].node = new_finger

    for x in range(len(self._finger)):
      if self._finger[x] is not None:
        print('finger table of ', self.id(), 'start: ', self._finger[x].start, 'node', self._finger[x].node.id())

    threading.Timer(10, self.update_finger).start()

  # called periodically.
  # clear the node’s predecessor pointer if n.predecessor is alive, or has failed
  def check_predecessor(self):
    lg = 'check_predecessor, predecessor of {}: , isAlive: {}'.format(self.predecessor().id(), self.predecessor().ping())
    self.log(lg)
    if not self.predecessor().ping():
      self._predecessor = None
    threading.Timer(10, self.check_predecessor).start()

  # this is called periodically(timer/deamon)
  # refresh finger table entries
  def _fix_fingers(self):
    # randomly pick an entry in finger table
    # call find_successor on its start_id
    pass

    # first fingers in decreasing distance, then successors in
    # increasing distance.
    self.log("_fix_fingers")
    # for remote in reversed(self._successors + self._finger):
    #   if remote != None and inrange(remote.id(), self.id(1), id) and remote.ping():
    #     return remote
    # return self
    threading.Timer(10, self.check_predecessor).start()
