# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import Qt, QtCore, QtGui, QtWidgets, QtQuick
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtGui import QPolygonF, QPainter
from PyQt5.Qt import Qt
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import os
import threading
import time
from wapp import WappWidget
import psutil


class Ui_MainWindow(QtWidgets.QMainWindow):
    speedTestSig = QtCore.pyqtSignal(str)
    bandWidthSig = QtCore.pyqtSignal(int,int)
    pingSig = QtCore.pyqtSignal(str)
    pingLossSig = QtCore.pyqtSignal(str)
    openVPNcertificateEnteredSig = QtCore.pyqtSignal()



    appExit = False

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        ### Create the app window
        self.setObjectName("self")

        ### Change the window's size
        self.resize(1000, 600)

        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)

        ### Handle the central widget
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.thi = 1;
        ### Implement the tabs layout
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(-10, -10, 1000, 571))
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setStyleSheet("QTabBar::tab {\n"
            "    background-color: white;\n"
            "    border-top: 1px solid rgba(0,0,0,0.2);\n"
            "    border-right: 1px solid rgba(0,0,0,0.2);\n"
            "    padding-bottom: 20px;\n"
            "    padding-top: 20px;\n"
            "    color: white;\n"
            "    width : 200px;\n"
            "    height: 50px;\n"
            "}\n"
            "\n"
            "QTabBar::tab:selected {\n"
            "    background-color: rgba(0,0,0,0.5);"
            "}\n"
            "\n"
            "QTabBar::tab:selected:hover {\n"
            "    background-color: rgba(0,0,0,0.5);"
            "}\n"
            "\n"
            "QTabBar::tab:hover {\n"
            "    background-color:  rgba(0,0,0,0.1);\n"
            "}\n"
            "\n"
            "QTabWidget::tab-bar {\n"
            "    \n"
            "}")
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.West)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setObjectName("tabWidget")

        ### Implement each individual tab
        self.home_tab = QtWidgets.QWidget()
        self.tab = QtWidgets.QWidget()
        self.tabSettings = QtWidgets.QWidget()
        self.tabMonitoring = pg.GraphicsLayoutWidget()
        self.home_tab.setObjectName("home_tab")
        self.tab.setObjectName("tab")
        self.tabSettings.setObjectName("tabSettings")
        self.tabMonitoring.setObjectName("tabMonitoring")

        self.tabWidget.addTab(self.home_tab, "")
        self.tabWidget.addTab(self.tab, "")
        self.tabWidget.addTab(self.tabMonitoring, "")
        self.tabWidget.addTab(self.tabSettings, "")


        self.BWplot = self.tabMonitoring.addPlot(title="Bandwidth /s")
        self.BWplot.plot(np.random.normal(size=100), pen=(255,0,0), name="Upload")
        self.BWplot.plot(np.random.normal(size=110)+5, pen=(0,255,0), name="Download")
        self.BWplot.setLabel('left', "Bandwidth", units='MB')
        self.BWplot.setLabel('bottom', "Seconds", units='s')

        self.tabWidget.setTabIcon(0, QtGui.QIcon('./images/tabHome.png'))
        self.tabWidget.setTabIcon(1, QtGui.QIcon('./images/tabMonitoring.png'))
        self.tabWidget.setTabIcon(2, QtGui.QIcon('./images/tabApps.png'))
        self.tabWidget.setTabIcon(123.3, QtGui.QIcon('./images/tabSettings.png'))

        self.tabWidget.tabBar().setTabToolTip(0, "Home")
        self.tabWidget.tabBar().setTabToolTip(1, "Apps")
        self.tabWidget.tabBar().setTabToolTip(2, "Monitoring")
        self.tabWidget.tabBar().setTabToolTip(3, "Settings")

        # self.tabWidget.iconSize(QtCore.QSize(40,40))

        ### Button
        self.pushButton_3 = QtWidgets.QPushButton(self.tab)
        self.pushButton_3.setGeometry(QtCore.QRect(520, 540, 80, 23))

        ### Menu bar
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 813, 20))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)

        ### Status bar
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        ### Central widget
        self.setCentralWidget(self.centralwidget)

        ### Layout for the home page
        self.groupBoxHome = QtWidgets.QGroupBox(self.home_tab)
        self.groupBoxHome.setGeometry(QtCore.QRect(0, 290, 778, 260))
        self.groupBoxHome.setObjectName("groupBoxHome")

        self.horizontalLayoutHome = QtWidgets.QHBoxLayout(self.groupBoxHome)
        self.horizontalLayoutHome.setObjectName("horizontalLayoutHome")

        ### Text browser
        self.textBrowserHomeInfo = QtWidgets.QTextBrowser(self.groupBoxHome)
        self.textBrowserHomeInfo.setObjectName("textBrowserHomeInfo")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowserHomeInfo.sizePolicy().hasHeightForWidth())
        self.textBrowserHomeInfo.setSizePolicy(sizePolicy)
        self.textBrowserHomeInfo.setMaximumSize(QtCore.QSize(250, 16777215))
        self.textBrowserHomeInfo.setText("[ INFORMATIONS ]")
        self.horizontalLayoutHome.addWidget(self.textBrowserHomeInfo)

        ### Buttons for the home page
        self.groupBoxHomeButtons = QtWidgets.QGroupBox(self.groupBoxHome)
        self.groupBoxHomeButtons.setObjectName("groupBoxHomeButtons")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxHomeButtons.sizePolicy().hasHeightForWidth())
        self.groupBoxHomeButtons.setSizePolicy(sizePolicy)
        self.groupBoxHomeButtons.setMaximumSize(QtCore.QSize(250, 16777215))
        self.verticalLayoutHome = QtWidgets.QVBoxLayout(self.groupBoxHomeButtons)
        self.verticalLayoutHome.setObjectName("verticalLayoutHome")

        self.textBrowserSpeedtest = QtWidgets.QTextBrowser(self.groupBoxHome)
        self.textBrowserSpeedtest.setObjectName("textBrowserSpeedtest")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowserSpeedtest.sizePolicy().hasHeightForWidth())
        self.textBrowserSpeedtest.setSizePolicy(sizePolicy)
        self.textBrowserSpeedtest.setText(self.readLastSpeedTest())
        self.verticalLayoutHome.addWidget(self.textBrowserSpeedtest)

        self.speedTestSig.connect(self.textBrowserSpeedtest.setText)
        self.bandWidthSig.connect(self.setBandWidthChart)

        self.pushButtonScan = QtWidgets.QPushButton(self.groupBoxHomeButtons)
        self.pushButtonScan.setObjectName("pushButtonScan")
        self.verticalLayoutHome.addWidget(self.pushButtonScan)
        self.pushButtonSpeed = QtWidgets.QPushButton(self.groupBoxHomeButtons)
        self.pushButtonSpeed.setObjectName("pushButtonSpeed")
        self.verticalLayoutHome.addWidget(self.pushButtonSpeed)
        self.horizontalLayoutHome.addWidget(self.groupBoxHomeButtons)

        self.pushButtonSpeed.clicked.connect(self.displaySpeedTest)

        ### Logo for the home page
        self.labelLogo = QtWidgets.QLabel(self.home_tab)
        self.labelLogo.setGeometry(QtCore.QRect(330, 130, 55, 16))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelLogo.sizePolicy().hasHeightForWidth())
        self.labelLogo.setSizePolicy(sizePolicy)
        self.labelLogo.setBaseSize(QtCore.QSize(250, 250))
        self.labelLogo.setObjectName("labelLogo")

        ### Network groupbox
        self.NetworkLayoutWidget = QtWidgets.QWidget(self.home_tab)
        self.NetworkLayoutWidget.setGeometry(QtCore.QRect(600, 10, 200, 100))
        self.NetworkLayout = QtWidgets.QVBoxLayout(self.NetworkLayoutWidget)

        ### Ip label
        self.Iplabel = QtWidgets.QLabel()
        self.Iplabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Iplabel.setObjectName("Iplabel")
        self.Iplabel.setText("Public IP adress: " + External_IP.Get_IP())
        self.NetworkLayout.addWidget(self.Iplabel)

        ### Ping label
        self.Pinglabel = QtWidgets.QLabel()
        self.Pinglabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Pinglabel.setObjectName("PingLabel")
        self.Pinglabel.setText("Pinging...")
        self.NetworkLayout.addWidget(self.Pinglabel)

        ### Ping label
        self.PingLosslabel = QtWidgets.QLabel()
        self.PingLosslabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.PingLosslabel.setObjectName("PingLabel")
        self.PingLosslabel.setText("")
        self.NetworkLayout.addWidget(self.PingLosslabel)

        self.pingLossSig.connect(self.PingLosslabel.setText)
        self.pingSig.connect(self.Pinglabel.setText)
        self.threadPing = threading.Thread(target=self.pingUpdate)
        self.threadPing.start()

        ### Insert items into the application list

        ### Create the application list
        self.list = QtWidgets.QListWidget()

        ### Insert some apps
        # self.createNewAppItem("Test 1");
        # self.createNewAppItem("Test 2");
        # self.createNewAppItem("Test 3");
        self.listApp = {}
        self.fillAppList()

        ### Arrange the app list layout
        self.appListLayoutWidget = QtWidgets.QWidget(self.tab)
        self.appListLayoutWidget.setGeometry(QtCore.QRect(20, 60, 411, 481))
        self.appListLayoutWidget.setObjectName("verticalLayoutWidget")
        self.appListLayout = QtWidgets.QVBoxLayout(self.appListLayoutWidget)
        self.appListLayout.setContentsMargins(0, 0, 0, 0)
        self.appListLayout.setObjectName("verticalLayout")
        self.appListLayout.addWidget(self.list)

        ### App search bar
        self.appSearchBar = QtWidgets.QLineEdit(self.tab)
        self.appSearchBar.setGeometry(QtCore.QRect(20, 20, 411, 23))
        self.appSearchBar.setObjectName("appSearchBar")
        self.appSearchBar.textChanged.connect(self.appSearchBarTextChanged)

        ## BandWidth chart
            #self.chart = QChart()
            #self.chart.legend().hide()
            #self.ChartView = QChartView(self.chart)
            #self.ChartView.setRenderHint(QPainter.Antialiasing)
            #self.chart.setTitle("Bandwidth by s")
            #self.seriesUp = QLineSeries()
            #self.seriesDown = QLineSeries()
            #self.pen1 = self.seriesUp.pen()
            #self.pen1.setColor(Qt.red)
            #self.seriesUp.setPen(self.pen1)
            #self.pen2 = self.seriesDown.pen()
            #self.pen2.setColor(Qt.blue)
            #self.seriesDown.setPen(self.pen2)
            #self.seriesUp.setUseOpenGL(True)
            #self.seriesDown.setUseOpenGL(True)

            #self.seriesUp.append(1,2)
            #self.seriesDown.append(1,3)
            #self.seriesUp.append(2,4)
            #self.seriesDown.append(2,1)

        #self.tabMonitoringMainLayout = QtWidgets.QHBoxLayout(self.tabMonitoring)
        #self.tabMonitoringMainLayout.setObjectName("tabMonitoringMainLayout")
        #self.tabMonitoringMainLayout.addWidget(self.ChartView)
        #self.tabMonitoring.setLayout(self.tabMonitoringMainLayout)

        ##### Settings tab
        ### Main layout
        self.tabSettingsMainLayout = QtWidgets.QHBoxLayout(self.tabSettings)
        self.tabSettingsMainLayout.setObjectName("tabSettingsMainLayout")

        ##### Sublayouts
        ### ID layout
        self.openVPNidFormVerticalLayout = QtWidgets.QVBoxLayout()
        self.openVPNidFormVerticalLayout.setObjectName("openVPNidFormVerticalLayout")
        self.tabSettingsMainLayout.addLayout(self.openVPNidFormVerticalLayout)

        ## Title layout label
        self.OpenVPNidFormlabel = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.OpenVPNidFormlabel.setFont(font)
        self.OpenVPNidFormlabel.setAlignment(QtCore.Qt.AlignCenter)
        self.OpenVPNidFormlabel.setObjectName("OpenVPNidFormlabel")
        self.OpenVPNidFormlabel.setText("Open VPN logins")
        self.openVPNidFormVerticalLayout.addWidget(self.OpenVPNidFormlabel)


        ## Form layout
        self.OpenVPNidFormLayout = QtWidgets.QFormLayout()
        self.OpenVPNidFormLayout.setObjectName("OpenVPNidFormLayout")
        self.openVPNidFormVerticalLayout.addLayout(self.OpenVPNidFormLayout)

        # Widgets declaration
        self.OpenVPNidLoginLabel = QtWidgets.QLabel()
        self.OpenVPNidLoginInput = QtWidgets.QLineEdit()
        self.OpenVPNidPasswordLabel = QtWidgets.QLabel()
        self.OpenVPNidPasswordInput = QtWidgets.QLineEdit()
        self.OpenVPNidSubmitButton = QtWidgets.QPushButton()

        # Widgets placement
        self.OpenVPNidFormLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.OpenVPNidLoginLabel)
        self.OpenVPNidFormLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.OpenVPNidLoginInput)
        self.OpenVPNidFormLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.OpenVPNidPasswordLabel)
        self.OpenVPNidFormLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.OpenVPNidPasswordInput)
        self.OpenVPNidFormLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.OpenVPNidSubmitButton)

        # Wigets naming
        self.OpenVPNidLoginLabel.setText("Login:")
        self.OpenVPNidPasswordLabel.setText("Password:")
        self.OpenVPNidSubmitButton.setText("Submit")

        # Button connecting
        self.OpenVPNidSubmitButton.setEnabled(False)
        self.OpenVPNidSubmitButton.clicked.connect(self.submitOpenVPNid)
        self.OpenVPNidLoginInput.textChanged.connect(self.enableOpenVPNidSubmit)
        self.OpenVPNidPasswordInput.textChanged.connect(self.enableOpenVPNidSubmit)



        ### Certificate layout
        self.openVPNfileLayout = QtWidgets.QVBoxLayout()
        self.openVPNfileLayout.setObjectName("openVPNfileLayout")
        self.tabSettingsMainLayout.addLayout(self.openVPNfileLayout)

        ## Widgets declaration
        self.openVPNfileDialogButton = QtWidgets.QPushButton()
        self.openVPNfilenameLabel = QtWidgets.QLabel()
        self.openVPNfilenameLabel2 = QtWidgets.QLabel()
        self.openVPNfileDialogButton2 = QtWidgets.QPushButton()
        self.openVPNsubmitButton = QtWidgets.QPushButton()

        ## Widget naming
        self.openVPNfileDialogButton.setText("Browse...")
        self.openVPNfilenameLabel.setText("Select VPN certificate: ")
        self.openVPNfileDialogButton2.setText("Browse...")
        self.openVPNfilenameLabel2.setText("Select second VPN certificate (optional): ")
        self.openVPNsubmitButton.setText("Submit")

        ## Widget placement
        self.openVPNfileLayout = QtWidgets.QVBoxLayout()
        self.openVPNidFormVerticalLayout.addLayout(self.openVPNfileLayout)
        self.openVPNfileLayout.addWidget(self.openVPNfilenameLabel)
        self.openVPNfileLayout.addWidget(self.openVPNfileDialogButton)
        self.openVPNfileLayout.addWidget(self.openVPNfilenameLabel2)
        self.openVPNfileLayout.addWidget(self.openVPNfileDialogButton2)
        self.openVPNfileLayout.addWidget(self.openVPNsubmitButton)

        self.openVPNsubmitButton.setEnabled(False)
        self.openVPNcertificate2Changed = False

        ## Button connections
        self.openVPNfileDialogButton.clicked.connect(self.selectVPNcertificate)
        self.openVPNfileDialogButton2.clicked.connect(self.selectVPNoptionalCertificate)
        self.openVPNsubmitButton.clicked.connect(self.openVPNsubmit)



        ### Signal connecting
        self.openVPNcertificateEnteredSig.connect(self.resetAppList)


        ### GUI arrangements
        self.retranslateUi(self)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)
        ##self.pushButton_3.clicked.connect(self.addAppClick)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBoxHome.setTitle(_translate("MainWindow", ""))
        self.groupBoxHomeButtons.setTitle(_translate("MainWindow", ""))
        self.pushButtonScan.setText(_translate("MainWindow", "Scan"))
        self.pushButtonSpeed.setText(_translate("MainWindow", "Speed Test"))

        self.labelLogo.setText(_translate("MainWindow", "Logo"))

        self.bwChartDisplay()

        #self.arrr = getBandWidth(self)
        #print(self.arrr[0])
        #print(self.arrr[1])

        self.pixmap = QtGui.QPixmap(os.getcwd() + 'logo.jpg')
        self.myScaledPixmap = self.pixmap.scaled(self.labelLogo.size(), Qt.KeepAspectRatio)
        self.labelLogo.setPixmap(self.myScaledPixmap)

        self.textBrowserHomeInfo.append("\n\tVitesse: " + "1000000000 km/h");
        self.textBrowserHomeInfo.append("\n\tNombre d'applications actives sur le réseau: "+"1000000000");

        self.appSearchBar.setPlaceholderText(_translate("MainWindow", "Search"))

        self.pushButton_3.setText(_translate("MainWindow", "PushButton"))

    @QtCore.pyqtSlot()
    def addAppClick(self):
        for i in range(self.list.count()):
            app_name = self.list.item(i).data(QtCore.Qt.UserRole)

    ### Add a new app item to the application list
    def createNewAppItem(self, processName, PID_list):
        wapp = QtWidgets.QListWidgetItem(self.list)
        wapp.setData(QtCore.Qt.UserRole, processName)
        wapp_widget = WappWidget()
        wapp_widget.setLabelText(processName)
        wapp_widget.setProcessName(processName)
        wapp_widget.setPIDlist(PID_list)
        wapp.setSizeHint(wapp_widget.sizeHint())
        self.list.addItem(wapp)
        self.list.setItemWidget(wapp, wapp_widget)

    ### Triggers when the app search bar text is changed
    def appSearchBarTextChanged(self):
        self.list.clear()
        if(self.appSearchBar.text() == ""):
            for app in self.listApp:
                self.createNewAppItem(app, self.listApp[app])
        else:
            for app in self.listApp:
                if self.appSearchBar.text().lower() in app.lower():
                    self.createNewAppItem(app, self.listApp[app])

    def displaySpeedTest(self):
        self.pushButtonSpeed.setEnabled(False)
        self.textBrowserSpeedtest.setText("Loading...")
        thread = threading.Thread(target=self.runSpeedTest)
        thread.start()

    def bwChartDisplay(self):
        self.threadBW = threading.Thread(target=self.bwChartGetValues)
        self.threadBW.daemaon = True
        self.threadBW.start()

    def bwChartGetValues(self):
        self.i = 0
        while(self.appExit is not True):
            self.i = 1+self.i
            arrayResult = getBandWidth(self)
            time.sleep(1)
            up = arrayResult[0]
            down = arrayResult[1]
            self.bandWidthSig.emit(up, down)

    def setBandWidthChart(self, up, down):
        print("a")
        #self.seriesUp.append(self.i, up)
        #self.seriesDown.append(self.i, down)

    def runSpeedTest(self):
        speedTestResult = SpeedTest.returnSpeedTestResult()

        strST = "Download rate: " + str(float("{0:.2f}".format(speedTestResult["download"] / 1000000))) + "Mb/s\n"
        strST += "Upload rate: " + str(float("{0:.2f}".format(speedTestResult["upload"] / 1000000))) + "Mb/s\n"
        strST += "Ping: " + str(int(speedTestResult["ping"])) + "\n"
        strST += "Server: " + str(speedTestResult["server"]["name"]) + " | " + str(speedTestResult["server"]["country"]) + " | " + str(speedTestResult["server"]["sponsor"]) + "\n"
        strST += str(speedTestResult["timestamp"])

        fh = open("./lastSpeedTest.txt", "w")
        fh.write(strST)
        fh.close()

        self.pushButtonSpeed.setEnabled(True)

        self.speedTestSig.emit(strST)

    def readLastSpeedTest(self):
        fr = open("./lastSpeedTest.txt", "r")
        strST = fr.read()
        fr.close()
        return strST

    def selectVPNcertificate(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","OpenVPN files (*.ovpn)", options=options)

        if(fileName != None):
            self.openVPNfilenameLabel.setText(fileName)
            self.openVPNsubmitButton.setEnabled(True)

    def selectVPNoptionalCertificate(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","OpenVPN files (*.ovpn)", options=options)

        if(fileName != None):
            self.openVPNfilenameLabel2.setText(fileName)
            self.openVPNcertificate2Changed = True

    def openVPNsubmit(self):
        certificate = self.openVPNfilenameLabel.text().replace("/",r'\\')

        try:
            openvpn.mainVPN(certificate)

            fw = open("./openVPNcertificates.txt", "w")
            fw.write(certificate + "\n")
            if( self.openVPNcertificate2Changed is not False ):
                certificate2 = self.openVPNfilenameLabel2.text().replace("/",r'\\')
                fw.write(certificate2 + "\n")
            fw.close()

            msg = QtWidgets.QMessageBox()
            msg.setText("openVPN certificate registered")
            msg.exec_()

            self.openVPNcertificateEnteredSig.emit()

        except(UnboundLocalError):
            msg = QtWidgets.QMessageBox()
            msg.setText("Invalid openVPN certificate")
            msg.exec_()



    def getAppListWithInternet(self):
        dic = {}
        for proc in psutil.process_iter():
            process = psutil.Process(proc.pid)
            pname = process.name()
            if proc.connections():
                if pname not in dic:
                    dic[pname] = [proc.pid]
                else:
                    dic[pname].append(proc.pid)
        return dic

    def fillAppList(self):
        self.listApp = self.getAppListWithInternet()
        for app in self.listApp:
            self.createNewAppItem(app, self.listApp[app])

    def resetAppList(self):
        self.list.clear()
        self.fillAppList()

    def submitOpenVPNid(self):
        fh = open("./openVPNid.txt", "w")
        fh.write(self.OpenVPNidLoginInput.text() + "\n" + self.OpenVPNidPasswordInput.text())
        fh.close()
        msg = QtWidgets.QMessageBox()
        msg.setText("Logins saved")
        msg.exec_()

    def checkIfValidOpenVPNLogins(self):
        if(self.OpenVPNidLoginInput.text() != "" and self.OpenVPNidPasswordInput.text() != ""):
            return True
        else:
            return False

    def enableOpenVPNidSubmit(self):
        if(self.checkIfValidOpenVPNLogins() == True):
            self.OpenVPNidSubmitButton.setEnabled(True)

        else:
            self.OpenVPNidSubmitButton.setEnabled(False)



    def pingUpdate(self):
        packetsSent = 0
        packetsReceived = 0

        while(self.appExit is not True):
            pingResult = ping.getPing()
            pingStr = pingResult['averageRoundTripTime']

            try:
                packetsSentSTR = pingResult['Sent'][:-1]
                packetsReceivedSTR = pingResult['Received'][:-1]
                packetsSent += int(packetsSentSTR)
                packetsReceived += int(packetsReceivedSTR)
                packetLossRatio = 100 - (100*(packetsSent / packetsReceived))
                self.pingSig.emit("Ping: " + str(pingStr))
                self.pingLossSig.emit("Loss ratio: " + str(packetLossRatio) + "%")
                time.sleep(1)
            except(TypeError, ValueError):
                print("ping error")

    def closeEvent(self, event):
        if(True):
            self.appExit = True
            event.accept()
        else:
            event.ignore()

from wapp import WappWidget
import sys
import time
sys.path.append("../Network")
import SpeedTest
import External_IP
import ping
from BandWidth import getBandWidth
import openvpn

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())
