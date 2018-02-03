# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'speedtest.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from appPopUpSecurity import appPopUpSecurity
from appPopUpNetwork import appPopUpNetwork
import sys
sys.path.append("../Network")
import SpeedTest
import threading

class SpeedTestWidget(QWidget):
    speedTestSig = pyqtSignal(dict)

    def __init__(self, parent=None):

        super(SpeedTestWidget, self).__init__(parent)

        #self.setGeometry(QRect(300, 500, 0 , 0))
        self.resize(500, 600)

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setObjectName("mainLayout")

        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)

        self.labelTitle = QLabel()
        self.mainLayout.addWidget(self.labelTitle)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelTitle.sizePolicy().hasHeightForWidth())
        self.labelTitle.setSizePolicy(sizePolicy)
        self.labelTitle.setFont(font)
        self.labelTitle.setObjectName("labelTitle")


        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        font.setPointSize(13)

        self.resultLayout = QFormLayout()
        self.resultLayout.setObjectName("resultLayout")
        self.mainLayout.addLayout(self.resultLayout)
        self.downloadRateLabel = QLabel()

        self.downloadRateLabel.setFont(font)
        self.downloadRateLabel.setObjectName("downloadRateLabel")
        self.resultLayout.setWidget(0, QFormLayout.LabelRole, self.downloadRateLabel)
        self.downloadRateValue = QLabel()
        self.downloadRateValue.setObjectName("downloadRateValue")
        self.resultLayout.setWidget(0, QFormLayout.FieldRole, self.downloadRateValue)
        self.uploadRateLabel = QLabel()

        self.uploadRateLabel.setFont(font)
        self.uploadRateLabel.setObjectName("uploadRateLabel")
        self.resultLayout.setWidget(1, QFormLayout.LabelRole, self.uploadRateLabel)
        self.uploadRateValue = QLabel()
        self.uploadRateValue.setObjectName("uploadRateValue")
        self.resultLayout.setWidget(1, QFormLayout.FieldRole, self.uploadRateValue)
        self.serverLabel = QLabel()

        self.pingLabel = QLabel()
        self.pingLabel.setFont(font)
        self.pingLabel.setObjectName("pingLabel")
        self.resultLayout.setWidget(2, QFormLayout.LabelRole, self.pingLabel)
        self.pingValue = QLabel()
        self.pingValue.setObjectName("pingValue")
        self.resultLayout.setWidget(2, QFormLayout.FieldRole, self.pingValue)

        self.serverLabel.setFont(font)
        self.serverLabel.setObjectName("serverLabel")
        self.resultLayout.setWidget(3, QFormLayout.LabelRole, self.serverLabel)
        self.resultServerLayout = QFormLayout()
        self.resultServerLayout.setObjectName("resultServerLayout")
        self.serverCityLabel = QLabel()

        self.serverCityLabel.setFont(font)
        self.serverCityLabel.setObjectName("serverCityLabel")
        self.resultServerLayout.setWidget(1, QFormLayout.LabelRole, self.serverCityLabel)
        self.serverCityValue = QLabel()
        self.serverCityValue.setObjectName("serverCityValue")
        self.resultServerLayout.setWidget(1, QFormLayout.FieldRole, self.serverCityValue)
        self.serverCountryLabel = QLabel()

        self.serverCountryLabel.setFont(font)
        self.serverCountryLabel.setObjectName("serverCountryLabel")
        self.resultServerLayout.setWidget(0, QFormLayout.LabelRole, self.serverCountryLabel)
        self.serverCountryValue = QLabel()
        self.serverCountryValue.setObjectName("serverCountryValue")
        self.resultServerLayout.setWidget(0, QFormLayout.FieldRole, self.serverCountryValue)
        self.serverProviderLabel = QLabel()

        self.serverProviderLabel.setFont(font)
        self.serverProviderLabel.setObjectName("serverProviderLabel")
        self.resultServerLayout.setWidget(2, QFormLayout.LabelRole, self.serverProviderLabel)
        self.serverProviderValue = QLabel()
        self.serverProviderValue.setObjectName("serverProviderValue")
        self.resultServerLayout.setWidget(2, QFormLayout.FieldRole, self.serverProviderValue)
        self.resultLayout.setLayout(3, QFormLayout.FieldRole, self.resultServerLayout)

        self.dateLabel = QLabel()
        self.dateLabel.setFont(font)
        self.dateLabel.setObjectName("dateLabel")
        self.resultLayout.setWidget(4, QFormLayout.LabelRole, self.dateLabel)
        self.dateValue = QLabel()
        self.dateValue.setObjectName("dateValue")
        self.resultLayout.setWidget(4, QFormLayout.FieldRole, self.dateValue)
        self.buttonStart = QPushButton()
        self.buttonStart.setObjectName("buttonStart")
        self.mainLayout.addWidget(self.buttonStart)

        self.labelTitle.setText("Speed Test")
        self.downloadRateLabel.setText("Download rate:")
        self.downloadRateValue.setText("TextLabel")
        self.uploadRateLabel.setText("Upload rate:")
        self.uploadRateValue.setText("TextLabel")
        self.serverLabel.setText("Server:")
        self.serverCityLabel.setText("City:")
        self.serverCityValue.setText("TextLabel")
        self.serverCountryLabel.setText("Country:")
        self.serverCountryValue.setText("TextLabel")
        self.serverProviderLabel.setText("Provider:")
        self.serverProviderValue.setText("TextLabel")
        self.dateLabel.setText("Date:")
        self.dateValue.setText("TextLabel")
        self.pingLabel.setText("Ping:")
        self.buttonStart.setText("Start speed test")

        self.speedTestSig.connect(self.displaySpeedTest)
        self.buttonStart.clicked.connect(self.startThread)

        last = self.readLastSpeedTest()
        if (last != None):
            self.displaySpeedTest(last)

    def setDownload(self, value):
        self.downloadRateValue.setText(value)

    def setUpload(self, value):
        self.uploadRateValue.setText(value)

    def setDate(self, value):
        self.dateValue.setText(value)

    def setPing(self, value):
        self.pingValue.setText(value)

    def setServer(self, value):
        self.serverCountryValue.setText(str(value["country"]))
        self.serverCityValue.setText(str(value["name"]))
        self.serverProviderValue.setText(str(value["sponsor"]))

    def displaySpeedTest(self, result):
        self.setDownload(str("%.2f" % (float(result["download"])/1000000)) + " Mb/s")
        self.setUpload(str("%.2f" % (float(result["upload"])/1000000)) + " Mb/s")
        self.setPing(str(result["ping"]) + " ms")
        self.setServer(result["server"])
        self.setDate(result["timestamp"])
        self.buttonStart.setEnabled(True)

    def startThread(self):
        thread = threading.Thread(target=self.runSpeedTest)
        thread.start()

    def runSpeedTest(self):
        self.buttonStart.setEnabled(True)
        self.setAllText("calculating...")
        speedTestResult = SpeedTest.returnSpeedTestResult()

        strST = str(speedTestResult["download"]) + "|"
        strST += str(speedTestResult["upload"]) + "|"
        strST += str(speedTestResult["ping"]) + "|"
        strST += str(speedTestResult["server"]["name"]) + "|" + str(speedTestResult["server"]["country"]) + "|" + str(speedTestResult["server"]["sponsor"]) + "|"
        strST += str(speedTestResult["timestamp"])

        fh = open("../data/lastSpeedTest.data", "w")
        fh.write(strST)
        fh.close()

        self.speedTestSig.emit(speedTestResult)


    def setAllText(self, value):
        self.setDownload(value)
        self.setUpload(value)
        self.setPing(value)
        self.setDate(value)
        self.serverCityValue.setText(value)
        self.serverCountryValue.setText(value)
        self.serverProviderValue.setText(value)

    def readLastSpeedTest(self):
        fr = open("../data/lastSpeedTest.data", "r")
        strST = fr.read()
        fr.close()

        if(strST != ""):
            values = strST.split("|")
            return { "download": values[0], "upload" : values[1], "ping" : values[2], "server": {"name" : values[3], "country" : values[4], "sponsor" : values[5]}, "timestamp" : values[6] }
        else:
            return None


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    appA = SpeedTestWidget()
    appA.show()
    sys.exit(app.exec_())
