from pox.core import core
from pox.forwarding.l2_learning import LearningSwitch
from pox.lib.util import dpid_to_str
from firewall import firewall1, firewall2

log = core.getLogger()

class controller(object):
    def __init__(self):
        core.openflow.addListeners(self)
    
    def _handle_ConnectionUp(self,event):
        switch_id = dpid_to_str(event.dpid)

        #Switches
        if (
            #Switch 1
            switch_id in "00-00-00-00-00-01"
            #Switch 2
            or switch_id in "00-00-00-00-00-02"
            #Switch 3
            or switch_id in "00-00-00-00-00-03"
            #Switch 4
            or switch_id in "00-00-00-00-00-04"
            #Switch 5
            or switch_id in "00-00-00-00-00-05"
            #Load-balancer 1
            or switch_id in "00-00-00-00-00-0b"
            #Load-balancer 2
            or switch_id in "00-00-00-00-00-0c"
            #IDS
            or switch_id in "00-00-00-00-00-0d"
            #NAPT
            or switch_id in "00-00-00-00-00-1f"):
            
            LearningSwitch(event.connection,False)
            
        #Firewall 1
        elif switch_id in "00-00-00-00-00-15":
            firewall1(event.connection,False)
        #Firewall 2
        elif switch_id in "00-00-00-00-00-16":
            firewall2(event.connection,False)
        else:
            log.debug("Unknown Network Entity")

def launch():
    log.debug("Started")
    core.registerNew(controller)