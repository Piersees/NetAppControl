"""Need to be run with Admin right"""

import Interfaces

#Those two lines will take out the errors generated by scapy like the message : WARNING: No route found for IPv6 destination :: (no default route?)
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

#Then you import scapy
from scapy.all import *


def GetPacketStats(nic):

    # Mettre la variable Nic accessible depuis Mine1.py ici
    interfaces = Interfaces.GetInterfaces(nic)

    # Description du nom de la carte wifi
    conf.iface = interfaces

    pkt = []

    #Initialisation des compteurs
    packet_type_cpt = {}

    packet_type_cpt["ALL"] = 0
    packet_type_cpt["TCP"] = 0
    packet_type_cpt["UDP"] = 0
    packet_type_cpt["ARP"] = 0
    packet_type_cpt["ICMP"] = 0
    packet_type_cpt["HTTP"] = 0
    packet_type_cpt["HTTPS"] = 0
    packet_type_cpt["DNS"] = 0
    packet_type_cpt["NBNS"] = 0
    #packet_type_cpt["SSL"] = 0
    #packet_type_cpt["QUIC"] = 0
    packet_type_cpt["LLMNR"] = 0

    packet_type_cpt["OTHER"] = 0


    def packet_cpt_callback(pkt):
        #pkt.show()
        packet_type_cpt["ALL"] = packet_type_cpt["ALL"] + 1

        if (TCP in pkt):
            packet_type_cpt["TCP"] = packet_type_cpt["TCP"] + 1

            if (pkt[TCP].dport == 80 or pkt[TCP].sport == 80):
                packet_type_cpt["HTTP"] = packet_type_cpt["HTTP"] + 1

            if (pkt[TCP].dport == 443 or pkt[TCP].sport == 443):
                packet_type_cpt["HTTPS"] = packet_type_cpt["HTTPS"] + 1

            if (pkt[TCP].dport == 5355 or pkt[TCP].sport == 5355):
               packet_type_cpt["LLMNR"] = packet_type_cpt["LLMNR"] + 1

            if (DNS in pkt):
                packet_type_cpt["DNS"] = packet_type_cpt["DNS"] + 1

            if (pkt[TCP].dport == 137 or pkt[TCP].sport == 137):
                packet_type_cpt["NBNS"] = packet_type_cpt["NBNS"] + 1


        elif (UDP in pkt):
            packet_type_cpt["UDP"] = packet_type_cpt["UDP"] + 1

            if (pkt[UDP].dport == 5355 or pkt[UDP].sport == 5355):
               packet_type_cpt["LLMNR"] = packet_type_cpt["LLMNR"] + 1

            if (DNS in pkt):
                packet_type_cpt["DNS"] = packet_type_cpt["DNS"] + 1

            if (pkt[UDP].dport == 80 or pkt[UDP].sport == 80):
                packet_type_cpt["HTTP"] = packet_type_cpt["HTTP"] + 1

            if (pkt[UDP].dport == 443 or pkt[UDP].sport == 443):
                packet_type_cpt["HTTPS"] = packet_type_cpt["HTTPS"] + 1

            if (pkt[UDP].dport == 137 or pkt[UDP].sport == 137):
                packet_type_cpt["NBNS"] = packet_type_cpt["NBNS"] + 1


        elif (ARP in pkt):
            packet_type_cpt["ARP"] = packet_type_cpt["ARP"] + 1

        elif (ICMP in pkt):
            packet_type_cpt["ICMP"] = packet_type_cpt["ICMP"] + 1

        else:
            packet_type_cpt["OTHER"] = packet_type_cpt["OTHER"] + 1


    #Sniff fonction: sniff 10 packets and for each call the fonciton packet_cpt_callback if there is no internet connection sniff will timeout after 20sec

    pkt = sniff(count=10, prn=packet_cpt_callback, timeout=20)


    #print("ALL:", packet_type_cpt["ALL"],"    TCP:", packet_type_cpt["TCP"],"     UDP:", packet_type_cpt["UDP"], "     ARP:", packet_type_cpt["ARP"], "     ICMP:", packet_type_cpt["ICMP"], "     HTTP:", packet_type_cpt["HTTP"], "     HTTPS:",      packet_type_cpt["HTTPS"],"     LLMNR:", packet_type_cpt["LLMNR"], "     DNS:", packet_type_cpt["DNS"],"     NBNS:", packet_type_cpt["NBNS"], "Autres:", packet_type_cpt["OTHER"])

    return packet_type_cpt


if __name__ =="__main__":
    GetPacketStats("Ethernet 3")
