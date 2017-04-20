from mininet.topo import Topo
from mininet.cli import CLI
from mininet.node import OVSSwitch
from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.log import setLogLevel, info
from testing import autotest
def int2dpid( dpid ):
      try:
        dpid = hex( dpid )[ 2: ]
        dpid = '0' * ( 16 - len( dpid ) ) + dpid
        return dpid
      except IndexError:
        raise Exception( 'Unable to derive default datapath ID - '
                       'please either specify a dpid or use a '
		       'canonical switch name such as s23.' )
class MyTopo( Topo ):
    "Simple topology example."
    

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        Host1 = self.addHost( 'h1',ip='100.0.0.11/24' )
        Host2 = self.addHost( 'h2',ip='100.0.0.12/24'  )
        Host3 = self.addHost( 'h3',ip='100.0.0.51/24'  )
        Host4 = self.addHost( 'h4',ip='100.0.0.52/24'  )
        DNS1 = self.addHost( 'ds1',ip='100.0.0.20/24' )
        DNS2 = self.addHost( 'ds2',ip='100.0.0.21/24' )
        DNS3 = self.addHost( 'ds3',ip='100.0.0.22/24' )
        Web1 = self.addHost( 'ws1',ip='100.0.0.40/24' )
        Web2 = self.addHost( 'ws2',ip='100.0.0.41/24')
        Web3 = self.addHost( 'ws3',ip='100.0.0.42/24' )
        Switch1 = self.addSwitch( 's1',dpid=int2dpid(1))
        Switch2 = self.addSwitch( 's2',dpid=int2dpid(2))
        Switch3 = self.addSwitch( 's3',dpid=int2dpid(3))
        Switch4 = self.addSwitch( 's4',dpid=int2dpid(4))
        Switch5 = self.addSwitch( 's5',dpid=int2dpid(5))
        lb1 = self.addSwitch( 'lb1',dpid=int2dpid(11))
        lb2 = self.addSwitch( 'lb2',dpid=int2dpid(12))
        ids = self.addSwitch( 'ids',dpid=int2dpid(13))
        Firewall1 = self.addSwitch( 'fw1',dpid=int2dpid(21))
        Firewall2 = self.addSwitch( 'fw2',dpid=int2dpid(22))
        napt = self.addSwitch( 'napt',dpid=int2dpid(31))

        # Add links
        self.addLink( Host1, Switch1 )
        self.addLink( Host2, Switch1 )
        self.addLink( Switch1, Firewall1 )
        self.addLink(Firewall1,Switch2)
        self.addLink(lb1,Switch2)
        self.addLink(ids,Switch2)
        self.addLink(Firewall2,Switch2)
        self.addLink(ids,lb2)
        self.addLink(lb2,Switch4)
        self.addLink(lb1,Switch3)
        self.addLink(Firewall2,napt)
        self.addLink(napt,Switch5)
        self.addLink(Host3,Switch5)
        self.addLink(Host4,Switch5)
        self.addLink(DNS1,Switch3)
        self.addLink(DNS2,Switch3)
        self.addLink(DNS3,Switch3)
        self.addLink(Web1,Switch4)
        self.addLink(Web2,Switch4)
        self.addLink(Web3,Switch4)

  

topos = { 'mytopo': ( lambda: MyTopo() ) }

def run():
  net=Mininet(topo=MyTopo(),controller=RemoteController('c0',ip='127.0.0.1',port=6633),switch=OVSSwitch)

  net.start()
  print "Testing network connectivity....."
  #fw1=net.get('fw1')
  #print ("the dpid of fw1 is"+fw1.dpid)
  h1=net.get('h1')
  result=h1.cmd('ping -c4 100.0.0.12')
  print result
  testing=autotest(net)
  psuccess= testing.test()
  print("***Result: %i%% correct transmition" % psuccess)
 # net.pingAll()
  CLI(net)
  net.stop()

if __name__=='__main__':
  setLogLevel('info')
  run()

