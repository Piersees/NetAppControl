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

class WappWidget(QWidget):
    def __init__(self, parent=None):

        super(WappWidget, self).__init__(parent)

        ### Create the sub widgets
        self.setStyleSheet("QPushButton{width:60px; height:60px;}")
        self.label = QLabel("Test")
        self.buttonNetwork = QPushButton()
        self.buttonSecurity = QPushButton()

        ### Resize the self.buttons
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.buttonNetwork.setSizePolicy(sizePolicy)
        self.buttonSecurity.setSizePolicy(sizePolicy)

        ### Add the sub widgets to a layout
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.buttonNetwork)
        layout.addWidget(self.buttonSecurity)

        ### Add an image to the buttons
        self.buttonNetwork.setIcon(QIcon('./wifi.png'))
        self.buttonNetwork.setIconSize(QSize(40,40))
        self.buttonSecurity.setIcon(QIcon('./lock.png'))
        self.buttonSecurity.setIconSize(QSize(40,40))

        self.setLabelText("abc")

        ### Set the layout to the widget
        self.setLayout(layout)

        ### Connect the buttons to functions
        self.buttonNetwork.clicked.connect(self.buttonNetworkClick)
        self.buttonSecurity.clicked.connect(self.buttonSecurityClick)

    ### Returns the label's text
    @pyqtSlot()
    def getLabelText(self):
        return self.label.text()

    ### Change the label's text
    @pyqtSlot(str)
    def setLabelText(self, value):
        self.label.setText(value)
        self.update()

    ### Triggers when the network button is clicked
    @pyqtSlot()
    def buttonNetworkClick(self):
        ### Open the form
        dialog = appPopUpNetwork()
        dialog.setTitle(self.label.text())

        ### Get the values entered
        value = dialog.exec_()

        ### Read the current actions file
        filename = "./appsActions.txt"
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

    ### Triggers when the security button is clicked
    @pyqtSlot()
    def buttonSecurityClick(self):
        ### Open the form
        dialog = appPopUpSecurity()
        dialog.setTitle(self.label.text())

        ### Get the values entered
        value = dialog.exec_()

        ### Read the current actions file
        filename = "./appsActions.txt"
        fr = open(filename, "r")
        data_list = fr.readlines()
        fr.close()

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


    labelText = pyqtProperty(str, getLabelText, setLabelText)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    wapp = WappWidget()
    wapp.show()
    sys.exit(app.exec_())
