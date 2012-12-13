import select
import socket
import sys
import pybonjour
from airplay.server.node import Node
from airplay.protocol import Protocol


class Browser:
    timeout  = 5
    queried  = []
    resolved = []
    browsed = []
    servers = {}
    
    def browse(self):
        regtype = Protocol.SEARCH
        browse_sdRef = pybonjour.DNSServiceBrowse(regtype = regtype,
                                                  callBack = self.browse_callback)
        
        try:
            try:
                while not self.browsed:
                    ready = select.select([browse_sdRef], [], [])
                    if browse_sdRef in ready[0]:
                        pybonjour.DNSServiceProcessResult(browse_sdRef)
            except KeyboardInterrupt:
                pass
        finally:
            browse_sdRef.close()
            self.browsed.pop()

    # Helper method to parse out the TXT Records returned since these aren't in
    # a real python data structure when returned by pybonjour
    def parse_txt_record(self, txtRecord):
        parsedRecord = {}
    
        while txtRecord:
            length = ord(txtRecord[0])
            pair = txtRecord[1:length+1].split('=', 1)
    
            if pair[0] and (pair[0] not in parsedRecord):
                if len(pair) == 1:
                    parsedRecord[pair[0]] = None
                else:
                    parsedRecord[pair[0]] = pair[1]
    
            txtRecord = txtRecord[length+1:]
    
        return parsedRecord
    
    
    # Callback that performs the dns lookup on the hostname
    def query_record_callback(self, sdRef, flags, interfaceIndex, errorCode, fullname,
                              rrtype, rrclass, rdata, ttl):
        if errorCode == pybonjour.kDNSServiceErr_NoError:
            print '  IP         =', socket.inet_ntoa(rdata)
            self.queried.append(True)
    
    
    # Callback that performs the initial lookup to get a list of targets
    # matching the type
    def resolve_callback(self, sdRef, flags, interfaceIndex, errorCode, fullname,
                         hosttarget, port, txtRecord):
        if errorCode != pybonjour.kDNSServiceErr_NoError:
            return
    
        print 'Resolved service:'
        print '  fullname   =', fullname
        print '  hosttarget =', hosttarget
        print '  port       =', port
    
        pairs = self.parse_txt_record(txtRecord)
        print '  txtRecord  =', pairs

        self.servers[fullname] = Node(fullname, hosttarget, port, pairs)
    
        query_sdRef = \
                pybonjour.DNSServiceQueryRecord(interfaceIndex = interfaceIndex,
                                                fullname = hosttarget,
                                                rrtype =
                                                pybonjour.kDNSServiceType_A,
                                                callBack = self.query_record_callback)
    
        try:
            while not self.queried:
                ready = select.select([query_sdRef], [], [], self.timeout)
                if query_sdRef not in ready[0]:
                    print 'Query record timed out'
                    break
                pybonjour.DNSServiceProcessResult(query_sdRef)
            else:
                self.queried.pop()
        finally:
            query_sdRef.close()
    
        self.resolved.append(True)
    
    
    def browse_callback(self, sdRef, flags, interfaceIndex, errorCode, serviceName,
                        regtype, replyDomain):
        if errorCode != pybonjour.kDNSServiceErr_NoError:
            return
        
        if not (flags & pybonjour.kDNSServiceFlagsAdd):
            print 'Service removed'
            return
    
        print 'Service added; resolving'
    
        resolve_sdRef = pybonjour.DNSServiceResolve(0,
                                                    interfaceIndex,
                                                    serviceName,
                                                    regtype,
                                                    replyDomain,
                                                    self.resolve_callback)
    
        try:
            while not self.resolved:
                ready = select.select([resolve_sdRef], [], [], self.timeout)
                if resolve_sdRef not in ready[0]:
                    print 'Resolve timed out'
                    break
                pybonjour.DNSServiceProcessResult(resolve_sdRef)
            else:
                self.resolved.pop()
        finally:
            resolve_sdRef.close()
        self.browsed.append(True)
    
    def findByName(self, name):
        return servers[name]
