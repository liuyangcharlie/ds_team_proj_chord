class FingerEntry(object):
  """docstring for FingerEntry"""
  def __init__(self, start, node):
    # start, ID hash of (n + 2^i) mod (2^m)
    self.start = start
    # node
    self.node = node
