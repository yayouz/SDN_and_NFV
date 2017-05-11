src_eth1 :: FromDevice($Name-eth1);
src_eth2 :: FromDevice($Name-eth2);

dst_eth1 :: Queue -> ToDevice($Name-eth1);
dst_eth2 :: Queue -> ToDevice($Name-eth2);

AddressInfo(Z1 $VIP/24 00:00:00:22:20:$MAC0);
AddressInfo(Z2 $VIP/24 00:00:00:22:20:$MAC1);

ARPQ_eth1 :: ARPQuerier(Z1) -> dst_eth1;
ARPQ_eth2 :: ARPQuerier(Z2) -> dst_eth2;

ARPR_eth1 :: ARPResponder($VIP/24 00:00:00:22:20:$MAC0) -> dst_eth1;
ARPR_eth2 :: ARPResponder($VIP/24 00:00:00:22:20:$MAC1) -> dst_eth2;

ETH_Z1 :: Classifier(12/0806 20/0001, 12/0806 20/0002, 12/0800,-);
ETH_Z2 :: Classifier(12/0806 20/0001, 12/0806 20/0002, 12/0800,-);

IP_Z1 :: IPClassifier(src $proto port $port,-)
IP_Z2 :: IPClassifier(icmp,dst $proto port $port,-)

SERVERS		:: RoundRobinIPMapper($VIP - $DIP0 - 0 1,$VIP - $DIP1 - 0 1,$VIP - $DIP2 - 0 1);
IP_RW 		:: IPRewriter(SERVERS, pattern $VIP 0-65535 - - 1 0);

PING :: ICMPPingResponder;



src_eth1 ->

			//Received a ARP Query
			ETH_Z2[0] ->
					ARPR_eth1;
					
			//Received a ARP Response, Place in ARP table for MAC encapsulations
			ETH_Z2[1] -> 
					[1]ARPQ_eth1;
					
			//Received an IP Packet
			ETH_Z2[2] ->
					Strip(14) -> CheckIPHeader ->
					
			//ICMP packet, Respond
					IP_Z2[0] ->
							PING ->
							ARPQ_eth1;
												
							
			//TCP or UDP, Rewrite to original source
					IP_Z2[1] ->
							IP_RW ->
							ARPQ_eth2;
						
			//Discard unimplemented IP packet processing
					IP_Z2[2] ->
						Discard;
						
			//Discard unimplemented Ethernet frame processing
			ETH_Z2[3] ->
					Discard;



src_eth2 ->
		
			//Received an ARP Query
			ETH_Z1[0] ->
					ARPR_eth2;
					
			//Received an ARP Response, Place in ARP table for MAC encapsulations
			ETH_Z1[1] ->
					[1]ARPQ_eth2;
					
			//Received an IP Packet
			ETH_Z1[2] ->
					Strip(14) -> CheckIPHeader ->
						
			//TCP or UDP packet, Rewrite original source
					IP_Z1[0] ->
							[1]IP_RW[1] ->
							ARPQ_eth1;
						
			//Discard unimplemented IP packet processing
					IP_Z1[1] -> 
							Discard;
						
			//Discard unimplemented Ethernet frame processing
			ETH_Z1[3] ->
					Discard;
