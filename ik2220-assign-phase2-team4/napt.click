//napt.click
AddressInfo(
	pri 10.0.0.1/24 2a:cb:0d:8e:25:51,
	pub 100.0.0.1/24 06:55:16:3d:1a:2d);
	
pri_device ::FromDevice(napt-eth2);
pub_device ::FromDevice(napt-eth1);
pri_class,pub_class :: Classifier(12/0800 /* IP packets */,
			      12/0806 20/0001 /* ARP requests */,
			       12/0806 20/0002 /*ARP response */,
			      - /* everything else */);
pri_arpq :: ARPQuerier(pri);//->Print(pri_arpq);
pub_arpq :: ARPQuerier(pub);//->Print(pub_arpq);

pri_arpr :: ARPResponder(pri);//->Print(pri_ARPR);
pub_arpr :: ARPResponder(pub);//->Print(pub_ARPR);

ICMP_rewr :: ICMPPingRewriter(pattern 100.0.0.1 - 0-65535# 0 1,drop);
IP_rewr :: IPRewriter(pattern 100.0.0.1 0-65535# - - 0 1, drop);

to_private ::Queue->Print(to_private)->ToDevice(napt-eth2);
to_public :: Queue->Print(to_public)->ToDevice(napt-eth1);

pri_device->Print(pri)->pri_class;
pri_class[0]
    ->Strip(14)
    -> CheckIPHeader
    ->pri_ip :: IPClassifier(icmp ,tcp or udp,-)
    ->[0]ICMP_rewr[0]
    ->pub_arpq
    //->Print(ICMPpri)
    //->ping :: ICMPPingResponder
    //->pub_q :: Queue
    ->to_public

   pri_ip[1]->[0]IP_rewr[0]->pub_arpq->to_public;
   pri_ip[2]->Discard;

pri_class[1]->pri_arpr->to_private;
pri_class[2]->[1]pri_arpq->to_private;
pri_class[3]->Discard;


pub_device->Print(pub)->pub_class;
pub_class[0]
    ->Strip(14)
    -> CheckIPHeader
    ->pub_ip :: IPClassifier(icmp ,tcp or udp,-)
    ->[1]ICMP_rewr[1]
     ->pri_arpq
     ->to_private;
     pub_ip[1]->[1]IP_rewr[1]->pri_arpq->to_private;
     pub_ip[2]->Discard;

pub_class[1]->pub_arpr->to_public;
pub_class[2]->[1]pub_arpq->to_public;
pub_class[3]->Discard;
