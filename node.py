# -*- coding: utf-8 -*-
#!/bin/python
import sys
import random
import math
import threading
import util

from env import *
from address import inrange, Address
from finger_entry import FingerEntry
from rpc_server_handler import Rpc
from serv.ttypes import RemoteNode

# TODO: get rid of legacy RemoteConnection
# class representing a local peer
class Node(object):
  def __init__(self, local_address, remote_address = None):
    self._address = local_address
    _id = self._address.__hash__() % NUM_SLOTS

    # while remote.getRemoteNodeByID(_id) is not None:
    #   _id = (_id + 1) % NUM_SLOTS

    self._id = _id

    # communication with other node via _remote
    # self._remote = remote

    # the RPC server of the node itself
    self.rpc_server = None

    # a hash map of thrift clients connected to remote nodes, key is a str of ip, value is the thrift client
    self.remote_clients = {}

    # initialize successor
    self._successor = None
    # list of successors as backup is to prevent lookup failure
    self._successors = [None for x in range(M_BIT)]
    # initialize predecessor
    self._predecessor = None
    # finger table
    self._finger = None
    self._leave = False

    # self._remote.addToNetwork(self._id, self)
    # start RPC server, RPC calls include ping(), find_successor_r(), notify_r(), etc.
    self.start_rpc_server()
    print('after start_rpc_server')

    # join the DHT(distribute hash table)
    self.join(remote_address)
    print('after join')

    # in case any node depatures
    self.check_predecessor()

  def ip(self):
    ip_addr, _ = self._address.__addr__()
    ip_addr = "invalid" if ip_addr is None else ip_addr
    print('rpc ip_addr: ', ip_addr)
    if ip_addr is not None:
        return ip_addr
    else:
        return ""

  def ip_r(self):
    ip_addr, _ = self._address.__addr__()
    ip_addr = "invalid" if ip_addr is None else ip_addr
    print('rpc ip_addr: ', ip_addr)
    if ip_addr is not None:
        return ip_addr
    else:
        return ""

  def port(self):
    _, port = self._address.__addr__()
    port = -1 if port is None else port
    return port

  def port_r(self):
    _, port = self._address.__addr__()
    port = -1 if port is None else port
    print('rpc port: ', port)
    return port

  # return RPC client connecting to the node specified by address
  def get_remote_node_by_ip(self, address):
    # check if already the corresponding client has been created
    ip_addr, port = address.__addr__()
    if ip_addr == util.local_ip():
      return self
    client_addr = '%s:%d' % (ip_addr, port)
    # print('-----------------------------')
    # print(ip, port)
    if client_addr not in self.remote_clients:
      self.remote_clients[client_addr] = util.create_rpc_client(ip_addr, port)

    print('self.remote_clients[client_addr].ping(): ', self.remote_clients[client_addr])

    return self.remote_clients[client_addr]

  def start_rpc_server(self):
    # Remote2
    self.rpc_server = Rpc(self)
    self.rpc_server.startServer()

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
    p = not self._leave
    print('ping: ', p)
    if p:
        return True
    else:
        return False

  def rpc_test(self, test_str):
    print('rpc_test: ', test_str)

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
    # remote_node = self._remote.getRemoteNode(remote_address)
    # TODO extract rpc methods into a independant class/module
    # TODO organize node logic, necessary remote calls
    # TODO write demo to try RPyC
      remote_node = self.get_remote_node_by_ip(remote_address)
      remote_node.rpc_test('rpc test rpc test rpc test')

    #   print('-----------')
      try:
        test_remote_node = self.get_remote_node_by_ip(remote_address)
        test_remote_node.ping()
      except:
        print('Could not connect')

      successor_rn = remote_node.find_successor_r(start)
      if util.isRemoteNodeType(successor_rn):
        successor = self.get_remote_node_by_ip(Address(successor_rn.ip_addr))
      else:
        successor = successor_rn
      self._finger[0] = FingerEntry(start, successor)
      # 2) point `to_be_added`’s `successor` to the node found
      if util.isRemoteNodeType(successor):
        successor = self.get_remote_node_by_ip(successor.ip_addr)
      self._successor = successor
      # 3) copy keys less than `ID(to_be_added)` from the `successor`
      predecessor_rn = successor.predecessor_r()
      print('predecessor_rn: ', predecessor_rn)
      self._predecessor = self.get_remote_node_by_ip(Address(predecessor_rn.ip_addr))
      # update its successor's predecessor
      rn = RemoteNode()
      rn.id = self.id()
      rn.ip_addr = self.ip()
      rn.port = self.port()

      print('set_predecessor, rn: ', rn)

      self._successor.set_predecessor(rn)

    else:
      # current node is the first node on the Chord ring
      self._successor = self
      # self._finger[0] = FingerEntry(self.id(), self)
      self._predecessor = self

    # TODO: rewrite and uncomment methods to adapt RPC calls
    # add other entries in finger table
    self.init_finger(remote_address)

    self.fix_finger()

    # self.update_successors()

    # 4) call `to_be_added`.stabilize() to update the nodes between `to_be_added` and its predecessor
    # self.stabilize()

    self.log("joined")

  # first node on circle that succeeds (n + 2^k−1) mod 2m, 1 <= k <= m
  # i-th entry means the 2^i far-away node from the current node
  def init_finger(self, remote_address = None):
    print('init_finger: ', remote_address)
    if remote_address:
      # get the arbitrary node in which the target node want to join
      # remote_node = self._remote.getRemoteNode(remote_address)
      remote_node = self.get_remote_node_by_ip(remote_address)

      # successor
      successor = self.successor()
      print('init_finger: successor: ', successor)
      if successor is None:
        successor = remote_node.find_successor_r(self.id())
        print('remote_node.find_successor_r(self.id()): ', successor)
        successor = self.get_remote_node_by_ip(Address(successor.ip_addr))
        self._successor = successor

      # initialize finger table
      for x in range(1, M_BIT):
        start_id = (self.id() + 2 ** x) % NUM_SLOTS
        self._finger[x] = FingerEntry(start_id, None)

      for x in range(0, M_BIT - 1):
        start_id = self._finger[x + 1].start
        if inrange(start_id, self.id(), self._finger[x].node.id_r()):
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

  # called periodically
  # back-up successor list, a M_BIT-long successor link list
  def update_successors(self):
    if self._leave:
      return

    successor = self._successor

    for x in range(M_BIT):
      if successor is not None:
        self._successors[x] = successor
        successor = successor.successor_r()
        successor = self.get_remote_node_by_ip(Address(successor.ip_addr))

    threading.Timer(2, self.update_successors).start()

  def id(self, offset = 0):
    if self._id is not None:
      return self._id
    else:
      return 0

  def id_r(self, offset = 0):
    if self._id is not None:
      return self._id
    else:
      return 0

  def successor(self):
    successor = self._successor
    # self.log('current successor %b' % self._successor.ping())

    if not successor.ping():
      for x in range(1, len(self._successors)):
        if self._successors[x].ping():
          successor = self._successors[x]

    # self.log('current successor %d' % successor.id())

    return successor

  def successor_r(self):
    suc = self.successor()
    ret = RemoteNode()

    if suc is not None:
      ret.id = suc.id_r()
      ret.ip_addr = suc.ip_r()
      ret.port = suc.port()

    print('successor_r ret: ', ret)

    return ret

  def predecessor(self):
    return self._predecessor

  def predecessor_r(self):
    pre = self.predecessor()
    ret = RemoteNode()

    if pre is not None:
      ret.id = pre.id_r()
      ret.ip_addr = pre.ip_r()
      ret.port = pre.port()

    print('rpc call predecessor_r, ret: ', ret)

    return ret

  def set_predecessor(self, pre_rn):
    # assign the RPC client to the remote node
    self._predecessor = self.get_remote_node_by_ip(Address(pre_rn.ip_addr))

    print('rpc call set_predecessor, pre_rn: ', pre_rn)

  def find_successor(self, id):
    self.log("find_successor of {}".format(id))
    # if self._predecessor exists, and _predecessor.id < id < self.id, the successor is current node
    print('-----------find_successor-----------')
    print(self._predecessor)
    if self._predecessor and inrange(id, self._predecessor.id_r(), self.id()):
      return self

    suc_rn = self.find_predecessor(id).successor_r()
    return self.get_remote_node_by_ip(Address(suc_rn.ip_addr))

  # RPC call
  def find_successor_r(self, id):
    self.log("find_successor_r of {}".format(id))
    suc = self.find_successor(id)
    ret = RemoteNode()

    ret.id = suc.id_r()
    ret.ip_addr = suc.ip_r()
    ret.port = suc.port()

    return ret

  def find_predecessor(self, id):
    lg = "find_predecessor of: {}".format(id)
    self.log(lg)
    node = self
    # when the ring only has one node, node.id is the same as node.successor.id,
    # if we are alone in the ring, we are the pred(id)
    if node.id_r() == node.successor_r().id:
      return node

    while not inrange(id, node.id_r(), node.successor().id_r() + 1):
      # if node is of type RemoteNode rather than Node, get its RPC client
      if not util.isRemoteNodeType(node):
        node = self.get_remote_node_by_ip(Address(node.ip_addr))

      node = node.closest_preceding_node_r(id)
      node = self.get_remote_node_by_ip(Address(node.ip_addr))

    return node

  def _closest_preceding_node(self, id):
    # from m down to 1
    for x in reversed(range(len(self._finger))):
      entry = self._finger[x]
      if entry != None and entry.node != None and inrange(entry.node.id_r(), self.id(), id):
        return entry.node

    return self

  def closest_preceding_node_r(self, id):
    node = self._closest_preceding_node(id)
    ret = RemoteNode()

    ret.id = node.id_r()
    ret.ip_addr = node.ip_r()
    ret.port = node.port_r()

    return ret

  def get_finger(self):
    finger = []
    for x in range(len(self._finger)):
      if self._finger[x] is not None:
        finger.append({'start': self._finger[x].start, 'node': self._finger[x].node.id_r()})
      else:
        finger.append({})

    return finger

  def update_finger(self, successor, index):
    if self._finger[index] is not None:
      if inrange(successor.id_r(), self.id() - 1, self._finger[index].node.id_r()):
        self._finger[index].node = successor
        self._predecessor.update_finger_r(successor, index)
        # print('finger table of ', self.id(), 'start: ', self._finger[x].start, 'node', self._finger[x].node.id())

    # threading.Timer(2, self.update_finger).start()

  def update_finger_r(self, successor_rn, index):
    successor = self.get_remote_node_by_ip(Address(successor_rn.ip_addr))
    self.update_finger(successor, index)

  def update_others(self):
    for x in range(1, M_BIT + 1):
      # find last node whose i-th finger might be current node
      start = (self.id() - 2 ** (x - 1)) % NUM_SLOTS
      pre = self.find_predecessor(start)
      # if only one node on the ring, no need to update others
      if pre.id_r() == self.id():
        continue

      rn = RemoteNode()
      rn.id = self.id()
      rn.ip_addr = self.ip()
      rn.port = self.port()

      pre.update_finger_r(rn, x)

  # called periodically
  # clear the node’s predecessor pointer if n.predecessor is alive, or has failed
  def check_predecessor(self):
    if self._leave:
      return

    # self.log('check_predecessor, predecessor of {}: , isAlive: {}'.format(self.predecessor().id(), self.predecessor().ping()))
    pre = self.predecessor()
    print('pre: ', pre)
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

    pre_rn = successor.predecessor_r()
    pre = self.get_remote_node_by_ip(Address(pre_rn.ip_addr))
    if pre is not None and inrange(pre.id_r(), self.id(), successor.id_r()):
      self.log('stabilize calls update_successor')
      self.update_successor(pre)

    rn = RemoteNode()
    rn.ip_addr = self.ip()
    rn.id = self.id()
    rn.port = self.port()

    successor.notify_r(rn)
    self.print_finger('stabilize')

    threading.Timer(2, self.stabilize).start()

  # receive request that some node thinks it might be our predecessor
  def notify(self, pre):
    # check if pre is the new predecessor
    if (self._predecessor is None or inrange(pre.id_r(), self._predecessor.id_r(), self.id())):
      self._predecessor = pre

  # RPC call
  def notify_r(self, pre):
    # check if pre is the new predecessor
    remote_node = self.get_remote_node_by_ip(Address(pre.ip_addr))
    self.notify(remote_node)
    # if (self._predecessor is None or inrange(pre.id(), self._predecessor.id(), self.id())):
    #   self._predecessor = pre

  # called periodically
  # randomly update finger table
  def fix_finger(self):
    if self._leave:
      return
    self.log('fix_finger')
    index = random.randrange(M_BIT - 1) + 1
    self._finger[index].node = self.find_successor(self._finger[index].start)
    self.print_finger('fix_finger')

    threading.Timer(2, self.fix_finger).start()

  # update both first entry in finger table and _successor
  def update_successor(self, new_s):
    self._successor = new_s
    self._finger[0].node = new_s

  def print_finger(self, mod='default'):
    for x in range(0, M_BIT):
      if self._finger[x] is not None:
        self.log('{}: finger table of {}, start: {}, node: {}'.format(mod, self.id(), self._finger[x].start, self._finger[x].node.id_r()))

