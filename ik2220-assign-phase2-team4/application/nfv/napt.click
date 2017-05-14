InputRateEth1, InputRateEth2				:: AverageCounter;
OutputRateEth1, OutputRateEth2				:: AverageCounter;
ARPQueryEth1, ARPQueryEth2					:: Counter;
ARPResponderEth1, ARPResponderEth2			:: Counter;
ICMPPrz,ICMPDMZ, ServiceEth1, ServiceEth2	:: Counter;
DropEth1,DropEth2,DropIP1,DropIP2			:: Counter;

src_eth1 :: FromDevice(napt-eth1);
src_eth2 :: FromDevice(napt-eth2);

dst_eth1 :: Queue -> OutputRateEth1 -> ToDevice(napt-eth1);
dst_eth2 :: Queue -> OutputRateEth2 -> ToDevice(napt-eth2);

AddressInfo(PRZ 10.0.0.1/32 00:00:00:22:20:01);
AddressInfo(DMZ 100.0.0.1/32 00:00:00:22:20:02);

ARPQ_eth1 :: ARPQuerier(DMZ) -> dst_eth1;
ARPQ_eth2 :: ARPQuerier(PRZ) -> dst_eth2;

ARPR_eth1 :: ARPResponder(100.0.0.1/32 00:00:00:22:20:01) -> ARPResponderEth1 -> dst_eth1;
ARPR_eth2 :: ARPResponder(10.0.0.1/32 00:00:00:22:20:02) -> ARPResponderEth2 -> dst_eth2;

ETH_PRZ :: Classifier(12/0806 20/0001, 12/0806 20/0002, 12/0800,-);
ETH_DMZ :: Classifier(12/0806 20/0001, 12/0806 20/0002, 12/0800,-);

IP_PRZ :: IPClassifier(icmp,tcp or udp,-)
IP_DMZ :: IPClassifier(icmp,tcp or udp,-)

IP_RW 		:: IPRewriter(pattern 100.0.0.1 0-65535 - - 0 1, drop);
ICMP_RW 	:: ICMPPingRewriter(pattern 100.0.0.1 - 0-65535 0 1, drop);

// Flow from Public Zone
src_eth1 ->
			InputRateEth1 ->
			
			//Received a ARP Query
			ETH_DMZ[0] ->
					ARPQueryEth1 ->
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
							ICMPDMZ -> 
							ARPQ_eth2;
							
			//TCP or UDP, Rewrite to original source
					IP_DMZ[1] ->
							[1]IP_RW[1] ->
							ServiceEth2 ->
							ARPQ_eth2;
						
			//Discard unimplemented IP packet processing
					IP_DMZ[2] ->
						DropIP1 ->
						Discard;
						
			//Discard unimplemented Ethernet frame processing
			ETH_DMZ[3] ->
					DropEth1 ->
					Discard;

// Flow from Private Zone
src_eth2 ->
			InputRateEth2 ->
			
			//Received an ARP Query
			ETH_PRZ[0] ->
					ARPQueryEth2 ->
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
							ICMPPrz -> 
							ARPQ_eth1;
						
			//TCP or UDP packet, Rewrite original source
					IP_PRZ[1] ->
							IP_RW ->
							ServiceEth1 -> 
							ARPQ_eth1;
						
			//Discard unimplemented IP packet processing
					IP_PRZ[2] -> 
							DropIP2 ->
							Discard;
						
			//Discard unimplemented Ethernet frame processing
			ETH_PRZ[3] ->
					DropEth2 ->
					Discard;
					
DriverManager(wait 1sec, print >napt.report "
=================== $Name Report ===================
Input Packet rate (pps):   	$(add $(InputRateEth1.rate) $(InputRateEth2.rate))
Output Packet rate (pps):  	$(add $(OutputRateEth1.rate) $(OutputRateEth2.rate))

Total # of input packets:  	$(add $(InputRateEth1.count) $(InputRateEth2.count))
Total # of output packets: 	$(add $(OutputRateEth1.count) $(OutputRateEth2.count))

Total # of ARP requests:	$(add $(ARPQueryEth1.count) $(ARPQueryEth2.count))
Total # of ARP responses: 	$(add $(ARPResponderEth1.count) $(ARPResponderEth2.count))

Total # of service packets:	$(add $(ServiceEth1.count) $(ServiceEth2.count))
Total # of ICMP packets: 	$(add $(ICMPPrz.count) $(ICMPDMZ.count))
Total # of dropped packets:	$(add $(DropEth1.count) $(DropEth2.count) $(DropIP1.count) $(DropIP2.count))
==================================================", loop);
