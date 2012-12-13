import sys

# Class to represent an actual server node.  This is an informational class
# only.
class Node:
    def __init__(self, name, domain, port, info):
        self.name = name
        self.domain = domain
        self.ip = ip
        self.port = port
        self.deviceid = info['deviceid']
        self.srcvers = info['srcvers']
        self.model = info['mode']

    def setIP(self, ip):
        self.ip = ip
