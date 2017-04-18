from pox.core import core
import pox.openflow.libopenflow_01 as  of
from forwarding.l2_learning import LearningSwitch

class firewall(LearningSwitch):
    
    def __init__(self,connection,transparent):
        super(firewall,self).__init__(connection,transparent)
        self.state = []
        
    def _handle_PacketIn(self,event):
        #    super(firewall,self)._handle_PacketIn(event)
        """Define PacketIn Logic Here"""

class firewall1(firewall):
    def __init__(self,connection,transparent):
        super(firewall1,self).__init__(connection, transparent)


class firewall2(firewall):       
    def __init__(self,connection,transparent):
        super(firewall2,self).__init__(connection, transparent)
        
   
