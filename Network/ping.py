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

hostname= "8.8.8.8" # determine the Ip to ping, like google.com

# subprocess try
try:
# ping commande
    response = subprocess.check_output(
        ['ping', '-n', '4', hostname],
        stderr=subprocess.STDOUT,  # get all output
        universal_newlines=True  # return string not bytes
        )

except subprocess.CalledProcessError:
    response = None

print (response)

#store ping as a list
datar= response.split(' ')

#delete unecessary infos
del datar[0:33]

#clean the list
datar= [x for x in datar if (x != '=' and x != '')] 
print (datar)

#create dictionary
ping_dict = {}
ping_dict['Sent'] = datar[2]
ping_dict['Received']= datar[4]
ping_dict['Lost']= datar[6]
ping_dict['averageRoundTripTime']= datar[-1]
ping_dict['maxRoundTripTIme']= datar[17]
ping_dict['min_round_trip_time']= datar[15]

print(ping_dict)
