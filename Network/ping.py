# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 15:03:02 2018

@author: aitza
"""
"""""""""""""""""""""""""""
" Ping Module, plugN'safe "
"   """"""""""""""""""    "
"""""""""""""""""""""""""""

# import subprocess to spawn a new process
import subprocess

def getPing():
    hostname= "8.8.8.8" # determine the Ip to ping, like google.com

    # subprocess try
    try:
    # ping commande
        response = subprocess.check_output(
            ['ping', '-n', '1', hostname],
            stderr=subprocess.STDOUT,  # get all output
            universal_newlines=True  # return string not bytes
            )

        #store ping as a list
        datar= response.split(' ')
        #delete unecessary infos
        del datar[0:15]

        #clean the list
        datar= [x for x in datar if (x != '=' and x != '')]

        #create dictionary
        ping_dict = {}
        ping_dict['Sent'] = datar[2]
        ping_dict['Received'] = datar[4]
        ping_dict['Lost']= datar[6]
        ping_dict['averageRoundTripTime']= datar[-1]
        ping_dict['maxRoundTripTime']= datar[17]
        ping_dict['min_round_trip_time']= datar[15]

        return ping_dict
        
    except subprocess.CalledProcessError:
        ping_dict = {}
        ping_dict['Sent'] = 1
        ping_dict['Received'] = 0
        ping_dict['Lost']= 1
        ping_dict['averageRoundTripTime']= 1000
        ping_dict['maxRoundTripTime']= 1000
        ping_dict['min_round_trip_time']= 1000
        return ping_dict

if __name__ == "__main__":
    getPing()
