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
                                        stderr=subprocess.STDOUT, universal_newlines=True,
                                        shell=True)

    except subprocess.CalledProcessError:
        print ("error")
        return "Wifi disabled check" #return an error messag
    
    res = []
    res= available.split("\n")

    ssid_dic = {}
    resoc=[]
    actual = None
    for lined in res:
        if ":" in lined:
            resoc = lined.replace("ÿ","").split(" : ")
            for i in range(len(resoc)):
                resoc[i] = resoc[i].strip()
                if "SSID" in resoc[i] and "BSSID" not in resoc[i]:
                    actual = resoc[i]
                    ssid_dic[actual] = []
                elif actual is not None and len(resoc)>=2 and resoc[1] not in ssid_dic[actual] and i+1 is len(resoc):
                    ssid_dic[actual].append(resoc[1])


    print(ssid_dic)
    return ssid_dic

if __name__ == "__main__":
    dic = wifi_info()
    for key in dic:
        print(dic[key])
        print("canal: " + dic[key][-3])
        percent = ""
        for i in dic[key]:
            if "%" in i:
                percent = i
        print("percentage: " + percent)