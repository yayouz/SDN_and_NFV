InputRateEth1, InputRateEth2		:: AverageCounter;
OutputRateEth1, OutputRateEth2		:: AverageCounter;
ARPQueryEth1, ARPQueryEth2			:: Counter;
ARPResponderEth1, ARPResponderEth2	:: Counter;
ICMPCount, ServiceEth1, ServiceEth2	:: Counter;
DropEth1,DropEth2,DropIP1,DropIP2	:: Counter;


src_eth1 :: FromDevice($Name-eth1);
src_eth2 :: FromDevice($Name-eth2);

dst_eth1 :: Queue -> OutputRateEth1 -> ToDevice($Name-eth1);
dst_eth2 :: Queue -> OutputRateEth2 -> ToDevice($Name-eth2);

AddressInfo(Z1 $VIP/32 00:00:00:22:20:$MAC0);
AddressInfo(Z2 $VIP/32 00:00:00:22:20:$MAC1);

ARPQ_eth1 :: ARPQuerier(Z1) -> dst_eth1;
ARPQ_eth2 :: ARPQuerier(Z2) -> dst_eth2;

ARPR_eth1 :: ARPResponder($VIP/32 00:00:00:22:20:$MAC0) -> ARPResponderEth1 -> dst_eth1;
ARPR_eth2 :: ARPResponder($VIP/32 00:00:00:22:20:$MAC1) -> ARPResponderEth2 -> dst_eth2;

ETH_Z1 :: Classifier(12/0806 20/0001, 12/0806 20/0002, 12/0800,-);
ETH_Z2 :: Classifier(12/0806 20/0001, 12/0806 20/0002, 12/0800,-);

IP_Z1 :: IPClassifier(src $proto port $port,-)
IP_Z2 :: IPClassifier(icmp,dst $proto port $port,-)

SERVERS		:: RoundRobinIPMapper($VIP - $DIP0 - 0 1,$VIP - $DIP1 - 0 1,$VIP - $DIP2 - 0 1);
IP_RW 		:: IPRewriter(SERVERS, pattern $VIP 0-65535 - - 1 0);

PING :: ICMPPingResponder;



src_eth1 ->
			InputRateEth1 ->
			
			//Received a ARP Query
			ETH_Z2[0] ->
					ARPQueryEth1 ->
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
							ICMPCount ->
							ARPQ_eth1;
												
							
			//TCP or UDP, Rewrite to original source
					IP_Z2[1] ->
							IP_RW ->
							ServiceEth2 ->
							ARPQ_eth2;
						
			//Discard unimplemented IP packet processing
					IP_Z2[2] ->
						DropIP1 ->
						Discard;
						
			//Discard unimplemented Ethernet frame processing
			ETH_Z2[3] ->
					DropEth1 ->
					Discard;


src_eth2 ->
			InputRateEth2 ->
			
			//Received an ARP Query
			ETH_Z1[0] ->
					ARPQueryEth2 ->
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
							ServiceEth1 ->
							ARPQ_eth1;
						
			//Discard unimplemented IP packet processing
					IP_Z1[1] -> 
							DropIP2 ->
							Discard;
						
			//Discard unimplemented Ethernet frame processing
			ETH_Z1[3] ->
					DropEth2 ->
					Discard;
					
DriverManager(wait 1sec, print >$(Name).report "
=================== $Name Report ===================
Input Packet rate (pps):   	$(add $(InputRateEth1.rate) $(InputRateEth2.rate))
Output Packet rate (pps):  	$(add $(OutputRateEth1.rate) $(OutputRateEth2.rate))

Total # of input packets:  	$(add $(InputRateEth1.count) $(InputRateEth2.count))
Total # of output packets: 	$(add $(OutputRateEth1.count) $(OutputRateEth2.count))

Total # of ARP requests:	$(add $(ARPQueryEth1.count) $(ARPQueryEth2.count))
Total # of ARP responses: 	$(add $(ARPResponderEth1.count) $(ARPResponderEth2.count))

Total # of service packets:	$(add $(ServiceEth1.count) $(ServiceEth2.count))
Total # of ICMP packets: 	$(ICMPCount.count)
Total # of dropped packets:	$(add $(DropEth1.count) $(DropEth2.count) $(DropIP1.count) $(DropIP2.count))
==================================================", loop);
					