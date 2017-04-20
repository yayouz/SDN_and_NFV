import os
import re
import signal
from time import sleep

class autotest(object):
    def __init__ (self,net):
        self.net = net


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

    def count(self, correct,total,success):
        if correct==True:
           total=total+1
           success=success+1
        else:
           total=total+1
        return total, success


    def test(self,net):
        total=0
        success=0
        h1=net.get('h1')
        h2=net.get('h2')
        h3=net.get('h3')
        h4=net.get('h4')
        ds1=net.get('ds1')
        ds2=net.get('ds2')
        ds3=net.get('ds3')
        ws1=net.get('ws1')
        ws2=net.get('ws2')
        ws3=net.get('ws3')

        """ICMP testing"""
        result=h1.cmd('ping -c 1 100.0.0.12')
        #print result
        total,success=self.count(self._parsePing(result),total,success)
        result=h2.cmd('ping -c 1 100.0.0.51')
        #print result
        total,success=self.count(not self._parsePing(result),total,success)
        result=h3.cmd('ping -c 1 100.0.0.11')
        #print result
        total,success=self.count(self._parsePing(result),total,success)
        result=h4.cmd('ping -c 1 100.0.0.51')
        #print result
        total,success=self.count(self._parsePing(result),total,success)

        """UDP testing"""


        """TCP testing"""
        psuccess=100*success/total
        #print("***Result: %i%% transmitted successfully" % psuccess)
        return psuccess
        
