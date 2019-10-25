# import hashlib
from env import *

# Helper function to determine if a key falls within a range
def inrange(c, a, b):
  # is c in [a,b)?, if a == b then it assumes a full circle
  # on the DHT, so it returns True.
#   if a < b:
  return a <= c and c < b

class Address(object):
  def __init__(self, ip, port=9999):
    self.ip = ip
    self.port = int(port)

  def __hash__(self):
    # return hashlib.sha1(("%s:%s" % (self.ip, self.port)).encode()) % SIZE
    h = hash(("%s:%s" % (self.ip, self.port)).encode()) % NUM_SLOTS
    # print('__ip__: ', self.ip, '__hash__: ', h)
    return h

  def __cmp__(self, other):
    return other.__hash__() < self.__hash__()

  def __eq__(self, other):
    return other.__hash__() == self.__hash__()

  def __str__(self):
    return "[\"%s\", %s]" % (self.ip, self.port)
