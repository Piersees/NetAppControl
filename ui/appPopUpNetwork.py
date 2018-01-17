# -*- coding: utf-8 -*-

# Dialog implementation generated from reading ui file 'appPopUpNetwork.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class appPopUpNetwork(QDialog):
    def __init__(self):
        super(appPopUpNetwork, self).__init__()

        ### Set up the form window
        self.setObjectName("self")
        self.resize(329, 349)

        ### Title
        self.labelTitle = QLabel(self)
        self.labelTitle.setGeometry(QRect(50, 10, 221, 71))
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.labelTitle.setFont(font)
        self.labelTitle.setTextFormat(Qt.AutoText)
        self.labelTitle.setAlignment(Qt.AlignCenter)
        self.labelTitle.setObjectName("label")

        ### Horizontal line
        self.line = QFrame(self)
        self.line.setGeometry(QRect(50, 85, 221, 16))
        self.line.setLineWidth(2)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")

        ### Network label
        self.labelNetwork = QLabel(self)
        self.labelNetwork.setGeometry(QRect(30, 125, 281, 16))
        font = QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.labelNetwork.setFont(font)
        self.labelNetwork.setAlignment(Qt.AlignCenter)
        self.labelNetwork.setObjectName("labelNetwork")

        ### Implement the form layout
        self.FormLayoutWidget_2 = QWidget(self)
        self.FormLayoutWidget_2.setGeometry(QRect(30, 155, 281, 131))
        self.FormLayoutWidget_2.setObjectName("FormLayoutWidget_2")
        self.FormLayout = QFormLayout(self.FormLayoutWidget_2)
        self.FormLayout.setContentsMargins(0, 0, 0, 0)
        self.FormLayout.setObjectName("FormLayout")

        ##### Duration menu
        ### Drop down menu label
        self.labelDuration = QLabel(self.FormLayoutWidget_2)
        self.labelDuration.setObjectName("labelDuration")
        self.FormLayout.setWidget(0, QFormLayout.LabelRole, self.labelDuration)

        ### Drop down menu
        self.durationBox = QComboBox(self.FormLayoutWidget_2)
        self.durationBox.setObjectName("durationBox")
        self.durationBox.addItem("")
        self.durationBox.addItem("")
        self.durationBox.addItem("")
        self.FormLayout.setWidget(0, QFormLayout.FieldRole, self.durationBox)

        self.durationBox.currentIndexChanged.connect(self.activateTimeInput)

        ##### Time menu
        ### Time label
        self.labelTime = QLabel(self.FormLayoutWidget_2)
        self.labelTime.setObjectName("labelTime")
        self.FormLayout.setWidget(1, QFormLayout.LabelRole, self.labelTime)

        ### Time input
        self.timeInput = QLineEdit(self.FormLayoutWidget_2)
        self.timeInput.setObjectName("timeInput")
        self.FormLayout.setWidget(1, QFormLayout.FieldRole, self.timeInput)
        self.timeInput.setEnabled(False)

        ##### Bandwidth menu
        ### Bandwidth label
        self.labelBandwidth = QLabel(self.FormLayoutWidget_2)
        self.labelBandwidth.setObjectName("labelBandwidth")
        self.FormLayout.setWidget(2, QFormLayout.LabelRole, self.labelBandwidth)

        ### Bandwidth input
        self.bandwidthInput = QLineEdit(self.FormLayoutWidget_2)
        self.bandwidthInput.setObjectName("bandwidthInput")
        self.FormLayout.setWidget(2, QFormLayout.FieldRole, self.bandwidthInput)

        ##### Mode menu
        ### Mode layout
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        ### Mode label
        self.labelMode = QLabel(self.FormLayoutWidget_2)
        self.labelMode.setObjectName("labelMode")
        self.FormLayout.setWidget(3, QFormLayout.LabelRole, self.labelMode)

        ### Mode radio buttons
        self.radioButtonPercent = QRadioButton(self.FormLayoutWidget_2)
        self.radioButtonPercent.setObjectName("radioButtonPercent")
        self.horizontalLayout.addWidget(self.radioButtonPercent)
        self.radioButtonMb = QRadioButton(self.FormLayoutWidget_2)
        self.radioButtonMb.setObjectName("radioButton")
        self.horizontalLayout.addWidget(self.radioButtonMb)
        self.FormLayout.setLayout(3, QFormLayout.FieldRole, self.horizontalLayout)

        ### Submit button
        self.pushButton = QPushButton(self)
        self.pushButton.setGeometry(QRect(220, 305, 91, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setEnabled(False)
        self.pushButton.clicked.connect(self.exitDialog)

        ### Enable or not the submit button
        self.pushButton.setEnabled(False)
        self.durationBox.currentIndexChanged.connect(self.enableSubmitting)
        self.timeInput.textChanged.connect(self.enableSubmitting)
        self.bandwidthInput.textChanged.connect(self.enableSubmitting)
        self.radioButtonPercent.toggled.connect(self.enableSubmitting)
        self.radioButtonMb.toggled.connect(self.enableSubmitting)

        self.retranslateUi(self)
        QMetaObject.connectSlotsByName(self)

    @pyqtSlot()
    def exitDialog(self):
        self.accept()

    @pyqtSlot(str)
    def setTitle(self, value):
        self.labelTitle.setText(value)

    ### Enable or disable the time input if it is needed or not
    @pyqtSlot()
    def activateTimeInput(self):
        if (self.durationBox.currentIndex() == 1):
            self.timeInput.setEnabled(True)
        else:
            self.timeInput.setEnabled(False)
            self.timeInput.setText("")

    ### Return true if the values entered for the duration are correct
    def checkIfDurationBoxIsCorrect(self):
        if( self.durationBox.currentIndex() == 1 and self.is_number(self.timeInput.text()) ):
            if ( int(self.timeInput.text()) < 0 ) :
                return False
            else:
                return True
        elif( self.durationBox.currentIndex() == 1):
            return False
        else: return True

    ### Return true if the value entered for the bandwidth is correct
    def checkIfBandwidthIsCorrect(self):
        if( self.is_number(self.bandwidthInput.text()) and int(self.bandwidthInput.text()) >= 0) :
            return True
        else:
            return False
        return True

    ### Return true if one of the button is checked
    def checkIfRadioButtonsAreCorrect(self):
        return ( self.radioButtonPercent.isChecked() or self.radioButtonMb.isChecked() )

    ### Return true is all of the values in the form are correct
    def checkIfFormIsComplete(self):
        return ( self.checkIfDurationBoxIsCorrect() and self.checkIfBandwidthIsCorrect() and self.checkIfRadioButtonsAreCorrect())

    ### Enable or disable the submit button if the form values are correct or not
    @pyqtSlot()
    def enableSubmitting(self):
        if(self.checkIfFormIsComplete()):
            self.pushButton.setEnabled(True)
        else:
            self.pushButton.setEnabled(False)

    def retranslateUi(self, Dialog):
        _translate = QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Network options"))
        self.labelNetwork.setText(_translate("Dialog", "Network"))
        self.pushButton.setText(_translate("Dialog", "OK"))
        self.labelDuration.setText(_translate("Dialog", "Duration"))
        self.durationBox.setItemText(0, _translate("Dialog", "Until the application is closed"))
        self.durationBox.setItemText(1, _translate("Dialog", "For a set period of time"))
        self.durationBox.setItemText(2, _translate("Dialog", "Forever"))
        self.labelTime.setText(_translate("Dialog", "Hours"))
        self.labelBandwidth.setText(_translate("Dialog", "Bandwidth"))
        self.radioButtonPercent.setText(_translate("Dialog", "Percent"))
        self.radioButtonMb.setText(_translate("Dialog", "MB/s"))
        self.labelMode.setText(_translate("Dialog", "Mode"))
        self.labelTitle.setText(_translate("Dialog", "Appli Name"))

    ### Is triggered when the form is the submit.
    ### Returns the following dictionary:
    #### 'duration' : the type of duration; 0: until the application is closed, 1: for a set period of time, 2: forever
    #### 'time' : the entered set period of time
    #### 'bandwidth' : the entered bandwidth
    #### 'percentage' : true if the bandwidth is in percentage, false otherwise
    def exec_(self):
        super(appPopUpNetwork, self).exec_()
        if( self.durationBox.currentIndex() == 1 ):
            return { 'duration' : self.durationBox.currentIndex(), 'time' : int(self.timeInput.text()), 'bandwidth' : self.bandwidthInput.text(), 'percentage' : self.radioButtonPercent.isChecked() }
        else:
            return { 'duration' : self.durationBox.currentIndex(), 'time' : 0, 'bandwidth' : self.bandwidthInput.text(), 'percentage' : self.radioButtonPercent.isChecked() }

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass

        return False
