import psutil
import time

"""

Return the upload and download rate in Kilo Byte per sec for the classic interface

"""

def getBandWidth(nic):
    mesure = True
    presc_UL = 0
    presc_DL = 0

    if nic is not None:
        OpenVpnCard = nic
    else:
        OpenVpnCard = "Not_Defined"

    iostat = psutil.net_io_counters(pernic=True, nowrap=True)

    for index, item in enumerate(iostat.items()):
        if item[1][0]!= 0 and item[0] != OpenVpnCard:
            card = item[0]

    #print(iostat[card])


    while(mesure):

        presc_UL=iostat[card][0]
        presc_DL=iostat[card][1]

        iostat = psutil.net_io_counters(pernic=True, nowrap=True)

        for index, item in enumerate(iostat.items()):
            if item[1][0] != 0 and item[0] != OpenVpnCard:
                card = item[0]

        upload_rate = (iostat[card][0] - presc_UL)/1000
        download_rate = (iostat[card][1] - presc_DL)/1000

        #print("Download: ",download_rate,"KB/s","   ","Upload: ",upload_rate,"KB/s")
        return [download_rate, upload_rate]
        #time.sleep(1)

    #mesure = False     #Put mesure to False to stop the


"""

Return the upload and download rate in Kilo Byte per sec for the OpenVPN interface

"""

def getBandWidthVPN(nic):
    mesure = True
    presc_UL = 0
    presc_DL = 0

    if nic is not None:
        OpenVpnCard = nic
    else:
        return "The VPN is Off"

    iostat = psutil.net_io_counters(pernic=True, nowrap=True)

    for index, item in enumerate(iostat.items()):
        if item[1][0]!= 0 and item[0] == OpenVpnCard:
            card = item[0]
    #print(iostat)

    while(mesure):

        presc_UL=iostat[card][0]
        presc_DL=iostat[card][1]

        iostat = psutil.net_io_counters(pernic=True, nowrap=True)

        for index, item in enumerate(iostat.items()):
            if item[1][0] != 0 and item[0] == OpenVpnCard:
                card = item[0]

        upload_rate = (iostat[card][0] - presc_UL)/1000
        download_rate = (iostat[card][1] - presc_DL)/1000

        #print("Download: ",download_rate,"KB/s","   ","Upload: ",upload_rate,"KB/s")
        return [download_rate, upload_rate]
        #time.sleep(1)

"""

Return the difference in pourcentage between the use of the interface of OpenVPN and the classic interface

"""

def getBandWidthDiff(nic):
    mesure = True

    if nic is not None:
        OpenVpnCard = nic
    else:
        return "The VPN is Off"
    iostat = psutil.net_io_counters(pernic=True, nowrap=True)

    for item in iostat.items():
        if item[1][0]!= 0 and item[0] != OpenVpnCard:
            card = item[0]

    for item in iostat.items():
        if item[0] == OpenVpnCard:
            VpnCard = item[0]


    while(mesure):

        presc_UL=iostat[card][0]
        presc_DL=iostat[card][1]
        presc_UL_VPN=iostat[VpnCard][0]
        presc_DL_VPN=iostat[VpnCard][1]

        iostat = psutil.net_io_counters(pernic=True, nowrap=True)

        for index, item in enumerate(iostat.items()):
            if item[1][0] != 0 and item[0] != OpenVpnCard:
                card = item[0]

        for index, item in enumerate(iostat.items()):
            if item[1][0] != 0 and item[0] == OpenVpnCard:
                VpnCard = item[0]


        upload_rate = (iostat[card][0] - presc_UL)/1000
        download_rate = (iostat[card][1] - presc_DL)/1000
        upload_rate_VPN = (iostat[VpnCard][0] - presc_UL_VPN)/1000
        download_rate_VPN = (iostat[VpnCard][1] - presc_DL_VPN)/1000

        total = upload_rate + download_rate
        total_VPN = upload_rate_VPN + download_rate_VPN
        total_global = total + total_VPN

        if total_global == 0:
            diff = 0
        else:
            diff = total_VPN *100 / total_global

        #print("Pourcentage VPN used: ",diff,"%")
        return diff+'%%'
        #time.sleep(1)


if __name__ =="__main__":
    getBandWidthDiff("Ethernet")
