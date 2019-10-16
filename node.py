#!/bin/python
import sys
import random

from env import *

# class representing a local peer
class Node(object):
  def __init__(self, local_address, remote, remote_address = None):
    self._address = local_address
    print("self id = %s", self.id())
    self._remote = remote
    self._shutdown = False
    # list of successors
    self._successors = []
    # join the DHT
    self.join(remote_address)
    # initially no commands
    # self._command = []

  # is this id within our range? i.e. is key in local node?
  def is_ours(self, id):
    # assert id >= 0 and id < SIZE
    # return inrange(id, self._predecessor.id(1), self.id(1))
    pass

  def shutdown(self):
    self._shutdown = True

  # logging function
  def log(self, info):
      f = open("/tmp/chord.log", "a+")
      f.write(str(self.id()) + " : " +  info + "\n")
      f.close()
      print(str(self.id()) + " : " +  info)

  def start(self):
    # start
    self.log("started")

  # return true if node does not leave, i.e. still in the Chord ring
  def ping(self):
    if self._shutdown:
      return False
    return True

  # find the exact successor by comparing the hash(n), can be regarded as a lookup
  def join(self, remote_address = None):
    # initialize finger table
    self._finger = {}

    # initialize predecessor
    self._predecessor = None

    if remote_address:
      pass
    else:
      # current node is the first node on the Chord ring
      self._finger[0] = self

    # set successor
    # successor =

    # stabilization
    # self.stabilize()

    self.log("joined")


  def update_successors(self):
    self.log("update successor")
    return True

  def get_successors(self):
    self.log("get_successors")
    return map(lambda node: (node._address.ip, node._address.port), self._successors[:N_SUCCESSORS-1])

  def id(self, offset = 0):
    # return (self._address.__hash__() + offset) % SIZE
    return self._address.__hash__()

  def successor(self):
    # We make sure to return an existing successor, there `might`
    # be redundance between _finger[0] and _successors[0], but
    # it doesn't harm
    # print("No successor available, aborting")
    pass

  def predecessor(self):
    return self._predecessor

  def find_successor(self, id):
    # The successor of a key can be us iff
    # - we have a pred(n)
    # - id is in (pred(n), n]
    self.log("find_successor")

    node = self.find_predecessor(id)
    return node.successor()

  def find_predecessor(self, id):
    self.log("find_predecessor")
    node = self
    # If we are alone in the ring, we are the pred(id)
    return node

  # called periodically.
  # clear the node’s predecessor pointer if n.predecessor has failed
  def check_predecessor():
    # check if the predecessor has left
    # if !self.predecessor.ping():
      # self.predecessor = nil
    pass

  def closest_preceding_node(self, id):
    # first fingers in decreasing distance, then successors in
    # increasing distance.
    self.log("closest_preceding_node")
    # for remote in reversed(self._successors + self._finger):
    #   if remote != None and inrange(remote.id(), self.id(1), id) and remote.ping():
    #     return remote
    # return self
