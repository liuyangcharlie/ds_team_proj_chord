#!/bin/python
import sys
import socket

sys.path.append('gen-py')

from serv import Remote

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
# pb, other options are `TJSONProtocol`, `TDebugProtocol`, etc.
from thrift.protocol import TBinaryProtocol


def create_rpc_client(ip, port=9090):
    print('--------')
    print('ip: ', ip, 'local_ip: ', local_ip())
    if ip == local_ip():
      return None

    # thrift_service is the defined Thrift service
    thrift_service = Remote

    # Make socket
    transport = TSocket.TSocket(ip, 9090)

    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)

    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    # Create a client to use the protocol encoder
    client = thrift_service.Client(protocol)

    # Connect!
    transport.open()

    print('client open!', client)

    # client.ping()
    # print('ping()')

    # sum_ = client.add(1, 1)
    # print('1+1=%d' % sum_)

    # Close!
    # transport.close()

    return client

# def log(info):
#     f = open("/tmp/chord.log", "a+")
#     f.write(str(self.id()) + " : " +  info + "\n")
#     f.close()
    # print(str(self.id()) + " : " +  info)

def local_ip():
  return socket.gethostbyname(socket.gethostname())

def isRemoteNodeType(node):
  # if node is the return value type of RPC methods('RemoteNode' type)
  # it may be of 'Client' type or 'Node' type
  return type(node).__name__ is not 'Client' and not callable(getattr(node, 'find_successor', None))