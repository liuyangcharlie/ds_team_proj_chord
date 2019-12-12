#!/usr/bin/env python

import glob
import sys
import os
import threading

from address import Address

dir_path = os.path.dirname(os.path.realpath(__file__))

sys.path.append(dir_path + '/gen-py')

from serv import Remote
#from tutorial.ttypes import InvalidOperation, Operation

#from shared.ttypes import SharedStruct

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol, TJSONProtocol
from thrift.server import TServer


class Rpc(object):
    def __init__(self, node):
        self.log = {}
        self.node = node

    # def ping(self):
    #     print('ping()ping()ping()ping()ping()ping()ping()')

    # def add(self, n1, n2):
    #     print('add(%d,%d)' % (n1, n2))
    #     return n1 + n2

    # find the node by address, aka key id
    # def getRemoteNode(self, address):
    #     # check cache
    #     if self.remote_clients[address.__str__()] != None:
    #         return self.remote_clients[address.__str__()]

    #     node = None

    #     # index = address.__hash__()
    #     # node = self._nodes[index]
    #     print('getRemoteNode()')

    #     return node

    def startServer(self):
        handler = self.node
        processor = Remote.Processor(handler)
        transport = TSocket.TServerSocket(host="0.0.0.0", port=9090)
        tfactory = TTransport.TBufferedTransportFactory()
        pfactory = TBinaryProtocol.TBinaryProtocolFactory()
        # pfactory = TJSONProtocol.TJSONProtocolFactory()

        # You could do one of these for a multithreaded server
        server = TServer.TThreadedServer(
               processor, transport, tfactory, pfactory)
        # server = TServer.TThreadPoolServer(
        #         processor, transport, tfactory, pfactory)

        print('Starting the server...')
        threading.Thread(target=server.serve).start()
        print('done.')
