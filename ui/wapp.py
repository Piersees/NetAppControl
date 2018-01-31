from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from appAbstract import appAbstract
import time
import sys
sys.path.append("../Network")
import inject

class WappWidget(appAbstract):

    def __init__(self, parent=None):

        super(WappWidget, self).__init__(parent)

        self.setStyleSheet("QPushButton{width:60px; height:60px;}")
        self.buttonNetwork.setIconSize(QSize(40,40))
        self.buttonSecurity.setIconSize(QSize(40,40))
        self.threadList = {}
        self.nic = None

    @pyqtSlot(str)
    def setProcessName(self, value):
        self.processName = value

    @pyqtSlot()
    def getProcessName(self):
        return self.processName

    @pyqtSlot(list)
    def setPIDlist(self, value):
        self.PID_list = value

    @pyqtSlot()
    def getPIDlist(self):
        return self.PID_list

    def colorSecurityButton(self, colored):
        if colored is True:
            self.buttonSecurity.setStyleSheet("width:60px; height:60px; background-color:rgb(135, 204, 78)")
        else:
            self.buttonSecurity.setStyleSheet("width:60px; height:60px")

    def setNic(self, nic):
        self.nic = nic

    def manageNetwork(self, durationType, durationTime, bandwidth, bandwidthType):
        ### TODO: regulate network
        pass

    def stopNetwork(self):
        ### TODO: stop network regulation
        pass

    def manageVPN(self, durationType, durationTime):
        if len(self.threadList) is not 0:
            self.colorSecurityButton(True)
            self.secured = True
            self.threadList = inject.ChangeProcessIp(self.PID_list, self.processName, self.nic)

    def stopVPN(self):
        ### TODO: stop VPN
        print("security stop")
        pass

    def clean(self):
        if len(self.threadList) is not 0:
            for key,thread in self.threadList.items():
                try:
                    thread.do_run = False
                except:
                    pass


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    wapp = WappWidget()
    wapp.show()
    sys.exit(app.exec_())
