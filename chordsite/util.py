import socket

def local_ip():
  return socket.gethostbyname(socket.gethostname())

def is_remote_node(node):
    # if node.ip == local_ip():
    #     return True
    # return False
    pass

def ringShape(node):
    s = []
    for x in range(len(node._nodes)):
      if node._nodes[x] is not None:
        s.append({'addr': node._nodes[x]._address.__str__(), 'finger': node._nodes[x].get_finger()})
      else:
        s.append(None)

    return s