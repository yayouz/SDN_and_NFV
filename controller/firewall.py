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
        
    def add_flow(self,event,outport):
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(event.parsed,event.port)
        msg.actions.append(of.ofp_action_output(port=outport))
        msg.idle_timeout = 2
        msg.data = event.ofp
        msg.flags = of.OFPFF_SEND_FLOW_REM
        self.connection.send(msg)
        
    def _handle_PacketIn(self,event):
        """Define PacketIn Logic Here"""
        packet = event.parsed
        
        if packet.find('arp') is not None:
            self.parent._handle_PacketIn(event)
        
        ipv4 = packet.find('ipv4')
        if ipv4 is not None:
            icmp = packet.find('icmp')
            dst_ip = str(ipv4.dstip)
            src_ip = str(ipv4.srcip)
            if icmp is not None:
                if not(
                    dst_ip in "100.0.0.20"
                    or dst_ip in "100.0.0.21"
                    or dst_ip in "100.0.0.22"
                    or dst_ip in "100.0.0.40"
                    or dst_ip in "100.0.0.41"
                    or dst_ip in "100.0.0.42"
                    ):
                    
                    if event.port == 1:
                        self.add_flow(event, 2)
                    else:
                        self.add_flow(event,1)
                    if icmp.type == ICMP_ECHO:
                        self.add_state((ICMP,src_ip,dst_ip,-1,-1))
                    
            elif packet.find('udp') is not None:
                udp = packet.find('udp')
                dst_port = str(udp.dstport)
                
                """Traffic Towards DNS servers"""
                if(
                    
                        (dst_ip in "100.0.0.20"
                         or dst_ip in "100.0.0.21"
                         or dst_ip in "100.0.0.22")
                     and 
                        dst_port in "53"):
                    
                    if event.port == 1:
                        self.add_flow(event, 2)
                    else:
                        self.add_flow(event,1)
                    self.add_state((TCP,src_ip,dst_ip,-1,dst_port))
                    
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
                    ):
                    
                    if event.port == 1:
                        self.add_flow(event, 2)
                    else:
                        self.add_flow(event,1)
                    self.add_state((TCP,src_ip,dst_ip,-1,dst_port))
                    
                else:
                    print(dst_ip + " " + dst_port + " TCP Unacceptable Dropped!")

    def _handle_FlowRemoved(self,event):
        for state in self.get_state():
            
            protocol,src_ip,dst_ip,src_port,dst_port = state
            
            #ICMP
            if(
                ICMP == int(event.ofp.match.nw_proto)
                and src_ip in str(event.ofp.match.nw_src)
                and dst_ip in str(event.ofp.match.nw_dst)
                ):
                self.remove_state(state)
                break
            #UDP
            elif(
                UDP == int(event.ofp.match.nw_proto)
                and src_ip in str(event.ofp.match.nw_src)
                and dst_ip in str(event.ofp.match.nw_dst)
                ):
                self.remove_state(state)
                break
            #TCP
            elif(
                TCP == int(event.ofp.match.nw_proto)
                and src_ip in str(event.ofp.match.nw_src)
                and dst_ip in str(event.ofp.match.nw_dst)
                ):
                self.remove_state(state)
                break
    
class firewall1(firewall):
    def __init__(self,connection,transparent):
        super(firewall1,self).__init__(connection, transparent)
        
    def get_state(self):
        return self.state
   
    def add_state(self,A):
        self.state.append(A)
        
    def _handle_PacketIn(self, event):
        packet = event.parsed
        ipv4 = packet.find('ipv4')
        
        """Allow Parent to handle MAC-learning"""
        if packet.find('arp') is not None:
            self.parent._handle_PacketIn(event)
        
        if ipv4 is not None:
            src_ip = str(ipv4.srcip)
            dst_ip = str(ipv4.dstip)
            icmp = packet.find('icmp')
            udp = packet.find('udp')
            tcp = packet.find('tcp')

            if icmp is not None:
                firewall._handle_PacketIn(self,event)
            elif udp is not None:
                port = str(udp.dstport)
                if (UDP,dst_ip,src_ip,-1,port) in self.state:
                    self.add_flow(event,2)
                else:
                    firewall._handle_PacketIn(self,event)
            elif tcp is not None:
                port = str(tcp.dstport)
                if (TCP,dst_ip,src_ip,-1,port) in self.state:
                    self.add_flow(event,2)
                else:
                    firewall._handle_PacketIn(self,event)

class firewall2(firewall):       
    def __init__(self,connection,transparent):
        super(firewall2,self).__init__(connection, transparent)
        
    def get_state(self):
        return self.state
   
    def add_state(self,A):
        self.state.append(A)

    def _handle_PacketIn(self, event):
        packet = event.parsed

        ipv4 = packet.find('ipv4')
        
        """Allow Parent to handle MAC-learning"""
        if packet.find('arp') is not None:
            self.parent._handle_PacketIn(event)
        
        elif ipv4 is not None:
            src_ip = str(ipv4.srcip)
            dst_ip = str(ipv4.dstip)
            icmp = packet.find('icmp')
            udp = packet.find('udp')
            tcp = packet.find('tcp')

            if icmp is not None:
                if (    (ICMP,dst_ip,src_ip,-1,-1) in self.state
                    and
                        icmp.type == ICMP_REPLY
                    ):
                    self.add_flow(event, 2)
                else:
                    firewall._handle_PacketIn(self,event)
            elif udp is not None:
                port = str(udp.dstport)
                if (UDP,dst_ip,src_ip,-1,port) in self.state:
                    self.add_flow(event,2)
                else:
                    firewall._handle_PacketIn(self,event)
            elif tcp is not None:
                port = str(tcp.dstport)
                if (TCP,dst_ip,src_ip,-1,port) in self.state:
                    self.add_flow(event,2)
                else:
                    firewall._handle_PacketIn(self,event)
