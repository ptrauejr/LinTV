import select
import socket
import sys
import pybonjour
from ..protocol import Protocol
from airplay.server.node import Node
from airplay.protocol import Protocol


class Browser:
    timeout  = 5
    queried  = []
    resolved = []
    servers = {}
    
    # Helper method to parse out the TXT Records returned since these aren't in
    # a real python data structure when returned by pybonjour
    def parse_txt_record(txtRecord):
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
    def query_record_callback(sdRef, flags, interfaceIndex, errorCode, fullname,
                              rrtype, rrclass, rdata, ttl):
        if errorCode == pybonjour.kDNSServiceErr_NoError:
            print '  IP         =', socket.inet_ntoa(rdata)
            queried.append(True)
    
    
    # Callback that performs the initial lookup to get a list of targets
    # matching the type
    def resolve_callback(sdRef, flags, interfaceIndex, errorCode, fullname,
                         hosttarget, port, txtRecord):
        if errorCode != pybonjour.kDNSServiceErr_NoError:
            return
    
        print 'Resolved service:'
        print '  fullname   =', fullname
        print '  hosttarget =', hosttarget
        print '  port       =', port
    
        pairs = parse_txt_record(txtRecord)
        print '  txtRecord  =', pairs

        server = Node(fullname, hosttarget, port, pairs)
        servers[fullname] = server
    
        query_sdRef = \
                pybonjour.DNSServiceQueryRecord(interfaceIndex = interfaceIndex,
                                                fullname = hosttarget,
                                                rrtype =
                                                pybonjour.kDNSServiceType_A,
                                                callBack = query_record_callback)
    
        try:
            while not queried:
                ready = select.select([query_sdRef], [], [], timeout)
                if query_sdRef not in ready[0]:
                    print 'Query record timed out'
                    break
                pybonjour.DNSServiceProcessResult(query_sdRef)
            else:
                queried.pop()
        finally:
            query_sdRef.close()
    
        resolved.append(True)
    
    
    def browse_callback(flags, interfaceIndex, errorCode, serviceName,
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
                                                    resolve_callback)
    
        try:
            while not resolved:
                ready = select.select([resolve_sdRef], [], [], timeout)
                if resolve_sdRef not in ready[0]:
                    print 'Resolve timed out'
                    break
                pybonjour.DNSServiceProcessResult(resolve_sdRef)
            else:
                resolved.pop()
        finally:
            resolve_sdRef.close()
    
    
    def browse(self):
        regtype = Protocol.SEARCH
        browse_sdRef = pybonjour.DNSServiceBrowse(regtype = regtype,
                                                  callBack = browse_callback)
        
        try:
            try:
                while True:
                    ready = select.select([browse_sdRef], [], [])
                    if browse_sdRef in ready[0]:
                        pybonjour.DNSServiceProcessResult(browse_sdRef)
            except KeyboardInterrupt:
                pass
        finally:
            browse_sdRef.close()
    

