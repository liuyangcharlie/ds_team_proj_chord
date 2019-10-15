#!/bin/python
import sys
import random

# class representing a local peer
class Node(object):
  def __init__(self, local_address, remote_address = None):
    self._address = local_address
    print("self id = %s", self.id())
    self._shutdown = False
    # list of successors
    self.successors_ = []
    # join the DHT
    self.join(remote_address)
    # we don't have deamons until we start
    # self.daemons_ = {}
    # initially no commands
    # self.command_ = []


  # is this id within our range? i.e. is key in local node?
  def is_ours(self, id):
    # assert id >= 0 and id < SIZE
    # return inrange(id, self.predecessor_.id(1), self.id(1))
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
    # set successor
    # successor =

    # stabilization
    # self.stabilize()

    self.log("joined")

  # called periodically.
  def stabilize(self):
    self.log("stabilize")
    suc = self.successor()
    # We may have found that x is our new successor iff
    # - x = pred(suc(n))
    # - x exists
    # - x is in range (n, suc(n))
    # - [n+1, suc(n)) is non-empty
    # fix finger_[0] if successor failed

  # called periodically.
  # notify during stabilization
  def notify(self, remote):
    # tell the successor about the node itself
    # Someone thinks they are our predecessor, they are iff
    # - we don't have a predecessor
    # OR
    # - the new node r is in the range (pred(n), n)
    # OR
    # - our previous predecessor is dead
    self.log("notify")

  # called periodically.
  # this is how new nodes initial- ize their finger table,
  # and how existing nodes incorporate new nodes into their finger tables
  def fix_fingers(self):
    # Randomly select an entry in finger_ table and update its value
    self.log("fix_fingers")
    # Keep calling us
    return True

  def update_successors(self):
    self.log("update successor")
    return True

  def get_successors(self):
    self.log("get_successors")
    return map(lambda node: (node._address.ip, node._address.port), self.successors_[:N_SUCCESSORS-1])

  def id(self, offset = 0):
    # return (self._address.__hash__() + offset) % SIZE
    return self._address.__hash__()

  def successor(self):
    # We make sure to return an existing successor, there `might`
    # be redundance between finger_[0] and successors_[0], but
    # it doesn't harm
    print("No successor available, aborting")
    self._shutdown = True
    sys.exit(-1)

  def predecessor(self):
    return self.predecessor_

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
    # for remote in reversed(self.successors_ + self.finger_):
    #   if remote != None and inrange(remote.id(), self.id(1), id) and remote.ping():
    #     return remote
    # return self


  # def register_command(self, cmd, callback):
  #   self.command_.append((cmd, callback))

  # def unregister_command(self, cmd):
  #   self.command_ = filter(lambda t: True if t[0] != cmd else False, self.command_)

# if __name__ == "__main__":
#   import sys
#   if len(sys.argv) == 2:
#     local = Node(Address("127.0.0.1", sys.argv[1]))
#   else:
#     local = Node(Address("127.0.0.1", sys.argv[1]), Address("127.0.0.1", sys.argv[2]))
#   local.start()
