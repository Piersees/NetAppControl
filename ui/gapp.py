from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from appAbstract import appAbstract
import time

class GappWidget(appAbstract):
    def __init__(self, parent=None):

        super(GappWidget, self).__init__(parent)

        self.buttonNames = QPushButton()
        self.buttonNames.setSizePolicy(self.sizePolicy)
        self.buttonNames.setIcon(QIcon('./images/question.png'))
        self.layout.addWidget(self.buttonNames)

        self.buttonDelete = QPushButton()
        self.buttonDelete.setSizePolicy(self.sizePolicy)
        self.buttonDelete.setIcon(QIcon('./images/delete.png'))
        self.layout.addWidget(self.buttonDelete)

        self.setStyleSheet("QPushButton{border-radius: 5px;width:40px; height:40px; border: 1px solid rgba(41, 107, 116,1); background-color: rgba(41, 107, 116,0);}QPushButton:hover{background-color: rgba(41, 107, 116,0.25);}")
        self.buttonNetwork.setIconSize(QSize(40,40))
        self.buttonNetwork.setIconSize(QSize(30,30))
        self.buttonSecurity.setIconSize(QSize(30,30))
        self.buttonNames.setIconSize(QSize(30,30))

        self.apps = {}

        self.buttonNames.clicked.connect(self.showNames)
        self.buttonDelete.clicked.connect(self.deleteElement)

    @pyqtSlot(str)
    def setName(self, value):
        self.name = value
        self.setLabelText(self.getName())

    @pyqtSlot()
    def getName(self):
        return self.name

    @pyqtSlot(dict)
    def setAppList(self, appList):
        self.appList = appList

    def fillGroup(self):
        self.names = self.returnGroupNameList()
        self.linkApps(self.names)

    def returnGroupNameList(self):
        fr = open('../data/appGroups.data')
        names = []
        for app in fr.readlines():
            line = app.split("|")
            if (self.name == line[0]):
                names.append(line[1].split("\n")[0])

        return names

    def linkApps(self, names):
        for app in self.appList:
            for name in names:
                if (app == name):
                    self.apps[app] = self.appList[app]


    def showNames(self):
        msg = QMessageBox()
        msg.setText(str(self.names))
        msg.exec_()

    def setSignal(self, signal):
        self.signalDel = signal

    def deleteElement(self):
        self.signalDel.emit(self.name)



    def manageNetwork(self, durationType, durationTime, bandwidth, bandwidthType):
        ### TODO: regulate network
        pass

    def manageVPN(self, durationType, durationTime):
        ### TODO: link with VPN
        pass

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    wapp = GappWidget()
    wapp.show()
    sys.exit(app.exec_())
