import os
import re
import signal
import time

class autotest(object):
    def __init__ (self,net):
        self.net = net
        self.total=0
        self.success=0
        self.h1 = self.net.get('h1')
        self.h2 = self.net.get('h2')
        self.h3 = self.net.get('h3')
        self.h4 = self.net.get('h4')
        self.ds1 = self.net.get('ds1')
        self.ds2 = self.net.get('ds2')
        self.ds3 = self.net.get('ds3')
        self.ws1 = self.net.get('ws1')
        self.ws2 = self.net.get('ws2')
        self.ws3 = self.net.get('ws3')
        self.insp = self.net.get('insp')
        #self.file = open('Phase_2_Report','w')
    
    def _parsePing(self, pingOutput ):
        "Parse ping output and return packets sent, received."
        # Check for downed link
        if 'connect: Network is unreachable' in pingOutput:
            return False
        r = r'(\d+) packets transmitted, (\d+) received'
        m = re.search( r, pingOutput )
        if m is None:
            
            error( '*** Error: could not parse ping output: %s\n' %
                   pingOutput )
            
            return False
        sent, received = int( m.group( 1 ) ), int( m.group( 2 ) )
        if received!=0:
          return True
        else:
          return False
     
    def _parseDig(self, digOutput ):
        if "connection timed out" in digOutput:
            return False
        else:
            return True

    def _parseWget(self, wgetOutput ):
         r = r'(POST)'
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

    def ping(self):
        print 'Ping Test (SRC -> DST Success!/Failed!)'
        print 'H1 -> H3 ',
        t1 = self.h1.cmd('ping -c 1 10.0.0.50')
        if self._parsePing(t1):
            print 'Success!'
        else:
            print 'Failed!'
        print 'H1 -> LoadBalance1',
        t2 = self.h1.cmd('ping -c 4 100.0.0.25')
        if self._parsePing(t2):
            print 'Success!'
        else:
            print 'Failed!'
        print 'H1 -> LoadBalance2',
        t3 = self.h1.cmd('ping -c 4 100.0.0.45')
        if self._parsePing(t3):
            print 'Success!'
        else:
            print 'Failed!'
        print 'H2 -> H3',
        t4 = self.h2.cmd('ping -c 1 10.0.0.50')
        if self._parsePing(t4):
            print 'Success!'
        else:
            print 'Failed!'
        print 'H1 -> H4',
        t5 = self.h1.cmd('ping -c 1 10.0.0.51')
        if self._parsePing(t5):
            print 'Success!'
        else:
            print 'Failed!'
        print 'H2 -> H4',
        t6 = self.h2.cmd('ping -c 1 10.0.0.51')
        if self._parsePing(t6):
            print 'Success!'
        else:
            print 'Failed!'
        print 'H2 -> LoadBalance1',
        t7 = self.h2.cmd('ping -c 4 100.0.0.25')
        if self._parsePing(t7):
            print 'Success!'
        else:
            print 'Failed!'
        print 'H2 -> LoadBalance2',
        t8 = self.h2.cmd('ping -c 4 100.0.0.45')
        if self._parsePing(t8):
            print 'Success!'
        else:
            print 'Failed!'
        
        print 'H3 -> H1',
        t9 = self.h3.cmd('ping -c 1 100.0.0.10')
        if self._parsePing(t9):
            print 'Success!'
        else:
            print 'Failed!'
        print 'H3 -> H2',
        t10 = self.h3.cmd('ping -c 1 100.0.0.11')
        if self._parsePing(t10):
            print 'Success!'
        else:
            print 'Failed!'
        
        print 'H4 -> H1',
        t11 = self.h4.cmd('ping -c 1 100.0.0.10')
        if self._parsePing(t11):
            print 'Success!'
        else:
            print 'Failed!'
        print 'H4 -> H2',
        t12 = self.h4.cmd('ping -c 1 100.0.0.11')
        if self._parsePing(t12):
            print 'Success!'
        else:
            print 'Failed!'
        
        print 'H4 -> H3',
        t13 = self.h4.cmd('ping -c 1 10.0.0.50')
        if self._parsePing(t13):
            print 'Success!'
        else:
            print 'Failed!'
        print 'H3 -> H4',
        t14 = self.h3.cmd('ping -c 1 10.0.0.51')
        if self._parsePing(t14):
            print 'Success!'
        else:
            print 'Failed!'
        print 'H1 -> H2',
        t15 = self.h1.cmd('ping -c 1 100.0.0.11')
        if self._parsePing(t15):
            print 'Success!'
        else:
            print 'Failed!'
        print 'H2 -> H1',
        t16 = self.h2.cmd('ping -c 1 100.0.0.10')
        if self._parsePing(t16):
            print 'Success!'
        else:
            print 'Failed!'
        print 'H3 -> LoadBalance1',
        t17 = self.h3.cmd('ping -c 2 100.0.0.25')
        if self._parsePing(t17):
            print 'Success!'
        else:
            print 'Failed!'
        print 'H3 -> LoadBalance2',
        t18 = self.h3.cmd('ping -c 2 100.0.0.45')
        if self._parsePing(t18):
            print 'Success!'
        else:
            print 'Failed!'
        print 'H4 -> LoadBalance1',
        t19 = self.h4.cmd('ping -c 2 100.0.0.25')
        if self._parsePing(t19):
            print 'Success!'
        else:
            print 'Failed!'
        print 'H4 -> LoadBalance2',
        t20 = self.h4.cmd('ping -c 1 100.0.0.45')
        if self._parsePing(t20):
            print 'Success!'
        else:
            print 'Failed!'

        print "Storing data in Phase_2_Report"
        
        print "Calculating Success Rate"
        
        x=0
        
        if self._parsePing(t1):
            x=x+1
            self.count(True)
        if self._parsePing(t2):
            x=x+1
            self.count(True)
        if self._parsePing(t3):
            x=x+1
            self.count(True)
        if self._parsePing(t4):
            x=x+1
            self.count(True)
        if self._parsePing(t5):
            x=x+1
            self.count(True)
        if self._parsePing(t6):
            x=x+1
            self.count(True)
        if self._parsePing(t7):
            x=x+1
            self.count(True)
        if self._parsePing(t8):
            x=x+1
            self.count(True)
        if self._parsePing(t9):
            x=x+1
            self.count(True)
        if self._parsePing(t10):
            x=x+1
            self.count(True)
        if self._parsePing(t11):
            x=x+1
            self.count(True)
        if self._parsePing(t12):
            x=x+1
            self.count(True)
        if self._parsePing(t13):
            x=x+1
            self.count(True)
        if self._parsePing(t14):
            x=x+1
            self.count(True)
        if self._parsePing(t15):
            x=x+1
            self.count(True)
        if self._parsePing(t16):
            x=x+1
            self.count(True)
        if self._parsePing(t17):
            x=x+1
            self.count(True)
        if self._parsePing(t18):
            x=x+1
            self.count(True)
        if self._parsePing(t19):
            x=x+1
            self.count(True)
        if self._parsePing(t20):
            x=x+1
            self.count(True)
        
        print 'Ping Tests Done'
        
        print "Succes rate: " + str(x)+"/20"
        print "Expected rate: 16/20"


    def http(self):
        self.ws1.cmd("sudo python Httpserver.py 80 &")
        self.ws2.cmd("sudo python Httpserver2.py 80 &")
        self.ws3.cmd("sudo python Httpserver3.py 80 &")
        self.insp.cmd("tcpdump -i eth0 -w insp.cap &")
        time.sleep(5)

        print 'TCP Testing (Only port 80)'
        print '(SRC -> DST Port X) Success!/Failed!'
        
        print 'H1 -> Web Port 80 method POST',
        t1 = self.h1.cmd('curl --max-time 5 -d "foo=bar&bin=baz" http://100.0.0.45:80')
        if self._parseWget(t1):
            print 'Success!'
        else:
            print 'Failed!'

        print 'H1 -> Web Port 22 method POST',
        t2 = self.h1.cmd('curl --max-time 5 -d "foo=bar&bin=baz" http://100.0.0.45:22')
        if self._parseWget(t2):
            print 'Success!'
        else:
            print 'Failed!'
            
        print 'H1 -> Web Port 53 method POST',
        t3 = self.h1.cmd('curl --max-time 5 -d "foo=bar&bin=baz" http://100.0.0.45:53')
        if self._parseWget(t3):
            print 'Success!'
        else:
            print 'Failed!'
            
        print 'H1 -> Web Port 88 method POST',
        t4 = self.h1.cmd('curl --max-time 5 -d "foo=bar&bin=baz" http://100.0.0.45:88')
        if self._parseWget(t4):
            print 'Success!'
        else:
            print 'Failed!'
            
        print 'H1 -> Web Port 115 method POST',
        t5 = self.h1.cmd('curl --max-time 5 -d "foo=bar&bin=baz" http://100.0.0.45:115')
        if self._parseWget(t5):
            print 'Success!'
        else:
            print 'Failed!'
            
        print 'H1 -> Web Port 123  method POST',
        t6 = self.h1.cmd('curl --max-time 5 -d "foo=bar&bin=baz" http://100.0.0.45:123')
        if self._parseWget(t6):
            print 'Success!'
        else:
            print 'Failed!'
            
        print 'H1 -> Web Port 156  method POST',
        t7 = self.h1.cmd('curl --max-time 5 -d "foo=bar&bin=baz" http://100.0.0.45:156')
        if self._parseWget(t7):
            print 'Success!'
        else:
            print 'Failed!'
            
        print 'H1 -> Web Port 199 method POST',
        t8 = self.h1.cmd('curl --max-time 5 -d "foo=bar&bin=baz" http://100.0.0.45:199')
        if self._parseWget(t8):
            print 'Success!'
        else:
            print 'Failed!'
            
        print 'H1 -> Web Port 220 method POST',
        t9 = self.h1.cmd('curl --max-time 5 -d "foo=bar&bin=baz" http://100.0.0.45:220')
        if self._parseWget(t9):
            print 'Success!'
        else:
            print 'Failed!'
            
        print 'H1 -> Web Port 443 method POST',
        t10 = self.h1.cmd('curl --max-time 5 -d "foo=bar&bin=baz" http://100.0.0.45:443')
        if self._parseWget(t10):
            print 'Success!'
        else:
            print 'Failed!'
        
        print 'H3 -> Web Port 80 method POST',
        t11 = self.h3.cmd('curl --max-time 5 -d "foo=bar&bin=baz" http://100.0.0.45:80')
        if self._parseWget(t11):
            print 'Success!'
        else:
            print 'Failed!'

        print 'H3 -> Web Port 22 method POST',
        t12 = self.h3.cmd('curl --max-time 5 -d "foo=bar&bin=baz" http://100.0.0.45:22')
        if self._parseWget(t12):
            print 'Success!'
        else:
            print 'Failed!'
            
        print 'H3 -> Web Port 53 method POST',
        t13 = self.h3.cmd('curl --max-time 5 -d "foo=bar&bin=baz" http://100.0.0.45:53')
        if self._parseWget(t13):
            print 'Success!'
        else:
            print 'Failed!'
            
        print 'H3 -> Web Port 88 method POST',
        t14 = self.h3.cmd('curl --max-time 5 -d "foo=bar&bin=baz" http://100.0.0.45:88')
        if self._parseWget(t14):
            print 'Success!'
        else:
            print 'Failed!'
            
        print 'H3 -> Web Port 115 method POST',
        t15 = self.h3.cmd('curl --max-time 5 -d "foo=bar&bin=baz" http://100.0.0.45:115')
        if self._parseWget(t15):
            print 'Success!'
        else:
            print 'Failed!'
            
        print 'H3 -> Web Port 123 method POST',
        t16 = self.h3.cmd('curl --max-time 5 -d "foo=bar&bin=baz" http://100.0.0.45:123')
        if self._parseWget(t16):
            print 'Success!'
        else:
            print 'Failed!'
            
        print 'H3 -> Web Port 156 method POST',
        t17 = self.h3.cmd('curl --max-time 5 -d "foo=bar&bin=baz" http://100.0.0.45:156')
        if self._parseWget(t17):
            print 'Success!'
        else:
            print 'Failed!'
            
        print 'H3 -> Web Port 199 method POST',
        t18 = self.h3.cmd('curl --max-time 5 -d "foo=bar&bin=baz" http://100.0.0.45:199')
        if self._parseWget(t18):
            print 'Success!'
        else:
            print 'Failed!'
            
        print 'H3 -> Web Port 220 method POST',
        t19 = self.h3.cmd('curl --max-time 5 -d "foo=bar&bin=baz" http://100.0.0.45:220')
        if self._parseWget(t19):
            print 'Success!'
        else:
            print 'Failed!'
            
        print 'H3 -> Web Port 443 method POST',
        t20 = self.h3.cmd('curl --max-time 5 -d "foo=bar&bin=baz" http://100.0.0.45:443')
        if self._parseWget(t20):
            print 'Success!'
        else:
            print 'Failed!'

        print 'H1 -> Web Port 80 method GET',
        t21 = self.h1.cmd('curl --max-time 5 http://100.0.0.45:80')
        if self._parseWget(t21):
            print 'Success!'
        else:
            print 'Failed!'

        print 'H1 -> Web Port 80 method HEAD',
        t22 = self.h1.cmd('curl --max-time -I 5 http://100.0.0.45:80')
        if self._parseWget(t22):
            print 'Success!'
        else:
            print 'Failed!'

        print 'H3 -> Web Port 80 method GET',
        t23 = self.h3.cmd('curl --max-time 5 http://100.0.0.45:80')
        if self._parseWget(t23):
            print 'Success!'
        else:
            print 'Failed!'

        print 'H3 -> Web Port 80 method HEAD',
        t24 = self.h3.cmd('curl --max-time -I 5 http://100.0.0.45:80')
        if self._parseWget(t24):
            print 'Success!'
        else:
            print 'Failed!'
            
        print "DNS Tests Done!"
        
        x=0
        
        if self._parseWget(t1):
           x=x+1
           self.count(True)
        if self._parseWget(t2):
           x=x+1
           self.count(True)
        if self._parseWget(t3):
           x=x+1
           self.count(True)
        if self._parseWget(t4):
           x=x+1
           self.count(True)
        if self._parseWget(t5):
           x=x+1
           self.count(True)
        if self._parseWget(t6):
           x=x+1
           self.count(True)
        if self._parseWget(t7):
           x=x+1
           self.count(True)
        if self._parseWget(t8):
           x=x+1
           self.count(True)
        if self._parseWget(t9):
           x=x+1
           self.count(True)
        if self._parseWget(t10):
           x=x+1
           self.count(True)
        if self._parseWget(t11):
           x=x+1
           self.count(True)
        if self._parseWget(t12):
           x=x+1
           self.count(True)
        if self._parseWget(t13):
           x=x+1
           self.count(True)
        if self._parseWget(t14):
           x=x+1
           self.count(True)
        if self._parseWget(t15):
           x=x+1
           self.count(True)
        if self._parseWget(t16):
           x=x+1
           self.count(True)
        if self._parseWget(t17):
           x=x+1
           self.count(True)
        if self._parseWget(t18):
           x=x+1
           self.count(True)
        if self._parseWget(t19):
           x=x+1
           self.count(True)
        if self._parseWget(t20):
           x=x+1
           self.count(True)
        if self._parseWget(t21):
           x=x+1
           self.count(True)
        if self._parseWget(t22):
           x=x+1
           self.count(True)
        if self._parseWget(t23):
           x=x+1
           self.count(True)
        if self._parseWget(t24):
           x=x+1
           self.count(True)
    
        print "Succes rate: " + str(x)+"/24"
        print "Expected rate: 2/24"     
        self.ws1.cmd('kill %python')
        self.ws2.cmd('kill %python')
        self.ws3.cmd('kill %python')
        self.insp.cmd('kill %python')

    def dns(self):
        self.ds1.cmd('python dns_server.py 100.0.0.20 &')
        self.ds2.cmd('python dns_server.py 100.0.0.21 &')
        self.ds3.cmd('python dns_server.py 100.0.0.22 &')
        
        print 'DNS Testing (Only port 53)'
        print '(SRC -> DST Port X) Success!/Failed!'
        
        print 'H1 -> DNS Port 80 ',
        t1 = self.h1.cmd('dig -p 80 @100.0.0.25 team4.ik2220.com')
        if self._parseDig(t1):
            print 'Success!'
        else:
            print 'Failed!'

        print 'H1 -> DNS Port 22 ',
        t2 = self.h1.cmd('dig -p 22 @100.0.0.25 team4.ik2220.com')
        if self._parseDig(t2):
            print 'Success!'
        else:
            print 'Failed!'
            
        print 'H1 -> DNS Port 53 ',
        t3 = self.h1.cmd('dig -p 53 @100.0.0.25 team4.ik2220.com')
        if self._parseDig(t3):
            print 'Success!'
        else:
            print 'Failed!'
            
        print 'H1 -> DNS Port 88 ',
        t4 = self.h1.cmd('dig -p 88 @100.0.0.25 team4.ik2220.com')
        if self._parseDig(t4):
            print 'Success!'
        else:
            print 'Failed!'
            
        print 'H1 -> DNS Port 115 ',
        t5 = self.h1.cmd('dig -p 115 @100.0.0.25 team4.ik2220.com')
        if self._parseDig(t5):
            print 'Success!'
        else:
            print 'Failed!'
            
        print 'H1 -> DNS Port 123 ',
        t6 = self.h1.cmd('dig -p 123 @100.0.0.25 team4.ik2220.com')
        if self._parseDig(t6):
            print 'Success!'
        else:
            print 'Failed!'
            
        print 'H1 -> DNS Port 156 ',
        t7 = self.h1.cmd('dig -p 156 @100.0.0.25 team4.ik2220.com')
        if self._parseDig(t7):
            print 'Success!'
        else:
            print 'Failed!'
            
        print 'H1 -> DNS Port 199 ',
        t8 = self.h1.cmd('dig -p 199 @100.0.0.25 team4.ik2220.com')
        if self._parseDig(t8):
            print 'Success!'
        else:
            print 'Failed!'
            
        print 'H1 -> DNS Port 220 ',
        t9 = self.h1.cmd('dig -p 220 @100.0.0.25 team4.ik2220.com')
        if self._parseDig(t9):
            print 'Success!'
        else:
            print 'Failed!'
            
        print 'H1 -> DNS Port 443 ',
        t10 = self.h1.cmd('dig -p 443 @100.0.0.25 team4.ik2220.com')
        if self._parseDig(t10):
            print 'Success!'
        else:
            print 'Failed!'
        
        print 'H3 -> DNS Port 80 ',
        t11 = self.h3.cmd('dig -p 80 @100.0.0.25 team4.ik2220.com')
        if self._parseDig(t11):
            print 'Success!'
        else:
            print 'Failed!'

        print 'H3 -> DNS Port 22 ',
        t12 = self.h3.cmd('dig -p 22 @100.0.0.25 team4.ik2220.com')
        if self._parseDig(t12):
            print 'Success!'
        else:
            print 'Failed!'
            
        print 'H3 -> DNS Port 53 ',
        t13 = self.h3.cmd('dig -p 53 @100.0.0.25 team4.ik2220.com')
        if self._parseDig(t13):
            print 'Success!'
        else:
            print 'Failed!'
            
        print 'H3 -> DNS Port 88 ',
        t14 = self.h3.cmd('dig -p 88 @100.0.0.25 team4.ik2220.com')
        if self._parseDig(t14):
            print 'Success!'
        else:
            print 'Failed!'
            
        print 'H3 -> DNS Port 115 ',
        t15 = self.h3.cmd('dig -p 115 @100.0.0.25 team4.ik2220.com')
        if self._parseDig(t15):
            print 'Success!'
        else:
            print 'Failed!'
            
        print 'H3 -> DNS Port 123 ',
        t16 = self.h3.cmd('dig -p 123 @100.0.0.25 team4.ik2220.com')
        if self._parseDig(t16):
            print 'Success!'
        else:
            print 'Failed!'
            
        print 'H3 -> DNS Port 156 ',
        t17 = self.h3.cmd('dig -p 156 @100.0.0.25 team4.ik2220.com')
        if self._parseDig(t17):
            print 'Success!'
        else:
            print 'Failed!'
            
        print 'H3 -> DNS Port 199 ',
        t18 = self.h3.cmd('dig -p 199 @100.0.0.25 team4.ik2220.com')
        if self._parseDig(t18):
            print 'Success!'
        else:
            print 'Failed!'
            
        print 'H3 -> DNS Port 220 ',
        t19 = self.h3.cmd('dig -p 220 @100.0.0.25 team4.ik2220.com')
        if self._parseDig(t19):
            print 'Success!'
        else:
            print 'Failed!'
            
        print 'H3 -> DNS Port 443 ',
        t20 = self.h3.cmd('dig -p 443 @100.0.0.25 team4.ik2220.com')
        if self._parseDig(t20):
            print 'Success!'
        else:
            print 'Failed!'
            
        print "DNS Tests Done!"

        print "Calculating Success Rate"
        x = 0
        
        if self._parseDig(t1):
            x = x+1
            self.count(True)
        if self._parseDig(t2):
            x = x+1
            self.count(True)
        if self._parseDig(t3):
            x = x+1
            self.count(True)
        if self._parseDig(t4):
            x = x+1
            self.count(True)
        if self._parseDig(t5):
            x = x+1
            self.count(True)
        if self._parseDig(t6):
            x = x+1
            self.count(True)
        if self._parseDig(t7):
            x = x+1
            self.count(True)
        if self._parseDig(t8):
            x = x+1
            self.count(True)
        if self._parseDig(t9):
            x = x+1
            self.count(True)
        if self._parseDig(t10):
            x = x+1
            self.count(True)
        if self._parseDig(t11):
            x = x+1
            self.count(True)
        if self._parseDig(t12):
            x = x+1
            self.count(True)
        if self._parseDig(t13):
            x = x+1
            self.count(True)
        if self._parseDig(t14):
            x = x+1
            self.count(True)
        if self._parseDig(t15):
            x = x+1
            self.count(True)
        if self._parseDig(t16):
            x = x+1
            self.count(True)
        if self._parseDig(t17):
            x = x+1
            self.count(True)
        if self._parseDig(t18):
            x = x+1
            self.count(True)
        if self._parseDig(t19):
            x = x+1
            self.count(True)
        if self._parseDig(t20):
            x = x+1
            self.count(True)

        print "Succes rate: " + str(x)+"/20"
        print "Expected rate: 2/20"     
        self.ds1.cmd('kill %python')
        self.ds2.cmd('kill %python')
        self.ds3.cmd('kill %python')
    
    def test(self):
        
        #self.file.write("ICMP TEST (pingall mininet)\n")
        self.ping()
        
        #self.file.write('\n\n\n\n')
        #self.file.write("DNS TEST (Testing 10 different ports from PbZ & PrZ")
        self.dns()
        
        #self.file.write('\n\n\n\n')
        #self.file.write("TCP TEST (Testing 10 different ports from PbZ & PrZ")
        self.http()
        
        psuccess=100*self.success/self.total
        
        #self.file.write('\n\n')
        #self.file.write("Total Success Rate:"+str(psuccess)+"%")


        #self.file.close()
        return psuccess
