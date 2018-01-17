# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 15:03:02 2018

@author: aitza
"""

import subprocess


hostname= "8.8.8.8"

try:
    
    print("test")
    response = subprocess.check_output(
        ['ping', '-n', '4', hostname],
        stderr=subprocess.STDOUT,  # get all output
        universal_newlines=True  # return string not bytes
        )

except subprocess.CalledProcessError:
    response = None

print (response)

#result_dick= response.dict()
