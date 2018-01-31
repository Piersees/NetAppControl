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

class appsInGroupWidget(QDialog):
    def __init__(self, parent=None):

        super(appsInGroupWidget, self).__init__(parent)
        self.resize(200, 400)
        self.setWindowTitle("Apps in group")

        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.labelTitle = QLabel()
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.labelTitle.setFont(font)
        self.labelTitle.setTextFormat(Qt.AutoText)
        self.labelTitle.setAlignment(Qt.AlignCenter)
        self.mainLayout.addWidget(self.labelTitle)

        self.list = QListWidget()
        self.list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.mainLayout.addWidget(self.list)

        self.appListLayoutWidget = QWidget()
        self.mainLayout.addWidget(self.appListLayoutWidget)
        self.appListLayout = QVBoxLayout(self.appListLayoutWidget)
        self.appListLayout.addWidget(self.list)

        self.buttonDelete = QPushButton()
        self.buttonDelete.setText("Delete")
        self.mainLayout.addWidget(self.buttonDelete)
        self.buttonDelete.clicked.connect(self.deleteSelection)

    def setTitle(self, title):
        self.labelTitle.setText(title)

    def fillList(self, listApp):
        self.list.clear()
        for app in listApp:
            self.list.addItem(app)

    def deleteSelection(self):
        toDelete = []
        for app in self.list.selectedItems():
            toDelete.append(app.text())
        self.delSig.emit(toDelete)

    def setDeleteSignal(self, signal):
        self.delSig = signal



if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    appA = appsInGroupWidget()
    appA.show()
    sys.exit(app.exec_())
