import psutil
import time



def getBandWidth(self):
    mesure = True
    presc_UL = 0
    presc_DL = 0

    iostat = psutil.net_io_counters(pernic=False, nowrap=True)

    #print(iostat)

    while(mesure):

        presc_UL=iostat[0]
        presc_DL=iostat[1]

        iostat = psutil.net_io_counters(pernic=False, nowrap=True)

        upload_rate = (iostat[0] - presc_UL)/1000
        download_rate = (iostat[1] - presc_DL)/1000

        #print("Download: ",download_rate,"KB/s","   ","Upload: ",upload_rate,"KB/s")
        return [download_rate, upload_rate]
        #time.sleep(1)

    #mesure = False     #Put mesure to False to stop the
