import os
import time
import win32file
import winreg as reg
import subprocess
from pathlib import Path
import shutil
from threading import Thread
import credential

def VPNConnect(OpenVpnPath,componentId,TcpConf):
    cmd = [OpenVpnPath,"--dev-node", componentId, "--config", TcpConf,"--route-nopull"]
    prog = subprocess.Popen(cmd,stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)

    time.sleep(0.1)
    prog.stdin.write(credential.login['mail'])
    prog.stdin.flush()
    time.sleep(0.1)
    prog.stdin.write(credential.login['password'])
    prog.stdin.close()

    while True:
        line = prog.stdout.readline()
        print(line)
        if b'Initialization' in line:
            print("Makeroute called")
            makeRoute()
        if line == '' and prog.poll() is not None:
            break

def getGateway():
    return 1


def makeRoute():
    gateway = getGateway()
    cmd = ["route", "add", "0.0.0.0", "mask", "0.0.0.0", "10.7.7.1", "if", "19"]
    prog = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)

ADAPTER_KEY = r'SYSTEM\CurrentControlSet\Control\Class\{4D36E972-E325-11CE-BFC1-08002BE10318}'

OpenVpnPath = "C:\\Program Files\\OpenVPN\\bin\\openvpn.exe"
ConfigPath = os.environ['USERPROFILE']+"\\OpenVPN\\config"

ConfTcp= "C:\\Users\\quent\\Downloads\\ovpn\\ovpn_tcp\\uk298.nordvpn.com.tcp.ovpn"
ConfUdp= "C:\\Users\\quent\\Downloads\\ovpn\\ovpn_udp\\uk298.nordvpn.com.udp.ovpn"

ConnectionKey = "SYSTEM\\CurrentControlSet\\Control\\Network\\{4D36E972-E325-11CE-BFC1-08002BE10318}"

with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, ADAPTER_KEY) as adapters:
    try:
        for i in range(10000):
            key_name = reg.EnumKey(adapters, i)
            with reg.OpenKey(adapters, key_name) as adapter:
                try:
                    component_id = reg.QueryValueEx(adapter, 'ComponentId')[0]
                    if component_id == 'tap0901':
                        key = reg.QueryValueEx(adapter, 'NetCfgInstanceId')[0]
                except :
                    pass
    except:
        pass

regConnection = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, ConnectionKey+"\\"+key+"\\Connection")
componentId = reg.QueryValueEx(regConnection, "name")[0]
print("RESULT: "+component_id)

if Path(ConfTcp).is_file() and Path(ConfUdp).is_file():
    TcpConf = ConfigPath + os.path.basename(ConfTcp)
    UdpConf = ConfigPath + os.path.basename(ConfUdp)
    if not Path(TcpConf).is_file():
        shutil.copy2(ConfTcp, TcpConf)
    if not Path().is_file():
        shutil.copy2(ConfUdp, UdpConf)

    thVPN = Thread(target=VPNConnect,args=(OpenVpnPath,componentId,TcpConf,))
    thVPN.start()
