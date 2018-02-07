from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

### The dialog window showing the apps in a group, and allowing the user to remove them from the group
class hostsInChannelWidget(QDialog):
    def __init__(self, parent=None):

        super(appsInGroupWidget, self).__init__(parent)
        self.setFixedSize(200, 400)
        self.setWindowTitle("Hosts in Channel")


        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.setStyleSheet("QDialog{background-color:white;}QLabel{color:rgba(41, 107, 116, 1);}QPushButton{border-radius: 20px;width:60px; height:60px;border: 1px solid rgb(41, 107, 116); background-color: rgb(41, 107, 116);}QPushButton:hover{border: 1px solid rgba(41, 107, 116, 0.5); background-color: rgba(41, 107, 116,0.5);}")

        ### Title label
        self.labelTitle = QLabel()
        font = QFont()
        font.setPointSize(20)
        font.setWeight(0)
        font.setLetterSpacing(QFont.AbsoluteSpacing,2)
        self.labelTitle.setFont(font)
        self.labelTitle.setTextFormat(Qt.AutoText)
        self.labelTitle.setAlignment(Qt.AlignCenter)

        self.mainLayout.addWidget(self.labelTitle)

        self.hostitemsLayout = QFormLayout()
        self.hostitemsLayout.setObjectName("hostitemsLayout")
        self.mainLayout.addLayout(self.hostitemsLayout)

        line0 = QFrame();
        line0.setFrameShape(QFrame.HLine);
        line0.setFrameShadow(QFrame.Sunken);
        self.hostitemsLayout.setWidget(0, QFormLayout.SpanningRole, line0)

        font = QFont()
        font.setBold(True)
        font.setWeight(75)

        self.hostnamelab = QLabel()
        self.hostitemsLayout.setWidget(1, QFormLayout.LabelRole, self.hostnamelab)

        self.siglab = QLabel()
        self.hostitemsLayout.setWidget(1, QFormLayout.FieldRole, self.siglab)

        line1 = QFrame();
        line1.setFrameShape(QFrame.HLine);
        line1.setFrameShadow(QFrame.Sunken);
        self.hostitemsLayout.setWidget(2, QFormLayout.SpanningRole, line1)


    def fillList(self, hostList, title):
        i = 2
        self.labelTitle.setText(title)
        for key, value in hostList:
            i = i + 1
            host = QLabel()
            host.setText(key)
            self.hostitemsLayout.setWidget(i, QFormLayout.LabelRole, host)

            sig = QLabel()
            sig.setText(value)
            self.hostitemsLayout.setWidget(i, QFormLayout.FieldRole, sig)

            i = i + 1

            line = QFrame();
            line.setFrameShape(QFrame.HLine);
            line.setFrameShadow(QFrame.Sunken);
            self.hostitemsLayout.setWidget(i, QFormLayout.SpanningRole, line)
