# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'appwidget.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from appPopUpSecurity import appPopUpSecurity
from appPopUpNetwork import appPopUpNetwork
import time

class appAbstract(QWidget):
    def __init__(self, parent=None):

        super(appAbstract, self).__init__(parent)


        ### Create the sub widgets
        self.label = QLabel("")
        self.buttonNetwork = QPushButton()
        self.buttonSecurity = QPushButton()

        ### Resize the self.buttons
        self.sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.sizePolicy.setHorizontalStretch(0)
        self.sizePolicy.setVerticalStretch(0)
        self.buttonNetwork.setSizePolicy(self.sizePolicy)
        self.buttonSecurity.setSizePolicy(self.sizePolicy)

        ### Add the sub widgets to a layout
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.buttonNetwork)
        self.layout.addWidget(self.buttonSecurity)

        ### Add an image to the buttons
        self.buttonNetwork.setIcon(QIcon('./images/wifi.png'))
        self.buttonSecurity.setIcon(QIcon('./images/lock.png'))

        ### Set the layout to the widget
        self.setLayout(self.layout)

        ### Connect the buttons to functions
        self.buttonNetwork.clicked.connect(self.buttonNetworkClick)
        self.buttonSecurity.clicked.connect(self.buttonSecurityClick)

        ### Enables de security button if an OpenVPN certificate is present
        self.buttonSecurity.setEnabled(self.hasRegisteredOpenVPNCertificate())

        self.secured = False
        self.networkManaged = False

    ### Returns the label's text
    @pyqtSlot()
    def getLabelText(self):
        return self.label.text()

    ### Change the label's text
    @pyqtSlot(str)
    def setLabelText(self, value):
        self.label.setText(value)
        self.update()

    @pyqtSlot(bool)
    def enableSecurityButton(self, value):
        self.buttonSecurity.setEnabled(value)

    @pyqtSlot()
    def getSecured(self):
        return self.secured

    @pyqtSlot()
    def getNetworkManaged(self):
        return self.networkManaged

    ### Triggers when the network button is clicked
    @pyqtSlot()
    def buttonNetworkClick(self):

        if self.networkManaged is False:
            ### Open the form
            dialog = appPopUpNetwork()
            dialog.setTitle(self.label.text())

            ### Get the values entered
            value = dialog.exec_()

            if (value != None):
                ### Read the current actions file
                filename = "../data/appsActions.data"
                fr = open(filename, "r")
                data_list = fr.readlines()
                fr.close()

                ### Update an exiting action if needed
                for line in data_list:
                    if self.label.text() + ",network" in line:
                        data_list.remove(line)

                ### Write into the file
                newLine = self.label.text() + ","
                newLine += "network,"
                newLine += str(value["duration"])+ ","
                newLine += str(time.time() + 3600*value["time"]) + ","
                newLine += str(value["bandwidth"]) + ","
                newLine += str(value["percentage"]) + "\n"
                data_list.append(newLine)
                fh = open(filename, "w")
                fh.writelines(data_list)
                fh.close()

                self.manageNetwork(value["duration"], value["time"], ["bandwidth"], ["percentage"])
        else:
            self.stopNetwork()



    def manageNetwork(self, durationType, durationTime, bandwidth, bandwidthType):
        pass

    def stopNetwork(self):
        pass

    ### Triggers when the security button is clicked
    @pyqtSlot()
    def buttonSecurityClick(self):
        if self.secured is False:
            ### Open the form
            dialog = appPopUpSecurity()
            dialog.setTitle(self.label.text())

            ### Get the values entered
            value = dialog.exec_()

            if (value != None):
                ### Read the current actions file
                filename = "../data/appsActions.data"
                fr = open(filename, "r")
                data_list = fr.readlines()
                fr.close()

                try :
                    ### Update an exiting action if needed
                    for line in data_list:
                        if self.label.text() + ",security" in line:
                            data_list.remove(line)

                    ### Write into the file
                    newLine = self.label.text() + ","
                    newLine += "security,"
                    newLine += str(value["duration"])+ ","
                    newLine += str(time.time() + 3600*value["time"]) + "\n"
                    data_list.append(newLine)
                    fh = open(filename, "w")
                    fh.writelines(data_list)
                    fh.close()

                    self.manageVPN(value["duration"], value["time"])
                except (RuntimeError):
                    print("App PID has changed, aborting action")
        else:
            self.stopVPN()

    def stopVPN(self):
        pass

    def manageVPN(self, durationType, durationTime):
        pass

    @pyqtSlot()
    def hasRegisteredOpenVPNCertificate(self):
        fr = open('../data/openVPNcertificates.data', "r")
        if ( fr.read() is not "" ):
            return True
        else:
            return False


    labelText = pyqtProperty(str, getLabelText, setLabelText)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    appA = appAbstract()
    appA.show()
    sys.exit(app.exec_())
