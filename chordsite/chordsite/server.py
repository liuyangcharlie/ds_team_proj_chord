import os

from .node import Node
from .remote import RemoteConnection
from .address import Address
from .env import M_BIT

# from simple_http_server import request_map
# from simple_http_server import Response
# from simple_http_server import MultipartFile
# from simple_http_server import Parameter
# from simple_http_server import Parameters
# from simple_http_server import Header
# from simple_http_server import JSONBody
# from simple_http_server import HttpError
# from simple_http_server import StaticFile
# from simple_http_server import Headers
# from simple_http_server import Cookies
# from simple_http_server import Cookie
# from simple_http_server import Redirect
# from setting import STATIC_ROOT
# import simple_http_server.server as server

m = M_BIT
address = ["127.0.0.1", "127.0.0.2", "127.0.0.3", "127.0.0.4"]
ring = None

# @request_map("/")
# def index():
#     dir = os.path.dirname(os.path.realpath(__file__))
#     return open(dir + "/app/index.html", 'r').read()

# @request_map("/index.css")
# def my_ctrl0():
#     dir = os.path.dirname(os.path.realpath(__file__))
#     return Headers({"content-type": "text/css"}), open(dir + "/app/index.css", 'r').read()

# @request_map("/index.js")
# def my_ctrl1():
#     dir = os.path.dirname(os.path.realpath(__file__))
#     return Headers({"content-type": "text/javascript"}), open(dir + "/app/index.js", 'r').read()

# @request_map("/create_ring")
def create_ring():
    global ring
    ring = RemoteConnection(address)
    # return Headers({"content-type": "application/json"}), {'error': None}

# @request_map("/print_ring")
def print_ring():
    global ring
    ring.printNodes()
#     return Headers({"content-type": "application/json"}), {'error': None}

# @request_map("/get_all_finger")
def get_all_finger():
    global ring
    rs = ring.ringShape()
#     return Headers({"content-type": "application/json"}), {'error': None, 'shape': rs, 'm': M_BIT}

# @request_map("/add_node")
def add_node(ip):
    global ring
    rs = ring.addNode(str(ip))
#     return Headers({"content-type": "application/json"}), {'error': None, 'shape': rs}

# @request_map("/lookup")
def lookup(key, id):
    global ring
    print('key, id', key, id)
    target = ring.lookup(int(key), int(id))
#     return Headers({"content-type": "application/json"}), {'error': None, 'target': target}

# @request_map("/remove_node")
def remove_node(id):
    global ring
    s = ring.nodeDepature(int(id))
#     return Headers({"content-type": "application/json"}), {'error': None, 'shape': s}



# server.start()
