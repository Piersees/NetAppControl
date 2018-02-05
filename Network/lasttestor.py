# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 15:26:25 2018

@author: aitza
"""
"""""""""""""""""""""""""""
" Scan Module, plugN'safe "
"   """"""""""""""""""    "
"""""""""""""""""""""""""""

#import nmap and socket
import nmap
import socket

def GetHostLan():
        
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Create a Socket
    
    s.connect(('google.com', 0)) #establish a connection
    
    
    ip = s.getsockname()[0] #get Ip address
    
    
    ns = nmap.PortScanner() #createz a nmap portScanner
    
    ns.scan(ip+'/24', arguments='-R -sn -PE -PR') #scan the network for connected hosts
    
    #print(ns._scan_result)
    
    #retrieve the hosts
    hosts_list = [(x, ns[x]['status']['state'],ns[x].hostname()) for x in ns.all_hosts()]
    
    #print(hosts_list)
    
    
    host_dict = {} #create a dict to store
    
    #get every hosts from the hosts list
    for nb,host in enumerate(hosts_list):
        #store it in the dictionary
        host_dict[host[0]] = { 'Hostname': host[2], 'Status': host[1]}
    #print(host_dict)
    return host_dict

if __name__ == "__main__":
    GetHostLan()
