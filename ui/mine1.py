# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import Qt, QtCore, QtGui, QtWidgets, QtQuick
from PyQt5.QtGui import QPolygonF, QPainter
from PyQt5.Qt import Qt
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import os
import threading
import psutil
from wapp import WappWidget
from gapp import GappWidget
import sys
import time
sys.path.append("../Network")
import SpeedTest
import External_IP
import ping
import NetworkScan
from BandWidth import getBandWidth
import openvpn

class Ui_MainWindow(QtWidgets.QMainWindow):
    speedTestSig = QtCore.pyqtSignal(str)
    bandWidthSig = QtCore.pyqtSignal(int,int)
    pingSig = QtCore.pyqtSignal(str)
    pingLossSig = QtCore.pyqtSignal(str)
    incomingConnectionSig = QtCore.pyqtSignal(dict)
    autoRefreshListSig = QtCore.pyqtSignal(dict)
    deleteGroupSig = QtCore.pyqtSignal(str)
    openVpnThread = None
    IP, HOSTNAME, STATUS = range(3)
    nic = None

    appExit = False

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        ### Create the app window
        self.setObjectName("self")

        ### Change the window's size
        self.resize(1000, 600)

        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        ### Handle the central widget
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.thi = 1;
        ### Implement the tabs layout
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(-10, -10, 1000, 571))
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidgetBar = self.tabWidget.tabBar()
        self.tabWidgetBar.setObjectName("tabWidgetBar")
        self.tabWidget.setStyleSheet("QTabBar#tabWidgetBar::tab {\n"
            "    background-color: white;\n"
            "    border-top: 1px solid rgba(0,0,0,0.2);\n"
            "    border-right: 1px solid rgba(0,0,0,0.2);\n"
            "    padding-bottom: 40px;\n"
            "    padding-top: 20px;\n"
            "    color: white;\n"
            "    width : 200px;\n"
            "    height: 81px;\n"
            "}\n"
            "\n"
            "QTabBar#tabWidgetMonitoringBar::tab {"
            "background-color: rgb(41, 107, 116);"
            "border-left: 1px solid rgba(0,0,0,0.2);"
            "border-bottom: 1px solid rgba(0,0,0,0.2);"
            "padding: 10px;"
            "color: white;"
            "width: 100px;"
            "}"
            "QTabBar#tabWidgetBar::tab:selected, QTabBar#tabWidgetMonitoringBar::tab:hover{\n"
            "    background-color: rgba(41, 107, 116,0.7);"
            "   color: white;"
            "}\n"
            "\n"
            "QTabBar#tabWidgetBar::tab:selected:hover{\n"
            "    background-color: rgba(41, 107, 116, 0.7);"
            "}\n"
            "\n"
            "QTabBar#tabWidgetMonitoringBar::tab:selected, QTabBar#tabWidgetBar::tab:hover, QTabBar#tabWidgetMonitoringBar::tab:selected:hover{\n"
            "    background-color: rgba(41, 107, 116, 0.3);\n"
            "   color: rgb(41, 107, 116);"
            "}\n"
            "\n"
            "QLineEdit {"
                "border-top: 0px solid white;"
                "border-left: 0px solid white;"
                "border-right: 0px solid white;"
                "padding-bottom: 5px;"
                "border-bottom: 1px solid #dddddd;"
            "}"
            "QLineEdit:focus{"
                "border-top: 0px solid white;"
                "border-left: 0px solid white;"
                "border-right: 0px solid white;"
                "border-bottom: 2px solid rgb(41, 107, 116);"
            "    padding-bottom: 5px;"
            "}"
            "QLineEdit:selected {"
            "border-top: 0px solid white;"
            "border-left: 0px solid white;"
            "border-right: 0px solid white;"
            "border-bottom: 2px solid rgb(41, 107, 116);"
            "    padding-bottom: 5px;"
            "}"
            "QPushButton#refreshAppsButton{"
            "width:15px; height:15px;border: 1px solid rgb(41, 107, 116); background-color: rgb(41, 107, 116); border-radius: 14px;"
            "}"
            "QPushButton#refreshAppsButton:hover{"
            "border: 1px solid rgba(41, 107, 116, 0.5); background-color: rgba(41, 107, 116,0.5); border-radius: 14px;"
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


        self.tabWidget.currentChanged.connect(self.onChange)

        self.tabWidget.addTab(self.home_tab, "")
        self.tabWidget.addTab(self.tab, "")
        self.tabWidget.addTab(self.tabMonitoring, "")
        self.tabWidget.addTab(self.tabSettings, "")



        ### Implement the tabs layout
        self.tabWidgetMonitoring = QtWidgets.QTabWidget(self.tabMonitoring)
        self.tabWidgetMonitoring.setObjectName("tabWidgetMonitoring")

        self.tabWidgetMonitoringBar = self.tabWidgetMonitoring.tabBar()
        self.tabWidgetMonitoringBar.setObjectName("tabWidgetMonitoringBar")

        self.bwTabMonitoring = pg.GraphicsLayoutWidget()
        self.bwTabConnections = QtWidgets.QWidget()

        self.bwTabMonitoring.setObjectName("bwTabMonitoring")
        self.bwTabConnections.setObjectName("bwTabConnections")

        self.tabWidgetMonitoring.addTab(self.bwTabMonitoring, "Bandwidth")
        self.tabWidgetMonitoring.addTab(self.bwTabConnections, "Connections")

        ## BandWidth graph
        self.BWplot = self.bwTabMonitoring.addPlot(title="Bandwidth over time")
        self.BWplot.setDownsampling(mode='peak')
        #self.BWplot.setClipToView(True)
        self.BWplot.setRange(xRange=[-100, 0])
        self.BWplot.showAxis('bottom', False)
        self.BWplot.addLegend()
        self.dataUL = np.empty(600)
        self.dataDL = np.empty(600)
        self.curveUL = self.BWplot.plot(self.dataUL, fillLevel=-0.25, brush=(200,50,50,100), pen=(255,0,0), name="Upload rate")
        self.curveDL = self.BWplot.plot(self.dataDL, fillLevel=-0.05, brush=(50,50,200,100), pen=(0,0,255), name="Download rate")
        self.BWplot.setLabel('left', "Bandwidth", units='kB')
        self.BWplot.showGrid(x=True, y=True)
        self.ptrBW = 0

        ## Incoming connections tab
        self.incomingConnectionsMainLayout = QVBoxLayout()
        self.bwTabConnections.setLayout(self.incomingConnectionsMainLayout)
        self.incomingConnectionsGroupBox = QGroupBox("Connections on your network")
        self.incomingConnectionsMainLayout.addWidget(self.incomingConnectionsGroupBox)
        self.incomingConnectionsGroupBox.setGeometry(10, 10, self.bwTabConnections.width()-20, self.bwTabConnections.height()-20)
        self.incomingConnectionsList = QTreeView()
        self.incomingConnectionsList.setRootIsDecorated(False)
        self.incomingConnectionsList.setAlternatingRowColors(True)

        self.incomingConnectionsLayout = QHBoxLayout()
        self.incomingConnectionsLayout.addWidget(self.incomingConnectionsList)
        self.incomingConnectionsGroupBox.setLayout(self.incomingConnectionsLayout)

        self.incomingConnectionsModel = self.createConnectionModel()
        self.incomingConnectionsList.setModel(self.incomingConnectionsModel)

        self.threadIncomingConnections = threading.Thread(target=self.manageConnectionsList)
        self.threadIncomingConnections.start()

        self.incomingConnectionSig.connect(self.resetConnectionsList)


        ### Setting up tab icons
        self.tabWidget.setTabIcon(0, QtGui.QIcon('./images/tabHome.png'))
        self.tabWidget.setTabIcon(2, QtGui.QIcon('./images/tabMonitoringColored.png'))
        self.tabWidget.setTabIcon(1, QtGui.QIcon('./images/tabAppsColored.png'))
        self.tabWidget.setTabIcon(3, QtGui.QIcon('./images/tabSettingsColored.png'))

        self.tabWidget.setIconSize(QSize(60,60))

        self.tabWidget.tabBar().setTabToolTip(0, "Home")
        self.tabWidget.tabBar().setTabToolTip(1, "Apps")
        self.tabWidget.tabBar().setTabToolTip(2, "Monitoring")
        self.tabWidget.tabBar().setTabToolTip(3, "Settings")


        # self.tabWidget.iconSize(QtCore.QSize(40,40))

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


        ### Create the application list
        self.list = QtWidgets.QListWidget()

        ### Insert items into the application list
        self.fillAppList()
        self.list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        ### Secure the needed apps in the list
        self.secureForeverSecuredApps()

        ### Arrange the app list layout
        self.appListLayoutWidget = QtWidgets.QWidget(self.tab)
        self.appListLayoutWidget.setGeometry(QtCore.QRect(20, 60, 411, 481))
        self.appListLayoutWidget.setObjectName("verticalLayoutWidget")
        self.appListLayout = QtWidgets.QVBoxLayout(self.appListLayoutWidget)
        self.appListLayout.setContentsMargins(0, 0, 0, 0)
        self.appListLayout.setObjectName("verticalLayout")
        self.appListLayout.addWidget(self.list)

        ### Link the selection changed event to a function
        self.list.itemSelectionChanged.connect(self.enableAddToGroupButton)

        ### Create the app groups groupbox
        self.groupBoxAppGroup = QtWidgets.QGroupBox(self.tab)
        self.groupBoxAppGroup.setObjectName("groupBoxAppGroup")
        self.groupBoxAppGroup.setGeometry(QtCore.QRect(450, 60, 320, 481))

        ### Create the app groups groupbox layout
        self.groupMainLayoutWidget = QtWidgets.QVBoxLayout(self.groupBoxAppGroup)
        self.groupMainLayoutWidget.setGeometry(QtCore.QRect(10, 10, 300, 460))
        self.groupMainLayoutWidget.setObjectName("groupMainLayoutWidget")

        ### Create the group list
        self.groupList = QtWidgets.QListWidget()

        ### Create the app group list layout
        self.groupListLayoutWidget = QtWidgets.QWidget()
        self.groupMainLayoutWidget.addWidget(self.groupListLayoutWidget)
        self.groupListLayoutWidget.setGeometry(QtCore.QRect(10, 10, 300, 450))
        self.groupListLayoutWidget.setObjectName("groupListLayoutWidget")
        self.groupListLayout = QtWidgets.QVBoxLayout(self.groupListLayoutWidget)
        self.groupListLayout.setContentsMargins(0, 0, 0, 0)
        self.groupListLayout.setObjectName("groupListLayout")
        self.groupListLayout.addWidget(self.groupList)

        ### Insert groups
        self.addGroups()

        ### Connect the delete event
        self.deleteGroupSig.connect(self.deleteGroup)

        ### Link the selection changed event to a function
        self.groupList.itemSelectionChanged.connect(self.enableAddToGroupButton)

        ### Create the buttons layout
        self.groupAppButtonsLayout = QtWidgets.QHBoxLayout()
        self.groupAppButtonsLayout.setObjectName("groupAppButtonsLayout")
        self.groupMainLayoutWidget.addLayout(self.groupAppButtonsLayout)

        ### Create the add button
        self.buttonGroupAppAdd = QtWidgets.QPushButton()
        self.groupAppButtonsLayout.addWidget(self.buttonGroupAppAdd)
        self.buttonGroupAppAdd.setObjectName("buttonGroupAppAdd")
        self.buttonGroupAppAdd.setText("Add to group")

        ### Create the new group button
        self.buttonGroupAppNew = QtWidgets.QPushButton()
        self.groupAppButtonsLayout.addWidget(self.buttonGroupAppNew)
        self.buttonGroupAppNew.setObjectName("buttonGroupAppNew")
        self.buttonGroupAppNew.setText("New")

        ### Connect the buttons
        self.buttonGroupAppNew.clicked.connect(self.createNewGroup)
        self.buttonGroupAppAdd.clicked.connect(self.addToGroup)
        self.buttonGroupAppAdd.setEnabled(False)


        ### App search bar
        self.appSearchBar = QtWidgets.QLineEdit(self.tab)
        self.appSearchBar.setGeometry(QtCore.QRect(20, 20, 411, 23))
        self.appSearchBar.setObjectName("appSearchBar")
        self.appSearchBar.textChanged.connect(self.appSearchBarTextChanged)

        ### Refresh button
        self.refreshAppsButton = QtWidgets.QPushButton(self.tab)
        self.refreshAppsButton.setGeometry(QtCore.QRect(441, 20, 30, 30))
        self.refreshAppsButton.setObjectName("refreshAppsButton")
        self.refreshAppsButton.setText("")
        self.refreshAppsButton.setIcon(QIcon('./images/refresh.png'))
        self.refreshAppsButton.clicked.connect(self.resetAppList)

        ### Automatically refresh
        self.autoRefreshListSig.connect(self.resetAppListWithDict)
        self.threadAutoRefresh = threading.Thread(target=self.autoRefreshList)
        self.threadAutoRefresh.start()

        ##### Settings tab
        ### Main layout
        self.tabSettingsMainLayout = QtWidgets.QHBoxLayout(self.tabSettings)
        self.tabSettingsMainLayout.setObjectName("tabSettingsMainLayout")
        self.tabSettings.setStyleSheet("")


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
        self.OpenVPNidFormlabel.setTextFormat(QtCore.Qt.RichText)
        self.openVPNidFormVerticalLayout.addWidget(self.OpenVPNidFormlabel)


        ## Form layout
        self.OpenVPNidFormLayout = QtWidgets.QFormLayout()
        self.OpenVPNidFormLayout.setObjectName("OpenVPNidFormLayout")
        self.OpenVPNidFormLayout.setContentsMargins(225, -1, 275, 0);
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



        self.line = QtWidgets.QFrame();
        self.line.setFrameShape(QtWidgets.QFrame.HLine);
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken);
        self.openVPNidFormVerticalLayout.addWidget(self.line)

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
        self.openVPNfileLayout = QtWidgets.QFormLayout()
        self.openVPNidFormVerticalLayout.addLayout(self.openVPNfileLayout)
        self.openVPNfileLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.openVPNfilenameLabel)
        self.openVPNfileLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.openVPNfileDialogButton)
        self.openVPNfileLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.openVPNfilenameLabel2)
        self.openVPNfileLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.openVPNfileDialogButton2)
        self.openVPNfileLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.openVPNsubmitButton)
        self.openVPNfileLayout.setContentsMargins(125, -1, 175, 0);


        self.openVPNsubmitButton.setEnabled(False)
        self.openVPNcertificate2Changed = False

        ## Button connections
        self.openVPNfileDialogButton.clicked.connect(self.selectVPNcertificate)
        self.openVPNfileDialogButton2.clicked.connect(self.selectVPNoptionalCertificate)
        self.openVPNsubmitButton.clicked.connect(self.openVPNsubmit)


        ### GUI arrangements
        self.retranslateUi(self)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

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
        wapp_widget.setNic(self.nic)
        wapp.setSizeHint(wapp_widget.sizeHint())
        self.list.addItem(wapp)
        self.list.setItemWidget(wapp, wapp_widget)

    ### Triggers when the app search bar text is changed
    def appSearchBarTextChanged(self):
        if(self.appSearchBar.text() == ""):
            for i in range(self.list.count()):
                self.list.item(i).setHidden(False)
        else:
            for i in range(self.list.count()):
                app = self.list.item(i)
                if self.appSearchBar.text().lower() in self.list.itemWidget(app).getLabelText().lower():
                    app.setHidden(False)
                else:
                    app.setHidden(True)

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
        iostat = psutil.net_io_counters(pernic=False, nowrap=True)

        while(self.appExit is not True):
            self.i = 1+self.i
            presc_UL=iostat[0]
            presc_DL=iostat[1]
            iostat = psutil.net_io_counters(pernic=False, nowrap=True)
            upload_rate = (iostat[0] - presc_UL)/1000
            download_rate = (iostat[1] - presc_DL)/1000
            arrayResult = [upload_rate, download_rate]
            up = arrayResult[0]
            down = arrayResult[1]
            self.bandWidthSig.emit(up, down)
            time.sleep(1)

    def setBandWidthChart(self, up, down):
        if self.ptrBW == 600:
            self.dataUL[:-1] = self.dataUL[1:]
            self.dataDL[:-1] = self.dataDL[1:]
            self.ptrBW = 599
        self.dataUL[self.ptrBW] = up
        self.dataDL[self.ptrBW] = down
        self.ptrBW += 1
        self.curveUL.setData(self.dataUL[:self.ptrBW])
        self.curveUL.setPos(-self.ptrBW, 0)
        self.curveDL.setData(self.dataDL[:self.ptrBW])
        self.curveDL.setPos(-self.ptrBW, 0)
        #dataUL[:-1] = dataUL[1:] #shift data in the array to the left
        #dataUL[-1] = upload
        #curveUL.setData(dataUL)
        #dataDL[:-1] = dataDL[1:] #shift data in the array to the left
        #dataDL[-1] = download
        #curveDL.setData(dataDL)

    def runSpeedTest(self):
        speedTestResult = SpeedTest.returnSpeedTestResult()

        strST = "Download rate: " + str(float("{0:.2f}".format(speedTestResult["download"] / 1000000))) + "Mb/s\n"
        strST += "Upload rate: " + str(float("{0:.2f}".format(speedTestResult["upload"] / 1000000))) + "Mb/s\n"
        strST += "Ping: " + str(int(speedTestResult["ping"])) + "\n"
        strST += "Server: " + str(speedTestResult["server"]["name"]) + " | " + str(speedTestResult["server"]["country"]) + " | " + str(speedTestResult["server"]["sponsor"]) + "\n"
        strST += str(speedTestResult["timestamp"])

        fh = open("../data/lastSpeedTest.data", "w")
        fh.write(strST)
        fh.close()

        self.pushButtonSpeed.setEnabled(True)

        self.speedTestSig.emit(strST)

    def readLastSpeedTest(self):
        fr = open("../data/lastSpeedTest.data", "r")
        strST = fr.read()
        fr.close()
        return strST

    def selectVPNcertificate(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","OpenVPN files (*.ovpn)", options=options)

        if(fileName != None):
            self.openVPNfilenameLabel.setText(fileName)
            self.openVPNsubmitButton.setEnabled(True)

    def selectVPNoptionalCertificate(self):
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","OpenVPN files (*.ovpn)", options=options)

        if(fileName != None):
            self.openVPNfilenameLabel2.setText(fileName)
            self.openVPNcertificate2Changed = True

    def openVPNsubmit(self):
        certificate = self.openVPNfilenameLabel.text().replace("/",r'\\')

        try:
            (self.OpenVpnThread,self.nic) = openvpn.mainVPN(certificate)

            fw = open("../data/openVPNcertificates.data", "w")
            fw.write(certificate + "\n")
            if( self.openVPNcertificate2Changed is not False ):
                certificate2 = self.openVPNfilenameLabel2.text().replace("/",r'\\')
                fw.write(certificate2 + "\n")
            fw.close()

            msg = QtWidgets.QMessageBox()
            msg.setText("openVPN certificate registered")
            msg.exec_()


            for i in range(self.list.count()):
                wapp = self.list.item(i)
                self.list.itemWidget(wapp).enableSecurityButton(True)
                self.list.itemWidget(wapp).setNic(self.nic)


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
            if ( self.appInWappList(self.listApp, app) is False ):
                self.createNewAppItem(app, self.listApp[app])

    def fillAppListWithDict(self, listApp):
        for app in listApp:
            if ( self.appInWappList(listApp, app) is False ):
                self.createNewAppItem(app, listApp[app])

    def compareWapp(self, wapp, apps, app):
        if(wapp.getProcessName() != app):
            return False
        else:
            if (wapp.getPIDlist() != apps[app]):
                return False
            return True

    def appInWappList(self, apps, app):
        for i in range(self.list.count()):
            wapp = self.list.item(i)
            if( self.compareWapp(self.list.itemWidget(wapp), apps, app) is True ):
                return True
        return False

    def clearList(self):
        apps = self.getAppListWithInternet()
        itemsToRemove = []
        for i in range(self.list.count()):
            wapp = self.list.item(i)
            toDelete = True
            for app in apps:
                if(self.compareWapp(self.list.itemWidget(wapp), apps, app) is True):
                    toDelete = False
            if(toDelete is True):
                itemsToRemove.append(self.list.item(i))
        for item in itemsToRemove:
            self.list.takeItem(self.list.row(item))

    def clearListWithList(self, apps):
        itemsToRemove = []
        for i in range(self.list.count()):
            wapp = self.list.item(i)
            toDelete = True
            for app in apps:
                if(self.compareWapp(self.list.itemWidget(wapp), apps, app) is True):
                    toDelete = False
            if(toDelete is True):
                itemsToRemove.append(self.list.item(i))
        for item in itemsToRemove:
            self.list.takeItem(self.list.row(item))


    def resetAppList(self):
        self.secureForeverSecuredApps()
        # self.clearList()
        # self.fillAppList()
        # self.appSearchBarTextChanged()

    def resetAppListWithDict(self, listApp):
        self.clearListWithList(listApp)
        self.fillAppListWithDict(listApp)
        self.appSearchBarTextChanged()

    def autoRefreshList(self):
        time.sleep(8)
        while(self.appExit is False):
            self.autoRefreshListSig.emit(self.getAppListWithInternet())
            self.secureForeverSecuredApps()
            time.sleep(5)


    def submitOpenVPNid(self):
        fh = open("../data/openVPNid.data", "w")
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
                packetLossRatio = 100 - (100*(packetsReceived / packetsSent))
                self.pingSig.emit("Ping: " + str(pingStr))
                self.pingLossSig.emit("Loss ratio: " + str(float("{0:.2f}".format(packetLossRatio / 1000000))) + "%")
                time.sleep(1)
            except(TypeError, ValueError):
                packetsSent += 1
                packetLossRatio = 100 - (100*(packetsReceived / packetsSent))
                self.pingSig.emit("Ping: lost")
                self.pingLossSig.emit("Loss ratio: " + str(float("{0:.2f}".format(packetLossRatio / 1000000))) + "%")


    #@pyqtSlot()
    def onChange(self,i): #changed!
        if i == 0:
            self.tabWidget.setTabIcon(0, QtGui.QIcon('./images/tabHome.png'))
            self.tabWidget.setTabIcon(2, QtGui.QIcon('./images/tabMonitoringColored.png'))
            self.tabWidget.setTabIcon(1, QtGui.QIcon('./images/tabAppsColored.png'))
            self.tabWidget.setTabIcon(3, QtGui.QIcon('./images/tabSettingsColored.png'))
        elif i == 2:
            self.tabWidget.setTabIcon(2, QtGui.QIcon('./images/tabMonitoring.png'))
            self.tabWidget.setTabIcon(0, QtGui.QIcon('./images/tabHomeColored.png'))
            self.tabWidget.setTabIcon(1, QtGui.QIcon('./images/tabAppsColored.png'))
            self.tabWidget.setTabIcon(3, QtGui.QIcon('./images/tabSettingsColored.png'))
        elif i == 1:
            self.tabWidget.setTabIcon(1, QtGui.QIcon('./images/tabApps.png'))
            self.tabWidget.setTabIcon(0, QtGui.QIcon('./images/tabHomeColored.png'))
            self.tabWidget.setTabIcon(2, QtGui.QIcon('./images/tabMonitoringColored.png'))
            self.tabWidget.setTabIcon(3, QtGui.QIcon('./images/tabSettingsColored.png'))
        elif i == 3:
            self.tabWidget.setTabIcon(3, QtGui.QIcon('./images/tabSettings.png'))
            self.tabWidget.setTabIcon(0, QtGui.QIcon('./images/tabHomeColored.png'))
            self.tabWidget.setTabIcon(2, QtGui.QIcon('./images/tabMonitoringColored.png'))
            self.tabWidget.setTabIcon(1, QtGui.QIcon('./images/tabAppsColored.png'))

    def createNewGroupWidget(self, name):
        gapp = QtWidgets.QListWidgetItem(self.groupList)
        gapp_widget = GappWidget()
        gapp_widget.setAppList(self.listApp)
        gapp_widget.setName(name)
        gapp_widget.setSignal(self.deleteGroupSig)
        gapp_widget.fillGroup()
        gapp.setSizeHint(gapp_widget.sizeHint())
        self.groupList.addItem(gapp)
        self.groupList.setItemWidget(gapp, gapp_widget)

    def addGroups(self):
        fr = open('../data/groups.data', 'r')
        names = []

        for name in fr.readlines():
            self.createNewGroupWidget(name.split("\n")[0])


    def createNewGroup(self):
        fr = open('../data/groups.data', 'r')
        groups = fr.readlines()
        fr.close()

        groupName, okPressed = QtWidgets.QInputDialog.getText(self, "New group","New group name:", QtWidgets.QLineEdit.Normal, "")

        alreadyExists = False
        if okPressed and groupName != '':
            for group in groups:
                if (groupName == group.split("\n")[0]):
                    alreadyExists = True

        if alreadyExists is False:
            fw = open('../data/groups.data', "a")
            fw.write(groupName + "\n")
            self.createNewGroupWidget(groupName)
            fw.close()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setText("Group already exists")
            msg.exec_()

    def addToGroup(self):
        processes = []
        data_list = []

        for process in self.list.selectedItems():
            processes.append(self.list.itemWidget(process).getLabelText())

        selectedGroup = self.groupList.itemWidget( self.groupList.selectedItems()[0] )
        name = selectedGroup.getName()

        fw = open('../data/appGroups.data', 'a')
        fr = open('../data/appGroups.data', 'r')
        existingProcesses = fr.readlines()
        fr.close()

        for process in processes:
            alreadyExists = False
            for existingProcess in existingProcesses:
                line = existingProcess.split('|')
                if name in line[0]:
                    if process in line[1]:
                        alreadyExists = True
            if alreadyExists is False:
                data_list.append(name + "|" + process + "\n")
        fw.writelines(data_list)
        fw.close()

        selectedGroup.fillGroup()

    def enableAddToGroupButton(self):
        if(self.list.selectedItems() and self.groupList.selectedItems()):
            self.buttonGroupAppAdd.setEnabled(True)
        else:
            self.buttonGroupAppAdd.setEnabled(False)

    def deleteGroup(self, groupName):
        fg = open('../data/groups.data' , 'r')
        group_list = fg.readlines()
        fg.close()
        fg = open('../data/appGroups.data', 'r')
        groupApps_list = fg.readlines()
        fg.close()

        insertGroups = []
        insertGroupApps = []

        for group in group_list:
            if ( groupName != group.split("\n")[0] ):
                insertGroups.append(group)
        for groupApp in groupApps_list:
            if ( groupName != groupApp.split("|")[0] ):
                insertGroupApps.append(groupApp)

        fw = open('../data/groups.data' , 'w')
        fw.writelines(insertGroups)
        fw.close()
        fw = open('../data/appGroups.data', 'w')
        fw.writelines(insertGroupApps)
        fw.close()

        for i in range(self.groupList.count()):
            gapp = self.groupList.item(i)
            if(self.groupList.itemWidget(gapp).getName() == groupName):
                indexToDelete = i

        self.groupList.takeItem(indexToDelete)

    def createConnectionModel(self):
        model = QStandardItemModel(0, 3, self)
        model.setHeaderData(self.IP, Qt.Horizontal, "IP address")
        model.setHeaderData(self.HOSTNAME, Qt.Horizontal, "Hostname")
        model.setHeaderData(self.STATUS, Qt.Horizontal, "Status")
        return model

    def addConnection(self,model, ip, hostname, status):
        self.incomingConnectionsModel.insertRow(0)
        self.incomingConnectionsModel.setData(self.incomingConnectionsModel.index(0, self.IP), ip)
        self.incomingConnectionsModel.setData(self.incomingConnectionsModel.index(0, self.HOSTNAME), hostname)
        self.incomingConnectionsModel.setData(self.incomingConnectionsModel.index(0, self.STATUS), status)

    def addAllConnections(self, incomingConnections):
        for incomingConnection in incomingConnections:
            self.addConnection(self.incomingConnectionsModel, incomingConnection, incomingConnections[incomingConnection]['Hostname'], incomingConnections[incomingConnection]['Status'])

    def deleteAllConnections(self):
        rangeModel = range(self.incomingConnectionsModel.rowCount())
        for i in rangeModel:
            self.incomingConnectionsModel.removeRow(self.incomingConnectionsList.indexAt(QtCore.QPoint(i,0)).row())

    def resetConnectionsList(self, incomingConnections):
        self.deleteAllConnections()
        self.addAllConnections(incomingConnections)

    def manageConnectionsList(self):
        while(self.appExit is False):
            time.sleep(3)
            self.incomingConnectionSig.emit(NetworkScan.GetHostLan())

    def getActionsList(self):
        fr = open('../data/appsActions.data', 'r')
        actions = fr.readlines()
        fr.close()

        list = []

        for action in actions:
            line = action.split(',')
            list.append({'processName':line[0], 'actionType':line[1], 'durationType':line[2], 'durationTime':line[3]})

        return list

    def secureForeverSecuredApps(self):
        actions = self.getActionsList()

        for action in actions:
            if ( (action['actionType'] == "security") and (int(action['durationType']) == 2) ):
                for i in range(self.list.count()):
                    wapp = self.list.item(i)
                    app = self.list.itemWidget(wapp)
                    try:
                        if(app.getProcessName() == action['processName'] and app.getSecured() is False):
                            app.manageVPN(action['durationType'], action['durationTime'])
                    except(AttributeError):
                        pass


    def closeEvent(self, event):
        if(True):
            try:
                self.OpenVpnThread.do_run = False
                self.OpenVpnThread.join()
            except:
                pass
            for i in range(self.list.count()):
                wapp = self.list.item(i)
                self.list.itemWidget(wapp).clean()

            self.appExit = True
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())
