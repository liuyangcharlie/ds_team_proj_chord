from chordsite import util
from chordsite.node import Node
from chordsite.remote import RemoteConnection
from chordsite.address import Address
from chordsite.env import M_BIT

m = M_BIT
# address = ["127.0.0.1", "127.0.0.2", "127.0.0.3", "127.0.0.4"]
global head
head = None


# def create_ring():
#     global head
#     # head = Node(address[0])
#     return head

# def print_ring():
#     global head
#     head.printNodes()

def get_all_finger(head):
    # global head
    rs = util.ringShape(head)
    print('rs: ', rs)
    return rs

# def add_node(ip):
#     global head
#     rs = head.addNode(str(ip))
#     return rs

# def lookup(key, id):
#     global head
#     print('key, id', key, id)
#     target = head.lookup(int(key), int(id))
#     return target

# def remove_node(id):
#     global head
#     s = head.nodeDepature(int(id))
#     return s

# if __name__ == "__main__":
#     head = Node(address[0])