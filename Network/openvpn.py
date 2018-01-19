import os
import time
import win32file
import winreg as reg
import subprocess
from pathlib import Path
import shutil
from threading import Thread

def VPNConnect(OpenVpnPath,componentId,TcpConf):
    cmd = [OpenVpnPath,"--dev-node", componentId, "--config", TcpConf,"--route-noexec"]
    prog = subprocess.Popen(cmd,stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)

    time.sleep(0.1)
    prog.stdin.write(b"quentin.alazay@yahoo.fr")
    prog.stdin.flush()
    time.sleep(0.1)
    prog.stdin.write(b"Pfe2018.")
    prog.stdin.close()

    while True:
        line = prog.stdout.readline()
        print(line)
        if line == '' and prog.poll() is not None:
            break

def makeRoute():
    cmd = ["route", "-p", "add", "0.0.0.0", "mask", "128.0.0.0", "192.168.1.1", "metric", "1", "if", "18"]
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
                    #print(component_id +"       "+reg.QueryValueEx(adapter, 'NetCfgInstanceId')[0])
                    if component_id == 'tap0901':
                        key = reg.QueryValueEx(adapter, 'NetCfgInstanceId')[0]
#                        try:
#                            reg.QueryValueEx(adapter, "*NdisDeviceType")
#                            print("Exists")
#                        except:
#
#                            newKey = reg.CreateKey(reg.HKEY_LOCAL_MACHINE,ADAPTER_KEY+"\\"+key_name+"\\")
#                            print(reg.HKEY_LOCAL_MACHINE,ADAPTER_KEY+"\\"+key_name)
#                            reg.SetValueEx(newKey,"*NdisDeviceType", 0,  reg.REG_DWORD, 0x00000001)
#                            reg.CloseKey(newKey)
#                            print("key created")
                except :
                    pass
    except:
        pass

regConnection = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, ConnectionKey+"\\"+key+"\\Connection")
componentId = reg.QueryValueEx(regConnection, "name")[0]
print("RESULT: "+componentId)

if Path(ConfTcp).is_file() and Path(ConfUdp).is_file():
    TcpConf = ConfigPath + os.path.basename(ConfTcp)
    UdpConf = ConfigPath + os.path.basename(ConfUdp)
    if not Path(TcpConf).is_file():
        shutil.copy2(ConfTcp, TcpConf)
    if not Path().is_file():
        shutil.copy2(ConfUdp, UdpConf)

    thVPN = Thread(target=VPNConnect,args=(OpenVpnPath,componentId,TcpConf,))
    thVPN.start()
