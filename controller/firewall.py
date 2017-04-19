from pox.core import core
import pox.openflow.libopenflow_01 as  of
from forwarding.l2_learning import LearningSwitch

ICMP_ECHO = 8
ICMP_REPLY = 0

ICMP = 1
TCP = 6
UDP = 14

class firewall(LearningSwitch):
    
    def __init__(self,connection,transparent):
        self.parent = super(firewall,self)
        self.parent.__init__(connection,transparent)
        self.state = []
        
    def get_state(self):
        return self.state
    
    def add_state(self,A):
        state.append(A)
        
    def remove_state(self,A):
        self.state.remove(A)
        
    def _handle_PacketIn(self,event):
        """Define PacketIn Logic Here"""
        packet = event.parsed
        
        if packet.find('arp') is not None:
            self.parent._handle_PacketIn(event)
        
        ipv4 = packet.find('ipv4')
        if ipv4 is not None:
            if packet.find('icmp') is not None:
                self.parent._handle_PacketIn(event)
            elif packet.find('udp') is not None:
                udp = packet.find('udp')
                dst_ip = str(ipv4.dstip)
                src_ip = str(ipv4.srcip)
                dst_port = str(udp.dstport)
                
                """Traffic Towards DNS servers"""
                if(
                    (
                        (dst_ip in "100.0.0.20"
                         or dst_ip in "100.0.0.21"
                         or dst_ip in "100.0.0.22")
                     and 
                        dst_port in "53")
                    or
                        (src_ip in "100.0.0.20"
                         or src_ip in "100.0.0.21"
                         or src_ip in "100.0.0.22")
                    ):
                    self.parent._handle_PacketIn(event)
                else:
                    print(dst_ip + " " + dst_port + " UDP Unacceptable Dropped!")
            elif packet.find('tcp') is not None:
                tcp = packet.find('tcp')
                dst_ip = str(ipv4.dstip)
                src_ip = str(ipv4.srcip)
                dst_port = str(tcp.dstport)
                
                """Traffic towards Web Servers"""
                if(
                    (
                        (dst_ip in "100.0.0.40"
                         or dst_ip in "100.0.0.41"
                         or dst_ip in "100.0.0.42")
                     and
                        dst_port in "80")
                    or
                        (src_ip in "100.0.0.40"
                         or src_ip in "100.0.0.41"
                         or src_ip in "100.0.0.42")
                    ):
                    self.parent._handlePacketIn(event)
                else:
                    print(dst_ip + " " + dst_port + " TCP Unacceptable Dropped!")

    def _handle_FlowRemoved(self,event):
        for state in self.get_state():
            
            protocol,src_ip,dst_ip,src_port,dst_port = state

            #ICMP
            if(
                ICMP == event.ofp.match.nw_proto
                and src_ip in str(event.ofp.match.nw_src)
                and dst_ip in str(event.ofp.match.nw_dst)
                ):
                self.remove_state(state)
            #UDP
            elif(
                UDP == event.ofp.match.nw_proto
                and src_ip in str(event.ofp.match.nw_src)
                and dst_ip in str(event.ofp.match.nw_dst)
                ):
                self.remove_state(state)
            #TCP
            elif(
                TCP == event.ofp.match.nw_proto
                and src_ip in str(event.ofp.match.nw_src)
                and dst_ip in str(event.ofp.match.nw_dst)
                ):
                self.remove_state(state)
            else:
                print(event.ofp)
    
class firewall1(firewall):
    def __init__(self,connection,transparent):
        self.parent = super(firewall1,self)
        self.parent.__init__(connection, transparent)
        
    def _handle_PacketIn(self, event):
        super(firewall1,self)._handle_PacketIn(event)

class firewall2(firewall):       
    def __init__(self,connection,transparent):
        self.parent = super(firewall2,self)
        self.parent.__init__(connection, transparent)
        
    def get_state(self):
        return self.state
    
    def add_state(self,A):
        self.state.append(A)

    def _handle_PacketIn(self, event):
        packet = event.parsed
        
        icmp = packet.find('icmp')
        udp = packet.find('udp')
        tcp = packet.find('tcp')
        ipv4 = packet.find('ipv4')
        
        """Allow Parent to handle MAC-learning"""
        if ipv4 is None:
            self.parent._handle_PacketIn(event)
        
        if ipv4 is not None:
            src_ip = str(ipv4.srcip)
            dst_ip = str(ipv4.dstip)

            if icmp is not None:
                
                if( 
                        icmp.type == ICMP_REPLY
                    and
                        (ICMP,dst_ip,src_ip,'*','*') in self.state
                    ):
                        self.add_state((ICMP,src_ip,dst_ip,'*','*'))
                        self.add_flow(event, 2)
                elif(
                        icmp.type == ICMP_ECHO
                    and
                        (src_ip in "100.0.0.51"
                         or src_ip in "100.0.0.52")
                     ):
                        self.add_state((ICMP,src_ip,dst_ip,'*','*'))
                        self.add_flow(event,1)
                else:
                    pass
            elif udp is not None:
                pass
            elif tcp is not None:
                pass
            else:
                pass
        
    def add_flow(self,event,outport):
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(event.parsed,event.port)
        msg.actions.append(of.ofp_action_output(port=outport))
        msg.idle_timeout = 2
        msg.data = event.ofp
        msg.flags = of.OFPFF_SEND_FLOW_REM
        self.connection.send(msg)
        
        
   
