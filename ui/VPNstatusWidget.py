# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'speedtest.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
sys.path.append("../Network")

class VPNstatusWidget(QWidget):

    def __init__(self, parent=None):

        super(VPNstatusWidget, self).__init__(parent)

        self.mainlayout = QHBoxLayout()
        self.setLayout(self.mainlayout)

        self.label = QLabel("VPN status:")
        self.mainlayout.addWidget(self.label)

        self.imgGreen = QPixmap('./images/vpngreen.png')
        self.imgRed = QPixmap('./images/vpnred.png')

        self.image = QLabel()
        self.image.setPixmap(self.imgRed)
        self.mainlayout.addWidget(self.image)

        self.secured = False

        self.setActive()

    def getStatus(self):
        return self.secured

    def setActive(self):
        self.secured = True
        self.image.setPixmap(self.imgGreen)

    def setInactive(self):
        self.secured = False
        self.image.setPixmap(self.imgRed)

    def toggleStatus(self):
        if self.secured is True:
            self.secured = False
            self.image.setPixmap(self.imgRed)
        else:
            self.secured = True
            self.image.setPixmap(self.imgGreen)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    appA = VPNstatusWidget()
    appA.show()
    sys.exit(app.exec_())
