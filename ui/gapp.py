from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from appAbstract import appAbstract
from appsInGroupWidget import appsInGroupWidget

class GappWidget(appAbstract):
    delInGroupSig = pyqtSignal(list)
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
        self.buttonSecurity.setIconSize(QSize(30,30))
        self.buttonNames.setIconSize(QSize(30,30))

        self.buttonSecurity.setToolTip("Security configuration")
        self.buttonDelete.setToolTip("Delete group")
        self.buttonNames.setToolTip("Applications")


        self.apps = {}

        self.buttonNames.clicked.connect(self.showNames)
        self.buttonDelete.clicked.connect(self.deleteElement)

        self.delInGroupSig.connect(self.delInGroup)

        self.securedAppList = []

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
        fr = open('data/appGroups.data')
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
        self.listPopUp = appsInGroupWidget()
        self.listPopUp.setTitle(self.name)
        self.listPopUp.fillList(self.names)
        self.listPopUp.setDeleteSignal(self.delInGroupSig)
        self.listPopUp.show()

        print(self.apps)

    def setSignal(self, signal):
        self.signalDel = signal

    def deleteElement(self):
        self.signalDel.emit(self.name)

    def delInGroup(self, appsToDelete):
        fr = open('data/appGroups.data', 'r')
        apps = fr.readlines()
        fr.close()
        print(apps)

        insertData = []

        for appToDelete in appsToDelete:
            for app in apps:
                line = app.split('|')
                if (line[0] == self.name and line[1].split('\n')[0] != appToDelete):
                    insertData.append(app)
            for name in self.names:
                if (appToDelete == name):
                    self.names.remove(name)

        self.listPopUp.fillList(self.names)

        fw = open('data/appGroups.data', 'w')
        fw.writelines(insertData)
        fw.close()

    def groupManageVPN(self, durationType, durationTime, wapps):
        for app in wapps:
            if app.getSecured() is False:
                app.manageVPN(durationType, durationTime)
                self.securedAppList.append(app)

    def stopVPN(self):
        try:
            for app in self.securedAppList:
                app.stopVPN()
        except:
            pass

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    wapp = GappWidget()
    wapp.show()
    sys.exit(app.exec_())
