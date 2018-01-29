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


    def manageNetwork(self, durationType, durationTime, bandwidth, bandwidthType):
        ### TODO: regulate network
        pass

    def manageVPN(self, durationType, durationTime):
        ### TODO: link with VPN
        pass


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    wapp = WappWidget()
    wapp.show()
    sys.exit(app.exec_())
