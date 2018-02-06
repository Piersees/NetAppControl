"""Need to be run with Admin right"""

import Interfaces

#Those two lines will take out the errors generated by scapy like the message : WARNING: No route found for IPv6 destination :: (no default route?)
import logging

import psutil

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
    packet_type_cpt["NetBIOS"] = 0
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

            if (pkt[TCP].dport == 137 or pkt[TCP].sport == 137 or pkt[TCP].dport == 138 or pkt[TCP].sport == 138 or pkt[TCP].dport == 139 or pkt[TCP].sport == 139):
                packet_type_cpt["NetBIOS"] = packet_type_cpt["NetBIOS"] + 1


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

            if (pkt[UDP].dport == 137 or pkt[UDP].sport == 137 or pkt[UDP].dport == 138 or pkt[UDP].sport == 138 or pkt[UDP].dport == 139 or pkt[UDP].sport == 139):
                packet_type_cpt["NetBIOS"] = packet_type_cpt["NetBIOS"] + 1


        elif (ARP in pkt):
            packet_type_cpt["ARP"] = packet_type_cpt["ARP"] + 1

        elif (ICMP in pkt):
            packet_type_cpt["ICMP"] = packet_type_cpt["ICMP"] + 1

        else:
            packet_type_cpt["OTHER"] = packet_type_cpt["OTHER"] + 1


    #Sniff fonction: sniff 10 packets and for each call the fonciton packet_cpt_callback if there is no internet connection sniff will timeout after 20sec

    pkt = sniff(count=10, prn=packet_cpt_callback, timeout=20)

    #print("ALL:", packet_type_cpt["ALL"],"    TCP:", packet_type_cpt["TCP"],"     UDP:", packet_type_cpt["UDP"], "     ARP:", packet_type_cpt["ARP"], "     ICMP:", packet_type_cpt["ICMP"], "     HTTP:", packet_type_cpt["HTTP"], "     HTTPS:",      packet_type_cpt["HTTPS"],"     LLMNR:", packet_type_cpt["LLMNR"], "     DNS:", packet_type_cpt["DNS"],"     NetBios:", packet_type_cpt["NetBIOS"], "Autres:", packet_type_cpt["OTHER"])


    return packet_type_cpt



def GetAppStats(nic):

    # Mettre la variable Nic accessible depuis Mine1.py ici
    interfaces = Interfaces.GetInterfaces(nic)

    # Description du nom de la carte wifi
    conf.iface = interfaces

    pkt = []

    appPorts = getPortsAppListWithInternet()

    global byte_app_cpt
    byte_app_cpt ={}

    for app in appPorts:
        byte_app_cpt[app]=0

    global pkt_cpt
    global total_len

    pkt_cpt = 0
    total_len = 0

    def packet_cpt_callback(pkt):

        global pkt_cpt
        global total_len

        pkt_cpt += 1

        try:
            if (TCP in pkt):
                for app in appPorts:
                    #print("App:",app)
                    for ports in appPorts[app]:
                        #print("Ports: ", ports)
                        if (pkt[TCP].dport == ports or pkt[TCP].sport == ports):
                            #print("App:",app," Ports:",ports," Lengh:",pkt[IP].len)
                            byte_app_cpt[app] = byte_app_cpt[app] + pkt[IP].len
                            total_len = total_len + pkt[IP].len

            elif (UDP in pkt):
                for app in appPorts:
                    #print("App:", app)
                    for ports in appPorts[app]:
                        #print("Ports: ", ports)
                        if (pkt[UDP].dport == ports or pkt[UDP].sport == ports):
                            #print("App:", app, " Ports:", ports, " Lengh:", pkt[IP].len)
                            byte_app_cpt[app] = byte_app_cpt[app] + pkt[IP].len
                            total_len = total_len + pkt[IP].len
        except:
            pass

    #Sniff fonction: sniff 10 packets and for each call the fonciton packet_cpt_callback if there is no internet connection sniff will timeout after 20sec
    pkt = sniff(count=100, prn=packet_cpt_callback,timeout=20)

    #print(pkt_cpt)
    #print(total_len)

    byte_app_pourcentage = {}

    for app in byte_app_cpt:
       byte_app_pourcentage[app] = byte_app_cpt[app]*100/total_len
       byte_app_pourcentage[app]=round(byte_app_pourcentage[app],2)

    return byte_app_pourcentage

def getPortsAppListWithInternet():
    dic = {}
    for proc in psutil.process_iter():
        try:
            if proc.connections():
                processConnections=proc.connections("inet4")
                ports = []

                if processConnections is not None:
                    for item in processConnections:
                        if item[3][1] == 80 or item[3][1] == 443 or item[3][1] == 5355:
                            print()
                        else:
                            ports.append(item[3][1])
                    dic[proc.name()] = ports

        except ( psutil.NoSuchProcess ):
            pass

    return dic


if __name__ =="__main__":
    GetPacketStats("Ethernet 3")
    #dic=getPortsAppListWithInternet()

    #byte_app_cpt=GetAppStats("Ethernet 3")
    #for app in byte_app_cpt:
    #    print(app," :",byte_app_cpt[app],"  Bytes")

