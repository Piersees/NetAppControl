import requests

def Get_IP():

    r = requests.get(r'http://jsonip.com')
    ip = r.json()['ip']
    return ip

