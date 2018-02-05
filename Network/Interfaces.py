
import winreg as reg
import psutil
import os


def GetInterfaces(nic):

    if nic is not None:
        OpenVpnCard = nic
    else:
        OpenVpnCard = "Not_Defined"

    iostat = psutil.net_io_counters(pernic=True, nowrap=True)

    for item in iostat.items():
        if item[1][0]!= 0 and item[0] != OpenVpnCard:
            card = item[0]

    ADAPTER_KEY = r'SYSTEM\CurrentControlSet\Control\Class\{4D36E972-E325-11CE-BFC1-08002BE10318}'

    ConnectionKey = "SYSTEM\\CurrentControlSet\\Control\\Network\\{4D36E972-E325-11CE-BFC1-08002BE10318}"

    interfaces = []

    with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, ADAPTER_KEY) as adapters:
        try:
            for i in range(10000):
                key_name = reg.EnumKey(adapters, i)
                with reg.OpenKey(adapters, key_name) as adapter:
                    try:
                        key = reg.QueryValueEx(adapter, 'NetCfgInstanceId')[0]
                        regConnection = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, ConnectionKey + "\\" + key + "\\Connection")
                        interfaces.append(reg.QueryValueEx(regConnection, "name")[0])
                    except:
                        pass
        except:
            pass

    for index,iface in enumerate(interfaces):
          if iface == card:
              CardNumber=index

    ADAPTER_KEY = r'SYSTEM\CurrentControlSet\Control\Class\{4D36E972-E325-11CE-BFC1-08002BE10318}'

    NetworkCard = []
    with reg.OpenKey(reg.HKEY_LOCAL_MACHINE, ADAPTER_KEY) as adapters:
        try:
            for i in range(10000):

                key_name = reg.EnumKey(adapters, i)
                with reg.OpenKey(adapters, key_name) as adapter:
                    try:
                        NetworkCard.append(reg.QueryValueEx(adapter, 'DriverDesc')[0])
                    except :
                        pass
        except:
            pass

    return NetworkCard[CardNumber]


if __name__ =="__main__":

  interfaces= GetInterfaces("Ethernet 3")

  print(interfaces)


