# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 14:04:55 2018

@author: aitza
"""
############################################
#  Wifi info module, plugN'safe  #     ###########
#        """"""""""""""          #########
##############################################

import subprocess

def wifi_info():
    try:
        available = subprocess.check_output('netsh wlan show network mode=bssid',
                                        stderr=subprocess.STDOUT,universal_newlines=True,
                                        shell=True)

    except subprocess.CalledProcessError:
        return "Wifi disabled check" #return an error messag
    
    res = []
    res= available.split("\n")

    ssid_dic = {}


    actual = None
    for line in res:
        if ":" in line:
            res = line.split(" : ")
            for i in range(len(res)):
                res[i] = res[i].strip()
            
                if "SSID" in res[i] and "BSSID" not in res[i]:
                    actual = res[i]
                    ssid_dic[actual] = {}
                
                elif actual is not None:
                    ssid_dic[actual][res[0]] = res[1]
    return ssid_dic

if __name__ == "__main__":
    wifi_info()