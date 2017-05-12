InputRateEth1, InputRateEth2						:: AverageCounter;
OutputRateEth1, OutputRateEth2, OutputRateEth3		:: AverageCounter;
Blocked,HTTPCounter :: Counter;

src_eth1 :: FromDevice(ids-eth1);
src_eth2 :: FromDevice(ids-eth2);

dst_eth1 :: Queue -> OutputRateEth1 -> ToDevice(ids-eth1);
dst_eth2 :: Queue -> OutputRateEth2 -> ToDevice(ids-eth2);
dst_insp :: Queue -> OutputRateEth3 -> ToDevice(ids-eth3);

ETH_class :: Classifier(12/0800,-);
Ip_class :: IPClassifier(dst tcp www or https,-);//port 80 and tcp opt ack,-);
Http_class :: Classifier(66/505554,    //PUT
			 66/504F5354,  //POST
			 66/474554,    //GET
			 66/48454144,  //HEAD
			 66/4f5054494f4e53,//OPTIONS
			 66/5452414345, //TRACE
			 66/44454c455445,//DELETE
			 66/434f4e4e454354,//CONNECT
			 -);

src_eth1-> InputRateEth1 -> ETH_class;
  ETH_class[0]->CheckIPHeader(14)->Ip_class;
	Ip_class[0]->HTTPCounter->Http_class;
	        //PUT
		Http_class[0]->dst_eth2;
		//POST
		Http_class[1]->dst_eth2;
		//GET  HEAD OPTIONS TRACE DELETE CONNECT
		Http_class[2,3,4,5,6,7]-> Blocked ->dst_insp;
		//others
		Http_class[8]->dst_eth2;
	Ip_class[1]->dst_eth2;
  ETH_class[1]->dst_eth2;

src_eth2 -> InputRateEth2 ->dst_eth1;


DriverManager(wait 1sec, print >ids.report "
=================== $Name Report ===================
Input Packet rate (pps):   	$(add $(InputRateEth1.rate) $(InputRateEth2.rate))
Output Packet rate (pps):  	$(add $(OutputRateEth1.rate) $(OutputRateEth2.rate) $(OutputRateEth3.rate))

Blocked Packet rate (pps):	$(OutputRateEth3.rate)

Total # of input packets:  	$(add $(InputRateEth1.count) $(InputRateEth2.count))

Total # of HTTP packets:	$(HTTPCounter.count)

Total # of blocked packets:	$(Blocked.count)
Total # of allowed packets:	$(add $(OutputRateEth1.count) $(OutputRateEth2.count))
==================================================", loop);
