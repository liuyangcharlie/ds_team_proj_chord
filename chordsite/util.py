import socket
import rpyc
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def local_ip():
  return socket.gethostbyname(socket.gethostname())

def is_remote_node(node):
    # if node.ip == local_ip():
    #     return True
    # return False
    pass

def ringShape(head):
    # read file node_addr to get add ips
    # TODO: we may be able to replace it with database
    s = []
    ip_arr = []
    f= open(os.path.abspath(os.path.join(BASE_DIR, '../node_addr')), 'r')
    for ip in f:
        i = ip.strip()
        if i:
            ip_arr.append(i)

    print('head.node_id(): ', head.node_id())

    local = local_ip()
    for ip in ip_arr:
        print('local: ', local, 'ip: ', ip, 'ip == local: ', ip == local)
        if ip == local:
            s.append(head.node_id())
        else:
            n = rpyc.connect(ip, 18861).root
            s.append(n.node_id())

    f.close()

    return s