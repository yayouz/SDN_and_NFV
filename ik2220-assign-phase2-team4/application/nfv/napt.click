src_eth1 :: FromDevice(napt-eth1);
src_eth2 :: FromDevice(napt-eth2);

dst_eth1 :: Queue -> ToDevice(napt-eth1);
dst_eth2 :: Queue -> ToDevice(napt-eth2);

AddressInfo(PRZ 10.0.0.1/24 00:00:00:22:20:01);
AddressInfo(DMZ 100.0.0.1/24 00:00:00:22:20:02);

ARPQ_eth1 :: ARPQuerier(DMZ) -> dst_eth1;
ARPQ_eth2 :: ARPQuerier(PRZ) -> dst_eth2;

ARPR_eth1 :: ARPResponder(100.0.0.1/24 00:00:00:22:20:01) -> dst_eth1;
ARPR_eth2 :: ARPResponder(10.0.0.1/24 00:00:00:22:20:02) -> dst_eth2;

ETH_PRZ :: Classifier(12/0806 20/0001, 12/0806 20/0002, 12/0800,-);
ETH_DMZ :: Classifier(12/0806 20/0001, 12/0806 20/0002, 12/0800,-);

IP_PRZ :: IPClassifier(icmp,tcp or udp,-)
IP_DMZ :: IPClassifier(icmp,tcp or udp,-)

IP_RW 	:: IPRewriter(pattern 100.0.0.1 0-65535# - - 0 1, drop);
ICMP_RW 	:: ICMPPingRewriter(pattern 100.0.0.1 - 0-65535# 0 1, drop);

// Flow from Public Zone
src_eth1 ->

			//Received a ARP Query
			ETH_DMZ[0] ->
					ARPR_eth1;
					
			//Received a ARP Response, Place in ARP table for MAC encapsulations
			ETH_DMZ[1] -> 
					[1]ARPQ_eth1;
					
			//Received an IP Packet
			ETH_DMZ[2] ->
					Strip(14) -> CheckIPHeader ->
					
			//ICMP packet, Rewrite to original source
					IP_DMZ[0] ->
							[1]ICMP_RW[1] ->
							ARPQ_eth2;
							
			//TCP or UDP, Rewrite to original source
					IP_DMZ[1] ->
							[1]IP_RW[1] ->
							ARPQ_eth2;
						
			//Discard unimplemented IP packet processing
					IP_DMZ[2] ->
						Discard;
						
			//Discard unimplemented Ethernet frame processing
			ETH_DMZ[3] ->
					Discard;

// Flow from Private Zone
src_eth2 ->
		
			//Received an ARP Query
			ETH_PRZ[0] ->
					ARPR_eth2;
					
			//Received an ARP Response, Place in ARP table for MAC encapsulations
			ETH_PRZ[1] ->
					[1]ARPQ_eth2;
					
			//Received an IP Packet
			ETH_PRZ[2] ->
					Strip(14) -> CheckIPHeader ->
					
			//ICMP packet, Rewrite original source
					IP_PRZ[0] ->
							ICMP_RW ->
							ARPQ_eth1;
						
			//TCP or UDP packet, Rewrite original source
					IP_PRZ[1] ->
							IP_RW ->
							ARPQ_eth1;
						
			//Discard unimplemented IP packet processing
					IP_PRZ[2] -> 
							Discard;
						
			//Discard unimplemented Ethernet frame processing
			ETH_PRZ[3] ->
					Discard;
