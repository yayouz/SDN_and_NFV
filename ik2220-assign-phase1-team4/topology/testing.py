import os
import re
import signal
from time import sleep

class autotest(object):
    def __init__ (self,net):
        self.net = net
        self.total=0
        self.success=0
    
    def _parsePing(self, pingOutput ):
        "Parse ping output and return packets sent, received."
        # Check for downed link
        if 'connect: Network is unreachable' in pingOutput:
            return (1, 0)
        r = r'(\d+) packets transmitted, (\d+) received'
        m = re.search( r, pingOutput )
        if m is None:
            
            error( '*** Error: could not parse ping output: %s\n' %
                   pingOutput )
            
            return (1, 0)
        sent, received = int( m.group( 1 ) ), int( m.group( 2 ) )
        if sent==received:
          return True
        else:
          return False
     
    def _parseIperf(self, iperfOutput ):
         r = r'([\d\.]+ \w+/sec)'
         m = re.findall( r, iperfOutput )
         r = r'(WARNING)'
         m2 = re.findall( r, iperfOutput )
         if (m and not m2):
             return True
         else:
             # was: raise Exception(...)
            # error( 'could not parse iperf output: ' % iperfOutput )
             return False

    def _parseWget(self, wgetOutput ):
         r = r'(200 OK)'
         m = re.findall( r, wgetOutput )
         if m:
             return True
         else:
             # was: raise Exception(...)
            # error( 'could not parse iperf output: ' % iperfOutput )
             return False

    def count(self,correct):
        if correct==True:
           self.total=self.total+1
           self.success=self.success+1
        else:
           self.total=self.total+1
        


    def test(self):

        h1=self.net.get('h1')
        h2=self.net.get('h2')
        h3=self.net.get('h3')
        h4=self.net.get('h4')
        ds1=self.net.get('ds1')
        ds2=self.net.get('ds2')
        ds3=self.net.get('ds3')
        ws1=self.net.get('ws1')
        ws2=self.net.get('ws2')
        ws3=self.net.get('ws3')

        """ICMP testing"""
        result=h1.cmd('ping -c 1 100.0.0.12')
        #print result
        self.count(self._parsePing(result))
        result=h2.cmd('ping -c 1 100.0.0.51')
        #print result
        self.count(not self._parsePing(result))
        result=h3.cmd('ping -c 1 100.0.0.11')
        #print result
        self.count(self._parsePing(result))
        result=h4.cmd('ping -c 1 100.0.0.51')
        #print result
        self.count(self._parsePing(result))


        """UDP testing"""
        ds1.cmd('iperf -u -s -p 53 &')
        ds2.cmd('iperf -u -s -p 53 &')
        ds3.cmd('iperf -u -s -p 53 &')
        resUDP=h1.cmd('iperf -u -c 100.0.0.20 -p 53')
        print resUDP
        self.count(self. _parseIperf(resUDP))

        resUDP=h3.cmd('iperf -u -c 100.0.0.21 -p 53')
        print resUDP
        self.count(self. _parseIperf(resUDP))

        resUDP=h2.cmd('iperf -u -c 100.0.0.22 -p 40')
        print resUDP
        self.count(not self. _parseIperf(resUDP))
        
        ws1.cmd('kill %while')
        ws2.cmd('kill %while')
        ws3.cmd('kill %while')


        """TCP testing"""
        ws1.cmd('python -m SimpleHTTPServer 80 &')
        ws2.cmd('python -m SimpleHTTPServer 80 &')
        ws3.cmd('python -m SimpleHTTPServer 80 &')
        sleep(10)

        resTCP=h1.cmd('wget 100.0.0.40')
        #print resTCP
        self.count(self._parseWget(resTCP))
        
        resTCP=h4.cmd('wget 100.0.0.42')
        #print resTCP
        self.count(self._parseWget(resTCP))
        
        resTCP=h3.cmd('iperf -c 100.0.0.42 -p 53')
        #print resTCP
        self.count(not self. _parseIperf(resTCP))

        ws1.cmd('kill %python')
        ws2.cmd('kill %python')
        ws3.cmd('kill %python')


        """Result computation"""
        psuccess=100*self.success/self.total
        print("***Result:total is:%d success is:%d" %(self.total,self.success))
        #print("***Result: %i%% transmitted successfully" % psuccess)
        
        
        return psuccess
