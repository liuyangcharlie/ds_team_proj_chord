from chordsite.node import Node
from chordsite.remote import RemoteConnection
from chordsite.address import Address
from chordsite.env import M_BIT

m = M_BIT
address = ["127.0.0.1", "127.0.0.2", "127.0.0.3", "127.0.0.4"]
ring = None


def create_ring():
    global ring
    ring = RemoteConnection(address)
    return ring

def print_ring():
    global ring
    ring.printNodes()

def get_all_finger():
    global ring
    rs = ring.ringShape()
    return rs

def add_node(ip):
    global ring
    rs = ring.addNode(str(ip))
    return rs

def lookup(key, id):
    global ring
    print('key, id', key, id)
    target = ring.lookup(int(key), int(id))
    return target

def remove_node(id):
    global ring
    s = ring.nodeDepature(int(id))
    return s
