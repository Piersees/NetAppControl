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
import time

def orderByChannel(dic):
    res = {}
    print(dic)
    for key in dic:
        percent = ""
        canal = 0
        for i in dic[key]:
            if "%" in i:
                percent = i
            if i.isdigit():
                canal = i
        if "Channel "+str(canal) in res:
            res["Channel "+str(canal)] = res["Channel "+str(canal)][key.split(": ")[1]] = [canal,percent]
            pass
        else:
            res["Channel "+str(canal)] = {key.split(": ")[1]:[canal,percent]}

    return res

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

    return orderByChannel(ssid_dic)

if __name__ == "__main__":
    dic = {}
    while len(dic) <2:
        dic = wifi_info()
        print(dic)
        time.sleep(2)
    print(dic)

