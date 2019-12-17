#!/bin/python
import rpyc

"""
RPyC notes:
- exposed_
- pass a class of which every connection will receive a separate instance. can pass a instance
"""
class RPC(rpyc.Service):
    """
    RPC class is to manage RPC connections of a Node.
    The LOCAL Node itself could have multiple connections with other REMOTE nodes,
    such as its successor, predecessor, and possibly other nodes in its FingerTable.

    parameter node refers to the node itself, very node has a single rpc server equipped with it
    """
    def __init__(self, node):
        self.node = node
        pass


    def exposed_find_pred(self):
        print('exposed_find_pred')
        pass

    def exposed_find_succ(self, id):
        print('exposed_find_succ')
        # call `node.find_successor`
        remote = self.node.find_successor(id)
        return remote

    def exposed_get_succ(self):
        print('exposed_get_succ')
        pass

    def exposed_get_pred(self):
        print('exposed_get_pred')
        pass

    def exposed_get_id(self, node_id):
        print('exposed_get_id')
        pass

    def exposed_node_ping(self):
        print('exposed_node_ping: ', self.node.ping())
        pass

    def exposed_update_finger(self):
        print('exposed_update_finger')
        pass

    # def exposed_get_remote_node(self):
    #     print('exposed_get_remote_node')
    #     pass

# if __name__ == "__main__":
    # from rpyc.utils.server import ThreadedServer

    # ThreadedServer(RPC(), port = 18871).start()

