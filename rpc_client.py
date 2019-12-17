import rpyc

"""
RPCClient is a set of functions/methods that a node would perform related to a remote node, such as:
# - getRemoteNode
"""
class RPCClient(object):
    def __init__(self, ip, port=18861):
        # self.node = node
        self.conn = rpyc.connect(ip, port)

    def get_conn(self):
        return self.conn

    def get_remote(self):
        return self.conn.root