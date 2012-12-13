import sys

# Class to represent an actual server node.  This is an informational class
# only.
class Node:
    def __init__(self, name, domain, ip, port, info):
        self.name = name
        self.domain = domain
        self.ip = ip
        self.port = port
