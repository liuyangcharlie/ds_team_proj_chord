#!/bin/python
import sys
import random
import math

from env import *
from address import inrange
from finger_entry import FingerEntry

# class representing a local peer
class Node(object):
  def __init__(self, local_address, remote, remote_address = None):
    self._address = local_address
    # print("self id = ", self.id())
    
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

    # join the DHT
    self.join(remote_address)

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
    # add other entries in finger table
    self.init_finger(remote_address)

    # initialize predecessor
    # self._predecessor = None

    if remote_address:
      # 1) add to a node `n`, n.find_successor(`to_be_added`)
      remote_node = self._remote.getRemoteNode(remote_address)
      successor = remote_node.find_successor(self.id())
      # 2) point `to_be_added`’s `successor` to the node found
      self._successor = successor
      # 3) copy keys less than `ID(to_be_added)` from the `successor`

    else:
      # current node is the first node on the Chord ring
      self._successor = self
    #   self._finger[0] = FingerEntry(self.id(), self)
      self._predecessor = self

    # 4) call `to_be_added`.stabilize() to update the nodes between `to_be_added` and its predecessor
    # self.stabilize()

    self.log("joined")

  # first node on circle that succeeds (n + 2^k−1) mod 2m, 1 <= k <= m
  # 第i项路由信息代表距离当前节点为2i的哈希空间数值所在的机器节点
  def init_finger(self, remote_address = None):
    if remote_address:
      # get the arbitrary node in which the target node want to join
      remote_node = self._remote.getRemoteNode(remote_address)

      # get attribute `start` for the first entry in this finger table
      start = self.id() + (2 ** 0)

      # assign the first entry, find the successor(k)
      successor_k = remote_node.find_successor(start)
      self._finger[0] = FingerEntry(start, successor_k)

      # successor
      successor = self.successor()
      if successor is None:
        successor = remote_node.find_successor(self.id())
        self._successor = successor

      self._predecessor = self._successor.predecessor
      self._successor._predecessor = self

      for x in range(1, M_BIT):
       keyID = (self.id() + 2 ** (x - 1)) % NUM_SLOTS
      self._finger[x] = FingerEntry(keyID, self)

    else:
    # n is the only node in the network
      for x in range(0, M_BIT):
        start_id = math.floor(self.id() + 2 ** (x - 1) % NUM_SLOTS)
        self._finger[x] = FingerEntry(start_id, self)

    for x in range(0, M_BIT):
      if self._finger[x] is not None:
        print('finger table of ', self.id() ,self._finger[x].node.id())
  # def update_successors(self):
  #   self.log("update successor")
  #   return True

  # def get_successors(self):
  #   self.log("get_successors")
  #   return map(lambda node: (node._address.ip, node._address.port), self._successors[:N_SUCCESSORS-1])

  def id(self, offset = 0):
    # return (self._address.__hash__() + offset) % SIZE
    return self._address.__hash__() % NUM_SLOTS
    # return self._address.__hash__()

  def successor(self):
    return self._successor

  def predecessor(self):
    return self._predecessor

  def find_successor(self, id):
    self.log("find_successor")
    # print('self.id(): ', self.id())
    # print('self._successor.id(): ', self._successor)
    return self.find_predecessor(id).successor()

  def find_predecessor(self, id):
    self.log("find_predecessor")
    node = self
    # If we are alone in the ring, we are the pred(id)
    while inrange(id, node.id(), node.successor().id()):
      node = node._closest_preceding_node(id)
    return node

  # called periodically.
  # clear the node’s predecessor pointer if n.predecessor is alive, or has failed
#   def check_predecessor(self):
#     if not self.predecessor().ping():
#       self._predecessor = nil

  def _closest_preceding_node(self, id):
    # from m down to 1
    for x in reversed(range(len(self._finger))):
      entry = self._finger[x]
      if inrange(entry.node.id(), self.id(), id):
        return entry.node

    return self

  # this is called periodically(timer/deamon)
  def _fix_fingers(self):
    pass

    # first fingers in decreasing distance, then successors in
    # increasing distance.
    self.log("closest_preceding_node")
    # for remote in reversed(self._successors + self._finger):
    #   if remote != None and inrange(remote.id(), self.id(1), id) and remote.ping():
    #     return remote
    # return self
